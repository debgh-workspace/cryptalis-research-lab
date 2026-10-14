"""Frozen C10 persistent-process timing harness. Coordinator wrapper only.

No profiling, query instrumentation, filtering, retries, or source swapping is
active during the timed samples. Every variant has its own source-pinned process.
"""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import select as pipe_select
import signal
import subprocess
import sys
import time
from contextlib import ExitStack
from uuid import UUID
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
MANIFEST_HASH = 'eff60dbe9dc7b2c428f4623f8a945312e2dbdc54219a53594f19685ab6e57d6b'
CANDIDATE_CF1_SHA256 = '8c6a3ad82865734200424b6ab949ef46c38540561be20b743188073fbf593fb4'
PURE_TEST_SHA256 = 'c0462824c21b7a3ed28007fd609d84d2d69d4961fe63e3109b216014a763065e'
WORKLOADS = ('in20-miss-ids', 'in20-hot-ids', 'in20-hot-text', 'equality-hot-text', 'point-text')
VARIANTS = ('native', 'original', 'candidate')
MISS = tuple('C8-missing-%d' % i for i in range(20))
HOT = ('exact', '雪😀') + tuple('C8-missing-%d' % i for i in range(18))
COUNTS = dict(zip(WORKLOADS, (0, 286, 286, 143, 1)))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_snapshot(root, variant, manifest, candidate_hash):
    assert digest(manifest) == MANIFEST_HASH
    assert candidate_hash == CANDIDATE_CF1_SHA256
    expected = json.loads(Path(manifest).read_text())
    assert len(expected) == 208
    if variant == 'candidate':
        assert candidate_hash != expected['src/cryptalis/crypto/cf1.py']
        expected['src/cryptalis/crypto/cf1.py'] = candidate_hash
        assert digest(root / 'experiments/test_term_literal_framing.py') == PURE_TEST_SHA256
        assert digest(root / 'experiments/c10_baseline_cf1.py') == 'd74abd2558023bf5ce1598fba0b61bb27198623dc56fb94ace24753531705278'
    assert {str(path.relative_to(root)) for path in (root / 'src').rglob('*') if path.is_file() and '__pycache__' not in path.parts} == {name for name in expected if name.startswith('src/')}
    actual = {name: digest(root / name) for name in expected}
    assert actual == expected
    return {'files': actual, 'baseline_manifest_sha256': MANIFEST_HASH}


def dependencies():
    result = {'python': platform.python_version(), 'executable': sys.executable, 'packages': {}}
    for name in ('SQLAlchemy', 'psycopg', 'cryptography', 'greenlet'):
        distribution = importlib.metadata.distribution(name)
        records = [f for f in distribution.files or () if str(f).endswith('.dist-info/RECORD')]
        assert len(records) == 1
        result['packages'][name] = {'version': distribution.version,
            'record_sha256': digest(distribution.locate_file(records[0]))}
    assert result['packages']['SQLAlchemy']['version'] in ('2.0.51', '2.1.3')
    return result


def clocks():
    return {'wall': time.perf_counter_ns(),
            'raw': time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW),
            'process': time.process_time_ns(), 'thread': time.thread_time_ns()}


def resource_snapshot():
    value = resource.getrusage(resource.RUSAGE_SELF)
    return {'user_cpu_s': value.ru_utime, 'system_cpu_s': value.ru_stime,
            'voluntary_context_switches': value.ru_nvcsw,
            'involuntary_context_switches': value.ru_nivcsw,
            'maxrss_kib_process_highwater': value.ru_maxrss}


def resource_deltas(before, after):
    return {name: after[name] - before[name] for name in before}


def parent_load():
    try:
        return list(os.getloadavg())
    except OSError:
        return None


def safe_error(error):
    original = getattr(error, 'orig', error)
    return {'type': type(error).__name__, 'original_type': type(original).__name__,
            'sqlstate': getattr(original, 'sqlstate', None), 'code': getattr(original, 'code', None)}


def row_digest(rows):
    return hashlib.sha256(json.dumps([[str(row[0]), *row[1:]] for row in rows],
        ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def emit(value):
    print(json.dumps(value, ensure_ascii=False, separators=(',', ':')), flush=True)


def protect_worker_parent(expected_parent):
    """Linux lab containment: an orphan worker must die with its coordinator."""
    import ctypes
    assert sys.platform.startswith('linux')
    libc = ctypes.CDLL(None, use_errno=True)
    # PR_SET_PDEATHSIG; SIGKILL also applies while a worker is stuck in native IO.
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), 'Cannot establish worker parent-death containment')
    if os.getppid() != expected_parent:
        os._exit(1)


def read_worker_receipt(stream, buffered=b'', timeout=180):
    deadline = time.monotonic() + timeout
    while b'\n' not in buffered:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Timing worker receipt deadline exceeded')
        ready, _, _ = pipe_select.select([stream.fileno()], [], [], remaining)
        if not ready:
            raise TimeoutError('Timing worker receipt deadline exceeded')
        chunk = os.read(stream.fileno(), 65536)
        if not chunk:
            raise RuntimeError('Timing worker terminated without a complete receipt')
        buffered += chunk
    line, buffered = buffered.split(b'\n', 1)
    return json.loads(line), buffered


def terminate_worker_group(process, grace=10):
    """Stop only this harness-owned process group; record any forced cleanup."""
    stages = []
    for signum in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, signum)
        except ProcessLookupError:
            pass
        stages.append(signum.name)
        try:
            process.wait(timeout=grace)
            return stages
        except subprocess.TimeoutExpired:
            if signum == signal.SIGKILL:
                raise
    return stages


def close_worker(variant, process, send, receive, metadata, *,
                 close_timeout=60, exit_timeout=60, kill_grace=10):
    """One worker's failure must not prevent cleanup of the remaining workers."""
    try:
        if process.poll() is None:
            try:
                send(variant, {'command': 'close'})
                response = receive(variant, timeout=close_timeout)
                metadata.setdefault('closure', {})[variant] = response
            except BaseException as failure:
                metadata.setdefault('closure_failures', {})[variant] = safe_error(failure)
            try:
                process.stdin.close()
            except BaseException as failure:
                metadata.setdefault('pipe_close_failures', {})[variant] = safe_error(failure)
            try:
                process.wait(timeout=exit_timeout)
            except subprocess.TimeoutExpired:
                metadata.setdefault('forced_termination', {})[variant] = terminate_worker_group(process, kill_grace)
    except BaseException as failure:
        metadata.setdefault('cleanup_failures', {})[variant] = safe_error(failure)
    finally:
        metadata.setdefault('worker_exit_codes', {})[variant] = process.poll()
        for stream in (process.stdout, process.stdin):
            try:
                stream.close()
            except BaseException as failure:
                metadata.setdefault('pipe_close_failures', {})[variant] = safe_error(failure)


def worker(root, variant, manifest, candidate_hash):
    # Configure source isolation before importing any project or fixture module.
    sys.path[:0] = [str(root / 'src'), str(root / 'tests')]
    import gc
    import psycopg
    from psycopg import sql
    from sqlalchemy import Text, bindparam, event, select
    from sqlalchemy.orm import sessionmaker
    import cryptalis.sqlalchemy as adapter
    import cryptalis.crypto.cf1 as cf1
    from cryptalis.crypto.keys import PreparedKeys
    from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
    from test_migration import TABLE_ID, keys, publish, run
    assert Path(adapter.__file__).resolve() == root / 'src/cryptalis/sqlalchemy.py'
    before = source_snapshot(root, variant, manifest, candidate_hash)
    assert gc.isenabled(), 'Ordinary enabled GC is required'
    assert sys.getprofile() is None and sys.gettrace() is None
    gc_state = (gc.isenabled(), gc.get_threshold())
    closing = False
    with ExitStack() as stack:
        app = stack.enter_context(single_tenant_public_cascade_application(
            rows=1000, unique=False, public_table=False))
        if variant != 'native':
            run(app, chunk_size=256)
            publish(app)
        with app.owner.begin() as connection:
            connection.exec_driver_sql(f'ANALYZE "{app.schema}".customer')
        if variant == 'native':
            session = stack.enter_context(sessionmaker(app.runtime)())
        else:
            ring = keys(TABLE_ID)
            factory = adapter.attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                keys=ring, deployment=(app.plan, app.pin))
            session = stack.enter_context(factory(tenant_id=TABLE_ID))
        C = app.Customer
        queries, parameters = {}, {}
        for workload in WORKLOADS:
            columns = (C.id,) if workload.endswith('-ids') else (C.id, C.name)
            if workload.startswith('in20'):
                predicate = C.name.in_(bindparam('needles', expanding=True, type_=Text()))
                parameters[workload] = {'needles': MISS if workload == 'in20-miss-ids' else HOT}
            elif workload == 'equality-hot-text':
                predicate = C.name == bindparam('needle', type_=Text())
                parameters[workload] = {'needle': 'exact'}
            else:
                predicate = C.id == UUID(int=600)
                parameters[workload] = {}
            queries[workload] = select(*columns).where(predicate).order_by(C.id)
        expected = {}
        def execute(workload, params=None):
            result = session.execute(queries[workload], parameters[workload] if params is None else params)
            try:
                return result.all()
            finally:
                result.close()
        emit({'event': 'fixture_ready', 'variant': variant, 'schema': app.schema,
              'source_before': before, 'dependencies': dependencies(),
              'gc': {'enabled': gc_state[0], 'threshold': gc_state[1]}})
        for line in sys.stdin:
            command = json.loads(line)
            if command['command'] == 'oracle':
                schema = command['native_schema']
                # End the read-only oracle transaction and close its handle
                # before any gates/timing or teardown of another child's schema.
                with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as driver:
                    for workload in WORKLOADS:
                        columns = sql.SQL('id') if workload.endswith('-ids') else sql.SQL('id, name')
                        if workload.startswith('in20'):
                            predicate = sql.SQL('name = ANY(%s::text[])')
                            value = list(MISS if workload == 'in20-miss-ids' else HOT)
                        elif workload == 'equality-hot-text':
                            predicate, value = sql.SQL('name = %s::text'), 'exact'
                        else:
                            predicate, value = sql.SQL('id = %s'), UUID(int=600)
                        query = sql.SQL('SELECT {} FROM {}.customer WHERE {} ORDER BY id').format(
                            columns, sql.Identifier(schema), predicate)
                        expected[workload] = driver.execute(query, (value,)).fetchall()
                        assert len(expected[workload]) == COUNTS[workload]
                assert driver.closed
                emit({'event': 'oracle', 'variant': variant, 'driver_connection_closed': True,
                      'hashes': {name: row_digest(value) for name, value in expected.items()}})
            elif command['command'] == 'gate':
                assert expected
                gate = []
                original_derive = cf1._derive
                calls, statements = [], []
                primitive_counts = {}
                originals = {'term': cf1._term, 'tuple_bytes': cf1.tuple_bytes,
                             'open_text': adapter.open_text, 'resolve': PreparedKeys._resolve}
                def counted(name, original):
                    def call(*args, **kwargs):
                        primitive_counts[name] = primitive_counts.get(name, 0) + 1
                        return original(*args, **kwargs)
                    return call
                def observed(material, info):
                    calls.append(material.context.purpose)
                    return original_derive(material, info)
                def cursor(connection, raw, statement, parameters, context, many):
                    statements.append(statement)
                cf1._derive = observed
                cf1._term = counted('term', originals['term'])
                cf1.tuple_bytes = counted('tuple_bytes', originals['tuple_bytes'])
                adapter.open_text = counted('open_text', originals['open_text'])
                PreparedKeys._resolve = counted('resolve', originals['resolve'])
                event.listen(app.runtime, 'before_cursor_execute', cursor)
                try:
                    for workload in (*WORKLOADS, 'list20-control'):
                        calls.clear(); statements.clear(); primitive_counts.clear()
                        actual_workload = 'in20-miss-ids' if workload == 'list20-control' else workload
                        params = {'needles': list(MISS)} if workload == 'list20-control' else None
                        value = execute(actual_workload, params)
                        assert value == expected[actual_workload] and len(statements) == 1
                        array_route = False
                        assert ('ANY' in statements[0]) == array_route
                        nonnull = sum(row[1] is not None for row in value) if actual_workload.endswith('-text') else 0
                        query_terms = 20 if workload.startswith('in20') or workload == 'list20-control' else 1 if workload == 'equality-hot-text' else 0
                        predicted_search = query_terms + nonnull
                        predicted = {'search': predicted_search, 'payload': nonnull} if variant != 'native' else {'search': 0, 'payload': 0}
                        actual = {'search': calls.count('search'), 'payload': calls.count('payload')}
                        assert actual == predicted and len(calls) == sum(actual.values())
                        predicted_primitives = {'term': query_terms + nonnull, 'resolve': 2 * query_terms + 4 * nonnull,
                            'open_text': nonnull, 'tuple_bytes': 3 * query_terms + 6 * nonnull - (2 * (query_terms + nonnull) if variant == 'candidate' else 0)}
                        if variant == 'native':
                            predicted_primitives = {name: 0 for name in predicted_primitives}
                        actual_primitives = {name: primitive_counts.get(name, 0) for name in predicted_primitives}
                        assert actual_primitives == predicted_primitives, (workload, actual_primitives, predicted_primitives)
                        assert not array_route and 'ANY' not in statements[0]
                        gate.append({'workload': workload, 'array_route': array_route,
                                     'derivations': actual, 'primitives': actual_primitives, 'expected_primitives': predicted_primitives, 'row_count': len(value), 'row_check': True})
                finally:
                    cf1._derive = original_derive
                    cf1._term = originals['term']
                    cf1.tuple_bytes = originals['tuple_bytes']
                    adapter.open_text = originals['open_text']
                    PreparedKeys._resolve = originals['resolve']
                    event.remove(app.runtime, 'before_cursor_execute', cursor)
                assert cf1._derive is original_derive
                assert (cf1._term, cf1.tuple_bytes, adapter.open_text, PreparedKeys._resolve) == tuple(originals.values())
                assert not event.contains(app.runtime, 'before_cursor_execute', cursor)
                emit({'event': 'gate', 'variant': variant, 'observations': gate,
                      'instrumentation_removed': True})
            elif command['command'] == 'batch':
                assert expected and gc_state == (gc.isenabled(), gc.get_threshold())
                workload, block = command['workload'], command['block']
                assert workload in WORKLOADS and 0 <= block < 7
                resources_before = resource_snapshot()
                for sample in range(50):
                    # Start/end include execute, full fetch and close. Equality,
                    # serialization and receipt IO occur only after end clocks.
                    start = clocks()
                    try:
                        result = execute(workload)
                    except BaseException as failure:
                        end = clocks()
                        emit({'event': 'sample', 'status': 'error', 'variant': variant,
                              'workload': workload, 'block': block, 'sample': sample,
                              'phase': 'warmup' if sample < 10 else 'measured',
                              'start_ns': start, 'end_ns': end,
                              'elapsed_ns': {name: end[name] - start[name] for name in start},
                              'error': safe_error(failure)})
                        return
                    end = clocks()
                    result = [tuple(row) for row in result]
                    row_check = result == expected[workload]
                    emit({'event': 'sample', 'status': 'ok' if row_check else 'row-mismatch',
                          'variant': variant, 'workload': workload, 'block': block, 'sample': sample,
                          'phase': 'warmup' if sample < 10 else 'measured',
                          'start_ns': start, 'end_ns': end,
                          'elapsed_ns': {name: end[name] - start[name] for name in start},
                          'row_check': row_check, 'rows': len(result), 'row_sha256': row_digest(result)})
                    if not row_check:
                        return
                resources_after = resource_snapshot()
                emit({'event': 'batch_complete', 'variant': variant, 'workload': workload, 'block': block,
                      'resources_before': resources_before, 'resources_after': resources_after,
                      'resource_deltas': resource_deltas(resources_before, resources_after)})
            elif command['command'] == 'close':
                closing = True
                break
            else:
                raise ValueError('Unknown harness command')
    # Only acknowledge closure after session rollback/close and actual fixture
    # schema teardown have completed, then recheck source stability.
    if not closing:
        raise RuntimeError('Coordinator input ended before explicit shutdown')
    after = source_snapshot(root, variant, manifest, candidate_hash)
    assert after == before
    emit({'event': 'closed', 'variant': variant, 'source_after': after,
          'fixture_teardown_completed': True})


def safety_receipts(configured, collection_hash):
    assert set(configured) == {'2.0.51', '2.1.3'}
    collection_path = ROOT / 'experiments/C10_SAFETY_COLLECTION.json'
    assert digest(collection_path) == collection_hash
    collection = json.loads(collection_path.read_text())
    assert set(collection) == {'2.0.51', '2.1.3'}
    receipts = {}
    for version, groups in configured.items():
        assert set(groups) == {'affected', 'supplemental'}
        assert set(collection[version]) == set(groups)
        receipts[version] = {}
        all_names = []
        for group, receipt in groups.items():
            assert set(receipt) == {'path', 'sha256'}
            path = Path(receipt['path']).resolve()
            assert digest(path) == receipt['sha256']
            document = ET.parse(path).getroot()
            assert not any(node.tag in ('failure', 'error', 'skipped') for node in document.iter())
            for node in document.iter():
                if node.tag in ('testsuite', 'testsuites'):
                    assert all(int(node.attrib.get(kind, '0')) == 0 for kind in ('failures', 'errors', 'skipped', 'disabled'))
            cases = list(document.iter('testcase'))
            names = [(case.attrib['classname'], case.attrib['name']) for case in cases]
            expected = [tuple(case) for case in collection[version][group]]
            assert len(expected) == len(set(expected)) and expected
            assert sorted(names) == sorted(expected)
            assert all(case.find(kind) is None for case in cases for kind in ('failure', 'error', 'skipped'))
            if group == 'affected':
                assert len(cases) == 213
                required = {'test_cf1', 'test_cf1_backend_failures', 'test_key_lease_renewal',
                    'test_payload_rotation_preparation', 'test_sqlalchemy_search', 'test_sqlalchemy_thread_isolation'}
                assert {cls.split('.')[-1] for cls, _ in names} == required
            all_names.extend(names)
            receipts[version][group] = {'path': str(path), 'sha256': digest(path), 'cases_passed': len(cases)}
        assert any(name == 'test_c10_source_isolated_postgres_native_oracle' for _, name in all_names)
        for required in ('test_async_cancellation_during_key_preparation_has_no_database_effect',
                         'test_async_database_cancellation_preserves_rollback_and_recovery',
                         'test_real_task_cancellation_releases_transaction_before_session_close',
                         'test_tuple_wire_bytes_match_independent_writer',
                         'test_tuple_never_implicitly_converts_parts'):
            assert any(name.split('[')[0] == required for _, name in all_names)
        collection_module = any(cls.split('.')[-1] == 'test_sqlalchemy_async_collection_methods' for cls, _ in all_names)
        assert collection_module == (version == '2.1.3')
        receipts[version]['whole_compatibility_gate'] = 'OPEN; unrelated native defaults/cache-order and other qualification gaps remain'
    return receipts


def pure_receipts(configured):
    assert set(configured) == {'2.0.51', '2.1.3'}
    receipts = {}
    for version, receipt in configured.items():
        assert set(receipt) == {'path', 'sha256'}
        path = Path(receipt['path']).resolve()
        assert digest(path) == receipt['sha256']
        result = json.loads(path.read_text())
        assert result['sqlalchemy'] == version and result['exit_code'] == 0
        assert result['counts'] == {'passed': 55} and result['failed_nodes'] == []
        assert result['source_unchanged'] is True
        assert result['source_test_sha256']['src/cryptalis/crypto/cf1.py'] == CANDIDATE_CF1_SHA256
        assert result['source_test_sha256']['experiments/test_term_literal_framing.py'] == PURE_TEST_SHA256
        assert Path(result['cf1_import_origin']).resolve() == ROOT / 'src/cryptalis/crypto/cf1.py'
        receipts[version] = {'path': str(path), 'sha256': digest(path), 'cases_passed': 55}
    return receipts


def test_c10_frozen_timing_protocol():
    # The parent must have entered via the unchanged fresh-two-role wrapper.
    assert '_cryptalis_test_preflight' in sys.modules
    protocol = ROOT / 'experiments/C10_TIMING_PROTOCOL.md'
    # Nonsecret root execution controls; this file cannot replace credential
    # authorization or the unchanged fresh-preflight admission above.
    control_path = ROOT / 'experiments/C10_COORDINATOR_APPROVAL.json'
    control = json.loads(control_path.read_text())
    assert set(control) == {'coordinator_approved', 'diagnostic_only',
        'whole_compatibility_gate', 'protocol_sha256', 'harness_sha256',
        'arithmetic_sha256', 'baseline_root', 'candidate_cf1_sha256', 'safety_collection_sha256', 'correctness_harness_sha256', 'cell_output_directories', 'safety_junit', 'pure_receipts'}
    assert control['coordinator_approved'] is True and control['diagnostic_only'] is True
    assert control['whole_compatibility_gate'] == 'OPEN'
    approval = control['protocol_sha256']
    assert approval == digest(protocol), 'Exact coordinator protocol approval is required'
    assert control['harness_sha256'] == digest(HERE)
    assert control['arithmetic_sha256'] == digest(HERE.with_name('c10_timing_arithmetic.py'))
    import sqlalchemy
    assert sqlalchemy.__version__ in ('2.0.51', '2.1.3')
    assert set(control['cell_output_directories']) == {'2.0.51', '2.1.3'}
    baseline = Path(control['baseline_root']).resolve()
    output = Path(control['cell_output_directories'][sqlalchemy.__version__]).resolve()
    assert control['correctness_harness_sha256'] == digest(HERE.with_name('test_c10_postgres_gates.py'))
    safety = safety_receipts(control['safety_junit'], control['safety_collection_sha256'])
    pure = pure_receipts(control['pure_receipts'])
    output.mkdir(parents=True, exist_ok=False)
    manifest = ROOT / 'experiments/C10_SOURCE_MANIFEST.json'
    assert digest(manifest) == MANIFEST_HASH
    import importlib.util
    helper_path = HERE.with_name('c10_timing_arithmetic.py')
    spec = importlib.util.spec_from_file_location('_c10_fixed_arithmetic', helper_path)
    arithmetic = importlib.util.module_from_spec(spec); spec.loader.exec_module(arithmetic)
    observations, workers, metadata = [], {}, {'protocol_sha256': approval, 'harness_sha256': digest(HERE),
        'arithmetic_sha256': digest(helper_path), 'status': 'running', 'started_utc_ns': time.time_ns(),
        'variant_metadata': {}, 'oracles': {}, 'untimed_gates': {}, 'failure': None,
        'safety_receipts': safety, 'pure_receipts': pure, 'experiment_scope': 'DIAGNOSTIC ONLY: fixed-literal term-framing, explicit supplied values',
        'whole_compatibility_gate': 'OPEN: preexisting native default omission/cache-order gap',
        'product_qualified': False, 'coordinator_control_sha256': digest(control_path),
        'batch_resources': [], 'candidate_cf1_sha256': control['candidate_cf1_sha256'],
        'source_manifest_sha256': MANIFEST_HASH,
        'contention_interpretation': 'Outside-sample batch observations include receipt IO; not causal proof, never used to filter samples'}
    def save_metadata():
        (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    read_buffers = {}
    def receive(variant, timeout=180):
        result, read_buffers[variant] = read_worker_receipt(
            workers[variant].stdout, read_buffers.get(variant, b''), timeout)
        if result.get('event') == 'worker_error':
            metadata.setdefault('worker_errors', {})[variant] = result
            save_metadata()
            raise AssertionError('Worker error; safe details retained in metadata')
        return result
    def send(variant, command):
        workers[variant].stdin.write(json.dumps(command) + '\n'); workers[variant].stdin.flush()
    with ExitStack() as cleanup, (output / 'samples.jsonl').open('x') as raw:
        try:
            for variant in VARIANTS:
                source = ROOT if variant == 'candidate' else baseline
                env = dict(os.environ)
                env['PYTHONDONTWRITEBYTECODE'] = '1'
                env['PYTHONPATH'] = os.pathsep.join((str(source / 'src'), str(source / 'tests')))
                stderr = cleanup.enter_context((output / (variant + '-stderr.log')).open('x'))
                process = subprocess.Popen([sys.executable, str(HERE), '--c10-worker', str(source), variant, str(manifest), control['candidate_cf1_sha256'], str(os.getpid())],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True,
                    env=env, cwd=source, bufsize=1, start_new_session=True)
                workers[variant] = process
                metadata['variant_metadata'][variant] = receive(variant, timeout=300)
                assert metadata['variant_metadata'][variant]['event'] == 'fixture_ready'
                save_metadata()
            assert len({metadata['variant_metadata'][variant]['dependencies']['packages']['SQLAlchemy']['version'] for variant in VARIANTS}) == 1
            native_schema = metadata['variant_metadata']['native']['schema']
            for variant in VARIANTS:
                send(variant, {'command': 'oracle', 'native_schema': native_schema})
                metadata['oracles'][variant] = receive(variant)
                assert metadata['oracles'][variant]['event'] == 'oracle'
                assert metadata['oracles'][variant]['driver_connection_closed'] is True
            assert metadata['oracles']['native']['hashes'] == metadata['oracles']['original']['hashes'] == metadata['oracles']['candidate']['hashes']
            metadata['all_oracle_transactions_closed_before_gates'] = True
            for variant in VARIANTS:
                send(variant, {'command': 'gate'})
                metadata['untimed_gates'][variant] = receive(variant)
                assert metadata['untimed_gates'][variant]['event'] == 'gate'
            save_metadata()
            for block in range(7):
                order = VARIANTS if block % 2 == 0 else VARIANTS[::-1]
                for workload in WORKLOADS:
                    for variant in order:
                        load_before = parent_load()
                        send(variant, {'command': 'batch', 'workload': workload, 'block': block})
                        for sample in range(50):
                            receipt = receive(variant)
                            receipt['sequence'] = len(observations)
                            receipt['variant_order'] = list(order)
                            raw.write(json.dumps(receipt, separators=(',', ':')) + '\n'); raw.flush()
                            observations.append(receipt)
                            assert receipt['event'] == 'sample' and receipt['status'] == 'ok'
                            assert (receipt['variant'], receipt['workload'], receipt['block'], receipt['sample']) == (variant, workload, block, sample)
                            assert receipt['row_sha256'] == metadata['oracles']['native']['hashes'][workload]
                        completion = receive(variant)
                        assert (completion['event'], completion['variant'], completion['workload'], completion['block']) == ('batch_complete', variant, workload, block)
                        metadata['batch_resources'].append({**completion,
                            'parent_load_before': load_before, 'parent_load_after': parent_load()})
                        save_metadata()
            summary = arithmetic.summarize(observations)
            (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
            metadata['status'] = 'sampling-complete'
        except BaseException as failure:
            metadata['status'], metadata['failure'] = 'failed', safe_error(failure)
            raise
        finally:
            try:
                raw.flush(); os.fsync(raw.fileno())
            except BaseException as failure:
                metadata['receipt_flush_failure'] = safe_error(failure)
                metadata['status'] = 'failed-receipt-flush'
            for variant, process in workers.items():
                close_worker(variant, process, send, receive, metadata)
            if metadata['status'] == 'sampling-complete':
                closed = metadata.get('closure', {})
                clean = (set(closed) == set(VARIANTS)
                    and all(item.get('event') == 'closed' and item.get('fixture_teardown_completed') is True for item in closed.values())
                    and all(code == 0 for code in metadata['worker_exit_codes'].values())
                    and not any(metadata.get(name) for name in ('closure_failures', 'cleanup_failures', 'forced_termination', 'pipe_close_failures')))
                metadata['status'] = 'complete' if clean else 'failed-source-or-worker-closure'
            metadata['observations_retained'] = len(observations)
            metadata['ended_utc_ns'] = time.time_ns()
            save_metadata()
    assert metadata['status'] == 'complete' and all(code == 0 for code in metadata['worker_exit_codes'].values())
    assert set(metadata.get('closure', {})) == set(VARIANTS)
    assert all(item['event'] == 'closed' for item in metadata['closure'].values())
    # Performance PASS/FAIL is a retained result, not grounds for rerunning pytest.


if __name__ == '__main__':
    assert len(sys.argv) == 7 and sys.argv[1] == '--c10-worker'
    protect_worker_parent(int(sys.argv[6]))
    try:
        worker(Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4]).resolve(), sys.argv[5])
    except BaseException as failure:
        emit({'event': 'worker_error', 'error': safe_error(failure)})
        raise SystemExit(1)

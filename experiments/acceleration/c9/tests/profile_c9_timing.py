"""Frozen C9 persistent-process timing harness. Coordinator wrapper only.

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
import subprocess
import sys
import time
from contextlib import ExitStack
from uuid import UUID
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
MANIFEST_HASH = 'aba658622e884084762e09be61aed54c7a1023af37d332af9f5143aa5e358688'
CANDIDATE_FILES = {
    'src/cryptalis/_sqlalchemy_search.py': '9d3564b80470bb98383af461807969952adc8eb2a82217ec3681c6928d7a1391',
    'src/cryptalis/crypto/cf1.py': '3d34b066e8e2b5983fcc5c1180226e666a7ba0a5fcacb8888ce7adfa66e73ed3',
}
WORKLOADS = ('in20-miss-ids', 'in20-hot-ids', 'in20-hot-text', 'equality-hot-text', 'point-text')
VARIANTS = ('native', 'original', 'candidate')
MISS = tuple('C8-missing-%d' % i for i in range(20))
HOT = ('exact', '雪😀') + tuple('C8-missing-%d' % i for i in range(18))
COUNTS = dict(zip(WORKLOADS, (0, 286, 286, 143, 1)))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_snapshot(root, variant, manifest):
    assert digest(manifest) == MANIFEST_HASH
    expected = json.loads(Path(manifest).read_text())
    assert len(expected) == 201
    if variant == 'candidate':
        expected.update(CANDIDATE_FILES)
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


def worker(root, variant, manifest):
    # Configure source isolation before importing any project or fixture module.
    sys.path[:0] = [str(root / 'src'), str(root / 'tests')]
    import gc
    import psycopg
    from psycopg import sql
    from sqlalchemy import Text, bindparam, event, select
    from sqlalchemy.orm import sessionmaker
    import cryptalis.sqlalchemy as adapter
    import cryptalis.crypto.cf1 as cf1
    from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
    from test_migration import TABLE_ID, keys, publish, run
    assert Path(adapter.__file__).resolve() == root / 'src/cryptalis/sqlalchemy.py'
    before = source_snapshot(root, variant, manifest)
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
                def observed(material, info):
                    calls.append(material.context.purpose)
                    return original_derive(material, info)
                def cursor(connection, raw, statement, parameters, context, many):
                    statements.append(statement)
                cf1._derive = observed
                event.listen(app.runtime, 'before_cursor_execute', cursor)
                try:
                    for workload in (*WORKLOADS, 'list20-control'):
                        calls.clear(); statements.clear()
                        actual_workload = 'in20-miss-ids' if workload == 'list20-control' else workload
                        params = {'needles': list(MISS)} if workload == 'list20-control' else None
                        value = execute(actual_workload, params)
                        assert value == expected[actual_workload] and len(statements) == 1
                        array_route = variant == 'candidate' and workload.startswith('in20')
                        assert ('ANY' in statements[0]) == array_route
                        nonnull = sum(row[1] is not None for row in value) if actual_workload.endswith('-text') else 0
                        query_terms = 20 if workload.startswith('in20') or workload == 'list20-control' else 1 if workload == 'equality-hot-text' else 0
                        predicted_search = (1 if array_route else query_terms) + nonnull
                        predicted = {'search': predicted_search, 'payload': nonnull} if variant != 'native' else {'search': 0, 'payload': 0}
                        actual = {'search': calls.count('search'), 'payload': calls.count('payload')}
                        assert actual == predicted and len(calls) == sum(actual.values())
                        gate.append({'workload': workload, 'array_route': array_route,
                                     'derivations': actual, 'row_count': len(value), 'row_check': True})
                finally:
                    cf1._derive = original_derive
                    event.remove(app.runtime, 'before_cursor_execute', cursor)
                assert cf1._derive is original_derive
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
    after = source_snapshot(root, variant, manifest)
    assert after == before
    emit({'event': 'closed', 'variant': variant, 'source_after': after,
          'fixture_teardown_completed': True})


def safety_receipts(configured):
    assert set(configured) == {'2.0.51', '2.1.3'}
    expected = {
        'test_c9_gate4_tuple_admission_and_fallback_controls[' + case + ']'
        for case in ('missing', 'required-default', 'supplied-tuple', 'not-in',
                     'equality', 'unsupported-expression', 'custom-codec', 'ambiguous')}
    expected.update('test_c9_gate4_tuple_bind_revalidates_prepared_context[' + case + ']'
                    for case in ('pid', 'tenant', 'lease'))
    expected.update(('test_c9_gate4_final_cursor_policy_check_after_tuple_processing',
                     'test_c9_gate4_returned_payload_still_resolves_keys_after_tuple_query',
                     'test_c9_gate5_native_driver_invalid_text_failure'))
    expected.update('test_c9_gate5_custom_generic_plans_and_driver_adaptation[' + shape + '-' + mode + ']'
        for shape in ('hot20', 'mixed-null20', 'all-null20')
        for mode in ('force_custom_plan', 'force_generic_plan'))
    assert len(expected) == 20
    receipts = {}
    for version, receipt in configured.items():
        assert set(receipt) == {'path', 'sha256'}
        path = Path(receipt['path']).resolve()
        assert digest(path) == receipt['sha256']
        cases = list(ET.parse(path).getroot().iter('testcase'))
        assert len(cases) == 20 and {case.attrib['name'] for case in cases} == expected
        assert all(case.find(kind) is None for case in cases for kind in ('failure', 'error', 'skipped'))
        receipts[version] = {'path': str(path), 'sha256': digest(path), 'provided_input_cases_passed': 20,
                             'whole_21_case_gate': 'OPEN; default omission/cache-order gap excluded explicitly'}
    return receipts


def test_c9_frozen_timing_protocol():
    # The parent must have entered via the unchanged fresh-two-role wrapper.
    assert '_cryptalis_test_preflight' in sys.modules
    protocol = ROOT / 'experiments/C9_TIMING_PROTOCOL.md'
    # Nonsecret root execution controls; this file cannot replace credential
    # authorization or the unchanged fresh-preflight admission above.
    control_path = ROOT / 'experiments/C9_COORDINATOR_APPROVAL.json'
    control = json.loads(control_path.read_text())
    assert set(control) == {'coordinator_approved', 'diagnostic_only',
        'whole_compatibility_gate', 'protocol_sha256', 'harness_sha256',
        'arithmetic_sha256', 'baseline_root', 'cell_output_directories', 'safety_junit'}
    assert control['coordinator_approved'] is True and control['diagnostic_only'] is True
    assert control['whole_compatibility_gate'] == 'OPEN'
    approval = control['protocol_sha256']
    assert approval == digest(protocol), 'Exact coordinator protocol approval is required'
    assert control['harness_sha256'] == digest(HERE)
    assert control['arithmetic_sha256'] == digest(HERE.with_name('c9_timing_arithmetic.py'))
    import sqlalchemy
    assert sqlalchemy.__version__ in ('2.0.51', '2.1.3')
    assert set(control['cell_output_directories']) == {'2.0.51', '2.1.3'}
    baseline = Path(control['baseline_root']).resolve()
    output = Path(control['cell_output_directories'][sqlalchemy.__version__]).resolve()
    safety = safety_receipts(control['safety_junit'])
    output.mkdir(parents=True, exist_ok=False)
    manifest = ROOT / 'experiments/C9_SOURCE_MANIFEST.json'
    assert digest(manifest) == MANIFEST_HASH
    import importlib.util
    helper_path = HERE.with_name('c9_timing_arithmetic.py')
    spec = importlib.util.spec_from_file_location('_c9_fixed_arithmetic', helper_path)
    arithmetic = importlib.util.module_from_spec(spec); spec.loader.exec_module(arithmetic)
    observations, workers, metadata = [], {}, {'protocol_sha256': approval, 'harness_sha256': digest(HERE),
        'arithmetic_sha256': digest(helper_path), 'status': 'running', 'started_utc_ns': time.time_ns(),
        'variant_metadata': {}, 'oracles': {}, 'untimed_gates': {}, 'failure': None,
        'safety_receipts': safety, 'experiment_scope': 'DIAGNOSTIC ONLY: explicit supplied values',
        'whole_21_case_compatibility_gate': 'OPEN: preexisting native default omission/cache-order gap',
        'product_qualified': False, 'coordinator_control_sha256': digest(control_path),
        'batch_resources': [],
        'contention_interpretation': 'Outside-sample batch observations include receipt IO; not causal proof, never used to filter samples'}
    def save_metadata():
        (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    def receive(variant):
        line = workers[variant].stdout.readline()
        assert line, 'Timing worker terminated without a complete receipt'
        result = json.loads(line)
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
                process = subprocess.Popen([sys.executable, str(HERE), '--c9-worker', str(source), variant, str(manifest)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True,
                    env=env, cwd=source, bufsize=1)
                workers[variant] = process
                metadata['variant_metadata'][variant] = receive(variant)
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
            raw.flush(); os.fsync(raw.fileno())
            for variant, process in workers.items():
                if process.poll() is None:
                    try:
                        send(variant, {'command': 'close'})
                        response = receive(variant)
                        metadata.setdefault('closure', {})[variant] = response
                    except BaseException as failure:
                        metadata.setdefault('closure_failures', {})[variant] = safe_error(failure)
                    finally:
                        process.stdin.close()
                    try:
                        process.wait(timeout=60)
                    except subprocess.TimeoutExpired:
                        process.terminate(); process.wait(timeout=10)
                metadata.setdefault('worker_exit_codes', {})[variant] = process.returncode
            if metadata['status'] == 'sampling-complete':
                closed = metadata.get('closure', {})
                clean = (set(closed) == set(VARIANTS)
                    and all(item.get('event') == 'closed' and item.get('fixture_teardown_completed') is True for item in closed.values())
                    and all(code == 0 for code in metadata['worker_exit_codes'].values())
                    and not metadata.get('closure_failures'))
                metadata['status'] = 'complete' if clean else 'failed-source-or-worker-closure'
            metadata['observations_retained'] = len(observations)
            metadata['ended_utc_ns'] = time.time_ns()
            save_metadata()
    assert metadata['status'] == 'complete' and all(code == 0 for code in metadata['worker_exit_codes'].values())
    assert set(metadata.get('closure', {})) == set(VARIANTS)
    assert all(item['event'] == 'closed' for item in metadata['closure'].values())
    # Performance PASS/FAIL is a retained result, not grounds for rerunning pytest.


if __name__ == '__main__':
    assert len(sys.argv) == 5 and sys.argv[1] == '--c9-worker'
    try:
        worker(Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4]).resolve())
    except BaseException as failure:
        emit({'event': 'worker_error', 'error': safe_error(failure)})
        raise SystemExit(1)

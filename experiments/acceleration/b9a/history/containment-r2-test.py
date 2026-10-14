"""B9A RED contract: public-fixture, one-model UUID/equality inactive preparation.

Only generation 1 fixture setup publishes. This file never publishes generation 2.
Missing experiment import is deliberately lazy: collection is not feature evidence.
Observer/barrier callbacks are test-only fault injection, never durable authority.
The worker entry belongs in the future experiment module and calls public_worker_main.
"""
from contextlib import contextmanager
from dataclasses import asdict, replace
import hashlib
import importlib
import json
import logging
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
from uuid import UUID, uuid4

import psycopg
import pytest
from sqlalchemy import create_engine, event, select

from cryptalis.crypto import FieldDescriptor, Keyring, WrappedRoot, seal_text
from cryptalis.sqlalchemy import attach
from test_migration import (application, run, publish, keys, engine, frames,
    independent_open, PublicFixtureProvider, PROVIDER, TENANT)
from test_retained_profile_safety_oracles import catalog, native_buffer

SCHEMA = 'cryptalis.experiment.inactive-payload-preparation/v1'
TARGET_ROOT = UUID(int=91002)
STATE_FIELDS = {'schema', 'kind', 'source_operation_id', 'source_plan_digest',
    'artifact_digest', 'phase', 'source_revision', 'batches', 'verification'}
BATCH_FIELDS = {'ordinal', 'cursor_before', 'cursor_after', 'rows',
    'target_commitment', 'row_count', 'logical_bytes'}


def feature():
    return importlib.import_module('experiments.payload_rotation_journal')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def target_keys(tenant, *, max_age=60):
    """Stable PUBLIC wrapper recipe, reconstructed independently in every exec."""
    source = keys(tenant)
    old = next(w.context for w in source.policy.wrappers if w.context.purpose == 'payload')
    new = replace(old, root_id=TARGET_ROOT, generation=2)
    policy = replace(source.policy, wrappers=source.policy.wrappers +
        (WrappedRoot(PROVIDER, new, b'PUBLIC TEST WRAPPER'),), payload_generation=2)
    return Keyring(policy, {PROVIDER: PublicFixtureProvider()}, max_age=max_age)


def row_commitment(record, frame):
    return digest({'record_id': str(record), 'tenant_id': str(TENANT),
        'is_null': frame is None,
        'frame_sha256': None if frame is None else hashlib.sha256(frame).hexdigest()})


def target_commitment(rows):
    # Independent receipt recipe. Bodies are hashed, never journaled or logged.
    return digest([{'record_id': str(r), 'tenant_id': str(t), 'batch_ordinal': n,
        'source_commitment': bytes(s).hex(), 'is_null': b is None,
        'frame_sha256': None if b is None else hashlib.sha256(bytes(b)).hexdigest()}
        for r, t, n, s, b in rows])


def logical_bytes(rows):
    return sum(32 + (0 if b is None else 3 * len(b) - 74) for _, b in rows)


def native_snapshot(f):
    with f.app.owner.connect() as c:
        journal = c.exec_driver_sql(f'SELECT operation_id,plan_digest,state FROM "{f.app.schema}"._cryptalis_journal ORDER BY operation_id').all()
        staged = c.exec_driver_sql(f'SELECT record_id,tenant_id,batch_ordinal,source_commitment,target_frame FROM {f.stage} ORDER BY record_id').all()
        metadata = c.exec_driver_sql('''SELECT c.oid,c.relname,c.relkind,c.relowner,c.relacl::text,
            a.attnum,a.attname,a.atttypid,a.attnotnull,a.attacl::text
            FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
            LEFT JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped
            WHERE n.nspname=%s ORDER BY c.oid,a.attnum''', (f.app.schema,)).all()
        return journal, staged, metadata


def source_snapshot(f):
    with f.app.owner.connect() as c:
        row = c.exec_driver_sql(f'SELECT operation_id,plan_digest,state FROM "{f.app.schema}"._cryptalis_journal WHERE operation_id=%s', (f.app.plan.operation_id,)).one()
        return row, catalog(c, f.app), frames(f.app, True), f.app.pin


def staged(f):
    return native_snapshot(f)[1]


def state(f):
    with f.app.owner.connect() as c:
        return c.exec_driver_sql(f'SELECT state FROM "{f.app.schema}"._cryptalis_journal WHERE operation_id=%s', (f.artifact.operation_id,)).scalar_one()


@contextmanager
def fixture(*, max_bytes=4096, bind=True):
    # Root explicitly authorized this ordinary synthetic generation-1 setup.
    with application(rows=5) as app:
        run(app); publish(app)
        assert app.pin.phase == 'ACTIVE'
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=keys, deployment=(app.plan, app.pin))
        with factory(tenant_id=TENANT) as s:
            s.get(app.Customer, UUID(int=103)).name = 'current edited 雪'
            s.delete(s.get(app.Customer, UUID(int=104)))
            s.add(app.Customer(id=UUID(int=120), tenant_id=TENANT, name='new current 😀', label='new'))
            s.commit()
        expected = {UUID(int=100): None, UUID(int=101): '', UUID(int=102): '雪😀',
                    UUID(int=103): 'current edited 雪', UUID(int=120): 'new current 😀'}
        stage_name = 'inactive_payload_' + uuid4().hex
        stage = f'"{app.schema}"."{stage_name}"'
        with app.owner.begin() as c:
            c.exec_driver_sql(f'''CREATE TABLE {stage} (
                operation_id uuid NOT NULL, record_id uuid NOT NULL, tenant_id uuid NOT NULL,
                batch_ordinal integer NOT NULL CHECK (batch_ordinal>0),
                source_commitment bytea NOT NULL CHECK (octet_length(source_commitment)=32),
                target_frame bytea, PRIMARY KEY (operation_id,record_id))''')
        document = app.plan.document['lock']['models'][0]['fields'][0]
        f = SimpleNamespace(app=app, stage=stage, stage_name=stage_name, factory=factory,
            expected=expected, descriptor=document['descriptor'],
            field=FieldDescriptor.from_compiled(document['descriptor'], document['descriptor_digest']),
            source=keys(TENANT), target=target_keys(TENANT), max_bytes=max_bytes)
        f.baseline = source_snapshot(f)
        f.current = tuple(f.baseline[2].items())
        assert len(f.current) == 5
        assert expected != {r: value for r,(_,value) in app.source.items()}
        assert {r: independent_open(b, f.descriptor, TENANT, r) for r, b in f.current} == expected
        if bind:
            f.artifact = bind_artifact(f)
        f.workers = []
        yield f


def bind_artifact(f):
    return feature().bind(f.app.plan, f.app.owner, current_pin=f.app.pin,
        stage_table=(f.app.schema, f.stage_name), tenant_id=TENANT,
        source_keys=f.source, target_keys=f.target, maintenance=f.app.approval,
        max_rows=2, max_bytes=f.max_bytes)


def enter(f, action='step', **changes):
    kwargs = dict(source_plan=f.app.plan, current_pin=f.app.pin, source_keys=f.source,
                  target_keys=f.target, maintenance=f.app.approval, action=action)
    kwargs.update(changes)
    return feature().enter(f.artifact, f.app.owner, **kwargs)


def finish(f):
    # Finite fixture: at most three chunks plus one terminal verification.
    for _ in range(4):
        result = enter(f)
        if result.status == 'PREPARED_INACTIVE':
            return result
        assert result.status == 'PREPARING'
    pytest.fail('five-row fixture did not reach terminal inactive inspection')


def assert_parity(f):
    rows = staged(f)
    assert [r for r, *_ in rows] == list(f.expected)
    assert all(t == TENANT for _, t, *_ in rows)
    target_context = next(w.context for w in f.target.policy.wrappers if w.context.generation == 2)
    assert {r: independent_open(None if b is None else bytes(b), f.descriptor,
        TENANT, r, target_context) for r, _, _, _, b in rows} == f.expected
    assert all((b is None) == (dict(f.current)[r] is None) for r, _, _, _, b in rows)
    assert all(b is None or bytes(b)[10:46] == dict(f.current)[r][10:46] for r, _, _, _, b in rows)
    assert source_snapshot(f) == f.baseline
    with f.factory(tenant_id=TENANT) as session:
        assert dict(session.execute(select(f.app.Customer.id, f.app.Customer.name)).all()) == f.expected
    s = state(f)
    assert set(s) == STATE_FIELDS and s['schema'] == SCHEMA
    assert s['kind'] == 'INACTIVE_PAYLOAD_PREPARATION' and s['phase'] == 'PREPARED_INACTIVE'
    assert s['source_operation_id'] == str(f.app.plan.operation_id)
    assert s['source_plan_digest'] == f.app.plan.digest and s['artifact_digest'] == f.artifact.digest
    assert s['source_revision'] == {
        'row_count': 5, 'membership': digest([str(r) for r,_ in f.current]),
        'content': digest([{'record_id': str(r), 'source_commitment': row_commitment(r,b)} for r,b in f.current])}
    assert len(s['batches']) == 3
    for ordinal, batch in enumerate(s['batches'], 1):
        subset = f.current[(ordinal-1)*2:ordinal*2]
        persisted = [r for r in rows if r[2] == ordinal]
        assert set(batch) == BATCH_FIELDS
        assert batch['ordinal'] == ordinal and batch['row_count'] == len(subset)
        assert batch['cursor_before'] == (None if ordinal == 1 else str(f.current[(ordinal-1)*2-1][0]))
        assert batch['cursor_after'] == str(subset[-1][0])
        assert batch['rows'] == [{'record_id': str(r), 'source_commitment': row_commitment(r,b),
                                  'is_null': b is None} for r,b in subset]
        assert batch['target_commitment'] == target_commitment(persisted)
        assert batch['logical_bytes'] == logical_bytes(subset)
        assert all(bytes(h).hex() == row_commitment(r,dict(f.current)[r]) for r,_,_,h,_ in persisted)
    assert s['verification'] == {'row_count': 5, 'target_commitment': target_commitment(rows)}
    with f.app.owner.connect() as c:
        assert c.exec_driver_sql(f'SELECT DISTINCT operation_id FROM {f.stage}').scalars().all() == [f.artifact.operation_id]
        assert c.exec_driver_sql(f'SELECT operation_id FROM "{f.app.schema}"._cryptalis_journal ORDER BY operation_id').scalars().all() == sorted([f.app.plan.operation_id, f.artifact.operation_id])
        assert c.exec_driver_sql('''SELECT count(*) FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname=%s AND c.relkind='r' AND c.relname LIKE '%%journal%%' ''', (f.app.schema,)).scalar_one() == 1


def count_seals(monkeypatch):
    module = importlib.import_module('cryptalis.crypto._payload_rotation')
    original, calls = module.seal_text, []
    def observe(value, field, tenant, record, prepared):
        calls.append(record)
        return original(value, field, tenant, record, prepared)
    monkeypatch.setattr(module, 'seal_text', observe)
    return calls


def test_current_values_same_journal_inactive(monkeypatch):
    feature()  # Named initial RED: missing feature, not collection failure.
    with fixture() as f:
        assert f.artifact.canonical_bytes == canonical(f.artifact.document)
        assert f.artifact.digest == hashlib.sha256(f.artifact.canonical_bytes).hexdigest()
        before = native_snapshot(f)
        assert enter(f, 'start').status == 'PREPARING'
        assert staged(f) == [] and state(f)['batches'] == []
        assert native_snapshot(f)[2] == before[2]
        finish(f); assert_parity(f)
        assert native_snapshot(f)[2] == before[2]
        calls = count_seals(monkeypatch)
        before = native_snapshot(f)
        assert enter(f, 'inspect').status == 'PREPARED_INACTIVE'
        assert calls == [] and native_snapshot(f) == before


def write_bundle(f, directory):
    # Separate host inputs. No connection strings, prepared keys, roots or frames.
    path = directory / 'public-b9a-input.json'
    pin = {k: str(v) if isinstance(v, UUID) else v for k,v in asdict(f.app.pin).items()}
    path.write_bytes(canonical({'artifact': f.artifact.document,
        'source_plan': f.app.plan.document, 'current_pin': pin,
        'maintenance': asdict(f.app.approval)}))
    return path


# Containment is Linux-lab-specific, matching the already reviewed C10 pattern.
# Bootstrap executes before importing the experiment or any database driver.
WORKER_BOOTSTRAP = r"""
import ctypes, os, runpy, signal, sys
expected = int(sys.argv[1])
if not sys.platform.startswith('linux'):
    raise RuntimeError('worker parent containment requires Linux')
libc = ctypes.CDLL(None, use_errno=True)
if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
    raise RuntimeError('cannot establish worker parent containment')
if os.getppid() != expected:
    os._exit(1)
mode, target, args = sys.argv[2], sys.argv[3], sys.argv[4:]
sys.argv = [target, *args]
if mode == 'module':
    runpy.run_module(target, run_name='__main__')
else:
    exec(compile(target, '<public-containment-child>', 'exec'))
"""
WORKER_OUTPUT_LIMIT = 65536


def launch_contained(mode, target, args=(), *, env=None):
    process = subprocess.Popen([sys.executable, '-c', WORKER_BOOTSTRAP,
        str(os.getpid()), mode, target, *args], env=env,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        start_new_session=True, bufsize=0)
    process._stdout_pending = b''
    process._output_bytes = 0
    process._stderr_seen = False
    process._pipes_eof = set()
    try:
        for stream in (process.stdin, process.stdout, process.stderr):
            os.set_blocking(stream.fileno(), False)
    except BaseException:
        terminate_worker_group(process)
        raise
    return process


def worker(f, directory, action='finish', *, barrier=None, ordinal=0):
    path = write_bundle(f, directory)
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join((str(Path(__file__).resolve().parents[1]),
        str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1] / 'src'), env.get('PYTHONPATH','')))
    env['CRYPTALIS_B9A_TEST_BARRIER'] = barrier or ''
    env['CRYPTALIS_B9A_TEST_ORDINAL'] = str(ordinal)
    # Public nonsecret tag, also supplied explicitly to psycopg in worker_main:
    # URL application_name cannot silently override this identity.
    env['CRYPTALIS_B9A_WORKER_APPNAME'] = 'b9a-worker-' + uuid4().hex
    env['PGAPPNAME'] = env['CRYPTALIS_B9A_WORKER_APPNAME']
    process = launch_contained('module', 'experiments.payload_rotation_journal',
                              (str(path), action), env=env)
    process._fixture = f
    process._appname = env['PGAPPNAME']
    f.workers.append(process)
    return process


def read_worker_output(process, deadline, *, line):
    """No buffered readline/communicate: bound bytes and total wall time.

    Drain both raw pipes so stderr cannot deadlock stdout. Retain no stderr
    contents and never include child bytes in diagnostic exceptions.
    """
    with selectors.DefaultSelector() as ready:
        for stream in (process.stdout, process.stderr):
            if stream not in process._pipes_eof:
                ready.register(stream, selectors.EVENT_READ)
        while True:
            if line and b'\n' in process._stdout_pending:
                value, process._stdout_pending = process._stdout_pending.split(b'\n', 1)
                return value
            if not ready.get_map():
                if line:
                    raise RuntimeError('worker exited without a complete receipt')
                value, process._stdout_pending = process._stdout_pending, b''
                return value
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('worker output deadline exceeded')
            events = ready.select(remaining)
            if not events:
                raise TimeoutError('worker output deadline exceeded')
            for key, _ in events:
                stream = key.fileobj
                try:
                    chunk = os.read(stream.fileno(), min(4096,
                        WORKER_OUTPUT_LIMIT - process._output_bytes + 1))
                except BlockingIOError:
                    continue
                if not chunk:
                    process._pipes_eof.add(stream)
                    ready.unregister(stream)
                    continue
                process._output_bytes += len(chunk)
                if process._output_bytes > WORKER_OUTPUT_LIMIT:
                    raise RuntimeError('worker output size limit exceeded')
                if stream is process.stderr:
                    process._stderr_seen = True
                else:
                    process._stdout_pending += chunk


def decode_worker_receipt(raw):
    try:
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError
        return value
    except (ValueError, UnicodeError, RecursionError):
        raise RuntimeError('worker receipt is malformed') from None


def worker_line(process, timeout=15):
    return decode_worker_receipt(read_worker_output(process,
        time.monotonic() + timeout, line=True))


def completed_worker(process, timeout=30):
    deadline = time.monotonic() + timeout
    raw = read_worker_output(process, deadline, line=False)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('worker completion deadline exceeded')
    process.wait(timeout=remaining)
    if process.returncode != 0 or process._stderr_seen:
        raise RuntimeError('worker failed; diagnostic contents withheld')
    return decode_worker_receipt(raw)


def terminate_worker_group(process, grace=1):
    """Finite cleanup of this start_new_session group, including descendants.

    SIGKILL is sent even if the direct child already exited after SIGTERM.
    Pipes are closed on every path. No database backend is signalled here.
    """
    if getattr(process, '_group_closed', False):
        return
    try:
        for signum in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(process.pid, signum)
            except ProcessLookupError:
                pass
            if signum == signal.SIGTERM:
                try:
                    process.wait(timeout=grace)
                except subprocess.TimeoutExpired:
                    pass
        process.wait(timeout=grace)
        process._group_closed = True
    finally:
        for stream in (process.stdin, process.stdout, process.stderr):
            stream.close()


# Parent-side wall bound includes driver import, connect, query, and shutdown.
# The only SQL is a read-only pg_stat_activity query using the existing owner.
BACKEND_PROBE = r"""
import json, os, sys, psycopg
pid = int(sys.argv[1])
appname = sys.argv[2]
with psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL'],
        connect_timeout=3, application_name='b9a-terminal-observer',
        options='-c statement_timeout=2000 -c lock_timeout=1000') as connection:
    count = connection.execute(
        'SELECT count(*) FROM pg_catalog.pg_stat_activity WHERE '
        '(pid=%s AND %s>0) OR (application_name=%s AND %s<>\'\')',
        (pid, pid, appname, appname)).fetchone()[0]
print(json.dumps({'alive': count}), flush=True)
"""


def terminal_backend(f, backend_pid=0, *, appname=''):
    deadline = time.monotonic() + 15
    try:
        while time.monotonic() < deadline:
            probe = launch_contained('code', BACKEND_PROBE,
                                     (str(backend_pid), appname))
            try:
                result = completed_worker(probe,
                    timeout=min(5, max(.001, deadline - time.monotonic())))
            finally:
                terminate_worker_group(probe)
            if type(result.get('alive')) is not int:
                raise RuntimeError('backend observer returned invalid receipt')
            if result['alive'] == 0:
                return
            time.sleep(min(.02, max(0, deadline - time.monotonic())))
        raise TimeoutError('original backend is not terminal; outcome remains unknown')
    except BaseException:
        abort_worker_cleanup(f)


def stop_worker(process):
    f = process._fixture
    try:
        terminate_worker_group(process)
        if not getattr(process, '_backend_terminal', False):
            terminal_backend(f, appname=process._appname)
            process._backend_terminal = True
    except BaseException:
        abort_worker_cleanup(f)


def abort_worker_cleanup(f):
    """Approved test-only fail-closed path, before application() can DROP.

    The unchanged outer coordinator owns final server stop. This deliberately
    loses the normal pytest summary and retains the fixture schema as evidence.
    Exit 86 is never a cleanup PASS. No backend is terminated by this harness.
    """
    for process in f.workers:
        try:
            terminate_worker_group(process)
        except BaseException:
            pass
    try:
        print('B9A containment UNKNOWN: backend termination unconfirmed; '
              'fixture teardown aborted (exit 86).', file=sys.stderr, flush=True)
    finally:
        os._exit(86)


def test_restart_preserves_committed_prefix(tmp_path):
    with fixture() as f:
        enter(f, 'start')
        p = worker(f, tmp_path, barrier='after_commit', ordinal=1)
        try:
            observation = worker_line(p)
            assert observation['point'] == 'after_commit' and observation['ordinal'] == 1
            prefix, receipt = staged(f), state(f)['batches'][0]
            assert len(prefix) == 2
            p.kill(); assert p.wait(timeout=10) == -signal.SIGKILL
            terminal_backend(f, observation['backend_pid'])
            q = worker(f, tmp_path)
            try:
                result = completed_worker(q)
                assert result['status'] == 'PREPARED_INACTIVE'
                assert result['sealed_records'] == [str(r) for r,_ in f.current[2:]]
                assert staged(f)[:2] == prefix and state(f)['batches'][0] == receipt
                assert_parity(f)
            finally: stop_worker(q)
        finally: stop_worker(p)


def test_uncommitted_chunk_rows_and_marker_rollback(tmp_path):
    with fixture() as f:
        enter(f, 'start'); enter(f)
        before = native_snapshot(f)
        p = worker(f, tmp_path, barrier='after_dml', ordinal=2)
        try:
            observation = worker_line(p)
            assert observation['point'] == 'after_dml' and observation['ordinal'] == 2
            assert observation['stage_rows'] == 4 and observation['batch_receipts'] == 2
            assert native_snapshot(f) == before  # In-flight rows invisible elsewhere.
            p.kill(); assert p.wait(timeout=10) == -signal.SIGKILL
            terminal_backend(f, observation['backend_pid'])
            assert native_snapshot(f) == before
            q = worker(f, tmp_path)
            try: assert completed_worker(q)['status'] == 'PREPARED_INACTIVE'
            finally: stop_worker(q)
            assert staged(f)[:2] == before[1]; assert_parity(f)
        finally: stop_worker(p)


def test_lost_reply_requires_inspection(tmp_path):
    from migration_commit_proxy import lost_commit_reply
    with fixture() as f:
        enter(f, 'start')
        armed = [False]
        def observer(point, **context):
            if point == 'before_commit' and context['ordinal'] == 1:
                armed[0] = True
        # Real wire fault, armed by the batch boundary, never a magic commit count.
        with lost_commit_reply(os.environ['CRYPTALIS_TEST_DATABASE_URL'],
                drop_after_sql=lambda sql: armed[0] and sql.strip().upper() == 'COMMIT') as (url,dropped):
            faulty = create_engine('postgresql+psycopg://', hide_parameters=True,
                                   creator=lambda: psycopg.connect(url))
            try:
                result = feature().enter(f.artifact, faulty, source_plan=f.app.plan,
                    current_pin=f.app.pin, source_keys=f.source, target_keys=f.target,
                    maintenance=f.app.approval, action='step', observer=observer)
                assert result.status == 'UNKNOWN' and result.code == 'inspection_required'
                assert dropped.wait(5)
            finally: faulty.dispose()
        prefix = staged(f)
        assert len(prefix) == 2 and len(state(f)['batches']) == 1
        q = worker(f, tmp_path)
        try:
            result = completed_worker(q)
            assert result['status'] == 'PREPARED_INACTIVE'
            assert result['sealed_records'] == [str(r) for r,_ in f.current[2:]]
        finally: stop_worker(q)
        assert staged(f)[:2] == prefix; assert_parity(f)


def test_busy_executor_is_pending(tmp_path):
    with fixture() as f:
        enter(f,'start'); enter(f)
        before = native_snapshot(f)
        p = worker(f,tmp_path,barrier='after_dml',ordinal=2)
        try:
            observation = worker_line(p)
            assert observation['ordinal'] == 2
            # Independent canonical full-source-model-set lock probe.
            models=f.app.plan.document['lock']['models']
            scope=int.from_bytes(hashlib.sha256(canonical([(m['schema'],m['table']) for m in models])).digest()[:8],'big',signed=True)
            with f.app.owner.connect() as c:
                acquired=c.exec_driver_sql('SELECT pg_catalog.pg_try_advisory_lock(%s)',(scope,)).scalar_one()
                if acquired: c.exec_driver_sql('SELECT pg_catalog.pg_advisory_unlock(%s)',(scope,))
                assert acquired is False
            result = enter(f)
            assert result.status == 'PENDING' and result.code == 'executor_busy'
            assert native_snapshot(f) == before
            assert os.write(p.stdin.fileno(), b'continue\n') == 9
            assert completed_worker(p)['status'] == 'PREPARED_INACTIVE'
            assert_parity(f)
        finally: stop_worker(p)


@pytest.mark.parametrize('change', ['same_value_reseal', 'insert_behind_cursor'])
def test_source_change_refuses_resume(change):
    with fixture() as f:
        enter(f,'start'); enter(f)
        if change == 'same_value_reseal':
            record = UUID(int=101)
            fresh = seal_text('', f.field, TENANT, record, keys(TENANT).prepare())
            column = '_cryptalis_' + f.field.field_id.hex
            with f.app.owner.begin() as c:
                c.exec_driver_sql(f'UPDATE "{f.app.schema}".customer SET "{column}"=%s WHERE id=%s', (fresh,record))
        else:
            with f.factory(tenant_id=TENANT) as session:
                session.add(f.app.Customer(id=UUID(int=99),tenant_id=TENANT,name='behind cursor',label='new'))
                session.commit()
        before = native_snapshot(f)
        with pytest.raises(feature().PreparationFailure) as error: enter(f)
        assert error.value.code == 'source_revision_changed'
        assert native_snapshot(f) == before


def test_changed_external_pin_refuses():
    with fixture() as f:
        enter(f,'start'); enter(f)
        before = native_snapshot(f)
        with pytest.raises(feature().PreparationFailure) as error:
            enter(f,current_pin=replace(f.app.pin,plan_digest='0'*64))
        assert error.value.code == 'source_authority_changed'
        assert native_snapshot(f) == before


@pytest.mark.parametrize('change', ['missing_row', 'valid_value_adjusted_hash'])
def test_inconsistent_prefix_refuses(change):
    with fixture() as f:
        enter(f,'start'); enter(f)
        record = UUID(int=101)
        with f.app.owner.begin() as c:
            if change == 'missing_row':
                c.exec_driver_sql(f'DELETE FROM {f.stage} WHERE record_id=%s',(record,))
            else:
                frame = seal_text('valid but different', f.field,TENANT,record,f.target.prepare())
                c.exec_driver_sql(f'UPDATE {f.stage} SET target_frame=%s WHERE record_id=%s',(frame,record))
                rows = c.exec_driver_sql(f'SELECT record_id,tenant_id,batch_ordinal,source_commitment,target_frame FROM {f.stage} ORDER BY record_id').all()
                current = state(f)
                current['batches'][0]['target_commitment'] = target_commitment(rows)
                c.exec_driver_sql(f'UPDATE "{f.app.schema}"._cryptalis_journal SET state=%s::jsonb WHERE operation_id=%s', (canonical(current).decode(),f.artifact.operation_id))
        before = native_snapshot(f)
        with pytest.raises(feature().PreparationFailure) as error: enter(f)
        assert error.value.code == 'prefix_inconsistent'
        assert native_snapshot(f) == before


@pytest.mark.parametrize('which', ['source','target'])
def test_expiry_before_commit_rolls_back(which, monkeypatch):
    import cryptalis.crypto.keys as key_module
    with fixture() as f:
        enter(f,'start'); enter(f)
        before = native_snapshot(f)
        now = [100.0]
        monkeypatch.setattr(key_module, 'time', SimpleNamespace(monotonic=lambda:now[0], monotonic_ns=lambda:int(now[0]*1e9)))
        source = Keyring(keys(TENANT).policy, {PROVIDER:PublicFixtureProvider()},max_age=10 if which=='source' else 60)
        target = target_keys(TENANT,max_age=10 if which=='target' else 60)
        observed = []
        def expire(point, **context):
            if point == 'after_dml' and context['ordinal'] == 2:
                c = context['connection']
                assert c.exec_driver_sql(f'SELECT count(*) FROM {f.stage}').scalar_one() == 4
                observed.append(point); now[0]=111.0
        with pytest.raises(feature().PreparationFailure) as error:
            enter(f,source_keys=source,target_keys=target,observer=expire)
        assert error.value.code == 'binding_expired' and observed == ['after_dml']
        assert native_snapshot(f) == before
        f.source=keys(TENANT); f.target=target_keys(TENANT)
        finish(f); assert_parity(f)


def test_existing_runtime_cannot_mutate_metadata():
    with fixture() as f:
        enter(f,'start')
        before=native_snapshot(f)
        journal=f'"{f.app.schema}"._cryptalis_journal'
        for relation in (f.stage,journal):
            for command in (f'INSERT INTO {relation} DEFAULT VALUES',
                            f'UPDATE {relation} SET operation_id=operation_id',
                            f'DELETE FROM {relation}', f'TRUNCATE {relation}',
                            f'ALTER TABLE {relation} OWNER TO "{f.app.role}"'):
                with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:
                    with pytest.raises(psycopg.errors.InsufficientPrivilege): c.execute(command)
        assert native_snapshot(f)==before
        with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:
            assert c.execute(f'SELECT count(*) FROM {journal}').fetchone()==(2,)
        with f.factory(tenant_id=TENANT) as session:
            assert session.get(f.app.Customer,UUID(int=102)).name=='雪😀'


@pytest.mark.parametrize('case',['exact_fit','first_row_over_budget'])
def test_chunk_budget_precedes_frame_transport(case,monkeypatch):
    with fixture(bind=False) as f:
        # Make the first native UUID frame the maximum cost, before binding.
        with f.factory(tenant_id=TENANT) as session:
            session.get(f.app.Customer,UUID(int=100)).name='budget-'+('x'*256)
            session.commit()
        current=tuple(frames(f.app,True).items())
        cost=logical_bytes(current[:1]); f.max_bytes=cost-(case=='first_row_over_budget')
        samples=[]
        def capture(connection,cursor,statement,parameters,context,many):
            if cursor.description is not None: samples.append(native_buffer(cursor))
        event.listen(f.app.owner,'after_cursor_execute',capture)
        calls=count_seals(monkeypatch)
        before=native_snapshot(f); samples.clear()
        try:
            if case=='first_row_over_budget':
                with pytest.raises(feature().PreparationFailure) as error: f.artifact=bind_artifact(f)
                assert error.value.code=='row_exceeds_chunk_byte_limit'
                observed=list(samples)
                # Driver-level result metadata: no source frame value transported.
                needle=current[0][1]
                assert observed and not calls
                assert not any(value is not None and (needle in value or needle.hex().encode() in value)
                    for _,rows in observed for row in rows for value in row)
                assert native_snapshot(f)==before
            else:
                f.artifact=bind_artifact(f); enter(f,'start'); enter(f)
                assert len(staged(f))==1
                assert state(f)['batches'][0]['logical_bytes']==cost
        finally: event.remove(f.app.owner,'after_cursor_execute',capture)


def test_safe_output_collector(capsys,caplog,monkeypatch):
    sentinel='UNPROTECTED-COLLECTOR-CALIBRATION'
    print(sentinel)
    logging.getLogger('b9a.collector').warning(sentinel)
    assert sentinel in capsys.readouterr().out and sentinel in caplog.text
    caplog.clear()
    with fixture() as f:
        enter(f,'start')
        secret_marker='PUBLIC-TEST-PROVIDER-RAW-EXCEPTION-MARKER'
        def fail(*args,**kwargs): raise RuntimeError(secret_marker)
        bad=target_keys(TENANT)
        monkeypatch.setattr(PublicFixtureProvider,'unwrap',fail)
        before=native_snapshot(f)
        with pytest.raises(feature().PreparationFailure) as error: enter(f,target_keys=bad)
        output=capsys.readouterr()
        diagnostic=output.out+output.err+caplog.text+str(error.value)
        forbidden=[secret_marker,'current edited 雪','new current 😀']
        forbidden += [v for k in ('CRYPTALIS_TEST_DATABASE_URL','CRYPTALIS_TEST_RUNTIME_DATABASE_URL') if (v:=os.environ.get(k))]
        forbidden += [value for _,b in f.current if b is not None for value in (b.hex(),repr(b),b[14:46].hex(),repr(b[14:46]))]
        for wrapper in f.target.policy.wrappers:
            root=hashlib.sha256(('PUBLIC MIGRATION FIXTURE:'+str(wrapper.context)).encode()).digest()
            forbidden.extend((root.hex(),repr(root)))
        assert all(value not in diagnostic for value in forbidden)
        assert native_snapshot(f)==before


def public_worker_main():
    """Called only by the experiment's __main__; public synthetic test harness.

    API observer(point, connection=..., ordinal=...) points: after_dml is after
    stage INSERT and journal conditional UPDATE but before the binding check;
    before_commit follows that check; after_commit follows an acknowledged COMMIT.
    These controls cannot authorize progress or bypass validation.
    """
    from cryptalis.migration import MigrationPlan,DeploymentPin,MaintenanceApproval
    doc=json.loads(Path(sys.argv[1]).read_bytes())
    m=feature()
    artifact=m.Artifact(canonical(doc['artifact']))
    source=MigrationPlan(canonical(doc['source_plan']))
    pin_doc=doc['current_pin']
    pin=DeploymentPin(UUID(pin_doc['target_id']),UUID(pin_doc['operation_id']),pin_doc['plan_digest'],pin_doc['phase'])
    approval=MaintenanceApproval(**doc['maintenance'])
    appname = os.environ['CRYPTALIS_B9A_WORKER_APPNAME']
    owner = create_engine('postgresql+psycopg://', hide_parameters=True,
        creator=lambda: psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL'],
                                       application_name=appname))
    sealed=[]
    b8=importlib.import_module('cryptalis.crypto._payload_rotation')
    original=b8.seal_text
    def observe_seal(value,field,tenant,record,prepared):
        sealed.append(str(record)); return original(value,field,tenant,record,prepared)
    b8.seal_text=observe_seal
    def barrier(point,**context):
        if point!=os.environ.get('CRYPTALIS_B9A_TEST_BARRIER') or context['ordinal']!=int(os.environ.get('CRYPTALIS_B9A_TEST_ORDINAL','0')): return
        c=context['connection']
        # Driver info avoids starting a new transaction after the commit barrier.
        backend=c.connection.driver_connection.info.backend_pid
        report={'point':point,'ordinal':context['ordinal'],'backend_pid':backend}
        if point=='after_dml':
            stage=artifact.document['stage']['qualified_name']
            schema=source.document['lock']['models'][0]['schema']
            report['stage_rows']=c.exec_driver_sql(f'SELECT count(*) FROM {stage}').scalar_one()
            report['batch_receipts']=c.exec_driver_sql(f'SELECT jsonb_array_length(state->\'batches\') FROM "{schema}"._cryptalis_journal WHERE operation_id=%s',(artifact.operation_id,)).scalar_one()
        print(json.dumps(report),flush=True)
        if sys.stdin.readline()!='continue\n': raise RuntimeError('test barrier not released')
    try:
        action=sys.argv[2]
        if action not in ('start','step','inspect','finish'): raise ValueError('invalid public worker action')
        for _ in range(4 if action=='finish' else 1):
            result=m.enter(artifact,owner,source_plan=source,current_pin=pin,
                source_keys=keys(TENANT),target_keys=target_keys(TENANT),maintenance=approval,
                action='step' if action=='finish' else action,observer=barrier)
            if result.status!='PREPARING' or action!='finish': break
        print(json.dumps({'status':result.status,'code':result.code,'sealed_records':sealed}),flush=True)
    finally:
        b8.seal_text=original; owner.dispose()

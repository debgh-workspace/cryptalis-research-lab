"""Untimed source-isolated C10 PostgreSQL differential gate; wrapper only.

Every process imports its complete frozen source. Native SQL is evaluated by
psycopg directly, independently of Cryptalis rewrite and result processing.
"""
from contextlib import ExitStack
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from uuid import UUID

from profile_c10_timing import (MANIFEST_HASH, VARIANTS, dependencies, digest,
                               emit, protect_worker_parent, safe_error, source_snapshot, terminate_worker_group)

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
VALUES = (None, '', 'exact', '雪😀', 'é', 'e\u0301', 'missing', 'exact')
CASES = ((), (None,), (None, None), ('exact', None), ('exact', 'exact'),
         ('雪😀', 'é'), tuple('absent-%d' % i for i in range(20)),
         ('exact', '雪😀') + tuple('absent-%d' % i for i in range(18)))
CASE_NAMES = ('empty', 'null', 'all-null', 'mixed', 'duplicates', 'unicode', 'miss20', 'hot20')


def canonical(rows):
    return [[str(value) if isinstance(value, UUID) else value for value in row] for row in rows]


def read_rows(session, statement, parameters):
    result = session.execute(statement, parameters)
    try:
        return [tuple(row) for row in result.all()]
    finally:
        result.close()


def worker(source, variant, manifest, candidate_hash):
    sys.path[:0] = [str(source / 'src'), str(source / 'tests')]
    import psycopg
    from psycopg import sql
    from sqlalchemy import Text, bindparam, event, select
    from sqlalchemy.orm import aliased
    import cryptalis.sqlalchemy as adapter
    from test_sqlalchemy_search import search_application, TENANT, OTHER
    assert Path(adapter.__file__).resolve() == source / 'src/cryptalis/sqlalchemy.py'
    before = source_snapshot(source, variant, manifest, candidate_hash)
    receipt = {'variant': variant, 'source_before': before, 'dependencies': dependencies(),
               'cases': {}, 'invalid_text': {}}
    with ExitStack() as stack:
        app = stack.enter_context(search_application(protected=variant != 'native', two_fields=True))
        for offset, tenant in enumerate((TENANT, OTHER)):
            with app.sessions(tenant_id=tenant) as session:
                session.add_all([app.Customer(id=UUID(int=1000 + offset * 100 + rank), tenant_id=tenant,
                    name=value, other_name=VALUES[(rank + 2) % len(VALUES)], label=value, rank=rank)
                    for rank, value in enumerate(VALUES)])
                session.commit()
        # A plain independent driver sees native text only. No attached-engine
        # bypass, product oracle helper, or protected-byte fallback is involved.
        if variant == 'native':
            oracle = stack.enter_context(psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
            oracle.execute('SET TRANSACTION READ ONLY')
        for offset, tenant in enumerate((TENANT, OTHER)):
            for use_alias in (False, True):
                with app.sessions(tenant_id=tenant) as session:
                    C = aliased(app.Customer) if use_alias else app.Customer
                    for name, values in zip(CASE_NAMES, CASES):
                        shared = bindparam('needles', expanding=True, type_=Text())
                        p, q, r = C.name.in_(shared), C.other_name.in_(shared), C.label.in_(shared)
                        params = {'needles': values}
                        projected = read_rows(session, select(C.id, p, q, r).where(C.tenant_id == tenant).order_by(C.id), params)
                        ids = read_rows(session, select(C.id).where(C.tenant_id == tenant, p, p).order_by(C.id), params)
                        payload = read_rows(session, select(C.id, C.name, C.other_name).where(C.tenant_id == tenant, p).order_by(C.id), params)
                        result = session.execute(select(C).where(C.tenant_id == tenant, p).order_by(C.id), params)
                        try:
                            entities = [(row.id, row.name, row.other_name) for row in result.scalars().all()]
                        finally:
                            result.close()
                        assert entities == payload
                        cutoff = UUID(int=1001 + offset * 100)
                        page = read_rows(session, select(C.id).where(C.tenant_id == tenant, p,
                            C.id > cutoff).order_by(C.id).limit(2), params)
                        assert page == [row for row in ids if row[0] > cutoff][:2]
                        item = {kind: canonical(rows) for kind, rows in
                            (('truth', projected), ('ids', ids), ('payload', payload), ('entities', entities), ('page', page))}
                        if variant == 'native':
                            truth = oracle.execute(sql.SQL('SELECT id, name = ANY(%s::text[]), '
                                'other_name = ANY(%s::text[]), label = ANY(%s::text[]) '
                                'FROM {}.customer WHERE tenant_id = %s ORDER BY id').format(sql.Identifier(app.schema)),
                                (list(values), list(values), list(values), tenant)).fetchall()
                            expected_payload = oracle.execute(sql.SQL('SELECT id, name, other_name FROM {}.customer '
                                'WHERE tenant_id = %s AND name = ANY(%s::text[]) ORDER BY id').format(sql.Identifier(app.schema)),
                                (tenant, list(values))).fetchall()
                            assert projected == truth and payload == expected_payload
                            assert ids == [(row[0],) for row in truth if row[1] is True]
                        receipt['cases'][f'{offset}/{use_alias}/in/{name}'] = item
                    for index, value in enumerate(VALUES):
                        statement = select(C.id, C.name, C.other_name).where(C.tenant_id == tenant,
                            C.name == bindparam('needle', type_=Text())).order_by(C.id)
                        actual = read_rows(session, statement, {'needle': value})
                        if variant == 'native':
                            expected = oracle.execute(sql.SQL('SELECT id, name, other_name FROM {}.customer '
                                'WHERE tenant_id = %s AND name = %s::text ORDER BY id').format(sql.Identifier(app.schema)),
                                (tenant, value)).fetchall()
                            assert actual == expected
                        receipt['cases'][f'{offset}/{use_alias}/equality/{index}'] = canonical(actual)
                    # Fixed point and lazy iteration retain native row identity.
                    for index, _ in enumerate(VALUES):
                        record = UUID(int=1000 + offset * 100 + index)
                        result = session.execute(select(C.id, C.name, C.other_name).where(
                            C.tenant_id == tenant, C.id == record))
                        try:
                            actual = [tuple(row) for row in result]
                        finally:
                            result.close()
                        if variant == 'native':
                            expected = oracle.execute(sql.SQL('SELECT id, name, other_name FROM {}.customer '
                                'WHERE tenant_id = %s AND id = %s').format(sql.Identifier(app.schema)),
                                (tenant, record)).fetchall()
                            assert actual == expected
                        receipt['cases'][f'{offset}/{use_alias}/point/{index}'] = canonical(actual)
        if variant == 'native':
            oracle.rollback(); oracle.close()
            assert oracle.closed
            receipt['independent_driver_oracle_closed'] = True
        else:
            for name, value in (('integer', 7), ('bytes', b'exact'), ('nul', 'x\x00y'), ('surrogate', '\ud800')):
                statements = []
                def cursor(connection, raw, statement, parameters, context, many):
                    statements.append(statement)
                with app.sessions(tenant_id=TENANT) as session:
                    event.listen(app.engine, 'before_cursor_execute', cursor)
                    try:
                        try:
                            read_rows(session, select(app.Customer.id).where(app.Customer.name ==
                                bindparam('needle', type_=Text())), {'needle': value})
                        except Exception as failure:
                            signature = safe_error(failure)
                        else:
                            raise AssertionError('Invalid text reached a successful query')
                    finally:
                        event.remove(app.engine, 'before_cursor_execute', cursor)
                    assert signature['type'] == 'StatementError' and signature['original_type'] == 'InvalidText'
                    assert not statements
                    receipt['invalid_text'][name] = {'error': signature, 'cursor_calls': len(statements),
                        'session_active': session.is_active, 'in_transaction': session.in_transaction()}
                    session.rollback()
    # ExitStack has really torn down the fixture before this success receipt.
    receipt['source_after'] = source_snapshot(source, variant, manifest, candidate_hash)
    assert receipt['source_after'] == before
    assert len(receipt['cases']) == 96
    receipt['fixture_teardown_completed'] = True
    emit(receipt)


def test_c10_source_isolated_postgres_native_oracle():
    assert '_cryptalis_test_preflight' in sys.modules
    control_path = ROOT / 'experiments/C10_CORRECTNESS_APPROVAL.json'
    control = json.loads(control_path.read_text())
    assert set(control) == {'coordinator_approved', 'protocol_sha256', 'harness_sha256',
        'timing_harness_sha256', 'candidate_cf1_sha256', 'baseline_root', 'cell_output_directories'}
    assert control['coordinator_approved'] is True
    assert digest(HERE) == control['harness_sha256']
    assert digest(HERE.with_name('profile_c10_timing.py')) == control['timing_harness_sha256']
    assert digest(ROOT / 'experiments/C10_TIMING_PROTOCOL.md') == control['protocol_sha256']
    assert set(control['cell_output_directories']) == {'2.0.51', '2.1.3'}
    deps = dependencies()
    version = deps['packages']['SQLAlchemy']['version']
    output = Path(control['cell_output_directories'][version]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = ROOT / 'experiments/C10_SOURCE_MANIFEST.json'
    assert digest(manifest) == MANIFEST_HASH
    baseline = Path(control['baseline_root']).resolve()
    metadata = {'status': 'running', 'started_utc_ns': time.time_ns(), 'dependencies': deps,
                'control_sha256': digest(control_path), 'variants': {}, 'failure': None,
                'product_qualified': False, 'whole_compatibility_gate': 'OPEN'}
    def save():
        (output / 'correctness.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n')
    save()
    try:
        for variant in VARIANTS:
            source = ROOT if variant == 'candidate' else baseline
            env = dict(os.environ)
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            env['PYTHONPATH'] = os.pathsep.join((str(source / 'src'), str(source / 'tests')))
            with (output / (variant + '-stdout.json')).open('x') as stdout, (output / (variant + '-stderr.log')).open('x') as stderr:
                child = subprocess.Popen([sys.executable, str(HERE), '--c10-worker', str(source), variant,
                    str(manifest), control['candidate_cf1_sha256'], str(os.getpid())], cwd=source, env=env,
                    stdout=stdout, stderr=stderr, text=True, start_new_session=True)
                try:
                    child.wait(timeout=300)
                except BaseException:
                    metadata.setdefault('forced_termination', {})[variant] = terminate_worker_group(child)
                    metadata.setdefault('exit_codes', {})[variant] = child.returncode
                    raise
            metadata.setdefault('exit_codes', {})[variant] = child.returncode
            assert child.returncode == 0, 'Correctness worker failed; raw safe receipt retained'
            receipt = json.loads((output / (variant + '-stdout.json')).read_text())
            assert receipt['variant'] == variant and receipt['fixture_teardown_completed'] is True
            assert receipt['dependencies'] == deps
            metadata['variants'][variant] = receipt
            save()
        variants = metadata['variants']
        assert variants['native']['independent_driver_oracle_closed'] is True
        assert variants['native']['cases'] == variants['original']['cases'] == variants['candidate']['cases']
        assert variants['original']['invalid_text'] == variants['candidate']['invalid_text']
        metadata['status'] = 'complete'
    except BaseException as failure:
        metadata['status'], metadata['failure'] = 'failed', safe_error(failure)
        raise
    finally:
        metadata['ended_utc_ns'] = time.time_ns()
        save()


if __name__ == '__main__':
    assert len(sys.argv) == 7 and sys.argv[1] == '--c10-worker'
    protect_worker_parent(int(sys.argv[6]))
    try:
        worker(Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4]).resolve(), sys.argv[5])
    except BaseException as failure:
        emit({'event': 'worker_error', 'error': safe_error(failure)})
        raise SystemExit(1)

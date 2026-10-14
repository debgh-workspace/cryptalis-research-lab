"""B9B profile-extension RED tests; no generation-2 publication.

Three independent native fixtures. Frozen B9A rejects unsupported_profile at bind.
These tests require future success: rejection is RED, never xfail or expected PASS.
"""
from contextlib import contextmanager
import hashlib
import hmac
import importlib
import json
import os
import signal
from types import SimpleNamespace
from uuid import UUID, uuid4

from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
import psycopg
from psycopg import sql
import pytest
from sqlalchemy import BigInteger, Column, Index, MetaData, Table, Text, Uuid, select, text
from sqlalchemy.orm import registry, sessionmaker

from cryptalis.crypto import FieldDescriptor
from cryptalis.manifest.compiler import Writer, WriterInventory, SearchReview
from cryptalis.sqlalchemy import attach
from test_migration import (DOMAIN, TABLE_ID, FIELD_ID, TENANT, PROVIDER,
    PublicFixtureProvider, WrappedRoot, keys, engine, run, publish)
import test_payload_rotation_journal as b9

PROFILES = ('uuid-storage', 'bigint-equality', 'bigint-storage')


def independent_open(body, descriptor, tenant, record, payload_context=None, *, field_id=FIELD_ID):
    """Separate HKDF/HMAC/framing path; same qualified AEAD primitive only."""
    if body is None:
        return None
    def pack(*parts):
        return len(parts).to_bytes(4, 'big') + b''.join(len(p).to_bytes(4, 'big') + p for p in parts)
    def derive(purpose, info):
        context = next(w.context for w in keys(tenant).policy.wrappers if w.context.purpose == purpose)
        if purpose=='payload' and payload_context is not None: context=payload_context
        root = PublicFixtureProvider().unwrap(WrappedRoot(PROVIDER, context, b'PUBLIC TEST WRAPPER'), context)
        salt = hashlib.sha256(pack(b'CF1/root', DOMAIN.bytes, tenant.bytes, context.root_id.bytes, context.generation.to_bytes(4, 'big'))).digest()
        prk = hmac.digest(salt, root, 'sha256')
        return hmac.digest(prk, info + b'\x01', 'sha256')
    if descriptor['record_codec'] == 'uuid16/v1':
        assert type(record) is UUID
        record_bytes = record.bytes
    else:
        assert descriptor['record_codec'] == 'int64-be/v1'
        assert type(record) is int and -(2**63) <= record < 2**63
        record_bytes = pack(b'int64', record.to_bytes(8, 'big', signed=True))
    equality = descriptor['representation'] == 'cf1-packed-equality/v1'
    assert body[:6] == bytes.fromhex('434631000101' if equality else '434631000100')
    assert int.from_bytes(body[6:10],'big')==(payload_context.generation if payload_context else 1)
    assert body[10:14] == bytes.fromhex('00000001' if equality else '00000000')
    size = 46 if equality else 14
    header = body[:size]
    key = derive('payload', pack(b'CF1/payload-key', field_id.bytes, record_bytes))
    digest = hashlib.sha256(json.dumps(descriptor, sort_keys=True, separators=(',', ':')).encode()).digest()
    aad = pack(b'CF1/payload', DOMAIN.bytes, tenant.bytes, field_id.bytes, record_bytes, digest, header)
    value = AESGCMSIV(key).decrypt(body[size:size+12], body[size+12:], aad)
    if equality:
        search_key = derive('search', pack(b'CF1/search-key', field_id.bytes, b'utf8-exact/v1', b'identity/v1', b'equality'))
        assert hmac.compare_digest(header[14:46], hmac.digest(search_key, pack(b'equality', value), 'sha256'))
    return value.decode('utf8')


@contextmanager
def native_application(profile):
    """Own native schema and model, with no UUID adapter around BIGINT IDs."""
    bigint = profile.startswith('bigint-')
    equality = profile.endswith('-equality')
    ids = ([-(2**63), -100, -10, -1, 0, 1, 10, 100, 2**63-1] if bigint else
           [UUID(int=i) for i in (1, 10, 20, 30, 40, 50, 60, 70, 2**128-1)])
    values = ['lower boundary', '', '雪😀', 'e\u0301', None, 'exact', 'trailing ', 'delete me', 'upper boundary']
    source = dict(zip(ids, ((TENANT, v) for v in values)))
    owner, runtime = engine('CRYPTALIS_TEST_DATABASE_URL'), engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
    schema = 'cryptalis_profile_' + uuid4().hex
    mapping = registry(metadata=MetaData(schema=schema))
    table = Table('customer', mapping.metadata,
        Column('id', BigInteger if bigint else Uuid, primary_key=True, autoincrement=False),
        Column('tenant_id', Uuid, nullable=False), Column('name', Text(collation='C')),
        Column('label', Text))
    if equality:
        Index('native_name', table.c.tenant_id, table.c.name)
    class Customer: pass
    mapping.map_imperatively(Customer, table)
    declaration = {'schema': 'cryptalis.protection/v1', 'profile': 'cf1', 'domain_id': str(DOMAIN),
        'models': [{'model': 'Customer', 'table_id': str(TABLE_ID), 'tenancy': {'column': 'tenant_id'},
            'fields': [{'name': 'name', 'field_id': str(FIELD_ID), 'protect': True,
                        'queries': ['equality'] if equality else [],
                        'accept_leakage': ['equality'] if equality else []}]}]}
    with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:
        role = c.execute('SELECT current_user').fetchone()[0]
    try:
        with owner.begin() as c:
            c.execute(text(f'CREATE SCHEMA "{schema}"'))
        mapping.metadata.create_all(owner)
        # Same ordinary generation-1 fixture grants as test_migration.application;
        # no role, credential, policy, stage grant, or journal grant is created.
        with psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL']) as c:
            c.execute(sql.SQL('REVOKE ALL ON SCHEMA {} FROM PUBLIC').format(sql.Identifier(schema)))
            c.execute(sql.SQL('GRANT USAGE ON SCHEMA {} TO {}').format(sql.Identifier(schema), sql.Identifier(role)))
            c.execute(sql.SQL('GRANT SELECT, INSERT, UPDATE, DELETE ON {}.customer TO {}').format(sql.Identifier(schema), sql.Identifier(role)))
        # Reverse insertion order is deliberately unlike native database ordering.
        with sessionmaker(runtime)() as session:
            session.add_all(Customer(id=k, tenant_id=t, name=v, label='public')
                            for k, (t, v) in reversed(list(source.items())))
            session.commit()
        m = importlib.import_module('cryptalis.migration')
        plan = m.plan(json.dumps(declaration).encode(), mapping, owner,
            writers=WriterInventory(True, (Writer(TABLE_ID, 'app', 'sqlalchemy', evidence='owned synthetic application'),)),
            search_reviews=(SearchReview(FIELD_ID, False, 'synthetic unbounded names'),) if equality else (),
            keys=keys, runtime_role=role, target_id=uuid4(),
            backfill_rows_per_second=1000, verify_rows_per_second=1000,
            temporary_bytes_per_row=700, wal_bytes_per_row=2000)
        pin = m.DeploymentPin(plan.target_id, plan.operation_id, plan.digest, 'PREPARED')
        yield SimpleNamespace(m=m, owner=owner, runtime=runtime, schema=schema, mapping=mapping,
            table=table, Customer=Customer, source=source, ids=ids, plan=plan, pin=pin, role=role,
            approval=m.MaintenanceApproval('test operator stopped inventoried workers and excluded owner writers', 3600))
    finally:
        runtime.dispose()
        with owner.begin() as c:
            c.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        owner.dispose()
        mapping.dispose()


@contextmanager
def profile_fixture(profile):
    with native_application(profile) as app:
        run(app); publish(app)
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=keys, deployment=(app.plan, app.pin))
        new_id = 50 if profile.startswith('bigint-') else UUID(int=65)
        expected = {r: v for r, (_, v) in app.source.items()}
        expected[app.ids[3]] = 'current edited 雪'
        del expected[app.ids[7]]
        expected[new_id] = 'new current 😀'
        expected = dict(sorted(expected.items()))
        with factory(tenant_id=TENANT) as session:
            session.get(app.Customer, app.ids[3]).name = expected[app.ids[3]]
            session.delete(session.get(app.Customer, app.ids[7]))
            session.add(app.Customer(id=new_id, tenant_id=TENANT, name=expected[new_id], label='new'))
            session.commit()
        stage_name = 'inactive_payload_' + uuid4().hex
        stage = f'"{app.schema}"."{stage_name}"'
        native_type = 'bigint' if profile.startswith('bigint-') else 'uuid'
        with app.owner.begin() as c:
            c.exec_driver_sql(f'''CREATE TABLE {stage} (
                operation_id uuid NOT NULL, record_id {native_type} NOT NULL, tenant_id uuid NOT NULL,
                batch_ordinal integer NOT NULL CHECK (batch_ordinal>0),
                source_commitment bytea NOT NULL CHECK (octet_length(source_commitment)=32),
                target_frame bytea, PRIMARY KEY (operation_id,record_id))''')
        document = app.plan.document['lock']['models'][0]['fields'][0]
        f = SimpleNamespace(app=app, profile=profile, stage=stage, stage_name=stage_name,
            factory=factory, expected=expected, descriptor=document['descriptor'],
            field=FieldDescriptor.from_compiled(document['descriptor'], document['descriptor_digest']),
            source=keys(TENANT), target=b9.target_keys(TENANT), max_bytes=4096, workers=[])
        f.baseline = b9.source_snapshot(f)
        f.current = tuple(f.baseline[2].items())
        assert f.field.record_codec == ('int64-be/v1' if native_type == 'bigint' else 'uuid16/v1')
        assert f.field.equality == profile.endswith('-equality')
        assert len(f.current) == 9 and list(dict(f.current)) == list(expected)
        assert expected != {r: v for r, (_, v) in app.source.items()}
        assert {r: independent_open(body, f.descriptor, TENANT, r) for r, body in f.current} == expected
        # Frozen B9A must reject here with PreparationFailure.code=unsupported_profile.
        # A different setup failure is a fixture blocker, not the intended RED.
        f.artifact = b9.bind_artifact(f)
        yield f


def logical_bytes(f, rows):
    identity = 24 if f.profile.startswith('bigint-') else 32
    overhead = 74 if f.field.equality else 42
    return sum(identity + (0 if body is None else 3 * len(body) - overhead) for _, body in rows)


def finish(f):
    for _ in range(6):  # Five two-row-limited batches and terminal verification.
        result = b9.enter(f)
        if result.status == 'PREPARED_INACTIVE':
            return result
        assert result.status == 'PREPARING'
    pytest.fail('nine-row profile did not complete inactive preparation')


def assert_profile_parity(f):
    rows = b9.staged(f)
    native = int if f.profile.startswith('bigint-') else UUID
    assert all(type(r) is native and type(t) is UUID and t == TENANT for r, t, *_ in rows)
    assert [r for r, *_ in rows] == list(f.expected)
    target_context = next(w.context for w in f.target.policy.wrappers if w.context.generation == 2)
    assert {r: independent_open(None if body is None else bytes(body), f.descriptor,
        TENANT, r, target_context) for r, _, _, _, body in rows} == f.expected
    for r, _, _, commitment, body in rows:
        old = dict(f.current)[r]
        assert (body is None) == (old is None)
        assert bytes(commitment).hex() == b9.row_commitment(r, old)
        if body is not None:
            body = bytes(body)
            assert body[:6] == old[:6] and int.from_bytes(body[6:10], 'big') == 2
            assert len(body) == len(old)
            # Storage-only has no term bytes. Do not compare nonce/ciphertext as terms.
            assert body[10:46 if f.field.equality else 14] == old[10:46 if f.field.equality else 14]
            if not f.field.equality:
                assert body[10:14] == b'\0' * 4
    assert b9.source_snapshot(f) == f.baseline and f.app.pin.phase == 'ACTIVE'
    with f.factory(tenant_id=TENANT) as session:
        observed = session.execute(select(f.app.Customer.id, f.app.Customer.name)).all()
        assert dict(observed) == f.expected and all(type(r) is native for r, _ in observed)
    state = b9.state(f)
    assert set(state) == b9.STATE_FIELDS and state['schema'] == b9.SCHEMA
    assert state['kind'] == 'INACTIVE_PAYLOAD_PREPARATION' and state['phase'] == 'PREPARED_INACTIVE'
    assert state['source_operation_id'] == str(f.app.plan.operation_id)
    assert state['source_plan_digest'] == f.app.plan.digest and state['artifact_digest'] == f.artifact.digest
    assert state['source_revision'] == {'row_count': 9,
        'membership': b9.digest([str(r) for r, _ in f.current]),
        'content': b9.digest([{'record_id': str(r), 'source_commitment': b9.row_commitment(r, body)} for r, body in f.current])}
    assert len(state['batches']) == 5
    for ordinal, batch in enumerate(state['batches'], 1):
        subset = f.current[(ordinal-1)*2:ordinal*2]
        persisted = [row for row in rows if row[2] == ordinal]
        assert set(batch) == b9.BATCH_FIELDS
        assert batch['ordinal'] == ordinal and batch['row_count'] == len(subset)
        assert batch['cursor_before'] == (None if ordinal == 1 else str(f.current[(ordinal-1)*2-1][0]))
        assert batch['cursor_after'] == str(subset[-1][0])
        assert batch['rows'] == [{'record_id': str(r), 'source_commitment': b9.row_commitment(r, body),
                                 'is_null': body is None} for r, body in subset]
        assert batch['target_commitment'] == b9.target_commitment(persisted)
        assert batch['logical_bytes'] == logical_bytes(f, subset) <= f.max_bytes
    assert state['verification'] == {'row_count': 9, 'target_commitment': b9.target_commitment(rows)}
    with f.app.owner.connect() as c:
        assert c.exec_driver_sql(f'SELECT DISTINCT operation_id FROM {f.stage}').scalars().all() == [f.artifact.operation_id]
        assert c.exec_driver_sql(f'SELECT operation_id FROM "{f.app.schema}"._cryptalis_journal ORDER BY operation_id').scalars().all() == sorted([f.app.plan.operation_id, f.artifact.operation_id])
        assert c.exec_driver_sql('''SELECT count(*) FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname=%s AND c.relkind='r' AND c.relname LIKE '%%journal%%' ''', (f.app.schema,)).scalar_one() == 1
        for table, column in ((f.stage, 'record_id'), (f'"{f.app.schema}".customer', 'id')):
            assert c.exec_driver_sql('''SELECT atttypid FROM pg_catalog.pg_attribute
                WHERE attrelid=pg_catalog.to_regclass(%s) AND attname=%s''', (table, column)).scalar_one() == (20 if native is int else 2950)


@pytest.mark.parametrize('profile', PROFILES)
def test_profile_current_values_same_journal_inactive(profile, monkeypatch):
    with profile_fixture(profile) as f:
        assert f.artifact.canonical_bytes == b9.canonical(f.artifact.document)
        assert f.artifact.digest == hashlib.sha256(f.artifact.canonical_bytes).hexdigest()
        before = b9.native_snapshot(f)
        assert b9.enter(f, 'start').status == 'PREPARING'
        assert b9.staged(f) == [] and b9.state(f)['batches'] == []
        finish(f); assert_profile_parity(f)
        assert b9.native_snapshot(f)[2] == before[2]
        calls = b9.count_seals(monkeypatch)
        before = b9.native_snapshot(f)
        assert b9.enter(f, 'inspect').status == 'PREPARED_INACTIVE'
        assert calls == [] and b9.native_snapshot(f) == before


@pytest.mark.parametrize('profile', PROFILES)
def test_profile_restart_preserves_committed_prefix(profile, tmp_path):
    with profile_fixture(profile) as f:
        assert b9.enter(f, 'start').status == 'PREPARING'
        p = b9.worker(f, tmp_path, action='step', barrier='after_commit', ordinal=1)
        try:
            observation = b9.worker_line(p)
            assert observation['point'] == 'after_commit' and observation['ordinal'] == 1
            prefix, receipt = b9.staged(f), b9.state(f)['batches'][0]
            assert len(prefix) == 2
            p.kill(); assert p.wait(timeout=10) == -signal.SIGKILL
            b9.terminal_backend(f, observation['backend_pid'])
            sealed = []
            # Reuse the frozen contained worker in one-step mode. Its four-step
            # finish cap cannot cover nine rows; each step reconstructs keys.
            for _ in range(5):
                q = b9.worker(f, tmp_path, action='step')
                try:
                    result = b9.completed_worker(q)
                    sealed.extend(result['sealed_records'])
                    assert b9.staged(f)[:2] == prefix and b9.state(f)['batches'][0] == receipt
                finally:
                    b9.stop_worker(q)
                if result['status'] == 'PREPARED_INACTIVE':
                    break
                assert result['status'] == 'PREPARING'
            assert result['status'] == 'PREPARED_INACTIVE'
            assert sealed == [str(r) for r, _ in f.current[2:]]
            assert_profile_parity(f)
            before = b9.native_snapshot(f)
            q = b9.worker(f, tmp_path, action='inspect')
            try:
                result = b9.completed_worker(q)
                assert result['status'] == 'PREPARED_INACTIVE' and result['sealed_records'] == []
            finally:
                b9.stop_worker(q)
            assert b9.native_snapshot(f) == before
        finally:
            b9.stop_worker(p)

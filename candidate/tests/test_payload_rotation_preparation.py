"""Inactive payload transforms: independent vectors and current native values.

All roots are public fixtures. No writer policy, runtime schema or external pin
is changed. Native staging tables below are test-owned inactive observations.
"""
from dataclasses import replace
import hashlib
import importlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

import pytest
from sqlalchemy import select

from cryptalis.crypto import (
    AuthenticationFailed, CryptoFailure, DevelopmentKeyProvider, InvalidContext,
    KeyContext, KeyPolicy, Keyring, KeyUnavailable, RepresentationMismatch,
    WrappedRoot, open_text, seal_text,
)
from cryptalis.crypto.cf1 import FieldDescriptor
from reference_cf1_vectors import encrypt, hkdf, tuple_bytes


VECTORS = json.loads((Path(__file__).parent / 'fixtures/cf1_vectors.json').read_text())['vectors']
NEW_ROOT = bytes(range(64, 96))  # PUBLIC fixture material only.
NEW_ID = UUID(int=8108)


def prepare(rows, field, tenant, source, target, **bounds):
    return importlib.import_module('cryptalis.crypto._payload_rotation').prepare_payload_rotation_batch(
        rows, field, tenant, source=source, target=target,
        max_rows=bounds.get('max_rows', 1000), max_bytes=bounds.get('max_bytes', 64 * 1024 * 1024))


def fixture(vector, *, max_age=60):
    field = FieldDescriptor.from_compiled(vector['descriptor'], vector['descriptor_digest'])
    tenant = UUID(vector['tenant_id'])
    record = vector['record_id'] if field.record_codec == 'int64-be/v1' else UUID(vector['record_id'])
    provider = DevelopmentKeyProvider()
    payload = KeyContext(field.domain_id, tenant, 'payload', UUID(vector['payload_root_id']), vector['payload_generation'])
    wrappers = [provider.wrap(bytes.fromhex(vector['payload_root']), payload)]
    if field.equality:
        search = KeyContext(field.domain_id, tenant, 'search', UUID(vector['search_root_id']), vector['search_generation'])
        wrappers.append(provider.wrap(bytes.fromhex(vector['search_root']), search))
    policy = KeyPolicy(field.domain_id, tenant, tuple(wrappers), payload.generation,
                       vector['search_generation'] or None)
    changed = replace(payload, root_id=NEW_ID, generation=payload.generation + 1)
    successor = replace(policy, wrappers=policy.wrappers + (provider.wrap(NEW_ROOT, changed),),
                        payload_generation=changed.generation)
    return SimpleNamespace(vector=vector, field=field, tenant=tenant, record=record,
        provider=provider, payload=payload, changed=changed,
        source=Keyring(policy, {provider.provider_id: provider}, max_age=max_age),
        target=Keyring(successor, {provider.provider_id: provider}, max_age=max_age))


def independent_frame(f, value, nonce, *, target):
    """Independent stdlib KDF/framing plus existing RFC8452 reference AEAD."""
    v = f.vector
    context = f.changed if target else f.payload
    root = NEW_ROOT if target else bytes.fromhex(v['payload_root'])
    record = (tuple_bytes(b'int64', f.record.to_bytes(8, 'big', signed=True))
              if type(f.record) is int else f.record.bytes)
    salt = hashlib.sha256(tuple_bytes(b'CF1/root', context.domain_id.bytes,
        context.tenant_id.bytes, context.root_id.bytes, context.generation.to_bytes(4, 'big'))).digest()
    key = hkdf(root, salt, tuple_bytes(b'CF1/payload-key', f.field.field_id.bytes, record), 32)
    header = (bytes.fromhex('4346310001') + bytes([int(f.field.equality)]) +
        context.generation.to_bytes(4, 'big') + v['search_generation'].to_bytes(4, 'big') + bytes.fromhex(v['term']))
    digest = hashlib.sha256(json.dumps(v['descriptor'], sort_keys=True,
        separators=(',', ':'), ensure_ascii=False).encode()).digest()
    aad = tuple_bytes(b'CF1/payload', context.domain_id.bytes, f.tenant.bytes,
                     f.field.field_id.bytes, record, digest, header)
    return header + nonce + encrypt(key, nonce, value.encode('utf8'), aad)


def logical_bytes(rows, field):
    # Source frame + prospective target frame + decoded UTF8 + UUID tenant
    # and native record bytes. Excludes Python/driver/provider overhead.
    overhead = 74 if field.equality else 42
    identity = 16 + (8 if field.record_codec == 'int64-be/v1' else 16)
    return sum(identity + (0 if frame is None else 2 * len(frame) + len(frame) - overhead)
               for _, frame in rows)


@pytest.mark.parametrize('vector', VECTORS, ids=lambda v: v['name'])
def test_frozen_source_and_independent_target_vector(vector):
    f = fixture(vector)
    original = bytes.fromhex(vector['frame'])
    assert independent_frame(f, vector['text'], bytes.fromhex(vector['nonce']), target=False) == original
    source, target = f.source.prepare(), f.target.prepare()
    rows = ((f.record, original),)
    result = prepare(rows, f.field, f.tenant, source, target)
    assert type(result) is tuple and result[0][0] == f.record
    rotated = result[0][1]
    header_size = 46 if f.field.equality else 14
    nonce = rotated[header_size:header_size + 12]
    assert nonce != bytes.fromhex(vector['nonce'])
    assert rotated == independent_frame(f, vector['text'], nonce, target=True)
    assert rotated[10:header_size] == original[10:header_size]
    assert open_text(rotated, f.field, f.tenant, f.record, target) == vector['text']
    assert open_text(original, f.field, f.tenant, f.record, source) == vector['text']
    assert rows == ((f.record, original),)


@pytest.mark.parametrize('vector', VECTORS, ids=lambda v: v['name'])
def test_null_empty_unicode_and_exact_logical_budget(vector):
    f = fixture(vector)
    source, target = f.source.prepare(), f.target.prepare()
    records = (1, 2, 3) if type(f.record) is int else tuple(UUID(int=i) for i in (1, 2, 3))
    expected = (None, '', 'current 雪 e\u0301')
    rows = tuple((record, seal_text(value, f.field, f.tenant, record, source))
                 for record, value in zip(records, expected))
    budget = logical_bytes(rows, f.field)
    with pytest.raises(InvalidContext):
        prepare(rows, f.field, f.tenant, source, target, max_bytes=budget - 1)
    with pytest.raises(InvalidContext):
        prepare(rows, f.field, f.tenant, source, target, max_rows=2)
    result = prepare(rows, f.field, f.tenant, source, target, max_rows=3, max_bytes=budget)
    assert tuple(open_text(frame, f.field, f.tenant, record, target) for record, frame in result) == expected
    assert result[0][1] is None


@pytest.mark.parametrize('fault', ['tenant', 'field', 'record', 'late_tag', 'historical_source',
                                 'search_generation', 'search_material', 'payload_material', 'payload_identity'])
def test_exact_binding_and_late_authentication_failure_return_no_batch(fault):
    f = fixture(VECTORS[1])
    source = f.source.prepare()
    target = f.target.prepare()
    rows = ((f.record, bytes.fromhex(f.vector['frame'])),)
    field, tenant = f.field, f.tenant
    if fault == 'tenant':
        tenant = UUID(int=919)
    elif fault == 'field':
        field = replace(field, field_id=UUID(int=920))
    elif fault == 'record':
        rows = ((UUID(int=921), rows[0][1]),)
    elif fault == 'late_tag':
        second = UUID(int=922)
        body = seal_text('second current value', field, tenant, second, source)
        rows += ((second, body[:-1] + bytes([body[-1] ^ 1])),)
    elif fault == 'historical_source':
        source, target = target, source  # Source reader knows old frame, but it is not the selected source generation.
    else:
        policy = f.target.policy
        wrappers = list(policy.wrappers)
        if fault.startswith('search_'):
            i = next(i for i, w in enumerate(wrappers) if w.context.purpose == 'search')
            context = wrappers[i].context
            if fault == 'search_generation':
                context = replace(context, generation=context.generation + 1, root_id=UUID(int=923))
                policy = replace(policy, search_generation=context.generation,
                    wrappers=tuple(w for j, w in enumerate(wrappers) if j != i) +
                    (f.provider.wrap(bytes(range(96, 128)), context),))
            else:
                wrappers[i] = f.provider.wrap(bytes(range(96, 128)), context)
                policy = replace(policy, wrappers=tuple(wrappers))
        else:
            context = f.changed
            material = NEW_ROOT
            if fault == 'payload_material':
                material = bytes.fromhex(f.vector['payload_root'])
            else:
                context = replace(context, root_id=f.payload.root_id)
            policy = replace(policy, wrappers=tuple(w for w in wrappers if w.context.purpose != 'payload') +
                             (f.provider.wrap(material, context),))
        target = Keyring(policy, {f.provider.provider_id: f.provider}).prepare()
    before = rows
    with pytest.raises(CryptoFailure):
        prepare(rows, field, tenant, source, target)
    assert rows == before


@pytest.mark.parametrize('which', ['source', 'target'])
@pytest.mark.parametrize('failure', ['pid', 'expiry_after_first_seal'])
def test_inherited_or_expired_material_cannot_return_a_partial_batch(which, failure, monkeypatch):
    import cryptalis.crypto.keys as key_module
    now = [100.0]
    monkeypatch.setattr(key_module, 'time', SimpleNamespace(
        monotonic=lambda: now[0], monotonic_ns=lambda: int(now[0] * 1e9)))
    f = fixture(VECTORS[1], max_age=10)
    first = (f.source if which == 'source' else f.target).prepare()
    now[0] = 105.0
    second = (f.target if which == 'source' else f.source).prepare()
    source, target = (first, second) if which == 'source' else (second, first)
    rows = tuple((UUID(int=i), seal_text('current-' + str(i), f.field, f.tenant, UUID(int=i), source)) for i in (1, 2))
    if failure == 'pid':
        if which == 'source': source = replace(source, _pid=-1)
        else: target = replace(target, _pid=-1)
    else:
        module = importlib.import_module('cryptalis.crypto._payload_rotation')
        actual = module.seal_text
        calls = []
        def expire(*args, **kwargs):
            result = actual(*args, **kwargs)
            calls.append(1)
            if len(calls) == 1: now[0] = 110.0
            return result
        monkeypatch.setattr(module, 'seal_text', expire)
    before = rows
    with pytest.raises(KeyUnavailable):
        prepare(rows, f.field, f.tenant, source, target)
    assert rows == before


@pytest.mark.parametrize('which', ['source', 'target'])
@pytest.mark.parametrize('row_count', [1, 2])
def test_expiry_after_final_seal_cannot_return_the_completed_batch(which, row_count, monkeypatch):
    """No next CF1 operation can substitute for the final recheck."""
    import cryptalis.crypto.keys as key_module
    now = [100.0]
    monkeypatch.setattr(key_module, 'time', SimpleNamespace(
        monotonic=lambda: now[0], monotonic_ns=lambda: int(now[0] * 1e9)))
    f = fixture(VECTORS[1], max_age=10)
    first = (f.source if which == 'source' else f.target).prepare()
    now[0] = 105.0
    second = (f.target if which == 'source' else f.source).prepare()
    source, target = (first, second) if which == 'source' else (second, first)
    rows = tuple((UUID(int=i), seal_text('current-' + str(i), f.field, f.tenant,
                  UUID(int=i), source)) for i in range(1, row_count + 1))
    before = rows
    module = importlib.import_module('cryptalis.crypto._payload_rotation')
    actual = module.seal_text
    completed = []
    def expire_after_success(*args, **kwargs):
        result = actual(*args, **kwargs)
        completed.append(True)
        if len(completed) == row_count:
            now[0] = 110.0
        return result
    monkeypatch.setattr(module, 'seal_text', expire_after_success)
    with pytest.raises(KeyUnavailable):
        prepare(rows, f.field, f.tenant, source, target)
    assert completed == [True] * row_count
    assert rows == before


@pytest.mark.parametrize('row_count', [1, 2])
def test_pid_change_after_final_seal_cannot_return_the_completed_batch(row_count, monkeypatch):
    """Controlled PID observation; actual fork controls remain in the CF1 suite."""
    import cryptalis.crypto.keys as key_module
    f = fixture(VECTORS[1])
    source, target = f.source.prepare(), f.target.prepare()
    rows = tuple((UUID(int=i), seal_text('current-' + str(i), f.field, f.tenant,
                  UUID(int=i), source)) for i in range(1, row_count + 1))
    before = rows
    module = importlib.import_module('cryptalis.crypto._payload_rotation')
    actual = module.seal_text
    completed = []
    real_pid = os.getpid()
    def change_pid_after_success(*args, **kwargs):
        result = actual(*args, **kwargs)
        completed.append(True)
        if len(completed) == row_count:
            monkeypatch.setattr(key_module, 'os', SimpleNamespace(getpid=lambda: real_pid + 1))
        return result
    monkeypatch.setattr(module, 'seal_text', change_pid_after_success)
    with pytest.raises(KeyUnavailable):
        prepare(rows, f.field, f.tenant, source, target)
    assert completed == [True] * row_count
    assert rows == before


@pytest.mark.parametrize('bad', ['duplicate', 'iterator', 'row_limit', 'byte_limit', 'same_generation'])
def test_invalid_batch_shape_and_limits_refuse_before_transformation(bad, monkeypatch):
    f = fixture(VECTORS[1])
    source, target = f.source.prepare(), f.target.prepare()
    rows = ((f.record, bytes.fromhex(f.vector['frame'])),)
    bounds = {}
    if bad == 'duplicate': rows += rows
    elif bad == 'iterator': rows = iter(rows)
    elif bad == 'row_limit': bounds['max_rows'] = 5001
    elif bad == 'byte_limit': bounds['max_bytes'] = 1024 ** 3 + 1
    else: target = source
    module = importlib.import_module('cryptalis.crypto._payload_rotation')
    monkeypatch.setattr(module, 'open_text', lambda *a, **k: pytest.fail('Invalid batch reached source transformation'))
    with pytest.raises(InvalidContext):
        prepare(rows, f.field, f.tenant, source, target, **bounds)


def test_native_current_values_inactive_staging_and_transform_back():
    from test_migration import application, run, publish, keys, TENANT, PROVIDER, independent_open, frames, PublicFixtureProvider
    from test_retained_profile_safety_oracles import snapshot
    from cryptalis.sqlalchemy import attach
    with application() as app:
        with app.owner.begin() as connection:
            connection.exec_driver_sql(f'CREATE TABLE "{app.schema}".native_rotation_reference AS SELECT id,tenant_id,name,label FROM "{app.schema}".customer')
        run(app); publish(app)
        descriptor_doc = app.plan.document['lock']['models'][0]['fields'][0]
        field = FieldDescriptor.from_compiled(descriptor_doc['descriptor'], descriptor_doc['descriptor_digest'])
        source_ring = keys(TENANT)
        old_payload = next(w.context for w in source_ring.policy.wrappers if w.context.purpose == 'payload')
        new_payload = replace(old_payload, root_id=NEW_ID, generation=2)
        target_ring = Keyring(replace(source_ring.policy,
            wrappers=source_ring.policy.wrappers + (WrappedRoot(PROVIDER, new_payload, b'PUBLIC TEST WRAPPER'),),
            payload_generation=2), {PROVIDER: PublicFixtureProvider()})
        source, target = source_ring.prepare(), target_ring.prepare()
        backup = frames(app, True)
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes, keys=keys, deployment=(app.plan, app.pin))
        edited, deleted, inserted = (UUID(int=i) for i in (101, 104, 120))
        with factory(tenant_id=TENANT) as session:
            session.get(app.Customer, edited).name = 'current before preparation 雪'
            session.delete(session.get(app.Customer, deleted))
            session.add(app.Customer(id=inserted, tenant_id=TENANT, name='new current 😀', label='new'))
            session.commit()
        with app.owner.begin() as connection:
            connection.exec_driver_sql(f'UPDATE "{app.schema}".native_rotation_reference SET name=%s WHERE id=%s', ('current before preparation 雪', edited))
            connection.exec_driver_sql(f'DELETE FROM "{app.schema}".native_rotation_reference WHERE id=%s', (deleted,))
            connection.exec_driver_sql(f'INSERT INTO "{app.schema}".native_rotation_reference VALUES (%s,%s,%s,%s)', (inserted, TENANT, 'new current 😀', 'new'))
            expected = dict(connection.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".native_rotation_reference ORDER BY id').all())
        current = tuple(sorted(frames(app, True).items()))
        assert {r: independent_open(b, descriptor_doc['descriptor'], TENANT, r) for r, b in current} == expected
        before = snapshot(app)
        rotated = prepare(current, field, TENANT, source, target)
        with app.owner.begin() as connection:
            connection.exec_driver_sql(f'CREATE TABLE "{app.schema}".inactive_payload_stage (id uuid PRIMARY KEY, frame bytea)')
            connection.exec_driver_sql(f'INSERT INTO "{app.schema}".inactive_payload_stage VALUES (%s,%s)', list(rotated))
            stored = connection.exec_driver_sql(f'SELECT id,frame FROM "{app.schema}".inactive_payload_stage ORDER BY id').all()
        assert {r: independent_open(bytes(b) if b is not None else None, descriptor_doc['descriptor'], TENANT, r, new_payload) for r, b in stored} == expected
        assert snapshot(app) == before
        assert all(b is None or b[10:46] == dict(current)[r][10:46] for r, b in rotated)

        # Inactive local feasibility oracle: transform a later current target
        # edit back, rather than restoring its earlier source/backup value.
        later = 'edited after inactive transform e\u0301'
        with app.owner.begin() as connection:
            connection.exec_driver_sql(f'UPDATE "{app.schema}".inactive_payload_stage SET frame=%s WHERE id=%s',
                (seal_text(later, field, TENANT, edited, target), edited))
            connection.exec_driver_sql(f'UPDATE "{app.schema}".native_rotation_reference SET name=%s WHERE id=%s', (later, edited))
            staged = tuple((r, bytes(b) if b is not None else None) for r, b in connection.exec_driver_sql(f'SELECT id,frame FROM "{app.schema}".inactive_payload_stage ORDER BY id'))
            expected = dict(connection.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".native_rotation_reference ORDER BY id').all())
        returned = prepare(staged, field, TENANT, target, source)
        assert {r: independent_open(b, descriptor_doc['descriptor'], TENANT, r) for r, b in returned} == expected
        assert expected[edited] == later
        assert snapshot(app) == before and dict(current) == frames(app, True)
        assert {r: independent_open(b, descriptor_doc['descriptor'], TENANT, r) for r, b in backup.items()} == {r: v for r, (_, v) in app.source.items()}

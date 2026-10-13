"""Finite, inactive rewrap proposals; exact root and existing-pin oracles."""
from dataclasses import replace
import hashlib
import importlib
import json
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from cryptalis import migration as m
from cryptalis.crypto import DevelopmentKeyProvider, KeyContext, KeyPolicy, Keyring, seal_text, open_text
from cryptalis.crypto._rewrap import prepare_rewrap
from test_cf1 import setup_keys, descriptor, TENANT, RECORD


def module():
    return importlib.import_module('cryptalis._rewrap_successor')


def fixture(*, historical=False, second_tenant=False, max_age=60):
    old, ring = setup_keys(equality=True, max_age=max_age)
    if historical:
        policy = ring.policy
        context = KeyContext(policy.domain_id, TENANT, 'payload', UUID(int=801), 3)
        wrapper = old.wrap(bytes(range(64, 96)), context)
        ring = Keyring(replace(policy, wrappers=policy.wrappers + (wrapper,), payload_generation=3),
                       {old.provider_id: old}, max_age=max_age)
    sources = {TENANT: ring}
    if second_tenant:
        tenant = UUID(int=802)
        policy = ring.policy
        contexts = [replace(w.context, tenant_id=tenant) for w in policy.wrappers]
        wrappers = tuple(old.wrap(hashlib.sha256(c._aad(old.provider_id)).digest(), c) for c in contexts)
        sources[tenant] = Keyring(replace(policy, tenant_id=tenant, wrappers=wrappers),
                                 {old.provider_id: old}, max_age=max_age)
    target = DevelopmentKeyProvider()
    targets = {t: Keyring(prepare_rewrap(r, target), {target.provider_id: target}, max_age=max_age)
               for t, r in sources.items()}
    doc = {'format': 'cryptalis.transition/retained-native-research-v0', 'kind': 'protect',
           'operation_id': str(uuid4()), 'target_id': str(uuid4()),
           'lock': {'domain_id': str(ring.policy.domain_id), 'models': []},
           'key_policies': {str(t): m._policy(r) for t, r in sources.items()}}
    source = m.MigrationPlan(m._canonical(doc))
    pin = m.DeploymentPin(source.target_id, source.operation_id, source.digest, 'ACTIVE')
    return SimpleNamespace(source=source, pin=pin, sources=sources, targets=targets, provider=target)


def prepare(f):
    return module().prepare(f.source, source_pin=f.pin, source_keys=f.sources, target_keys=f.targets)


def verify(plan, f):
    return module().verify(plan, f.source, source_pin=f.pin, source_keys=f.sources, target_keys=f.targets)


def test_exact_roots_historical_readers_and_immutable_source_survive():
    f = fixture(historical=True, second_tenant=True)
    original_artifact = f.source.artifact
    policies = {t: r.policy for t, r in f.sources.items()}
    field = descriptor(equality=True)
    frame = seal_text('é e\u0301 雪', field, TENANT, RECORD, f.sources[TENANT].prepare())
    plan = prepare(f)
    assert plan.operation_id != f.source.operation_id
    assert plan.target_id == f.source.target_id
    assert plan.document['source_artifact_digest'] == f.source.digest
    assert plan.document['schema_lock_digest'] == hashlib.sha256(f.source.lock_bytes).hexdigest()
    assert set(plan.document['inventory']) == {str(t) for t in f.sources}
    assert f.source.artifact == original_artifact
    assert {t: r.policy for t, r in f.sources.items()} == policies
    assert module().RootRewrapPlan(plan.artifact) == plan
    assert verify(plan, f) is None
    for keys in (f.sources[TENANT], f.targets[TENANT]):
        assert open_text(frame, field, TENANT, RECORD, keys.prepare()) == 'é e\u0301 雪'
    # Existing active-policy admission must continue rejecting the new artifact.
    with pytest.raises(m.TransitionFailure, match='external_policy_mismatch'):
        m._admit(plan, m.DeploymentPin(plan.target_id, plan.operation_id, plan.digest, 'ACTIVE'))
    with pytest.raises(m.TransitionFailure, match='key_policy_changed'):
        m._ring(f.targets[TENANT], TENANT, f.source)


@pytest.mark.parametrize('fault', ['phase', 'digest', 'operation', 'target'])
def test_foreign_or_nonactive_source_pin_refuses_before_provider(fault):
    f = fixture()
    changes = {'phase': 'ACTIVATING', 'digest': 'a' * 64, 'operation': uuid4(), 'target': uuid4()}
    name = {'digest': 'plan_digest', 'operation': 'operation_id', 'target': 'target_id'}.get(fault, fault)
    f.pin = replace(f.pin, **{name: changes[fault]})
    f.provider.unwrap = lambda *args: pytest.fail('provider called before source admission')
    with pytest.raises(m.TransitionFailure):
        prepare(f)


@pytest.mark.parametrize('fault', ['missing_source', 'missing_target', 'extra_source', 'extra_target',
                                  'wrong_tenant', 'changed_generation', 'missing_history', 'different_root'])
def test_incomplete_or_changed_inventory_is_refused(fault):
    f = fixture(historical=True)
    if fault == 'missing_source': f.sources.clear()
    elif fault == 'missing_target': f.targets.clear()
    elif fault == 'extra_source': f.sources[uuid4()] = f.sources[TENANT]
    elif fault == 'extra_target': f.targets[uuid4()] = f.targets[TENANT]
    else:
        ring = f.targets[TENANT]; p = ring.policy
        if fault == 'wrong_tenant': f.targets = {uuid4(): ring}
        elif fault == 'changed_generation':
            f.targets[TENANT] = Keyring(replace(p, payload_generation=1), {f.provider.provider_id: f.provider})
        elif fault == 'missing_history':
            f.targets[TENANT] = Keyring(replace(p, wrappers=p.wrappers[1:]), {f.provider.provider_id: f.provider})
        else:
            wrappers = list(p.wrappers)
            wrappers[0] = f.provider.wrap(b'Z' * 32, wrappers[0].context)
            f.targets[TENANT] = Keyring(replace(p, wrappers=tuple(wrappers)), {f.provider.provider_id: f.provider})
    with pytest.raises(m.TransitionFailure):
        prepare(f)


@pytest.mark.parametrize('fault', ['unknown_field', 'version', 'source_id', 'target_id', 'operation_id',
                                  'digest', 'inventory', 'generation', 'duplicate_root', 'whitespace'])
def test_strict_artifact_parser_rejects_ambiguous_proposals(fault):
    f = fixture(historical=True); plan = prepare(f); d = plan.document
    inventory = d['inventory'][str(TENANT)]
    if fault == 'unknown_field': d['unexpected'] = True
    elif fault == 'version': d['format'] = 'cryptalis.root-rewrap/research-v999'
    elif fault == 'source_id': d['source_operation_id'] = 'NOT_A_UUID'
    elif fault == 'target_id': d['target_id'] = str(UUID(int=0))
    elif fault == 'operation_id': d['operation_id'] = d['source_operation_id']
    elif fault == 'digest': d['source_artifact_digest'] = 'A' * 64
    elif fault == 'inventory': d['target_key_policies'].pop(str(TENANT))
    elif fault == 'generation': inventory['payload_generation'] = True
    elif fault == 'duplicate_root': inventory['roots'].append(inventory['roots'][0])
    raw = m._canonical(d) + (b' ' if fault == 'whitespace' else b'')
    with pytest.raises(m.TransitionFailure, match='invalid_rewrap_plan'):
        module().RootRewrapPlan(raw)


def test_changed_target_policy_after_preparation_requires_new_plan():
    f = fixture(); plan = prepare(f)
    other = DevelopmentKeyProvider()
    f.targets[TENANT] = Keyring(prepare_rewrap(f.sources[TENANT], other), {other.provider_id: other})
    with pytest.raises(m.TransitionFailure): verify(plan, f)


def test_later_tenant_provider_work_cannot_outlive_an_earlier_source_lease(monkeypatch):
    import cryptalis.crypto.keys as keys
    now = [100.0]
    monkeypatch.setattr(keys, 'time', SimpleNamespace(monotonic=lambda: now[0], monotonic_ns=lambda: int(now[0] * 1e9)))
    f = fixture(second_tenant=True, max_age=10)
    old_unwrap = f.provider.unwrap
    def unwrap(wrapper, context):
        root = old_unwrap(wrapper, context)
        if context.tenant_id == UUID(int=802) and context.purpose == 'search': now[0] += 10
        return root
    f.provider.unwrap = unwrap
    with pytest.raises(m.TransitionFailure): prepare(f)


def test_provider_detail_is_suppressed_and_original_reader_remains_available():
    f = fixture()
    def offline(*args): raise RuntimeError('PRIVATE_PROVIDER_DETAIL')
    f.provider.unwrap = offline
    with pytest.raises(m.TransitionFailure) as error: prepare(f)
    assert 'PRIVATE_PROVIDER_DETAIL' not in str(error.value)
    assert f.sources[TENANT].prepare().policy is f.sources[TENANT].policy


def test_interruption_propagates_without_a_plan():
    f = fixture()
    def interrupted(*args): raise KeyboardInterrupt()
    f.provider.unwrap = interrupted
    with pytest.raises(KeyboardInterrupt): prepare(f)


@pytest.mark.parametrize('warm', [False, True])
def test_changed_target_provider_identity_refuses_even_with_live_material(warm):
    f = fixture()
    if warm:
        f.targets[TENANT].prepare()
        f.provider.provider_id = uuid4()
    else:
        unwrap = f.provider.unwrap
        def changed(wrapper, context):
            result = unwrap(wrapper, context)
            if context.purpose == 'search': f.provider.provider_id = uuid4()
            return result
        f.provider.unwrap = changed
    with pytest.raises(m.TransitionFailure): prepare(f)


def test_cross_tenant_verification_rechecks_earliest_source_lease(monkeypatch):
    import cryptalis.crypto.keys as keys
    now = [100.0]
    monkeypatch.setattr(keys, 'time', SimpleNamespace(monotonic=lambda: now[0], monotonic_ns=lambda: int(now[0] * 1e9)))
    f = fixture(second_tenant=True, max_age=10)
    tenant = UUID(int=802)
    later = f.sources[tenant]
    f.sources[tenant] = Keyring(later.policy, later._providers, max_age=30)
    now[0] = 109.0
    unwrap = f.provider.unwrap
    def delayed(wrapper, context):
        result = unwrap(wrapper, context)
        if context.tenant_id == tenant and context.purpose == 'search': now[0] += 1.5
        return result
    f.provider.unwrap = delayed
    # Later source and both target leases are still valid. Only the earlier
    # source expires after its comparison, while a later tenant is preparing.
    with pytest.raises(m.TransitionFailure): prepare(f)
    assert f.sources[tenant].prepare().policy is later.policy
    for ring in f.targets.values(): assert ring.prepare().policy is ring.policy


def test_historical_frame_and_current_search_bytes_survive_candidate_binding():
    f = fixture(historical=True)
    ring = f.sources[TENANT]
    historic = Keyring(replace(ring.policy, payload_generation=1), ring._providers)
    field = descriptor(equality=True)
    old_frame = seal_text('retained historical value', field, TENANT, RECORD, historic.prepare())
    new_frame = seal_text('retained historical value', field, TENANT, RECORD, ring.prepare())
    assert old_frame[6:10] != new_frame[6:10]
    assert old_frame[14:46] == new_frame[14:46]
    prepare(f)
    for reader in (ring, f.targets[TENANT]):
        for frame in (old_frame, new_frame):
            assert open_text(frame, field, TENANT, RECORD, reader.prepare()) == 'retained historical value'


def test_live_warm_target_lease_is_not_immediate_provider_revocation():
    f = fixture()
    f.targets[TENANT].prepare()
    def offline(*args): raise RuntimeError('PRIVATE_PROVIDER_DETAIL')
    f.provider.unwrap = offline
    assert verify(prepare(f), f) is None


def test_real_compiled_source_candidate_changes_no_database_or_active_authority():
    from sqlalchemy import event, select
    from cryptalis import deprotection
    from cryptalis.crypto import FieldDescriptor
    from cryptalis.sqlalchemy import attach, PolicyMismatch
    from test_migration import application, run, publish, keys, frames, TENANT as database_tenant, independent_open
    with application() as app:
        run(app); publish(app)
        before = frames(app, True)
        artifact = app.plan.artifact
        model = app.plan.document['lock']['models'][0]
        with app.owner.connect() as connection:
            journal_before = connection.exec_driver_sql(
                f'SELECT operation_id,plan_digest,state FROM "{app.schema}"._cryptalis_journal ORDER BY operation_id').all()
            schema_before = m._facts(connection, model)
        source = keys(database_tenant)
        provider = DevelopmentKeyProvider()
        target = Keyring(prepare_rewrap(source, provider), {provider.provider_id: provider})
        proposal = module().prepare(app.plan, source_pin=app.pin,
                                    source_keys={database_tenant: source}, target_keys={database_tenant: target})
        assert proposal.document['schema_lock_digest'] == hashlib.sha256(app.plan.lock_bytes).hexdigest()
        field = model['fields'][0]
        expected = FieldDescriptor.from_compiled(field['descriptor'], field['descriptor_digest'])
        for record, frame in before.items():
            value = app.source[record][1]
            assert independent_open(frame, field['descriptor'], database_tenant, record) == value
            assert open_text(frame, expected, database_tenant, record, target.prepare()) == value
        # The source remains independently admitted. The inactive successor
        # fails the existing dispatcher before it can inspect or mutate SQL.
        m.check_deployment(app.plan, app.owner, pin=app.pin)
        candidate_pin = m.DeploymentPin(proposal.target_id, proposal.operation_id, proposal.digest, 'ACTIVE')
        with pytest.raises(m.TransitionFailure, match='external_policy_mismatch'):
            m.check_deployment(proposal, app.owner, pin=candidate_pin)
        sessions = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                          keys=lambda tenant: target, deployment=(app.plan, app.pin))
        emitted = []
        def observed(*args): emitted.append(True)
        event.listen(app.runtime, 'before_cursor_execute', observed)
        try:
            with pytest.raises(PolicyMismatch):
                with sessions(tenant_id=database_tenant) as session:
                    session.scalars(select(app.Customer)).all()
            assert not emitted
        finally:
            event.remove(app.runtime, 'before_cursor_execute', observed)
        with pytest.raises(m.TransitionFailure, match='key_policy_changed'):
            deprotection.plan(app.plan, app.owner, source_pin=app.pin,
                keys=lambda tenant: target, plaintext_runtime_role=app.role + '_not_created',
                backfill_rows_per_second=1000, verify_rows_per_second=1000,
                temporary_bytes_per_row=700, wal_bytes_per_row=2000)
        assert app.plan.artifact == artifact and frames(app, True) == before
        with app.owner.connect() as connection:
            assert connection.exec_driver_sql(
                f'SELECT operation_id,plan_digest,state FROM "{app.schema}"._cryptalis_journal ORDER BY operation_id').all() == journal_before
            assert m._facts(connection, model) == schema_before

"""Current-data recovery when an unchanged reverse operation sees key drift.

This rejects attempted payload/search policy changes. It does not implement
rotation, publish a successor, or grant a mixed-generation runtime policy.
"""
from dataclasses import replace
from uuid import UUID, uuid5

import pytest
from sqlalchemy import event, select

from cryptalis.crypto import Keyring, WrappedRoot
from cryptalis.migration import TransitionFailure
from cryptalis.sqlalchemy import attach
from test_deprotection import execute
from test_migration import (
    DOMAIN, FIELD_ID, PROVIDER, TABLE_ID, TENANT, PublicFixtureProvider,
    application, frames, independent_open, keys, publish, run,
)
from test_retained_profile_safety_oracles import snapshot
from test_retained_public_metadata import reverse


def decode(app, bodies):
    descriptor = app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
    return {identity: independent_open(body, descriptor, TENANT, identity)
            for identity, body in bodies.items()}


class UnusedPublicProvider(PublicFixtureProvider):
    def __init__(self):
        self.calls = 0

    def unwrap(self, wrapper, context):
        self.calls += 1
        return super().unwrap(wrapper, context)


def changed_ring(purpose, provider):
    source = keys(TENANT).policy
    old = next(wrapper for wrapper in source.wrappers if wrapper.context.purpose == purpose)
    context = replace(old.context, generation=2,
                      root_id=uuid5(DOMAIN, 'B7 public hypothetical ' + purpose))
    wrapper = WrappedRoot(PROVIDER, context, b'PUBLIC TEST WRAPPER')
    # Keep the original reader wrappers. Even a well-formed finite reader set
    # cannot authorize different active generations for this existing plan.
    policy = replace(source, wrappers=source.wrappers + (wrapper,),
                     **{purpose + '_generation': 2})
    return Keyring(policy, {PROVIDER: provider})


def staged_prefix(app, identities):
    column = '_cryptalis_' + FIELD_ID.hex + '_plain'
    with app.owner.connect() as connection:
        return connection.exec_driver_sql(
            f'SELECT id,"{column}" FROM "{app.schema}".customer '
            'WHERE id=ANY(%s) ORDER BY id', (list(identities),)).all()


@pytest.mark.parametrize('purpose', ['payload', 'search'])
@pytest.mark.parametrize('recovery', ['resume', 'abort'])
def test_generation_policy_drift_keeps_committed_prefix_and_current_data(purpose, recovery):
    with application() as app:
        with app.owner.connect() as connection:
            original = connection.exec_driver_sql(
                f'SELECT id,tenant_id,name,label FROM "{app.schema}".customer ORDER BY id').all()
        expected = {row[0]: tuple(row) for row in original}
        run(app)
        publish(app)
        source_artifact = app.plan.artifact
        backup = frames(app, True)
        backup_copy = dict(backup)
        assert decode(app, backup) == {row[0]: row[2] for row in original}
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=keys, deployment=(app.plan, app.pin))

        # Exercise update, NULL change, deletion and insertion after protection.
        # The first durable reverse prefix includes an edited value, so a stale
        # pre-protection snapshot cannot satisfy the final expected rows.
        edited, nulled, deleted, inserted = (UUID(int=i) for i in (101, 103, 104, 120))
        with factory(tenant_id=TENANT) as session:
            row = session.get(app.Customer, edited)
            row.name, row.label = 'current edited after protection 雪', 'current public label'
            session.get(app.Customer, nulled).name = None
            session.delete(session.get(app.Customer, deleted))
            session.add(app.Customer(id=inserted, tenant_id=TENANT,
                name='inserted after protection e\u0301', label='new public row'))
            session.commit()
        expected[edited] = (edited, TENANT, 'current edited after protection 雪', 'current public label')
        expected[nulled] = (nulled, TENANT, None, expected[nulled][3])
        del expected[deleted]
        expected[inserted] = (inserted, TENANT, 'inserted after protection e\u0301', 'new public row')
        current = frames(app, True)
        assert decode(app, current) == {identity: row[2] for identity, row in expected.items()}
        assert current != backup
        d, plan, pin, consent = reverse(app)
        execute(app, d, plan, pin, consent, 'EXPANDED')

        provider = UnusedPublicProvider()
        drifted = changed_ring(purpose, provider)
        calls = 0
        at_refusal = []
        refused = False
        sql_after_refusal = []

        def resolver(tenant):
            nonlocal calls, refused
            assert tenant == TENANT
            calls += 1
            if calls == 1:
                return keys(tenant)
            # A separate owner connection observes the actual committed first
            # chunk before the next chunk's policy is returned to admission.
            at_refusal.append(snapshot(app))
            refused = True
            return drifted

        def observe(connection, cursor, statement, parameters, context, many):
            if refused:
                sql_after_refusal.append(True)  # Do not retain SQL or values.

        event.listen(app.owner, 'before_cursor_execute', observe)
        try:
            with pytest.raises(TransitionFailure) as failure:
                d.apply(plan, app.owner, keys=resolver, pin=pin,
                    approval=app.approval, plaintext_approval=consent, chunk_size=2)
            assert failure.value.code == 'key_policy_changed'
            assert calls == 2 and provider.calls == 0
            assert sql_after_refusal == []
        finally:
            event.remove(app.owner, 'before_cursor_execute', observe)
        assert len(at_refusal) == 1 and snapshot(app) == at_refusal[0]
        assert frames(app, True) == current
        with app.owner.connect() as connection:
            state = connection.exec_driver_sql(
                f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',
                (plan.operation_id,)).scalar_one()
        progress = state['models'][str(TABLE_ID)]
        prefix_ids = tuple(sorted(expected)[:2])
        assert state['phase'] == 'EXPANDED'
        assert (progress['rows'], progress['chunks'], progress['cursor']) == (2, 1, str(prefix_ids[-1]))
        prefix = staged_prefix(app, prefix_ids)
        assert prefix == [(identity, expected[identity][2]) for identity in prefix_ids]

        if recovery == 'resume':
            restored = d.DeprotectionPlan(plan.artifact)
            execute(app, d, restored, pin, consent, 'BACKFILLED')
            assert staged_prefix(app, prefix_ids) == prefix
            assert frames(app, True) == current
            execute(app, d, restored, pin, consent)
        else:
            assert d.abort(plan, app.owner, pin=pin, approval=app.approval,
                           plaintext_approval=consent).phase == 'ABORTED'
            app.m.check_deployment(app.plan, app.owner, pin=app.pin)
            assert frames(app, True) == current
            with factory(tenant_id=TENANT) as session:
                observed = session.execute(select(app.Customer.id, app.Customer.tenant_id,
                    app.Customer.name, app.Customer.label).order_by(app.Customer.id)).all()
                assert observed == [expected[key] for key in sorted(expected)]
                session.get(app.Customer, edited).name = 'new current edit after abort 😀'
                session.commit()
            expected[edited] = (edited, TENANT, 'new current edit after abort 😀', expected[edited][3])
            newer_d, newer, newer_pin, newer_consent = reverse(app)
            execute(app, newer_d, newer, newer_pin, newer_consent)

        # Stop at the existing plaintext-pending boundary. No role handoff,
        # new writer credentials, or external publication is performed.
        with app.owner.connect() as connection:
            final = connection.exec_driver_sql(
                f'SELECT id,tenant_id,name,label FROM "{app.schema}".customer ORDER BY id').all()
        assert final == [expected[key] for key in sorted(expected)]
        assert app.plan.artifact == source_artifact
        assert backup == backup_copy
        assert decode(app, backup) == {row[0]: row[2] for row in original}

"""Real reverse-resume refusals preserve exact current values and metadata."""
import json
from dataclasses import replace
from uuid import UUID, uuid4

import pytest

from cryptalis.migration import DeploymentPin, TransitionFailure
from test_deprotection import prepared, execute, plaintext_role
from test_migration import application, keys

PHASES = ('EXPANDED', 'BACKFILLED', 'VERIFIED', 'PLAINTEXT_PENDING')


def snapshot(app, reverse):
    with app.owner.connect() as connection:
        present = connection.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)',
                                            (f'"{app.schema}"._cryptalis_journal',)).scalar_one()
        journal = connection.exec_driver_sql(
            f'SELECT operation_id,plan_digest,state FROM "{app.schema}"._cryptalis_journal ORDER BY operation_id').all() if present else None
        schemas = [app.m._facts(connection, model) for model in reverse.document['lock']['models']]
        guards = [app.m._guard_facts(connection, reverse, model) for model in reverse.document['lock']['models']]
        values = connection.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all()
    return journal, schemas, guards, values


def corrupt(app, reverse, fault):
    with app.owner.begin() as connection:
        journal = f'"{app.schema}"._cryptalis_journal'
        if fault == 'source_missing':
            connection.exec_driver_sql(f'DELETE FROM {journal} WHERE operation_id=%s', (app.plan.operation_id,))
        elif fault == 'source_digest':
            connection.exec_driver_sql(f'UPDATE {journal} SET plan_digest=%s WHERE operation_id=%s',
                                      ('f' * 64, app.plan.operation_id))
        elif fault == 'source_phase':
            connection.exec_driver_sql(f"UPDATE {journal} SET state=jsonb_set(state,'{{phase}}',%s::jsonb) WHERE operation_id=%s",
                                      (json.dumps('ACTIVE'), app.plan.operation_id))
        elif fault == 'link_missing':
            connection.exec_driver_sql(f"UPDATE {journal} SET state=state-'source_operation_id' WHERE operation_id=%s",
                                      (reverse.operation_id,))
        else:
            name = 'source_operation_id' if fault == 'link_operation' else 'source_plan_digest'
            value = str(uuid4()) if fault == 'link_operation' else 'a' * 64
            connection.exec_driver_sql(f"UPDATE {journal} SET state=jsonb_set(state,'{{{name}}}',%s::jsonb) WHERE operation_id=%s",
                                      (json.dumps(value), reverse.operation_id))


@pytest.mark.parametrize('phase', PHASES)
@pytest.mark.parametrize('fault', ['source_missing', 'source_digest', 'source_phase',
                                  'link_operation', 'link_digest', 'link_missing'])
def test_reverse_resume_refuses_inconsistent_predecessor_without_effects(phase, fault):
    with application() as app:
        d, plan, pin, consent = prepared(app)
        execute(app, d, plan, pin, consent, phase)
        corrupt(app, plan, fault)
        before = snapshot(app, plan)
        failure = None
        try:
            execute(app, d, d.DeprotectionPlan(plan.artifact), pin, consent)
        except TransitionFailure as error:
            failure = error
        after = snapshot(app, plan)
        assert after == before, 'Inconsistent predecessor allowed reverse data/schema/journal progress'
        assert failure is not None, 'Inconsistent predecessor was reported as successful reverse state'
        assert failure.code == 'source_state_changed'


@pytest.mark.parametrize('phase', PHASES)
def test_exact_predecessor_allows_artifact_reconstruction_and_current_data_resume(phase):
    with application() as app:
        d, plan, pin, consent = prepared(app)
        execute(app, d, plan, pin, consent, phase)
        result = execute(app, d, d.DeprotectionPlan(plan.artifact), pin, consent)
        assert result.phase == 'PLAINTEXT_PENDING'
        with app.owner.connect() as connection:
            assert dict(connection.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".customer').all()) == {
                identity: value for identity, (_, value) in app.source.items()}
            source = connection.exec_driver_sql(
                f'SELECT plan_digest,state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',
                (app.plan.operation_id,)).one()
            assert source[0] == app.plan.digest and source[1]['phase'] == 'DEPROTECTING'


def test_completed_abort_stays_idempotent_when_a_new_reverse_owns_the_source():
    with application() as app:
        d, old, old_pin, old_consent = prepared(app)
        execute(app, d, old, old_pin, old_consent, 'BACKFILLED')
        assert d.abort(old, app.owner, pin=old_pin, approval=app.approval,
                       plaintext_approval=old_consent).phase == 'ABORTED'
        newer = d.plan(app.plan, app.owner, source_pin=app.pin, keys=keys,
                       plaintext_runtime_role=plaintext_role(), backfill_rows_per_second=1000,
                       verify_rows_per_second=1000, temporary_bytes_per_row=700, wal_bytes_per_row=2000)
        new_pin = DeploymentPin(newer.target_id, newer.operation_id, newer.digest, 'PREPARED')
        new_consent = d.PlaintextApproval(newer.target_id, newer.operation_id, newer.digest,
                                         True, 'Synthetic retained public-root backup reader')
        execute(app, d, newer, new_pin, new_consent, 'EXPANDED')
        before = snapshot(app, newer)
        assert d.abort(old, app.owner, pin=old_pin, approval=app.approval,
                       plaintext_approval=old_consent).phase == 'ABORTED'
        assert snapshot(app, newer) == before
        assert execute(app, d, newer, new_pin, new_consent).phase == 'PLAINTEXT_PENDING'



def restore_source_link(app, reverse, name):
    value = str(app.plan.operation_id) if name == 'source_operation_id' else app.plan.digest
    with app.owner.begin() as connection:
        connection.exec_driver_sql(
            f"UPDATE \"{app.schema}\"._cryptalis_journal SET state=jsonb_set(state,'{{{name}}}',%s::jsonb) WHERE operation_id=%s",
            (json.dumps(value), reverse.operation_id))


def test_abort_refuses_changed_reverse_link_then_resumes_after_exact_repair():
    with application() as app:
        d, plan, pin, consent = prepared(app)
        execute(app, d, plan, pin, consent, 'BACKFILLED')
        corrupt(app, plan, 'link_operation')
        before = snapshot(app, plan)
        with pytest.raises(TransitionFailure, match='source_state_changed'):
            d.abort(plan, app.owner, pin=pin, approval=app.approval, plaintext_approval=consent)
        assert snapshot(app, plan) == before
        # Fixture-only exact restoration from the unchanged authenticated plan;
        # the implementation performs no journal repair or authority inference.
        restore_source_link(app, plan, 'source_operation_id')
        assert d.abort(plan, app.owner, pin=pin, approval=app.approval,
                       plaintext_approval=consent).phase == 'ABORTED'
        app.m.check_deployment(app.plan, app.owner, pin=app.pin)


def test_active_removal_refuses_changed_reverse_link_and_preserves_current_edits():
    import psycopg
    from test_deprotection import plaintext_url
    from test_migration import frames, independent_open, TENANT
    with application() as app:
        d, plan, pin, consent = prepared(app)
        backup = frames(app, True)
        descriptor = app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        for identity, frame in backup.items():
            assert independent_open(frame, descriptor, TENANT, identity) == app.source[identity][1]
        execute(app, d, plan, pin, consent)
        assert execute(app, d, plan, replace(pin, phase='PLAINTEXT_ACTIVATING'),
                       consent, 'PLAINTEXT_ACTIVE').phase == 'PLAINTEXT_ACTIVE'
        # Existing authorized plaintext fixture role; no account or credential
        # is created. Real native data changes must survive refused removal.
        expected = {identity: value for identity, (_, value) in app.source.items()}
        identity = UUID(int=105)
        expected[identity] = 'edited after plaintext publication 雪'
        with psycopg.connect(plaintext_url()) as connection:
            assert dict(connection.execute(f'SELECT id,name FROM "{app.schema}".customer').fetchall()) == {
                identity: value for identity, (_, value) in app.source.items()}
            connection.execute(f'UPDATE "{app.schema}".customer SET name=%s WHERE id=%s',
                               (expected[identity], identity))
        corrupt(app, plan, 'link_digest')
        before = snapshot(app, plan)
        proof = d.RemovalApproval(plan.digest, 'Synthetic native plaintext read and committed write above',
                                  'Retained synthetic public-root frames independently decoded above', True)
        removing = replace(pin, phase='REMOVING')
        with pytest.raises(TransitionFailure, match='source_state_changed'):
            d.remove(plan, app.owner, pin=removing, approval=app.approval,
                     plaintext_approval=consent, removal_approval=proof)
        assert snapshot(app, plan) == before
        restore_source_link(app, plan, 'source_plan_digest')
        assert d.remove(plan, app.owner, pin=removing, approval=app.approval,
                        plaintext_approval=consent, removal_approval=proof).phase == 'REMOVED'
        with psycopg.connect(plaintext_url()) as connection:
            assert dict(connection.execute(f'SELECT id,name FROM "{app.schema}".customer').fetchall()) == expected

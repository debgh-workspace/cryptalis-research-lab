"""Generation-1-only characterization. PASS is NOT pending-switch safety.

The two deliberately named gap tests freeze current source-derived behavior.
Synthetic unsupported journal phases are fixture data, never authorized product
states. No live payload replacement or generation-2 publication is performed.
"""
from contextlib import contextmanager
import copy
import json

import pytest
from sqlalchemy import Column, MetaData, Table, Text, Uuid, event, select
from sqlalchemy.orm import registry

from cryptalis import migration
from cryptalis.sqlalchemy import attach, PolicyMismatch
from test_migration import TENANT, engine, frames, keys
import test_payload_rotation_journal as b9

UNSUPPORTED_PENDING = 'TEST_ONLY_UNSUPPORTED_ROTATION_PENDING'


def _read(factory, customer):
    with factory(tenant_id=TENANT) as session:
        return dict(session.execute(select(customer.id, customer.name)).all())


@contextmanager
def _fresh_attachment(f, key_source=keys):
    # A genuinely fresh native mapper and runtime engine: do not reattach the
    # already modified original mapper or reuse its policy-bearing processors.
    mapping = registry(metadata=MetaData(schema=f.app.schema))
    table = Table('customer', mapping.metadata,
        Column('id', Uuid, primary_key=True, autoincrement=False),
        Column('tenant_id', Uuid, nullable=False),
        Column('name', Text(collation='C')), Column('label', Text))
    class Customer:
        pass
    mapping.map_imperatively(Customer, table)
    runtime = engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
    try:
        factory = attach(mapping, runtime, lock=f.app.plan.lock_bytes,
                         keys=key_source, deployment=(f.app.plan, f.app.pin))
        yield factory, Customer, runtime
    finally:
        runtime.dispose()
        mapping.dispose()


def _admitted(f):
    # Existing unguarded runtime connection for deployment inspection; the
    # original app.runtime is already attached and forbids raw metadata SQL.
    runtime = engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
    try:
        migration.check_deployment(f.app.plan, runtime, pin=f.app.pin)
    finally:
        runtime.dispose()
    with _fresh_attachment(f) as (factory, customer, _):
        assert _read(factory, customer) == f.expected


@contextmanager
def _fixture_phase(f, operation_id, phase):
    """Exact temporary owner-authored metadata probe; restore before teardown."""
    journal = f'"{f.app.schema}"._cryptalis_journal'
    with f.app.owner.begin() as c:
        digest, old = c.exec_driver_sql(
            f'SELECT plan_digest,state FROM {journal} WHERE operation_id=%s FOR UPDATE',
            (operation_id,)).one()
        changed = copy.deepcopy(old)
        changed['phase'] = phase
        result = c.exec_driver_sql(
            f'UPDATE {journal} SET state=%s::jsonb '
            'WHERE operation_id=%s AND plan_digest=%s AND state=%s::jsonb',
            (json.dumps(changed), operation_id, digest, json.dumps(old)))
        assert result.rowcount == 1
    try:
        yield changed
    finally:
        with f.app.owner.begin() as c:
            result = c.exec_driver_sql(
                f'UPDATE {journal} SET state=%s::jsonb '
                'WHERE operation_id=%s AND plan_digest=%s AND state=%s::jsonb',
                (json.dumps(old), operation_id, digest, json.dumps(changed)))
            assert result.rowcount == 1


def _live_unchanged(f):
    assert frames(f.app, True) == dict(f.current)
    assert f.app.pin == f.baseline[3]


def test_inactive_preparation_keeps_source_admitted(monkeypatch):
    with b9.fixture() as f:
        _admitted(f)
        assert b9.enter(f, 'start').status == 'PREPARING'
        assert b9.enter(f).committed_batches == 1
        _admitted(f)
        assert b9.finish(f).status == 'PREPARED_INACTIVE'
        _admitted(f)
        before = b9.native_snapshot(f)
        seals = b9.count_seals(monkeypatch)
        writes = []
        def collect(connection, cursor, statement, parameters, context, many):
            if statement.lstrip().split(None, 1)[0].upper() in (
                    'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'TRUNCATE'):
                writes.append(statement.split(None, 1)[0].upper())
        event.listen(f.app.owner, 'before_cursor_execute', collect)
        try:
            assert b9.enter(f, 'inspect').status == 'PREPARED_INACTIVE'
        finally:
            event.remove(f.app.owner, 'before_cursor_execute', collect)
        assert seals == [] and writes == []
        assert b9.native_snapshot(f) == before
        assert b9.source_snapshot(f) == f.baseline


def test_gap_successor_phase_alone_leaves_original_deployment_admitted():
    # This PASS proves an admission limitation, not a legitimate pending state.
    with b9.fixture() as f:
        b9.enter(f, 'start'); b9.finish(f)
        before = b9.native_snapshot(f)
        with _fixture_phase(f, f.artifact.operation_id, UNSUPPORTED_PENDING):
            _admitted(f)
            _live_unchanged(f)
        assert b9.native_snapshot(f) == before
        assert b9.source_snapshot(f) == f.baseline


def test_unsupported_source_phase_denies_deployment_and_fresh_attachment():
    with b9.fixture() as f:
        _admitted(f)
        before = b9.native_snapshot(f)
        with _fixture_phase(f, f.app.plan.operation_id, UNSUPPORTED_PENDING):
            runtime = engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
            try:
                with pytest.raises(migration.TransitionFailure) as caught:
                    migration.check_deployment(f.app.plan, runtime, pin=f.app.pin)
                assert caught.value.code == 'restored_state_behind_external_pin'
            finally:
                runtime.dispose()
            with pytest.raises(PolicyMismatch):
                with _fresh_attachment(f):
                    pytest.fail('unsupported source state admitted a fresh attachment')
            _live_unchanged(f)
        assert b9.native_snapshot(f) == before
        _admitted(f)


def test_target_keys_cannot_reuse_source_deployment():
    with b9.fixture() as f:
        before = b9.native_snapshot(f)
        with _fresh_attachment(f, b9.target_keys) as (factory, customer, runtime):
            sql = []
            def collect(*args):
                sql.append(True)
            event.listen(runtime, 'before_cursor_execute', collect)
            try:
                with pytest.raises(PolicyMismatch):
                    _read(factory, customer)
            finally:
                event.remove(runtime, 'before_cursor_execute', collect)
            assert sql == []  # Factory's policy check occurs before DB work.
        assert b9.native_snapshot(f) == before
        assert b9.source_snapshot(f) == f.baseline


def test_gap_warm_attachment_retains_reads_after_source_phase_probe():
    # Existing host contract requires old workers stopped. This test does not
    # promise warm-worker termination or endorse using this phase for cutover.
    with b9.fixture() as f:
        assert _read(f.factory, f.app.Customer) == f.expected
        before = b9.native_snapshot(f)
        with _fixture_phase(f, f.app.plan.operation_id, UNSUPPORTED_PENDING):
            assert _read(f.factory, f.app.Customer) == f.expected
            _live_unchanged(f)
        assert b9.native_snapshot(f) == before
        assert b9.source_snapshot(f) == f.baseline

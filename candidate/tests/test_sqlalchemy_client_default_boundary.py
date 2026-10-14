"""Prepared native oracles for client UUID defaults, not new admission.

These tests never assign a missing ID or call its default themselves. The
attached test records the current documented refusal; it is not parity.
"""
import asyncio
from contextlib import contextmanager
import importlib
import inspect as python_inspect
import json
import os
from types import SimpleNamespace
from uuid import UUID, uuid4

import psycopg
from psycopg import sql
import pytest
from sqlalchemy import Column, MetaData, Table, Text, Uuid, event, inspect, text
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.orm.attributes import NO_VALUE

from cryptalis.manifest.compiler import Writer, WriterInventory
from cryptalis.sqlalchemy import UnsupportedProtectedOperation, attach
from test_migration import DOMAIN, FIELD_ID, TABLE_ID, TENANT, engine, keys, publish, run


class SyntheticDefaultFailure(Exception):
    pass


async def maybe(value):
    return await value if python_inspect.isawaitable(value) else value


@contextmanager
def default_application(callback_kind, *, seed_tenant=False):
    owner = engine('CRYPTALIS_TEST_DATABASE_URL')
    runtime = engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
    schema = 'cryptalis_client_default_' + uuid4().hex
    tracking = SimpleNamespace(calls=[], trace=[], rows=[], fail_at=None, cursor=[],
                               generated=0, setup_calls=())

    def next_identity(context=None):
        # Invocation is exclusively SQLAlchemy's native default dispatch.
        assert 'before_execute' in tracking.trace
        assert all(inspect(row).attrs.id.loaded_value is NO_VALUE
                   for row in tracking.rows)
        values = context.get_current_parameters() if context is not None else None
        if values is not None:
            assert type(values['name']) is str
            assert values['tenant_id'] == TENANT
            assert values.get('id') is None
        identity = UUID(int=9000 + tracking.generated)
        tracking.generated += 1
        tracking.calls.append((identity, None if values is None else values['name']))
        tracking.trace.append('default')
        if len(tracking.calls) == tracking.fail_at:
            raise SyntheticDefaultFailure('owned synthetic callback failure')
        return identity

    def noarg_default():
        return next_identity()

    def context_default(context):
        return next_identity(context)

    mapping = registry(metadata=MetaData(schema=schema))
    table = Table('customer', mapping.metadata,
        Column('id', Uuid, primary_key=True, autoincrement=False,
               default=noarg_default if callback_kind == 'noarg' else context_default),
        Column('tenant_id', Uuid, nullable=False),
        Column('name', Text(collation='C'), nullable=False),
        Column('label', Text, nullable=False))

    class Customer:
        pass

    mapping.map_imperatively(Customer, table)
    declaration = {'schema': 'cryptalis.protection/v1', 'profile': 'cf1',
        'domain_id': str(DOMAIN), 'models': [{
            'model': 'Customer', 'table_id': str(TABLE_ID),
            'tenancy': {'column': 'tenant_id'}, 'fields': [{
                'name': 'name', 'field_id': str(FIELD_ID), 'protect': True,
                'queries': [], 'accept_leakage': []}]}]}
    with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as connection:
        role = connection.execute('select current_user').fetchone()[0]
    try:
        with owner.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        mapping.metadata.create_all(owner)
        with psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL']) as connection:
            connection.execute(sql.SQL('REVOKE ALL ON SCHEMA {} FROM PUBLIC').format(sql.Identifier(schema)))
            connection.execute(sql.SQL('GRANT USAGE ON SCHEMA {} TO {}').format(sql.Identifier(schema), sql.Identifier(role)))
            connection.execute(sql.SQL('GRANT SELECT, INSERT, UPDATE, DELETE ON {}.customer TO {}').format(sql.Identifier(schema), sql.Identifier(role)))
        if seed_tenant:
            # The transition pins only tenants present in source data. Create
            # that separate existing row via the actual native default, never
            # by assigning an ID or editing the deployment policy inventory.
            seed = Customer(tenant_id=TENANT, name='synthetic policy seed', label='policy seed')
            tracking.rows = [seed]
            assert inspect(seed).attrs.id.loaded_value is NO_VALUE
            def observe_seed(connection, statement, multiparams, params, options):
                if getattr(statement, 'is_insert', False):
                    tracking.trace.append('before_execute')
            event.listen(runtime, 'before_execute', observe_seed)
            try:
                with sessionmaker(runtime, expire_on_commit=False)() as session:
                    session.add(seed)
                    session.commit()
                    assert len(tracking.calls) == 1 and seed.id == tracking.calls[0][0]
            finally:
                event.remove(runtime, 'before_execute', observe_seed)
            tracking.setup_calls = tuple(tracking.calls)
            tracking.calls.clear()
            tracking.trace.clear()
            tracking.rows.clear()
        migration = importlib.import_module('cryptalis.migration')
        proposal = migration.plan(json.dumps(declaration).encode(), mapping, owner,
            writers=WriterInventory(True, (Writer(TABLE_ID, 'app', 'sqlalchemy',
                evidence='owned synthetic client-default application'),)),
            search_reviews=(), keys=keys, runtime_role=role, target_id=uuid4(),
            backfill_rows_per_second=1000, verify_rows_per_second=1000,
            temporary_bytes_per_row=700, wal_bytes_per_row=2000)
        assert not tracking.calls
        if seed_tenant:
            assert str(TENANT) in proposal.document['key_policies']
        yield SimpleNamespace(m=migration, owner=owner, runtime=runtime, schema=schema,
            mapping=mapping, table=table, Customer=Customer, tracking=tracking,
            plan=proposal, pin=migration.DeploymentPin(
                proposal.target_id, proposal.operation_id, proposal.digest, 'PREPARED'),
            approval=migration.MaintenanceApproval(
                'test operator stopped inventoried workers and excluded owner writers', 3600))
    finally:
        runtime.dispose()
        with owner.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        owner.dispose()
        mapping.dispose()


async def make_factory(app, mode, attached=False):
    asynchronous = None
    target = app.runtime
    if mode == 'async':
        asynchronous = target = create_async_engine('postgresql+psycopg://', hide_parameters=True,
            async_creator=lambda: psycopg.AsyncConnection.connect(
                os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
    if attached:
        factory = await maybe(attach(app.mapping, target, lock=app.plan.lock_bytes,
            keys=keys, deployment=(app.plan, app.pin)))
    else:
        factory = async_sessionmaker(target) if asynchronous else sessionmaker(target)
    return factory, target.sync_engine if asynchronous else target, asynchronous


@contextmanager
def observe_native_boundary(app, session, target):
    tracking = app.tracking
    sync_session = getattr(session, 'sync_session', session)

    def before_flush(*args):
        tracking.trace.append('before_flush')

    def before_insert(*args):
        tracking.trace.append('before_insert')

    def before_execute(connection, statement, multiparams, params, options):
        if getattr(statement, 'is_insert', False):
            tracking.trace.append('before_execute')

    def before_cursor(connection, cursor, statement, parameters, context, many):
        if context.isinsert:
            tracking.trace.append('before_cursor')
            # Public SQLAlchemy cursor event, after native defaults and bind
            # processing, before DBAPI execution; owned synthetic data only.
            tracking.cursor.append(parameters)
            assert all(inspect(row).attrs.id.loaded_value is NO_VALUE
                       for row in tracking.rows)

    registrations = [(sync_session, 'before_flush', before_flush),
                     (app.Customer, 'before_insert', before_insert),
                     (target, 'before_execute', before_execute),
                     (target, 'before_cursor_execute', before_cursor)]
    for subject, name, callback in registrations:
        event.listen(subject, name, callback)
    try:
        yield
    finally:
        for subject, name, callback in reversed(registrations):
            event.remove(subject, name, callback)


def row_values(app):
    with app.owner.connect() as connection:
        return list(connection.exec_driver_sql(
            f'SELECT id, tenant_id, name, label FROM "{app.schema}".customer ORDER BY label'))


def leaves(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from leaves(item)
    elif isinstance(value, (tuple, list)):
        for item in value:
            yield from leaves(item)
    else:
        yield value


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('callback_kind', ['noarg', 'context'])
def test_native_client_uuid_default_phase_and_explicit_id_suppression(mode, callback_kind):
    with default_application(callback_kind) as app:
        async def scenario():
            factory, target, asynchronous = await make_factory(app, mode)
            session = factory(expire_on_commit=False)
            try:
                rows = [app.Customer(tenant_id=TENANT, name='synthetic ' + label, label=label)
                        for label in ('alpha', 'beta')]
                app.tracking.rows = rows
                assert all(inspect(row).attrs.id.loaded_value is NO_VALUE for row in rows)
                session.add_all(rows)
                assert not app.tracking.calls
                with observe_native_boundary(app, session, target):
                    await maybe(session.flush())
                trace = app.tracking.trace
                assert len(app.tracking.calls) == 2 and len(app.tracking.cursor) >= 1
                # Calibration: the identical cursor-event collector must see
                # the known plaintext in this unprotected native control.
                observed = list(leaves(app.tracking.cursor))
                assert all(row.name in observed for row in rows)
                assert trace.index('before_flush') < trace.index('before_insert')
                assert trace.index('before_insert') < trace.index('before_execute')
                assert trace.index('before_execute') < trace.index('default') < trace.index('before_cursor')
                assert {row.id for row in rows} == {call[0] for call in app.tracking.calls}
                assert all(type(row.id) is UUID and inspect(row).persistent for row in rows)
                if callback_kind == 'context':
                    assert {row.name: row.id for row in rows} == {
                        name: identity for identity, name in app.tracking.calls}
                await maybe(session.commit())
                assert row_values(app) == [(row.id, TENANT, row.name, row.label) for row in rows]
                # This separate explicitly assigned row checks native callback
                # suppression only. It is never substituted for a missing-ID
                # application or attached compatibility case.
                assigned = app.Customer(id=UUID(int=9999), tenant_id=TENANT,
                    name='synthetic explicit', label='explicit')
                session.add(assigned)
                await maybe(session.commit())
                assert len(app.tracking.calls) == 2
            finally:
                await maybe(session.close())
                assert target.pool.checkedout() == 0
                if asynchronous is not None:
                    await asynchronous.dispose()
        asyncio.run(scenario())


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('failure', ['callback', 'constraint'])
def test_native_failed_client_default_batch_preserves_unassigned_ids_and_retries(mode, failure):
    with default_application('context') as app:
        async def scenario():
            factory, target, asynchronous = await make_factory(app, mode)
            session = factory(expire_on_commit=False)
            try:
                rows = [app.Customer(tenant_id=TENANT, name='synthetic ' + label, label=label)
                        for label in ('alpha', 'beta')]
                app.tracking.rows = rows
                if failure == 'callback':
                    app.tracking.fail_at = 2
                else:
                    rows[1].label = None
                session.add_all(rows)
                with observe_native_boundary(app, session, target):
                    with pytest.raises(StatementError if failure == 'callback' else IntegrityError) as caught:
                        await maybe(session.flush())
                if failure == 'callback':
                    assert type(caught.value.orig) is SyntheticDefaultFailure
                    assert not app.tracking.cursor
                else:
                    assert caught.value.orig.sqlstate == '23502'
                    assert app.tracking.cursor
                assert len(app.tracking.calls) == 2
                assert not session.is_active and session.in_transaction()
                assert all(inspect(row).transient and inspect(row).identity is None
                           and inspect(row).attrs.id.loaded_value is NO_VALUE for row in rows)
                assert row_values(app) == []
                await maybe(session.rollback())
                assert session.is_active and not session.in_transaction()
                app.tracking.fail_at = None
                rows[1].label = 'beta'
                session.add_all(rows)
                with observe_native_boundary(app, session, target):
                    await maybe(session.commit())
                assert len(app.tracking.calls) == 4
                assert {row.id for row in rows} == {identity for identity, _ in app.tracking.calls[2:]}
                assert {row.id for row in rows}.isdisjoint(identity for identity, _ in app.tracking.calls[:2])
                assert row_values(app) == [(row.id, TENANT, row.name, row.label) for row in rows]
            finally:
                await maybe(session.close())
                assert target.pool.checkedout() == 0
                if asynchronous is not None:
                    await asynchronous.dispose()
        asyncio.run(scenario())


@pytest.mark.parametrize('mode', ['sync', 'async'])
def test_current_attached_client_uuid_default_is_loud_refusal_before_callback_or_insert(mode):
    with default_application('noarg', seed_tenant=True) as app:
        run(app)
        publish(app)
        payload = '_cryptalis_' + FIELD_ID.hex
        def persisted():
            with app.owner.connect() as connection:
                return list(connection.exec_driver_sql(
                    f'SELECT id, tenant_id, name, label, "{payload}" FROM "{app.schema}".customer ORDER BY label'))
        baseline = persisted()
        assert len(baseline) == len(app.tracking.setup_calls) == 1
        async def scenario():
            factory, target, asynchronous = await make_factory(app, mode, attached=True)
            session = factory(tenant_id=TENANT, expire_on_commit=False)
            try:
                row = app.Customer(tenant_id=TENANT, name='synthetic refused', label='refused')
                app.tracking.rows = [row]
                assert inspect(row).attrs.id.loaded_value is NO_VALUE
                session.add(row)
                with observe_native_boundary(app, session, target):
                    with pytest.raises(UnsupportedProtectedOperation):
                        await maybe(session.flush())
                assert not app.tracking.calls and not app.tracking.cursor
                assert inspect(row).attrs.id.loaded_value is NO_VALUE
                assert not session.is_active
                await maybe(session.rollback())
                assert session.is_active
                assert persisted() == baseline
            finally:
                await maybe(session.close())
                assert target.pool.checkedout() == 0
                if asynchronous is not None:
                    await asynchronous.dispose()
        asyncio.run(scenario())

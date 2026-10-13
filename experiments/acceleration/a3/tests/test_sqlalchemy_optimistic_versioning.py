"""Native optimistic-versioning oracles for ordinary protected ORM writes.

The integer version mapper exists before planning. These tests never enable
private bulk UPDATE and do not qualify freshness against malicious replay.
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
from sqlalchemy import Column, Integer, MetaData, Table, Text, Uuid, inspect, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.orm.exc import StaleDataError

from cryptalis.manifest.compiler import Writer, WriterInventory
from cryptalis.sqlalchemy import attach
from test_migration import (DOMAIN, FIELD_ID, TABLE_ID, TENANT, engine,
                            independent_open, keys, publish, run)


RECORD = UUID(int=101)


@contextmanager
def versioned_application():
    """Independent native/attached schemas with the same original mapper."""
    owner = engine('CRYPTALIS_TEST_DATABASE_URL')
    runtime = engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
    schema = 'cryptalis_versioning_' + uuid4().hex
    mapping = registry(metadata=MetaData(schema=schema))
    table = Table('customer', mapping.metadata,
        Column('id', Uuid, primary_key=True, autoincrement=False),
        Column('tenant_id', Uuid, nullable=False),
        Column('name', Text(collation='C')),
        Column('label', Text),
        Column('version_id', Integer, nullable=False))

    class Customer:
        pass

    mapping.map_imperatively(Customer, table, version_id_col=table.c.version_id)
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
            connection.execute(sql.SQL('GRANT USAGE ON SCHEMA {} TO {}').format(
                sql.Identifier(schema), sql.Identifier(role)))
            connection.execute(sql.SQL('GRANT SELECT, INSERT, UPDATE, DELETE ON {}.customer TO {}').format(
                sql.Identifier(schema), sql.Identifier(role)))
        with sessionmaker(runtime)() as session:
            row = Customer(id=RECORD, tenant_id=TENANT, name='initial alpha', label='public unchanged')
            session.add(row)
            session.commit()
            assert row.version_id == 1
        migration = importlib.import_module('cryptalis.migration')
        proposal = migration.plan(json.dumps(declaration).encode(), mapping, owner,
            writers=WriterInventory(True, (Writer(TABLE_ID, 'app', 'sqlalchemy',
                evidence='owned synthetic versioned application'),)),
            search_reviews=(), keys=keys, runtime_role=role, target_id=uuid4(),
            backfill_rows_per_second=1000, verify_rows_per_second=1000,
            temporary_bytes_per_row=700, wal_bytes_per_row=2000)
        pin = migration.DeploymentPin(proposal.target_id, proposal.operation_id, proposal.digest, 'PREPARED')
        yield SimpleNamespace(m=migration, owner=owner, runtime=runtime, schema=schema,
            mapping=mapping, table=table, Customer=Customer, plan=proposal, pin=pin,
            role=role, approval=migration.MaintenanceApproval(
                'test operator stopped inventoried workers and excluded owner writers', 3600))
    finally:
        runtime.dispose()
        with owner.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        owner.dispose()
        mapping.dispose()


async def maybe(value):
    return await value if python_inspect.isawaitable(value) else value


async def factory_for(app, mode, attached):
    async_engine = None
    if mode == 'async':
        async_engine = create_async_engine('postgresql+psycopg://', hide_parameters=True,
            async_creator=lambda: psycopg.AsyncConnection.connect(
                os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
        factory = (await attach(app.mapping, async_engine, lock=app.plan.lock_bytes,
            keys=keys, deployment=(app.plan, app.pin))) if attached else async_sessionmaker(async_engine)
    else:
        factory = (attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
            keys=keys, deployment=(app.plan, app.pin))) if attached else sessionmaker(app.runtime)
    return factory, async_engine


def storage_snapshot(app, attached):
    """Owner observation and independent CF1 decoder, outside both Sessions."""
    payload = '_cryptalis_' + FIELD_ID.hex
    columns = f'name, label, version_id, "{payload}"' if attached else 'name, label, version_id'
    with app.owner.connect() as connection:
        row = connection.exec_driver_sql(
            f'SELECT {columns} FROM "{app.schema}".customer WHERE id=%s', (RECORD,)).one_or_none()
    if row is None:
        return None, None
    if attached:
        assert app.plan.document['format'] == 'cryptalis.transition/retained-native-research-v0'
        assert row[0] is None  # No plaintext survives in the retained native slot.
        body = bytes(row[3])
        descriptor = json.loads(app.plan.lock_bytes)['models'][0]['fields'][0]['descriptor']
        plaintext = independent_open(body, descriptor, TENANT, RECORD)
        return (plaintext, row[1], row[2]), body
    return tuple(row), None


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('action', ['update', 'delete'])
def test_stale_versioned_orm_write_matches_native_and_recovers(mode, action):
    """A stale write cannot replace/delete the winner; rollback permits retry."""
    observations = []
    for attached in (False, True):
        with versioned_application() as app:
            if attached:
                run(app)
                publish(app)

            async def scenario():
                factory, async_engine = await factory_for(app, mode, attached)
                options = {'expire_on_commit': False}
                if attached:
                    options['tenant_id'] = TENANT
                winner, loser = factory(**options), factory(**options)
                try:
                    first = await maybe(winner.get(app.Customer, RECORD))
                    stale = await maybe(loser.get(app.Customer, RECORD))
                    assert (first.name, first.version_id) == ('initial alpha', 1)
                    assert (stale.name, stale.version_id) == ('initial alpha', 1)
                    first.name = 'winner beta'
                    await maybe(winner.commit())
                    assert first.version_id == 2
                    winner_snapshot = storage_snapshot(app, attached)
                    assert winner_snapshot[0] == ('winner beta', 'public unchanged', 2)
                    assert (stale.name, stale.version_id) == ('initial alpha', 1)
                    if action == 'update':
                        stale.name = 'stale gamma'
                    else:
                        await maybe(loser.delete(stale))
                    transaction = loser.get_transaction()
                    with pytest.raises(StaleDataError) as caught:
                        await maybe(loser.flush())
                    assert type(caught.value) is StaleDataError
                    state = inspect(stale)
                    observed = (loser.is_active, loser.in_transaction(),
                        loser.in_nested_transaction(), transaction.is_active,
                        stale in loser, state.persistent, state.deleted,
                        state.expired, tuple(sorted(state.expired_attributes)),
                        len(loser.new), len(loser.dirty), len(loser.deleted))
                    assert not loser.is_active and not transaction.is_active
                    assert storage_snapshot(app, attached) == winner_snapshot
                    await maybe(loser.rollback())
                    assert loser.is_active
                    recovered = await maybe(loser.get(app.Customer, RECORD))
                    assert (recovered.name, recovered.version_id) == ('winner beta', 2)
                    if action == 'update':
                        recovered.name = 'recovered delta'
                    else:
                        await maybe(loser.delete(recovered))
                    await maybe(loser.commit())
                    final = storage_snapshot(app, attached)[0]
                    assert final == (('recovered delta', 'public unchanged', 3)
                                     if action == 'update' else None)
                    return observed, final
                finally:
                    await maybe(winner.close())
                    await maybe(loser.close())
                    if async_engine is not None:
                        await async_engine.dispose()

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], f'Native/attached versioned ORM state differs: {observations}'

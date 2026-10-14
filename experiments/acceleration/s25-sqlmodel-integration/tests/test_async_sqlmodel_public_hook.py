"""Pinned optional SQLModel regression; use the reviewed source-overlay matrix."""
import asyncio
from contextlib import nullcontext
import os
from pathlib import Path
import traceback
from uuid import UUID

import pytest
from importlib.metadata import PackageNotFoundError, version

# This optional matrix must be selected only in its exact existing cell.
# Refuse collection explicitly rather than silently skip missing coverage.
try:
    _optional_cell = (version('sqlmodel'), version('SQLAlchemy'))
except PackageNotFoundError as error:
    raise pytest.UsageError('Select this regression only in the reviewed SQLModel 0.0.47 / SQLAlchemy 2.0.51 cell; no dependency installation is implied') from None
if _optional_cell != ('0.0.47', '2.0.51'):
    raise pytest.UsageError('This regression requires exactly SQLModel 0.0.47 / SQLAlchemy 2.0.51; use the explicit matrix exclusion in other cells')

from sqlalchemy import bindparam, delete, event, func, insert, select as sa_select, update
from sqlalchemy.engine import Row, ScalarResult
from sqlalchemy.exc import DBAPIError, MultipleResultsFound, NoResultFound, PendingRollbackError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.util.concurrency import await_only
from sqlmodel import select
from sqlmodel.ext.asyncio import session as native_module

from async_sqlmodel_oracle_support import (adapter, application, enable, fixture, independent_open,
    native_membership, NativeAsyncSession, NativeSession, origin_check,
    owner_rows, parameter_leaves, public_rows, row, sessions_for, support, write_record)
from cryptalis.crypto import Keyring, KeyUnavailable


def assert_sanitized_provider_failure(actual, injected, marker):
    assert type(actual) is KeyUnavailable
    assert actual is not injected
    assert actual.__cause__ is None
    assert actual.__suppress_context__ is True
    # `from None` suppresses display; it need not erase __context__.
    assert marker in str(injected) and marker in repr(injected)
    displayed = str(actual) + repr(actual) + ''.join(traceback.format_exception(actual))
    assert marker not in displayed


@pytest.fixture(scope='module', autouse=True)
def frozen_source_and_environment():
    origin_check()
    yield
    origin_check()


def test_async_sqlmodel_exact_mro_and_single_dispatch(monkeypatch):
    enable(monkeypatch)
    original_exec = NativeAsyncSession.exec
    calls, execute_calls = [], []
    async def native_exec(self, *args, **kwargs):
        calls.append(True)
        return await original_exec(self, *args, **kwargs)
    async def forbidden_execute(*args, **kwargs):
        execute_calls.append(True)
        raise AssertionError('Native SQLModel exec must not call async execute')
    support.guarded_async_session_class.cache_clear()
    try:
        with monkeypatch.context() as patch:
            patch.setattr(NativeAsyncSession, 'exec', native_exec)
            patch.setattr(adapter._AsyncSession, 'execute', forbidden_execute)
            with application(True) as app:
                async def scenario():
                    async with sessions_for(app) as (engine, factory):
                        async with factory(tenant_id=app.tenant) as session:
                            native_membership(session, True)
                            flushes, queries = [], []
                            def before_flush(*args):
                                flushes.append(True)
                            def do_execute(*args):
                                queries.append(True)
                            event.listen(session.sync_session, 'before_flush', before_flush)
                            event.listen(session.sync_session, 'do_orm_execute', do_execute)
                            try:
                                session.add(row(app, 'ordinary', 0)); await session.flush()
                                assert (await session.exec(select(app.Customer.name))).one() == 'ordinary'
                                assert calls == flushes == queries == [True]
                                assert execute_calls == []
                                write_record('async-sqlmodel-mro.jsonl', {
                                    'async_mro': [c.__module__ + '.' + c.__qualname__ for c in type(session).__mro__],
                                    'sync_mro': [c.__module__ + '.' + c.__qualname__ for c in type(session.sync_session).__mro__],
                                    'native_exec_calls': 1, 'flush_events': 1, 'query_events': 1})
                                await session.rollback()
                            finally:
                                event.remove(session.sync_session, 'before_flush', before_flush)
                                event.remove(session.sync_session, 'do_orm_execute', do_execute)
                asyncio.run(scenario())
    finally:
        support.guarded_async_session_class.cache_clear()
    assert NativeAsyncSession.exec is original_exec


@pytest.mark.parametrize('shape', ['entity', 'scalar', 'tuple', 'count', 'parameter', 'sa-select'])
def test_async_sqlmodel_exec_native_shapes(shape, monkeypatch):
    enable(monkeypatch)
    observations = []
    for protected in (False, True):
        with application(protected) as app:
            async def scenario():
                async with sessions_for(app) as (engine, factory):
                    async with factory(tenant_id=app.tenant, expire_on_commit=False) as session:
                        native_membership(session, protected)
                        session.add_all(row(app, value, rank) for rank, value in enumerate([None, '', '雪😀é']))
                        await session.commit()
                        C = app.Customer
                        statements = {
                            'entity': select(C).order_by(C.rank),
                            'scalar': select(C.name).order_by(C.rank),
                            'tuple': select(C.name, C.rank).order_by(C.rank),
                            'count': select(func.count()).select_from(C),
                            'parameter': select(C.name).where(C.rank == bindparam('wanted_rank')),
                            'sa-select': sa_select(C).order_by(C.rank),
                        }
                        result = await session.exec(statements[shape],
                            params={'wanted_rank': 2} if shape == 'parameter' else None)
                        values = result.all()
                        result_type = type(result).__module__ + '.' + type(result).__qualname__
                        if shape in ('entity', 'scalar', 'count', 'parameter'):
                            assert isinstance(result, ScalarResult)
                        else:
                            assert not isinstance(result, ScalarResult)
                            assert all(isinstance(value, Row) for value in values)
                        if shape == 'entity':
                            assert all(type(value) is C for value in values)
                            normalized = [(value.name, value.rank) for value in values]
                        elif shape == 'sa-select':
                            assert all(len(value) == 1 and type(value[0]) is C for value in values)
                            normalized = [(value[0].name, value[0].rank) for value in values]
                        elif shape == 'tuple':
                            normalized = [tuple(value) for value in values]
                        else:
                            normalized = values
                        expected = ([3] if shape == 'count' else ['雪😀é'] if shape == 'parameter'
                            else [None, '', '雪😀é'] if shape == 'scalar'
                            else [(None, 0), ('', 1), ('雪😀é', 2)])
                        assert normalized == expected
                        assert (await session.exec(select(C.rank).where(C.rank == 1))).one() == 1
                        assert (await session.exec(select(C.rank).where(C.rank == -1))).first() is None
                        with pytest.raises(NoResultFound):
                            (await session.exec(select(C.rank).where(C.rank == -1))).one()
                        with pytest.raises(MultipleResultsFound):
                            (await session.exec(select(C.rank))).one()
                        await session.rollback()
                    return result_type, normalized
            observations.append(asyncio.run(scenario()))
            write_record('async-sqlmodel-arms.jsonl', {'test': 'shapes', 'shape': shape,
                'protected': protected, 'completed': True, 'result': observations[-1]})
    assert observations[0] == observations[1]


@pytest.mark.parametrize('mode', ['enabled', 'no-autoflush', 'statement-off', 'call-overrides-statement'])
def test_async_sqlmodel_exec_autoflush_precedence(mode, monkeypatch):
    enable(monkeypatch)
    observations = []
    for protected in (False, True):
        with application(protected) as app:
            async def scenario():
                async with sessions_for(app) as (engine, factory):
                    async with factory(tenant_id=app.tenant) as session:
                        session.add(row(app, 'outer', 0)); await session.flush()
                        pending = row(app, 'pending', 1); session.add(pending)
                        flushes = []
                        def before_flush(*args):
                            flushes.append(True)
                        event.listen(session.sync_session, 'before_flush', before_flush)
                        try:
                            statement = select(app.Customer.rank).order_by(app.Customer.rank)
                            options = {}
                            if mode in ('statement-off', 'call-overrides-statement'):
                                statement = statement.execution_options(autoflush=False)
                            if mode == 'call-overrides-statement':
                                options['autoflush'] = True
                            context = session.no_autoflush if mode == 'no-autoflush' else nullcontext()
                            with context:
                                values = (await session.exec(statement, execution_options=options)).all()
                            expected_flush = mode in ('enabled', 'call-overrides-statement')
                            observed = values, len(flushes), pending in session.new
                            assert observed == ([0, 1] if expected_flush else [0], int(expected_flush), not expected_flush)
                            await session.rollback()
                            return observed
                        finally:
                            event.remove(session.sync_session, 'before_flush', before_flush)
            observations.append(asyncio.run(scenario()))
            assert owner_rows(app) == []
    assert observations[0] == observations[1]


@pytest.mark.parametrize('loading', ['selectin', 'joined'])
def test_async_sqlmodel_eager_relationships(loading, monkeypatch):
    enable(monkeypatch)
    observations = []
    for protected in (False, True):
        with application(protected, relationships=True) as app:
            async def scenario():
                async with sessions_for(app) as (engine, factory):
                    async with factory(tenant_id=app.tenant, expire_on_commit=False) as session:
                        parent = row(app, 'parent', 0)
                        parent.children = [app.Child(id=UUID(int=3000), customer_id=parent.id, note='public-child')]
                        session.add(parent); await session.commit()
                    async with factory(tenant_id=app.tenant) as session:
                        option = selectinload(app.Customer.children) if loading == 'selectin' else joinedload(app.Customer.children)
                        parent = (await session.exec(select(app.Customer).options(option))).unique().one()
                        observed = parent.name, [(child.note, child.customer is parent) for child in parent.children]
                        assert observed == ('parent', [('public-child', True)])
                        await session.rollback()
                        return observed
            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1]


def test_async_sqlmodel_exec_authority_is_fresh_between_operations(monkeypatch):
    enable(monkeypatch)
    with application(True) as app:
        async def scenario():
            selected, calls = [], []
            def resolve(tenant):
                selected.append(app.rings[tenant])
                return app.rings[tenant]
            async with sessions_for(app, keys=resolve) as (engine, factory):
                async with factory(tenant_id=app.tenant, expire_on_commit=False) as session:
                    session.add(row(app, 'kept', 0)); await session.commit()
                    assert (await session.exec(select(app.Customer.name))).one() == 'kept'
                    healthy = app.rings[app.tenant]
                    failure = KeyUnavailable()
                    provider_marker = 'synthetic-provider-secret-v3-authority'
                    failure.args = (provider_marker,)
                    class FailingProvider:
                        provider_id = app.provider.provider_id
                        def unwrap(self, *args):
                            calls.append('unwrap'); raise failure
                        async def unwrap_async(self, *args):
                            calls.append('unwrap_async'); raise failure
                    cold = Keyring(healthy.policy, {app.provider.provider_id: FailingProvider()})
                    app.rings[app.tenant] = cold
                    emitted = []
                    def before_cursor(*args):
                        emitted.append(True)
                    event.listen(engine.sync_engine, 'before_cursor_execute', before_cursor)
                    try:
                        with pytest.raises(KeyUnavailable) as caught:
                            await session.exec(select(app.Customer.name))
                        assert_sanitized_provider_failure(caught.value, failure, provider_marker)
                        assert selected[-1] is cold and calls == ['unwrap_async'] and emitted == []
                        assert session.is_active
                    finally:
                        app.rings[app.tenant] = healthy
                        event.remove(engine.sync_engine, 'before_cursor_execute', before_cursor)
                    assert (await session.exec(select(app.Customer.name))).one() == 'kept'
                    assert selected[-1] is healthy
                    await session.rollback()
        asyncio.run(scenario())
    write_record('async-sqlmodel-provider-completion.jsonl', {
        'test': 'authority-freshness', 'protected': True, 'completed': True,
        'fresh_ring_selected': True, 'async_provider_called_once': True,
        'failed_operation_emitted_no_sql': True, 'session_remained_active': True,
        'healthy_ring_restored_and_read_completed': True})


@pytest.mark.parametrize('unit', ['root', 'savepoint'])
@pytest.mark.parametrize('fault', ['provider', 'cancel'])
def test_async_sqlmodel_exec_failed_autoflush_recovers(fault, unit, monkeypatch):
    enable(monkeypatch)
    nested = unit == 'savepoint'
    observations = []
    for protected in (False, True):
        with application(protected) as app:
            async def scenario():
                async with sessions_for(app) as (engine, factory):
                    async with factory(tenant_id=app.tenant, expire_on_commit=False) as session:
                        session.add(row(app, 'outer', 0)); await session.flush()
                        transaction = await session.begin_nested() if nested else session.get_transaction()
                        pending = row(app, 'retry-same-object', 1); session.add(pending)
                        healthy = app.rings[app.tenant]
                        entered, never = asyncio.Event(), asyncio.Event()
                        calls = []
                        failure = KeyUnavailable()
                        provider_marker = 'synthetic-provider-secret-v3-autoflush'
                        if protected and fault == 'provider':
                            failure.args = (provider_marker,)
                        async def fail_async(*args):
                            calls.append('fault'); entered.set()
                            if fault == 'cancel':
                                await never.wait()
                            raise failure
                        class FailingProvider:
                            provider_id = app.provider.provider_id
                            async def unwrap_async(self, *args):
                                return await fail_async()
                            def unwrap(self, *args):
                                raise AssertionError('Async path must use async unwrap')
                        def native_fault(connection, cursor, statement, *args):
                            if statement.lstrip().upper().startswith('INSERT '):
                                await_only(fail_async())
                        if protected:
                            app.rings[app.tenant] = Keyring(healthy.policy,
                                {app.provider.provider_id: FailingProvider()})
                        else:
                            event.listen(engine.sync_engine, 'before_cursor_execute', native_fault)
                        task = None
                        try:
                            if fault == 'cancel':
                                task = asyncio.create_task(session.exec(select(app.Customer.rank)))
                                await asyncio.wait_for(entered.wait(), timeout=5)
                                task.cancel()
                                with pytest.raises(asyncio.CancelledError):
                                    await task
                                assert task.cancelled()
                            else:
                                with pytest.raises(KeyUnavailable) as caught:
                                    await session.exec(select(app.Customer.rank))
                                if protected:
                                    assert_sanitized_provider_failure(caught.value, failure, provider_marker)
                                else:
                                    assert caught.value is failure
                            assert calls == ['fault']
                            failed = session.is_active, transaction.is_active, pending in session
                            assert failed == (False, False, False)
                        finally:
                            if task is not None and not task.done():
                                task.cancel()
                                try:
                                    await task
                                except asyncio.CancelledError:
                                    pass
                            app.rings[app.tenant] = healthy
                            if event.contains(engine.sync_engine, 'before_cursor_execute', native_fault):
                                event.remove(engine.sync_engine, 'before_cursor_execute', native_fault)
                        with pytest.raises(PendingRollbackError):
                            await session.commit()
                        if nested:
                            await transaction.rollback(); await session.commit()
                        else:
                            await session.rollback()
                        assert session.is_active
                        session.add(pending); await session.commit()
                        values = (await session.exec(select(app.Customer.name).order_by(app.Customer.rank))).all()
                        assert values == (['outer', 'retry-same-object'] if nested else ['retry-same-object'])
                        await session.rollback()
                        return failed, values
            observations.append(asyncio.run(scenario()))
        write_record('async-sqlmodel-provider-completion.jsonl', {
            'test': 'failed-autoflush-recovery', 'fault': fault, 'unit': unit,
            'protected': protected, 'completed': True,
            'failed_state': observations[-1][0],
            'recovered_values': observations[-1][1],
            'same_object_retry_completed': True})
    assert observations[0] == observations[1]


async def refusal_without_activation(app, monkeypatch, *, logging=False):
    attempts, actions, emitted = [], [], []
    async def no_connection():
        attempts.append(True)
        raise AssertionError('Admission refusal must not connect')
    engine = create_async_engine('postgresql+psycopg://', echo=logging,
        hide_parameters=not logging, async_creator=no_connection)
    def unexpected(*args):
        actions.append(True)
        raise AssertionError('Admission refusal must not validate or activate')
    def cursor(*args):
        emitted.append(True)
    before = tuple(column.type for table in app.mapping.metadata.tables.values() for column in table.columns)
    try:
        with monkeypatch.context() as patch:
            patch.setattr(adapter._Attachment, 'validate', unexpected)
            patch.setattr(adapter._Attachment, 'activate', unexpected)
            event.listen(engine.sync_engine, 'before_cursor_execute', cursor)
            expected = adapter.UnsafeEngineLogging if logging else adapter.UnsupportedSQLModelRuntime
            with pytest.raises(expected):
                await adapter.attach(app.mapping, engine, lock=app.plan.lock_bytes, keys=app.keys)
        assert attempts == actions == emitted == []
        after = tuple(column.type for table in app.mapping.metadata.tables.values() for column in table.columns)
        assert len(before) == len(after) and all(a is b for a, b in zip(before, after))
    finally:
        event.remove(engine.sync_engine, 'before_cursor_execute', cursor)
        await engine.dispose()


def test_async_sqlmodel_default_gate_refuses_without_activation(monkeypatch):
    monkeypatch.setattr(support, '_experimental_async_sqlmodel', False, raising=False)
    with application(True) as app:
        asyncio.run(refusal_without_activation(app, monkeypatch))


def test_async_sqlmodel_default_off_after_cached_class(monkeypatch):
    enable(monkeypatch)
    with application(True) as app:
        async def warm():
            async with sessions_for(app) as (engine, factory):
                async with factory(tenant_id=app.tenant) as session:
                    native_membership(session, True)
                    assert (await session.exec(select(app.Customer.rank))).all() == []
                    await session.rollback()
        asyncio.run(warm())
    monkeypatch.setattr(support, '_experimental_async_sqlmodel', False)
    with application(True) as app:
        asyncio.run(refusal_without_activation(app, monkeypatch))


@pytest.mark.parametrize('cell', ['sqlmodel-other', 'sa20-other-patch', 'sa21'])
def test_async_sqlmodel_version_refusal_without_activation(cell, monkeypatch):
    enable(monkeypatch)
    with application(True) as app:
        with monkeypatch.context() as patch:
            if cell == 'sqlmodel-other':
                patch.setattr(support, 'version', lambda name: '0.0.48')
            else:
                patch.setattr(support.sqlalchemy, '__version__', '2.1.3' if cell == 'sa21' else '2.0.54')
            asyncio.run(refusal_without_activation(app, patch))


def test_async_sqlmodel_logging_precedes_version_refusal(monkeypatch):
    monkeypatch.setattr(support, '_experimental_async_sqlmodel', False, raising=False)
    with application(True) as app:
        asyncio.run(refusal_without_activation(app, monkeypatch, logging=True))


@pytest.mark.parametrize('entry', ['bind', 'binds', 'class_', 'sync_session_class', '_owner', '_asynchronous', 'native-sync', 'native-async'])
def test_async_sqlmodel_factory_and_unattached_session_refusals(entry, monkeypatch):
    enable(monkeypatch)
    with application(True) as app:
        async def scenario():
            async with sessions_for(app) as (engine, factory):
                emitted = []
                def observe(*args):
                    emitted.append(True)
                event.listen(engine.sync_engine, 'before_cursor_execute', observe)
                try:
                    if entry.startswith('native-'):
                        async with NativeAsyncSession(engine) as unguarded:
                            with pytest.raises(adapter.UnsupportedProtectedOperation):
                                if entry == 'native-sync':
                                    await unguarded.run_sync(lambda sync: sync.exec(select(app.Customer)).all())
                                else:
                                    await unguarded.exec(select(app.Customer))
                            await unguarded.rollback()
                    else:
                        with pytest.raises(adapter.UnsupportedProtectedOperation):
                            factory(tenant_id=app.tenant, **{entry: object()})
                    assert emitted == []
                finally:
                    event.remove(engine.sync_engine, 'before_cursor_execute', observe)
        asyncio.run(scenario())


@pytest.mark.parametrize('verb', ['insert', 'update', 'delete'])
def test_async_sqlmodel_exec_dml_disabled_refuses(verb, monkeypatch):
    enable(monkeypatch)
    with application(True, public_table=True) as app:
        before = public_rows(app)
        async def scenario():
            async with sessions_for(app) as (engine, factory):
                async with factory(tenant_id=app.tenant) as session:
                    table = app.public_table
                    statement = (insert(table).values(id=UUID(int=2999), label='never', rank=9) if verb == 'insert'
                        else update(table).values(label='never') if verb == 'update' else delete(table))
                    writes = []
                    def observe(connection, cursor, sql, *args):
                        if sql.lstrip().upper().startswith(('INSERT ', 'UPDATE ', 'DELETE ')):
                            writes.append(True)
                    event.listen(engine.sync_engine, 'before_cursor_execute', observe)
                    try:
                        with pytest.raises(adapter.UnsupportedProtectedOperation):
                            await session.exec(statement)
                        assert writes == []
                        await session.rollback()
                    finally:
                        event.remove(engine.sync_engine, 'before_cursor_execute', observe)
        asyncio.run(scenario())
        assert public_rows(app) == before and owner_rows(app) == []


def test_async_sqlmodel_wire_and_independent_frames(monkeypatch):
    enable(monkeypatch)
    markers = ['OWNED-LAB-MARKER-alpha', 'OWNED-LAB-MARKER-beta']
    observations = []
    for protected in (False, True):
        with application(protected) as app:
            async def scenario():
                seen, writes = [], []
                async with sessions_for(app) as (engine, factory):
                    def collect(connection, cursor, statement, parameters, *args):
                        if statement.lstrip().upper().startswith('INSERT '):
                            writes.append(True)
                            seen.extend(value for value in parameter_leaves(parameters)
                                if type(value) is str and value in markers)
                    event.listen(engine.sync_engine, 'before_cursor_execute', collect)
                    try:
                        for rank, tenant in enumerate((app.tenant, fixture.OTHER)):
                            async with factory(tenant_id=tenant, expire_on_commit=False) as session:
                                session.add(row(app, markers[rank], rank, tenant=tenant)); await session.commit()
                                assert (await session.exec(select(app.Customer.name).where(app.Customer.tenant_id == tenant))).one() == markers[rank]
                                await session.rollback()
                        assert writes
                        assert seen == ([] if protected else markers)
                    finally:
                        event.remove(engine.sync_engine, 'before_cursor_execute', collect)
                return len(writes), seen
            observations.append(asyncio.run(scenario()))
            stored = owner_rows(app)
            assert len(stored) == 2
            for identity, tenant, value, rank in stored:
                assert (independent_open(app, value, tenant, identity) if protected else value) == markers[rank]
    assert observations[0][1] == markers and observations[1][1] == []


@pytest.mark.parametrize('unit', ['root', 'savepoint'])
def test_async_sqlmodel_exec_result_boundary_after_native_call(unit, monkeypatch):
    """Test-only pinned result-helper injection; runtime uses only public exec.

    Genuine UPDATE RETURNING and the unmodified native helper finish first.
    Native may commit; protected quarantines the failed unit. This intentional
    difference is asserted per arm, never relabelled native state equality.
    """
    enable(monkeypatch)
    nested = unit == 'savepoint'
    for protected in (False, True):
        with application(protected, public_table=True) as app:
            baseline = owner_rows(app)
            async def scenario():
                async with sessions_for(app, public_update=protected) as (engine, factory):
                    async with factory(tenant_id=app.tenant) as session:
                        original = native_module._ensure_sync_result
                        assert NativeAsyncSession.exec.__globals__['_ensure_sync_result'] is original
                        executed, reached, cleanups = [], [], []
                        original_cleanup = adapter._failed_flush_preparation
                        def cleanup(sync_session, error):
                            cleanups.append((sync_session, error))
                            return original_cleanup(sync_session, error)
                        failure = DBAPIError(None, None, RuntimeError('synthetic after native SQLModel result'))
                        def after_cursor(connection, cursor, statement, *args):
                            if statement.lstrip().upper().startswith('UPDATE '):
                                executed.append(cursor)
                        async def fail_after_result(result, calling_method):
                            completed = await original(result, calling_method)
                            cursor_result = result if getattr(result, '_is_cursor', False) else getattr(result, 'raw', None)
                            context = getattr(cursor_result, 'context', None)
                            assert context is not None and context.isupdate
                            assert len(executed) == 1 and context.cursor is executed[0]
                            assert completed is result and list(completed.keys()) == ['id', 'label']
                            reached.append({'native_helper_completed': True, 'genuine_update': True,
                                'result_type': type(result).__module__ + '.' + type(result).__qualname__})
                            write_record('async-sqlmodel-post-result-reach.jsonl', {
                                'unit': unit, 'protected': protected,
                                'native_helper_completed': True, 'genuine_update': True,
                                'synthetic_exception_reached': True,
                                'driver_cursor_type': type(context.cursor).__module__ + '.' + type(context.cursor).__qualname__})
                            raise failure
                        table = app.public_table
                        await session.exec(update(table).where(table.c.id == UUID(int=2000)).values(label='outer-valid'))
                        transaction = await session.begin_nested() if nested else session.get_transaction()
                        event.listen(engine.sync_engine, 'after_cursor_execute', after_cursor)
                        prior = adapter._delete_experiment.ResultBoundary(object())
                        token = adapter._delete_experiment._result_boundary.set(prior)
                        try:
                            with monkeypatch.context() as patch:
                                patch.setattr(native_module, '_ensure_sync_result', fail_after_result)
                                patch.setattr(adapter, '_failed_flush_preparation', cleanup)
                                with pytest.raises(DBAPIError) as caught:
                                    await session.exec(update(table).where(table.c.id == UUID(int=2002))
                                        .values(label='completed-before-fault').returning(table.c.id, table.c.label))
                                assert caught.value is failure
                            assert adapter._delete_experiment._result_boundary.get() is prior
                            assert cleanups == ([(session.sync_session, failure)] if protected else [])
                        finally:
                            adapter._delete_experiment._result_boundary.reset(token)
                            event.remove(engine.sync_engine, 'after_cursor_execute', after_cursor)
                        assert native_module._ensure_sync_result is original
                        assert adapter._failed_flush_preparation is original_cleanup
                        assert len(executed) == len(reached) == 1
                        assert session.is_active is (not protected)
                        assert transaction.is_active is (not protected)
                        assert adapter._delete_experiment._result_boundary.get() is None
                        if protected:
                            with pytest.raises(PendingRollbackError):
                                await session.commit()
                            if nested:
                                await transaction.rollback(); await session.commit()
                            else:
                                await session.rollback()
                        else:
                            await session.commit()
                        after = public_rows(app)
                        assert after[0][1] == ('outer-valid' if not protected or nested else None)
                        assert after[1][1] == ('old-2' if protected else 'completed-before-fault')
                        assert owner_rows(app) == baseline
                        assert engine.sync_engine.pool.checkedout() == 0
                        await session.exec(update(table).where(table.c.id == UUID(int=2002)).values(label='recovered'))
                        await session.commit()
                        assert public_rows(app)[1][1] == 'recovered'
                        assert owner_rows(app) == baseline
                        write_record('async-sqlmodel-post-result.jsonl', {'unit': unit,
                            'protected': protected, 'reached': reached,
                            'policy': 'quarantined' if protected else 'native-committable',
                            'recovered': True, 'synthetic_fault': True})
            asyncio.run(scenario())

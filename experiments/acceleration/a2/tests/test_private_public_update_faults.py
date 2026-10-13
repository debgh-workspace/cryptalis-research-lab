"""Native transaction/fault oracles for the private public-table UPDATE slice.

These controls add no protected-table bulk capability. The frozen A1 runtime is
unchanged; a native differential failure is evidence, not an expected xfail.
"""
import asyncio
import inspect
import json
import os
import time
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

import psycopg
import pytest
from sqlalchemy import event, select, update
from sqlalchemy.exc import DBAPIError, PendingRollbackError
import sqlalchemy.ext.asyncio.session as native_async_session
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util.concurrency import await_only

from cryptalis.crypto import Keyring, KeyUnavailable
import cryptalis.crypto.keys as key_module
from cryptalis.sqlalchemy import attach
from test_migration import PublicFixtureProvider, TENANT, keys, publish, run
from test_private_public_update import public_update_application


async def maybe(value):
    return await value if inspect.isawaitable(value) else value


def protected_rows(app):
    with app.owner.connect() as connection:
        return connection.exec_driver_sql(
            f'SELECT row_to_json(t) FROM "{app.schema}".customer t ORDER BY id').scalars().all()


def lock_observation(app):
    """An independent owner transaction probes the exact outer-write row."""
    with app.owner.begin() as connection:
        try:
            label = connection.exec_driver_sql(
                f'SELECT label FROM "{app.schema}".public_task WHERE id=%s FOR UPDATE NOWAIT',
                (UUID(int=2000),)).scalar_one()
        except DBAPIError as error:
            assert error.orig.sqlstate == '55P03'
            return 'locked', None
        return 'available', label


async def session_for(app, mode, attached, resolver=keys):
    engine = None
    if mode == 'async':
        engine = create_async_engine('postgresql+psycopg://', hide_parameters=True,
            async_creator=lambda: psycopg.AsyncConnection.connect(
                os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
        factory = (await attach(app.mapping, engine, lock=app.plan.lock_bytes,
            keys=resolver, deployment=(app.plan, app.pin))) if attached else async_sessionmaker(engine)
    else:
        factory = (attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
            keys=resolver, deployment=(app.plan, app.pin))) if attached else sessionmaker(app.runtime)
    if attached:
        factory._owner._experimental_public_update_tables = (app.public_table,)
    return factory(tenant_id=TENANT) if attached else factory(), engine


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('nested', [False, True], ids=['root', 'savepoint'])
def test_public_update_database_error_matches_native_transaction(mode, nested):
    """A real int4 overflow must retain native Session/SAVEPOINT semantics.

    Observe state before explicit rollback and before Session.close can rescue
    cleanup. Then use the same Session successfully, checking outer-work scope
    and exact protected storage with an independent owner connection.
    """
    observations = []
    for attached in (False, True):
        with public_update_application() as app:
            if attached:
                run(app); publish(app)
            baseline = protected_rows(app)

            async def scenario():
                session, engine = await session_for(app, mode, attached)
                P = app.PublicTask
                try:
                    await maybe(session.execute(update(P).where(P.id == UUID(int=2000)).values(label='outer-valid')))
                    transaction = await maybe(session.begin_nested()) if nested else session.get_transaction()
                    with pytest.raises(DBAPIError) as caught:
                        await maybe(session.execute(update(P).where(P.id == UUID(int=2002)).values(rank=2**40)))
                    assert caught.value.orig.sqlstate == '22003'
                    observed = (session.is_active, session.in_transaction(),
                        session.in_nested_transaction(), transaction.is_active, lock_observation(app))
                    await maybe(transaction.rollback() if nested else session.rollback())
                    assert session.is_active
                    await maybe(session.execute(update(P).where(P.id == UUID(int=2002)).values(label='recovered')))
                    await maybe(session.commit())
                    # No close/expunge/new Session hides a failed-unit mismatch.
                    recovered = [tuple(row) for row in await maybe(session.execute(
                        select(P.id, P.label, P.rank).order_by(P.id)))]
                    assert recovered[0][1] == ('outer-valid' if nested else None)
                    assert recovered[2][1:] == ('recovered', 2)
                    await maybe(session.rollback())
                    assert lock_observation(app) == ('available', 'outer-valid' if nested else None)
                    assert protected_rows(app) == baseline
                    return observed
                finally:
                    await maybe(session.close())
                    if engine is not None:
                        await engine.dispose()

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], f'Native/attached failed transaction differs: {observations}'


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('nested', [False, True], ids=['root', 'savepoint'])
def test_public_update_actual_autoflush_integrity_error_keeps_native_failed_unit(mode, nested):
    """The DBAPIError correction must not revive an actual failed ORM flush."""
    observations = []
    for attached in (False, True):
        with public_update_application() as app:
            if attached:
                run(app); publish(app)
            baseline = protected_rows(app)

            async def scenario():
                session, engine = await session_for(app, mode, attached)
                P = app.PublicTask
                try:
                    await maybe(session.execute(update(P).where(P.id == UUID(int=2000)).values(label='outer-valid')))
                    transaction = await maybe(session.begin_nested()) if nested else session.get_transaction()
                    # "exact" already exists for this tenant: native and encrypted
                    # unique indexes must both fail the real pending INSERT.
                    pending = app.Customer(id=UUID(int=9001), tenant_id=TENANT, name='exact', label='never-written')
                    session.add(pending)
                    with pytest.raises(DBAPIError) as caught:
                        await maybe(session.execute(update(P).where(P.id == UUID(int=2002)).values(label='never-updated')))
                    assert caught.value.orig.sqlstate == '23505'
                    observed = (session.is_active, session.in_transaction(),
                        session.in_nested_transaction(), transaction.is_active,
                        pending in session, lock_observation(app))
                    assert not session.is_active and not transaction.is_active
                    await maybe(transaction.rollback() if nested else session.rollback())
                    await maybe(session.execute(update(P).where(P.id == UUID(int=2002)).values(label='recovered')))
                    await maybe(session.commit())
                    with app.owner.connect() as connection:
                        rows = connection.exec_driver_sql(f'SELECT label FROM "{app.schema}".public_task ORDER BY id').scalars().all()
                    assert rows[0] == ('outer-valid' if nested else None)
                    assert rows[2] == 'recovered'
                    assert protected_rows(app) == baseline
                    assert lock_observation(app) == ('available', 'outer-valid' if nested else None)
                    return observed
                finally:
                    await maybe(session.close())
                    if engine is not None:
                        await engine.dispose()

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], f'Actual autoflush failure differs: {observations}'


class FaultProvider(PublicFixtureProvider):
    def __init__(self):
        self.offline = False
        self.calls = []

    def unwrap(self, wrapper, context):
        if self.offline:
            self.calls.append('fault')
            raise RuntimeError('A2_PROVIDER_DETAIL_MUST_NOT_ESCAPE')
        return super().unwrap(wrapper, context)


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('nested', [False, True], ids=['root', 'savepoint'])
@pytest.mark.parametrize('fault', ['cold_unavailable', 'expired_renewal'])
def test_public_update_provider_failure_at_autoflush_matches_native(mode, nested, fault, monkeypatch):
    observations = []
    for attached in (False, True):
        with public_update_application() as app:
            if attached:
                run(app); publish(app)
            baseline = protected_rows(app)

            async def scenario():
                healthy = keys(TENANT)
                rings = {TENANT: healthy}
                session, engine = await session_for(app, mode, attached, rings.__getitem__)
                sync_engine = engine.sync_engine if engine is not None else app.runtime
                provider = FaultProvider()
                calls, emitted = [], []
                def native_fault(connection, cursor, statement, *rest):
                    if statement.lstrip().upper().startswith('INSERT '):
                        calls.append('fault')
                        raise KeyUnavailable()
                def observe(connection, cursor, statement, *rest):
                    if statement.lstrip().upper().startswith(('INSERT ', 'UPDATE ', 'DELETE ')):
                        emitted.append(statement.split(None, 1)[0].upper())
                P = app.PublicTask
                try:
                    await maybe(session.execute(update(P).where(P.id == UUID(int=2000)).values(label='outer-valid')))
                    transaction = await maybe(session.begin_nested()) if nested else session.get_transaction()
                    pending = app.Customer(id=UUID(int=9002), tenant_id=TENANT, name='pending-provider', label='never-written')
                    session.add(pending)
                    provider.offline = False
                    ring = Keyring(healthy.policy, {provider.provider_id: provider}, max_age=1)
                    # Substitute only the key module's clock object. Asyncio and
                    # the process clock retain real time; no private cache edits.
                    now = [time.monotonic()]
                    with monkeypatch.context() as patch:
                        patch.setattr(key_module, 'time', SimpleNamespace(
                            monotonic=lambda: now[0], monotonic_ns=time.monotonic_ns))
                        if attached and fault == 'expired_renewal':
                            await maybe(ring.prepare_async() if mode == 'async' else ring.prepare())
                            now[0] += 2
                        provider.offline = True
                        rings[TENANT] = ring
                        if not attached:
                            event.listen(sync_engine, 'before_cursor_execute', native_fault)
                        event.listen(sync_engine, 'before_cursor_execute', observe)
                        with pytest.raises(KeyUnavailable) as caught:
                            await maybe(session.execute(update(P).where(P.id == UUID(int=2002)).values(label='never-updated')))
                        assert 'A2_PROVIDER_DETAIL_MUST_NOT_ESCAPE' not in str(caught.value)
                    assert (provider.calls if attached else calls) == ['fault']
                    assert emitted == []
                    observed = (session.is_active, session.in_transaction(),
                        session.in_nested_transaction(), transaction.is_active,
                        pending in session, lock_observation(app))
                    rings[TENANT] = healthy
                    event.remove(sync_engine, 'before_cursor_execute', observe)
                    if not attached:
                        event.remove(sync_engine, 'before_cursor_execute', native_fault)
                    await maybe(transaction.rollback() if nested else session.rollback())
                    assert session.is_active and pending not in session
                    await maybe(session.execute(update(P).where(P.id == UUID(int=2002)).values(label='recovered')))
                    await maybe(session.commit())
                    with app.owner.connect() as connection:
                        rows = connection.exec_driver_sql(f'SELECT label FROM "{app.schema}".public_task ORDER BY id').scalars().all()
                    assert rows[0] == ('outer-valid' if nested else None)
                    assert rows[2] == 'recovered'
                    assert protected_rows(app) == baseline
                    assert lock_observation(app) == ('available', 'outer-valid' if nested else None)
                    return observed
                finally:
                    rings[TENANT] = healthy
                    for callback in (native_fault, observe):
                        if event.contains(sync_engine, 'before_cursor_execute', callback):
                            event.remove(sync_engine, 'before_cursor_execute', callback)
                    await maybe(session.close())
                    if engine is not None:
                        await engine.dispose()

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], f'Provider/native failed unit differs: {observations}'


@pytest.mark.parametrize('nested', [False, True], ids=['root', 'savepoint'])
def test_public_update_real_async_cancellation_matches_native_cleanup(nested):
    """Cancel the actual pending task, not an injected CancelledError object."""
    observations = []
    for attached in (False, True):
        with public_update_application() as app:
            if attached:
                run(app); publish(app)
            baseline = protected_rows(app)

            async def scenario():
                healthy = keys(TENANT)
                rings = {TENANT: healthy}
                session, engine = await session_for(app, 'async', attached, rings.__getitem__)
                entered, never = asyncio.Event(), asyncio.Event()
                calls, emitted = [], []
                task = None
                P = app.PublicTask
                pending = app.Customer(id=UUID(int=9003), tenant_id=TENANT, name='pending-cancellation', label='never-written')
                class AwaitedProvider(PublicFixtureProvider):
                    def unwrap(self, *args):
                        raise AssertionError('Async UPDATE must use async provider preparation')
                    async def unwrap_async(self, *args):
                        calls.append('fault')
                        entered.set()
                        await never.wait()
                        raise AssertionError('Cancellation must interrupt the provider await')
                provider = AwaitedProvider()
                def native_fault(native_session, flush_context, instances):
                    # Preparation is before driver entry. Cancelling inside a
                    # cursor event instead invalidates the physical connection
                    # and is a different, whole-transaction native boundary.
                    assert pending in native_session.new
                    calls.append('fault')
                    entered.set()
                    await_only(never.wait())
                    raise AssertionError('Cancellation must interrupt native preparation')
                def observe(connection, cursor, statement, *rest):
                    if statement.lstrip().upper().startswith(('INSERT ', 'UPDATE ', 'DELETE ')):
                        emitted.append(statement.split(None, 1)[0].upper())
                async def work():
                    async with session.begin_nested() if nested else session.begin():
                        if not nested:
                            await session.execute(update(P).where(P.id == UUID(int=2000)).values(label='outer-valid'))
                        session.add(pending)
                        rings[TENANT] = Keyring(healthy.policy, {provider.provider_id: provider})
                        if not attached:
                            event.listen(session.sync_session, 'before_flush', native_fault)
                        event.listen(engine.sync_engine, 'before_cursor_execute', observe)
                        await session.execute(update(P).where(P.id == UUID(int=2002)).values(label='never-updated'))
                try:
                    if nested:
                        await session.execute(update(P).where(P.id == UUID(int=2000)).values(label='outer-valid'))
                    task = asyncio.create_task(work())
                    await asyncio.wait_for(entered.wait(), timeout=5)
                    task.cancel()
                    with pytest.raises(asyncio.CancelledError):
                        await asyncio.wait_for(task, timeout=5)
                    assert task.cancelled() and calls == ['fault'] and emitted == []
                    observed = (session.is_active, session.in_transaction(),
                        session.in_nested_transaction(), engine.sync_engine.pool.checkedout(),
                        pending in session, lock_observation(app))
                    assert observed == (True, nested, False, int(nested), False,
                        ('locked', None) if nested else ('available', None)), f'attached={attached}: {observed}'
                    assert protected_rows(app) == baseline
                    rings[TENANT] = healthy
                    if event.contains(session.sync_session, 'before_flush', native_fault):
                        event.remove(session.sync_session, 'before_flush', native_fault)
                    event.remove(engine.sync_engine, 'before_cursor_execute', observe)
                    await session.execute(update(P).where(P.id == UUID(int=2002)).values(label='recovered'))
                    await session.commit()
                    assert protected_rows(app) == baseline
                    assert lock_observation(app) == ('available', 'outer-valid' if nested else None)
                    with app.owner.connect() as connection:
                        assert connection.exec_driver_sql(f'SELECT label FROM "{app.schema}".public_task WHERE id=%s',
                            (UUID(int=2002),)).scalar_one() == 'recovered'
                    return observed
                finally:
                    if task is not None and not task.done():
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    rings[TENANT] = healthy
                    if event.contains(session.sync_session, 'before_flush', native_fault):
                        event.remove(session.sync_session, 'before_flush', native_fault)
                    if event.contains(engine.sync_engine, 'before_cursor_execute', observe):
                        event.remove(engine.sync_engine, 'before_cursor_execute', observe)
                    await session.close()
                    await engine.dispose()

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], f'Cancelled native/attached unit differs: {observations}'


@pytest.mark.parametrize('nested', [False, True], ids=['root', 'savepoint'])
def test_public_update_async_synthetic_post_result_failure_is_quarantined(nested, monkeypatch):
    """Synthetic fault after native result completion protects outer quarantine.

    This is not a reproduced psycopg cursor fault. The exact native async result
    helper first completes successfully for a genuine UPDATE RETURNING. We
    record its actual result/cursor reach, then raise at that function's return
    boundary. Native committability and attached quarantine are both observed.
    """
    for attached in (False, True):
        with public_update_application() as app:
            if attached:
                run(app); publish(app)
            baseline = protected_rows(app)

            async def scenario():
                session, engine = await session_for(app, 'async', attached)
                P = app.PublicTask
                executed, reached = [], []
                original_ensure = native_async_session._ensure_sync_result
                assert native_async_session.AsyncSession.execute.__globals__['_ensure_sync_result'] is original_ensure
                failure = DBAPIError(None, None, RuntimeError('synthetic post-native-result boundary'))
                def record_success(connection, cursor, statement, *rest):
                    if statement.lstrip().upper().startswith('UPDATE '):
                        executed.append(cursor)
                async def fault_after_native_result(result, calling_method):
                    completed = await original_ensure(result, calling_method)
                    cursor_result = result if getattr(result, '_is_cursor', False) else getattr(result, 'raw', None)
                    context = getattr(cursor_result, 'context', None)
                    assert context is not None and context.isupdate
                    assert len(executed) == 1 and context.cursor is executed[0]
                    reached.append({
                        'attached': attached, 'nested': nested,
                        'result_type': type(result).__module__ + '.' + type(result).__qualname__,
                        'is_cursor': bool(getattr(result, '_is_cursor', False)),
                        'cursor_present_after_native_helper': getattr(cursor_result, 'cursor', None) is not None,
                        'driver_cursor_type': type(context.cursor).__module__ + '.' + type(context.cursor).__qualname__,
                        'native_helper_completed': completed is result,
                        'genuine_update_completed': True,
                        'synthetic_exception_reached': False,
                        'fault_kind': 'synthetic after native _ensure_sync_result returned; not a natural driver fault',
                    })
                    assert completed is result and list(completed.keys()) == ['id', 'label']
                    reached[-1]['synthetic_exception_reached'] = True
                    raise failure
                try:
                    await session.execute(update(P).where(P.id == UUID(int=2000)).values(label='outer-valid'))
                    transaction = await session.begin_nested() if nested else session.get_transaction()
                    event.listen(engine.sync_engine, 'after_cursor_execute', record_success)
                    with monkeypatch.context() as patch:
                        patch.setattr(native_async_session, '_ensure_sync_result', fault_after_native_result)
                        with pytest.raises(DBAPIError) as caught:
                            table = app.public_table
                            await session.execute(update(table).where(table.c.id == UUID(int=2002))
                                .values(label='completed-before-result-fault').returning(table.c.id, table.c.label))
                        assert caught.value is failure
                    event.remove(engine.sync_engine, 'after_cursor_execute', record_success)
                    assert len(executed) == len(reached) == 1, f'attached={attached}: injection must fire once'
                    assert session.is_active is (not attached), f'attached={attached}'
                    assert transaction.is_active is (not attached)
                    if attached:
                        with pytest.raises(PendingRollbackError):
                            await session.commit()
                        if nested:
                            await transaction.rollback()
                            await session.commit()
                        else:
                            await session.rollback()
                    else:
                        # Demonstrate the native distinction with actual committed
                        # synthetic rows; no claim of identical post-result policy.
                        await session.commit()
                    with app.owner.connect() as connection:
                        rows = connection.exec_driver_sql(f'SELECT label FROM "{app.schema}".public_task ORDER BY id').scalars().all()
                    assert rows[0] == ('outer-valid' if not attached or nested else None)
                    assert rows[2] == ('old-2' if attached else 'completed-before-result-fault')
                    assert protected_rows(app) == baseline
                    assert engine.sync_engine.pool.checkedout() == 0
                    await session.execute(update(P).where(P.id == UUID(int=2002)).values(label='recovered'))
                    await session.commit()
                    assert lock_observation(app) == ('available', rows[0])
                    assert protected_rows(app) == baseline
                finally:
                    evidence = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent
                    (evidence / f'a2-post-result-reach-{attached}-{nested}.json').write_text(json.dumps(reached, indent=2) + '\n')
                    if event.contains(engine.sync_engine, 'after_cursor_execute', record_success):
                        event.remove(engine.sync_engine, 'after_cursor_execute', record_success)
                    await session.close()
                    await engine.dispose()

            asyncio.run(scenario())

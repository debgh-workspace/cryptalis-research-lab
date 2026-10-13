"""Independent transaction-state and database-lock oracles for async failure cleanup."""

import asyncio

import pytest
from sqlalchemy import event, select
from sqlalchemy.exc import DBAPIError

from cryptalis.crypto import Keyring, KeyUnavailable
from test_sqlalchemy_search import _async_factory, _row, search_application


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
@pytest.mark.parametrize("fault", ["provider", "cancel"])
@pytest.mark.parametrize("boundary", ["body", "exit"])
def test_async_transaction_failure_releases_state_connection_and_row_lock(protected, fault, boundary):
    """Observe before Session.close: final cleanup must not hide a failed exit.

    Native controls raise the same exception in the body or before commit.
    Protected exit cells fail at an actual cold key-provider preparation call.
    Cancellation here is an injected CancelledError; real task cancellation has
    a separate test and must not be inferred from this control.
    """
    with search_application(protected, attach_now=False) as app:
        async def run():
            engine, sessions = await _async_factory(app)
            session = None
            original_unwrap = app.provider.unwrap_async
            healthy = app.rings[app.tenant]
            error = KeyUnavailable if fault == "provider" else asyncio.CancelledError
            calls = []
            try:
                row = _row(app, "before", 1)
                identity = row.id
                async with sessions(tenant_id=app.tenant) as seed:
                    seed.add(row)
                    await seed.commit()
                session = sessions(tenant_id=app.tenant)

                async def fail_provider(*args):
                    calls.append("provider")
                    raise error()

                def fail_commit(*args):
                    calls.append("native-commit")
                    raise error()

                with pytest.raises(error):
                    async with session.begin():
                        current = await session.get(app.Customer, identity)
                        current.name, current.rank = "after", 2
                        await session.flush()
                        # Use public keyring construction to create a cold lease;
                        # no mutation of cache internals or process-wide clocks.
                        if protected:
                            app.provider.unwrap_async = fail_provider
                            app.rings[app.tenant] = Keyring(healthy.policy, {app.provider.provider_id: app.provider})
                        elif boundary == "exit":
                            event.listen(session.sync_session, "before_commit", fail_commit, once=True)
                        if boundary == "body":
                            raise error()

                # Independent owner connection proves both rollback visibility
                # and lock release, before any session close can rescue them.
                locked = False
                with app.owner_engine.begin() as connection:
                    connection.exec_driver_sql("SET LOCAL lock_timeout = '100ms'")
                    try:
                        rank = connection.exec_driver_sql(
                            f'SELECT rank FROM "{app.schema}".customer WHERE id = %s FOR UPDATE',
                            (identity,)).scalar_one()
                    except DBAPIError as exc:
                        if getattr(exc.orig, "sqlstate", None) != "55P03":
                            raise
                        locked, rank = True, None
                observed = (session.in_transaction(), engine.sync_engine.pool.checkedout(), locked, rank)
                assert calls == ([] if boundary == "body" else ["provider" if protected else "native-commit"])
                assert observed == (False, 0, False, 1)
                # A surviving externally owned session must accept a new unit
                # of work after the failed context, not merely be disposable.
                app.provider.unwrap_async = original_unwrap
                app.rings[app.tenant] = healthy
                async with session.begin():
                    assert await session.scalar(select(app.Customer.name).where(app.Customer.id == identity)) == "before"
            finally:
                app.provider.unwrap_async = original_unwrap
                app.rings[app.tenant] = healthy
                if session is not None:
                    await session.close()
                await engine.dispose()
        asyncio.run(run())


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
def test_real_task_cancellation_releases_transaction_before_session_close(protected):
    """Cancel a suspended provider await; native control suspends in the body."""
    with search_application(protected, attach_now=False) as app:
        async def run():
            engine, sessions = await _async_factory(app)
            session, task = None, None
            original_unwrap, healthy = app.provider.unwrap_async, app.rings[app.tenant]
            entered, never = asyncio.Event(), asyncio.Event()
            try:
                row = _row(app, "before", 1)
                identity = row.id
                async with sessions(tenant_id=app.tenant) as seed:
                    seed.add(row)
                    await seed.commit()
                session = sessions(tenant_id=app.tenant)

                async def blocked_provider(*args):
                    entered.set()
                    await never.wait()
                    raise AssertionError("The provider must be cancelled, not released")

                async def work():
                    async with session.begin():
                        current = await session.get(app.Customer, identity)
                        current.rank = 2
                        await session.flush()
                        if protected:
                            app.provider.unwrap_async = blocked_provider
                            app.rings[app.tenant] = Keyring(healthy.policy, {app.provider.provider_id: app.provider})
                        else:
                            entered.set()
                            await never.wait()

                task = asyncio.create_task(work())
                await asyncio.wait_for(entered.wait(), timeout=5)
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
                assert task.cancelled()
                # A real independent NOWAIT lock probe distinguishes cleanup
                # from merely observing the old committed row under MVCC.
                blocked = False
                with app.owner_engine.begin() as connection:
                    try:
                        rank = connection.exec_driver_sql(
                            f'SELECT rank FROM "{app.schema}".customer WHERE id = %s FOR UPDATE NOWAIT',
                            (identity,)).scalar_one()
                    except DBAPIError as exc:
                        if getattr(exc.orig, "sqlstate", None) != "55P03":
                            raise
                        blocked, rank = True, None
                assert (session.in_transaction(), engine.sync_engine.pool.checkedout(), blocked, rank) == (False, 0, False, 1)
            finally:
                if task is not None and not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                app.provider.unwrap_async = original_unwrap
                app.rings[app.tenant] = healthy
                if session is not None:
                    await session.close()
                await engine.dispose()
        asyncio.run(run())

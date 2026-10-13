"""SQLAlchemy 2.1 collection methods must prepare keys before implicit I/O."""

import asyncio
import os
from uuid import uuid4

import psycopg
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

pytestmark = pytest.mark.skipif(not hasattr(AsyncSession, "merge_all"),
    reason="Native collection APIs were introduced in SQLAlchemy 2.1; not part of the 2.0 cell")

from cryptalis.sqlalchemy import attach
from test_sqlalchemy_adapter import TENANT, app, db, runtime_access


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
@pytest.mark.parametrize("warm", [False, True], ids=["cold", "warm"])
@pytest.mark.parametrize("method", ["merge_all", "delete_all"])
def test_async_collection_methods_preserve_native_detached_behavior(app, runtime_access, protected, warm, method):
    if protected:
        app.switch()

    async def scenario():
        engine = create_async_engine("postgresql+psycopg://", hide_parameters=True,
            async_creator=lambda: psycopg.AsyncConnection.connect(os.environ["CRYPTALIS_TEST_RUNTIME_DATABASE_URL"]))
        try:
            if protected:
                factory = await attach(app.mapping, engine, lock=app.plan.lock_bytes, keys=app.rings.__getitem__)
            else:
                native = async_sessionmaker(engine)
                factory = lambda *, tenant_id, **options: native(**options)
            identities = [uuid4(), uuid4()]
            rows = [app.Customer(id=identity, tenant_id=TENANT, name=f"collection-{i}",
                                 note=value, secret="private fixture", rank=i)
                    for i, (identity, value) in enumerate(zip(identities, (None, "é 雪")))]
            async with factory(tenant_id=TENANT, expire_on_commit=False) as seed:
                seed.add_all(rows)
                await seed.commit()
            if method == "merge_all":
                rows[0].note = "edited while detached"
            async with factory(tenant_id=TENANT) as session:
                if warm:
                    await session.get(app.Customer, identities[0])
                if method == "merge_all":
                    merged = await session.merge_all(rows)
                    assert len(merged) == 2
                    assert [row.note for row in merged] == ["edited while detached", "é 雪"]
                    assert all(current is not detached for current, detached in zip(merged, rows))
                else:
                    # An unloaded relationship performs an implicit SELECT even
                    # with no child rows. The restricted runtime has SELECT only.
                    await session.delete_all(rows)
                await session.commit()
            async with factory(tenant_id=TENANT) as check:
                actual = [tuple(row) for row in await check.execute(select(app.Customer.rank, app.Customer.note).order_by(app.Customer.rank))]
                assert actual == ([(0, "edited while detached"), (1, "é 雪")] if method == "merge_all" else [])
        finally:
            await engine.dispose()
    asyncio.run(scenario())


@pytest.mark.parametrize("fault", ["provider", "cancel"])
def test_merge_all_prepares_before_implicit_io_and_preserves_failure(fault):
    from sqlalchemy import event
    from cryptalis.crypto import Keyring, KeyUnavailable
    from test_sqlalchemy_search import _async_factory, _row, search_application

    with search_application(True, attach_now=False) as state:
        async def scenario():
            engine, sessions = await _async_factory(state)
            healthy = state.rings[state.tenant]
            original = state.provider.unwrap_async
            failure = KeyUnavailable if fault == "provider" else asyncio.CancelledError
            calls, statements = [], []
            def capture(*args):
                statements.append("SQL")
            async def fail(*args):
                calls.append("unwrap")
                raise failure()
            try:
                row = _row(state, "original", 1)
                identity = row.id
                async with sessions(tenant_id=state.tenant, expire_on_commit=False) as seed:
                    seed.add(row)
                    await seed.commit()
                row.name = "detached update"
                state.provider.unwrap_async = fail
                state.rings[state.tenant] = Keyring(healthy.policy, {state.provider.provider_id: state.provider})
                event.listen(engine.sync_engine, "before_cursor_execute", capture)
                async with sessions(tenant_id=state.tenant) as session:
                    with pytest.raises(failure):
                        await session.merge_all([row])
                    assert calls == ["unwrap"]
                    assert statements == []
                    assert not session.in_transaction()
                    assert not session.dirty and not session.new
                    state.provider.unwrap_async = original
                    state.rings[state.tenant] = healthy
                    assert (await session.get(state.Customer, identity)).name == "original"
                    merged = await session.merge_all([row])
                    assert merged[0].name == "detached update"
                    await session.commit()
                async with sessions(tenant_id=state.tenant) as check:
                    assert (await check.get(state.Customer, identity)).name == "detached update"
            finally:
                state.provider.unwrap_async = original
                state.rings[state.tenant] = healthy
                event.remove(engine.sync_engine, "before_cursor_execute", capture)
                await engine.dispose()
        asyncio.run(scenario())

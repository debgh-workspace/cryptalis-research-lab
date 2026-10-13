"""Independent native state and raw PostgreSQL oracles for nested failures."""
import asyncio
import pytest
from sqlalchemy import event,select
from cryptalis.crypto import Keyring,KeyUnavailable
from test_sqlalchemy_search import _async_factory,_row,search_application

@pytest.mark.parametrize('protected',[False,True],ids=['native','attached'])
@pytest.mark.parametrize('fault',['provider','cancel'])
def test_nested_exit_failure_releases_inner_lock_and_keeps_outer_usable(protected,fault):
    with search_application(protected,attach_now=False) as app:
        async def scenario():
            engine,sessions=await _async_factory(app)
            healthy=app.rings[app.tenant];original=app.provider.unwrap_async
            error=KeyUnavailable if fault=='provider' else asyncio.CancelledError
            try:
                row=_row(app,'before',1);identity=row.id
                async with sessions(tenant_id=app.tenant) as seed:
                    seed.add(row);await seed.commit()
                async with sessions(tenant_id=app.tenant) as s:
                    async with s.begin():
                        with pytest.raises(error):
                            async with s.begin_nested():
                                current=await s.get(app.Customer,identity);current.name='inner edit';current.rank=2
                                await s.flush()
                                if protected:
                                    async def fail(*args):raise error()
                                    app.provider.unwrap_async=fail
                                    app.rings[app.tenant]=Keyring(healthy.policy,{app.provider.provider_id:app.provider})
                                else:
                                    def fail_commit(*args):raise error()
                                    event.listen(s.sync_session,'before_commit',fail_commit,once=True)
                        assert s.in_transaction() and not s.in_nested_transaction()
                        # Lock release must precede outer rollback/session close.
                        with app.owner_engine.begin() as c:
                            assert c.exec_driver_sql(f'SELECT rank FROM "{app.schema}".customer WHERE id=%s FOR UPDATE NOWAIT',(identity,)).scalar_one()==1
                        app.provider.unwrap_async=original;app.rings[app.tenant]=healthy
                        assert await s.scalar(select(app.Customer.name).where(app.Customer.id==identity))=='before'
                        s.add(_row(app,'after',3))
                    assert not s.in_transaction()
                async with sessions(tenant_id=app.tenant) as s:
                    assert list(await s.scalars(select(app.Customer.rank).order_by(app.Customer.rank)))==[1,3]
                assert engine.sync_engine.pool.checkedout()==0
            finally:
                app.provider.unwrap_async=original;app.rings[app.tenant]=healthy
                await engine.dispose()
        asyncio.run(scenario())

@pytest.mark.parametrize('protected',[False,True],ids=['native','attached'])
def test_cancelled_nested_exit_cleans_permission_and_reuses_pool(protected):
    with search_application(protected,attach_now=False) as app:
        async def scenario():
            engine,sessions=await _async_factory(app)
            healthy=app.rings[app.tenant];original=app.provider.unwrap_async
            entered=asyncio.Event();never=asyncio.Event()
            session=sessions(tenant_id=app.tenant)
            async def block(*args):entered.set();await never.wait()
            async def work():
                async with session.begin():
                    async with session.begin_nested():
                        session.add(_row(app,'cancelled',1));await session.flush()
                        if protected:
                            app.provider.unwrap_async=block
                            app.rings[app.tenant]=Keyring(healthy.policy,{app.provider.provider_id:app.provider})
                        else:await block()
            task=asyncio.create_task(work())
            try:
                await asyncio.wait_for(entered.wait(),5);task.cancel()
                with pytest.raises(asyncio.CancelledError):await task
                assert not session.in_transaction() and engine.sync_engine.pool.checkedout()==0
                app.provider.unwrap_async=original;app.rings[app.tenant]=healthy
                async with session.begin():assert list(await session.scalars(select(app.Customer.rank)))==[]
                # Independent physical row count, no decryption needed.
                with app.owner_engine.connect() as c:assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".customer').scalar_one()==0
            finally:
                if not task.done():task.cancel()
                app.provider.unwrap_async=original;app.rings[app.tenant]=healthy
                await session.close();await engine.dispose()
        asyncio.run(scenario())

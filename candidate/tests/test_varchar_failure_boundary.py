"""VARCHAR value refusal preserves native failed-unit boundaries."""
import asyncio,inspect
import pytest
from sqlalchemy import String,select,event
from sqlalchemy.exc import DataError,PendingRollbackError
from test_sqlalchemy_search import search_application,_row,_async_factory
from cryptalis._native_text import CharacterLimitExceeded

async def maybe(value):return await value if inspect.isawaitable(value) else value

@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('nested',[False,True])
def test_overlength_value_matches_native_rollback_boundary(mode,nested):
    outcomes=[]
    for protected in (False,True):
        with search_application(protected,attach_now=mode=='sync',field_type=String(3,collation='C')) as app:
            async def scenario():
                async_engine=None
                if mode=='async':async_engine,factory=await _async_factory(app);engine=async_engine.sync_engine
                else:factory=app.sessions;engine=app.engine
                sql=[]
                def observe(c,cursor,statement,parameters,context,many):sql.append(statement)
                event.listen(engine,'before_cursor_execute',observe)
                s=factory(tenant_id=app.tenant)
                try:
                    s.add(_row(app,'pre',1));await maybe(s.flush())
                    savepoint=await maybe(s.begin_nested()) if nested else None
                    s.add(_row(app,'abcd',2));sql.clear()
                    with pytest.raises(CharacterLimitExceeded if protected else DataError) as failure:
                        await maybe(s.flush())
                    if protected:
                        assert not any(q.lstrip().upper().startswith(('INSERT ','UPDATE ','DELETE ','SELECT ')) for q in sql)
                    else:assert failure.value.orig.sqlstate=='22001'
                    with pytest.raises(PendingRollbackError):await maybe(s.commit())
                    if nested:
                        await maybe(savepoint.rollback());await maybe(s.commit())
                    else:await maybe(s.rollback())
                    await maybe(s.close())
                    fresh=factory(tenant_id=app.tenant)
                    try:return list(await maybe(fresh.scalars(select(app.Customer.name))))
                    finally:await maybe(fresh.close())
                finally:
                    await maybe(s.close());event.remove(engine,'before_cursor_execute',observe)
                    if async_engine is not None:await async_engine.dispose()
            outcomes.append(asyncio.run(scenario()))
    assert outcomes==[['pre'],['pre']] if nested else outcomes==[[],[]]

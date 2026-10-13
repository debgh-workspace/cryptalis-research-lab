"""A6 real compiled VARCHAR plan and actual guarded runtime, no plugins."""
import asyncio,inspect
import pytest
from sqlalchemy import String,select
from test_sqlalchemy_search import search_application,_row,_async_factory

async def maybe(value):return await value if inspect.isawaitable(value) else value

@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('action',['insert','update'])
@pytest.mark.parametrize('supplied',[None,'abc ','ab  ','雪😀é'])
def test_varchar_runtime_preserves_native_state_and_search(mode,action,supplied):
    outcomes=[]
    for protected in (False,True):
        with search_application(protected,attach_now=mode=='sync',field_type=String(3,collation='C')) as app:
            async def scenario():
                engine=None
                if mode=='async':engine,factory=await _async_factory(app)
                else:factory=app.sessions
                s=factory(tenant_id=app.tenant)
                try:
                    row=_row(app,'old' if action=='update' else supplied,1);s.add(row)
                    if action=='update':await maybe(s.flush());row.name=supplied
                    await maybe(s.flush());assigned=row.name
                    stored=(await maybe(s.scalars(select(app.Customer.name).where(app.Customer.id==row.id)))).one()
                    matched=bool(list(await maybe(s.scalars(select(app.Customer.id).where(app.Customer.name==supplied)))))
                    await maybe(s.refresh(row));refreshed=row.name
                    await maybe(s.rollback())
                    return assigned,stored,refreshed,matched
                finally:
                    await maybe(s.close())
                    if engine is not None:await engine.dispose()
            outcomes.append(asyncio.run(scenario()))
    assert outcomes[0]==outcomes[1]
    assert outcomes[1][0]==supplied

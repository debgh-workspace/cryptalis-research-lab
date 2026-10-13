"""Negative controls: no implicit flush means no failed-flush rollback."""
import asyncio,inspect,sys
from pathlib import Path
import pytest
from sqlalchemy import select,event
from test_sqlalchemy_search import search_application,_row,_async_factory
from cryptalis.crypto import Keyring,KeyUnavailable
async def maybe(value):return await value if inspect.isawaitable(value) else value

@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('suppression',['session','context','statement','call','clean_read','clean_commit','clean_flush'])
def test_provider_failure_without_native_flush_preserves_unit(mode,suppression):
 with search_application(True,attach_now=mode=='sync') as app:
  async def scenario():
   engine=None
   if mode=='async':engine,factory=await _async_factory(app)
   else:factory=app.sessions
   s=factory(tenant_id=app.tenant);healthy=app.rings[app.tenant]
   original=app.provider.unwrap;original_async=app.provider.unwrap_async
   calls=[]
   def fail(*args):calls.append(1);raise KeyUnavailable()
   async def fail_async(*args):return fail()
   try:
    s.add(_row(app,'prefix',1));await maybe(s.flush())
    if not suppression.startswith('clean_'):s.add(_row(app,'pending',2))
    if suppression=='session':s.autoflush=False
    app.provider.unwrap=fail;app.provider.unwrap_async=fail_async
    app.rings[app.tenant]=Keyring(healthy.policy,{app.provider.provider_id:app.provider})
    statement=select(app.Customer.rank)
    if suppression=='statement':statement=statement.execution_options(autoflush=False)
    if suppression=='core':statement=select(app.Customer.__table__.c.rank)
    try:
     if suppression=='clean_commit':await maybe(s.commit())
     elif suppression=='clean_flush':await maybe(s.flush())
     elif suppression=='context':
      with s.no_autoflush:await maybe(s.execute(statement))
     elif suppression=='call':await maybe(s.execute(statement,execution_options={'autoflush':False}))
     else:await maybe(s.execute(statement))
    except KeyUnavailable:pass
    # Sync clean commit/flush require no key at all; async currently prepares.
    assert s.is_active,'Read-only/preparation failure acquired a false failed-flush state'
    app.provider.unwrap=original;app.provider.unwrap_async=original_async;app.rings[app.tenant]=healthy
    s.expunge_all();await maybe(s.commit())
    assert list(await maybe(s.scalars(select(app.Customer.name))))==['prefix']
   finally:
    app.provider.unwrap=original;app.provider.unwrap_async=original_async;app.rings[app.tenant]=healthy
    await maybe(s.close())
    if engine is not None:await engine.dispose()
  asyncio.run(scenario())

"""Variant oracle: provider preparation before commit and query autoflush."""
import asyncio,inspect,sys,json,sqlalchemy
from pathlib import Path
import pytest
from sqlalchemy import event,select
from test_sqlalchemy_search import search_application,_row,_async_factory
CORPUS=[]
@pytest.fixture(scope='module',autouse=True)
def corpus_receipt():
 yield
 p=Path(__file__).resolve().parents[2]/'evidence'/('master-s4-compatibility-implicit-flush-corpus-v1-sa'+sqlalchemy.__version__+'.json')
 p.write_text(json.dumps({'version':'cryptalis.compatibility-corpus/v1','results':CORPUS,'scope':'Commit and implicit ORM SELECT flush preparation failures; async-only streams are extra controls, not four-cell corpus entries.'},indent=2))

async def maybe(value):
 return await value if inspect.isawaitable(value) else value
@pytest.mark.parametrize('mode,entrypoint', [(m,n) for m,names in [('sync',('commit','autoflush','scalar','scalars')),('async',('commit','autoflush','scalar','scalars','stream','stream_scalars'))] for n in names])
@pytest.mark.parametrize('nested',[False,True])
def test_provider_failure_at_implicit_flush_boundary(mode,nested,entrypoint):
 record={'id':'provider_implicit_'+entrypoint+('_savepoint' if nested else '_root'),'mode':mode,'classification':'DEFECT'}
 if entrypoint not in ('stream','stream_scalars'):CORPUS.append(record)
 from sqlalchemy import event
 from cryptalis.crypto import Keyring,KeyUnavailable
 observations=[]
 for protected in (False,True):
  with search_application(protected,attach_now=mode=='sync') as app:
   async def scenario():
    engine=None
    if mode=='async':engine,sessions=await _async_factory(app);sync_engine=engine.sync_engine
    else:sessions=app.sessions;sync_engine=app.engine
    s=sessions(tenant_id=app.tenant);calls=[]
    healthy=app.rings[app.tenant];original_sync=app.provider.unwrap;original_async=app.provider.unwrap_async
    def fail(*args):calls.append('fault');raise KeyUnavailable()
    async def fail_async(*args):return fail()
    def native_fault(c,cursor,statement,*args):
     if statement.lstrip().upper().startswith(('INSERT ','UPDATE ','DELETE ')):fail()
    try:
     s.add(_row(app,'outer-valid',1));await maybe(s.flush())
     tx=await maybe(s.begin_nested()) if nested else None
     if nested:s.add(_row(app,'inner-valid',2));await maybe(s.flush())
     if protected:
      app.provider.unwrap=fail;app.provider.unwrap_async=fail_async
      app.rings[app.tenant]=Keyring(healthy.policy,{app.provider.provider_id:app.provider})
     else:event.listen(sync_engine,'before_cursor_execute',native_fault)
     s.add(_row(app,'never-written',3))
     with pytest.raises(KeyUnavailable):
      if entrypoint=='commit':await maybe(tx.commit() if tx is not None else s.commit())
      else:await maybe(getattr(s,'execute' if entrypoint=='autoflush' else entrypoint)(select(app.Customer.rank)))
     active=s.is_active
     app.provider.unwrap=original_sync;app.provider.unwrap_async=original_async;app.rings[app.tenant]=healthy
     if not protected:event.remove(sync_engine,'before_cursor_execute',native_fault)
     s.expunge_all()
     try:await maybe(tx.commit() if tx is not None else s.commit());outcome='COMMITTED'
     except Exception as exc:
      outcome=type(exc).__name__;await maybe(tx.rollback() if tx is not None else s.rollback())
     if nested:await maybe(s.commit())
     stored=list(await maybe(s.scalars(select(app.Customer.name).order_by(app.Customer.rank))))
     assert calls==['fault']
     return active,outcome,stored
    finally:
     app.provider.unwrap=original_sync;app.provider.unwrap_async=original_async;app.rings[app.tenant]=healthy
     if not protected and event.contains(sync_engine,'before_cursor_execute',native_fault):event.remove(sync_engine,'before_cursor_execute',native_fault)
     await maybe(s.close())
     if engine is not None:await engine.dispose()
   observations.append(asyncio.run(scenario()))
 assert observations[0]==observations[1],f'Provider/native failed unit differs: {observations}'
 assert observations[0]==(False,'PendingRollbackError',['outer-valid'] if nested else [])
 record.update(classification='IDENTICAL',native_recovery=observations[0],protected_recovery=observations[1])


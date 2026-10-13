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
 p=Path(__file__).resolve().parents[2]/'evidence'/('master-s4-compatibility-core-flush-corpus-v1-sa'+sqlalchemy.__version__+'.json')
 p.write_text(json.dumps({'version':'cryptalis.compatibility-corpus/v1','results':CORPUS,'scope':'Native/protected preparation failure recovery, current product unless explicitly marked prototype'},indent=2)+'\n')

async def maybe(value):
 return await value if inspect.isawaitable(value) else value
@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('nested',[False,True])
@pytest.mark.parametrize('suppression',['none','statement','call','session','context','no_pending'])
def test_core_query_provider_boundary_matches_native_version(mode,nested,suppression):
 record={'id':'provider_core_'+suppression+('_savepoint' if nested else '_root'),'mode':mode,'classification':'DEFECT'};CORPUS.append(record)
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
     if statement.lstrip().upper().startswith(('INSERT ','UPDATE ','DELETE ','SELECT ')):fail()
    try:
     s.add(_row(app,'outer-valid',1));await maybe(s.flush())
     tx=await maybe(s.begin_nested()) if nested else None
     if nested:s.add(_row(app,'inner-valid',2));await maybe(s.flush())
     if protected:
      app.provider.unwrap=fail;app.provider.unwrap_async=fail_async
      app.rings[app.tenant]=Keyring(healthy.policy,{app.provider.provider_id:app.provider})
     else:event.listen(sync_engine,'before_cursor_execute',native_fault)
     if suppression!='no_pending':s.add(_row(app,'never-written',3))
     statement=select(app.Customer.__table__.c.rank)
     if suppression=='statement':statement=statement.execution_options(autoflush=False)
     if suppression=='session':s.autoflush=False
     with pytest.raises(KeyUnavailable):
      if suppression=='context':
       with s.no_autoflush:await maybe(s.execute(statement))
      elif suppression=='call':await maybe(s.execute(statement,execution_options={'autoflush':False}))
      else:await maybe(s.execute(statement))
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
 record.update(native_recovery=observations[0],protected_recovery=observations[1])
 assert observations[0]==observations[1],f'Provider/native failed unit differs: {observations}'
 record['classification']='IDENTICAL'
 # Native behavior is deliberately observed per dependency version, not assumed.


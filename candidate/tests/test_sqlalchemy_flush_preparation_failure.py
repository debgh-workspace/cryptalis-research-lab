"""Native failed-flush transaction boundaries, including an existing SAVEPOINT."""
import asyncio,inspect,json
from pathlib import Path
import sqlalchemy
from sqlalchemy import event
from sqlalchemy.exc import DataError
from cryptalis.crypto import InvalidText
import pytest
from sqlalchemy import select
from test_sqlalchemy_search import search_application,_row,_async_factory

CORPUS=[]
@pytest.fixture(scope='module',autouse=True)
def corpus_receipt():
 yield
 p=Path(__file__).resolve().parents[2]/'evidence'/('master-s4-compatibility-flush-corpus-v1-sa'+sqlalchemy.__version__+'.json')
 p.write_text(json.dumps({'version':'cryptalis.compatibility-corpus/v1','results':CORPUS,'scope':'NUL writes are REJECTED-LOUD; their transaction recovery must match native. Provider-failure unit transitions compare the same KeyUnavailable error and stored-state oracle.'},indent=2))

async def maybe(value):
 return await value if inspect.isawaitable(value) else value

@pytest.mark.parametrize('entrypoint',['flush','commit','autoflush'])
@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('nested',[False,True])
def test_rejected_text_flush_cannot_commit_a_prefix_that_native_discards(mode,nested,entrypoint):
 record={'id':'nul_rejection_'+entrypoint+('_savepoint' if nested else '_root'),'mode':mode,'classification':'DEFECT'};CORPUS.append(record)
 observations=[]
 for protected in (False,True):
  with search_application(protected,attach_now=mode=='sync') as app:
   async def scenario():
    engine=None
    if mode=='async':engine,sessions=await _async_factory(app)
    else:sessions=app.sessions
    s=sessions(tenant_id=app.tenant);writes=[]
    tracked=engine.sync_engine if engine is not None else app.engine
    def emitted(c,cursor,statement,*args):
     if statement.lstrip().upper().startswith(('INSERT ','UPDATE ','DELETE ')):writes.append(statement.split()[0])
    try:
     s.add(_row(app,'outer-valid',1));await maybe(s.flush())
     tx=await maybe(s.begin_nested()) if nested else None
     if nested:s.add(_row(app,'inner-valid',2));await maybe(s.flush())
     s.add(_row(app,'invalid\x00text',3))
     event.listen(tracked,'before_cursor_execute',emitted)
     with pytest.raises(InvalidText if protected else DataError) as initial:
      if entrypoint=='flush':await maybe(s.flush())
      elif entrypoint=='commit':await maybe(tx.commit() if tx is not None else s.commit())
      else:await maybe(s.execute(select(app.Customer.rank)))
     if protected:
      assert writes==[]
      record.update(reason=str(initial.value),alternative=initial.value.remedy,protected_data_sql=0)
     event.remove(tracked,'before_cursor_execute',emitted)
     active=s.is_active
     s.expunge_all()
     try:
      await maybe(tx.commit() if tx is not None else s.commit());outcome='COMMITTED'
     except Exception as exc:
      outcome=type(exc).__name__
      await maybe(tx.rollback() if tx is not None else s.rollback())
     if nested:await maybe(s.commit())
     stored=[r[0] for r in await maybe(s.execute(select(app.Customer.name).order_by(app.Customer.rank)))]
     return active,outcome,stored
    finally:
     if event.contains(tracked,'before_cursor_execute',emitted):event.remove(tracked,'before_cursor_execute',emitted)
     await maybe(s.close())
     if engine is not None:await engine.dispose()
   observations.append(asyncio.run(scenario()))
 assert observations[0]==observations[1],f'Native/protected failed flush boundary differs: {observations}'
 assert observations[0]==(False,'PendingRollbackError',['outer-valid'] if nested else [])
 record.update(classification='REJECTED-LOUD',native_recovery=observations[0],protected_recovery=observations[1])


@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('nested',[False,True])
def test_failed_preparation_rollback_quarantines_connection(mode,nested,monkeypatch):
 with search_application(True,attach_now=mode=='sync') as app:
  async def scenario():
   engine=None
   if mode=='async':engine,sessions=await _async_factory(app);sync_engine=engine.sync_engine
   else:sessions=app.sessions;sync_engine=app.engine
   s=sessions(tenant_id=app.tenant)
   try:
    s.add(_row(app,'outer',1));await maybe(s.flush())
    tx=await maybe(s.begin_nested()) if nested else None
    if nested:s.add(_row(app,'inner',2));await maybe(s.flush())
    if mode=='async':connection=(await s.connection()).sync_connection
    else:connection=s.connection()
    method='do_rollback_to_savepoint' if nested else 'do_rollback'
    original=getattr(sync_engine.dialect,method);called=[]
    def fail(*args):called.append(True);raise RuntimeError('PRIVATE_CLEANUP_DIAGNOSTIC')
    monkeypatch.setattr(sync_engine.dialect,method,fail)
    s.add(_row(app,'invalid\x00text',3))
    try:
     with pytest.raises(Exception) as caught:await maybe(s.flush())
    finally:monkeypatch.setattr(sync_engine.dialect,method,original)
    assert called and connection.invalidated, 'Failed cleanup must quarantine the physical connection'
    import traceback
    assert 'PRIVATE_CLEANUP_DIAGNOSTIC' not in ''.join(traceback.format_exception(caught.value))
    with app.owner_engine.connect() as c:
     assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".customer').scalar_one()==0
   finally:
    await maybe(s.close())
    if engine is not None:await engine.dispose()
  asyncio.run(scenario())

@pytest.mark.parametrize('mode',['sync','async'])
@pytest.mark.parametrize('nested',[False,True])
def test_provider_failure_during_flush_keeps_native_failed_unit_boundary(mode,nested):
 record={'id':'provider_failed_flush'+('_savepoint' if nested else '_root'),'mode':mode,'classification':'DEFECT'};CORPUS.append(record)
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
     with pytest.raises(KeyUnavailable):await maybe(s.flush())
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

@pytest.mark.parametrize('nested',[False,True])
def test_real_cancelled_provider_flush_matches_native_unit(nested):
 from sqlalchemy import event
 from sqlalchemy.util.concurrency import await_only
 from cryptalis.crypto import Keyring
 observations=[]
 for protected in (False,True):
  with search_application(protected,attach_now=False) as app:
   async def scenario():
    engine,sessions=await _async_factory(app);s=sessions(tenant_id=app.tenant)
    entered=asyncio.Event();never=asyncio.Event();calls=[]
    healthy=app.rings[app.tenant];original=app.provider.unwrap_async
    async def blocked(*args):calls.append(True);entered.set();await never.wait()
    def native_wait(mapper,connection,target):await_only(blocked())
    task=None
    try:
     s.add(_row(app,'outer-valid',1));await s.flush()
     tx=await s.begin_nested() if nested else None
     if nested:s.add(_row(app,'inner-valid',2));await s.flush()
     if protected:
      app.provider.unwrap_async=blocked;app.rings[app.tenant]=Keyring(healthy.policy,{app.provider.provider_id:app.provider})
     else:event.listen(app.Customer,'before_insert',native_wait)
     s.add(_row(app,'never-written',3));task=asyncio.create_task(s.flush())
     await asyncio.wait_for(entered.wait(),5);task.cancel()
     with pytest.raises(asyncio.CancelledError):await task
     active=s.is_active
     app.provider.unwrap_async=original;app.rings[app.tenant]=healthy
     if not protected:event.remove(app.Customer,'before_insert',native_wait)
     s.expunge_all()
     try:await (tx.commit() if tx is not None else s.commit());outcome='COMMITTED'
     except Exception as exc:
      outcome=type(exc).__name__;await (tx.rollback() if tx is not None else s.rollback())
     if nested:await s.commit()
     stored=list(await s.scalars(select(app.Customer.name).order_by(app.Customer.rank)))
     assert calls==[True]
     return active,outcome,stored
    finally:
     if task is not None and not task.done():task.cancel()
     app.provider.unwrap_async=original;app.rings[app.tenant]=healthy
     if event.contains(app.Customer,'before_insert',native_wait):event.remove(app.Customer,'before_insert',native_wait)
     await s.close();assert engine.sync_engine.pool.checkedout()==0;await engine.dispose()
   observations.append(asyncio.run(scenario()))
 assert observations[0]==observations[1]==(False,'PendingRollbackError',['outer-valid'] if nested else [])

@pytest.mark.parametrize('mode',['sync','async'])
def test_failed_invalidation_closes_dbapi_adapter_without_leaking_details(mode,monkeypatch):
 with search_application(True,attach_now=mode=='sync') as app:
  async def scenario():
   engine=None
   if mode=='async':engine,sessions=await _async_factory(app);sync_engine=engine.sync_engine
   else:sessions=app.sessions;sync_engine=app.engine
   s=sessions(tenant_id=app.tenant)
   try:
    s.add(_row(app,'outer',1));await maybe(s.flush())
    connection=(await s.connection()).sync_connection if mode=='async' else s.connection()
    handle=connection.connection.dbapi_connection
    original_rollback=sync_engine.dialect.do_rollback;original_invalidate=connection.invalidate
    def fail(*args,**kwargs):raise RuntimeError('PRIVATE_ROLLBACK_OR_INVALIDATION')
    monkeypatch.setattr(sync_engine.dialect,'do_rollback',fail);monkeypatch.setattr(connection,'invalidate',fail)
    s.add(_row(app,'invalid\x00text',2))
    try:
     with pytest.raises(Exception) as caught:await maybe(s.flush())
    finally:
     monkeypatch.setattr(sync_engine.dialect,'do_rollback',original_rollback);monkeypatch.setattr(connection,'invalidate',original_invalidate)
    assert handle.closed
    import traceback
    assert 'PRIVATE_ROLLBACK_OR_INVALIDATION' not in ''.join(traceback.format_exception(caught.value))
    connection.invalidate() # Lab bookkeeping after the deliberate invalidate fault is removed.
    with app.owner_engine.connect() as c:assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".customer').scalar_one()==0
   finally:
    await maybe(s.close())
    if engine is not None:await engine.dispose()
  asyncio.run(scenario())

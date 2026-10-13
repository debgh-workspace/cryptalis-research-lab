"""Native SAVEPOINT rollback/release behavior on a protected ORM session."""
from uuid import uuid4
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from test_sqlalchemy_adapter import TENANT, app, db, factory, runtime_access

@pytest.mark.parametrize('protected', [False, True], ids=['native','attached'])
@pytest.mark.parametrize('outcome', ['release','rollback','constraint'])
def test_savepoint_preserves_outer_transaction(app, protected, outcome):
    sessions=factory(app,protected)
    def row(rank,name):
        return app.Customer(id=uuid4(),tenant_id=TENANT,name=name,note='private',secret='',rank=rank)
    with sessions(tenant_id=TENANT) as session:
        with session.begin():
            session.add(row(1,'outer'))
            session.flush()
            if outcome=='constraint':
                with pytest.raises(IntegrityError) as err:
                    with session.begin_nested():
                        session.add(row(2,'outer'))
                        session.flush()
                assert err.value.orig.sqlstate=='23505'
            else:
                nested=session.begin_nested()
                session.add(row(2,'inner'))
                session.flush()
                if outcome=='release': nested.commit()
                else: nested.rollback()
            session.add(row(3,'after'))
        assert not session.in_transaction()
    with sessions(tenant_id=TENANT) as session:
        result=[tuple(r) for r in session.execute(select(app.Customer.rank,app.Customer.note).order_by(app.Customer.rank))]
        assert result==([(1,'private'),(2,'private'),(3,'private')] if outcome=='release' else [(1,'private'),(3,'private')])

@pytest.mark.parametrize('protected',[False,True],ids=['native','attached'])
@pytest.mark.parametrize('mode',['context','handle','close','outer-rollback'])
def test_multilevel_savepoint_values_and_expiration(app,protected,mode):
    from sqlalchemy import inspect
    sessions=factory(app,protected)
    def row(rank,name):return app.Customer(id=uuid4(),tenant_id=TENANT,name=name,note='é 雪',secret='',rank=rank)
    with sessions(tenant_id=TENANT) as s:
        s.autoflush=False
        s.expire_on_commit=False
        with s.begin():
            original=row(1,'outer');s.add(original)
            nested=s.begin_nested() # Native unconditional pre-savepoint flush.
            assert inspect(original).persistent
            original.note='first nested edit';s.flush()
            if mode=='context':
                with s.begin_nested():s.add(row(2,'second'));s.flush()
            else:
                inner=s.begin_nested();s.add(row(2,'second'));s.flush()
                inner.commit() if mode=='handle' else inner.close()
            nested.rollback()
            assert inspect(original).expired
            assert original.note=='é 雪'
            s.add(row(3,'after'))
            if mode=='outer-rollback':s.rollback()
    with sessions(tenant_id=TENANT) as s:
        result=[tuple(r) for r in s.execute(select(app.Customer.rank,app.Customer.note).order_by(app.Customer.rank))]
        assert result==([] if mode=='outer-rollback' else [(1,'é 雪'),(3,'é 雪')])

@pytest.mark.parametrize('clause',['savepoint','release','rollback','raw','driver','direct-native'])
def test_caller_forged_savepoint_control_never_reaches_cursor(app,clause,monkeypatch):
    import psycopg
    raw_calls=[]
    original=psycopg.Cursor.execute
    def observed(cursor,*args,**kwargs):
        raw_calls.append("raw cursor")
        return original(cursor,*args,**kwargs)
    from sqlalchemy import event,text
    from sqlalchemy.sql.expression import SavepointClause,ReleaseSavepointClause,RollbackToSavepointClause
    from cryptalis.sqlalchemy import UnsupportedProtectedOperation
    sessions=factory(app,True)
    with sessions(tenant_id=TENANT) as s:
        with s.begin():
            with s.begin_nested():
                s.execute(select(app.Customer.rank)).all()
                c=s.connection();seen=[]
                def before(*args):seen.append('cursor')
                event.listen(c,'before_cursor_execute',before)
                try:
                    with monkeypatch.context() as patch:
                        patch.setattr(psycopg.Cursor,"execute",observed)
                        with pytest.raises(UnsupportedProtectedOperation):
                            if clause=='raw':c.execute(text('SAVEPOINT forged'))
                            elif clause=='driver':c.exec_driver_sql('SAVEPOINT forged')
                            elif clause=='direct-native':c.begin_nested()
                            else:
                                cls={'savepoint':SavepointClause,'release':ReleaseSavepointClause,'rollback':RollbackToSavepointClause}[clause]
                                c.execute(cls('sa_savepoint_1'))
                    # exec_driver_sql passes before_cursor_execute before the
                    # existing dialect guard, but cannot reach the raw cursor.
                    if clause!='driver':assert seen==[]
                    assert raw_calls==[]
                finally:event.remove(c,'before_cursor_execute',before)
                assert s.execute(select(app.Customer.rank)).all()==[]

@pytest.mark.parametrize('protected',[False,True],ids=['native','attached'])
@pytest.mark.parametrize('outcome',['release','rollback','constraint'])
def test_async_savepoints_preserve_native_continuation(app,runtime_access,protected,outcome):
    import asyncio,os,psycopg
    from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
    from cryptalis.sqlalchemy import attach
    if protected:app.switch()
    async def scenario():
        engine=create_async_engine('postgresql+psycopg://',hide_parameters=True,async_creator=lambda:psycopg.AsyncConnection.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
        try:
            if protected:sessions=await attach(app.mapping,engine,lock=app.plan.lock_bytes,keys=app.rings.__getitem__)
            else:
                native=async_sessionmaker(engine);sessions=lambda *,tenant_id,**kw:native(**kw)
            def row(rank,name):return app.Customer(id=uuid4(),tenant_id=TENANT,name=name,note=None if rank==1 else '雪',secret='',rank=rank)
            async with sessions(tenant_id=TENANT) as s:
                async with s.begin():
                    s.add(row(1,'outer'));await s.flush()
                    if outcome=='constraint':
                        with pytest.raises(IntegrityError) as caught:
                            async with s.begin_nested():s.add(row(2,'outer'));await s.flush()
                        assert caught.value.orig.sqlstate=='23505'
                    else:
                        tx=await s.begin_nested();s.add(row(2,'inner'));await s.flush()
                        if outcome=='release':await tx.commit()
                        else:await tx.rollback()
                    s.add(row(3,'after'))
            async with sessions(tenant_id=TENANT) as s:
                values=[tuple(r) for r in await s.execute(select(app.Customer.rank,app.Customer.note).order_by(app.Customer.rank))]
                assert values==([(1,None),(2,'雪'),(3,'雪')] if outcome=='release' else [(1,None),(3,'雪')])
            assert engine.sync_engine.pool.checkedout()==0
        finally:await engine.dispose()
    asyncio.run(scenario())

@pytest.mark.parametrize('attempt',['different-clause','different-connection'])
def test_control_permission_cannot_be_reused_by_reentrant_callback(app,attempt,monkeypatch):
    import psycopg
    from sqlalchemy import event
    from sqlalchemy.sql.expression import SavepointClause
    from cryptalis.sqlalchemy import UnsupportedProtectedOperation
    state={'armed':False,'other':None,'checked':False}
    def earlier_listener(connection,statement,multiparams,params,options):
        if not state['armed'] or not isinstance(statement,SavepointClause):return
        state['armed']=False
        calls=[];native=psycopg.Cursor.execute
        def observe(cursor,*args,**kwargs):
            calls.append('raw control SQL');return native(cursor,*args,**kwargs)
        target=connection if attempt=='different-clause' else state['other']
        forged=SavepointClause('forged') if attempt=='different-clause' else statement
        with monkeypatch.context() as patch:
            patch.setattr(psycopg.Cursor,'execute',observe)
            with pytest.raises(UnsupportedProtectedOperation):target.execute(forged)
        assert calls==[]
        state['checked']=True
    # Install before attachment so this callback precedes guard admission.
    event.listen(app.engine,'before_execute',earlier_listener)
    try:
        sessions=factory(app,True)
        with sessions(tenant_id=TENANT) as first,sessions(tenant_id=TENANT) as second:
            first.execute(select(app.Customer.rank)).all()
            second.execute(select(app.Customer.rank)).all()
            state['other']=second.connection();state['armed']=True
            with first.begin_nested():first.execute(select(app.Customer.rank)).all()
            assert state['checked']
            assert first.execute(select(app.Customer.rank)).all()==[]
    finally:event.remove(app.engine,'before_execute',earlier_listener)

@pytest.mark.parametrize('control',['release','rollback'])
def test_failed_savepoint_control_quarantines_the_whole_unit(app,control):
    import psycopg
    from sqlalchemy import event
    from sqlalchemy.exc import DBAPIError,PendingRollbackError,InvalidRequestError
    sessions=factory(app,True)
    with sessions(tenant_id=TENANT) as s:
        s.add(app.Customer(id=uuid4(),tenant_id=TENANT,name='outer',note='private',secret='',rank=1));s.flush()
        tx=s.begin_nested()
        s.add(app.Customer(id=uuid4(),tenant_id=TENANT,name='inner',note='private',secret='',rank=2));s.flush()
        prefix='RELEASE SAVEPOINT' if control=='release' else 'ROLLBACK TO SAVEPOINT'
        def fail(connection,cursor,statement,params,context,many):
            if statement.startswith(prefix):raise psycopg.OperationalError('synthetic control transport failure')
        event.listen(app.engine,'before_cursor_execute',fail)
        try:
            with pytest.raises((DBAPIError,psycopg.Error)):
                tx.commit() if control=='release' else tx.rollback()
        finally:event.remove(app.engine,'before_cursor_execute',fail)
        # A failed cleanup must not let a later commit publish the inner work.
        with pytest.raises((PendingRollbackError,InvalidRequestError)):
            s.commit()
        s.rollback()
    with sessions(tenant_id=TENANT) as check:
        assert check.execute(select(app.Customer.rank)).all()==[]

@pytest.mark.parametrize('control',['release','rollback'])
def test_real_backend_termination_during_control_discards_uncommitted_work(app,control):
    import os,psycopg
    from sqlalchemy import event
    from sqlalchemy.exc import DBAPIError,PendingRollbackError,InvalidRequestError
    sessions=factory(app,True)
    with sessions(tenant_id=TENANT) as s:
        s.add(app.Customer(id=uuid4(),tenant_id=TENANT,name='outer-kill',note='private',secret='',rank=1));s.flush()
        tx=s.begin_nested()
        s.add(app.Customer(id=uuid4(),tenant_id=TENANT,name='inner-kill',note='private',secret='',rank=2));s.flush()
        pid=s.connection().connection.dbapi_connection.info.backend_pid
        prefix='RELEASE SAVEPOINT' if control=='release' else 'ROLLBACK TO SAVEPOINT'
        killed=[]
        def terminate(connection,cursor,statement,params,context,many):
            if statement.startswith(prefix):
                with psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL']) as observer:
                    assert observer.execute('SELECT pg_terminate_backend(%s)',(pid,)).fetchone()==(True,)
                killed.append(pid)
        event.listen(app.engine,'before_cursor_execute',terminate)
        try:
            with pytest.raises((DBAPIError,psycopg.Error)):
                tx.commit() if control=='release' else tx.rollback()
        finally:event.remove(app.engine,'before_cursor_execute',terminate)
        assert killed==[pid]
        with pytest.raises((PendingRollbackError,InvalidRequestError)):s.commit()
        s.rollback()
    with sessions(tenant_id=TENANT) as check:
        assert check.execute(select(app.Customer.rank)).all()==[]
    assert app.engine.pool.checkedout()==0

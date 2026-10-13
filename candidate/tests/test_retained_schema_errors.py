"""Real stale-factory failure and native-error controls; no schema auto-repair."""
import asyncio,os,traceback,pickle
from uuid import UUID
import psycopg,pytest
from sqlalchemy import select,event
from sqlalchemy.exc import DBAPIError,IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine
from cryptalis.sqlalchemy import attach,PolicyMismatch
from test_migration import application,run,publish,keys,TENANT
from test_retained_public_metadata import reverse
from test_deprotection import execute


def assert_safe(error,app):
    assert isinstance(error,PolicyMismatch),type(error).__name__
    assert error.code=='ProtectedSchemaMismatch'
    assert 'Roll back' in str(error) and 'attachment' in str(error)
    assert app.schema not in str(error) and '_cryptalis_' not in str(error)
    rendered=''.join(traceback.format_exception(error))
    assert app.schema not in rendered
    assert error.effects=='transaction_requires_rollback'
    restored=pickle.loads(pickle.dumps(error))  # Trusted local round trip only.
    assert (restored.code,restored.operation_id,restored.effects)==(error.code,error.operation_id,error.effects)
    assert restored.__cause__ is None and restored.__context__ is None


@pytest.mark.parametrize('asynchronous',[False,True])
@pytest.mark.parametrize('predicate_only',[False,True])
def test_stale_retained_factory_reports_safe_schema_mismatch(asynchronous,predicate_only):
    with application() as app:
        with app.owner.connect() as c:
            expected=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all()
        run(app);publish(app)
        statement=(select(app.Customer.label).where(app.Customer.name=='exact') if predicate_only else select(app.Customer.name)).order_by(app.Customer.id)
        expected_query=[r[3] for r in expected if r[2]=='exact'] if predicate_only else [r[2] for r in expected]
        public=select(app.Customer.label).order_by(app.Customer.id)
        if not asynchronous:
            factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
            with factory(tenant_id=TENANT) as s:assert list(s.scalars(statement))==expected_query
            d,p,pin,consent=reverse(app);execute(app,d,p,pin,consent)
            with factory(tenant_id=TENANT) as s:
                error=None
                try:list(s.scalars(statement))
                except Exception as caught:error=caught
                assert_safe(error,app)
                s.rollback()
                assert list(s.scalars(public))==[r[3] for r in expected]
        else:
            async def check():
                engine=create_async_engine('postgresql+psycopg://',hide_parameters=True,async_creator=lambda:psycopg.AsyncConnection.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
                try:
                    factory=await attach(app.mapping,engine,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
                    async with factory(tenant_id=TENANT) as s:assert list((await s.scalars(statement)))==expected_query
                    d,p,pin,consent=reverse(app);execute(app,d,p,pin,consent)
                    async with factory(tenant_id=TENANT) as s:
                        error=None
                        try:list(await s.scalars(statement))
                        except Exception as caught:error=caught
                        assert_safe(error,app)
                        await s.rollback()
                        assert list(await s.scalars(public))==[r[3] for r in expected]
                finally:await engine.dispose()
            asyncio.run(check())
        with app.owner.connect() as c:
            assert c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all()==expected


def test_unprotected_missing_column_remains_native_error():
    with application() as app:
        run(app);publish(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with app.owner.begin() as c:c.exec_driver_sql(f'ALTER TABLE "{app.schema}".customer RENAME COLUMN label TO native_label')
        with factory(tenant_id=TENANT) as s:
            with pytest.raises(DBAPIError) as error:s.scalars(select(app.Customer.label)).all()
            assert error.value.orig.sqlstate=='42703'
            s.rollback()


def test_protected_unique_violation_remains_native_error():
    with application() as app:
        run(app);publish(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with factory(tenant_id=TENANT) as s:
            s.add(app.Customer(id=UUID(int=999),tenant_id=TENANT,name='exact',label='duplicate control'))
            with pytest.raises(IntegrityError) as error:s.commit()
            assert error.value.orig.sqlstate=='23505'
            s.rollback()


@pytest.mark.parametrize('before_attach',[False,True])
def test_explicit_host_error_policy_is_not_overridden(before_attach):
    class HostPolicyError(ValueError):pass
    def host(context):
        if getattr(context.original_exception,'sqlstate',None)=='42703':
            return HostPolicyError('host schema policy')
    with application() as app:
        run(app);publish(app)
        if before_attach:event.listen(app.runtime,'handle_error',host,retval=True)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        if not before_attach:event.listen(app.runtime,'handle_error',host,retval=True)
        d,p,pin,consent=reverse(app);execute(app,d,p,pin,consent)
        with factory(tenant_id=TENANT) as s:
            with pytest.raises(HostPolicyError,match='host schema policy'):
                s.scalars(select(app.Customer.name)).all()
            s.rollback()


def test_other_protected_select_database_failure_remains_native():
    from sqlalchemy import literal
    with application() as app:
        run(app);publish(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with factory(tenant_id=TENANT) as s:
            with pytest.raises(DBAPIError) as error:
                s.execute(select(app.Customer.name,literal(1)/literal(0))).all()
            assert error.value.orig.sqlstate=='22012'
            s.rollback()
            assert list(s.scalars(select(app.Customer.name).order_by(app.Customer.id)))==[v for _,(_,v) in sorted(app.source.items())]

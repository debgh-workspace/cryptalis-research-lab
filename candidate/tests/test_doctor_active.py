"""Active doctor uses existing read-only deployment/role contracts, never row verification."""
import json
from dataclasses import replace
import pytest
from sqlalchemy import event
from test_migration import application, run
from cryptalis.doctor import doctor


def activate(app):
    run(app)
    app.pin=replace(app.pin,phase='ACTIVATING')
    run(app,until='ACTIVE')
    app.pin=replace(app.pin,phase='ACTIVE')


def inspect_active(app,**kwargs):
    declaration=json.dumps(app.plan.document['lock']['declaration']).encode()
    return doctor(declaration,phase='active',mapping=app.mapping,engine=kwargs.pop('engine',app.runtime),
                  deployment=(app.plan,kwargs.pop('pin',app.pin)),**kwargs)


def test_active_doctor_checks_deployment_and_runtime_role_without_rows_or_keys():
    with application() as app:
        activate(app)
        statements=[]
        def capture(conn,cursor,statement,params,context,many):statements.append(statement)
        event.listen(app.runtime,'before_cursor_execute',capture)
        try: report=inspect_active(app)
        finally:event.remove(app.runtime,'before_cursor_execute',capture)
        assert report['checks']['deployment']['status']=='CHECKED'
        assert report['checks']['roles']['status']=='CHECKED'
        assert report['checks']['ciphertext']['status']=='NOT_INSPECTED'
        assert report['checks']['provider']['status']=='NOT_INSPECTED'
        assert report['checks']['native_admission']['status']=='NOT_INSPECTED'
        assert report['ready'] is False and report['complete'] is False
        assert not any(f'"{app.schema}"."customer"' in s for s in statements)


def test_active_doctor_refuses_owner_engine():
    with application() as app:
        activate(app)
        report=inspect_active(app,engine=app.owner)
        assert report['checks']['deployment']['status']=='REJECTED'
        assert report['checks']['deployment']['code']=='attachment_requires_planned_runtime_role'
        assert report['checks']['roles']['status']=='NOT_INSPECTED'


def test_active_doctor_refuses_stale_external_pin():
    with application() as app:
        activate(app)
        report=inspect_active(app,pin=replace(app.pin,phase='PREPARED'))
        assert report['checks']['deployment']['status']=='REJECTED'
        assert report['checks']['roles']['status']=='NOT_INSPECTED'

@pytest.mark.parametrize('autocommit',[False,True])
def test_active_doctor_is_enforced_read_only(autocommit):
    with application() as app:
        activate(app)
        def inject(conn,cursor,statement,params,context,many):
            if 'pg_catalog.pg_class' in statement:
                cursor.execute(f'DELETE FROM "{app.schema}".customer WHERE false')
        event.listen(app.runtime,'before_cursor_execute',inject)
        try:
            selected=app.runtime.execution_options(isolation_level='AUTOCOMMIT') if autocommit else app.runtime
            report=inspect_active(app,engine=selected)
        finally:event.remove(app.runtime,'before_cursor_execute',inject)
        assert report['checks']['deployment']['status']=='UNAVAILABLE'
        assert report['checks']['deployment']['sqlstate']=='25006'
        assert report['checks']['roles']['status']=='NOT_INSPECTED'


def test_active_doctor_refuses_schema_drift_without_repair():
    with application() as app:
        activate(app)
        with app.owner.begin() as c:c.exec_driver_sql(f'ALTER TABLE "{app.schema}".customer ADD COLUMN external_change text')
        report=inspect_active(app)
        assert report['checks']['deployment']['status']=='REJECTED'
        assert report['checks']['deployment']['code']=='active_schema_mismatch'
        with app.owner.connect() as c:
            assert c.exec_driver_sql('SELECT count(*) FROM information_schema.columns WHERE table_schema=%s AND column_name=%s',(app.schema,'external_change')).scalar_one()==1


def test_active_doctor_requires_matching_manifest_before_database_inspection():
    with application() as app:
        activate(app)
        doc=app.plan.document['lock']['declaration'];doc['models'][0]['model']='DifferentCustomer'
        statements=[]
        def capture(*args):statements.append(True)
        event.listen(app.runtime,'before_cursor_execute',capture)
        try:report=doctor(json.dumps(doc).encode(),phase='active',engine=app.runtime,deployment=(app.plan,app.pin))
        finally:event.remove(app.runtime,'before_cursor_execute',capture)
        assert report['checks']['deployment']['code']=='deployment_declaration_mismatch'
        assert statements==[]


def test_active_doctor_missing_inputs_remain_unknown():
    from test_protection_compiler import declaration
    report=doctor(json.dumps(declaration()).encode(),phase='active')
    assert report['checks']['deployment']['status']=='UNAVAILABLE'
    assert report['checks']['roles']['status']=='NOT_INSPECTED'


def test_active_doctor_malformed_inner_plan_is_rejected_without_raw_error():
    with application() as app:
        activate(app)
        document=app.plan.document
        document['lock']['models']=None
        malformed=replace(app.plan,artifact=app.m._canonical(document))
        pin=replace(app.pin,plan_digest=malformed.digest)
        declaration=json.dumps(app.plan.document['lock']['declaration']).encode()
        report=doctor(declaration,phase='active',engine=app.runtime,deployment=(malformed,pin))
        assert report['checks']['deployment']['status']=='REJECTED'
        assert report['checks']['deployment']['code']=='invalid_deployment_state'
        assert report['checks']['roles']['status']=='NOT_INSPECTED'

"""Independent observation controls for snapshot and payload-only access."""
import json
import pytest
from sqlalchemy import event
from sqlalchemy.exc import DBAPIError
from test_migration import application, keys
from test_doctor_active import activate
from test_doctor_ciphertext import inspect_frames, snapshot
from cryptalis.doctor import doctor


def test_ciphertext_audit_keeps_snapshot_across_committed_writer():
    with application() as app:
        activate(app);calls=[]
        field=app.plan.document['lock']['models'][0]['fields'][0]
        def interleave(tenant):
            if not calls:
                with app.owner.begin() as c:
                    c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{field["payload_column"]}"=NULL')
                calls.append(True)
            return keys(tenant)
        report=inspect_frames(app,keys=interleave)['checks']['ciphertext']
        assert calls==[True]
        assert report['status']=='CHECKED'
        assert report['rows_observed']==7 and report['nonnull_cells_authenticated']==6
        assert report['null_cells_observed']==1
        later=inspect_frames(app)['checks']['ciphertext']
        assert later['status']=='CHECKED' and later['nonnull_cells_authenticated']==0
        assert later['null_cells_observed']==7


def test_audit_needs_no_original_source_column_select():
    with application() as app:
        activate(app)
        field=app.plan.document['lock']['models'][0]['fields'][0]
        with app.owner.begin() as c:
            c.exec_driver_sql(f'REVOKE SELECT ON "{app.schema}".customer FROM "{app.role}"')
            c.exec_driver_sql(f'GRANT SELECT(id,tenant_id,"{field["payload_column"]}") ON "{app.schema}".customer TO "{app.role}"')
        with app.runtime.connect() as c:
            with pytest.raises(DBAPIError) as failure:
                c.exec_driver_sql(f'SELECT name FROM "{app.schema}".customer')
            assert failure.value.orig.sqlstate=='42501'
        audit=inspect_frames(app)['checks']['ciphertext']
        assert audit['status']=='CHECKED' and audit['nonnull_cells_authenticated']==6


@pytest.mark.parametrize('autocommit',[False,True])
def test_audit_payload_read_is_enforced_read_only(autocommit):
    with application() as app:
        activate(app);before=snapshot(app);injected=[]
        field=app.plan.document['lock']['models'][0]['fields'][0]
        def inject(conn,cursor,statement,params,context,many):
            if field['payload_column'] in statement and f'"{app.schema}"."customer"' in statement:
                injected.append(True)
                try: cursor.execute(f'DELETE FROM "{app.schema}".customer WHERE false')
                except Exception as failure:
                    injected.append(getattr(failure,'sqlstate',None))
                    raise
        event.listen(app.runtime,'before_cursor_execute',inject)
        try:
            selected=app.runtime.execution_options(isolation_level='AUTOCOMMIT') if autocommit else app.runtime
            report=doctor(json.dumps(app.plan.document['lock']['declaration']).encode(),phase='active',
                          engine=selected,deployment=(app.plan,app.pin),audit_ciphertext=True,keys=keys)
        finally:event.remove(app.runtime,'before_cursor_execute',inject)
        assert injected==[True,'25006']
        assert report['checks']['ciphertext']['status']=='UNAVAILABLE'
        assert snapshot(app)==before


def test_row_budget_remains_global_at_table_boundary():
    from test_migration_multitable import multiple_tables
    with multiple_tables() as app:
        activate(app)
        audit=inspect_frames(app,audit_row_limit=len(app.source))['checks']['ciphertext']
        assert audit['status']=='PARTIAL' and audit['rows_observed']==len(app.source)


def test_empty_audit_never_resolves_keys():
    with application(rows=0) as app:
        activate(app);calls=[]
        def resolver(tenant):calls.append(True);return keys(tenant)
        audit=inspect_frames(app,keys=resolver)['checks']['ciphertext']
        assert audit['status']=='CHECKED' and audit['rows_observed']==0
        assert audit['nonnull_cells_authenticated']==0 and calls==[]

"""Read-only frame observation cannot certify lifecycle, membership or freshness."""
import json
from test_migration import application, keys, independent_open
from test_doctor_active import activate
from cryptalis.doctor import doctor


def inspect_frames(app,**kw):
    raw=json.dumps(app.plan.document['lock']['declaration']).encode()
    return doctor(raw,phase='active',engine=app.runtime,deployment=(app.plan,app.pin),
                  audit_ciphertext=True,keys=kw.pop('keys',keys),**kw)


def snapshot(app):
    field=app.plan.document['lock']['models'][0]['fields'][0]
    with app.owner.connect() as c:
        rows=c.exec_driver_sql(f'SELECT id,tenant_id,"{field["payload_column"]}" FROM "{app.schema}".customer ORDER BY id').all()
        journal=c.exec_driver_sql(f'SELECT state::text FROM "{app.schema}"._cryptalis_journal').all()
    return rows,journal


def test_explicit_audit_authenticates_only_visible_nonnull_cells_without_changes():
    with application() as app:
        activate(app);before=snapshot(app)
        field=app.plan.document['lock']['models'][0]['fields'][0]
        assert {record:independent_open(frame,field['descriptor'],tenant,record) for record,tenant,frame in before[0]}=={r:v for r,(t,v) in app.source.items()}
        report=inspect_frames(app)
        audit=report['checks']['ciphertext']
        assert audit['status']=='CHECKED' and audit['rows_observed']==7
        assert audit['nonnull_cells_authenticated']==6 and audit['null_cells_observed']==1
        assert report['ready'] is False and report['complete'] is False
        assert report['checks']['provider']['status']=='NOT_INSPECTED'
        assert snapshot(app)==before


def test_audit_row_cutoff_is_partial():
    with application() as app:
        activate(app)
        audit=inspect_frames(app,audit_row_limit=1)['checks']['ciphertext']
        assert audit['status']=='PARTIAL' and audit['rows_observed']==1


def test_audit_byte_cutoff_precedes_key_resolution():
    with application() as app:
        activate(app);calls=[]
        def resolver(tenant):calls.append(True);return keys(tenant)
        audit=inspect_frames(app,keys=resolver,audit_byte_limit=1)['checks']['ciphertext']
        assert audit['status']=='PARTIAL' and audit['rows_observed']==0
        assert calls==[]


def test_corrupt_frame_is_rejected_without_echo_or_changes():
    with application(unique=False) as app:
        activate(app)
        field=app.plan.document['lock']['models'][0]['fields'][0]
        col='"'+field['payload_column']+'"'
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET {col}=pg_catalog.set_byte({col},pg_catalog.octet_length({col})-1,pg_catalog.mod(pg_catalog.get_byte({col},pg_catalog.octet_length({col})-1)+1,256)) WHERE {col} IS NOT NULL')
        before=snapshot(app)
        report=inspect_frames(app)
        assert report['checks']['ciphertext']['status']=='REJECTED'
        assert '雪😀' not in json.dumps(report,ensure_ascii=False)
        assert snapshot(app)==before


def test_key_resolver_error_is_unavailable_without_secret_text():
    with application() as app:
        activate(app)
        def broken(tenant):raise RuntimeError('PRIVATE_PROVIDER_CREDENTIAL_DETAIL')
        report=inspect_frames(app,keys=broken)
        assert report['checks']['ciphertext']['status']=='UNAVAILABLE'
        assert 'PRIVATE_PROVIDER_CREDENTIAL_DETAIL' not in json.dumps(report)


def test_wrong_tenant_key_policy_is_refused_before_unwrap(monkeypatch):
    from uuid import UUID
    from test_migration import PublicFixtureProvider
    with application() as app:
        activate(app);calls=[]
        def forbidden(*args):calls.append(True);raise AssertionError('wrong policy reached provider')
        monkeypatch.setattr(PublicFixtureProvider,'unwrap',forbidden)
        report=inspect_frames(app,keys=lambda tenant:keys(UUID(int=777)))
        assert report['checks']['ciphertext']['status']=='REJECTED'
        assert calls==[]


def test_no_opt_in_does_not_call_resolver():
    with application() as app:
        activate(app);calls=[]
        def resolver(tenant):calls.append(True);return keys(tenant)
        report=doctor(json.dumps(app.plan.document['lock']['declaration']).encode(),phase='active',
                      engine=app.runtime,deployment=(app.plan,app.pin),keys=resolver)
        assert report['checks']['ciphertext']['code']=='ciphertext_audit_opt_in_required'
        assert calls==[]


def test_omission_and_null_substitution_are_explicitly_not_proven():
    with application() as app:
        activate(app)
        field=app.plan.document['lock']['models'][0]['fields'][0]
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{field["payload_column"]}"=NULL')
            c.exec_driver_sql(f'DELETE FROM "{app.schema}".customer WHERE id=(SELECT min(id::text)::uuid FROM "{app.schema}".customer)')
        report=inspect_frames(app)
        audit=report['checks']['ciphertext']
        assert audit['status']=='CHECKED' and audit['rows_observed']==6
        assert audit['nonnull_cells_authenticated']==0 and audit['null_cells_observed']==6
        assert {'NULL substitution','absent rows','same-context replay or freshness'}<=set(audit['not_proven'])
        assert report['ready'] is False and report['complete'] is False


def test_multitable_multitenant_multifield_audit_matches_independent_oracle():
    from test_migration_multitable import multiple_tables, assert_independent_values
    with multiple_tables() as app:
        activate(app);assert_independent_values(app)
        audit=inspect_frames(app)['checks']['ciphertext']
        values=[v for _,v in app.source.values()]+[v for _,v in app.other_source.values()]+list(app.notes.values())
        assert audit['status']=='CHECKED'
        assert audit['rows_observed']==len(app.source)+len(app.other_source)
        assert audit['nonnull_cells_authenticated']==sum(v is not None for v in values)
        assert audit['null_cells_observed']==sum(v is None for v in values)


import pytest
@pytest.mark.parametrize('limits',[{'audit_row_limit':True},{'audit_row_limit':0},{'audit_row_limit':10001},
                                  {'audit_byte_limit':False},{'audit_byte_limit':0},{'audit_byte_limit':67108865}])
def test_invalid_audit_bounds_are_rejected(limits):
    from test_protection_compiler import declaration
    report=doctor(json.dumps(declaration()).encode(),phase='active',audit_ciphertext=True,keys=keys,**limits)
    assert report['checks']['ciphertext']['code']=='invalid_audit_bounds'
    assert report['checks']['deployment']['status']=='NOT_INSPECTED'


@pytest.mark.parametrize('delta',[-1,0])
def test_exact_cumulative_byte_boundary(delta):
    with application() as app:
        activate(app)
        rows,_=snapshot(app)
        expected_cost=sum(32+(0 if frame is None else 2*len(frame)+74) for _,_,frame in rows)
        audit=inspect_frames(app,audit_byte_limit=expected_cost+delta)['checks']['ciphertext']
        assert audit['status']==('CHECKED' if delta==0 else 'PARTIAL')
        assert audit['rows_observed']==(7 if delta==0 else 6)
        assert audit['estimated_byte_cost']<=expected_cost+delta


def test_exact_row_boundary_is_not_falsely_partial():
    with application() as app:
        activate(app)
        audit=inspect_frames(app,audit_row_limit=7)['checks']['ciphertext']
        assert audit['status']=='CHECKED' and audit['rows_observed']==7


def test_audit_requires_explicit_keys_before_database_access():
    from test_protection_compiler import declaration
    report=doctor(json.dumps(declaration()).encode(),phase='active',audit_ciphertext=True)
    assert report['checks']['ciphertext']['code']=='active_phase_and_explicit_keys_required'
    assert report['checks']['deployment']['status']=='NOT_INSPECTED'

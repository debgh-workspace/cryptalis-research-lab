"""Advisory findings must not contradict already admitted runtime profiles."""
import json
import pytest
from test_sqlalchemy_adapter import app, db

@pytest.mark.parametrize('spelling', [
    '12345678-1234-5678-1234-567812345678',
    '12345678123456781234567812345678',
    '{12345678-1234-5678-1234-567812345678}',
    '1234-5678-1234-5678-1234-5678-1234-5678',
])
def test_admitted_uuid_literal_is_not_falsely_reported_as_refused(app, spelling):
    source=f'from test_sqlalchemy_adapter import Customer\nsession.get(Customer, {spelling!r})\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/query.py':source})
    codes={f['code'] for f in report['findings']}
    assert 'uuid_text_record_bind_refused_if_attached' not in codes
    assert 'record_bind_requires_staging' in codes
    assert spelling not in json.dumps(report)
    assert report['staging_required'] is True


def test_delete_finding_discloses_private_profile_without_granting_it(app):
    source='from sqlalchemy import delete\nstatement=delete(None)\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/query.py':source})
    finding=next(f for f in report['findings'] if f['code']=='core_dml_refused_if_attached')
    assert 'default' in finding['reason'].lower()
    assert 'private' in finding['alternative'].lower()
    assert report['authority']=='ADVISORY_NOT_AUTHENTICATED'
    assert report['staging_required'] is True

@pytest.mark.parametrize('protected',[False,True])
@pytest.mark.parametrize('style',['canonical','compact','braces','four_digit_groups'])
def test_real_native_and_protected_uuid_text_point_read(app, protected, style):
    from uuid import UUID
    from test_sqlalchemy_adapter import factory, TENANT
    identity=UUID('12345678-1234-5678-1234-567812345678')
    spelling={'canonical':str(identity),'compact':identity.hex,'braces':'{'+str(identity)+'}',
              'four_digit_groups':'-'.join(identity.hex[i:i+4] for i in range(0,32,4))}[style]
    sessions=factory(app,protected)
    with sessions(tenant_id=TENANT) as session:
        session.add(app.Customer(id=identity,tenant_id=TENANT,name='oracle',note='café',secret='',rank=1))
        session.commit()
    with sessions(tenant_id=TENANT) as session:
        row=session.get(app.Customer,spelling)
        assert (row.id,row.note,row.secret)==(identity,'café','')

"""Doctor must disclose its inspection boundary and leave real native state unchanged."""
import json
import pytest
from sqlalchemy import event
from test_protection_compiler import app, engine, declaration, inventory, reviews, snapshot


def invoke(app, **kw):
    from cryptalis.doctor import doctor
    e,m,_,_=app
    return doctor(json.dumps(declaration()).encode(),mapping=m,engine=e,
                  writers=inventory(),search_reviews=reviews(),**kw)


def test_native_dynamic_doctor_is_partial_and_read_only(app):
    before=snapshot(app)
    report=invoke(app,sources={'app/query.py':b'raise RuntimeError("DO_NOT_EXECUTE_SECRET")'})
    assert report['checks']['native_admission']['status']=='CHECKED'
    assert report['checks']['compatibility']['status']=='PARTIAL'
    assert report['checks']['provider']['status']=='NOT_INSPECTED'
    assert report['checks']['ciphertext']['status']=='NOT_INSPECTED'
    assert report['ready'] is False and report['complete'] is False
    assert 'DO_NOT_EXECUTE_SECRET' not in json.dumps(report)
    assert snapshot(app)==before


def test_static_doctor_never_claims_schema_admission():
    from cryptalis.doctor import doctor
    report=doctor(json.dumps(declaration()).encode())
    assert report['checks']['manifest']['status']=='CHECKED'
    assert report['checks']['native_admission']['status']=='NOT_INSPECTED'
    assert report['ready'] is False


def test_invalid_manifest_is_sanitized():
    from cryptalis.doctor import doctor
    report=doctor(b'{"PRIVATE_SECRET":')
    assert report['checks']['manifest']['status']=='REJECTED'
    assert 'PRIVATE_SECRET' not in json.dumps(report)


@pytest.mark.parametrize('autocommit',[False,True])
def test_doctor_native_write_injection_is_database_rejected(app,autocommit):
    from cryptalis.doctor import doctor
    e,m,_,schema=app
    before=snapshot(app)
    def inject(conn,cursor,statement,parameters,context,many):
        if 'pg_catalog.pg_class' in statement:
            cursor.execute(f'DELETE FROM "{schema}".customer WHERE false')
    event.listen(e,'before_cursor_execute',inject)
    try:
        selected=e.execution_options(isolation_level='AUTOCOMMIT') if autocommit else e
        report=doctor(json.dumps(declaration()).encode(),mapping=m,engine=selected,
                      writers=inventory(),search_reviews=reviews())
    finally:
        event.remove(e,'before_cursor_execute',inject)
    assert report['checks']['native_admission']['status']=='UNAVAILABLE'
    assert report['checks']['native_admission']['sqlstate']=='25006'
    assert snapshot(app)==before


def test_doctor_cli_is_explicitly_incomplete(tmp_path,capsys):
    from cryptalis.cli import main
    path=tmp_path/'protection.json'
    path.write_text(json.dumps(declaration()))
    original=path.read_bytes()
    assert main(['doctor',str(path),'--json'])==3
    report=json.loads(capsys.readouterr().out)
    assert report['ready'] is False and report['checks']['native_admission']['status']=='NOT_INSPECTED'
    assert path.read_bytes()==original


def test_doctor_cli_invalid_json_is_rejected_without_echo(tmp_path,capsys):
    from cryptalis.cli import main
    path=tmp_path/'bad.json';path.write_bytes(b'PRIVATE_BAD_CONTENT')
    assert main(['doctor',str(path),'--json'])==2
    output=capsys.readouterr().out
    assert 'PRIVATE_BAD_CONTENT' not in output
    assert json.loads(output)['checks']['manifest']['status']=='REJECTED'


def test_doctor_incomplete_inputs_and_wrong_phase_are_not_silently_ignored(app):
    from cryptalis.doctor import doctor
    raw=json.dumps(declaration()).encode()
    report=doctor(raw,mapping=app[1])
    assert report['checks']['native_admission']['code']=='incomplete_dynamic_inputs'
    report=doctor(raw,phase='unknown_phase')
    assert report['checks']['native_admission']['code']=='unsupported_diagnostic_phase'


def test_doctor_rejected_host_inventory_is_not_schema_pass(app):
    from cryptalis.doctor import doctor
    report=doctor(json.dumps(declaration()).encode(),mapping=app[1],engine=app[0],
                  writers=inventory(complete=False),search_reviews=reviews())
    assert report['checks']['native_admission']['status']=='REJECTED'
    assert 'writer_inventory' in report['checks']['native_admission']['codes']
    assert report['checks']['compatibility']['status']=='NOT_INSPECTED'


def test_doctor_no_source_is_not_application_compatibility(app):
    report=invoke(app)
    assert report['checks']['compatibility']['status']=='NOT_INSPECTED'
    assert report['checks']['compatibility']['report']['staging_required'] is True


def test_doctor_preserves_connection_options_and_reads_no_application_rows(app):
    e,_,_,schema=app
    with e.connect() as c:
        before=(c.exec_driver_sql('SHOW search_path').scalar_one(),
                c.exec_driver_sql('SHOW transaction_read_only').scalar_one())
    statements=[]
    def record(conn,cursor,statement,parameters,context,many):statements.append(statement)
    event.listen(e,'before_cursor_execute',record)
    try:report=invoke(app)
    finally:event.remove(e,'before_cursor_execute',record)
    assert report['checks']['native_admission']['status']=='CHECKED'
    assert statements and not any(f'"{schema}".customer' in q for q in statements)
    assert not any('SELECT *' in q.upper() for q in statements)
    with e.connect() as c:
        after=(c.exec_driver_sql('SHOW search_path').scalar_one(),
               c.exec_driver_sql('SHOW transaction_read_only').scalar_one())
    assert after==before


def test_doctor_invalid_source_inventory_is_visibly_unavailable(app):
    report=invoke(app,sources={'../outside.py':b'pass'})
    assert report['checks']['native_admission']['status']=='CHECKED'
    assert report['checks']['compatibility']['status']=='UNAVAILABLE'
    assert report['checks']['compatibility']['code']=='invalid_source_label'


def test_doctor_native_schema_refusal_is_sanitized_and_read_only(app):
    e,_,_,schema=app
    with e.begin() as c:
        c.exec_driver_sql(f'ALTER TABLE "{schema}".customer ALTER COLUMN email SET DEFAULT \'PRIVATE_DEFAULT\'')
    before=snapshot(app)
    report=invoke(app)
    assert report['checks']['native_admission']['status']=='REJECTED'
    assert 'PRIVATE_DEFAULT' not in json.dumps(report)
    assert snapshot(app)==before


def test_doctor_non_sqlstate_exception_metadata_is_not_echoed(app,monkeypatch):
    import importlib
    module=importlib.import_module('cryptalis.doctor')
    from cryptalis.manifest.compiler import InspectionUnavailable
    def unavailable(*args,**kwargs):raise InspectionUnavailable('PRIVATE_NOT_SQLSTATE')
    monkeypatch.setattr(module,'compile_protection',unavailable)
    report=invoke(app)
    assert report['checks']['native_admission']['sqlstate'] is None
    assert 'PRIVATE_NOT_SQLSTATE' not in json.dumps(report)

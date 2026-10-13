"""Advisory source scanning must explain limits without executing application code."""
import hashlib
import json
import pytest
from sqlalchemy import event
from test_sqlalchemy_adapter import app, db
from test_migration import application


def codes(report):
    return {finding['code'] for finding in report['findings']}


def test_migration_plan_report_is_read_only_and_does_not_echo_source_values():
    with application() as state:
        statements=[]
        def capture(*args):statements.append(True)
        event.listen(state.owner,'before_cursor_execute',capture)
        event.listen(state.runtime,'before_cursor_execute',capture)
        original=state.plan.artifact
        source=b'from sqlalchemy import delete, text\nfrom test_migration import Customer\nstatement=delete(Customer)\nraw=text("NEVER_ECHO_THIS_PRIVATE_LITERAL")\nraise RuntimeError("SCANNING_MUST_NOT_EXECUTE_ME")\n'
        try:
            report=state.plan.compatibility_report(state.mapping,sources={'app/jobs.py':source})
        finally:
            event.remove(state.owner,'before_cursor_execute',capture)
            event.remove(state.runtime,'before_cursor_execute',capture)
        assert statements==[] and state.plan.artifact==original
        assert report['effects']=='NONE' and report['staging_required'] is True
        assert report['coverage']=='PARTIAL' and report['authority']=='ADVISORY_NOT_AUTHENTICATED'
        assert {'core_dml_refused_if_attached','raw_sql_refused_if_attached'}<=codes(report)
        assert 'NEVER_ECHO_THIS_PRIVATE_LITERAL' not in json.dumps(report)
        assert 'SCANNING_MUST_NOT_EXECUTE_ME' not in json.dumps(report)
        assert report['sources'][0]['sha256']==hashlib.sha256(source).hexdigest()


def test_no_sources_cannot_claim_application_compatibility(app):
    report=app.plan.compatibility_report(app.mapping)
    assert report['coverage']=='NOT_INSPECTED'
    assert report['staging_required'] is True
    assert 'query_sources_not_inspected' in codes(report)


def test_storage_only_null_checks_are_not_misreported_as_equality(app):
    source='from test_sqlalchemy_adapter import Customer\na=Customer.note == None\nb=Customer.note != None\nc=Customer.note.is_(None)\nd=Customer.note.is_not(None)\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/queries.py':source})
    assert 'storage_only_comparison_refused_if_attached' not in codes(report)
    assert report['staging_required'] is True


def test_storage_only_nonnull_comparison_has_practical_alternative(app):
    report=app.plan.compatibility_report(app.mapping,sources={'app/queries.py':'from test_sqlalchemy_adapter import Customer\nq=Customer.note == "value"\n'})
    finding=next(f for f in report['findings'] if f['code']=='storage_only_comparison_refused_if_attached')
    assert finding['line']==2 and finding['alternative']
    assert finding['status']=='SOURCE-INSPECTED'


def test_shadowed_import_is_uncertain_not_a_false_definite_refusal(app):
    source='from sqlalchemy import delete\ndef work(delete):\n    return delete(1)\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':source})
    assert 'core_dml_refused_if_attached' not in codes(report)
    assert 'shadowed_query_binding' in codes(report)


def test_parse_failure_is_disclosed_without_source_text(app):
    report=app.plan.compatibility_report(app.mapping,sources={'app/broken.py':'def bad(:\n "PRIVATE_LITERAL"'})
    assert 'query_source_unparseable' in codes(report)
    assert report['coverage']=='PARTIAL'
    assert 'PRIVATE_LITERAL' not in json.dumps(report)


@pytest.mark.parametrize('source,expected_line', [
    ('from sqlalchemy import delete as remove\nremove(None)\n', 2),
    ('import sqlalchemy as sa\nsa.delete(None)\n', 2),
])
def test_imported_aliases_are_identified(app, source, expected_line):
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':source})
    findings=[f for f in report['findings'] if f['code']=='core_dml_refused_if_attached']
    assert len(findings)==1 and findings[0]['line']==expected_line


def test_ordinary_instance_delete_is_not_a_core_dml_warning(app):
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':'def work(session, row):\n    session.delete(row)\n'})
    assert 'core_dml_refused_if_attached' not in codes(report)


def test_rebound_import_is_reported_as_unknown(app):
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':'from sqlalchemy import delete\ndelete=custom_callable\ndelete(1)\n'})
    assert 'core_dml_refused_if_attached' not in codes(report)
    assert 'rebound_query_binding' in codes(report)


def test_comprehension_scope_does_not_leak_into_outer_query(app):
    source='from sqlalchemy import delete\nx=[delete(1) for delete in callbacks]\ny=delete(None)\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':source})
    findings=[f for f in report['findings'] if f['code']=='core_dml_refused_if_attached']
    assert [f['line'] for f in findings]==[3]


def test_native_python_encoding_cookie_is_honored(app):
    source=b'# coding: latin-1\nfrom sqlalchemy import delete\n# caf\xe9\ndelete(None)\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':source})
    assert 'query_source_unparseable' not in codes(report)
    assert 'core_dml_refused_if_attached' in codes(report)


def test_default_argument_query_construction_is_inspected(app):
    source='from sqlalchemy import text\ndef work(query=text("PRIVATE_DEFAULT")):\n    pass\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/jobs.py':source})
    assert 'raw_sql_refused_if_attached' in codes(report)
    assert 'PRIVATE_DEFAULT' not in json.dumps(report)


@pytest.mark.parametrize('sources', [
    {'app/jobs.py': b'#'+b'x'*(1024*1024)},
    {f'app/file_{n}.py': b'pass' for n in range(257)},
    {'../outside.py': b'pass'},
    {'app/jobs.py': object()},
])
def test_source_limits_fail_loudly_and_safely(app, sources):
    from cryptalis.manifest.compatibility import CompatibilityInspectionUnavailable
    with pytest.raises(CompatibilityInspectionUnavailable) as caught:
        app.plan.compatibility_report(app.mapping,sources=sources)
    assert caught.value.effects=='NONE' and caught.value.code


def test_dynamic_and_literal_uuid_keys_have_distinct_findings(app):
    source='from test_sqlalchemy_adapter import Customer\nsession.get(Customer, "PRIVATE_UUID_TEXT")\nsession.get_one(Customer, token.sub)\n'
    report=app.plan.compatibility_report(app.mapping,sources={'app/deps.py':source})
    assert {'uuid_text_record_bind_refused_if_attached','record_bind_requires_staging'}<=codes(report)
    assert 'PRIVATE_UUID_TEXT' not in json.dumps(report)


def test_deep_ast_has_a_safe_typed_failure(app):
    from cryptalis.manifest.compatibility import CompatibilityInspectionUnavailable
    source='value='+ '+'.join('1' for _ in range(2000))
    with pytest.raises(CompatibilityInspectionUnavailable) as caught:
        app.plan.compatibility_report(app.mapping,sources={'app/deep.py':source})
    assert caught.value.code in ('ast_budget_exceeded','analysis_depth_exceeded')


@pytest.mark.parametrize('raw', [b'{', b'[]', b'{"schema":"cryptalis.lock/v1","models":[{}]}',
    b'{"schema":"cryptalis.lock/v1","models":[{"model":[],"schema":"s","table":"t","record":{},"fields":[]}]}'])
def test_malformed_plan_report_has_a_safe_typed_failure(app, raw):
    from dataclasses import replace
    from cryptalis.manifest.compatibility import CompatibilityInspectionUnavailable
    with pytest.raises(CompatibilityInspectionUnavailable) as caught:
        replace(app.plan, lock_bytes=raw).compatibility_report(app.mapping)
    assert caught.value.code=='invalid_compiled_lock'
    assert caught.value.effects=='NONE'


def test_same_named_model_with_different_table_is_not_silently_matched(app):
    from dataclasses import replace
    document=json.loads(app.plan.lock_bytes)
    document['models'][0]['table']='different_table'
    report=replace(app.plan,lock_bytes=json.dumps(document).encode()).compatibility_report(app.mapping)
    assert 'mapping_identity_mismatch' in codes(report)


@pytest.mark.parametrize('operator', ['eq', 'in_', 'not_in', 'empty_in'])
def test_storage_only_warning_matches_actual_pre_sql_refusal(app, operator):
    from sqlalchemy import select
    from test_sqlalchemy_adapter import factory, TENANT
    from cryptalis.sqlalchemy import UnsupportedProtectedOperation
    expression={'eq':'Customer.note == "x"','in_':'Customer.note.in_(["x"])',
                'not_in':'Customer.note.not_in(["x"])','empty_in':'Customer.note.in_([])'}[operator]
    report=app.plan.compatibility_report(app.mapping,sources={'app/query.py':
        'from test_sqlalchemy_adapter import Customer\nquery='+expression+'\n'})
    assert 'storage_only_comparison_refused_if_attached' in codes(report)
    sessions=factory(app,True)
    field=app.Customer.note
    clause={'eq':lambda:field=='x','in_':lambda:field.in_(['x']),
            'not_in':lambda:field.not_in(['x']),'empty_in':lambda:field.in_([])}[operator]()
    statements=[]
    def capture(*args):statements.append(True)
    event.listen(app.engine,'before_cursor_execute',capture)
    try:
        with sessions(tenant_id=TENANT) as session:
            with pytest.raises(UnsupportedProtectedOperation):
                session.scalars(select(app.Customer).where(clause)).all()
        assert statements==[]
    finally:
        event.remove(app.engine,'before_cursor_execute',capture)

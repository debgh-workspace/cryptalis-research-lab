"""Real report input/mapping/aggregation boundary, with no engine or compiled plan."""
import hashlib
import json
import unittest

from sqlalchemy import Column, MetaData, Table, Text, Uuid
from sqlalchemy.orm import registry
from cryptalis.manifest.compatibility import CompatibilityInspectionUnavailable, inspect_plan_compatibility


CODE = 'encrypted_nullsafe_comparison_refused_if_attached'
REASON = 'This encrypted NULL-safe comparison is not admitted through the attached factory.'
ALTERNATIVE = ('Review exact NULL-aware alternatives in staging; ordinary equality or inequality is not a general replacement. '
               'Never bypass the attached factory or use a plaintext fallback.')


def fixture(table_name='customer'):
    mapping = registry()
    customer = type('Customer', (), {'__module__': 'fixture.models'})
    table = Table(table_name, MetaData(schema='app_schema'),
                  Column('id', Uuid, primary_key=True), Column('tenant_id', Uuid, nullable=False),
                  Column('secret', Text(collation='C')), Column('note', Text(collation='C')))
    mapping.map_imperatively(customer, table)
    # Exactly the report's declared input shape. No compiler or catalog claims.
    document = {'schema': 'cryptalis.lock/v1', 'models': [{
        'model': 'Customer', 'schema': 'app_schema', 'table': 'customer',
        'record': {'column': 'id', 'codec': 'uuid16/v1'},
        'fields': [{'name': 'secret', 'queries': ['eq']}, {'name': 'note', 'queries': []}],
    }]}
    raw = json.dumps(document, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return mapping, customer, table, raw


class ReportIntegrationTests(unittest.TestCase):
    def test_real_mapping_aggregates_two_diagnostics_and_snapshot_metadata(self):
        mapping, customer, table, raw = fixture()
        try:
            original = raw
            sources = {
                'app/z_query.py': b"from fixture.models import Customer\nquery = Customer.note.is_not_distinct_from(None)\nraise RuntimeError('MUST_NOT_EXECUTE')\n",
                'app/a_query.py': b"from fixture.models import Customer\nquery = Customer.secret.is_distinct_from('PRIVATE_VALUE')\n",
            }
            report = inspect_plan_compatibility(raw, mapping, sources=sources)
            self.assertEqual(raw, original)
            self.assertEqual(customer.__table__, table)
            self.assertEqual(report['format'], 'cryptalis.compatibility-report/v1')
            self.assertEqual(report['effects'], 'NONE')
            self.assertEqual(report['authority'], 'ADVISORY_NOT_AUTHENTICATED')
            self.assertEqual(report['coverage'], 'PARTIAL')
            self.assertIs(report['staging_required'], True)
            self.assertEqual(report['lock_digest'], hashlib.sha256(original).hexdigest())
            self.assertEqual(report['models'], [{'model': 'Customer', 'schema': 'app_schema', 'table': 'customer',
                'record_codec': 'uuid16/v1', 'fields': [{'name': 'secret', 'queries': ['eq']}, {'name': 'note', 'queries': []}]}])
            self.assertEqual(report['sources'], [dict(path=p, sha256=hashlib.sha256(sources[p]).hexdigest(),
                bytes=len(sources[p]), input_kind='bytes') for p in ('app/a_query.py', 'app/z_query.py')])
            self.assertEqual(report['findings'], [dict(code=CODE, path=p, line=2, reason=REASON,
                alternative=ALTERNATIVE, certainty='CONDITIONAL_REFUSAL', status='SOURCE-INSPECTED')
                for p in ('app/a_query.py', 'app/z_query.py')])
            rendered = json.dumps(report)
            self.assertNotIn('PRIVATE_VALUE', rendered)
            self.assertNotIn('MUST_NOT_EXECUTE', rendered)
            self.assertIn('PRIVATE_VALUE', json.dumps({'exposed': 'PRIVATE_VALUE'}))
        finally:
            mapping.dispose()

    def test_actual_report_validation_rejects_invalid_mapping_and_lock_shape(self):
        mapping, _, _, raw = fixture()
        try:
            for supplied_raw, supplied_mapping, code in (
                (raw, object(), 'invalid_mapping'),
                (b'{"schema":"wrong","models":[]}', mapping, 'invalid_compiled_lock'),
                (b'{"schema":"cryptalis.lock/v1","models":[{"model":"Customer","schema":"app_schema","table":"customer","record":{"codec":"uuid16/v1"},"fields":[{"name":"secret","queries":[1]}]}]}', mapping, 'invalid_compiled_lock'),
            ):
                with self.subTest(code=code):
                    with self.assertRaises(CompatibilityInspectionUnavailable) as caught:
                        inspect_plan_compatibility(supplied_raw, supplied_mapping, sources={})
                    self.assertEqual(caught.exception.code, code)
                    self.assertEqual(caught.exception.effects, 'NONE')
                    self.assertEqual(caught.exception.stage, 'compatibility_source_inspection')
        finally:
            mapping.dispose()

    def test_real_table_identity_mismatch_stays_unresolved(self):
        mapping, _, _, raw = fixture(table_name='different_customer')
        try:
            report = inspect_plan_compatibility(raw, mapping, sources={'app/query.py':
                'from fixture.models import Customer\nq = Customer.secret.is_distinct_from(None)\n'})
            self.assertEqual([(f['code'], f['certainty'], f['path'], f['line']) for f in report['findings']],
                             [('mapping_identity_mismatch', 'UNRESOLVED', None, None)])
            self.assertEqual(report['coverage'], 'PARTIAL')
            self.assertIs(report['staging_required'], True)
        finally:
            mapping.dispose()

    def test_empty_and_unparseable_sources_do_not_become_clean_admission(self):
        mapping, _, _, raw = fixture()
        try:
            empty = inspect_plan_compatibility(raw, mapping)
            self.assertEqual(empty['coverage'], 'NOT_INSPECTED')
            self.assertEqual([f['code'] for f in empty['findings']], ['query_sources_not_inspected'])
            self.assertIs(empty['staging_required'], True)
            broken = inspect_plan_compatibility(raw, mapping, sources={'app/bad.py': 'def bad(:\n "PRIVATE_PARSE_VALUE"'})
            self.assertEqual(broken['coverage'], 'PARTIAL')
            self.assertEqual([(f['code'], f['certainty']) for f in broken['findings']], [('query_source_unparseable', 'UNRESOLVED')])
            self.assertNotIn('PRIVATE_PARSE_VALUE', json.dumps(broken))
            self.assertIs(broken['staging_required'], True)
        finally:
            mapping.dispose()


if __name__ == '__main__':
    unittest.main()

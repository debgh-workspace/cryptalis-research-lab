"""Measured rates round-trip without changing the strict manifest grammar."""
import json
import math

import pytest

from cryptalis.manifest.compiler import Writer, WriterInventory, SearchReview
from test_migration import application, keys, TABLE_ID, FIELD_ID, run, publish
from test_deprotection import api, plaintext_role
from cryptalis.migration import MigrationPlan, TransitionFailure
from cryptalis.manifest.parser import ManifestInvalid, decode_manifest_json


def protect_plan(app, kwargs):
    return app.m.plan(json.dumps(app.plan.document['lock']['declaration']).encode(), app.mapping, app.owner,
        writers=WriterInventory(True, (Writer(TABLE_ID, 'app', 'sqlalchemy', evidence='owned fixture'),)),
        search_reviews=(SearchReview(FIELD_ID, False, 'synthetic names'),),
        keys=keys, runtime_role=app.role, target_id=app.plan.target_id, **kwargs)


@pytest.mark.parametrize('rates', [(20.5, 10.25), (1000.0, 500.0)])
@pytest.mark.parametrize('direction', ['protect', 'reverse', 'reverse_fractional_source'])
def test_fractional_measured_rates_survive_read_only_plan_roundtrip(direction, rates):
    kwargs = dict(backfill_rows_per_second=rates[0], verify_rows_per_second=rates[1],
                  temporary_bytes_per_row=700, wal_bytes_per_row=2000)
    with application() as app:
        assert MigrationPlan(app.plan.artifact).artifact == app.plan.artifact
        if direction == 'reverse_fractional_source':
            app.plan = protect_plan(app, kwargs)
            from dataclasses import replace
            app.pin = replace(app.pin, operation_id=app.plan.operation_id, plan_digest=app.plan.digest)
        if direction != 'protect':
            run(app)
            publish(app)
        with app.owner.connect() as c:
            before = c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all()
            columns = c.exec_driver_sql('SELECT column_name FROM information_schema.columns WHERE table_schema=%s ORDER BY ordinal_position', (app.schema,)).all()
        if direction == 'protect':
            plan = protect_plan(app, kwargs)
        else:
            plan = api().plan(app.plan, app.owner, source_pin=app.pin, keys=keys,
                              plaintext_runtime_role=plaintext_role(), **kwargs)
        restored = type(plan)(plan.artifact)
        assert restored.artifact == plan.artifact
        assert restored.digest == plan.digest
        assert restored.document['estimates']['backfill_rows_per_second'] == rates[0]
        assert restored.document['estimates']['verify_rows_per_second'] == rates[1]
        assert restored.document['estimates']['writer_pause_seconds_estimate'] == math.ceil(len(app.source)/rates[0] + len(app.source)/rates[1])
        with app.owner.connect() as c:
            assert c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all() == before
            assert c.exec_driver_sql('SELECT column_name FROM information_schema.columns WHERE table_schema=%s ORDER BY ordinal_position', (app.schema,)).all() == columns


@pytest.mark.parametrize('location', ['row_count', 'policy_digest', 'unexpected_nested_rates'])
def test_float_admission_does_not_expand_beyond_measured_rate_paths(location):
    with application() as app:
        doc = app.plan.document
        if location == 'row_count':
            doc['estimates']['rows'] = 7.0
        elif location == 'policy_digest':
            tenant = next(iter(doc['key_policies']))
            assert isinstance(doc['key_policies'][tenant], str)
            doc['key_policies'][tenant] = 1.0
        else:
            doc['source_plan'] = {'estimates': {'backfill_rows_per_second': 20.5}}
        raw = json.dumps(doc, sort_keys=True, separators=(',', ':')).encode()
        with pytest.raises(TransitionFailure, match='invalid_plan'):
            MigrationPlan(raw)


@pytest.mark.parametrize('rate', [0.0, -1.5, float('inf'), -float('inf'), float('nan')])
def test_invalid_float_rate_is_rejected_by_artifact_reader(rate):
    with application() as app:
        doc = app.plan.document
        doc['estimates']['backfill_rows_per_second'] = rate
        raw = json.dumps(doc, sort_keys=True, separators=(',', ':')).encode()
        with pytest.raises(TransitionFailure, match='invalid_plan'):
            MigrationPlan(raw)


def test_manifest_decoder_stays_integer_only_even_at_rate_named_fields():
    raw = b'{"estimates":{"backfill_rows_per_second":20.5}}'
    with pytest.raises(ManifestInvalid):
        decode_manifest_json(raw)

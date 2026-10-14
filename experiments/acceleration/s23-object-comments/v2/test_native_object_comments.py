"""Four synthetic native-metadata oracles; no product admission change.

Run only through the unchanged fresh-role preflight and serialized lab wrapper.
A mismatch is an ordinary failure, never an accepted refusal or xfail.
"""
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
from uuid import UUID

PACKET = Path(__file__).resolve().parent
LAB = PACKET.parents[1]
SOURCE = LAB / 'candidate-s23-object-comments-oracle-20261014'
sys.path.insert(0, str(SOURCE / 'tests'))

import cryptalis
import pytest
import sqlalchemy
from psycopg import sql
from sqlalchemy.orm import sessionmaker

import test_migration as migration_helper
import test_deprotection as reverse_helper
import test_retained_public_metadata as metadata_helper
import test_transition_rate_estimates as plan_helper
from cryptalis.sqlalchemy import attach


CASES = ('standalone_index', 'unique_constraint',
         'constraint_backing_index', 'absent_comments')
COMMENT = 'Synthetic owner\'s "quoted" object comment: 雪😀'
EDITED = 'current synthetic value after protection 雪'
EDIT_ID = UUID(int=105)


def _assert_source_identity():
    manifest = json.loads((PACKET / 'BASELINE_S23_MANIFEST.json').read_text())
    for name, digest in manifest['source_sha256'].items():
        observed = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
        assert observed == digest, 'isolated S23 source/helper pin mismatch'
    assert Path(cryptalis.__file__).resolve() == SOURCE / 'src/cryptalis/__init__.py'
    for module in (migration_helper, reverse_helper, metadata_helper, plan_helper):
        assert Path(module.__file__).resolve() == SOURCE / 'tests' / (module.__name__ + '.py')
    assert (PACKET / 'conftest.py').read_bytes() == (SOURCE / 'tests/conftest.py').read_bytes()
    assert sqlalchemy.__version__ in ('2.1.3', '2.0.51')


def _execute_composed(connection, statement):
    connection.exec_driver_sql(statement.as_string(connection.connection.driver_connection))


def _configure_native_objects(app, case):
    """Only ordinary synthetic comments and an already admitted UNIQUE shape."""
    with app.owner.begin() as connection:
        if case != 'standalone_index':
            _execute_composed(connection, sql.SQL(
                'ALTER TABLE {} ADD CONSTRAINT {} UNIQUE USING INDEX {}'
            ).format(sql.Identifier(app.schema, 'customer'),
                     sql.Identifier('native_name'), sql.Identifier('native_name')))
        if case in ('standalone_index', 'constraint_backing_index'):
            statement = sql.SQL('COMMENT ON INDEX {} IS {}').format(
                sql.Identifier(app.schema, 'native_name'), sql.Literal(COMMENT))
            _execute_composed(connection, statement)
        elif case == 'unique_constraint':
            statement = sql.SQL('COMMENT ON CONSTRAINT {} ON {} IS {}').format(
                sql.Identifier('native_name'), sql.Identifier(app.schema, 'customer'),
                sql.Literal(COMMENT))
            _execute_composed(connection, statement)


def _native_metadata(app):
    """Independent catalog observations; do not call product schema inspectors."""
    with app.owner.connect() as connection:
        table_oid = connection.exec_driver_sql('''
            SELECT t.oid FROM pg_catalog.pg_class t
            JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
            WHERE n.nspname=%s AND t.relname='customer'
        ''', (app.schema,)).scalar_one()
        index = connection.exec_driver_sql('''
            SELECT i.indexrelid, i.indrelid, ix.relname,
                   i.indisunique, i.indisvalid, i.indisready,
                   i.indimmediate, i.indnullsnotdistinct,
                   pg_catalog.pg_get_indexdef(i.indexrelid),
                   pg_catalog.obj_description(i.indexrelid, 'pg_class')
            FROM pg_catalog.pg_index i
            JOIN pg_catalog.pg_class t ON t.oid=i.indrelid
            JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
            JOIN pg_catalog.pg_class ix ON ix.oid=i.indexrelid
            WHERE n.nspname=%s AND t.relname='customer' AND ix.relname='native_name'
        ''', (app.schema,)).one()
        constraints = connection.exec_driver_sql('''
            SELECT co.conname, co.contype, co.condeferrable, co.condeferred,
                   co.convalidated, pg_catalog.pg_get_constraintdef(co.oid),
                   pg_catalog.obj_description(co.oid, 'pg_constraint'),
                   co.conindid, co.conrelid
            FROM pg_catalog.pg_constraint co
            JOIN pg_catalog.pg_class t ON t.oid=co.conrelid
            JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
            WHERE n.nspname=%s AND t.relname='customer' AND co.conname='native_name'
            ORDER BY co.conname
        ''', (app.schema,)).all()
    assert len(constraints) in (0, 1)
    assert index[1] == table_oid, 'named index belongs to a different native table'
    # Compare independent observations, not the equality used in a JOIN.
    # OIDs identify each sample only; recreation may allocate new object OIDs.
    linked = tuple(row[-2] == index[0] and row[-1] == table_oid for row in constraints)
    assert all(linked), 'constraint does not own the observed named native index'
    return {
        'comments': {'index': index[-1],
                     'constraint': constraints[0][-3] if constraints else None},
        'shape': {'index': tuple(index[2:-1]),
                  'constraints': tuple(tuple(row[:6]) + (same_index,)
                                       for row, same_index in zip(constraints, linked, strict=True))},
    }


def _native_values(app):
    with app.owner.connect() as connection:
        statement = sql.SQL('SELECT id, tenant_id, name, label FROM {} ORDER BY id').format(
            sql.Identifier(app.schema, 'customer'))
        return [tuple(row) for row in connection.exec_driver_sql(
            statement.as_string(connection.connection.driver_connection)).all()]


def _expected_comments(case):
    return {'index': COMMENT if case in ('standalone_index', 'constraint_backing_index') else None,
            'constraint': COMMENT if case == 'unique_constraint' else None}


def _fresh_protection_plan(app):
    # application() already made an initial read-only plan. Bind the actual
    # commented native fixture into a fresh public plan before applying anything.
    app.plan = plan_helper.protect_plan(app, dict(
        backfill_rows_per_second=1000, verify_rows_per_second=1000,
        temporary_bytes_per_row=700, wal_bytes_per_row=2000))
    app.pin = replace(app.pin, operation_id=app.plan.operation_id, plan_digest=app.plan.digest)


def _edit_current_value(app, protected):
    if protected:
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=migration_helper.keys, deployment=(app.plan, app.pin))
        session = factory(tenant_id=migration_helper.TENANT)
    else:
        session = sessionmaker(app.runtime)()
    with session:
        row = session.get(app.Customer, EDIT_ID)
        assert row is not None
        row.name = EDITED
        session.commit()
        assert row.name == EDITED


def _observe(app, before, expected_values, path, stage):
    observed = _native_metadata(app)
    sample = {
        'stage': stage,
        'object_shape_preserved': observed['shape'] == before['shape'],
        'comments_preserved': observed['comments'] == before['comments'],
        'current_values_preserved': _native_values(app) == expected_values,
    }
    path['observations'].append(sample)
    # Compare booleans separately so a failure does not dump SQL definitions.
    assert sample['object_shape_preserved'], 'native index/constraint shape changed'
    assert sample['current_values_preserved'], 'current native values changed'
    assert sample['comments_preserved'], 'native object comment was not preserved'


@pytest.mark.parametrize('case', CASES)
def test_native_object_comments_survive_protection_reverse_and_removal(case):
    _assert_source_identity()
    destination = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent / 'object-comment-outcomes.jsonl'
    record = {'id': 'object-comments/' + case, 'sqlalchemy': sqlalchemy.__version__,
              'classification': 'INCOMPLETE_OR_FAILED', 'paths': []}
    try:
        for protected in (False, True):
            path = {'path': 'lifecycle' if protected else 'native',
                    'completed': False, 'observations': [], 'removal': 'NOT_REACHED'}
            record['paths'].append(path)
            with migration_helper.application(unique=case != 'standalone_index') as app:
                _configure_native_objects(app, case)
                before = _native_metadata(app)
                assert before['comments'] == _expected_comments(case)
                assert len(before['shape']['constraints']) == (0 if case == 'standalone_index' else 1)
                if before['shape']['constraints']:
                    assert before['shape']['constraints'][0][-1] is True
                original = _native_values(app)
                expected = [(identity, tenant, EDITED if identity == EDIT_ID else value, label)
                            for identity, tenant, value, label in original]
                if protected:
                    _fresh_protection_plan(app)
                    migration_helper.run(app)
                    migration_helper.publish(app)
                _edit_current_value(app, protected)
                if not protected:
                    path['removal'] = 'NOT_APPLICABLE'
                    _observe(app, before, expected, path, 'NATIVE_UNTOUCHED_OBJECTS')
                else:
                    d, plan, pin, consent = metadata_helper.reverse(app)
                    result = reverse_helper.execute(app, d, plan, pin, consent)
                    assert result.phase == 'PLAINTEXT_PENDING'
                    # Stop on metadata loss before product removal. The owned
                    # synthetic schema still receives normal fixture teardown.
                    _observe(app, before, expected, path, 'PLAINTEXT_PENDING')
                    metadata_helper.complete_removal(app, d, plan, pin, consent)
                    path['removal'] = 'REMOVED'
                    _observe(app, before, expected, path, 'REMOVED')
            # A path is complete only after its fixture teardown succeeds.
            path['completed'] = True
        record['classification'] = 'IDENTICAL'
    finally:
        primary = sys.exception()
        try:
            with destination.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(record, sort_keys=True) + '\n')
        except Exception:
            if primary is None:
                raise
            primary.add_note('The safe object-comment outcome receipt could not be written.')

"""Native PostgreSQL catalog identities versus environment-dependent deparsing."""
from contextlib import contextmanager
from pathlib import Path
import json,os
import asyncio
import sqlalchemy
import pytest
from sqlalchemy import event
from uuid import uuid4
import psycopg
from psycopg import sql
from sqlalchemy import create_engine
from test_migration import application,keys,TABLE_ID,FIELD_ID
from cryptalis import migration as m
from cryptalis.manifest.compiler import Writer,WriterInventory,SearchReview

@contextmanager
def visible_parent():
    with application() as app:
        with app.owner.begin() as c:
            c.exec_driver_sql(f'CREATE TABLE "{app.schema}".child(id uuid PRIMARY KEY,parent_id uuid REFERENCES "{app.schema}".customer(id))')
        engine=create_engine('postgresql+psycopg://',hide_parameters=True,creator=lambda:psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL'],options=f'-c search_path={app.schema},pg_catalog'))
        try:yield app,engine
        finally:engine.dispose()

def native_definition(c,schema):
    return c.exec_driver_sql('SELECT oid,conrelid,confrelid,conkey,confkey,pg_catalog.pg_get_constraintdef(oid) FROM pg_catalog.pg_constraint WHERE conrelid=%s::regclass AND contype=\'f\'',(f'{schema}.child',)).one()

def test_catalog_deparser_changes_text_without_changing_object_identity():
    with visible_parent() as (app,engine),engine.connect() as c:
        before=native_definition(c,app.schema)
        c.exec_driver_sql('SET LOCAL search_path=pg_catalog')
        after=native_definition(c,app.schema)
        assert tuple(before[:5])==tuple(after[:5])
        assert before[5]!=after[5]
        if 'CRYPTALIS_LAB_PROGRESS' in os.environ: (Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent/'native-deparser-proof.json').write_text(json.dumps({'same_object_identity':True,'ambient':before[5],'canonical':after[5]},indent=2))

def test_schema_fingerprint_is_independent_of_caller_path():
    with visible_parent() as (app,engine),engine.connect() as c:
        model=app.plan.document['lock']['models'][0]
        ambient=m._facts(c,model)
        c.exec_driver_sql('SET LOCAL search_path=pg_catalog')
        canonical=m._facts(c,model)
        assert ambient==canonical

def test_unchanged_foreign_key_schema_plans_from_application_path():
    with visible_parent() as (app,engine):
        manifest=app.plan.document['lock']['declaration']
        plan=m.plan(json.dumps(manifest).encode(),app.mapping,engine,writers=WriterInventory(True,(Writer(TABLE_ID,'app','sqlalchemy',evidence='Only this isolated fixture writes these tables'),)),search_reviews=(SearchReview(FIELD_ID,False,'Synthetic fixture names'),),keys=keys,runtime_role=app.role,target_id=uuid4(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        assert plan.document['lock']['models'][0]['schema']==app.schema

@pytest.mark.parametrize('nested', [False, True])
def test_inspection_preserves_caller_transaction_and_path(nested):
    with visible_parent() as (app, engine), engine.connect() as c:
        root = c.begin()
        outer = c.begin_nested() if nested else None
        row = uuid4()
        c.exec_driver_sql(f'INSERT INTO "{app.schema}".child(id) VALUES (%s)', (row,))
        path = c.exec_driver_sql('SHOW search_path').scalar_one()
        m._facts(c, app.plan.document['lock']['models'][0])
        assert c.exec_driver_sql('SHOW search_path').scalar_one() == path
        assert c.get_nested_transaction() is outer
        with app.owner.connect() as other:
            assert other.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".child WHERE id=%s', (row,)).scalar_one() == 0
        if outer: outer.commit()
        root.commit()
        with app.owner.connect() as other:
            assert other.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".child WHERE id=%s', (row,)).scalar_one() == 1

@pytest.mark.parametrize('native', [False, True])
@pytest.mark.parametrize('failure', ['python', 'server', 'interrupt', 'cancel'])
def test_failed_inspection_preserves_outer_work_and_cancellation(failure, native):
    with visible_parent() as (app, engine), engine.connect() as c:
        root = c.begin()
        row = uuid4()
        c.exec_driver_sql(f'INSERT INTO "{app.schema}".child(id) VALUES (%s)', (row,))
        path = c.exec_driver_sql('SHOW search_path').scalar_one()
        primary = {'python': RuntimeError('synthetic read'), 'interrupt': KeyboardInterrupt(), 'cancel': asyncio.CancelledError()}.get(failure)
        fired = []
        def inject(conn, cursor, statement, parameters, context, many):
            if 'FROM pg_catalog.pg_constraint' in statement and not fired:
                fired.append(True)
                if failure == 'server': cursor.execute('SELECT 1/0')
                else: raise primary
        event.listen(c, 'before_cursor_execute', inject)
        try:
            with pytest.raises(BaseException) as caught:
                if native:
                    with c.begin_nested(): native_definition(c, app.schema)
                else:
                    m._facts(c, app.plan.document['lock']['models'][0])
        finally:
            event.remove(c, 'before_cursor_execute', inject)
        assert fired
        if primary is not None: assert caught.value is primary
        else: assert getattr(getattr(caught.value, 'orig', caught.value), 'sqlstate', None) == '22012'
        if failure in ('interrupt', 'cancel') and sqlalchemy.__version__.startswith('2.1.'):
            assert c.invalidated  # 2.1 wraps event dispatch; 2.0 propagates before it.
            root.rollback()
            with app.owner.connect() as other:
                assert other.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".child WHERE id=%s', (row,)).scalar_one() == 0
            return
        assert c.exec_driver_sql('SHOW search_path').scalar_one() == path
        assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".child WHERE id=%s', (row,)).scalar_one() == 1
        root.commit()
        with app.owner.connect() as other:
            assert other.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".child WHERE id=%s', (row,)).scalar_one() == 1


def test_real_foreign_key_change_remains_visible():
    with visible_parent() as (app, engine), engine.begin() as c:
        model = app.plan.document['lock']['models'][0]
        before = m._facts(c, model)
        c.exec_driver_sql(f'ALTER TABLE "{app.schema}".child DROP CONSTRAINT child_parent_id_fkey')
        c.exec_driver_sql(f'ALTER TABLE "{app.schema}".child ADD CONSTRAINT child_parent_id_fkey FOREIGN KEY(parent_id) REFERENCES "{app.schema}".customer(id) ON DELETE CASCADE')
        after = m._facts(c, model)
        assert before != after

@pytest.mark.parametrize('stage', ['rollback', 'release', 'restore'])
def test_uncertain_scope_cleanup_never_returns_catalog_facts(stage):
    from cryptalis.manifest.compiler import InspectionUnavailable
    with visible_parent() as (app, engine), engine.connect() as c:
        c.begin()
        dbapi = c.connection.dbapi_connection
        def read_fault(conn, cursor, statement, parameters, context, many):
            if stage == 'rollback' and 'FROM pg_catalog.pg_constraint' in statement:
                raise RuntimeError('PRIVATE synthetic read sentinel')
            if stage == 'restore' and 'set_config' in statement:
                raise RuntimeError('PRIVATE synthetic restore sentinel')
        def cleanup_fault(*args):
            raise RuntimeError('PRIVATE synthetic cleanup sentinel')
        event.listen(c, 'before_cursor_execute', read_fault)
        event.listen(c, 'rollback_savepoint' if stage != 'release' else 'release_savepoint', cleanup_fault)
        try:
            with pytest.raises(InspectionUnavailable) as caught:
                m._facts(c, app.plan.document['lock']['models'][0])
            assert 'PRIVATE' not in str(caught.value)
            assert 'do not reuse this connection' in str(caught.value)
            assert c.invalidated
            assert dbapi.closed
        finally:
            event.remove(c, 'before_cursor_execute', read_fault)
            event.remove(c, 'rollback_savepoint' if stage != 'release' else 'release_savepoint', cleanup_fault)
            c.rollback()


def test_invalidation_failure_closes_physical_connection(monkeypatch):
    from cryptalis.manifest.compiler import InspectionUnavailable
    with visible_parent() as (app, engine), engine.connect() as c:
        c.begin()
        dbapi = c.connection.dbapi_connection
        def fail(*args, **kwargs): raise RuntimeError('PRIVATE cleanup sentinel')
        event.listen(c, 'release_savepoint', fail)
        monkeypatch.setattr(c, 'invalidate', fail)
        try:
            with pytest.raises(InspectionUnavailable) as caught:
                m._facts(c, app.plan.document['lock']['models'][0])
            assert dbapi.closed
            assert 'PRIVATE' not in str(caught.value)
            assert ('connection_invalidate', 'RuntimeError') in caught.value.cleanup_errors
        finally:
            event.remove(c, 'release_savepoint', fail)
            monkeypatch.undo()
            c.invalidate()
            c.rollback()

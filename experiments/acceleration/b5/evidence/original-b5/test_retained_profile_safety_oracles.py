"""Independent retained-profile coverage; historical legacy failures stay intact."""
from dataclasses import replace
from uuid import UUID

import psycopg
import pytest
from sqlalchemy import event

from test_deprotection import prepared,execute,plaintext_url
from test_migration import application,frames,independent_open,TENANT,FIELD_ID
from test_retained_public_metadata import reverse


def catalog(c,app):
    # Native catalog/value snapshots deliberately do not use migration._facts,
    # reverse._model, or the executor's own schema-equivalence implementation.
    target=f'"{app.schema}".customer'
    columns=c.exec_driver_sql('''SELECT a.attnum,a.attname,a.atttypid::bigint,
        a.atttypmod,a.attcollation::bigint,a.attnotnull,a.attidentity,a.attgenerated,
        a.attstorage,a.attcompression,a.attstattarget,a.attacl::text,
        pg_catalog.col_description(a.attrelid,a.attnum),pg_catalog.pg_get_expr(d.adbin,d.adrelid)
        FROM pg_catalog.pg_attribute a LEFT JOIN pg_catalog.pg_attrdef d
        ON d.adrelid=a.attrelid AND d.adnum=a.attnum
        WHERE a.attrelid=pg_catalog.to_regclass(%s) AND a.attnum>0 AND NOT a.attisdropped
        ORDER BY a.attnum''',(target,)).all()
    indexes=c.exec_driver_sql('''SELECT pg_catalog.pg_get_indexdef(indexrelid),indisvalid,indisready
        FROM pg_catalog.pg_index WHERE indrelid=pg_catalog.to_regclass(%s)
        ORDER BY pg_catalog.pg_get_indexdef(indexrelid)''',(target,)).all()
    triggers=c.exec_driver_sql('''SELECT tgname,tgenabled,pg_catalog.pg_get_triggerdef(oid)
        FROM pg_catalog.pg_trigger WHERE tgrelid=pg_catalog.to_regclass(%s)
        AND NOT tgisinternal ORDER BY tgname''',(target,)).all()
    oid=c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)::oid',(target,)).scalar_one()
    return oid,columns,indexes,triggers


def snapshot(app):
    with app.owner.connect() as c:
        state=c.exec_driver_sql(f'SELECT operation_id,plan_digest,state FROM "{app.schema}"._cryptalis_journal ORDER BY operation_id').all()
        data=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
        values=(list(data.keys()),data.all())
        return catalog(c,app),state,values


def native_values(app):
    with app.owner.connect() as c:
        data=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
        return list(data.keys()),data.all()


def independent_frames(app):
    retained=frames(app,True)
    descriptor=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
    assert {key:independent_open(body,descriptor,TENANT,key) for key,body in retained.items()}=={
        key:value for key,(_,value) in app.source.items()}
    return retained


@pytest.mark.parametrize('phase',['backfill','verify'])
def test_retained_reverse_protected_byte_refusal_preserves_exact_state_and_recovers(phase):
    with application(rows=2) as app:
        assert app.plan.document['format']=='cryptalis.transition/retained-native-research-v0'
        expected={UUID(int=100):'prefix 雪',UUID(int=101):'雪😀'*8192}
        with app.owner.begin() as c:
            for identity,value in expected.items():
                c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET name=%s WHERE id=%s',(value,identity))
                app.source[identity]=(TENANT,value)
        original=native_values(app)
        d,plan,pin,consent=prepared(app)
        backup=independent_frames(app)
        if phase=='backfill':
            execute(app,d,plan,pin,consent,'EXPANDED')
            with app.owner.connect() as c:expanded_catalog=catalog(c,app)
            with pytest.raises(app.m.TransitionFailure,match='row_exceeds_chunk_byte_limit'):
                execute(app,d,plan,pin,consent,'BACKFILLED',chunk_bytes=512)
            # A fitting prefix can commit, but the oversized successor is not
            # skipped or falsely marked complete. A repeat must add no effects.
            with app.owner.connect() as c:
                assert catalog(c,app)==expanded_catalog
                assert c.exec_driver_sql(f'SELECT "_cryptalis_{FIELD_ID.hex}_plain" FROM "{app.schema}".customer ORDER BY id').all()==[(expected[UUID(int=100)],),(None,)]
                state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',(plan.operation_id,)).scalar_one()
                assert state['phase']=='EXPANDED'
                assert next(iter(state['models'].values()))['rows']==1
            stop='BACKFILLED'
        else:
            execute(app,d,plan,pin,consent,'BACKFILLED',chunk_bytes=1024*1024)
            stop='VERIFIED'
        before=snapshot(app)
        fetched=[]
        def observe(conn,cursor,statement,*args):
            if statement.startswith('WITH _cryptalis_candidates'):
                fetched.append(cursor.rowcount)
        event.listen(app.owner,'after_cursor_execute',observe)
        try:
            with pytest.raises(app.m.TransitionFailure,match='row_exceeds_chunk_byte_limit'):
                execute(app,d,plan,pin,consent,stop,chunk_bytes=512)
        finally:
            event.remove(app.owner,'after_cursor_execute',observe)
        assert fetched and fetched[-1]==0, 'Oversized payload must not be returned before refusal'
        assert snapshot(app)==before
        assert frames(app,True)==backup
        assert execute(app,d,plan,pin,consent,chunk_bytes=1024*1024).phase=='PLAINTEXT_PENDING'
        assert native_values(app)==original


def test_retained_reverse_never_projects_untouched_wide_public_value_into_chunk_transport():
    with application() as app:
        wide='untouched public 雪😀'*4096
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',(wide,))
        expected=native_values(app)
        d,plan,pin,consent=prepared(app)
        with app.owner.connect() as c:
            public_before=next(row for row in catalog(c,app)[1] if row[1]=='label')
        projected=[]
        def observe(conn,cursor,statement,*args):
            if statement.startswith('WITH _cryptalis_candidates'):
                projected.append(tuple(column.name for column in cursor.description))
        event.listen(app.owner,'after_cursor_execute',observe)
        try:
            assert execute(app,d,plan,pin,consent,'BACKFILLED',chunk_bytes=512).phase=='BACKFILLED'
            assert execute(app,d,plan,pin,consent,chunk_bytes=512).phase=='PLAINTEXT_PENDING'
        finally:
            event.remove(app.owner,'after_cursor_execute',observe)
        assert projected and all('label' not in columns for columns in projected)
        assert any('_cryptalis_'+FIELD_ID.hex+'_plain' in columns for columns in projected)
        with app.owner.connect() as c:
            assert next(row for row in catalog(c,app)[1] if row[1]=='label')==public_before
        assert native_values(app)==expected


def test_retained_public_select_acl_survives_removal_without_relaxing_retired_writes():
    from test_migration import run,publish
    with application() as app:
        expected=native_values(app)
        run(app);publish(app)
        backup=independent_frames(app)
        # Exact existing legacy/retained metadata fixture, within this synthetic
        # schema and role. No new principal or broader reader policy is added.
        with app.owner.begin() as c:
            c.exec_driver_sql(f'GRANT SELECT(label) ON "{app.schema}".customer TO "{app.role}"')
        with app.owner.connect() as c:
            before=next(row for row in catalog(c,app)[1] if row[1]=='label')
            assert before[11] is not None
        d,plan,pin,consent=reverse(app)
        execute(app,d,plan,pin,consent)
        execute(app,d,plan,replace(pin,phase='PLAINTEXT_ACTIVATING'),consent,'PLAINTEXT_ACTIVE')
        with psycopg.connect(plaintext_url()) as c:
            assert c.execute(f'SELECT * FROM "{app.schema}".customer ORDER BY id').fetchall()==expected[1]
        proof=d.RemovalApproval(plan.digest,'Existing plaintext-role native SELECT matched all current rows',
                                'Retained public-root CF1 frames independently decoded before and after removal',True)
        assert d.remove(plan,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,
                        plaintext_approval=consent,removal_approval=proof).phase=='REMOVED'
        d.check_removed(plan,app.owner,pin=replace(pin,phase='REMOVED'))
        with app.owner.connect() as c:
            assert next(row for row in catalog(c,app)[1] if row[1]=='label')==before
            assert not c.exec_driver_sql('SELECT pg_catalog.has_table_privilege(%s,pg_catalog.to_regclass(%s),%s)',
                (app.role,f'"{app.schema}".customer','INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER')).scalar_one()
            assert not c.exec_driver_sql('SELECT pg_catalog.has_any_column_privilege(%s,pg_catalog.to_regclass(%s),%s)',
                (app.role,f'"{app.schema}".customer','INSERT,UPDATE,REFERENCES')).scalar_one()
        assert native_values(app)==expected
        descriptor=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        assert {key:independent_open(body,descriptor,TENANT,key) for key,body in backup.items()}=={
            key:value for key,(_,value) in app.source.items()}

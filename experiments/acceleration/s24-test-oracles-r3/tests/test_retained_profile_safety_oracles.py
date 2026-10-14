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


def native_buffer(cursor):
    """Observe libpq result buffers without advancing the driver's cursor."""
    result=cursor.pgresult
    assert result is not None
    fields=tuple((result.fname(i).decode(),result.ftable(i),result.ftablecol(i),
                  result.ftype(i),result.fformat(i)) for i in range(result.nfields))
    rows=tuple(tuple(result.get_value(r,i) for i in range(result.nfields))
               for r in range(result.ntuples))
    return fields,rows


def identities(sample):
    fields,rows=sample
    assert fields[0][3]==2950  # Native UUID identity, independently declared fixture.
    return tuple(UUID(bytes=row[0]) if fields[0][4] else UUID(row[0].decode()) for row in rows)


def fetched_value_bytes(sample):
    # Logical driver values, not network bytes, Python object overhead or RSS.
    fields,rows=sample
    total=0
    for row in rows:
        for field,value in zip(fields,row):
            if value is None:continue
            if field[3]==2950:total+=16
            elif field[3]==17 and field[4]==0:
                assert value.startswith(b'\\x')
                total+=len(bytes.fromhex(value[2:].decode()))
            else:total+=len(value)
    return total


def projection(c,app,names):
    oid,columns,_,_=catalog(c,app)
    by_name={row[1]:row[0] for row in columns}
    return tuple((oid,by_name[name]) for name in names)


def assert_no_public_source(sample,public,marker):
    fields,rows=sample
    assert public not in tuple((f[1],f[2]) for f in fields), 'public source column returned under any alias'
    assert not any(marker in value for row in rows for value in row if value is not None), 'public value marker returned'


def assert_trace(samples,expected_ids,expected_projection,budget):
    assert len(samples)==len(expected_ids), 'unexpected result sequence'
    for sample,expected in zip(samples,expected_ids):
        fields,_=sample
        assert tuple((f[1],f[2]) for f in fields)==expected_projection, 'unexpected native column provenance'
        assert identities(sample)==expected, 'unexpected returned identity'
        assert fetched_value_bytes(sample)<=budget, 'result exceeds logical fetched-value bound'


@pytest.mark.parametrize('phase',['backfill','verify'])
def test_retained_reverse_protected_byte_refusal_preserves_exact_state_and_recovers(phase):
    with application(rows=2) as app:
        assert app.plan.document['format']=='cryptalis.transition/retained-native-comments-research-v1'
        assert app.plan.object_comment_contract == 'INVENTORIED'
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
            with app.owner.connect() as c:
                expanded_catalog=catalog(c,app)
                first_projection=projection(c,app,['id','tenant_id','_cryptalis_'+FIELD_ID.hex])
            first_results=[]
            def observe_first(conn,cursor,statement,*args):
                if statement.startswith('WITH _cryptalis_candidates'):
                    first_results.append(native_buffer(cursor))
            event.listen(app.owner,'after_cursor_execute',observe_first)
            try:
                with pytest.raises(app.m.TransitionFailure,match='row_exceeds_chunk_byte_limit'):
                    execute(app,d,plan,pin,consent,'BACKFILLED',chunk_bytes=512)
            finally:
                event.remove(app.owner,'after_cursor_execute',observe_first)
            assert_trace(first_results,[(UUID(int=100),),()],first_projection,512)
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
        names=['id','tenant_id','_cryptalis_'+FIELD_ID.hex]
        if phase=='verify':names.append('_cryptalis_'+FIELD_ID.hex+'_plain')
        with app.owner.connect() as c:expected_projection=projection(c,app,names)
        def observe(conn,cursor,statement,*args):
            if statement.startswith('WITH _cryptalis_candidates'):
                fetched.append(native_buffer(cursor))
        event.listen(app.owner,'after_cursor_execute',observe)
        try:
            with pytest.raises(app.m.TransitionFailure,match='row_exceeds_chunk_byte_limit'):
                execute(app,d,plan,pin,consent,stop,chunk_bytes=512)
        finally:
            event.remove(app.owner,'after_cursor_execute',observe)
        expected_results=[()] if phase=='backfill' else [(UUID(int=100),),()]
        assert_trace(fetched,expected_results,expected_projection,512)
        assert all(UUID(int=101) not in identities(sample) for sample in fetched)
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
        execute(app,d,plan,pin,consent,'EXPANDED',chunk_bytes=512)
        projected=[]
        with app.owner.connect() as c:
            public=projection(c,app,['label'])[0]
            backfill_projection=projection(c,app,['id','tenant_id','_cryptalis_'+FIELD_ID.hex])
            verify_projection=projection(c,app,['id','tenant_id','_cryptalis_'+FIELD_ID.hex,'_cryptalis_'+FIELD_ID.hex+'_plain'])
        def observe(conn,cursor,statement,*args):
            if statement.startswith('WITH _cryptalis_candidates'):
                projected.append(native_buffer(cursor))
        event.listen(app.owner,'after_cursor_execute',observe)
        try:
            assert execute(app,d,plan,pin,consent,'BACKFILLED',chunk_bytes=512).phase=='BACKFILLED'
            assert execute(app,d,plan,pin,consent,chunk_bytes=512).phase=='PLAINTEXT_PENDING'
        finally:
            event.remove(app.owner,'after_cursor_execute',observe)
        assert projected
        seen={backfill_projection:[],verify_projection:[]}
        for sample in projected:
            assert_no_public_source(sample,public,wide.encode())
            provenance=tuple((field[1],field[2]) for field in sample[0])
            assert provenance in seen, 'unexpected result expression or aliased source'
            assert fetched_value_bytes(sample)<=512
            seen[provenance].extend(identities(sample))
        assert all(values==sorted(app.source) for values in seen.values())
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


def test_native_aliased_public_projection_is_detected_without_consuming_cursor():
    with application(rows=1) as app:
        marker='native aliased public marker 雪'*1024
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',(marker,))
        statement=f'SELECT label AS innocuous_value FROM "{app.schema}".customer ORDER BY id'
        captured=[]
        def observe(conn,cursor,sql,*args):
            if sql==statement:captured.append(native_buffer(cursor))
        event.listen(app.owner,'after_cursor_execute',observe)
        try:
            with app.owner.connect() as c:
                public=projection(c,app,['label'])[0]
                # The observer must leave the ordinary caller's result intact.
                assert c.exec_driver_sql(statement).all()==[(marker,)]
        finally:event.remove(app.owner,'after_cursor_execute',observe)
        assert len(captured)==1
        assert captured[0][0][0][0]=='innocuous_value'
        assert 'label' not in [field[0] for field in captured[0][0]]
        assert any(marker.encode() in value for row in captured[0][1] for value in row if value is not None)
        with pytest.raises(AssertionError,match='public source column'):
            assert_no_public_source(captured[0],public,marker.encode())
        # Derived values can lose column provenance; the byte marker is separate.
        with pytest.raises(AssertionError,match='public value marker'):
            assert_no_public_source(captured[0],(-1,-1),marker.encode())


def test_native_earlier_oversize_result_is_detected_despite_empty_tail():
    with application(rows=2) as app:
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET name=%s WHERE id=%s',('雪'*8192,UUID(int=101)))
        selected=f'SELECT id,tenant_id,name FROM "{app.schema}".customer WHERE id=\'{UUID(int=101)}\' ORDER BY id'
        empty=f'SELECT id,tenant_id,name FROM "{app.schema}".customer WHERE false ORDER BY id'
        captured=[]
        def observe(conn,cursor,statement,*args):
            if statement in (selected,empty):captured.append(native_buffer(cursor))
        event.listen(app.owner,'after_cursor_execute',observe)
        try:
            with app.owner.connect() as c:
                columns=projection(c,app,['id','tenant_id','name'])
                assert len(c.exec_driver_sql(selected).all())==1
                assert c.exec_driver_sql(empty).all()==[]
        finally:event.remove(app.owner,'after_cursor_execute',observe)
        assert identities(captured[-1])==()  # The previous last-only check misses this.
        assert fetched_value_bytes(captured[0])>512
        with pytest.raises(AssertionError,match='unexpected returned identity'):
            assert_trace(captured,[(UUID(int=100),),()],columns,512)
        with pytest.raises(AssertionError,match='logical fetched-value bound'):
            assert_trace(captured,[(UUID(int=101),),()],columns,512)

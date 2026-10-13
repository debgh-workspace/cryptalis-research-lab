"""Independent UTF8 accounting and PG prefix/oversize migration oracles."""
import pytest
from sqlalchemy import event
from test_migration import application, keys, TENANT, frames, independent_open


def cost(value):
    # Fixture uses UUID record+tenant, one searchable text field.
    return 32 + (0 if value is None else 2*len(value.encode('utf8'))+74)

@pytest.mark.parametrize('budget',[32,137,138,258,1000])
def test_database_selects_exact_byte_bounded_prefix(budget):
    with application() as app:
        model=app.plan.document['lock']['models'][0]
        expected=[];used=0
        for record,(tenant,value) in sorted(app.source.items()):
            if used+cost(value)>budget:break
            expected.append(record);used+=cost(value)
        with app.owner.connect() as c:
            rows=app.m._stream(c,model,limit=7,byte_limit=budget)
        assert [r[0] for r in rows]==expected
        assert sum(cost(r[2]) for r in rows)<=budget


def test_byte_bound_committed_prefix_resume_and_full_verification():
    with application() as app:
        result=app.m.apply(app.plan,app.owner,keys=keys,pin=app.pin,approval=app.approval,
                           chunk_size=7,chunk_bytes=138,until='BACKFILLED')
        assert result.committed_rows==7 and result.committed_chunks>1
        desc=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        before=frames(app)
        assert {r:independent_open(f,desc,TENANT,r) for r,f in before.items()}=={r:v for r,(t,v) in app.source.items()}
        # Verification has a separate source+frame+decoded-value budget and
        # must refuse if one current row cannot fit, without changing frames.
        with pytest.raises(app.m.TransitionFailure) as err:
            app.m.apply(app.plan,app.owner,keys=keys,pin=app.pin,approval=app.approval,
                        chunk_bytes=32,until='VERIFIED')
        assert err.value.code=='row_exceeds_chunk_byte_limit' and frames(app)==before
        result=app.m.apply(app.plan,app.owner,keys=keys,pin=app.pin,approval=app.approval,
                           chunk_bytes=1024,until='PENDING')
        assert result.phase=='PENDING'
        assert frames(app,switched=True)==before


def test_oversize_after_committed_prefix_never_skips_a_row():
    with application(rows=4) as app:
        with pytest.raises(app.m.TransitionFailure) as err:
            app.m.apply(app.plan,app.owner,keys=keys,pin=app.pin,approval=app.approval,
                        chunk_size=4,chunk_bytes=106,until='BACKFILLED')
        assert err.value.code=='row_exceeds_chunk_byte_limit'
        before=frames(app);ordered=sorted(before)
        assert before[ordered[1]] is not None and all(before[r] is None for r in ordered[2:])
        with app.owner.connect() as c:
            state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal').scalar_one()
        assert next(iter(state['models'].values()))['rows']==2
        result=app.m.apply(app.plan,app.owner,keys=keys,pin=app.pin,approval=app.approval,
                           chunk_bytes=1024,until='BACKFILLED')
        assert result.committed_rows==4
        assert {r:frames(app)[r] for r in ordered[:2]}=={r:before[r] for r in ordered[:2]}

@pytest.mark.parametrize('bound',[0,-1,True,1.5,None,2**30+1])
def test_invalid_byte_bound_refuses_before_any_sql(bound):
    with application() as app:
        seen=[]
        def emitted(*args):seen.append(1)
        event.listen(app.owner,'before_cursor_execute',emitted)
        try:
            with pytest.raises(app.m.TransitionFailure) as err:
                app.m.apply(app.plan,app.owner,keys=keys,pin=app.pin,approval=app.approval,chunk_bytes=bound)
            assert err.value.code=='invalid_apply_bound' and seen==[]
        finally:event.remove(app.owner,'before_cursor_execute',emitted)


def test_oversize_payload_is_not_returned_to_client_before_refusal():
    with application(rows=1) as app:
        record=next(iter(app.source))
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET name=%s WHERE id=%s',('雪'*8192,record))
        returned=[]
        def observed(conn,cursor,statement,parameters,context,many):
            if statement.startswith('WITH _cryptalis_candidates'):returned.append(cursor.rowcount)
        event.listen(app.owner,'after_cursor_execute',observed)
        try:
            with app.owner.connect() as c:
                with pytest.raises(app.m.TransitionFailure) as error:
                    app.m._stream(c,app.plan.document['lock']['models'][0],byte_limit=1024)
            assert error.value.code=='row_exceeds_chunk_byte_limit'
            assert returned==[0]
        finally:event.remove(app.owner,'after_cursor_execute',observed)


def test_multi_field_accounting_includes_storage_only_frame_overhead():
    import json
    from uuid import UUID,uuid4
    from test_migration import TABLE_ID,FIELD_ID
    from cryptalis.manifest.compiler import Writer,WriterInventory,SearchReview
    with application(rows=4) as app:
        declaration=app.plan.document['lock']['declaration']
        extra=UUID(int=607)
        declaration['models'][0]['fields'].append({'name':'label','field_id':str(extra),'protect':True,'queries':[],'accept_leakage':[]})
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',('雪😀'*30,))
        proposal=app.m.plan(json.dumps(declaration).encode(),app.mapping,app.owner,
            writers=WriterInventory(True,(Writer(TABLE_ID,'app','sqlalchemy',evidence='byte-bound fixture'),)),
            search_reviews=(SearchReview(FIELD_ID,False,'unbounded names'),),keys=keys,runtime_role=app.role,
            target_id=uuid4(),backfill_rows_per_second=1000,verify_rows_per_second=1000,
            temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        pin=app.m.DeploymentPin(proposal.target_id,proposal.operation_id,proposal.digest,'PREPARED')
        model=proposal.document['lock']['models'][0]
        # 420 UTF8 bytes across source+future storage-only frame, plus42frame
        # bytes. The first row is NULL for the searchable name:32+462=494.
        with app.owner.connect() as c:
            rows=app.m._stream(c,model,byte_limit=494)
        label_position=2+next(i for i,f in enumerate(model['fields']) if f['column']=='label')
        assert len(rows)==1 and rows[0][label_position]=='雪😀'*30
        result=app.m.apply(proposal,app.owner,keys=keys,pin=pin,approval=app.approval,
                           chunk_size=4,chunk_bytes=700,until='BACKFILLED')
        assert result.committed_rows==4 and result.committed_chunks==4
        with app.owner.connect() as c:
            rows=c.exec_driver_sql(f'SELECT id, "_cryptalis_{extra.hex}" FROM "{app.schema}".customer ORDER BY id').all()
        field=next(f for f in model['fields'] if f['column']=='label')
        assert all(independent_open(bytes(body),field['descriptor'],TENANT,record,field_id=extra)=='雪😀'*30 for record,body in rows)

"""Independent native metadata/value oracle for the explicit retained profile."""
from dataclasses import replace
import pytest
from cryptalis.migration import DeploymentPin
from test_migration import application,run,publish,keys
from test_deprotection import api,plaintext_role,execute


def metadata(c,app):
    return c.exec_driver_sql('''SELECT t.oid::bigint,a.attnum,a.atttypid::bigint,
        a.atttypmod,a.attcollation::bigint,a.attnotnull,a.attidentity,a.attgenerated,
        a.attstorage,a.attcompression,a.attstattarget,a.attacl::text,
        pg_catalog.col_description(t.oid,a.attnum),pg_catalog.pg_get_expr(d.adbin,d.adrelid)
        FROM pg_catalog.pg_class t JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
        JOIN pg_catalog.pg_attribute a ON a.attrelid=t.oid
        LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid=t.oid AND d.adnum=a.attnum
        WHERE n.nspname=%s AND t.relname='customer' AND a.attname='label' AND NOT a.attisdropped''',(app.schema,)).one()


def reverse(app):
    d=api()
    plan=d.plan(app.plan,app.owner,source_pin=app.pin,keys=keys,plaintext_runtime_role=plaintext_role(),
        backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
    pin=DeploymentPin(plan.target_id,plan.operation_id,plan.digest,'PREPARED')
    consent=d.PlaintextApproval(plan.target_id,plan.operation_id,plan.digest,True,'Owned synthetic fixture; current native oracle and reader retained')
    return d,plan,pin,consent


@pytest.mark.parametrize('attribute',['comment','column_grant','statistics','storage','compression'])
def test_retained_public_metadata_survives_current_data_reverse(attribute):
    with application() as app:
        assert app.plan.document['format']=='cryptalis.transition/retained-native-research-v0'
        with app.owner.connect() as c:
            result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
            original=(list(result.keys()),result.all())
        run(app);publish(app)
        statements={
            'comment':f'''COMMENT ON COLUMN "{app.schema}".customer.label IS 'current native metadata' ''',
            'column_grant':f'GRANT SELECT(label) ON "{app.schema}".customer TO "{app.role}"',
            'statistics':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STATISTICS 100',
            'storage':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STORAGE EXTERNAL',
            'compression':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET COMPRESSION pglz',
        }
        with app.owner.begin() as c:c.exec_driver_sql(statements[attribute])
        with app.owner.connect() as c:before=metadata(c,app)
        d,plan,pin,consent=reverse(app)
        with app.owner.connect() as c:
            assert metadata(c,app)==before
            assert c.exec_driver_sql("SELECT count(*) FROM information_schema.columns WHERE table_schema=%s AND column_name LIKE '%%_plain'",(app.schema,)).scalar_one()==0
        assert execute(app,d,plan,pin,consent).phase=='PLAINTEXT_PENDING'
        with app.owner.connect() as c:
            assert metadata(c,app)==before
            result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
            assert (list(result.keys()),result.all())==original


@pytest.mark.parametrize('wide',[False,True])
def test_retained_reverse_preserves_public_edits_without_copy_staging(wide):
    with application() as app:
        run(app);publish(app)
        d,plan,pin,consent=reverse(app)
        assert execute(app,d,plan,pin,consent,'BACKFILLED',chunk_bytes=512).phase=='BACKFILLED'
        value='wide public suffix'*2048 if wide else 'current public edit 雪'
        with app.owner.begin() as c:
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',(value,))
        with app.owner.connect() as c:
            before=metadata(c,app)
            assert c.exec_driver_sql("SELECT count(*) FROM information_schema.columns WHERE table_schema=%s AND column_name LIKE '%%_copy_%%'",(app.schema,)).scalar_one()==0
        assert execute(app,d,plan,pin,consent,chunk_bytes=512).phase=='PLAINTEXT_PENDING'
        with app.owner.connect() as c:
            assert metadata(c,app)==before
            rows=c.exec_driver_sql(f'SELECT id,tenant_id,name,label FROM "{app.schema}".customer ORDER BY id').all()
            assert rows==[(k,t,v,value) for k,(t,v) in sorted(app.source.items())]


def complete_removal(app,d,plan,pin,consent):
    execute(app,d,plan,replace(pin,phase='PLAINTEXT_ACTIVATING'),consent,'PLAINTEXT_ACTIVE')
    # These are explicit fixture attestations for the removal state machine.
    # Independent backup/package-free proofs live in their own end-to-end tests.
    approval=d.RemovalApproval(plan.digest,'synthetic native metadata oracle','separate backup-reader qualification required',True)
    assert d.remove(plan,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,
                    plaintext_approval=consent,removal_approval=approval).phase=='REMOVED'
    d.check_removed(plan,app.owner,pin=replace(pin,phase='REMOVED'))


@pytest.mark.parametrize('attribute',['comment','statistics','storage','compression'])
def test_native_public_metadata_survives_final_removal(attribute):
    with application() as app:
        run(app);publish(app)
        statements={
            'comment':f"COMMENT ON COLUMN \"{app.schema}\".customer.label IS 'retained after removal'",
            'statistics':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STATISTICS 100',
            'storage':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STORAGE EXTERNAL',
            'compression':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET COMPRESSION pglz',
        }
        with app.owner.begin() as c:
            c.exec_driver_sql(statements[attribute])
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',('current public value 雪',))
        with app.owner.connect() as c:before=metadata(c,app)
        d,plan,pin,consent=reverse(app)
        execute(app,d,plan,pin,consent)
        complete_removal(app,d,plan,pin,consent)
        with app.owner.connect() as c:
            assert metadata(c,app)==before
            assert c.exec_driver_sql(f'SELECT id,tenant_id,name,label FROM "{app.schema}".customer ORDER BY id').all()==[(k,t,v,'current public value 雪') for k,(t,v) in sorted(app.source.items())]
            assert c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)',(app.schema+'._cryptalis_journal',)).scalar_one() is None
            assert c.exec_driver_sql("SELECT count(*) FROM information_schema.columns WHERE table_schema=%s AND column_name LIKE '%%_cryptalis_%%'",(app.schema,)).scalar_one()==0

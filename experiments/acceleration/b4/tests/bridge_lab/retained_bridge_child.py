"""Run only via the unchanged role-preflight runner in a separate installed package."""
from pathlib import Path
from dataclasses import replace
from types import SimpleNamespace
from uuid import UUID,uuid4
import json,os,subprocess,sys
import pytest,psycopg
from _bridge_binding import verify_package,verify_source
TARGET=Path(os.environ['CRYPTALIS_BRIDGE_TARGET_SOURCE']).resolve()
sys.path.insert(0,str(TARGET/'tests'))
from sqlalchemy import MetaData,Table,create_engine,select
from sqlalchemy.orm import registry
from cryptalis import migration as m,deprotection as d
from cryptalis.manifest.compiler import WriterInventory,Writer,SearchReview
from cryptalis.sqlalchemy import attach
from test_migration import keys,independent_open,engine,TENANT,TABLE_ID,FIELD_ID
from test_deprotection import plaintext_url,retire_old_role


def check_binding(cfg):
    import cryptalis,test_migration,test_deprotection
    selected=cfg['binding']
    verify_source(selected)
    assert Path(selected['source']).resolve()==TARGET
    assert Path(sys.executable).absolute()==Path(selected['python']).absolute()
    origin=Path(cryptalis.__file__).resolve()
    assert origin.is_relative_to(Path(sys.prefix).resolve())
    verify_package(origin.parent,selected)
    assert Path(test_migration.__file__).resolve()==TARGET/'tests/test_migration.py'
    assert Path(test_deprotection.__file__).resolve()==TARGET/'tests/test_deprotection.py'
    assert all(Path(module.__file__).resolve().is_relative_to(origin.parent)
               for name,module in tuple(sys.modules.items())
               if (name=='cryptalis' or name.startswith('cryptalis.'))
               and getattr(module,'__file__',None))


def test_installed_current_bridge_stage():
    assert '_cryptalis_test_preflight' in sys.modules
    cfg=json.loads(Path(os.environ['CRYPTALIS_BRIDGE_CONFIG']).read_text())
    check_binding(cfg)
    assert os.environ['CRYPTALIS_BRIDGE_MODE'] in ('probe','roundtrip','reject_old_restore')
    if os.environ['CRYPTALIS_BRIDGE_MODE']=='probe':
        return
    owner=engine('CRYPTALIS_TEST_DATABASE_URL')
    if os.environ['CRYPTALIS_BRIDGE_MODE']=='reject_old_restore':
        reverse=d.DeprotectionPlan(Path(cfg['reverse_plan']).read_bytes())
        latest=m.DeploymentPin(reverse.target_id,reverse.operation_id,reverse.digest,'REMOVED')
        try:
            with pytest.raises(m.TransitionFailure):d.check_removed(reverse,owner,pin=latest)
        finally:
            owner.dispose()
            check_binding(cfg)
        return
    with pytest.raises(m.TransitionFailure,match='invalid_plan'):
        m.MigrationPlan(cfg['old_plan'].encode())
    runtime=create_engine('postgresql+psycopg://',creator=lambda:psycopg.connect(plaintext_url()),hide_parameters=True)
    role=psycopg.conninfo.conninfo_to_dict(plaintext_url())['user']
    original_role=psycopg.conninfo.conninfo_to_dict(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL'])['user']
    mapping=registry(metadata=MetaData(schema=cfg['schema']))
    table=Table('customer',mapping.metadata,autoload_with=owner)
    class Customer:pass
    mapping.map_imperatively(Customer,table)
    def native():
        with owner.connect() as c:
            r=c.exec_driver_sql(f'SELECT * FROM "{cfg["schema"]}".customer ORDER BY id')
            return list(r.keys()),r.all()
    before=native();expected={UUID(k):v for k,v in cfg['expected']}
    try:
        proposal=m.plan(json.dumps(cfg['declaration']).encode(),mapping,owner,writers=WriterInventory(True,(Writer(TABLE_ID,'app','sqlalchemy',evidence='single owned synthetic bridge actor; maintenance exclusion'),)),search_reviews=(SearchReview(FIELD_ID,False,'synthetic unbounded names'),),keys=keys,runtime_role=role,target_id=uuid4(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        pin=m.DeploymentPin(proposal.target_id,proposal.operation_id,proposal.digest,'PREPARED')
        approval=m.MaintenanceApproval('owned synthetic actors stopped; existing role handoff reviewed explicitly',3600)
        m.apply(proposal,owner,keys=keys,pin=pin,approval=approval,chunk_size=2,until='PENDING')
        m.apply(proposal,owner,keys=keys,pin=replace(pin,phase='ACTIVATING'),approval=approval,until='ACTIVE')
        active=replace(pin,phase='ACTIVE')
        field=proposal.document['lock']['models'][0]['fields'][0]
        with owner.connect() as c:
            rows=c.exec_driver_sql(f'SELECT id,tenant_id,"{field["payload_column"]}" FROM "{cfg["schema"]}".customer').all()
            oid=c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)::oid',(f'"{cfg["schema"]}".customer',)).scalar_one()
        assert {r:independent_open(bytes(frame) if frame is not None else None,field['descriptor'],t,r) for r,t,frame in rows}==expected
        factory=attach(mapping,runtime,lock=proposal.lock_bytes,keys=keys,deployment=(proposal,active))
        with factory(tenant_id=TENANT) as session:
            assert {r.id:r.name for r in session.scalars(select(Customer))}==expected
        reverse=d.plan(proposal,owner,source_pin=active,keys=keys,plaintext_runtime_role=original_role,backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        rp=m.DeploymentPin(reverse.target_id,reverse.operation_id,reverse.digest,'PREPARED')
        consent=d.PlaintextApproval(reverse.target_id,reverse.operation_id,reverse.digest,True,'explicit synthetic plaintext bridge; retained encrypted legacy dump and independent readers')
        d.apply(reverse,owner,keys=keys,pin=rp,approval=approval,plaintext_approval=consent,until='PLAINTEXT_PENDING')
        # Explicit fixture operator handoff uses two existing roles; no credential or role creation.
        retire_old_role(SimpleNamespace(),reverse)
        d.apply(reverse,owner,keys=keys,pin=replace(rp,phase='PLAINTEXT_ACTIVATING'),approval=approval,plaintext_approval=consent,until='PLAINTEXT_ACTIVE')
        assert native()==before
        info=psycopg.conninfo.conninfo_to_dict(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL'])
        env=dict(os.environ,PGHOST=info['host'],PGPORT=info['port'],PGUSER=info['user'],PGPASSWORD=info['password'],PGDATABASE=info['dbname'])
        worker=TARGET/'tests/deprotection_native_worker.py'
        r=subprocess.run([sys.executable,'-I','-S',str(worker),cfg['schema']],env=env,capture_output=True,text=True,timeout=25)
        assert r.returncode==0,'Package-free current workload failed; diagnostics withheld'
        assert json.loads(r.stdout)['package_absent']
        removal=d.RemovalApproval(reverse.digest,'actual package-free current CRUD/query passed','retained legacy encrypted dump and independently verified same current data',True)
        assert d.remove(reverse,owner,pin=replace(rp,phase='REMOVING'),approval=approval,plaintext_approval=consent,removal_approval=removal).phase=='REMOVED'
        assert native()==before
        with owner.connect() as c:
            final_oid=c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)::oid',(f'"{cfg["schema"]}".customer',)).scalar_one()
        assert final_oid==oid==cfg['oid']
        Path(cfg['reverse_plan']).write_bytes(reverse.artifact)
        Path(cfg['output']).write_text(json.dumps({'binding':cfg['binding'],'same_table_oid':oid==cfg['oid'],'independent_values':len(expected),'phase':'REMOVED','scope':'synthetic maintenance/plaintext bridge; no transparent online upgrade'}))
    finally:
        runtime.dispose();owner.dispose();mapping.dispose()
        check_binding(cfg)

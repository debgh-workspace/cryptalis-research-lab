"""Owned synthetic maintenance bridge; never an automatic artifact upgrade."""
from dataclasses import replace
import json,os,subprocess,sys
from pathlib import Path
from uuid import UUID
import pytest,psycopg
from sqlalchemy import String
LEGACY=Path(__file__).resolve().parents[2]
ROOT=LEGACY.parent
from _bridge_binding import manifest,verify_source
sys.path.insert(0,str(LEGACY/'tests'))
from test_migration import application,keys,independent_open,TENANT
from test_deprotection import prepared,execute,plaintext_url
from cryptalis.sqlalchemy import attach


def native(app):
    with app.owner.connect() as c:
        r=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
        values=(list(r.keys()),[list(row) for row in r.all()])
        columns=c.exec_driver_sql('SELECT a.attname,pg_catalog.format_type(a.atttypid,a.atttypmod),a.attnotnull,co.collname FROM pg_catalog.pg_attribute a LEFT JOIN pg_catalog.pg_collation co ON co.oid=a.attcollation WHERE a.attrelid=pg_catalog.to_regclass(%s) AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum',(f'"{app.schema}".customer',)).all()
        indexes=c.exec_driver_sql('SELECT pg_catalog.pg_get_indexdef(indexrelid) FROM pg_catalog.pg_index WHERE indrelid=pg_catalog.to_regclass(%s) ORDER BY pg_catalog.pg_get_indexdef(indexrelid)',(f'"{app.schema}".customer',)).all()
        return (*values,columns,indexes)


def pg_environment(url):
    i=psycopg.conninfo.conninfo_to_dict(url)
    return dict(os.environ,PGHOST=i['host'],PGPORT=i['port'],PGUSER=i['user'],PGPASSWORD=i['password'],PGDATABASE=i['dbname'])


def package_free(app,env):
    r=subprocess.run([sys.executable,'-I','-S',str(LEGACY/'tests/deprotection_native_worker.py'),app.schema],env=env,capture_output=True,text=True,timeout=25)
    assert r.returncode==0,'Package-free workload failed; diagnostics withheld'
    result=json.loads(r.stdout);assert result['package_absent']
    return {UUID(k):v for k,v in result['rows']}


def current_child(config,mode,log,selected):
    verify_source(selected)
    current=Path(selected['source'])
    env=dict(os.environ,PYTHONPATH=str(current/'tests')+os.pathsep+str(ROOT/'toolchain'),
             CRYPTALIS_BRIDGE_CONFIG=str(config),CRYPTALIS_BRIDGE_MODE=mode,
             CRYPTALIS_BRIDGE_TARGET_SOURCE=str(current))
    env.pop('CRYPTALIS_LAB_PROGRESS',None)
    # Never inherit the legacy PYTHONPATH into this complete installed package.
    child=Path(__file__).with_name('retained_bridge_child.py')
    r=subprocess.run([selected['python'],str(current/'scripts/test_postgres.py'),'--','-q',str(child),'--tb=short'],
                     cwd=current,env=env,capture_output=True,text=True,timeout=90)
    from run_baseline import redact
    log.write_text(redact(r.stdout+r.stderr))
    evidence=Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent
    prefix=log.parent.name+'-'+log.stem
    (evidence/(prefix+'.log')).write_text(log.read_text())
    (evidence/(prefix+'-binding.json')).write_text(json.dumps(selected,indent=2)+'\n')
    verify_source(selected)
    assert r.returncode==0,'Explicit target child failed; inspect retained child log'


@pytest.mark.parametrize('bounded_text',[False,True])
def test_legacy_plaintext_bridge_then_explicit_current_roundtrip(tmp_path,bounded_text,bridge_target):
    import cryptalis
    origin=Path(cryptalis.__file__).resolve()
    assert origin.parent==LEGACY/'src/cryptalis'
    assert manifest(origin.parent)==manifest(LEGACY/'src/cryptalis')
    assert all(Path(module.__file__).resolve().is_relative_to(origin.parent)
               for name,module in tuple(sys.modules.items())
               if (name=='cryptalis' or name.startswith('cryptalis.'))
               and getattr(module,'__file__',None))
    config=tmp_path/'bridge.json'
    config.write_text(json.dumps({'binding':bridge_target}))
    # Validate installed bytes and helper provenance before fixture lifecycle work.
    current_child(config,'probe',tmp_path/'current-probe.log',bridge_target)
    with application(field_type=String(64,collation='C') if bounded_text else None) as app:
        before=native(app)
        with app.owner.connect() as c:
            oid=c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)::oid',(f'"{app.schema}".customer',)).scalar_one()
        d,p,pin,consent=prepared(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with factory(tenant_id=TENANT) as session:
            session.get(app.Customer,UUID(int=105)).name='latest legacy edit 雪'
            session.get(app.Customer,UUID(int=104)).label='public current 雪'*1024
            session.commit()
        expected={k:v[1] for k,v in app.source.items()};expected[UUID(int=105)]='latest legacy edit 雪'
        for row in before[1]:
            if row[0]==UUID(int=105):row[2]=expected[row[0]]
            if row[0]==UUID(int=104):row[3]='public current 雪'*1024
        descriptor=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        with app.owner.connect() as c:
            rows=c.exec_driver_sql(f'SELECT id,tenant_id,name FROM "{app.schema}".customer').all()
        assert {r:independent_open(bytes(frame) if frame is not None else None,descriptor,t,r) for r,t,frame in rows}==expected
        env=pg_environment(os.environ['CRYPTALIS_TEST_DATABASE_URL']);backup=tmp_path/'legacy-protected.sql'
        with backup.open('wb') as out:
            r=subprocess.run(['pg_dump','--schema='+app.schema],env=env,stdout=out,stderr=subprocess.PIPE,timeout=25)
        assert r.returncode==0,'Encrypted backup failed; diagnostics withheld'
        execute(app,d,p,pin,consent)
        execute(app,d,p,replace(pin,phase='PLAINTEXT_ACTIVATING'),consent,'PLAINTEXT_ACTIVE')
        native_env=pg_environment(plaintext_url());assert package_free(app,native_env)==expected
        removal=d.RemovalApproval(p.digest,'actual package-free CRUD/query matched latest synthetic values','encrypted dump retained; independent legacy decoder already matched all current frames; restore checked at end',True)
        assert d.remove(p,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,plaintext_approval=consent,removal_approval=removal).phase=='REMOVED'
        assert package_free(app,native_env)==expected
        assert native(app)==before
        config=tmp_path/'bridge.json'
        config.write_text(json.dumps({'binding':bridge_target,'schema':app.schema,'declaration':app.plan.document['lock']['declaration'],'old_plan':app.plan.artifact.decode(),'oid':oid,'expected':[[str(k),v] for k,v in expected.items()],'output':str(tmp_path/'current-result.json'),'reverse_plan':str(tmp_path/'current-reverse.json')}))
        # Keep this legacy fixture alive; the child has its explicitly selected complete package.
        current_child(config,'roundtrip',tmp_path/'current-roundtrip.log',bridge_target)
        result=json.loads((tmp_path/'current-result.json').read_text())
        assert result['binding']==bridge_target
        assert result['same_table_oid'] and result['independent_values']==len(expected)
        assert result['phase']=='REMOVED' and native(app)==before
        with app.owner.begin() as c:c.exec_driver_sql(f'DROP SCHEMA "{app.schema}" CASCADE')
        r=subprocess.run(['psql','-X','-q','-v','ON_ERROR_STOP=1','-f',str(backup)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=25)
        assert r.returncode==0,'Retained backup restore failed; diagnostics withheld'
        current_child(config,'reject_old_restore',tmp_path/'current-restore-check.log',bridge_target)
        with app.owner.connect() as c:
            rows=c.exec_driver_sql(f'SELECT id,tenant_id,name FROM "{app.schema}".customer').all()
        assert {r:independent_open(bytes(frame) if frame is not None else None,descriptor,t,r) for r,t,frame in rows}==expected

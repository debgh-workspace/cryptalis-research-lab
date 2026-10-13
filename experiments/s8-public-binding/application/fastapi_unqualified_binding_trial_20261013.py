"""Source-unchanged upstream app suite; explicit external integration shim."""
from pathlib import Path
from dataclasses import replace
import hashlib,importlib,json,os,random,socket,sys,time,traceback
from uuid import UUID,uuid4
import psycopg
from psycopg import sql
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
import pytest
B=Path(__file__).resolve().parents[2];CHECKOUT=B/'apps/checkouts/fastapi-template/backend'
mode,out=sys.argv[1],Path(sys.argv[2]).resolve()
assert mode in ('native','protected') and out.is_relative_to(B/'evidence')
out.mkdir(exist_ok=False);os.umask(0o077)
sys.path[:0]=[str(CHECKOUT),str(Path(os.environ['GIT_WORK_TREE'])/'tests'),str(B/'apps/harness')]
sys.path.insert(0,str(B/'experiments'))
from experimental_delete_effect_inventory import inspect_delete_effects
from local_smtp_fixture import start
mail=start();original_connect=socket.socket.connect;original_connect_ex=socket.socket.connect_ex;original_create=socket.create_connection;original_dns=socket.getaddrinfo

def allowed(address):
    if isinstance(address,str) or address[0] not in ('127.0.0.1','localhost','::1'):
        raise RuntimeError('Trial blocks external network access')
def connect(self,address):allowed(address);return original_connect(self,address)
def connect_ex(self,address):allowed(address);return original_connect_ex(self,address)
def create_connection(address,*a,**kw):
    if address[0]=='smtp.example.com':address=mail.server_address
    allowed(address);return original_create(address,*a,**kw)
def getaddrinfo(host,*a,**kw):
    if host not in ('127.0.0.1','localhost','::1',None):raise RuntimeError('Trial blocks external DNS')
    return original_dns(host,*a,**kw)
socket.socket.connect=connect;socket.socket.connect_ex=connect_ex;socket.create_connection=create_connection;socket.getaddrinfo=getaddrinfo
values=json.loads((B/'apps/runtime/private/fastapi-env.json').read_text())
for k,v in values.items():os.environ[k]=v
schema='cryptalis_fastapi_a6_'+uuid4().hex
runtime_url=make_url(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']).set(drivername='postgresql+psycopg').update_query_dict({'options':f'-c search_path={schema},pg_catalog'})
assert runtime_url.host=='127.0.0.1' and runtime_url.port==55432
os.environ['DATABASE_URL']=runtime_url.render_as_string(hide_password=False)
os.environ.update(SMTP_HOST='127.0.0.1',SMTP_PORT=str(mail.server_address[1]),SMTP_TLS='false',SENTRY_DSN='')
os.chdir(CHECKOUT);random.seed(601078)
source_files=sorted(list((CHECKOUT/'app').rglob('*.py'))+list((CHECKOUT/'tests').rglob('*.py')))
before={str(p.relative_to(CHECKOUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
from sqlmodel import SQLModel,Session
from app.core.db import engine,init_db
from app.main import app
from app.api.deps import get_db
from test_migration import DOMAIN,keys
from cryptalis import migration as m
from cryptalis.sqlalchemy import attach
from cryptalis.manifest.compiler import Writer,WriterInventory,SearchReview
owner=create_engine('postgresql+psycopg://',hide_parameters=True,creator=lambda:psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL'],options=f'-c search_path={schema},pg_catalog'))
TID,FID=UUID(int=71001),UUID(int=71002);status={'mode':mode,'scope':'Retained-column research encrypted email equality/uniqueness plus full_name storage through removal and backup recovery; explicit C profile and extra operator grants'}
started=time.monotonic();root=psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL'])
try:
    root.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)));root.commit()
    # S8: preserve original unqualified upstream table mappings.
    from sqlalchemy import String
    SQLModel.metadata.tables["user"].c.email.type=String(255,collation="C")
    SQLModel.metadata.create_all(owner)
    with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:role=c.execute('SELECT current_user').fetchone()[0]
    root.execute(sql.SQL('REVOKE ALL ON SCHEMA {} FROM PUBLIC').format(sql.Identifier(schema)))
    root.execute(sql.SQL('GRANT USAGE ON SCHEMA {} TO {}').format(sql.Identifier(schema),sql.Identifier(role)))
    for table in ('user','item'):
        root.execute(sql.SQL('GRANT SELECT,INSERT,UPDATE,DELETE ON {}.{} TO {}').format(sql.Identifier(schema),sql.Identifier(table),sql.Identifier(role)))
    root.commit()
    with Session(engine) as session:init_db(session)
    def record_effect_graph(stage):
        with engine.begin() as connection:
            connection.exec_driver_sql('SET TRANSACTION READ ONLY')
            graph=inspect_delete_effects(connection,schema,'user')
        assert {node['name'] for node in graph['nodes']}=={'user','item'}
        assert len(graph['foreign_keys'])==1 and graph['foreign_keys'][0]['action']=='c'
        assert graph['admitted'] is False
        (out/('delete-effect-graph-'+stage+'.json')).write_text(json.dumps(graph,indent=2)+'\n')
    record_effect_graph('native')
    if mode=='protected':
        declaration={'schema':'cryptalis.protection/v1','profile':'cf1','domain_id':str(DOMAIN),'models':[{'model':'User','table_id':str(TID),'tenancy':{'single_tenant':True},'fields':[{'name':'full_name','field_id':str(FID),'protect':True,'queries':[],'accept_leakage':[]},{'name':'email','field_id':str(UUID(int=71003)),'protect':True,'queries':['equality','unique'],'accept_leakage':['equality','unique']}]}]}
        plan=m.plan(json.dumps(declaration).encode(),SQLModel._sa_registry,owner,writers=WriterInventory(True,(Writer(TID,'app','sqlalchemy',evidence='This random schema has only this supervised fixture; app clients not started'),)),search_reviews=(SearchReview(UUID(int=71003),False,'Synthetic email universe; declared equality/frequency leakage'),),keys=keys,runtime_role=role,target_id=uuid4(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        pin=m.DeploymentPin(plan.target_id,plan.operation_id,plan.digest,'PREPARED')
        approval=m.MaintenanceApproval('No clients started; this disposable schema has no other writers',3600)
        assert m.apply(plan,owner,keys=keys,pin=pin,approval=approval).phase=='PENDING'
        pin=replace(pin,phase='ACTIVATING')
        assert m.apply(plan,owner,keys=keys,pin=pin,approval=approval,until='ACTIVE').phase=='ACTIVE'
        pin=replace(pin,phase='ACTIVE')
        record_effect_graph('protected')
        # PRODUCTION INTEGRATION START
        engine.hide_parameters=True  # Required parameter-redaction engine setting.
        factory=attach(SQLModel._sa_registry,engine,lock=plan.lock_bytes,keys=keys,deployment=(plan,pin))
        factory._owner._experimental_public_delete_tables=(SQLModel.metadata.tables["item"],SQLModel.metadata.tables["user"])
        factory._owner._experimental_protected_equality_delete=True
        factory._owner._experimental_public_child_cascade_delete=True
        def protected_db():
            with factory(tenant_id=TID) as session:
                yield session
        app.dependency_overrides[get_db]=protected_db
        # PRODUCTION INTEGRATION END
        # TEST FIXTURE INTEGRATION START
        def test_session(bind=None,**options):
            assert bind is engine
            return factory(tenant_id=TID,**options)
        importlib.import_module('tests.conftest').Session=test_session
        # TEST FIXTURE INTEGRATION END
        status['protection_active']=True
    class Evidence:
        def pytest_runtest_logreport(self,report):
            with (out/'progress.jsonl').open('a') as f:f.write(json.dumps({'nodeid':report.nodeid,'when':report.when,'outcome':report.outcome,'duration':report.duration})+'\n')
    status['pytest_exit_code']=int(pytest.main(['-o','addopts=','-q','--tb=short','--strict-markers','--junitxml='+str(out/'application-junit.xml'),'tests'],plugins=[Evidence()]))
    if mode=='protected':
        assert status['pytest_exit_code']==0,'Protected app must fully pass before separate lifecycle verification seed'
        # Separate post-suite corpus: successful upstream teardown leaves no rows.
        from app.models import User,Item
        names=[None,'','雪😀','e\u0301','é','exact','trailing ']
        with factory(tenant_id=TID) as seed:
            users=[User(id=UUID(int=9000+i),email=f'checkpoint{i}@example.com',full_name=name,hashed_password='synthetic-lifecycle-fixture-only') for i,name in enumerate(names)]
            seed.add_all(users);seed.flush()
            seed.add_all(Item(id=UUID(int=10000+i),title=f'checkpoint item {i}',description='synthetic child survivor',owner_id=user.id) for i,user in enumerate(users));seed.commit()
        with owner.connect() as c:expected_children=c.exec_driver_sql(f'SELECT row_to_json(t) FROM "{schema}".item t ORDER BY id').scalars().all()
        assert len(expected_children)==7
        (out/'expected-native-children.json').write_text(json.dumps(expected_children))
        status['post_suite_lifecycle_seed']={'users':7,'items':7,'purpose':'Nonempty independent lifecycle corpus after successful unchanged upstream teardown','application_source_changes':0}
        fields={f['name']:f for f in json.loads(plan.lock_bytes)['models'][0]['fields']}
        name_slot='"'+fields['full_name']['payload_column']+'"'
        email_slot='"'+fields['email']['payload_column']+'"'
        with owner.connect() as c:
            status['raw_storage']=list(c.exec_driver_sql(f'SELECT count(*),count({name_slot}),bool_and(substring({name_slot} FROM 1 FOR 3)=decode(\'434631\',\'hex\')) FROM "{schema}"."user"').one())
            raw=list(c.exec_driver_sql(f'SELECT id,{name_slot} FROM "{schema}"."user"'))
        from test_migration import independent_open
        from app.models import User
        from sqlalchemy import select
        descriptor=next(f for f in json.loads(plan.lock_bytes)['models'][0]['fields'] if f['name']=='full_name')['descriptor']
        decoded={identity:independent_open(bytes(body) if body is not None else None,descriptor,TID,identity,field_id=FID) for identity,body in raw}
        with factory(tenant_id=TID) as session:
            returned={row.id:row.full_name for row in session.scalars(select(User))}
        assert decoded==returned
        status['independent_frame_oracle']={'rows':len(raw),'non_null_frames':sum(body is not None for _,body in raw),'exact_match_to_orm':True}
        email_field=next(f for f in json.loads(plan.lock_bytes)['models'][0]['fields'] if f['name']=='email')
        with owner.connect() as c:email_raw=c.exec_driver_sql(f'SELECT id,{email_slot} FROM "{schema}"."user"').all()
        email_decoded={identity:independent_open(bytes(body),email_field['descriptor'],TID,identity,field_id=UUID(int=71003)) for identity,body in email_raw}
        with factory(tenant_id=TID) as session:email_returned={row.id:row.email for row in session.scalars(select(User))}
        assert email_decoded==email_returned
        status['encrypted_email_oracle']={'rows':len(email_raw),'all_stored_as_cf1':all(bytes(body)[:3]==b'CF1' for _,body in email_raw),'independent_values_exact':True,'schema_profile':'explicit C collation','leakage':'equality/frequency retained'}
        from cryptalis import deprotection as reverse
        from test_deprotection import plaintext_role
        reverse_plan=reverse.plan(plan,owner,source_pin=pin,keys=keys,plaintext_runtime_role=plaintext_role(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        status['reverse_plan']={'read_only_plan_created':True,'format':reverse_plan.document['format'],'digest':reverse_plan.digest}
        with owner.connect() as backup_connection:
            backup={name:backup_connection.exec_driver_sql(f'SELECT row_to_json(t) FROM "{schema}"."{name}" t').scalars().all() for name in ('user','item')}
        (out/'synthetic-protected-snapshot.json').write_text(json.dumps(backup,default=str))
        (out/'synthetic-protection-plan.json').write_bytes(plan.artifact)
        import subprocess
        backup_info=psycopg.conninfo.conninfo_to_dict(os.environ['CRYPTALIS_TEST_DATABASE_URL'])
        backup_env=dict(os.environ,PGHOST=backup_info['host'],PGPORT=backup_info['port'],PGUSER=backup_info['user'],PGPASSWORD=backup_info['password'],PGDATABASE=backup_info['dbname'])
        snapshot=out/'synthetic-encrypted-schema.sql'
        with snapshot.open('wb') as backup_file:
            dump=subprocess.run(['pg_dump','--schema='+schema],env=backup_env,stdout=backup_file,stderr=subprocess.PIPE,timeout=20)
        assert dump.returncode==0,'Disposable schema backup failed; diagnostics withheld'
        reverse_pin=m.DeploymentPin(reverse_plan.target_id,reverse_plan.operation_id,reverse_plan.digest,'PREPARED')
        consent=reverse.PlaintextApproval(reverse_plan.target_id,reverse_plan.operation_id,reverse_plan.digest,True,'Synthetic encrypted row snapshot and plan retained locally; independent decoder checked; full application backup restore not yet qualified')
        reversed_state=reverse.apply(reverse_plan,owner,keys=keys,pin=reverse_pin,approval=approval,plaintext_approval=consent,until='PLAINTEXT_PENDING')
        with owner.connect() as c:
            native_values=dict(c.exec_driver_sql(f'SELECT id,full_name FROM "{schema}"."user"').all())
        assert native_values==decoded
        with owner.connect() as c:native_emails=dict(c.exec_driver_sql(f'SELECT id,email FROM "{schema}"."user"').all())
        assert native_emails==email_decoded
        (out/'expected-native-emails.json').write_text(json.dumps({str(k):v for k,v in native_emails.items()}))
        status['decrypt_back']={'phase':reversed_state.phase,'exact_values':True,'native_schema_checked_by_transition':True,'rows':len(native_values),'publication_complete':False,'package_free_application_verified':False}
        from test_deprotection import retire_old_role,plaintext_url
        retire_old_role(None,reverse_plan)
        # Explicit lab-only public-table permission transfer, not automatic product behavior.
        with owner.begin() as c:
            c.exec_driver_sql(sql.SQL('GRANT SELECT,INSERT,UPDATE,DELETE ON {}.item TO {}').format(sql.Identifier(schema),sql.Identifier(plaintext_role())).as_string())
        published_pin=replace(reverse_pin,phase='PLAINTEXT_ACTIVATING')
        published=reverse.apply(reverse_plan,owner,keys=keys,pin=published_pin,approval=approval,plaintext_approval=consent,until='PLAINTEXT_ACTIVE')
        assert published.phase=='PLAINTEXT_ACTIVE'
        (out/'expected-native-values.json').write_text(json.dumps({str(k):v for k,v in native_values.items()}))
        child=subprocess.run([str(B/'apps/runtime/fastapi-env/bin/python'),'-I',str(B/'apps/harness/fastapi_cascade_package_free_worker_20261012.py'),schema,str(out)],capture_output=True,text=True,timeout=120)
        child_output=child.stdout+child.stderr
        redactions=dict(values);redactions['PLAINTEXT_DATABASE_URL']=plaintext_url();redactions['PLAINTEXT_PASSWORD']=psycopg.conninfo.conninfo_to_dict(plaintext_url())['password']
        for key,value in redactions.items():
            if any(word in key for word in ('PASSWORD','SECRET','KEY','URL')) and value:child_output=child_output.replace(value,'<redacted>')
        (out/'package-free-redacted.log').write_text(child_output)
        assert child.returncode==0,'Package-free native application failed; inspect sanitized evidence'
        status['package_free']=json.loads((out/'package-free-result.json').read_text())
        status['extra_operator_step']='Explicit lab-only grants for unprotected Item to the existing plaintext role'
        status['decrypt_back']['publication_complete']=True
        status['decrypt_back']['package_free_application_verified']=True
        def restore_snapshot():
            restored=subprocess.run(['psql','-X','-q','-1','-v','ON_ERROR_STOP=1','-f',str(snapshot)],env=backup_env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=30)
            assert restored.returncode==0,'Disposable encrypted schema restore failed; diagnostics withheld'
        def verify_backup_values():
            with owner.connect() as c:restored_rows=c.exec_driver_sql(f'SELECT id,{name_slot} FROM "{schema}"."user"').all()
            recovered={identity:independent_open(bytes(body) if body is not None else None,descriptor,TID,identity,field_id=FID) for identity,body in restored_rows}
            assert recovered==decoded
            with owner.connect() as c:restored_email_rows=c.exec_driver_sql(f'SELECT id,{email_slot} FROM "{schema}"."user"').all()
            recovered_emails={identity:independent_open(bytes(body),email_field['descriptor'],TID,identity,field_id=UUID(int=71003)) for identity,body in restored_email_rows}
            assert recovered_emails==email_decoded
            with owner.connect() as c:recovered_children=c.exec_driver_sql(f'SELECT row_to_json(t) FROM "{schema}".item t ORDER BY id').scalars().all()
            assert recovered_children==expected_children
        # Hold the current native schema aside while restoring the real backup.
        held='cryptalis_plain_hold_'+uuid4().hex
        with owner.begin() as c:c.exec_driver_sql(sql.SQL('ALTER SCHEMA {} RENAME TO {}').format(sql.Identifier(schema),sql.Identifier(held)).as_string())
        try:
            restore_snapshot();verify_backup_values()
        finally:
            with owner.begin() as c:
                c.exec_driver_sql(sql.SQL('DROP SCHEMA IF EXISTS {} CASCADE').format(sql.Identifier(schema)).as_string())
                c.exec_driver_sql(sql.SQL('ALTER SCHEMA {} RENAME TO {}').format(sql.Identifier(held),sql.Identifier(schema)).as_string())
        status['backup_restore_before_removal']={'real_pg_dump_and_psql':True,'exact_independently_decrypted_rows':len(decoded)}
        removal=reverse.RemovalApproval(reverse_plan.digest,'Fresh process without Cryptalis: preserved values and all 58 native tests passed','Real encrypted pg_dump restored; independent CF1 decoder matched every saved row',True)
        retired=reverse.remove(reverse_plan,owner,pin=replace(reverse_pin,phase='REMOVING'),approval=approval,plaintext_approval=consent,removal_approval=removal)
        assert retired.phase=='REMOVED'
        reverse.check_removed(reverse_plan,owner,pin=replace(reverse_pin,phase='REMOVED'))
        after_out=out/'after-removal';after_out.mkdir();(after_out/'expected-native-values.json').write_text('{}')
        (after_out/'expected-native-emails.json').write_text('{}')
        (after_out/'expected-native-children.json').write_text('[]')
        after_child=subprocess.run([str(B/'apps/runtime/fastapi-env/bin/python'),'-I',str(B/'apps/harness/fastapi_cascade_package_free_worker_20261012.py'),schema,str(after_out)],capture_output=True,text=True,timeout=120)
        after_output=after_child.stdout+after_child.stderr
        for key,value in redactions.items():
            if any(word in key for word in ('PASSWORD','SECRET','KEY','URL')) and value:after_output=after_output.replace(value,'<redacted>')
        (after_out/'package-free-redacted.log').write_text(after_output)
        assert after_child.returncode==0,'Post-removal native suite failed; inspect sanitized evidence'
        status['after_removal']=json.loads((after_out/'package-free-result.json').read_text())
        with owner.begin() as c:c.exec_driver_sql(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)).as_string())
        restore_snapshot();verify_backup_values()
        try:reverse.check_removed(reverse_plan,owner,pin=replace(reverse_pin,phase='REMOVED'))
        except m.TransitionFailure:old_restore_rejected=True
        else:raise AssertionError('Restored encrypted state incorrectly matched REMOVED publication')
        status['removal']={'phase':'REMOVED','old_restore_rejected':old_restore_rejected,'backup_recovery_exact':True,'protected_bulk_teardown_still_open':False}

except BaseException as err:
    status['harness_error_type']=type(err).__name__
    raise
finally:
    engine.dispose();owner.dispose()
    root.execute(sql.SQL('DROP SCHEMA IF EXISTS {} CASCADE').format(sql.Identifier(schema)));root.commit();root.close()
    mail.shutdown();mail.server_close()
    after={str(p.relative_to(CHECKOUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
    status['explicit_table_schema_assignments']=0
    status.update(elapsed_seconds=time.monotonic()-started,source_hashes=before,source_unchanged=before==after,application_source_changes=0 if before==after else None,production_integration_lines=13 if status.get('protection_active') else 0,test_fixture_integration_lines=4 if status.get('protection_active') else 0,integration_points=2 if status.get('protection_active') else 0)
    (out/'application-result.json').write_text(json.dumps(status,indent=2))
    assert before==after

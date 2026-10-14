"""Current-data native PostgreSQL oracles for approved offline deprotection."""
from dataclasses import replace
import importlib
import json
from uuid import UUID
import pytest
from sqlalchemy import select
from test_migration import application, run, publish, keys, TENANT, engine
from cryptalis.migration import DeploymentPin, TransitionFailure
from cryptalis.sqlalchemy import attach


def api():
    return importlib.import_module('cryptalis.deprotection')


def ciphertext_column(app):
    # Fixed field identity from the independent fixture, not a discovered
    # arbitrary bytea column that could mask missing or misplaced data.
    from test_migration import FIELD_ID
    if app.plan.document['format'] in (
            'cryptalis.transition/retained-native-research-v0',
            'cryptalis.transition/retained-native-comments-research-v1'):
        return '_cryptalis_'+FIELD_ID.hex
    raise AssertionError('fixture requires an exact admitted retained-native format')


def assert_encrypted_storage(c,app):
    payload=ciphertext_column(app)
    assert c.exec_driver_sql('SELECT data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s',(app.schema,'customer',payload)).scalar_one()=='bytea'
    if payload!='name':
        assert c.exec_driver_sql('SELECT data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s',(app.schema,'customer','name')).scalar_one()=='text'
        assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".customer WHERE name IS NOT NULL').scalar_one()==0


def plaintext_url():
    from pathlib import Path
    return (Path.home()/'.cryptalis-writer-url').read_text().strip()


def plaintext_role():
    from psycopg.conninfo import conninfo_to_dict
    return conninfo_to_dict(plaintext_url())['user']


def retire_old_role(app,p):
    """Explicit authorized lab operator step; product prints and never executes."""
    from pathlib import Path
    import os,psycopg
    from psycopg.conninfo import conninfo_to_dict
    options=conninfo_to_dict(os.environ['CRYPTALIS_TEST_DATABASE_URL'])
    assert options['host']=='127.0.0.1' and str(options['port'])=='55432'
    options.update(user='lab_admin',password=(Path.home()/'admin-password').read_text().strip())
    with psycopg.connect(**options,autocommit=True) as admin:
        admin.execute(p.cutover_procedure(create_role=False))


def prepared(app):
    run(app); publish(app)
    d=api()
    p=d.plan(app.plan,app.owner,source_pin=app.pin,keys=keys,plaintext_runtime_role=plaintext_role(),
             backfill_rows_per_second=1000,verify_rows_per_second=1000,
             temporary_bytes_per_row=700,wal_bytes_per_row=2000)
    pin=DeploymentPin(p.target_id,p.operation_id,p.digest,'PREPARED')
    consent=d.PlaintextApproval(p.target_id,p.operation_id,p.digest,True,
        'Synthetic retained backup and public fixture reader retained by test operator')
    return d,p,pin,consent


def execute(app,d,p,pin,consent,until='PLAINTEXT_PENDING',**kw):
    if until=='PLAINTEXT_ACTIVE':retire_old_role(app,p)
    return d.apply(p,app.owner,keys=keys,pin=pin,approval=app.approval,
                   plaintext_approval=consent,until=until,chunk_size=2,**kw)


def test_reverse_plan_is_read_only_and_binds_active_source():
    with application() as app:
        d,p,pin,consent=prepared(app)
        assert p.document['source_pin']['phase']=='ACTIVE'
        assert p.document['source_pin']['plan_digest']==app.plan.digest
        expected = {
            'cryptalis.transition/retained-native-research-v0': 'cryptalis.reverse/retained-native-research-v0',
            'cryptalis.transition/retained-native-comments-research-v1': 'cryptalis.reverse/retained-native-comments-research-v1',
        }[app.plan.document['format']]
        assert p.document['format']==expected
        with app.owner.connect() as c:
            assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}"._cryptalis_journal').scalar_one()==1
            assert_encrypted_storage(c,app)


def test_current_edits_and_native_values_survive_reverse_switch():
    with application() as app:
        d,p,pin,consent=prepared(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        expected={k:v[1] for k,v in app.source.items()}
        with factory(tenant_id=TENANT) as s:
            s.get(app.Customer,UUID(int=105)).name='edited after protection 雪'
            s.commit()
        expected[UUID(int=105)]='edited after protection 雪'
        assert execute(app,d,p,pin,consent).phase=='PLAINTEXT_PENDING'
        activating=replace(pin,phase='PLAINTEXT_ACTIVATING')
        assert execute(app,d,p,activating,consent,'PLAINTEXT_ACTIVE').phase=='PLAINTEXT_ACTIVE'
        import psycopg
        from sqlalchemy import create_engine
        native=create_engine('postgresql+psycopg://',creator=lambda:psycopg.connect(plaintext_url()))
        with native.connect() as c:
            observed=dict(c.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".customer').all())
            assert observed==expected
            assert c.exec_driver_sql("SELECT data_type FROM information_schema.columns WHERE table_schema=%s AND column_name='name'",(app.schema,)).scalar_one()=='text'
        # Retired attached sessions cannot silently interpret plaintext as frames.
        from cryptalis.crypto import CryptoFailure
        from sqlalchemy.exc import SQLAlchemyError
        with pytest.raises((CryptoFailure,SQLAlchemyError)):
            with factory(tenant_id=TENANT) as s:s.scalar(select(app.Customer.name))


@pytest.mark.parametrize('change',['absent','wrong_operation','no_consent','no_backup'])
def test_plaintext_approval_refuses_before_staging(change):
    with application() as app:
        d,p,pin,a=prepared(app)
        if change=='absent':a=None
        if change=='wrong_operation':a=replace(a,operation_id=UUID(int=9999))
        if change=='no_consent':a=replace(a,accept_plaintext_at_rest=False)
        if change=='no_backup':a=replace(a,retained_backup_recovery='')
        with pytest.raises(TransitionFailure,match='plaintext_approval_required'):
            execute(app,d,p,pin,a,'EXPANDED')
        with app.owner.connect() as c:
            assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}"._cryptalis_journal').scalar_one()==1


@pytest.mark.parametrize('phase',['EXPANDED','BACKFILLED','VERIFIED','PLAINTEXT_PENDING'])
def test_runtime_writes_remain_fenced_until_publication(phase):
    import psycopg,os
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a,phase)
        with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:
            with pytest.raises(psycopg.Error) as error:
                c.execute(f'UPDATE "{app.schema}".customer SET label=%s',('unpublished',))
            assert error.value.sqlstate=='55000'
        with pytest.raises(TransitionFailure):app.m.check_deployment(app.plan,app.owner,pin=app.pin)


@pytest.mark.parametrize('change',['staging','frame','membership','fence','generation'])
def test_changed_verified_data_never_switches(change):
    from test_migration import FIELD_ID
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a,'VERIFIED')
        col='_cryptalis_'+FIELD_ID.hex+'_plain'
        payload=ciphertext_column(app)
        with app.owner.begin() as c:
            if change=='staging':c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{col}"=%s WHERE id=%s',('different',UUID(int=102)))
            if change=='frame':c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{payload}"=set_byte("{payload}",octet_length("{payload}")-1,get_byte("{payload}",octet_length("{payload}")-1)#1) WHERE id=%s',(UUID(int=102),))
            if change=='membership':c.exec_driver_sql(f'DELETE FROM "{app.schema}".customer WHERE id=%s',(UUID(int=102),))
            if change=='fence':c.exec_driver_sql(f'ALTER TABLE "{app.schema}".customer DISABLE TRIGGER ALL')
            if change=='generation':c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{payload}"=set_byte("{payload}",9,2) WHERE id=%s',(UUID(int=102),))
        with pytest.raises(TransitionFailure):execute(app,d,p,pin,a)
        with app.owner.connect() as c:
            assert_encrypted_storage(c,app)
            state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',(p.operation_id,)).scalar_one()
            assert state['phase']=='VERIFIED'


@pytest.mark.parametrize('phase',['EXPANDED','BACKFILLED','VERIFIED','PLAINTEXT_PENDING','PLAINTEXT_ACTIVE'])
def test_resume_each_committed_reverse_phase(phase):
    with application() as app:
        d,p,pin,a=prepared(app)
        if phase=='PLAINTEXT_ACTIVE':
            execute(app,d,p,pin,a)
            pin=replace(pin,phase='PLAINTEXT_ACTIVATING')
        execute(app,d,p,pin,a,phase)
        # Reconstruct artifact, not a mutable in-memory continuation.
        fresh=d.DeprotectionPlan(p.artifact)
        if phase!='PLAINTEXT_ACTIVE':execute(app,d,fresh,pin,a)
        execute(app,d,fresh,replace(pin,phase='PLAINTEXT_ACTIVATING'),a,'PLAINTEXT_ACTIVE')
        with app.owner.connect() as c:
            assert dict(c.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".customer').all())=={k:v[1] for k,v in app.source.items()}


@pytest.mark.parametrize('wrong',['operation','target','digest','unknown_phase','stale_phase'])
def test_reverse_pin_rejects_wrong_or_restored_state(wrong):
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a,'EXPANDED')
        if wrong=='operation':pin=replace(pin,operation_id=UUID(int=123))
        if wrong=='target':pin=replace(pin,target_id=UUID(int=123))
        if wrong=='digest':pin=replace(pin,plan_digest='f'*64)
        if wrong=='unknown_phase':pin=replace(pin,phase='FUTURE')
        if wrong=='stale_phase':pin=replace(pin,phase='PLAINTEXT_ACTIVE')
        with pytest.raises(TransitionFailure):execute(app,d,p,pin,a)


def test_pending_requires_explicit_external_publication():
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a)
        with pytest.raises(TransitionFailure,match='matching_plaintext_publication_required'):
            execute(app,d,p,pin,a,'PLAINTEXT_ACTIVE')


def test_abort_before_switch_restores_current_protected_application():
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a,'BACKFILLED')
        result=d.abort(p,app.owner,pin=pin,approval=app.approval,plaintext_approval=a)
        assert result.phase=='ABORTED'
        app.m.check_deployment(app.plan,app.owner,pin=app.pin)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with factory(tenant_id=TENANT) as s:
            assert {r.id:r.name for r in s.scalars(select(app.Customer))}=={k:v[1] for k,v in app.source.items()}
        with pytest.raises(TransitionFailure):execute(app,d,p,pin,a)


def test_remove_requires_proofs_and_retires_only_owned_metadata():
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a)
        execute(app,d,p,replace(pin,phase='PLAINTEXT_ACTIVATING'),a,'PLAINTEXT_ACTIVE')
        removal=d.RemovalApproval(p.digest,'executed native workload receipt','executed retained-backup receipt',True)
        with pytest.raises(TransitionFailure):
            d.remove(p,app.owner,pin=replace(pin,phase='PLAINTEXT_ACTIVE'),approval=app.approval,plaintext_approval=a,removal_approval=removal)
        with pytest.raises(TransitionFailure):
            d.remove(p,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,plaintext_approval=a,removal_approval=None)
        result=d.remove(p,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,plaintext_approval=a,removal_approval=removal)
        assert result.phase=='REMOVED'
        d.check_removed(p,app.owner,pin=replace(pin,phase='REMOVED'))
        # Idempotent acknowledgement after commit loss uses the same external pin.
        assert d.remove(p,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,plaintext_approval=a,removal_approval=removal).phase=='REMOVED'


def worker(app,p,tmp_path,phase,pin_phase='PREPARED',mode='exit'):
    import subprocess,sys
    from pathlib import Path
    artifact=tmp_path/'reverse.json';artifact.write_bytes(p.artifact)
    return subprocess.Popen([sys.executable,str(Path(__file__).with_name('deprotection_worker.py')),
        str(artifact),phase,pin_phase,mode],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)


@pytest.mark.parametrize('phase',['EXPANDED','BACKFILLED','VERIFIED','PLAINTEXT_PENDING','PLAINTEXT_ACTIVE'])
def test_sigkill_each_phase_and_independent_resume(phase,tmp_path):
    import signal
    with application() as app:
        d,p,pin,a=prepared(app)
        pin_phase='PREPARED'
        if phase=='PLAINTEXT_ACTIVE':
            execute(app,d,p,pin,a);retire_old_role(app,p);pin_phase='PLAINTEXT_ACTIVATING'
        process=worker(app,p,tmp_path,phase,pin_phase,'pause')
        try:
            assert process.stdout.readline().strip()==phase
            process.kill();assert process.wait(timeout=10)==-signal.SIGKILL
            resumed=worker(app,p,tmp_path,'PLAINTEXT_ACTIVE' if phase=='PLAINTEXT_ACTIVE' else 'PLAINTEXT_PENDING',pin_phase)
            stdout,stderr=resumed.communicate(timeout=20)
            assert resumed.returncode==0,stderr
            assert stdout.strip()==('PLAINTEXT_ACTIVE' if phase=='PLAINTEXT_ACTIVE' else 'PLAINTEXT_PENDING')
            with app.owner.connect() as c:
                assert dict(c.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".customer').all())=={k:v[1] for k,v in app.source.items()}
        finally:
            if process.poll() is None:process.kill();process.wait(timeout=10)


def test_sigkill_uncommitted_second_batch_preserves_exact_prefix(tmp_path):
    import signal
    from test_migration import FIELD_ID,TABLE_ID
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a,'EXPANDED')
        process=worker(app,p,tmp_path,'PLAINTEXT_PENDING',mode='kill_second_chunk')
        process.communicate(timeout=20);assert process.returncode==-signal.SIGKILL
        with app.owner.connect() as c:
            state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',(p.operation_id,)).scalar_one()
            assert state['models'][str(TABLE_ID)]['rows']==2
            assert state['models'][str(TABLE_ID)]['chunks']==1
            # First row is NULL; use cursor and exact staged values, not COUNT(non-NULL).
            rows=c.exec_driver_sql(f'SELECT id,"_cryptalis_{FIELD_ID.hex}_plain" FROM "{app.schema}".customer ORDER BY id').all()
            assert [r[1] for r in rows]==[None,'',None,None,None,None,None]
        execute(app,d,p,pin,a)


def test_package_free_workload_backup_recovery_and_old_restore_rejection(tmp_path):
    import os,subprocess,sys,psycopg
    from pathlib import Path
    from test_migration import independent_open
    with application() as app:
        d,p,pin,a=prepared(app)
        # Retain a real encrypted PostgreSQL schema backup, never a plaintext copy.
        info=psycopg.conninfo.conninfo_to_dict(os.environ['CRYPTALIS_TEST_DATABASE_URL'])
        env=dict(os.environ,PGHOST=info['host'],PGPORT=info['port'],PGUSER=info['user'],PGPASSWORD=info['password'],PGDATABASE=info['dbname'])
        runtime_info=psycopg.conninfo.conninfo_to_dict(plaintext_url())
        native_env=dict(os.environ,PGHOST=runtime_info['host'],PGPORT=runtime_info['port'],PGUSER=runtime_info['user'],PGPASSWORD=runtime_info['password'],PGDATABASE=runtime_info['dbname'])
        snapshot=tmp_path/'protected.sql'
        with snapshot.open('wb') as out:
            r=subprocess.run(['pg_dump','--schema='+app.schema],env=env,stdout=out,stderr=subprocess.PIPE,timeout=20)
        assert r.returncode==0,'Backup failed; diagnostics withheld'
        execute(app,d,p,pin,a)
        execute(app,d,p,replace(pin,phase='PLAINTEXT_ACTIVATING'),a,'PLAINTEXT_ACTIVE')
        r=subprocess.run([sys.executable,'-I','-S',str(Path(__file__).with_name('deprotection_native_worker.py')),app.schema],env=native_env,capture_output=True,text=True,timeout=20)
        assert r.returncode==0,r.stderr
        result=json.loads(r.stdout);assert result['package_absent']
        assert {UUID(k):v for k,v in result['rows']}=={k:v[1] for k,v in app.source.items()}
        removal=d.RemovalApproval(p.digest,'package-free child CRUD/query passed','retained schema backup and deterministic fixture reader',True)
        d.remove(p,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,plaintext_approval=a,removal_approval=removal)
        d.check_removed(p,app.owner,pin=replace(pin,phase='REMOVED'))
        r=subprocess.run([sys.executable,'-I','-S',str(Path(__file__).with_name('deprotection_native_worker.py')),app.schema],env=native_env,capture_output=True,text=True,timeout=20)
        assert r.returncode==0,r.stderr
        with app.owner.begin() as c:c.exec_driver_sql(f'DROP SCHEMA "{app.schema}" CASCADE')
        r=subprocess.run(['psql','-X','-q','-v','ON_ERROR_STOP=1','-f',str(snapshot)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=20)
        assert r.returncode==0,'Restore failed; diagnostics withheld'
        with pytest.raises(TransitionFailure):d.check_removed(p,app.owner,pin=replace(pin,phase='REMOVED'))
        # Independent CF1 framing/HKDF decoder, not deprotection's own transform.
        descriptor=p.document['lock']['models'][0]['fields'][0]['descriptor']
        payload=ciphertext_column(app)
        with app.owner.connect() as c:
            rows=c.exec_driver_sql(f'SELECT id,tenant_id,"{payload}" FROM "{app.schema}".customer').all()
            recovered={r[0]:independent_open(bytes(r[2]) if r[2] is not None else None,descriptor,r[1],r[0]) for r in rows}
        assert recovered=={k:v[1] for k,v in app.source.items()}


def test_native_uniqueness_nulls_and_collation_are_restored():
    import os,psycopg
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a)
        execute(app,d,p,replace(pin,phase='PLAINTEXT_ACTIVATING'),a,'PLAINTEXT_ACTIVE')
        with psycopg.connect(plaintext_url()) as c:
            with pytest.raises(psycopg.errors.UniqueViolation):
                with c.transaction():c.execute(f'INSERT INTO "{app.schema}".customer(id,tenant_id,name) VALUES (%s,%s,%s)',(UUID(int=990),TENANT,'exact'))
            c.execute(f'INSERT INTO "{app.schema}".customer(id,tenant_id,name) VALUES (%s,%s,NULL)',(UUID(int=991),TENANT))
            assert c.execute(f'SELECT count(*) FROM "{app.schema}".customer WHERE name IS NULL').fetchone()==(2,)
            assert c.execute(f'SELECT count(*) FROM "{app.schema}".customer WHERE name IN (%s,%s)',('é','e\u0301')).fetchone()==(2,)
            assert c.execute(f'SELECT count(*) FROM "{app.schema}".customer WHERE name=%s',('trailing',)).fetchone()==(0,)


def test_provider_outage_mid_batch_preserves_prefix_and_emits_no_later_sql():
    from sqlalchemy import event
    from test_migration import PublicFixtureProvider,PROVIDER,TABLE_ID
    from cryptalis.crypto import Keyring
    class Failing(PublicFixtureProvider):
        calls=0;failed=False
        def unwrap(self,w,c):
            self.calls+=1
            if self.calls>2:
                self.failed=True;raise RuntimeError('synthetic unavailable')
            return super().unwrap(w,c)
    with application() as app:
        d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'EXPANDED')
        provider=Failing();after_failure=[]
        def observe(conn,cursor,statement,params,context,many):
            if provider.failed:after_failure.append(statement)
        event.listen(app.owner,'before_cursor_execute',observe)
        try:
            with pytest.raises(TransitionFailure):
                d.apply(p,app.owner,keys=lambda t:Keyring(keys(t).policy,{PROVIDER:provider}),pin=pin,
                        approval=app.approval,plaintext_approval=a,chunk_size=2)
            assert not after_failure
        finally:event.remove(app.owner,'before_cursor_execute',observe)
        with app.owner.connect() as c:
            state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',(p.operation_id,)).scalar_one()
            assert state['models'][str(TABLE_ID)]['rows']==2
        execute(app,d,p,pin,a)


def test_wrong_row_ciphertext_is_rejected_before_plaintext_batch_commit():
    with application() as app:
        d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'EXPANDED')
        payload=ciphertext_column(app)
        with app.owner.begin() as c:
            frame=c.exec_driver_sql(f'SELECT "{payload}" FROM "{app.schema}".customer WHERE id=%s',(UUID(int=102),)).scalar_one()
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{payload}"=NULL WHERE id=%s',(UUID(int=102),))
            c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{payload}"=%s WHERE id=%s',(frame,UUID(int=103)))
        with pytest.raises(TransitionFailure):execute(app,d,p,pin,a)


@pytest.mark.parametrize('commit_number',[3,4,5,6,7,8,9])
def test_lost_reverse_commit_reply_resumes_exact_current_values(commit_number):
    import os,psycopg
    from sqlalchemy import create_engine
    from migration_commit_proxy import lost_commit_reply
    with application() as app:
        d,p,pin,a=prepared(app)
        with lost_commit_reply(os.environ['CRYPTALIS_TEST_DATABASE_URL'],commit_number=commit_number) as (url,dropped):
            proxied=create_engine('postgresql+psycopg://',hide_parameters=True,creator=lambda:psycopg.connect(url))
            try:
                with pytest.raises(TransitionFailure):
                    d.apply(p,proxied,keys=keys,pin=pin,approval=app.approval,plaintext_approval=a,chunk_size=2)
                assert dropped.is_set()
            finally:proxied.dispose()
        execute(app,d,p,pin,a)
        with app.owner.connect() as c:
            assert dict(c.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".customer').all())=={k:v[1] for k,v in app.source.items()}


def test_unknown_journal_state_and_unexpected_removal_operation_refuse():
    with application() as app:
        d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'EXPANDED')
        with app.owner.begin() as c:
            c.exec_driver_sql(f"UPDATE \"{app.schema}\"._cryptalis_journal SET state=jsonb_set(state,'{{phase}}','\"UNKNOWN\"') WHERE operation_id=%s",(p.operation_id,))
        with pytest.raises(TransitionFailure,match='unknown_or_aborted_reverse_state'):execute(app,d,p,pin,a)
    with application() as app:
        d,p,pin,a=prepared(app);execute(app,d,p,pin,a)
        execute(app,d,p,replace(pin,phase='PLAINTEXT_ACTIVATING'),a,'PLAINTEXT_ACTIVE')
        with app.owner.begin() as c:
            c.exec_driver_sql(f'INSERT INTO "{app.schema}"._cryptalis_journal VALUES (%s,%s,%s::jsonb)',(UUID(int=777),'a'*64,json.dumps({'phase':'ABORTED'})))
        approval=d.RemovalApproval(p.digest,'native test','backup test',True)
        with pytest.raises(TransitionFailure,match='unreviewed_journal_operations'):
            d.remove(p,app.owner,pin=replace(pin,phase='REMOVING'),approval=app.approval,plaintext_approval=a,removal_approval=approval)


def test_aborted_reverse_is_idempotent_and_later_reviewed_removal_completes():
    with application() as app:
        d,p,pin,a=prepared(app)
        execute(app,d,p,pin,a,'BACKFILLED')
        d.abort(p,app.owner,pin=pin,approval=app.approval,plaintext_approval=a)
        assert d.abort(p,app.owner,pin=pin,approval=app.approval,plaintext_approval=a).phase=='ABORTED'
        newer=d.plan(app.plan,app.owner,source_pin=app.pin,keys=keys,plaintext_runtime_role=plaintext_role(),
             backfill_rows_per_second=1000,verify_rows_per_second=1000,
             temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        newpin=DeploymentPin(newer.target_id,newer.operation_id,newer.digest,'PREPARED')
        newa=d.PlaintextApproval(newer.target_id,newer.operation_id,newer.digest,True,'verified public fixture backup')
        execute(app,d,newer,newpin,newa)
        execute(app,d,newer,replace(newpin,phase='PLAINTEXT_ACTIVATING'),newa,'PLAINTEXT_ACTIVE')
        proof=d.RemovalApproval(newer.digest,'native workload','retained backup',True)
        assert d.remove(newer,app.owner,pin=replace(newpin,phase='REMOVING'),approval=app.approval,plaintext_approval=newa,removal_approval=proof).phase=='REMOVED'


@pytest.mark.parametrize('changed',['format','source_pin','unknown_member','retired_digest'])
def test_malformed_reverse_contract_refuses_without_effects(changed):
    from cryptalis.manifest.compiler import _canonical
    with application() as app:
        d,p,pin,a=prepared(app);doc=p.document
        if changed=='format':doc['format']='cryptalis.reverse/v999'
        if changed=='source_pin':doc['source_pin']['plan_digest']='0'*64
        if changed=='unknown_member':doc['fallback_plaintext']=True
        if changed=='retired_digest':doc['retirable_aborted']=[{'operation_id':str(UUID(int=765)),'plan_digest':'not-a-digest'}]
        with pytest.raises(TransitionFailure,match='invalid_reverse_plan'):d.DeprotectionPlan(_canonical(doc))


def test_key_expiry_mid_batch_commits_no_plaintext(monkeypatch):
    import time
    from test_migration import TABLE_ID,FIELD_ID,PROVIDER,PublicFixtureProvider
    from cryptalis.crypto import Keyring
    with application() as app:
        d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'EXPANDED')
        original=d.open_text;calls=[0]
        def slow(*args):
            result=original(*args);calls[0]+=1
            if calls[0]==1:time.sleep(.04)
            return result
        monkeypatch.setattr(d,'open_text',slow)
        with pytest.raises(TransitionFailure):
            d.apply(p,app.owner,keys=lambda t:Keyring(keys(t).policy,{PROVIDER:PublicFixtureProvider()},max_age=.02),pin=pin,
                    approval=app.approval,plaintext_approval=a,chunk_size=2)
        with app.owner.connect() as c:
            state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',(p.operation_id,)).scalar_one()
            assert state['models'][str(TABLE_ID)]['rows']==0
            assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".customer WHERE "_cryptalis_{FIELD_ID.hex}_plain" IS NOT NULL').scalar_one()==0

"""Fresh-process recovery of synthetic CF1 data stored in real PostgreSQL."""
import hashlib,json,subprocess,sys
from dataclasses import asdict
from cryptalis.crypto import FileDevelopmentKeyProvider,KeyPolicy,Keyring,create_root
from cryptalis.sqlalchemy import attach
from test_sqlalchemy_search import search_application,_row


def test_database_frame_is_readable_after_provider_process_restart(tmp_path):
    with search_application(True,attach_now=False) as app:
        path=tmp_path/'development.key';provider=FileDevelopmentKeyProvider.create(path)
        old=app.keys(app.tenant).policy
        wrappers=tuple(create_root(provider,w.context) for w in old.wrappers)
        policy=KeyPolicy(old.domain_id,old.tenant_id,wrappers,old.payload_generation,old.search_generation)
        ring=Keyring(policy,{provider.provider_id:provider})
        sessions=attach(app.mapping,app.engine,lock=app.plan.lock_bytes,keys=lambda tenant:ring)
        value='synthetic restart value: é e\u0301 雪'
        row=_row(app,value,1);identity=row.id
        with sessions(tenant_id=app.tenant) as s:s.add(row);s.commit()
        descriptor=json.loads(app.plan.lock_bytes)['models'][0]['fields'][0]
        payload={'path':str(path),'schema':app.schema,'record':str(identity),'tenant':str(app.tenant),
          'domain':str(old.domain_id),'payload_generation':old.payload_generation,'search_generation':old.search_generation,
          'descriptor':descriptor['descriptor'],'descriptor_digest':descriptor['descriptor_digest'],
          'wrappers':[{'provider_id':str(w.provider_id),'context':asdict(w.context),'sealed':w.sealed.hex()} for w in wrappers]}
        code='''import json,os,sys,hashlib
from uuid import UUID
import psycopg
from psycopg import sql
from cryptalis.crypto import FileDevelopmentKeyProvider,FieldDescriptor,KeyContext,KeyPolicy,Keyring,WrappedRoot,open_text
p=json.load(sys.stdin);provider=FileDevelopmentKeyProvider.open(p['path']);wrappers=[]
for w in p['wrappers']:
 c=w['context']
 for key in ('domain_id','tenant_id','root_id'):c[key]=UUID(c[key])
 wrappers.append(WrappedRoot(UUID(w['provider_id']),KeyContext(**c),bytes.fromhex(w['sealed'])))
policy=KeyPolicy(UUID(p['domain']),UUID(p['tenant']),tuple(wrappers),p['payload_generation'],p['search_generation'])
keys=Keyring(policy,{provider.provider_id:provider}).prepare()
with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:
 frame=c.execute(sql.SQL('SELECT name FROM {}.customer WHERE id=%s').format(sql.Identifier(p['schema'])),(UUID(p['record']),)).fetchone()[0]
value=open_text(frame,FieldDescriptor.from_compiled(p['descriptor'],p['descriptor_digest']),UUID(p['tenant']),UUID(p['record']),keys)
print(hashlib.sha256(value.encode()).hexdigest())
'''
        result=subprocess.run([sys.executable,'-c',code],input=json.dumps(payload,default=str),text=True,capture_output=True,check=True,timeout=10)
        assert result.stdout.strip()==hashlib.sha256(value.encode()).hexdigest()
        before=path.read_bytes();path.unlink()
        missing=subprocess.run([sys.executable,'-c',code],input=json.dumps(payload,default=str),text=True,capture_output=True,timeout=10)
        assert missing.returncode!=0 and 'FileCustodyUnavailable' in missing.stderr
        assert not path.exists() # No implicit key regeneration.
        # Explicit operator restoration of this synthetic retained custody copy.
        path.write_bytes(before);path.chmod(0o600)
        restored=subprocess.run([sys.executable,'-c',code],input=json.dumps(payload,default=str),text=True,capture_output=True,check=True,timeout=10)
        assert restored.stdout==result.stdout

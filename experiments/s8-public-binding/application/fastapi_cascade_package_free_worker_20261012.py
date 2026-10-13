"""Fresh native process, no Cryptalis package; disposable loopback app only."""
from pathlib import Path
import importlib.util,json,os,socket,sys
assert importlib.util.find_spec('cryptalis') is None
B=Path(__file__).resolve().parents[2];schema,out=sys.argv[1],Path(sys.argv[2])
assert schema.startswith('cryptalis_fastapi_a6_') and out.is_relative_to(B/'evidence')
values=json.loads((B/'apps/runtime/private/fastapi-env.json').read_text());os.environ.update(values)
sys.path.insert(0,str(B/'apps/harness'))
from local_smtp_fixture import start
mail=start();connect0=socket.socket.connect;connect_ex0=socket.socket.connect_ex;create0=socket.create_connection;dns0=socket.getaddrinfo

def allowed(a):
    if isinstance(a,str) or a[0] not in ('127.0.0.1','localhost','::1'):raise RuntimeError('Only disposable loopback services allowed')
def connect(self,a):allowed(a);return connect0(self,a)
def connect_ex(self,a):allowed(a);return connect_ex0(self,a)
def create(a,*args,**kw):
    if a[0]=='smtp.example.com':a=mail.server_address
    allowed(a);return create0(a,*args,**kw)
def dns(host,*args,**kw):
    if host not in ('127.0.0.1','localhost','::1',None):raise RuntimeError('External DNS blocked')
    return dns0(host,*args,**kw)
socket.socket.connect=connect;socket.socket.connect_ex=connect_ex;socket.create_connection=create;socket.getaddrinfo=dns
import psycopg
from sqlalchemy.engine import URL
info=psycopg.conninfo.conninfo_to_dict((Path.home()/'.cryptalis-writer-url').read_text().strip())
assert info['host']=='127.0.0.1' and str(info['port'])=='55432'
url=URL.create('postgresql+psycopg',username=info['user'],password=info['password'],host=info['host'],port=int(info['port']),database=info['dbname'],query={'options':f'-c search_path={schema},pg_catalog'})
os.environ['DATABASE_URL']=url.render_as_string(hide_password=False)
os.environ.update(SMTP_HOST='127.0.0.1',SMTP_PORT=str(mail.server_address[1]),SMTP_TLS='false',SENTRY_DSN='')
checkout=B/'apps/checkouts/fastapi-template/backend';sys.path.insert(0,str(checkout));os.chdir(checkout)
from app.core.db import engine
engine.hide_parameters=True
from sqlmodel import Session,select,delete
from app.models import User,Item
with Session(engine) as native_session:
    observed={str(row.id):row.full_name for row in native_session.scalars(select(User))}
    expected=json.loads((out/'expected-native-values.json').read_text())
    assert observed==expected,'Package-free preserved-value mismatch'
    email_evidence=out/'expected-native-emails.json'
    if email_evidence.exists():
        observed_emails={str(row.id):row.email for row in native_session.scalars(select(User))}
        assert observed_emails==json.loads(email_evidence.read_text()),'Package-free email mismatch'
    child_evidence=out/'expected-native-children.json'
    if child_evidence.exists():
        observed_children=native_session.connection().exec_driver_sql('SELECT row_to_json(t) FROM item t ORDER BY id').scalars().all()
        assert observed_children==json.loads(child_evidence.read_text()),'Package-free public-child mismatch'
    # Reproduce native upstream teardown before a second isolated suite campaign.
    native_session.execute(delete(Item));native_session.execute(delete(User));native_session.commit()
import pytest
try:
    code=int(pytest.main(['-o','addopts=','-q','--tb=short','--strict-markers','--junitxml='+str(out/'package-free-junit.xml'),'tests']))
    assert importlib.util.find_spec('cryptalis') is None
    (out/'package-free-result.json').write_text(json.dumps({'pytest_exit_code':code,'package_absent':True,'new_plaintext_runtime_role':True,'application_source_edits':0,'preserved_values_exact_before_reset':True,'fixture_reset_before_suite':True,'email_values_checked':email_evidence.exists(),'child_values_checked':child_evidence.exists()}))
finally:engine.dispose();mail.shutdown();mail.server_close()
raise SystemExit(code)

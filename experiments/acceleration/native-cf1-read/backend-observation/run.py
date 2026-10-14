import sys,json,hashlib,copy
from pathlib import Path
from uuid import UUID
R=Path(__file__).parent.absolute();O=R.parent/'candidate-native-cf1-read-20261014'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for p,h in json.loads((R/'PINS.json').read_text()).items():
 if sha(p)!=h:raise RuntimeError('Input changed: '+p)
build=json.loads((R/'build/build.json').read_text())
for p,h in build['pins'].items():
 if sha(p)!=h:raise RuntimeError('Build pin changed: '+p)
if sys.executable!=str(R.parent/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14):raise RuntimeError('Interpreter mismatch')
sys.path.insert(0,str(R/'build'))
import native_cf1 as n
if Path(n.__file__).parent!=R/'build':raise RuntimeError('Origin mismatch')
if n.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Backend mismatch: '+n.backend_version())
manifest=json.loads((R/'cases.json').read_text());records=[];ids=set();controls=[]
def check(rec):
 if rec['before']!=rec['after']:raise ValueError('queue mismatch')
 if any(m[2]!='default' for m in rec['methods']):raise ValueError('provider mismatch')
for c in manifest['cases']:
 if c['id'] in ids:raise RuntimeError('Duplicate case')
 ids.add(c['id']);s=manifest['fixtures']['uuid-'+c['rep']+'-unicode'];eq=c['rep']=='equality'
 raw=(O/s['frame_path']).read_bytes()
 if sha(O/s['frame_path'])!=s['frame_sha256']:raise RuntimeError('Fixture mismatch')
 def uuid(key):return UUID(s[key]).bytes
 def bundle(prefix):return (bytes.fromhex(s[prefix+'_root']),uuid('domain_id'),uuid('tenant_id'),uuid(prefix+'_root_id'),s[prefix+'_generation'].to_bytes(4,'big'))
 pm=bundle('payload');sm=bundle('search') if eq else None
 action=c['action'];fault=int(action[5:]) if action.startswith('fault') else 0
 if action=='badtag':raw=raw[:-1]+bytes([raw[-1]^1])
 if action=='wrongsearch':sm=(bytes([sm[0][0]^1])+sm[0][1:],*sm[1:])
 args=(raw,int(eq),uuid('domain_id'),uuid('tenant_id'),uuid('field_id'),bytes.fromhex(s['descriptor_digest']),bytes.fromhex(s['typed_record_id']),pm,sm,fault)
 n.queue_seed(c['sentinels']);before=n.queue_peek(c['sentinels'])
 if len(before)!=c['sentinels']:raise RuntimeError('Sentinel count mismatch')
 for i,e in enumerate(before):
  if e!=((128<<23)|(100+i),'public-sentinel.c',700+i,'public_sentinel',f'public-sentinel-{i}',3):raise RuntimeError('Sentinel fixture mismatch')
 value,error,methods,properties=n.observe(*args);after=n.queue_drain()
 if action=='success':
  if error is not None or type(value)is not bytes or value.hex()!=c['expected']:raise RuntimeError('Success mismatch')
  outcome={'hex':value.hex(),'type':'bytes'}
 else:
  if value is not None or type(error)is not RuntimeError or error.args!=(c['expected'],):raise RuntimeError('Refusal mismatch')
  outcome={'exception':'RuntimeError','args':list(error.args)}
 expected_slots=[] if fault==1 else [0,1] if fault==10 else [0,1,2] if (not eq or action=='badtag' or fault==17) else [0,1,2,3,4] if fault==30 else [0,1,2,3,4,5]
 if [x[0] for x in methods]!=expected_slots:raise RuntimeError('Fetched slots mismatch')
 if 2 in expected_slots and properties[:2]!=(32,12):raise RuntimeError('Cipher property mismatch')
 rec=dict(id=c['id'],outcome=outcome,before=before,after=after,methods=methods,cipher_properties=properties)
 check(rec);records.append(rec)
 if c['id']=='equality-success-q2':
  for kind in ['queue','provider']:
   bad=copy.deepcopy(rec)
   if kind=='queue':bad['after']=bad['after'][:-1]
   else:bad['methods']=[(x[0],x[1],'unexpected') for x in bad['methods']]
   try:check(bad)
   except ValueError:controls.append(kind)
   else:raise RuntimeError('Comparator control survived')
if len(records)!=36 or controls!=['queue','provider']:raise RuntimeError('Incomplete records/controls')
with (R/f'results-O{sys.flags.optimize}.json').open('x') as out:json.dump(dict(records=records,controls=controls,backend=n.backend_version(),origin=n.__file__,optimize=sys.flags.optimize,binary_sha256=sha(n.__file__),manifest_sha256=sha(R/'cases.json')),out,indent=2)
print('PASS',len(records),sys.flags.optimize)

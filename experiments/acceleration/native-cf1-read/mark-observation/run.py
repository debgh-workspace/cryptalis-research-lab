import sys,json,hashlib
from pathlib import Path
from uuid import UUID
R=Path(__file__).parent.absolute();O=R.parent/'candidate-native-cf1-read-20261014'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for p,h in json.loads((R/'PINS.json').read_text()).items():
 if sha(p)!=h:raise RuntimeError('Input changed: '+p)
for p,h in json.loads((R/'build/build.json').read_text())['pins'].items():
 if sha(p)!=h:raise RuntimeError('Build pin changed: '+p)
if sys.executable!=str(R.parent/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14):raise RuntimeError('Interpreter mismatch')
if sys.flags.optimize not in (0,1):raise RuntimeError('Optimization mismatch')
sys.path.insert(0,str(R/'build'))
import native_cf1 as n
if Path(n.__file__).parent!=R/'build' or n.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Backend/origin mismatch')
manifest=json.loads((R/'cases.json').read_text());records=[];ids=set()
def init(config):
 n.queue_seed(1 if config.startswith('lower') else 2)
 statuses=[n.mark_set()]
 if config.startswith('lower'):n.queue_append(1)
 if config in ('top-twice','lower-plus-top'):statuses.append(n.mark_set())
 if any(x!=1 for x in statuses):raise RuntimeError('Mark setup failed')
 return statuses
for c in manifest['cases']:
 if c['id'] in ids:raise RuntimeError('Duplicate ID')
 ids.add(c['id']);args=None
 if c['kind']=='helper':
  s=manifest['fixtures']['uuid-'+c['rep']+'-unicode'];eq=c['rep']=='equality';action=c['action']
  raw=(O/s['frame_path']).read_bytes()
  if sha(O/s['frame_path'])!=s['frame_sha256']:raise RuntimeError('Fixture changed')
  def uuid(k):return UUID(s[k]).bytes
  def bundle(p):return(bytes.fromhex(s[p+'_root']),uuid('domain_id'),uuid('tenant_id'),uuid(p+'_root_id'),s[p+'_generation'].to_bytes(4,'big'))
  pm=bundle('payload');sm=bundle('search') if eq else None
  fault=int(action[5:]) if action.startswith('fault') else 0
  if action=='badtag':raw=raw[:-1]+bytes([raw[-1]^1])
  if action=='wrongsearch':sm=(bytes([sm[0][0]^1])+sm[0][1:],*sm[1:])
  args=(raw,int(eq),uuid('domain_id'),uuid('tenant_id'),uuid('field_id'),bytes.fromhex(s['descriptor_digest']),bytes.fromhex(s['typed_record_id']),pm,sm,fault)
 statuses=init(c['configuration']);control_status=None;outcome=None;methods=None;properties=None
 if c['kind']=='control':
  if c['variant']=='consume-one':control_status=n.mark_pop()
  elif c['variant']=='add-one':control_status=n.mark_set()
  if control_status is not None and control_status!=1:raise RuntimeError('Control setup failed')
 else:
  value,error,methods,properties=n.observe(*args)
  if action=='success':
   if error is not None or type(value)is not bytes or value.hex()!=c['expected_outcome']:raise RuntimeError('Success mismatch')
   outcome={'hex':value.hex(),'type':'bytes'}
  else:
   if value is not None or type(error)is not RuntimeError or error.args!=(c['expected_outcome'],):raise RuntimeError('Refusal mismatch')
   outcome={'exception':'RuntimeError','args':list(error.args)}
 # Peeks report endpoints, not a hidden queue/mark snapshot.
 observed={'initial_endpoints':n.queue_peek(2),'steps':[]}
 for expected_step in c['expected']['steps']:
  n.queue_append(2)
  distance=n.mark_count();pop=n.mark_pop()
  observed['steps'].append({'distance':distance,'pop':pop,'endpoints':n.queue_peek(2)})
 observed['drained']=n.queue_drain()
 # JSON normalization converts public tuple records to manifest list records.
 observed=json.loads(json.dumps(observed))
 equal=observed==c['expected']
 if equal!=c['expect_equal']:raise RuntimeError('Semantic comparison mismatch: '+c['id'])
 if not equal and observed!=c['expected_mutated']:raise RuntimeError('Wrong negative-control divergence: '+c['id'])
 records.append(dict(id=c['id'],setup_statuses=statuses,control_status=control_status,outcome=outcome,methods=methods,cipher_properties=properties,observed=observed,equal_to_preserved=equal))
if len(records)!=60:raise RuntimeError('Incomplete cases')
with (R/f'results-O{sys.flags.optimize}.json').open('x') as out:json.dump(dict(records=records,backend=n.backend_version(),origin=n.__file__,optimize=sys.flags.optimize,binary_sha256=sha(n.__file__),manifest_sha256=sha(R/'cases.json')),out,indent=2)
print('PASS',len(records),sys.flags.optimize)

"""Independent stdlib-only data audit. Never imports candidate code."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent.parent/'candidate-native-return-expiry-20261014'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 if not ok:raise RuntimeError(label)
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
pins=read(R/'PINS.json')['pins'];check(len(pins)==684,'pin count')
for name,h in pins.items():check(sha(Path(name))==h,'pin '+name)
check(sha(R/'cases.json')=='61526cc88cd30e869a8f2bffbeba86a97dc9343d8ddcad30fecb2235690a553e','frozen cases')
check(sha(R/'PINS.json')=='9fdaf8c6e5cc8dd2c6a5f125447639fae60c6e2694b394438b17602fbcc72d38','frozen pins')
art=read(R/'ARTIFACTS.json')['files'];check(len(art)==23,'inventory count')
for name,h in art.items():check(sha(R/name)==h,'artifact '+name)
check(set(art)=={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and p.name!='ARTIFACTS.json'},'exact inventory')
m=read(R/'cases.json');expected=[{'id':c['id'],'actual':c['expected']} for c in m['cases']]
check([x['id'] for x in expected]==['after-native-return/storage/payload','after-native-return/equality/search'],'ids')
launches=read(R/'LAUNCHES.json');check(len(launches)==6,'launch count');summary=[];positive=[]
for opt in (0,1):
 for mode in ('metadata','trace','positive'):
  name=f'{mode}-o{opt}-01';rp=R/'evidence'/f'{name}.json';result=read(rp);launch=read(R/'evidence'/f'{name}-launch.json')
  check(same(launch,launches[len(summary)]),'launch index')
  check(launch['command']==[str(R.parent/'repo/.venv/bin/python'),'-B']+(['-O'] if opt else [])+[str(R/'run.py'),mode,f'evidence/{name}.json'],'command')
  check(launch['stdout']=='','stdout');check(launch['result_sha256']==sha(rp),'receipt digest')
  check(result['mode']==mode and type(result['optimize']) is int and result['optimize']==opt,'mode')
  check(result['verified_pins']==684 and result['pins_sha256']==sha(R/'PINS.json') and result['manifest_sha256']==sha(R/'cases.json'),'preimport receipt pins')
  check(result['python_executable']==str(R.parent/'repo/.venv/bin/python'),'interpreter')
  check(result['native_backend']=='OpenSSL 3.5.7 9 Jun 2026' and result['oracle_backend']=='OpenSSL 4.0.3 29 Sep 2026','backends')
  build=read(R.parent/'candidate-native-cf1-read-20261014/build-03-normal/build.json');check(result['native_origin']==build['binary'],'native origin')
  if mode=='positive':
   check(launch['exit']==0 and launch['stderr']=='' and result['status']=='PASS','positive exit')
   check(same(result['observations'],expected),'entire positive record')
   check(result['negative'] is None and 'error' not in result and 'error_type' not in result,'no hidden positive failure');positive.append(result['observations'])
  else:
   idx=0 if mode=='metadata' else 1;n=result['negative'];check(same(n['original'],expected[idx]['actual']),'original negative observation')
   changed=copy.deepcopy(expected[idx]['actual'])
   if mode=='metadata':changed['stage']='deliberately-wrong-stage'
   else:changed['trace']+=changed['trace'][:1]
   check(same(n,{'mode':mode,'case_id':expected[idx]['id'],'original_verified':True,'original':expected[idx]['actual'],'mutated':changed}),'entire negative record')
   check(launch['exit']==1 and result['status']=='FAIL' and result['observations']==[],'negative exit')
   check(result['error_type']=='RuntimeError' and result['error']=='Exact return-expiry mismatch','negative error')
   check(launch['stderr'].startswith('Traceback (most recent call last):\n') and launch['stderr'].count('Traceback (most recent call last):')==1 and launch['stderr'].endswith('RuntimeError: Exact return-expiry mismatch\n') and "exact(changed,case['expected'])" in launch['stderr'],'negative intended stack')
  summary.append({'mode':mode,'optimization':opt,'exit':launch['exit'],'full_record_verified':True})
check(same(*positive),'cross-mode equivalence')
print(json.dumps({'status':'PASS','data_only':True,'pins_verified':len(pins),'artifact_files_verified':len(art),'cases_sha256':sha(R/'cases.json'),'pins_sha256':sha(R/'PINS.json'),'artifacts_sha256':sha(R/'ARTIFACTS.json'),'launches':summary,'unexpected_failures':False},indent=2))

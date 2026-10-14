"""Read-only stdlib evidence audit; never executes/imports candidate code."""
import copy,hashlib,json
from pathlib import Path
N=Path(__file__).resolve().parent;B=N.parent;R=B/'candidate-native-resource-balance-20261014'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(b,label):
 if not b:raise RuntimeError(label)
 checks.append(label)
def exact(a,b):return type(a)==type(b) and (a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a) if isinstance(a,dict) else len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b)) if isinstance(a,list) else a==b)
d=read(R/'cases.json');pins=read(R/'PINS.json')['pins'];source=read(R/'SOURCE_PINS.json')['pins']
check(len(pins)==692,'692 frozen pins')
for collection in [pins,source]:
 for p,h in collection.items():check(sha(Path(p))==h,'frozen pin '+p)
for p,h in read(N/'STATIC_AUDIT.json')['reviewed_hashes'].items():check(sha(B/p)==h,'reviewed source unchanged '+p)
launches=read(R/'LAUNCHES.json');check([l['name'] for l in launches]==[m+'-O'+str(o) for o in (0,1) for m in ('release','transfer','positive')],'exact launch schedule')
receipts={}
for l in launches:
 p=R/'evidence'/(l['name']+'.json');check(sha(p)==l['receipt_sha256'],'receipt hash '+l['name']);a=read(p);receipts[l['name']]=a
 mode,opt=l['name'].split('-O');opt=int(opt)
 check(a['mode']==mode and a['optimize']==opt,'receipt mode '+l['name'])
 check(a['pins_sha256']==sha(R/'PINS.json') and a['cases_sha256']==sha(R/'cases.json') and a['verified_pins']==len(pins),'receipt provenance '+l['name'])
 check(l['exit']==(0 if mode=='positive' else 1),'exit '+l['name'])
 check(a['status']==('PASS' if mode=='positive' else 'FAIL'),'status '+l['name'])
 check(a['native_origin']==read(R/'build/build.json')['binary'],'native origin '+l['name'])
 check(a['native_backend']=='OpenSSL 3.5.7 9 Jun 2026','backend receipt '+l['name'])
 if mode!='positive':
  check(a['error']=='Exact resource mismatch' and a['error_type']=='RuntimeError' and len(a['observations'])==1,'negative signature '+l['name'])
  obs=a['observations'][0];first=d['cases'][0]
  check(obs['original_verified'] is True and obs['perturbed_field']==mode,'negative verified origin '+l['name'])
  check(exact(obs['original_balance'],first['balance_expected']) and exact(obs['actual'],first['expected']),'negative real success '+l['name'])
  expected=copy.deepcopy(obs['original_balance'])
  if mode=='release':expected[0][0][1]-=1
  else:expected[0][9][2]=0
  check(exact(obs['balance'],expected),'one intended mutation '+l['name'])
  check((R/'evidence'/(l['name']+'.stderr')).read_text().rstrip().endswith('RuntimeError: Exact resource mismatch'),'negative stderr '+l['name'])
  continue
 check(len(a['observations'])==170,'full observation count '+l['name'])
 check([x['id'] for x in a['observations']]==[x['id'] for x in d['cases']+d['direct_cases']],'complete ordered observations '+l['name'])
 totals={n:dict(acquired=0,released=0,transferred=0) for n in d['resource_names']}
 for obs,c in zip(a['observations'],d['cases']+d['direct_cases']):
  if 'balance_expected' in c:
   expected=c['balance_expected'];public=c['expected']
   check(obs['native_entry_trace']==[{'entry':'open_encoded','selector':c['selector']}] and obs['same_prepared_group']==c['group'],'wrapper routing '+obs['id'])
  elif c['phase']=='refusal':
   expected=[[[0,0,0,0,0] for _ in range(10)],0,0];public={'exception':c['expected_exception']}
  else:
   expected=next(x['balance_expected'] for x in d['cases'] if bool(d['fixtures'][x['fixture']]['search_generation'])==bool(c['rep']) and 'value' in x['expected']);public={'value_type':'bytes','value_hex':'61626364656667'}
  check(exact(obs['actual'],public),'exact public outcome '+obs['id'])
  check(exact(obs['balance'],expected),'exact ledger '+obs['id'])
  for name,row in zip(d['resource_names'],obs['balance'][0]):
   acq,rel,transfer,live,peak=row
   check(acq==rel+transfer and live==0 and peak in (0,1),'balanced owned reference '+name+' '+obs['id'])
   for k,v in zip(('acquired','released','transferred'),row[:3]):totals[name][k]+=v
  check(obs['balance'][1]==0,'zero outstanding scratch bytes '+obs['id'])
 check(exact(totals,read(R/'VERIFICATION.json')['per_mode_totals']),'independent totals '+l['name'])
check(exact(receipts['positive-O0']['observations'],receipts['positive-O1']['observations']),'exact O0/O1 observation parity')
check(read(R/'build/build.json')['exit_code']==0,'successful recorded build')
if (R/'ARTIFACTS.json').exists():
 artifacts=read(R/'ARTIFACTS.json')['files']
 check(set(artifacts)=={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and p.name!='ARTIFACTS.json'},'complete final artifact inventory')
 for p,h in artifacts.items():check(sha(R/p)==h,'final artifact '+p)
 check(sha(R/'ARTIFACTS.json')=='0d99959cda5c84f5f2d10d173c897ae6e1cdd4b5a64bb78e3ba8506fe39f07c2','author final inventory freeze')
 check(sha(R/'RESULTS.md')=='cd22774a4b2f35ddf56155165133c0dc127be6109f955d30a9975b60111d7fe5','author final results freeze')
result={'status':'PASS','checks':len(checks),'observations_per_positive':170,'negative_controls':4,'pins':len(pins),'source_pins':len(source),'per_mode_totals':totals,'details':checks}
(N/'POSTRUN_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='details'}))

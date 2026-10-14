import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
m=json.loads((R/'cases.json').read_text());pins=json.loads((R/'PINS.json').read_text())
for path,digest in pins.items():
 if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise RuntimeError('Pin changed')
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
positives=[]
for opt in (0,1):
 p=json.loads((R/f'evidence/r2-o{opt}-positive.json').read_text())
 if p['status']!='PASS' or p['optimize']!=opt:raise RuntimeError('Bad positive')
 expected=[{'id':c['id'],'actual':c['expected']} for c in m['cases']]
 if not same(p['observations'],expected):raise RuntimeError('Observation mismatch')
 positives.append(p['observations'])
 for mode,id_ in [('abi','abi/type/0/0'),('fork','fork/000')]:
  n=json.loads((R/f'evidence/r2-o{opt}-{mode}.json').read_text())
  if (n['status'],n['error_type'],n['error'])!=('FAIL','RuntimeError','Negative oracle mismatch'):raise RuntimeError('Wrong negative')
  rec=n['observations'][-1];c=next(c for c in m['cases'] if c['id']==id_)
  if rec['id']!=id_ or not same(rec['verified_original'],c['expected']):raise RuntimeError('Negative original unverified')
  mut=json.loads(json.dumps(c['expected']))
  if mode=='abi':mut['exception']='TypeError'
  else:mut['inherited']['trace']=[]
  if not same(mut,rec['mutated']):raise RuntimeError('Wrong mutation')
if not same(*positives):raise RuntimeError('Optimization observations differ')
with (R/'VERIFICATION.json').open('x') as f:json.dump({'status':'PASS','pins':len(pins),'predeclared_entries':len(m['cases']),'optimization_observations_equal':True,'negative_controls':4,'scope':'stdlib data correspondence; no candidate execution'},f,indent=2)

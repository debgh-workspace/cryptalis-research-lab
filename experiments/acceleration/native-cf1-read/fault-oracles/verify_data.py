"""Standalone stdlib correspondence verification; no candidate imports."""
import ast,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
    if not c:raise RuntimeError(m)
m=json.loads((R/'cases.json').read_text()); cases=m['cases']; ids=[c['id'] for c in cases]
require(len(ids)==149 and len(set(ids))==149,'case inventory')
pins=json.loads((R/'PINS.json').read_text())['pins']
for n,h in pins.items():require(sha(Path(n))==h,'pin '+n)
launches=json.loads((R/'LAUNCHES.json').read_text());require(len(launches)==6,'launch count')
positives=[]
for launch in launches:
    p=R/launch['receipt'];require(sha(p)==launch['receipt_sha256'],'receipt digest')
    d=json.loads(p.read_text());require(d['cases_sha256']==sha(R/'cases.json') and d['pins_sha256']==sha(R/'PINS.json'),'provenance')
    if d['mode']=='positive':
        require(launch['exit']==0 and launch['stderr']=='' and d['status']=='PASS','positive state')
        require([x['id'] for x in d['observations']]==ids,'ordered ids')
        for c,o in zip(cases,d['observations']):
            require(o['actual']==c['expected'],'exact record')
            require(o['native_entry_trace']==[{'entry':'open_encoded','selector':c['selector']}],'entry trace')
        positives.append(d['observations'])
    else:
        require(launch['exit']==1 and d['error']=='Exact fault oracle mismatch','negative state')
        o=d['observations'][-1]; c=next(c for c in cases if c['id']==o['id'])
        require(o['original_verified'] and o['original']==c['expected'],'negative original')
        delta=[k for k in o['actual'] if o['actual'][k]!=o['original'][k]]
        require(delta==[d['mode']],'single negative field')
require(len(positives)==2 and positives[0]==positives[1],'optimization parity')
for p in R.glob('*.py'):require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'assert')
print(json.dumps({'status':'PASS','frozen_cases':149,'positive_launches':2,'intentional_negative_launches':4,'original_and_new_pins_verified':len(pins),'exact_o0_o1_observation_parity':True}))

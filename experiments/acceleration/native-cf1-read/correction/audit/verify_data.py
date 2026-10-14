"""Independent stdlib-only data audit; no candidate imports or execution."""
from pathlib import Path
import ast, collections, hashlib, json
BASE=Path(__file__).resolve().parent.parent
R=BASE/'candidate-native-cf1-read-correction-20261014'; O=BASE/'candidate-native-cf1-read-20261014'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,label):
    if not ok: raise RuntimeError(label)
def read(p): return json.loads(p.read_text())
m=read(R/'cases.json'); pins=read(R/'PINS.json')['pins']; originals=read(O/'ARTIFACTS.json')['files']
require(len(pins)==628,'pin count');require(len(originals)==130,'original count')
for p,h in pins.items(): require(sha(Path(p))==h,'pin '+p)
for p,h in originals.items(): require(sha(O/p)==h,'original '+p)
ids=[c['id'] for c in m['cases']];require(len(ids)==len(set(ids))==43,'case IDs')
for key,f in m['fixtures'].items():
    require(f['text'].encode('utf8').hex()==f['encoded_text'],'UTF8 '+key)
    require(hashlib.sha256(json.dumps(f['descriptor'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==f['descriptor_digest'],'descriptor '+key)
    require(sha((O if f['frame_origin']=='original' else R)/f['frame_path'])==f['frame_sha256'],'frame '+key)
for eq in (0,1):
    cases=[c for c in m['cases'] if c['id'].startswith(f'scope/{eq}/')];fs=[m['fixtures'][c['fixture']] for c in cases]
    require(len(fs)==3 and fs[0]==fs[2] and fs[0]['tenant_id']!=fs[1]['tenant_id'] and fs[0]['record_id']!=fs[1]['record_id'],'A/B/A')
positive=[]; negative=[]
for opt in (0,1):
    for mode in ('positive','negative'):
        p=R/'evidence'/f'{mode}-o{opt}-01.json';x=read(p);l=read(R/'evidence'/f'launch-{mode}-o{opt}-01.json')
        require(l['receipt_sha256']==sha(p),'receipt hash');require(x['optimize']==opt,'mode');require(x['verified_pin_count']==628 and x['pins_sha256']==sha(R/'PINS.json'),'receipt pins')
        if mode=='positive':
            require(l['exit']==0 and not l['stderr'] and x['status']=='PASS' and x['passed']==ids and len(x['observations'])==43,'positive result')
            for c,a in zip(m['cases'],x['observations']):
                require(a['id']==c['id'] and a['actual']==c['expected'] and a['native_calls']==c['native_calls'],'observation')
                require(a['decode_hook_completed']==(True if c['kind']=='decode-expiry' else None),'decode marker')
                expectedkeys={'value','value_type','trace'} if 'value' in c['expected'] else {'exception','code','stage','retryable','effects','remedy','operation_present','trace'}
                require(set(c['expected'])==expectedkeys,'observation schema')
            positive.append(x['observations'])
        else:
            marker=[{'id':'actual-output-perturbation','native_calls':1,'original_verified':True,'perturbation_applied_to_actual_return':True,'comparison_expected':'reject'}]
            require(l['exit']==1 and x['status']=='FAIL' and not x['passed'] and x['error_type']=='RuntimeError' and x['error']=='Mismatch: actual-output-perturbation' and x['observations']==marker,'negative exact cause')
            require(l['stderr'].splitlines()[-1]=='RuntimeError: Mismatch: actual-output-perturbation','negative stderr')
            negative.append(x['observations'])
require(positive[0]==positive[1] and negative[0]==negative[1],'O0/O1 parity')
require(all(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))) for p in R.glob('*.py')),'assert-free checks')
freeze=read(R/'evidence/freeze-01.json');require(freeze['case_manifest_sha256']==sha(R/'cases.json') and freeze['exit']==0,'freeze digest')
result={'status':'PASS','scope':'Independent data/source review, no execution attestation','verified_pins':628,'verified_original_files':130,'positive_unique_ordered_ids':43,'fixtures_verified':len(m['fixtures']),'success_or_null':12,'refusals':31,'positive_and_negative_O0_O1_parity':True,'manifest_sha256':sha(R/'cases.json'),'pins_sha256':sha(R/'PINS.json'),'original_inventory_sha256':sha(O/'ARTIFACTS.json'),'kinds':dict(collections.Counter(c['kind'] for c in m['cases']))}
print(json.dumps(result,indent=2))

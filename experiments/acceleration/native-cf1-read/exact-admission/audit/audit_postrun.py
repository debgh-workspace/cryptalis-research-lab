"""Independent receipt inspection, stdlib only; does not load candidate code."""
import collections,hashlib,json
from pathlib import Path
B=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable');R=B/'candidate-native-read-admission-20261014';N=Path(__file__).parent
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
checks=[]
def demand(x,label):
 if not x:raise RuntimeError(label)
 checks.append(label)
def equal(a,b,label):demand(canonical(a)==canonical(b),label)
m=load(R/'cases.json');pins=load(R/'PINS.json')['pins'];pre=load(N/'verification.json')
demand(sha(R/'cases.json')==pre['manifest_sha256'],'preexecution manifest hash unchanged')
demand(sha(R/'PINS.json')==pre['pins_sha256'],'preexecution pin inventory hash unchanged')
for path,digest in pins.items():demand(sha(Path(path))==digest,'pin '+path)
art=load(R/'ARTIFACTS.json')['files']
equal(sorted(art),sorted(str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and p.name!='ARTIFACTS.json'),'complete final artifact membership')
for path,digest in art.items():demand(sha(R/path)==digest,'artifact '+path)
original=load(B/'candidate-native-cf1-read-20261014/cases.json')
equal(m['original_ids'],[x['id'] for x in original['cases']],'original ordered ids')
equal(m['original_fixtures'],original['fixtures'],'original fixtures')
for old,new in zip(original['cases'],m['cases']):equal({k:v for k,v in old.items() if k!='expected'},{k:v for k,v in new.items() if k not in ('kind','expected')},'original invocation '+old['id'])
ids=[x['id'] for x in m['cases']];byid={x['id']:x for x in m['cases']}
demand(len(ids)==len(byid)==1098,'1098 distinct IDs')
launches=load(R/'LAUNCHES.json');actual_launches=[];positive=[];negative_results=[]
for optimization in (0,1):
 for mode in ('text','type','stage','trace','positive'):
  stem=f'{mode}-o{optimization}-01';p=R/f'evidence/{stem}.json';a=load(p);l=load(R/f'evidence/{stem}-launch.json');actual_launches.append(l)
  equal(a['mode'],mode,stem+' mode');equal(a['optimize'],optimization,stem+' optimization')
  equal(a['verified_pins'],650,stem+' checked pin count');equal(a['manifest_sha256'],pre['manifest_sha256'],stem+' manifest');equal(a['pins_sha256'],pre['pins_sha256'],stem+' pins')
  equal(l['result_sha256'],sha(p),stem+' launch hash');equal(l['stdout'],'',stem+' stdout')
  command=[str(B/'repo/.venv/bin/python'),'-B']+(['-O'] if optimization else [])+[str(R/'run.py'),mode,f'evidence/{stem}.json']
  equal(l['command'],command,stem+' exact launch command')
  if mode=='positive':
   equal(a['status'],'PASS',stem+' status');equal(l['exit'],0,stem+' exit');equal(l['stderr'],'',stem+' stderr');equal(a['negative'],None,stem+' no negative');equal([o['id'] for o in a['observations']],ids,stem+' complete ordered IDs')
   for c,o in zip(m['cases'],a['observations']):
    expected={'id':c['id'],'actual':c['expected'],'decode_hook_completed':c.get('source_kind')=='decode-expiry','synthetic_nonce_calls':1 if c['kind']=='seal' else 0}
    equal(o,expected,stem+' exact full observation '+c['id'])
   positive.append(a['observations'])
  else:
   equal(a['status'],'FAIL',stem+' status');equal(l['exit'],1,stem+' exit');equal(a['error_type'],'RuntimeError',stem+' error class');equal(a['error'],'Exact admission mismatch',stem+' error message');demand(l['stderr'].rstrip().endswith('RuntimeError: Exact admission mismatch'),stem+' traceback signature');equal(a['observations'],[],stem+' no observations')
   n=a['negative'];ctl=next(c for c in m['negative_controls'] if c['mode']==mode);equal(n['mode'],mode,stem+' control mode');equal(n['case_id'],ctl['case_id'],stem+' control ID');equal(n['original_verified'],True,stem+' verified actual');equal(n['original'],byid[ctl['case_id']]['expected'],stem+' original actual')
   changed=[k for k in set(n['original'])|set(n['mutated']) if canonical(n['original'].get(k))!=canonical(n['mutated'].get(k))];field={'text':'value','type':'value_type','stage':'stage','trace':'trace'}[mode];equal(changed,[field],stem+' one targeted field changed')
   desired={'text':lambda:n['original']['value']+'!ADMISSION-NEGATIVE!','type':lambda:'bytes','stage':lambda:'deliberately-wrong-stage','trace':lambda:n['original']['trace']+n['original']['trace'][:1]}[mode]()
   equal(n['mutated'][field],desired,stem+' exact mutation');negative_results.append({'mode':mode,'optimization':optimization,'case_id':n['case_id'],'field':field})
equal(actual_launches,launches,'LAUNCHES exact ten ordered receipts');equal(positive[0],positive[1],'O0 O1 full observations equal')
demand(not list((R/'evidence').glob('*timeout*')),'no timeout receipts')
summary={'status':'PASS','scope':'Independent data-only postrun audit; not historical execution attestation or full DESIGN approval','checks_passed':len(checks),'pins_checked':len(pins),'artifacts_checked':len(art),'cases_per_mode':len(ids),'outcomes_per_mode':dict(collections.Counter(c['expected'].get('exception',c['expected'].get('value_type')) for c in m['cases'])),'negative_controls':negative_results,'manifest_sha256':sha(R/'cases.json'),'pins_sha256':sha(R/'PINS.json'),'artifacts_sha256':sha(R/'ARTIFACTS.json'),'positive_receipt_sha256':{str(o):sha(R/f'evidence/positive-o{o}-01.json') for o in (0,1)},'all_checks':checks}
(N/'POSTRUN_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='all_checks'},indent=2))

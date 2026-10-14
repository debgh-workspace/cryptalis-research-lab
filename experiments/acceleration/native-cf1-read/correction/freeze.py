"""Freeze exact new oracles without importing or executing native candidate."""
import copy
import hashlib
import json
import sys
from pathlib import Path
from uuid import UUID
ROOT=Path(__file__).parent.absolute();ORIGINAL=ROOT.parent/'candidate-native-cf1-read-20261014'
sys.path[:0]=[str(ROOT),str(ROOT.parent/'candidate-s20-restored-20261014/src')]
import support as s
from cryptalis.crypto import cf1
from cryptalis.crypto import keys as k

old=json.loads((ORIGINAL/'cases.json').read_text())
fixtures={};cases=[]

def get(stem):
    name='grid-'+stem+'-1';spec=copy.deepcopy(old['fixtures'][name]);spec['frame_origin']='original'
    spec['text']='abcdefg';spec['encoded_text']=spec['text'].encode().hex()
    fixtures[name]=spec;return name,spec

def add(identity,kind,name,expected,native_calls,**extra):
    cases.append({'id':identity,'kind':kind,'fixture':name,'expected':expected,'native_calls':native_calls,**extra})

for eq in (0,1):
 for big in (0,1):
  for single in (0,1):
    stem=f'{eq}{big}{single}';name,orig=get(stem)
    altered=copy.deepcopy(orig);altered['descriptor']['table_id']=str(UUID(int=222))
    if single:altered['tenant_id']=str(UUID(int=222))
    altered['descriptor_digest']=hashlib.sha256(json.dumps(altered['descriptor'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    altered_name='table-'+stem;fixtures[altered_name]=altered
    f,t,r=s.values(altered);arguments=(s.frame(altered),f,t,r,s.keys(altered))
    expected=s.expected_failure(altered,k.AuthenticationFailed,['payload','search'] if eq else ['payload'])
    if s.observe(cf1.open_text,arguments)!=expected:raise RuntimeError('Table oracle disagreement')
    add('table-derived/'+stem,'context',altered_name,expected,1)
    for label in ('valid','malformed'):
        expected=s.expected_failure(orig,k.KeyUnavailable,[])
        f,t,r=s.values(orig);raw=s.frame(orig) if label=='valid' else b''
        observed=s.observe(cf1.open_text,(raw,f,t,r,s.keys(orig,policy_domain=str(UUID(int=333)))))
        if observed!=expected:raise RuntimeError('Policy-domain oracle disagreement')
        add('policy-domain/'+stem+'/'+label,'context',name,expected,0,
            policy_domain=str(UUID(int=333)),empty_frame=label=='malformed')

(ROOT/'fixtures').mkdir()
for eq in (0,1):
    name,a=get(f'{eq}00');b=copy.deepcopy(a)
    b['tenant_id']=str(UUID(int=444));b['record_id']=str(UUID(int=555))
    b['text']='scope-B-雪';b['encoded_text']=b['text'].encode().hex();b['frame_origin']='correction'
    bname='scope-B-'+str(eq);path=ROOT/'fixtures'/(bname+'.bin');f,t,r=s.values(b)
    raw=cf1.seal_text(b['text'],f,t,r,s.keys(b))
    with path.open('xb') as out:out.write(raw)
    b['frame_path']=str(path.relative_to(ROOT));b['frame_sha256']=hashlib.sha256(raw).hexdigest();fixtures[bname]=b
    # Exact independent round-trip is part of new fixture construction, not an old candidate check.
    if cf1.open_text(raw,f,t,r,s.keys(b))!=b['text']:raise RuntimeError('New scope fixture invalid')
    for step,which in enumerate((name,bname,name)):
        spec=fixtures[which]
        add(f'scope/{eq}/{step}','scope',which,s.expected_success(spec,spec['text']),1,group='scope-'+str(eq))
    add(f'scope-null/{eq}','scope',name,s.expected_success(a,None),0,group='scope-'+str(eq),null_frame=True)
    for step,state in enumerate(('valid','expire','fresh')):
        expected=s.expected_failure(a,k.KeyUnavailable,['payload']) if state=='expire' else s.expected_success(a,a['text'])
        add(f'lifecycle/{eq}/{state}','lifecycle',name,expected,0 if state=='expire' else 1,
            group='life-'+str(eq),state=state)
    for purpose in (('payload','search') if eq else ('payload',)):
        before=['payload','search'] if eq else ['payload']
        after=['payload','search'] if purpose=='search' else ['payload']
        add(f'decode-expiry/{eq}/{purpose}','decode-expiry',name,
            s.expected_failure(a,k.KeyUnavailable,before+after),1,purpose=purpose)
    before=['payload','search'] if eq else ['payload']
    add(f'post-native-pid/{eq}','post-native-pid',name,s.expected_failure(a,k.KeyUnavailable,before+['payload']),1)

negative={'id':'actual-output-perturbation','fixture':'grid-100-1',
    'original_expected':s.expected_success(fixtures['grid-100-1'],'abcdefg'),
    'mutation':'append literal !CORRECTION-NEGATIVE! to actual candidate result AFTER validating unmodified result',
    'expected_exit':1,'expected_error':'Mismatch: actual-output-perturbation','native_calls':1}
ids=[c['id'] for c in cases]
if len(cases)!=43 or len(set(ids))!=43:raise RuntimeError('Unexpected finite case list')
manifest={'scope':'New correction only; full DESIGN HOLD, no timings','positive_count':43,'cases':cases,
 'negative':negative,'fixtures':fixtures,'optimization_modes':[0,1],
 'expected_python':'3.12.14','expected_oracle':'50.0.2 / OpenSSL 4.0.3 29 Sep 2026','expected_native':'OpenSSL 3.5.7 9 Jun 2026'}
with (ROOT/'cases.json').open('x') as out:json.dump(manifest,out,indent=2,ensure_ascii=False);out.write('\n')
print(json.dumps({'status':'FROZEN','positive_cases':43,'negative_cases':1,
 'manifest_sha256':hashlib.sha256((ROOT/'cases.json').read_bytes()).hexdigest()}))

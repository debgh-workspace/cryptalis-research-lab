"""Freeze source-policy expectations without importing crypto or candidate."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent; B=R.parent; O=B/'candidate-native-cf1-read-20261014'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
    with (R/n).open('x') as f:json.dump(v,f,indent=2);f.write('\n')
build=json.loads((O/'build-04-diagnostic/build.json').read_text())
for n,h in build['pins'].items():
    if sha(Path(n))!=h:raise RuntimeError('Original pin mismatch: '+n)
old=json.loads((O/'cases.json').read_text()); sites=json.loads((O/'fault-sites.json').read_text())
# Stage categories are independently specified from MAPPING.md and pinned pyca
# process_data map_err(InvalidTag), rather than native status strings/mapper.
policy={'cipher.data':'AuthenticationFailed','cipher.final':'AuthenticationFailed'}
backend={'exception':'CryptoBackendUnavailable','code':'CryptoBackendUnavailable','stage':'cryptographic backend','retryable':True,'effects':'none','remedy':'Check OS randomness and the installed cryptography backend. Do not switch algorithms.','operation_present':True,'cause_suppressed':True}
auth={'exception':'AuthenticationFailed','code':'AuthenticationFailed','stage':'authentication','retryable':False,'effects':'none','remedy':'Check expected context and exact admitted roots; investigate possible data alteration.','operation_present':True,'cause_suppressed':True}
fixtures={k:old['fixtures'][k] for k in ('grid-000-1','grid-100-1')}
cases=[]
for fid,s in fixtures.items():
    eq=bool(s['search_generation']); pre=['payload','search'] if eq else ['payload']
    def expected(error=None):
        v=dict(auth if error=='AuthenticationFailed' else backend) if error else {'value':'abcdefg','value_type':'str'}
        purposes=pre if error else pre+pre
        v['trace']=[[s['descriptor']['domain_id'],s['tenant_id'],p,s[p+'_generation']] for p in purposes]
        v['native_calls']=1
        return v
    for number,label in sites.items():
        if not eq and (label.startswith('search.') or label.startswith('mac.')):continue
        category=policy.get(label,'CryptoBackendUnavailable')
        group=f'{fid}/{number}'
        for phase,selector in [('before',0),('fault',int(number)),('recovery',0)]:
            cases.append({'id':group+'/'+phase,'group':group,'fixture':fid,'selector':selector,'bad_tag':False,'site':label,'expected':expected(category if phase=='fault' else None)})
    for selector,category in [(0,'AuthenticationFailed'),(13,'CryptoBackendUnavailable')]+([(21,'AuthenticationFailed')] if eq else []):
        cases.append({'id':fid+'/bad-tag/'+str(selector),'group':fid+'/bad-tag/'+str(selector),'fixture':fid,'selector':selector,'bad_tag':True,'expected':expected(category)})
save('cases.json',{'scope':'Finite source-policy fault oracle; full admission HOLD','policy_sources':['candidate-notes-native-failure-mapping-20261014/MAPPING.md','candidate-notes-native-failure-mapping-20261014/pyca-aead.rs:318-319','candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py:203-210','candidate-s20-restored-20261014/src/cryptalis/crypto/keys.py:22-72'],'fixtures':fixtures,'cases':cases,'negative_fields':['stage','trace']})
pins=dict(build['pins'])
for tree in [O,B/'candidate-notes-native-failure-mapping-20261014']:
    for p in tree.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
for p in R.glob('*.py'):pins[str(p)]=sha(p)
pins[str(R/'cases.json')]=sha(R/'cases.json')
save('PINS.json',{'pins':pins,'build_manifest_sha256':sha(O/'build-04-diagnostic/build.json')})
save('FREEZE.json',{'cases':len(cases),'cases_sha256':sha(R/'cases.json'),'pins_sha256':sha(R/'PINS.json'),'pin_count':len(pins),'candidate_imported':False})
print(len(cases),len(pins))

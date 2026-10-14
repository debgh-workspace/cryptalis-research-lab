"""Exact assertion-independent bounded public-fixture diagnostic oracle."""
import hashlib,importlib,json,sys,sysconfig
from pathlib import Path
from uuid import UUID
R=Path(__file__).absolute().parent;B=R.parent
mode=sys.argv[1];outfile=R/sys.argv[2]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def equal(a,b):
    if type(a) is not type(b) or a!=b: raise RuntimeError('Exact oracle mismatch')
pins=json.loads((R/'PINS.json').read_text())
for path,d in pins['pins'].items(): equal(sha(path),d)
equal(sys.executable,str(B/'repo/.venv/bin/python'));equal(tuple(sys.version_info[:3]),(3,12,14))
if sys.flags.optimize not in (0,1): raise RuntimeError('Optimization mode')
equal(sha(R/'cases.json'),pins['cases_sha256'])
manifest=json.loads((R/'cases.json').read_text());cases=manifest['cases']
equal(len(cases),14);equal(len({v['id'] for v in cases}),14)
native=importlib.import_module('native_cf1');equal(native.__file__,pins['binary'])
equal(native.backend_version(),'OpenSSL 3.5.7 9 Jun 2026')
def observe(case):
    v=case['input'];h=bytes.fromhex; k=case['kind']
    if k=='aes':
        return {'sealed':native.primitive('seal',h(v['key']),h(v['nonce']),h(v['aad']),h(v['plaintext'])).hex(),'plaintext':native.primitive('open',h(v['key']),h(v['nonce']),h(v['aad']),h(v['sealed'])).hex()}
    if k=='hkdf_sha256': return {'output':native.primitive('hkdf',h(v['ikm']),h(v['salt']),h(v['info']),bytes([v['length']])).hex()}
    if k=='hmac_sha256': return {'output':native.primitive('hmac',h(v['key']),h(v['message']),b'',b'').hex()}
    def material(p): return (h(v[p+'_root']),UUID(v['domain_id']).bytes,UUID(v['tenant_id']).bytes,UUID(v[p+'_root_id']).bytes,v[p+'_generation'].to_bytes(4,'big'))
    result=native.intermediates(h(v['frame']),int(bool(v['search_generation'])),UUID(v['domain_id']).bytes,UUID(v['tenant_id']).bytes,UUID(v['field_id']).bytes,h(v['descriptor_digest']),h(v['typed_record_id']),material('payload'),material('search') if v['search_generation'] else None)
    equal(type(result),dict)
    for x in result.values(): equal(type(x),bytes)
    return {**{k:b.hex() for k,b in result.items()},'text':result['encoded_text'].decode('utf8','strict')}
receipt={'mode':mode,'optimize':sys.flags.optimize,'python':sys.version,'python_executable':sys.executable,'soabi':sysconfig.get_config_var('SOABI'),'pins_sha256':sha(R/'PINS.json'),'cases_sha256':sha(R/'cases.json'),'binary_sha256':sha(pins['binary']),'backend':native.backend_version(),'observations':[]}
exitcode=0
try:
    if mode=='positive':
        for case in cases:
            actual=observe(case);equal(actual,case['expected']);receipt['observations'].append({'id':case['id'],'actual':actual})
        equal([o['id'] for o in receipt['observations']],[c['id'] for c in cases]);receipt['status']='PASS'
    else:
        control=next(c for c in manifest['negative_controls'] if c['id']==mode)
        case=next(c for c in cases if c['id']==control['case_id'])
        actual=observe(case);equal(actual,case['expected']);receipt['original_verified']=True
        receipt['unmodified_actual']=actual.copy();field=control['field'];actual[field]=('00' if actual[field][:2]!='00' else '01')+actual[field][2:]
        receipt['perturbed_actual']=actual;receipt['control']=control
        equal(actual,case['expected']);raise RuntimeError('Negative control escaped')
except Exception as e:
    receipt['status']='FAIL';receipt['exception']=type(e).__name__;receipt['message']=str(e);exitcode=1
with outfile.open('x') as f: json.dump(receipt,f,indent=2);f.write('\n')
raise SystemExit(exitcode)

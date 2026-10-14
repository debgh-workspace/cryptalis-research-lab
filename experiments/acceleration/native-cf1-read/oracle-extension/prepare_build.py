"""Freeze public expectations and compile once; no crypto execution."""
import hashlib,json,subprocess,sys,sysconfig
from pathlib import Path
R=Path(__file__).absolute().parent; B=R.parent
PY=str(B/'repo/.venv/bin/python')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    with p.open('x') as f: json.dump(x,f,indent=2);f.write('\n')
if sys.executable!=PY or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize: raise RuntimeError('Python pin')
p=B/'candidate-s20-restored-20261014/tests/fixtures/cf1_vectors.json'
if sha(p)!='24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e': raise RuntimeError('Fixture pin')
f=json.loads(p.read_text()); cases=[]
for i,v in enumerate(f['primitive_vectors']['aes256_gcm_siv']): cases.append({'id':f'primitive/aes256-gcm-siv/{i}','kind':'aes','input':v,'expected':{'sealed':v['sealed'],'plaintext':v['plaintext']}})
for kind in ['hkdf_sha256','hmac_sha256']:
    v=f['primitive_vectors'][kind];cases.append({'id':'primitive/'+kind,'kind':kind,'input':v,'expected':{'output':v['output']}})
fields=['payload_salt','payload_key','search_salt','search_key','header','aad','term','encoded_text']
for v in f['vectors']:
    if bytes.fromhex(v['encoded_text']).decode('utf8')!=v['text']: raise RuntimeError('Frozen text mismatch')
    cases.append({'id':'intermediate/'+v['name'],'kind':'intermediate','input':v,'expected':{**{k:v[k] for k in fields},'text':v['text']}})
if len(cases)!=14 or len({x['id'] for x in cases})!=14: raise RuntimeError('Case list')
write(R/'cases.json',{'fixture':str(p),'fixture_sha256':sha(p),'cases':cases,'negative_controls':[{'id':'wrong-hkdf','case_id':'primitive/hkdf_sha256','field':'output'},{'id':'wrong-intermediate','case_id':'intermediate/'+f['vectors'][0]['name'],'field':'payload_key'}]})
# Verify and retain inherited sources/dependency pins without importing candidate/product.
pins=json.loads((B/'candidate-native-cf1-read-correction-20261014/PINS.json').read_text())['pins']
for path,d in pins.items():
    if sha(path)!=d: raise RuntimeError('Inherited pin changed: '+path)
originals={str(p):sha(p) for name in ['candidate-native-cf1-read-20261014','candidate-native-cf1-read-correction-20261014','candidate-notes-native-correction-audit-20261014','candidate-notes-native-cf1-design-20261014'] for p in (B/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
write(R/'ORIGINALS.json',originals)
for path in R.iterdir():
    if path.is_file(): pins[str(path)]=sha(path)
write(R/'PREBUILD.json',{'pins':pins,'cases_sha256':sha(R/'cases.json')})
include='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12'
binary=R/('native_cf1'+sysconfig.get_config_var('EXT_SUFFIX'))
cmd=['/usr/bin/gcc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-std=c11','-DCF1_DIAGNOSTIC','-I'+include,str(R/'native_cf1.c'),'-lcrypto','-o',str(binary)]
r=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
rec={'command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'compiler':subprocess.check_output(['/usr/bin/gcc','--version'],text=True),'python':sys.version,'python_executable':sys.executable,'soabi':sysconfig.get_config_var('SOABI'),'prebuild_sha256':sha(R/'PREBUILD.json')}
write(R/'build-01.json',rec)
if r.returncode: raise SystemExit(r.returncode)
linked=subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True)
for line in linked.splitlines():
    for word in line.split():
        if word.startswith('/') and Path(word).is_file(): pins[word]=sha(word)
pins[str(binary)]=sha(binary);pins[str(R/'build-01.json')]=sha(R/'build-01.json');pins[str(R/'PREBUILD.json')]=sha(R/'PREBUILD.json')
for path,d in pins.items():
    if sha(path)!=d: raise RuntimeError('Build pin changed: '+path)
write(R/'PINS.json',{'pins':pins,'binary':str(binary),'ldd':linked,'cases_sha256':sha(R/'cases.json')})
print('Frozen 14 cases; diagnostic build complete')

"""Pin immutable old artifacts, freeze new oracles, then seal new input manifest."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).parent.absolute();BASE=ROOT.parent;OLD=BASE/'candidate-native-cf1-read-20261014'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
if sys.executable!=str(BASE/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize!=0:
    raise RuntimeError('Preparation requires pinned Python, optimization zero')
if sha(OLD/'ARTIFACTS.json')!='bd6fba6d773ca746ae8ac0bc4ecc0f539f95fcf244b488b3bd6bc9e191ea81a8':
    raise RuntimeError('Original final inventory changed')
old_artifacts=json.loads((OLD/'ARTIFACTS.json').read_text())['files']
pins={str(OLD/name):pin for name,pin in old_artifacts.items()}
pins[str(OLD/'ARTIFACTS.json')]=sha(OLD/'ARTIFACTS.json')
pins.update(json.loads((OLD/'build-03-normal/build.json').read_text())['pins'])
for name,pin in pins.items():
    if sha(name)!=pin:raise RuntimeError('Original artifact/dependency changed: '+name)
import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
if cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Oracle version mismatch')
cmd=[sys.executable,'-B',str(ROOT/'freeze.py')]
result=subprocess.run(cmd,capture_output=True,text=True,timeout=60,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
record={'command':cmd,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
    'python_executable':sys.executable,'python':sys.version,'optimize':sys.flags.optimize,'old_artifact_count':len(old_artifacts),
    'original_inventory_sha256':sha(OLD/'ARTIFACTS.json'),'scope':'New baseline oracle construction; no native candidate imports or old tests'}
if (ROOT/'cases.json').is_file():record['case_manifest_sha256']=sha(ROOT/'cases.json')
with (ROOT/'evidence/freeze-01.json').open('x') as out:json.dump(record,out,indent=2);out.write('\n')
if result.returncode:raise RuntimeError('New oracle construction failed; preserved receipt')
for name,pin in pins.items():
    if sha(name)!=pin:raise RuntimeError('Original changed during construction: '+name)
for path in ROOT.rglob('*'):
    if path.is_file() and path.name!='PINS.json':pins[str(path)]=sha(path)
with (ROOT/'PINS.json').open('x') as out:json.dump({'scope':'New finite correction pinned before native import','pins':pins},out,indent=2);out.write('\n')
print(result.stdout.strip());print(json.dumps({'pins':len(pins),'pins_sha256':sha(ROOT/'PINS.json')}))

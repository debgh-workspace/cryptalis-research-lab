"""Verify inherited evidence and freeze complete exact oracle with stdlib only."""
import ast,hashlib,json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).absolute().parent;B=R.parent;O=B/'candidate-native-cf1-read-20261014';C=B/'candidate-native-cf1-read-correction-20261014'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14):raise RuntimeError('Pinned Python required')
pins=json.loads((O/'build-03-normal/build.json').read_text())['pins']
for directory in (O,C,B/'candidate-native-read-admission-20261014'):
    inventory=json.loads((directory/'ARTIFACTS.json').read_text())['files']
    for name,h in inventory.items():pins[str(directory/name)]=h
    pins[str(directory/'ARTIFACTS.json')]=sha(directory/'ARTIFACTS.json')
for name,h in pins.items():
    if sha(Path(name))!=h:raise RuntimeError('Inherited pin mismatch: '+name)
for path in R.glob('*.py'):
    tree=ast.parse(path.read_text())
    if any(isinstance(n,ast.Assert) for n in ast.walk(tree)):raise RuntimeError('Assert-based checks')
cmd=[sys.executable,'-B',str(R/'freeze.py')]
p=subprocess.run(cmd,capture_output=True,text=True,timeout=90,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
record={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'crypto_imports':False}
if (R/'cases.json').exists():record['manifest_sha256']=sha(R/'cases.json')
with (R/'evidence/freeze-01.json').open('x') as out:json.dump(record,out,indent=2);out.write('\n')
if p.returncode:raise RuntimeError('Freeze failed; preserve failure before correction')
for name,h in pins.items():
    if sha(Path(name))!=h:raise RuntimeError('Inherited pin changed')
for path in R.rglob('*'):
    if path.is_file() and path.name!='PINS.json':pins[str(path)]=sha(path)
with (R/'PINS.json').open('x') as out:json.dump({'scope':'Frozen before any candidate import; new exact-output oracle only','pins':pins},out,indent=2);out.write('\n')
print(json.dumps({'manifest_sha256':sha(R/'cases.json'),'pins_sha256':sha(R/'PINS.json'),'pins':len(pins)}))

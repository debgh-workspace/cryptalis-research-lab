import hashlib,json,os,subprocess,sys,sysconfig
from pathlib import Path
R=Path(__file__).absolute().parent;B=R.parent;O=B/'candidate-native-cf1-read-20261014';F=B/'candidate-native-fault-oracles-20261014'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14):raise RuntimeError('Interpreter pin')
pins=json.loads((F/'PINS.json').read_text())['pins']
for p,h in pins.items():
    if sha(p)!=h:raise RuntimeError('Old pin mismatch '+p)
# All originals preserved, including prior admission and audits.
for directory in [O,F,B/'candidate-native-read-admission-20261014']:
    for p in directory.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
for p in R.iterdir():
    if p.is_file():pins[str(p)]=sha(p)
save(R/'SOURCE_PINS.json',{'pins':pins})
include='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12'
for p in list(Path(include).rglob('*.h'))+list(Path('/usr/include/openssl').glob('*.h'))+[Path('/usr/bin/gcc'),Path('/usr/libexec/gcc/x86_64-linux-gnu/14/cc1'),Path('/usr/bin/ld'),Path('/usr/bin/as')]:pins[str(p)]=sha(p)
build=R/'build';build.mkdir();binary=build/('native_cf1'+sysconfig.get_config_var('EXT_SUFFIX'))
command=['/usr/bin/gcc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-std=c11','-DCF1_DIAGNOSTIC','-I'+include,str(R/'native_cf1.c'),'-lcrypto','-o',str(binary)]
proc=subprocess.run(command,capture_output=True,text=True,timeout=60)
receipt={'command':command,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'binary':str(binary),'python':sys.version,'soabi':sysconfig.get_config_var('SOABI'),'pins':pins,'cryptography_origin':json.loads((O/'build-04-diagnostic/build.json').read_text())['cryptography_origin']}
if proc.returncode==0:
    linked=subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True);receipt['ldd']=linked
    for word in linked.split():
        if word.startswith('/') and Path(word).is_file():pins[word]=sha(word)
    pins[str(binary)]=sha(binary)
save(build/'build.json',receipt)
if proc.returncode:raise RuntimeError('Compile failed')
for p,h in pins.items():
    if sha(p)!=h:raise RuntimeError('Pin changed '+p)
pins[str(build/'build.json')]=sha(build/'build.json')
pins[str(R/'SOURCE_PINS.json')]=sha(R/'SOURCE_PINS.json')
save(R/'PINS.json',{'pins':pins})
print(json.dumps({'compiled':str(binary),'pins':len(pins)}))

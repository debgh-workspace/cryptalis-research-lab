"""Bounded isolated compile/provenance driver. No installs or benchmarks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig

ROOT=Path(__file__).parent.absolute();BASE=ROOT.parent
EXPECTED_PY=str(BASE/'repo/.venv/bin/python')
S20=BASE/'candidate-s20-restored-20261014'
if sys.executable!=EXPECTED_PY or sys.version_info[:3]!=(3,12,14): raise RuntimeError('Pinned executable/version required')
if sys.flags.optimize!=0: raise RuntimeError('Build uses optimization flag zero')
PINS={'src/cryptalis/crypto/cf1.py':'d74abd2558023bf5ce1598fba0b61bb27198623dc56fb94ace24753531705278',
'src/cryptalis/crypto/keys.py':'b76d60f32011705726cc73f6211fa52e5624e475fc63573e578aa9e5078aea56',
 'tests/fixtures/cf1_vectors.json':'24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e'}
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
for path,pin in PINS.items():
    if digest(S20/path)!=pin: raise RuntimeError('S20 source/fixture pin mismatch')
import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
if cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026': raise RuntimeError('Pinned oracle versions required')
if str(BASE/'repo/.venv/') not in str(cryptography.__file__): raise RuntimeError('Wrong oracle origin')
mode=sys.argv[1]; build=ROOT/sys.argv[2]
if mode not in ('normal','diagnostic','skip-term','sanitizer'): raise RuntimeError('Unknown build mode')
build.mkdir(); binary=build/('native_cf1'+sysconfig.get_config_var('EXT_SUFFIX'))
flags=['-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-std=c11']
if mode!='normal': flags+=['-DCF1_DIAGNOSTIC']
if mode=='skip-term': flags+=['-DCF1_SKIP_TERM']
if mode=='sanitizer': flags+=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer']
include=Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12')
if not (include/'Python.h').is_file(): raise RuntimeError('Pinned include missing')
command=['/usr/bin/gcc',*flags,'-I'+str(include),str(ROOT/'native_cf1.c'),'-lcrypto','-o',str(binary)]
inputs=[ROOT/'native_cf1.c',ROOT/'native_read.py',ROOT/'SCOPE.md',ROOT/'fault-sites.json',ROOT/'fixture_support.py',ROOT/'generate_cases.py',ROOT/'validate.py',ROOT/'build.py',ROOT/'launch.py',Path(EXPECTED_PY)]
inputs+=list((S20/'src/cryptalis').rglob('*.py'))+[S20/'tests/fixtures/cf1_vectors.json']
inputs+=list(Path(cryptography.__file__).parent.rglob('*.py'))+list(Path(cryptography.__file__).parent.rglob('*.so'))
inputs+=list(include.rglob('*.h'))+list(Path('/usr/include/openssl').glob('*.h'))
inputs += [Path('/usr/bin/gcc'), Path('/usr/libexec/gcc/x86_64-linux-gnu/14/cc1'), Path('/usr/bin/ld'), Path('/usr/bin/as')]
inputs+=list(ROOT.glob('cases.json'))+list((ROOT/'fixtures').glob('*.bin'))
pins={str(path):digest(path) for path in inputs}
proc=subprocess.run(command,capture_output=True,text=True,timeout=60)
receipt={'scope':'Correctness-only compile; no timing','command':command,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,
 'python_executable':sys.executable,'python':sys.version,'optimize':sys.flags.optimize,'soabi':sysconfig.get_config_var('SOABI'),
 'cryptography':cryptography.__version__,'cryptography_origin':cryptography.__file__,'pyca_backend':backend.openssl_version_text(),
 'compiler':subprocess.check_output(['/usr/bin/gcc','--version'],text=True),'mode':mode,'pins':pins}
if proc.returncode==0:
    linked=subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True); receipt['ldd']=linked
    dependencies=[]
    for line in linked.splitlines():
        for word in line.split():
            if word.startswith('/') and Path(word).is_file(): dependencies.append(word)
    receipt['pins'].update({path:digest(path) for path in dependencies})
    receipt['pins'][str(binary)]=digest(binary);receipt['binary']=str(binary)
for path,pin in pins.items():
    if digest(path)!=pin: raise RuntimeError('Build input changed')
with (build/'build.json').open('x') as out: json.dump(receipt,out,indent=2);out.write('\n')
print(json.dumps({'mode':mode,'exit':proc.returncode,'receipt':str(build/'build.json')}))
sys.exit(proc.returncode)

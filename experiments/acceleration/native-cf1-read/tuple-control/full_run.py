"""Future full-wrapper child; no execution authorized by source preparation."""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import sysconfig
R=Path(__file__).parent.absolute();B=R.parent;O=B/'candidate-native-cf1-read-20261014'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
mode,name=sys.argv[1:]
dest=R/name
receipt={'status':'FAIL','mode':mode,'optimize':sys.flags.optimize,'observations':[],'negative':None}
runtime=None
untouched=None
p=None
try:
    p=json.loads((R/'FULL_RUN_FREEZE.json').read_text())
    if mode not in p['modes'] or dest.exists() or not dest.parent.is_dir():raise RuntimeError('Invalid launch')
    if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize not in (0,1) or sysconfig.get_config_var('SOABI')!='cpython-312-x86_64-linux-gnu':raise RuntimeError('Python mismatch')
    if any(k in os.environ for k in p['reject_environment']):raise RuntimeError('Environment override')
    for name,h in p['pins'].items():
        if sha(name)!=h:raise RuntimeError('Pin mismatch: '+name)
    for name in ('full_runtime.py','full_run.py','full_launch.py'):
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((R/name).read_text()))):raise RuntimeError('Assertion-based check')
    receipt.update(freeze_sha256=sha(R/'FULL_RUN_FREEZE.json'),verified_pins=len(p['pins']),hooks_sha256=sha(R/'FULL_HOOKS.json'))
    build=R/'build-direct-01-normal';bm=json.loads((build/'build.json').read_text())
    if bm['status']!='BUILT' or bm['mode']!='normal':raise RuntimeError('Normal build required')
    sys.path[:0]=[str(build),str(R),str(O),str(B/'candidate-s20-restored-20261014/src')]
    import cryptography,native_tuple,tuple_read,fixture_support
    from cryptography.hazmat.backends.openssl.backend import backend
    from cryptalis.crypto import cf1,keys
    if native_tuple.__file__!=bm['binary'] or hasattr(native_tuple,'tuple_alloc_failure'):raise RuntimeError('Wrong native surface/origin')
    if cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026' or cryptography.__file__!=p['cryptography_origin']:raise RuntimeError('Wrong Python crypto backend')
    for module,path in [(tuple_read,R/'tuple_read.py'),(fixture_support,O/'fixture_support.py'),(cf1,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py'),(keys,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/keys.py')]:
        if Path(module.__file__)!=path:raise RuntimeError('Wrong module origin')
    untouched=(cf1.tuple_bytes,cf1.open_text,cf1._derive,cf1._term,cf1._aad,cf1.os,cf1.os.urandom)
    receipt.update(python=sys.version,python_executable=sys.executable,native_origin=native_tuple.__file__,crypto_origin=cryptography.__file__,crypto_backend=backend.openssl_version_text())
    import full_runtime as runtime
    runtime.run(mode)
    if untouched!=(cf1.tuple_bytes,cf1.open_text,cf1._derive,cf1._term,cf1._aad,cf1.os,cf1.os.urandom):raise RuntimeError('Canonical baseline mutated')
    for name,h in p['pins'].items():
        if sha(name)!=h:raise RuntimeError('Post-run pin changed')
    receipt['status']='PASS'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc))
    raise
finally:
    if untouched is not None and untouched!=(cf1.tuple_bytes,cf1.open_text,cf1._derive,cf1._term,cf1._aad,cf1.os,cf1.os.urandom):
        receipt.update(status='FAIL',error_type='RuntimeError',error='Canonical baseline mutated')
    if p is not None:
        for name,h in p['pins'].items():
            if sha(name)!=h:receipt.update(status='FAIL',error_type='RuntimeError',error='Final pin mismatch')
    if runtime is not None:
        receipt['observations']=runtime.observations;receipt['negative']=runtime.negative_record
    with dest.open('x') as out:json.dump(receipt,out,ensure_ascii=False,indent=2);out.write('\n')

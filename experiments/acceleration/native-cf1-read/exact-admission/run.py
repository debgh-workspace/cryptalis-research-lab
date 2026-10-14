"""Enforce all pins before candidate imports, exclusively record outcome."""
import ast,hashlib,json,sys,sysconfig
from pathlib import Path
R=Path(__file__).absolute().parent;B=R.parent;O=B/'candidate-native-cf1-read-20261014'
mode=sys.argv[1];dest=R/sys.argv[2]
if mode not in ('positive','text','type','stage','trace') or dest.exists():raise RuntimeError('Invalid launch')
receipt={'status':'FAIL','mode':mode,'optimize':sys.flags.optimize,'observations':[],'negative':None}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
try:
    pins=json.loads((R/'PINS.json').read_text())['pins']
    for name,h in pins.items():
        if sha(Path(name))!=h:raise RuntimeError('Pin mismatch: '+name)
    receipt.update(verified_pins=len(pins),pins_sha256=sha(R/'PINS.json'),manifest_sha256=sha(R/'cases.json'))
    for p in R.glob('*.py'):
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))):raise RuntimeError('Assert-based check')
    if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize not in (0,1) or sysconfig.get_config_var('SOABI')!='cpython-312-x86_64-linux-gnu':raise RuntimeError('Python environment mismatch')
    sys.path[:0]=[str(O/'build-03-normal'),str(O),str(B/'candidate-s20-restored-20261014/src')]
    import cryptography,native_cf1,native_read,fixture_support
    from cryptography.hazmat.backends.openssl.backend import backend
    from cryptalis.crypto import cf1,keys
    build=json.loads((O/'build-03-normal/build.json').read_text())
    if native_cf1.__file__!=build['binary'] or native_cf1.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Native origin/backend mismatch')
    if cryptography.__file__!=build['cryptography_origin'] or cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Oracle origin/backend mismatch')
    for module,path in [(native_read,O/'native_read.py'),(fixture_support,O/'fixture_support.py'),(cf1,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py'),(keys,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/keys.py')]:
        if Path(module.__file__)!=path:raise RuntimeError('Source origin mismatch')
    receipt.update(python=sys.version,python_executable=sys.executable,native_origin=native_cf1.__file__,native_backend=native_cf1.backend_version(),oracle_backend=backend.openssl_version_text())
    import runtime
    runtime.run(mode);receipt['status']='PASS'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc));raise
finally:
    if 'runtime' in sys.modules:
        receipt['observations']=sys.modules['runtime'].observations;receipt['negative']=sys.modules['runtime'].negative_record
    with dest.open('x') as out:json.dump(receipt,out,ensure_ascii=False,indent=2);out.write('\n')

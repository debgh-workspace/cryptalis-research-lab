"""Pin old binary/dependencies plus new correction artifacts before imports."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import sysconfig
ROOT=Path(__file__).parent.absolute();BASE=ROOT.parent
ORIGINAL=BASE/'candidate-native-cf1-read-20261014'
mode=sys.argv[1];output=ROOT/'evidence'/sys.argv[2]
if mode not in ('positive','negative') or output.exists():raise RuntimeError('Invalid mode or existing receipt')
result={'status':'FAIL','mode':mode,'python_executable':sys.executable,'python':sys.version,'optimize':sys.flags.optimize,
        'passed':[],'observations':[],'scope':'Correction-only; original suite not rerun; full DESIGN HOLD; no timings'}
try:
    provenance=json.loads((ROOT/'PINS.json').read_text())
    for name,pin in provenance['pins'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=pin:raise RuntimeError('Pinned artifact changed: '+name)
    expected_python=str(BASE/'repo/.venv/bin/python')
    if sys.executable!=expected_python or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize not in (0,1):raise RuntimeError('Wrong Python environment')
    if sysconfig.get_config_var('SOABI')!='cpython-312-x86_64-linux-gnu':raise RuntimeError('Wrong Python ABI')
    result['pins_sha256']=hashlib.sha256((ROOT/'PINS.json').read_bytes()).hexdigest()
    result['verified_pin_count']=len(provenance['pins'])
    for name in ('launch.py','support.py','freeze.py','check.py'):
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((ROOT/name).read_text()))):raise RuntimeError('Assert-based check')
    sys.path[:0]=[str(ROOT),str(ORIGINAL/'build-03-normal'),str(ORIGINAL),str(BASE/'candidate-s20-restored-20261014/src')]
    import cryptography
    from cryptography.hazmat.backends.openssl.backend import backend
    if cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Wrong oracle version')
    old=json.loads((ORIGINAL/'build-03-normal/build.json').read_text())
    if cryptography.__file__!=old['cryptography_origin']:raise RuntimeError('Wrong oracle origin')
    import native_cf1,native_read
    from cryptalis.crypto import cf1,keys
    if native_cf1.__file__!=old['binary'] or native_cf1.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Wrong native origin/backend')
    for module,name in [(cf1,'cf1.py'),(keys,'keys.py')]:
        if Path(module.__file__)!=BASE/'candidate-s20-restored-20261014/src/cryptalis/crypto'/name:raise RuntimeError('Wrong source origin')
    if Path(native_read.__file__)!=ORIGINAL/'native_read.py':raise RuntimeError('Wrong wrapper origin')
    result.update(cryptography=cryptography.__version__,pyca_backend=backend.openssl_version_text(),native_backend=native_cf1.backend_version(),native_origin=native_cf1.__file__)
    import check
    check.run(negative=mode=='negative')
    result['passed']=check.passed;result['observations']=check.observations;result['status']='PASS'
except BaseException as exc:
    result['error_type']=type(exc).__name__;result['error']=str(exc)
    if 'check' in sys.modules:
        result['passed']=sys.modules['check'].passed;result['observations']=sys.modules['check'].observations
    raise
finally:
    with output.open('x') as out:json.dump(result,out,indent=2,ensure_ascii=False);out.write('\n')
    print(json.dumps({'status':result['status'],'passed':len(result['passed']),'receipt':str(output)}))

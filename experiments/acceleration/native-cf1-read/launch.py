"""Enforce frozen full input/binary/dependency pins BEFORE candidate import."""
import ast
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import sysconfig
ROOT=Path(__file__).parent.absolute();BASE=ROOT.parent
build=ROOT/sys.argv[1]; output=ROOT/'evidence'/sys.argv[2]
if output.exists(): raise RuntimeError('Evidence already exists')
receipt={'status':'FAIL','passed':[],'python_executable':sys.executable,'python':sys.version,'optimize':sys.flags.optimize,
         'soabi':sysconfig.get_config_var('SOABI'),'arguments':sys.argv[1:]}
try:
    manifest=json.loads((build/'build.json').read_text())
    if manifest['exit_code']!=0: raise RuntimeError('Cannot load a failed build')
    if sys.executable!=str(BASE/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14): raise RuntimeError('Wrong executable/version')
    if sys.flags.optimize not in (0,1) or sysconfig.get_config_var('SOABI')!=manifest['soabi']: raise RuntimeError('Wrong ABI/flags')
    for path,pin in manifest['pins'].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=pin: raise RuntimeError('Pinned artifact changed: '+path)
    receipt['build_manifest_sha256']=hashlib.sha256((build/'build.json').read_bytes()).hexdigest()
    receipt['pins']=manifest['pins']
    for path in ('validate.py','fixture_support.py','native_read.py','generate_cases.py','launch.py'):
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((ROOT/path).read_text()))): raise RuntimeError('Assert-based check found')
    sys.path[:0]=[str(build),str(ROOT),str(BASE/'candidate-s20-restored-20261014/src')]
    import cryptography
    from cryptography.hazmat.backends.openssl.backend import backend
    if cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026': raise RuntimeError('Wrong oracle environment')
    if cryptography.__file__!=manifest['cryptography_origin']: raise RuntimeError('Oracle import origin changed')
    import native_cf1
    if native_cf1.__file__!=manifest['binary']: raise RuntimeError('Wrong native import origin')
    if native_cf1.backend_version()!='OpenSSL 3.5.7 9 Jun 2026': raise RuntimeError('Wrong native backend')
    from cryptalis.crypto import cf1,keys
    if Path(cf1.__file__)!=BASE/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py': raise RuntimeError('Wrong source origin')
    receipt.update(cryptography=cryptography.__version__,pyca_backend=backend.openssl_version_text(),native_backend=native_cf1.backend_version(),source_origin=cf1.__file__,native_origin=native_cf1.__file__)
    import validate
    validate.run()
    receipt['passed']=validate.passed;receipt['status']='PASS'
except BaseException as exc:
    receipt['error_type']=type(exc).__name__;receipt['error']=str(exc)
    if 'validate' in sys.modules: receipt['passed']=sys.modules['validate'].passed
    raise
finally:
    with output.open('x') as out: json.dump(receipt,out,indent=2);out.write('\n')
    print(json.dumps({'status':receipt['status'],'passed':len(receipt['passed']),'receipt':str(output)}))

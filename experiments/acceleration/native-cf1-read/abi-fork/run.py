import hashlib,json,os,sys,sysconfig
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent;O=B/'candidate-native-cf1-read-20261014'
receipt={'status':'FAIL','optimize':sys.flags.optimize,'observations':[]}
try:
 pins=json.loads((R/'PINS.json').read_text())
 for path,digest in pins.items():
  if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise RuntimeError('Pin mismatch: '+path)
 if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize not in (0,1):raise RuntimeError('Interpreter mismatch')
 build=json.loads((O/'build-03-normal/build.json').read_text())
 if sysconfig.get_config_var('SOABI')!=build['soabi']:raise RuntimeError('ABI mismatch')
 sys.path[:0]=[str(O/'build-03-normal'),str(O),str(B/'candidate-s20-restored-20261014/src')]
 import native_cf1,cryptography
 from cryptography.hazmat.backends.openssl.backend import backend
 from cryptalis.crypto import cf1
 if native_cf1.__file__!=build['binary'] or native_cf1.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Native origin mismatch')
 if cryptography.__file__!=build['cryptography_origin'] or cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Oracle environment mismatch')
 if Path(cf1.__file__)!=B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py':raise RuntimeError('Source origin mismatch')
 import runtime
 runtime.run(sys.argv[2] if len(sys.argv)>2 else None);receipt['status']='PASS'
except BaseException as exc:
 receipt.update(error_type=type(exc).__name__,error=str(exc));raise
finally:
 if 'runtime' in sys.modules:receipt['observations']=runtime.observations
 with (R/'evidence'/sys.argv[1]).open('x') as f:json.dump(receipt,f,indent=2)

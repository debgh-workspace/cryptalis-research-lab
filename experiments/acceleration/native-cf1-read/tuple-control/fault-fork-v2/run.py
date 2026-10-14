"""Future bounded fault/fork child. No execution authorized yet."""
import hashlib
import json
import os
from pathlib import Path
import sys
R=Path(__file__).parent.absolute();T=R.parent;B=T.parent
mode,name=sys.argv[1:];dest=R/name
receipt={'status':'FAIL','mode':mode,'optimize':sys.flags.optimize,'observations':[],'fork_receipts':[],'fork_attempts':[],'negative':None}
runtime=None;baseline=None;freeze=None

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check():
    if any(k in os.environ for k in freeze['reject_environment']):raise RuntimeError('Environment override')
    for path,h in freeze['pins'].items():
        if sha(path)!=h:raise RuntimeError('Pin mismatch: '+path)
    for root,expected in freeze['bytecode_inventory'].items():
        if sorted(str(f) for f in Path(root).rglob('*.pyc') if f.is_file())!=expected:raise RuntimeError('Bytecode inventory mismatch')
try:
    freeze=json.loads((R/'FREEZE.json').read_text())
    if mode not in freeze['modes'] or dest.exists():raise RuntimeError('Invalid launch')
    if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize not in (0,1):raise RuntimeError('Python mismatch')
    check();receipt['precheck']='PASS';receipt['freeze_sha256']=sha(R/'FREEZE.json')
    build=T/'build-direct-01-diagnostic'
    bm=json.loads((build/'build.json').read_text())
    if bm['status']!='BUILT' or bm['mode']!='diagnostic':raise RuntimeError('Wrong diagnostic build')
    sys.path[:0]=[str(R),str(build),str(T),str(B/'candidate-native-cf1-read-20261014'),str(B/'candidate-s20-restored-20261014/src')]
    import native_tuple,tuple_read,cryptography,fixture_support
    from cryptography.hazmat.backends.openssl.backend import backend
    from cryptalis.crypto import cf1,keys
    if native_tuple.__file__!=bm['binary'] or not hasattr(native_tuple,'tuple_alloc_failure'):raise RuntimeError('Wrong native import')
    if cryptography.__file__!=freeze['cryptography_origin'] or cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Wrong backend')
    for mod,path in [(tuple_read,T/'tuple_read.py'),(cf1,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py'),(keys,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/keys.py'),(fixture_support,B/'candidate-native-cf1-read-20261014/fixture_support.py')]:
        if Path(mod.__file__)!=path:raise RuntimeError('Wrong source origin')
    baseline=(cf1.tuple_bytes,cf1.open_text,cf1._derive,cf1._term,cf1._aad,cf1.os.urandom,tuple_read._native_tuple_bytes)
    import runtime
    def child_guard():
        check()
        if baseline!=(cf1.tuple_bytes,cf1.open_text,cf1._derive,cf1._term,cf1._aad,cf1.os.urandom,tuple_read._native_tuple_bytes) or runtime.pbaseline.tuple_bytes is not runtime.original_p_tuple:
            raise RuntimeError('Child binding restoration failure')
        return {'source_cache':'PASS','bindings':'PASS'}
    runtime.child_check=child_guard
    runtime.run(mode)
    receipt['status']='PASS'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc));raise
finally:
    try:
        if freeze is not None:check();receipt['postcheck']='PASS'
        if baseline is not None and baseline!=(cf1.tuple_bytes,cf1.open_text,cf1._derive,cf1._term,cf1._aad,cf1.os.urandom,tuple_read._native_tuple_bytes):raise RuntimeError('Baseline or tuple binding changed')
    except BaseException as exc:
        receipt.update(status='FAIL',error_type=type(exc).__name__,error=str(exc));raise
    finally:
        if runtime is not None:
            receipt['observations']=runtime.observations;receipt['fork_receipts']=runtime.fork_receipts;receipt['fork_attempts']=runtime.fork_attempts;receipt['negative']=runtime.negative_record
        with dest.open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')

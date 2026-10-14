"""Standalone public-vector comparison. No product import, database or timing."""
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
import sysconfig
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from cryptography.hazmat.backends.openssl.backend import backend
import cryptography

ROOT = Path(__file__).resolve().parent
BINARY = ROOT / ('native_direction' + sysconfig.get_config_var('EXT_SUFFIX'))
spec = importlib.util.spec_from_file_location('native_direction', BINARY)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
FIXTURE = ROOT.parent / 'candidate-accel-payload-integrated-20261014/tests/fixtures/cf1_vectors.json'
checks = []
def check(label, fn):
    fn()
    checks.append(label)
def equal(actual, expected):
    if actual != expected:
        raise AssertionError('Output mismatch')

def refuse(args, error):
    try:
        native.decrypt_once(*args)
    except error as exc:
        if str(exc) not in ('Native operation failed', 'Exact bytes required', 'Invalid bounded input'):
            raise AssertionError('Unexpected refusal text')
    else:
        raise AssertionError('Expected bounded refusal')

def main():
    vectors = json.loads(FIXTURE.read_text())['primitive_vectors']['aes256_gcm_siv']
    for i, v in enumerate(vectors):
        args = [bytes.fromhex(v[k]) for k in ('key','nonce','sealed','aad')]
        plain = bytes.fromhex(v['plaintext'])
        check(f'rfc8452-vector-{i}', lambda a=args,p=plain: equal(native.decrypt_once(*a),p))
    rng = random.Random(0xC11)
    for n in (0, 1, 7, 16, 17, 31, 1024, 65536):
        key, nonce, aad, plain = rng.randbytes(32), rng.randbytes(12), rng.randbytes(23), rng.randbytes(n)
        sealed = AESGCMSIV(key).encrypt(nonce, plain, aad)
        args = [key,nonce,sealed,aad]
        check(f'pyca-public-fixture-{n}', lambda a=args,p=plain: equal(native.decrypt_once(*a),p))
        for position in range(4):
            changed = list(args)
            value = bytearray(changed[position]); value[-1] ^= 1; changed[position] = bytes(value)
            check(f'public-fixture-auth-refusal-{n}-{position}', lambda a=changed: refuse(a,ValueError))
        check(f'fresh-call-after-refusal-{n}', lambda a=args,p=plain: equal(native.decrypt_once(*a),p))
    good = [bytes(range(32)), bytes(range(12)), AESGCMSIV(bytes(range(32))).encrypt(bytes(range(12)),b'public',b'aad'), b'aad']
    for position in range(4):
        for wrong in (bytearray(b'x'),memoryview(b'x'),'x',None):
            changed=list(good);changed[position]=wrong
            check(f'exact-type-{position}-{type(wrong).__name__}',lambda a=changed:refuse(a,TypeError))
    for position, wrong in [(0,b''),(0,b'x'*31),(0,b'x'*33),(1,b'x'*11),(1,b'x'*13),(2,b'x'*15),(2,b'x'*(16*1024*1024+17)),(3,b'x'*(16*1024*1024+1))]:
        changed=list(good);changed[position]=wrong
        check(f'length-{position}-{len(wrong)}',lambda a=changed:refuse(a,ValueError))

receipt={'scope':'Direction-specific AES-256-GCM-SIV public-vector probe only; no fused CF1, no performance or product admission', 'python':sys.version.split()[0], 'optimize':sys.flags.optimize, 'validation_style':'explicit exceptions', 'cryptography':cryptography.__version__, 'pyca_backend':backend.openssl_version_text(), 'native_backend':native.backend_version(), 'fixture_sha256':hashlib.sha256(FIXTURE.read_bytes()).hexdigest(), 'source_sha256':hashlib.sha256((ROOT/'native_direction.c').read_bytes()).hexdigest(), 'binary_sha256':hashlib.sha256(BINARY.read_bytes()).hexdigest()}
try:
    if '--negative-control' in sys.argv:
        equal(b'wrong', b'expected')
    main();receipt['status']='PASS'
except BaseException as exc:
    receipt['status']='FAIL';receipt['failure']={'type':type(exc).__name__,'message':str(exc)}
    raise
finally:
    receipt['passed_checks']=checks;receipt['count']=len(checks)
    (ROOT/'evidence/explicit-o1-negative.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'passed':len(checks),'native_backend':receipt['native_backend']}))

"""Supplemental, synthetic-public-fixture checks only; no product imports or timing."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import sysconfig

ROOT = Path(__file__).absolute().parent
BASE = ROOT.parent / 'candidate-native-direction-probe-20261014'
PYTHON = '/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python'
PINS = {
    'native_direction.c': '5933299b46e349cd0e80032fd89beffd797e5ad04230cbfda1d985ef1eca0239',
    'native_direction.cpython-312-x86_64-linux-gnu.so': '393cf26a573870a9e7e1d3b12a3196528f9301f840214dbc05d84e1cb37575ed',
}
LIMIT = 16 * 1024 * 1024
negative = '--negative-control' in sys.argv
receipt_path = ROOT / ('receipt-o%d-%s.json' % (sys.flags.optimize, 'negative' if negative else 'positive'))
if receipt_path.exists():
    raise RuntimeError('Refusing to overwrite evidence')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def snapshot():
    return {str(p.relative_to(BASE)): digest(p) for p in sorted(BASE.rglob('*')) if p.is_file()}

receipt = {
    'scope': 'Supplemental owned native_direction component checks, synthetic public inputs only; no benchmark, product integration or database',
    'python': sys.version,
    'executable': sys.executable,
    'optimize': sys.flags.optimize,
    'negative_control': negative,
    'harness_sha256': digest(Path(__file__)),
    'expected_component_sha256': PINS,
    'checks': [],
}

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def check(label, fn, **details):
    item = {'label': label, **details}
    receipt['checks'].append(item)
    try:
        fn()
    except BaseException as exc:
        item.update(status='FAIL', error_type=type(exc).__name__)
        raise
    else:
        item['status'] = 'PASS'

def equal(actual, expected):
    require(type(actual) is bytes, 'Unexpected result type')
    require(actual == expected, 'Result mismatch')

def refuse(args, error, message=None):
    try:
        native.decrypt_once(*args)
    except BaseException as exc:
        require(type(exc) is error, 'Unexpected exception type')
        if message is not None:
            require(str(exc) == message, 'Unexpected refusal category')
    else:
        raise RuntimeError('Expected refusal')

try:
    require(sys.executable == PYTHON, 'Wrong interpreter path')
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(Path(__file__).read_text()))), 'Optimization-sensitive check')
    receipt['base_before'] = snapshot()
    for name, expected in PINS.items():
        require(receipt['base_before'].get(name) == expected, 'Frozen component mismatch')
    receipt['pins_verified_before_native_load'] = True
    import cryptography
    from cryptography.hazmat.backends.openssl.backend import backend
    from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
    from cryptography.exceptions import InvalidTag
    receipt['cryptography'] = cryptography.__version__
    receipt['pyca_backend'] = backend.openssl_version_text()
    require(cryptography.__version__ == '50.0.2', 'Wrong cryptography version')
    require(backend.openssl_version_text() == 'OpenSSL 4.0.3 29 Sep 2026', 'Wrong pyca backend')
    binary_name = 'native_direction' + sysconfig.get_config_var('EXT_SUFFIX')
    require(binary_name in PINS, 'Unexpected ABI')
    spec = importlib.util.spec_from_file_location('native_direction', BASE / binary_name)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    receipt['native_backend'] = native.backend_version()
    if negative:
        check('intentional-equality-negative-control', lambda: equal(b'public-actual', b'public-expected'))
    else:
        key = bytes(range(32))
        counter = 0
        def fixture(plain, aad):
            global counter
            counter += 1
            nonce = counter.to_bytes(12, 'big')
            oracle = AESGCMSIV(key)
            sealed = oracle.encrypt(nonce, plain, aad)
            equal(oracle.decrypt(nonce, sealed, aad), plain)
            return [key, nonce, sealed, aad]
        def oracle_refuse(args):
            try:
                AESGCMSIV(args[0]).decrypt(args[1], args[2], args[3])
            except InvalidTag:
                return
            raise RuntimeError('Oracle accepted changed body')
        for size in (1, 17, 4096):
            plain = b'P' * size
            args = fixture(plain, b'public-aad')
            check('body-original-%d' % size, lambda a=args, p=plain: equal(native.decrypt_once(*a), p))
            for offset in sorted({0, size // 2, size - 1}):
                changed = list(args)
                value = bytearray(changed[2]); value[offset] ^= 1; changed[2] = bytes(value)
                require(changed[2][-16:] == args[2][-16:], 'Tag unexpectedly changed')
                require(changed[2][:-16] != args[2][:-16], 'Body unchanged')
                check('body-oracle-refusal-%d-%d' % (size, offset), lambda a=changed: oracle_refuse(a), body_bytes=size, offset=offset, tag_unchanged=True)
                check('body-native-refusal-%d-%d' % (size, offset), lambda a=changed: refuse(a, ValueError, 'Native operation failed'))
                check('body-recovery-%d-%d' % (size, offset), lambda a=args, p=plain: equal(native.decrypt_once(*a), p))
        plain = b'public-baseline'
        good = fixture(plain, b'public-aad')
        class BytesSubclass(bytes):
            pass
        for position in range(4):
            changed = list(good); changed[position] = BytesSubclass(good[position])
            check('bytes-subclass-argument-%d' % position, lambda a=changed: refuse(a, TypeError, 'Exact bytes required'))
        for count in (0, 1, 2, 3, 5):
            args = good[:count] if count < 4 else good + [b'public-extra']
            check('wrong-positional-arity-%d' % count, lambda a=args: refuse(a, TypeError))
        check('recovery-after-shape-refusals', lambda: equal(native.decrypt_once(*good), plain))
        for name, plen, alen in (
            ('input-below', LIMIT-1, 23), ('input-at', LIMIT, 23),
            ('aad-below', 31, LIMIT-1), ('aad-at', 31, LIMIT),
            ('both-below', LIMIT-1, LIMIT-1), ('both-at', LIMIT, LIMIT),
        ):
            p = b'P' * plen; aad = b'A' * alen
            args = fixture(p, aad)
            check('valid-' + name, lambda a=args, p=p: equal(native.decrypt_once(*a), p), plaintext_bytes=plen, aad_bytes=alen, sealed_bytes=len(args[2]), independent_pyca_roundtrip=True)
            del args, p, aad
        for name, plen, alen in (('input-plus-one', LIMIT+1, 23), ('aad-plus-one', 31, LIMIT+1)):
            p = b'P' * plen; aad = b'A' * alen
            args = fixture(p, aad)
            check('bounded-refusal-' + name, lambda a=args: refuse(a, ValueError, 'Invalid bounded input'), plaintext_bytes=plen, aad_bytes=alen, sealed_bytes=len(args[2]), independent_pyca_roundtrip=True)
            check('recovery-after-' + name, lambda: equal(native.decrypt_once(*good), plain))
            del args, p, aad
    receipt['status'] = 'PASS'
except BaseException as exc:
    receipt['status'] = 'FAIL'
    receipt['failure_type'] = type(exc).__name__
    # Do not serialize arbitrary exception text or input values.
finally:
    receipt['base_after'] = snapshot()
    receipt['base_unchanged'] = receipt.get('base_before') == receipt['base_after']
    if not receipt['base_unchanged']:
        receipt['status'] = 'FAIL'
    receipt['passed_checks'] = sum(x.get('status') == 'PASS' for x in receipt['checks'])
    receipt['failed_checks'] = sum(x.get('status') == 'FAIL' for x in receipt['checks'])
    with receipt_path.open('x') as stream:
        json.dump(receipt, stream, indent=2); stream.write('\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'optimize', 'negative_control', 'passed_checks', 'failed_checks', 'base_unchanged')}))
sys.exit(0 if receipt['status'] == 'PASS' else 1)

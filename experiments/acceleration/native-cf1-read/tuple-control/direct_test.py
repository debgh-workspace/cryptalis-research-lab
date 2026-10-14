"""Direct ABI correctness only; called by launch_direct.py after origin checks."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent

class BytesSubclass(bytes):
    pass


def run(native, diagnostic, negative=False):
    manifest = json.loads((ROOT/'DIRECT_MANIFEST.json').read_text())
    oracle = {c['id']: c for c in json.loads((ROOT/'tuple-oracle.json').read_text())['cases']}
    results = []
    def need(ok, label):
        if not ok:
            raise RuntimeError(label)
    def refusal(fn, args, expected, kwargs=None):
        try:
            value = fn(*args, **(kwargs or {}))
        except Exception as exc:
            need(type(exc) is expected, 'exception class mismatch')
            if expected is ValueError:
                need(str(exc) == 'Invalid tuple shape', 'exception message mismatch')
            return
        del value
        raise RuntimeError('unexpected return')
    def recovery():
        c = oracle['generic/all-octets']
        actual = native.tuple_bytes(*(bytes.fromhex(p) for p in c['parts_hex']))
        need(type(actual) is bytes and actual == bytes.fromhex(c['expected_hex']), 'recovery mismatch')
    required = manifest['diagnostic_ids' if diagnostic else 'normal_ids']
    for ident in required:
        if ident.startswith('oracle/'):
            c = oracle[ident[7:]]
            actual = native.tuple_bytes(*(bytes.fromhex(p) for p in c['parts_hex']))
            if negative:
                # Downstream harness negative: mutate ACTUAL immutable bytes, never expected.
                actual = bytes([actual[0] ^ 1]) + actual[1:]
            need(type(actual) is bytes and actual == bytes.fromhex(c['expected_hex']), 'tuple mismatch: '+ident)
        elif ident.startswith('abi/type/'):
            _, _, pos, kind = ident.split('/')
            bad = {'None':None, 'bytearray':bytearray(b'x'), 'memoryview':memoryview(b'x'),
                   'bytes-subclass':BytesSubclass(b'x'), 'str':'x', 'int':1}[kind]
            args = [b'\x00']*7; args[int(pos)] = bad
            refusal(native.tuple_bytes, args, ValueError)
        elif ident == 'abi/eight-parts':
            refusal(native.tuple_bytes, [b'']*8, ValueError)
        elif ident == 'abi/keywords':
            refusal(native.tuple_bytes, [], TypeError, {'parts':b'\x00'})
        elif ident == 'abi/cap-exact':
            actual = native.tuple_bytes(b'x'*16777720)
            expected = bytes.fromhex('00000001010001f8') + b'x'*16777720
            need(type(actual) is bytes and actual == expected, 'cap exact mismatch')
            del actual, expected
        elif ident == 'abi/cap-plus-one':
            refusal(native.tuple_bytes, [b'x'*16777721], ValueError)
        elif ident == 'abi/sum-cap-plus-one':
            refusal(native.tuple_bytes, [b'x'*8388858, b'x'*8388859], ValueError)
        elif ident == 'fault/output-allocation':
            refusal(native.tuple_alloc_failure, [b'\x00'], MemoryError)
        elif ident == 'fault/type-before-allocation':
            refusal(native.tuple_alloc_failure, [None], ValueError)
        elif ident.startswith('refcount/'):
            action = ident.split('/')[1]
            item = bytes(bytearray(range(256)))
            large = b'x'*16777721 if action == 'size-refusal' else bytes(bytearray(range(255)))
            before = (sys.getrefcount(item), sys.getrefcount(large))
            for _ in range(1000):
                if action == 'success':
                    result = native.tuple_bytes(item, large)
                    del result
                elif action == 'type-refusal':
                    refusal(native.tuple_bytes, [item, large, None], ValueError)
                elif action == 'size-refusal':
                    refusal(native.tuple_bytes, [item, large], ValueError)
                elif action == 'diagnostic-allocation-refusal':
                    refusal(native.tuple_alloc_failure, [item, large], MemoryError)
                else:
                    raise RuntimeError('unknown refcount action')
            need(before == (sys.getrefcount(item), sys.getrefcount(large)), 'retained input reference')
            del item, large
        else:
            raise RuntimeError('unknown case '+ident)
        recovery()
        results.append({'id':ident, 'status':'PASS', 'recovery':'PASS'})
    need([r['id'] for r in results] == required, 'coverage mismatch')
    return results

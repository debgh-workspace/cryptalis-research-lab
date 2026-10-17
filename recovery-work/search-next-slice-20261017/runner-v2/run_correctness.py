"""New same-host SA21 no-DB experiment; root admission/selection required."""
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import time
import unittest
from types import MappingProxyType, SimpleNamespace
from uuid import UUID

ROOT = Path('/workspace/scratch/cb28ee9f5f4a/recovery-work/search-next-slice-20261017/runner-v2')
STDLIB = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12')
HOST = '/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'
PREFIX = ROOT / 'bytecode-absent'
CAP = 16 * 1024 * 1024
VARIANTS = ('baseline', 'candidate', 'mutant-stale', 'mutant-tenant', 'mutant-point', 'mutant-null')

def stamp(path):
    p = Path(path)
    assert p.is_absolute() and '..' not in p.parts
    for parent in p.parents:
        s = parent.lstat()
        assert stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and 1 <= s.st_nlink and 0 <= s.st_size <= CAP
    return (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def read(path, expected_stamp):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        s = os.fstat(stream.fileno())
        assert (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns) == expected_stamp
        data = stream.read(CAP + 1)
    assert len(data) <= CAP and stamp(path) == expected_stamp
    return data

def absent(path):
    assert not os.path.lexists(path)

class CappedLog(io.StringIO):
    def write(self, text):
        if self.tell() + len(text) > 262144:
            raise RuntimeError('unittest diagnostic ceiling')
        return super().write(text)

def suite_for(adapter, catalog):
    from sqlalchemy import BigInteger, column
    from cryptalis.crypto import cf1
    from cryptalis.crypto.keys import (AuthenticationFailed, InvalidContext, KeyUnavailable,
        KeyContext, KeyPolicy, PreparedKeys, WrappedRoot, _Material)
    A, B = UUID(catalog['A']), UUID(catalog['B'])
    DOMAIN, FIELD, ROOT_ID, PROVIDER = (UUID(int=i) for i in (10, 11, 12, 13))

    def descriptor(tenant=A, *, equality=False, uuid_record=False, single=False):
        return cf1.FieldDescriptor(DOMAIN, tenant if single else UUID(int=14), FIELD,
            'uuid16/v1' if uuid_record else 'int64-be/v1',
            'single-tenant-uuid/v1' if single else 'uuid16/v1',
            'cf1-packed-equality/v1' if equality else 'cf1-storage/v1', bytes(range(32)))

    def prepared(tenant, equality=False, expired=False, missing=False, wrong_pid=False):
        # Synthetic pre-admitted material only: never instantiate/call any provider.
        contexts = [KeyContext(DOMAIN, tenant, 'payload', ROOT_ID, 1)]
        if equality:
            contexts.append(KeyContext(DOMAIN, tenant, 'search', UUID(int=15), 2))
        wrappers = tuple(WrappedRoot(PROVIDER, c, b'synthetic-not-a-provider-wrapper') for c in contexts)
        policy = KeyPolicy(DOMAIN, tenant, wrappers, 1, 2 if equality else None)
        materials = {(c.purpose, c.generation): _Material(c,
            bytes(range(32)) if c.purpose == 'payload' else bytes(range(32, 64)),
            0.0 if expired else time.monotonic() + 300.0) for c in contexts}
        if missing:
            materials.clear()
        return PreparedKeys(policy, MappingProxyType(materials), -1 if wrong_pid else os.getpid())

    def processor(tenant=A, keys='keys-A', points=(), field=None):
        record_column = column('record', BigInteger())
        operation = SimpleNamespace(keys=keys, tenant=tenant,
            points=tuple((record_column, point) for point in points))
        p = adapter._ReadText(SimpleNamespace(descriptor=field or descriptor()), operation, record_column)
        return p, operation

    class Correctness(unittest.TestCase):
        def expect_error(self, expected_type, operation):
            try:
                operation()
            except Exception as error:
                self.assertIs(type(error), expected_type,
                              'operation raised an unexpected exception class')
            else:
                self.fail('operation did not raise the required exception')

        def observe(self, p, row, expected):
            calls = []
            original = adapter.open_text
            def observed(payload, field, tenant, record, keys):
                calls.append({'tenant': str(tenant), 'record': record, 'keys': keys,
                              'payload': payload.hex() if payload is not None else None})
                return 'OBSERVER_RETURN'
            adapter.open_text = observed
            try:
                if 'error' in expected:
                    self.expect_error(AuthenticationFailed, lambda: p.process_result_value(row, None))
                else:
                    result = p.process_result_value(row, None)
                    self.assertEqual(result, expected.get('result', 'OBSERVER_RETURN'))
                self.assertEqual(len(calls), expected['open_text_calls'])
                if calls:
                    self.assertEqual(calls, [{k: expected[k] for k in ('tenant', 'record', 'keys', 'payload')}])
            finally:
                adapter.open_text = original

        def literal(self, case):
            p, operation = processor()
            name = case['id']
            token = None
            if name == 'wrong-point': p.points = (7,)
            elif name in ('rebind-tenant-reject-old', 'rebind-tenant-parse-new'): p.tenant = B
            elif name == 'rebind-equal-distinct':
                fresh = UUID(str(A)); self.assertIsNot(fresh, A); p.tenant = fresh
            elif name == 'restore-original-object': p.tenant = B; p.tenant = A
            elif name == 'rebind-keys': p.keys = 'keys-B'
            elif name == 'rebind-points': p.points = (8,)
            elif name == 'operation-rebound-after-construction':
                operation.tenant = B; operation.keys = 'keys-B'; operation.points = ((None, 8),)
            elif name == 'ambient-operation-changed':
                token = adapter._operation.set(SimpleNamespace(tenant=B, keys='keys-B', points=(8,)))
            elif name == 'new-processor-B':
                q, _ = processor(B, 'keys-B')
                expected_a = dict(open_text_calls=1, tenant=str(A), record=7, keys='keys-A', payload=None)
                self.observe(p, [None, 7, str(A)], expected_a)
                self.observe(q, case['row'], case['expected'])
                self.observe(p, [None, 7, str(A)], expected_a)
                return
            try:
                self.observe(p, case['row'], case['expected'])
            finally:
                if token is not None: adapter._operation.reset(token)

        def test_additional_fallback_and_codecs(self):
            fail = dict(error='AuthenticationFailed', open_text_calls=0)
            ok = dict(open_text_calls=1, tenant=str(A), record=7, keys='keys-A', payload=None)
            class TextSubclass(str): pass
            class UUIDSubclass(UUID): pass
            for row_tenant in (A, str(A).encode(), object()):
                with self.subTest(invalid_tenant_type=type(row_tenant).__name__):
                    self.observe(processor()[0], [None, 7, row_tenant], fail)
            self.observe(processor()[0], [None, 7, TextSubclass(str(A))], ok)
            self.observe(processor(UUIDSubclass(str(A)))[0], [None, 7, str(A)], ok)
            for bad_record in (True, False, 7.0, '7'):
                with self.subTest(invalid_record_type=type(bad_record).__name__):
                    self.observe(processor()[0], [None, bad_record, str(A)], fail)
            self.observe(processor()[0], [None, 7, str(A)], ok)
            field = descriptor(uuid_record=True)
            record = UUID(int=7)
            p, _ = processor(points=(record,), field=field)
            # Observer serializes UUID record separately for literal comparison.
            expected = dict(ok, record=record)
            self.observe(p, [None, str(record), str(A)], expected)
            self.observe(p, [None, 'not-a-uuid', str(A)], fail)
            self.observe(p, [None, str(UUID(int=8)), str(A)], fail)
            single, _ = processor(field=descriptor(single=True))
            self.observe(single, [None, None, str(A)], dict(result=None, open_text_calls=0))
            self.observe(single, [None, None, None], fail)
            self.observe(single, [None, None, str(B)], fail)
            self.observe(single, [None, 7, str(A)], ok)

        def test_real_cf1_context_matrix(self):
            for equality in (False, True):
                for uuid_record in (False, True):
                    for single in (False, True):
                        with self.subTest(equality=equality, uuid_record=uuid_record, single=single):
                            record = UUID(int=7) if uuid_record else 7
                            other_record = UUID(int=8) if uuid_record else 8
                            wire_record = str(record) if uuid_record else record
                            other_wire = str(other_record) if uuid_record else other_record
                            field = descriptor(equality=equality, uuid_record=uuid_record, single=single)
                            keys = prepared(A, equality)
                            frame = cf1.seal_text('alpha', field, A, record, keys)
                            p, _ = processor(keys=keys, field=field)
                            self.assertEqual(p.process_result_value([frame.hex(), wire_record, str(A)], None), 'alpha')
                            self.expect_error(AuthenticationFailed, lambda: p.process_result_value([frame.hex(), wire_record, str(B)], None))
                            self.expect_error(AuthenticationFailed, lambda: p.process_result_value([frame.hex(), other_wire, str(A)], None))
                            corrupt = frame[:-1] + bytes([frame[-1] ^ 1])
                            self.expect_error(AuthenticationFailed, lambda: p.process_result_value([corrupt.hex(), wire_record, str(A)], None))
                            self.assertIsNone(p.process_result_value([None, wire_record, str(A)], None))
                            for defect in ('expired', 'missing', 'wrong_pid'):
                                p.keys = prepared(A, equality, **{defect: True})
                                self.expect_error(KeyUnavailable, lambda: p.process_result_value([None, wire_record, str(A)], None))
                            p.keys = prepared(B, equality)
                            self.expect_error(KeyUnavailable, lambda: p.process_result_value([None, wire_record, str(A)], None))
                            # A stale canonical-text shortcut must not authenticate under B.
                            p.tenant = B
                            self.expect_error(AuthenticationFailed, lambda: p.process_result_value([frame.hex(), wire_record, str(A)], None))
                            field_b = descriptor(B, equality=equality, uuid_record=uuid_record, single=single)
                            keys_b = prepared(B, equality)
                            frame_b = cf1.seal_text('beta', field_b, B, record, keys_b)
                            q, _ = processor(B, keys_b, field=field_b)
                            p.keys = keys; p.tenant = A
                            for proc, row, literal in ((p, [frame.hex(), wire_record, str(A)], 'alpha'),
                                    (q, [frame_b.hex(), wire_record, str(B)], 'beta'),
                                    (p, [frame.hex(), wire_record, str(A)], 'alpha')):
                                self.assertEqual(proc.process_result_value(row, None), literal)

    for case in catalog['cases']:
        def method(self, case=case): self.literal(case)
        setattr(Correctness, 'test_literal_' + case['id'].replace('-', '_'), method)
    return unittest.defaultTestLoader.loadTestsFromTestCase(Correctness)

def main():
    admitted = {}; before = {}; final = {}; primary = None; results = None; diagnostic = CappedLog(); stage = 'STARTUP'
    try:
        assert len(sys.argv) == 3 and sys.argv[1] in VARIANTS
        variant, seal = sys.argv[1:]
        assert len(seal) == 64 and all(c in '0123456789abcdef' for c in seal)
        assert Path(__file__) == ROOT / 'run_correctness.py' and Path.cwd() == ROOT
        assert sys.executable == HOST and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
        assert not sys.flags.optimize and sys.pycache_prefix == str(PREFIX)
        assert dict(os.environ) == {'LANG':'C.UTF-8', 'LC_ALL':'C.UTF-8', 'TZ':'UTC'}
        absent(PREFIX)
        assert not any(n in sys.modules for n in ('site', 'sitecustomize', 'usercustomize', 'pytest', 'conftest', 'cryptalis', 'sqlalchemy'))
        source_path = ROOT / 'SOURCE.sha256'; before[str(source_path)] = stamp(source_path)
        source_raw = read(source_path, before[str(source_path)])
        assert hashlib.sha256(source_raw).hexdigest() == seal
        admitted[str(source_path)] = seal
        manifest = {}
        for line in source_raw.decode().splitlines():
            digest, name = line.split('  ', 1)
            assert len(digest) == 64 and all(c in '0123456789abcdef' for c in digest)
            assert name not in manifest and not Path(name).is_absolute() and '..' not in Path(name).parts
            manifest[name] = digest
        control_names = ('run_correctness.py', 'DEPENDENCIES.json', 'VIEWS.json', 'ORACLES.json', 'PLAN.md')
        # Full control metadata first; retain stamps through expanded admission.
        for name in control_names: before[str(ROOT/name)] = stamp(ROOT/name)
        controls = {}
        for name in control_names:
            data = read(ROOT/name, before[str(ROOT/name)])
            assert hashlib.sha256(data).hexdigest() == manifest[name]
            admitted[str(ROOT/name)] = manifest[name]; controls[name] = data
        deps = json.loads(controls['DEPENDENCIES.json']); views = json.loads(controls['VIEWS.json'])
        catalog = json.loads(controls['ORACLES.json'])
        assert len(deps['files']) == 399 and len(views[variant]) == 43 and len(catalog['cases']) == 23
        assert len({c['id'] for c in catalog['cases']}) == 23
        view = ROOT/'views'/variant/'src'
        for item in views[variant]:
            path = item['path']; assert Path(path).is_relative_to(view)
            assert manifest[str(Path(path).relative_to(ROOT))] == item['sha256']
            admitted[path] = item['sha256']
        for path, digest in deps['files'].items():
            assert Path(path).is_relative_to(deps['prefix'])
            admitted[path] = digest
        stage = 'FULL_ADMISSION'
        complete = {path: stamp(path) for path in admitted}
        assert all(complete[p] == s for p, s in before.items())
        before = complete
        for path, digest in admitted.items():
            assert hashlib.sha256(read(path, before[path])).hexdigest() == digest
        trusted = str(STDLIB) + os.sep
        allowed = set(admitted)
        def audit(event, args):
            if event == 'open':
                path, mode, flags = args
                if isinstance(path, int): return  # only owned fdopen in this runner
                path = os.fsdecode(path)
                if not os.path.isabs(path) or os.path.normpath(path) != path:
                    raise PermissionError('noncanonical read denied')
                if (isinstance(mode, str) and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                    raise PermissionError('write denied')
                if path.endswith(('.pyc', '.pyo')):
                    raise PermissionError('bytecode body denied')
                if path not in allowed and not (path.startswith(trusted) and '/site-packages/' not in path):
                    raise PermissionError('undeclared read denied')
            if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn')) or event in ('os.system', 'os.fork', 'os.forkpty', 'os.remove', 'os.rename', 'os.mkdir', 'os.rmdir', 'os.link', 'os.symlink', 'os.truncate'):
                raise PermissionError('external operation denied')
        sys.addaudithook(audit)
        sys.path[:] = [str(view), deps['prefix'], str(STDLIB), str(STDLIB/'lib-dynload')]
        stage = 'IMPORT_SQLALCHEMY'
        import sqlalchemy
        assert sqlalchemy.__version__ == '2.1.3'
        stage = 'IMPORT_CRYPTALIS'
        import cryptalis.sqlalchemy as adapter
        stage = 'BUILD_SUITE'
        suite = suite_for(adapter, catalog)
        assert suite.countTestCases() == 25
        stage = 'RUN_SUITE'
        results = unittest.TextTestRunner(stream=diagnostic, verbosity=2).run(suite)
        assert not any(n in sys.modules for n in ('pytest', 'conftest', 'psycopg', 'psycopg_binary'))
    except BaseException as error:
        primary = type(error).__name__
    finally:
        # Complete metadata pass; hash each safely unchanged leaf independently.
        stamps = {}
        for path in admitted:
            try:
                stamps[path] = stamp(path)
                assert path in before and stamps[path] == before[path]
                final[path] = 'METADATA_PASS'
            except BaseException as error: final[path] = 'METADATA_' + type(error).__name__
        for path, digest in admitted.items():
            if final[path] != 'METADATA_PASS': continue
            try:
                assert hashlib.sha256(read(path, stamps[path])).hexdigest() == digest
                final[path] = 'PASS'
            except BaseException as error: final[path] = 'HASH_' + type(error).__name__
        try: absent(PREFIX); absence = 'PASS'
        except BaseException as error: absence = type(error).__name__
        tests_ok = results is not None and results.testsRun == 25 and results.wasSuccessful()
        closure_ok = bool(admitted) and len(admitted) == 448 and all(v == 'PASS' for v in final.values())
        success = primary is None and tests_ok and closure_ok and absence == 'PASS'
        summary = {'scope':'same-host-SA21-noDB-new-search-candidate', 'variant':sys.argv[1] if len(sys.argv)>1 else None,
            'status':'PASS' if success else 'HOLD', 'primary_type':primary, 'primary_stage':stage if primary else None,
            'tests_run':results.testsRun if results else 0,
            'failures':[test.id() for test, _ in results.failures] if results else [],
            'errors':[test.id() for test, _ in results.errors] if results else [],
            'admitted':len(admitted), 'closure':final, 'bytecode_absence':absence,
            'no_performance_claim':True}
        sys.stderr.write(diagnostic.getvalue()); sys.stderr.flush()
        sys.stdout.write('CORRECTNESS_JSON ' + json.dumps(summary, sort_keys=True) + '\n'); sys.stdout.flush()
    return 0 if success else 1

if __name__ == '__main__':
    raise SystemExit(main())

"""Fixed no-DB scanner test entry; root owns admission and external limits."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import unittest

ROOT = Path('/workspace/scratch/cb28ee9f5f4a/recovery-work/search-nullsafe-advisory-20261017/report-execution-v1')
STDLIB = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12')
HOST = '/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'
PREFIX = ROOT / 'bytecode-absent'
CAP = 16 * 1024 * 1024


def stamp(path):
    path = Path(path)
    assert path.is_absolute() and '..' not in path.parts
    for parent in path.parents:
        assert stat.S_ISDIR(parent.lstat().st_mode)
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink >= 1 and s.st_size <= CAP
    return (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def body(path, expected):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        s = os.fstat(stream.fileno())
        assert (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns) == expected
        data = stream.read(CAP + 1)
    assert len(data) <= CAP and stamp(path) == expected
    return data


def audit(event, args):
    if event == 'open':
        path, mode, flags = args
        if (mode and any(c in mode for c in 'wax+')) or (flags and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):
            raise PermissionError('write forbidden')
        if isinstance(path, int):
            return
        raw = os.fsdecode(path)
        p = Path(raw)
        if raw != str(p) or '..' in p.parts or not p.is_absolute() or p.suffix in ('.pyc', '.pyo'):
            raise PermissionError('unadmitted read')
        if str(p) not in expected and not (p.is_relative_to(STDLIB) and 'site-packages' not in p.parts):
            raise PermissionError('unadmitted read')
    if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn')) or event in ('os.system', 'os.fork', 'os.forkpty', 'os.remove', 'os.rename', 'os.rmdir', 'os.mkdir', 'os.link', 'os.symlink', 'os.truncate', 'os.chmod', 'os.chown', 'os.utime'):
        raise PermissionError('effect forbidden')


expected, before, closure = {}, {}, {}
record = {'variant': None, 'tests_run': 0, 'failures': [], 'errors': [], 'primary_type': None, 'closure': closure}
passed = False
try:
    if sys.flags.optimize:
        raise RuntimeError("optimized Python is not admitted")
    assert len(sys.argv) == 3
    variant, seal = sys.argv[1:]
    record['variant'] = variant
    assert variant in ('baseline', 'candidate') and len(seal) == 64
    assert sys.executable == HOST and Path.cwd() == ROOT
    assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode
    assert sys.pycache_prefix == str(PREFIX) and not os.path.lexists(PREFIX)
    assert dict(os.environ) == {'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TZ': 'UTC'}
    sp = str(ROOT / 'SOURCE.sha256')
    before[sp] = stamp(sp)
    expected[sp] = seal
    raw = body(sp, before[sp])
    assert hashlib.sha256(raw).hexdigest() == seal
    for line in raw.decode('ascii').splitlines():
        digest, name = line.split('  ', 1)
        assert len(digest) == 64 and not Path(name).is_absolute() and '..' not in Path(name).parts
        p = str(ROOT / name)
        assert p not in expected
        expected[p] = digest
    assert len(expected) == 13
    # Complete packet metadata before member hashes or dependency-map parsing.
    for p in expected:
        current = stamp(p)
        if p in before:
            assert before[p] == current
        else:
            before[p] = current
    packet = {p: body(p, before[p]) for p in expected}
    assert all(hashlib.sha256(b).hexdigest() == expected[p] for p, b in packet.items())
    deps = json.loads(packet[str(ROOT / 'DEPENDENCIES.json')])
    assert len(deps['files']) == 299
    for p, digest in deps['files'].items():
        assert p.startswith(deps['prefix'] + '/') and p not in expected
        expected[p] = digest
    assert len(expected) == 312
    # All expanded metadata succeeds before any dependency body hash.
    for p in expected:
        current = stamp(p)
        if p in before:
            assert before[p] == current
        else:
            before[p] = current
    for p, digest in expected.items():
        assert hashlib.sha256(body(p, before[p])).hexdigest() == digest
    sys.addaudithook(audit)
    sys.path[:] = [str(ROOT / 'views' / variant / 'src'), deps['prefix'], str(STDLIB), str(STDLIB / 'lib-dynload')]
    spec = importlib.util.spec_from_file_location('nullsafe_tests', ROOT / 'test_report_integration.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(module.ReportIntegrationTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    record.update(tests_run=result.testsRun, failures=[str(t) for t, _ in result.failures], errors=[str(t) for t, _ in result.errors])
    passed = result.wasSuccessful() and result.testsRun == 4
except BaseException as exc:
    record['primary_type'] = type(exc).__name__
finally:
    safe = []
    for p in expected:
        try:
            assert p in before and stamp(p) == before[p]
            safe.append(p)
        except BaseException:
            closure[p] = 'METADATA_HOLD'
    for p in safe:
        try:
            assert hashlib.sha256(body(p, before[p])).hexdigest() == expected[p]
            closure[p] = 'PASS'
        except BaseException:
            closure[p] = 'HASH_HOLD'
    record['bytecode_absence'] = 'PASS' if not os.path.lexists(PREFIX) else 'HOLD'
    record['status'] = 'PASS' if passed and record['primary_type'] is None and len(closure) == 312 and set(closure.values()) == {'PASS'} and record['bytecode_absence'] == 'PASS' else 'HOLD'
    print('SCANNER_JSON ' + json.dumps(record, sort_keys=True), flush=True)
sys.exit(0 if record['status'] == 'PASS' else 1)

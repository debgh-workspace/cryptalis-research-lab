"""Bounded raw same-host result-processor samples; root selection required."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time
import gc
import resource
from types import MappingProxyType, SimpleNamespace
from uuid import UUID

ROOT = Path('/workspace/scratch/cb28ee9f5f4a/recovery-work/search-next-slice-20261017/benchmark-v2')
STDLIB = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12')
HOST = '/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'
PREFIX = ROOT / 'bytecode-absent'
CAP = 16 * 1024 * 1024
VARIANTS = ('baseline', 'candidate')

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

def measure(adapter, workload, index, samples):
    from sqlalchemy import BigInteger, column
    from cryptalis.crypto import cf1
    from cryptalis.crypto.keys import KeyContext, KeyPolicy, PreparedKeys, WrappedRoot, _Material
    tenant = UUID('aaaaaaaa-1111-4111-8111-111111111111')
    domain, table, field_id, provider = (UUID(int=i) for i in (10, 11, 12, 13))
    fixtures = {}
    # All construction, encryption and strings are outside measured intervals.
    for cell in workload['cells']:
        equality = cell['representation'] == 'equality'
        assert cell['representation'] in ('storage', 'equality')
        assert cell['tenant_form'] in ('canonical', 'uppercase')
        assert cell['payload_bytes'] in (16, 1024)
        field = cf1.FieldDescriptor(domain, table, field_id, 'int64-be/v1', 'uuid16/v1',
            'cf1-packed-equality/v1' if equality else 'cf1-storage/v1', bytes(range(32)))
        contexts = [KeyContext(domain, tenant, 'payload', UUID(int=14), 1)]
        if equality: contexts.append(KeyContext(domain, tenant, 'search', UUID(int=15), 2))
        wrappers = tuple(WrappedRoot(provider, c, b'synthetic-not-a-provider-wrapper') for c in contexts)
        policy = KeyPolicy(domain, tenant, wrappers, 1, 2 if equality else None)
        materials = {(c.purpose, c.generation): _Material(c,
            bytes(range(32)) if c.purpose == 'payload' else bytes(range(32, 64)),
            time.monotonic() + 300.0) for c in contexts}
        keys = PreparedKeys(policy, MappingProxyType(materials), os.getpid())
        plaintext = 'x' * cell['payload_bytes']
        frame = cf1.seal_text(plaintext, field, tenant, 7, keys)
        row_tenant = str(tenant) if cell['tenant_form'] == 'canonical' else str(tenant).upper()
        row = [frame.hex(), 7, row_tenant]
        operation = SimpleNamespace(keys=keys, tenant=tenant, points=())
        proc = adapter._ReadText(SimpleNamespace(descriptor=field), operation, column('record', BigInteger()))
        assert proc.process_result_value(row, None) == plaintext
        assert cell['id'] not in fixtures
        fixtures[cell['id']] = (proc.process_result_value, row, plaintext)
    # Both members of a pair use exactly the same cell order. Across pairs rotate/reverse it.
    pair = index // 2
    order = [c['id'] for c in workload['cells']]
    order = order[pair:] + order[:pair]
    if pair % 2: order.reverse()
    for cell_id in order:
        process, row, expected = fixtures[cell_id]
        sample = {'cell':cell_id, 'position':len(samples), 'status':'STARTED'}
        samples.append(sample)
        gc.collect()
        for _ in range(workload['warmup_calls']):
            assert process(row, None) == expected
        outputs = []
        enabled = gc.isenabled()
        gc.disable()
        try:
            before = resource.getrusage(resource.RUSAGE_SELF)
            cpu_start = time.process_time_ns()
            wall_start = time.perf_counter_ns()
            for _ in range(workload['timed_calls']):
                outputs.append(process(row, None))
            wall_end = time.perf_counter_ns()
            cpu_end = time.process_time_ns()
            after = resource.getrusage(resource.RUSAGE_SELF)
        finally:
            if enabled: gc.enable()
        assert len(outputs) == workload['timed_calls']
        assert all(type(value) is str and value == expected for value in outputs)
        sample.update({'status':'COMPLETE', 'calls':len(outputs),
            'warmup_calls':workload['warmup_calls'], 'outputs_verified':len(outputs),
            'wall_ns':wall_end-wall_start, 'cpu_ns':cpu_end-cpu_start,
            'maxrss_before_kib':before.ru_maxrss, 'maxrss_after_kib':after.ru_maxrss,
            'voluntary_switches':after.ru_nvcsw-before.ru_nvcsw,
            'involuntary_switches':after.ru_nivcsw-before.ru_nivcsw,
            'minor_faults':after.ru_minflt-before.ru_minflt,
            'major_faults':after.ru_majflt-before.ru_majflt})
        del outputs
    return samples

def main():
    admitted = {}; before = {}; final = {}; primary = None; samples = None; stage = 'STARTUP'
    try:
        assert len(sys.argv) == 4 and sys.argv[1] in VARIANTS
        variant, index_text, seal = sys.argv[1:]
        assert index_text in tuple(str(i) for i in range(16))
        index = int(index_text)
        assert len(seal) == 64 and all(c in '0123456789abcdef' for c in seal)
        assert Path(__file__) == ROOT / 'benchmark.py' and Path.cwd() == ROOT
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
        control_names = ('benchmark.py', 'DEPENDENCIES.json', 'VIEWS.json', 'WORKLOAD.json', 'PLAN.md')
        # Full control metadata first; retain stamps through expanded admission.
        for name in control_names: before[str(ROOT/name)] = stamp(ROOT/name)
        controls = {}
        for name in control_names:
            data = read(ROOT/name, before[str(ROOT/name)])
            assert hashlib.sha256(data).hexdigest() == manifest[name]
            admitted[str(ROOT/name)] = manifest[name]; controls[name] = data
        deps = json.loads(controls['DEPENDENCIES.json']); views = json.loads(controls['VIEWS.json'])
        workload = json.loads(controls['WORKLOAD.json'])
        assert len(deps['files']) == 399 and len(views[variant]) == 43
        assert workload['sequence'] == ['baseline', 'candidate', 'candidate', 'baseline'] * 4
        assert workload['sequence'][index] == variant and len(workload['cells']) == 8
        assert workload['warmup_calls'] == 128 and workload['timed_calls'] == 4096
        assert sys.platform == 'linux'
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
                if (isinstance(mode, str) and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                    raise PermissionError('write denied')
                if isinstance(path, int): return  # read-only owned fdopen; no fd write exception
                path = os.fsdecode(path)
                if not os.path.isabs(path) or os.path.normpath(path) != path:
                    raise PermissionError('noncanonical read denied')
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
        stage = 'MEASURE'
        samples = []
        measure(adapter, workload, index, samples)
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
        samples_ok = samples is not None and len(samples) == 8 and all(s.get('outputs_verified') == 4096 and s.get('status') == 'COMPLETE' for s in samples)
        closure_ok = bool(admitted) and len(admitted) == 448 and all(v == 'PASS' for v in final.values())
        success = primary is None and samples_ok and closure_ok and absence == 'PASS'
        summary = {'scope':'same-host-SA21-noDB-realCF1-ReadText',
            'variant':sys.argv[1] if len(sys.argv)>1 else None,
            'index':int(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2].isdigit() else None,
            'status':'PASS' if success else 'HOLD', 'primary_type':primary,
            'primary_stage':stage if primary else None, 'samples':samples,
            'admitted':len(admitted), 'closure':final, 'bytecode_absence':absence,
            'claims':'raw local samples only; reducer and independent review required'}
        sys.stdout.write('BENCHMARK_JSON ' + json.dumps(summary, sort_keys=True) + '\n'); sys.stdout.flush()
    return 0 if success else 1

if __name__ == '__main__':
    raise SystemExit(main())

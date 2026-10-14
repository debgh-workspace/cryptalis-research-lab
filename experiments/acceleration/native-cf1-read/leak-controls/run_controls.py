"""Bounded stdlib-only supervisor. No candidate imports or provider operations."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).absolute().parent
CAP = 1048576
OVERLAY = {
    'ASAN_OPTIONS': 'detect_leaks=1:leak_check_at_exit=1:halt_on_error=1:abort_on_error=0',
    'LSAN_OPTIONS': 'exitcode=23:report_objects=1',
    'UBSAN_OPTIONS': 'halt_on_error=1:print_stacktrace=1',
}

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def save(name, obj):
    with (ROOT / name).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

START = time.monotonic()

def run(label, argv, env):
    # Claim every output before launching, preserving partial failures.
    handles = {k: (ROOT / (label + '.' + k)).open('xb') for k in ('stdout', 'stderr')}
    receipt_file = (ROOT / (label + '.json')).open('x')
    receipt = {'argv': argv, 'cwd': str(ROOT), 'status': 'FAILED', 'environment_overlay': OVERLAY if env else {}}
    proc = None
    sel = selectors.DefaultSelector()
    sizes = {'stdout': 0, 'stderr': 0}
    problem = None
    try:
        deadline = min(START + 150, time.monotonic() + 30)
        proc = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, start_new_session=True)
        for key, stream in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
            os.set_blocking(stream.fileno(), False)
            sel.register(stream, selectors.EVENT_READ, key)
        while sel.get_map():
            if time.monotonic() >= deadline:
                problem = 'deadline-exceeded'
                break
            for event, _ in sel.select(min(0.1, max(0, deadline-time.monotonic()))):
                block = os.read(event.fileobj.fileno(), 65536)
                key = event.data
                if not block:
                    sel.unregister(event.fileobj)
                    event.fileobj.close()
                    continue
                room = CAP - sizes[key]
                handles[key].write(block[:room])
                sizes[key] += min(len(block), room)
                if len(block) > room:
                    problem = key + '-cap-exceeded'
                    break
            if problem:
                break
        if not problem:
            try:
                proc.wait(timeout=max(0.001, deadline-time.monotonic()))
            except subprocess.TimeoutExpired:
                problem = 'exit-deadline-exceeded'
        if problem:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)
        receipt.update(exit=proc.returncode, problem=problem, captured_bytes=sizes,
                       status='CAPTURED' if problem is None else 'FAILED')
    except BaseException as exc:
        receipt.update(error_type=type(exc).__name__, error=str(exc))
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)
        raise
    finally:
        sel.close()
        for handle in handles.values():
            handle.close()
        for key in handles:
            receipt[key + '_sha256'] = digest(ROOT / (label + '.' + key))
        json.dump(receipt, receipt_file, indent=2)
        receipt_file.write('\n')
        receipt_file.close()
    if problem:
        raise RuntimeError(label + ': ' + problem)
    return receipt, (ROOT / (label + '.stdout')).read_text(), (ROOT / (label + '.stderr')).read_text()

def main():
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    launcher_pin = json.loads((ROOT / 'LAUNCHER_FREEZE.json').read_text())
    if digest(__file__) != launcher_pin['launcher_sha256']:
        raise RuntimeError('Launcher pin changed')
    for path, wanted in freeze['pins'].items():
        if digest(path) != wanted:
            raise RuntimeError('Frozen pin mismatch: ' + path)
    if (ROOT / 'leak_control').exists():
        raise RuntimeError('Refuse existing binary')
    selected = {key: value for key, value in os.environ.items()
                if key in ('LD_PRELOAD', 'LD_AUDIT') or key.startswith(('ASAN_', 'LSAN_', 'UBSAN_', 'SANITIZER_'))}
    # Only equal frozen settings may be inherited. No removals or global changes.
    conflicts = [key for key, value in selected.items()
                 if (key not in OVERLAY and value) or (key in OVERLAY and value != OVERLAY[key])]
    save('PREFLIGHT.json', {'status': 'BLOCKED' if conflicts else 'PASS',
                          'relevant_inherited_names': sorted(selected),
                          'conflicting_names': sorted(conflicts),
                          'launcher_sha256': digest(__file__), 'freeze_sha256': digest(ROOT/'FREEZE.json')})
    if conflicts:
        raise RuntimeError('Conflicting inherited loader/sanitizer settings: ' + ', '.join(conflicts))
    argv = ['/usr/bin/gcc', '-std=c11', '-O1', '-g', '-Wall', '-Wextra', '-Werror',
            '-fno-omit-frame-pointer', '-fno-optimize-sibling-calls',
            '-fsanitize=address,undefined', 'leak_control.c', '-o', 'leak_control']
    build, stdout, stderr = run('build', argv, None)
    if build['exit'] != 0:
        raise RuntimeError('Compilation failed')
    save('BINARY.json', {'sha256': digest(ROOT/'leak_control'), 'source_sha256': digest(ROOT/'leak_control.c')})
    elf, stdout, stderr = run('elf', ['/usr/bin/readelf', '-d', 'leak_control'], None)
    if elf['exit'] != 0 or 'libasan.so.8' not in stdout or 'libubsan.so.1' not in stdout:
        raise RuntimeError('Unexpected dynamic dependencies')
    env = dict(os.environ)
    env.update(OVERLAY)
    results = []
    for mode in ('clean', 'free', 'leak'):
        receipt, stdout, stderr = run(mode, ['./leak_control', mode], env)
        expected_stdout = 'CONTROL completed mode=%s bytes=%d normal-return\n' % (mode, 0 if mode == 'clean' else 131071)
        if stdout != expected_stdout:
            raise RuntimeError(mode + ': unexpected stdout')
        if mode != 'leak':
            if receipt['exit'] != 0 or stderr:
                raise RuntimeError(mode + ': expected clean exit/stderr')
        else:
            required = ['LeakSanitizer: detected memory leaks',
                        'Direct leak of 131071 byte(s) in 1 object(s)',
                        '131071 byte(s) leaked in 1 allocation(s)', 'allocation_control', 'leak_control.c']
            if receipt['exit'] != 23 or not all(x in stderr for x in required):
                raise RuntimeError('leak: detector/provenance signature not established; independent address review may be required')
        results.append({'mode': mode, 'exit': receipt['exit'], 'status': 'EXPECTED'})
    save('RESULTS.json', {'status': 'PASS_STANDALONE_CONTROLS_ONLY', 'results': results,
                          'binary_sha256': digest(ROOT/'leak_control'),
                          'source_sha256': digest(ROOT/'leak_control.c'),
                          'launcher_sha256': digest(__file__)})

if __name__ == '__main__':
    try:
        main()
    except BaseException as exc:
        save('STOP.json', {'status': 'STOPPED_NO_RETRY', 'error_type': type(exc).__name__, 'error': str(exc)})
        raise

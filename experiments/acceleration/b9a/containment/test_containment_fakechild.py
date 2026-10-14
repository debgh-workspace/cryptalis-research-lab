"""Bounded stdlib-only controls. AST-load only transport helpers, no product/DB imports."""
import ast
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
import unittest

SOURCE = Path(__file__).parent / 'tests/test_payload_rotation_journal.py'
NAMES = {'WORKER_BOOTSTRAP', 'WORKER_OUTPUT_LIMIT', 'launch_contained',
         'read_worker_output', 'decode_worker_receipt', 'worker_line',
         'completed_worker', 'terminate_worker_group', 'abort_worker_cleanup'}
tree = ast.parse(SOURCE.read_text())
selected = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in NAMES:
        selected.append(node)
    elif isinstance(node, ast.Assign) and any(isinstance(n, ast.Name) and n.id in NAMES for n in node.targets):
        selected.append(node)
namespace = dict(globals())
exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE), 'exec'), namespace)
for name in NAMES:
    globals()[name] = namespace[name]


def fake(code):
    env = {k: v for k, v in os.environ.items() if not k.startswith(('CRYPTALIS_', 'PG'))}
    return launch_contained('code', code, env=env)


def terminal(pid):
    try:
        # Only the PID emitted by our own fake child is inspected.
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[0] == 'Z'
    except FileNotFoundError:
        return True


class ContainmentControls(unittest.TestCase):
    def check_failure(self, code, method, error, message, timeout=.15):
        p = fake(code)
        started = time.monotonic()
        try:
            with self.assertRaisesRegex(error, message):
                method(p, timeout=timeout)
        finally:
            terminate_worker_group(p, grace=.2)
        self.assertLess(time.monotonic() - started, 2)
        self.assertIsNotNone(p.returncode)
        self.assertTrue(all(s.closed for s in (p.stdin, p.stdout, p.stderr)))

    def test_silence_deadline(self):
        self.check_failure('import time; time.sleep(30)', worker_line, TimeoutError, 'deadline')

    def test_partial_line_deadline(self):
        self.check_failure("import os,time; os.write(1,b'{'); time.sleep(30)", worker_line, TimeoutError, 'deadline')

    def test_malformed_receipt_safe_error(self):
        self.check_failure("print('PRIVATE-FAKE-DIAGNOSTIC', flush=True)", worker_line, RuntimeError, '^worker receipt is malformed$')

    def test_completion_timeout(self):
        self.check_failure("import time; print('{}',flush=True); time.sleep(30)", completed_worker, TimeoutError, 'deadline')

    def test_partial_eof(self):
        self.check_failure("import os; os.write(1,b'{')", worker_line, RuntimeError, 'complete receipt')

    def test_stdout_size_bound(self):
        self.check_failure("import os,time; os.write(1,b'x'*100000); time.sleep(30)", worker_line, RuntimeError, 'size limit', timeout=1)

    def test_stderr_size_bound_and_drain(self):
        self.check_failure("import os,time; os.write(2,b'x'*100000); time.sleep(30)", worker_line, RuntimeError, 'size limit', timeout=1)

    def test_stderr_safe_completion_error(self):
        self.check_failure("import os; os.write(2,b'PRIVATE-FAKE-DIAGNOSTIC'); print('{}',flush=True)", completed_worker, RuntimeError, '^worker failed; diagnostic contents withheld$')

    def test_coalesced_receipts_preserve_remainder(self):
        p = fake("import os; os.write(1,b'{\"first\":1}\\n{\"second\":2}\\n')")
        try:
            self.assertEqual(worker_line(p, timeout=1), {'first': 1})
            self.assertEqual(completed_worker(p, timeout=1), {'second': 2})
        finally:
            terminate_worker_group(p, grace=.2)

    def test_group_cleanup_includes_term_ignoring_descendant(self):
        p = fake("""import json, os, signal, time
child = os.fork()
if child == 0:
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    os.write(1, (json.dumps({'pid': os.getpid()})+'\\n').encode())
    time.sleep(30)
else:
    time.sleep(30)
""")
        child = None
        try:
            child = worker_line(p, timeout=1)['pid']
        finally:
            terminate_worker_group(p, grace=.2)
        deadline = time.monotonic()+1
        while child is not None and not terminal(child) and time.monotonic()<deadline:
            time.sleep(.01)
        self.assertIsNotNone(child)
        self.assertTrue(terminal(child))
        self.assertTrue(all(s.closed for s in (p.stdin, p.stdout, p.stderr)))

    def test_parent_death_kills_direct_child(self):
        # Coordinator imports this file without executing unittest.main; only
        # selected stdlib transport functions can be imported or executed.
        code = f"""import json, runpy
n = runpy.run_path({str(Path(__file__).resolve())!r})
p = n['fake'](\"import os,json,time; print(json.dumps({{'pid':os.getpid()}}),flush=True); time.sleep(30)\")
receipt = n['worker_line'](p, timeout=1)
print(json.dumps(receipt), flush=True)
"""
        coordinator = fake(code)
        child = None
        try:
            child = completed_worker(coordinator, timeout=2)['pid']
        finally:
            terminate_worker_group(coordinator, grace=.2)
        deadline = time.monotonic()+1
        while child is not None and not terminal(child) and time.monotonic()<deadline:
            time.sleep(.01)
        self.assertIsNotNone(child)
        self.assertTrue(terminal(child))

    def test_unknown_cleanup_aborts_before_finally(self):
        code = f"""import json, runpy, types
n = runpy.run_path({str(Path(__file__).resolve())!r})
p = n['fake'](\"import os,json,time; print(json.dumps({{'pid':os.getpid()}}),flush=True); time.sleep(30)\")
receipt = n['worker_line'](p, timeout=1)
print(json.dumps(receipt), flush=True)
try:
    n['abort_worker_cleanup'](types.SimpleNamespace(workers=[p]))
finally:
    print('UNSAFE-TEARDOWN-RAN', flush=True)
"""
        coordinator = fake(code)
        child = None
        try:
            stdout, stderr = coordinator.communicate(timeout=3)
            self.assertEqual(coordinator.returncode, 86)
            self.assertEqual(stderr, b'B9A containment UNKNOWN: backend termination unconfirmed; fixture teardown aborted (exit 86).\n')
            self.assertNotIn(b'UNSAFE-TEARDOWN-RAN', stdout)
            child = json.loads(stdout)['pid']
        finally:
            terminate_worker_group(coordinator, grace=.2)
        self.assertTrue(terminal(child))


if __name__ == '__main__':
    unittest.main(verbosity=2)

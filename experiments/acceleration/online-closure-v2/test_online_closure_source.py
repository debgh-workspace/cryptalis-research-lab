"""Source-structure checks only. Never import the fixture or contact PostgreSQL.

Prepared, NOT RUN. Passing these checks would not prove lock/race safety.
Run only after coordinator admission; no pytest collection of candidate tests.
"""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / 'candidate-online-closure-v2-20261014'


def method(filename, classname, name):
    source = (CANDIDATE / 'tests' / filename).read_text()
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == classname)
    node = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == name)
    return node, ast.get_source_segment(source, node)


def calls(node, attr):
    return [n for n in ast.walk(node) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == attr]


class OnlineClosureSourceChecks(unittest.TestCase):
    def test_pin_and_phase_are_read_together_with_share(self):
        node, text = method('_online_cf1_lab.py', 'CF1EnumerationLab', '_require_pin')
        self.assertIn('SELECT crypto_pin,phase FROM operation WHERE singleton AND id=%s', text)
        self.assertIn('query += " FOR SHARE"', text)
        self.assertIn('if lock and row[1] != "PREPARING":', text)
        self.assertIn('raise FixturePhaseMismatch', text)
        self.assertEqual(len(calls(node, 'execute')), 1)
        self.assertLess(text.index('query += " FOR SHARE"'), text.index('c.execute'))
        self.assertLess(text.index('c.execute'), text.index('if lock and row[1]'))

    def test_every_admitted_producer_and_installer_checks_inside_transaction(self):
        entries = [('_online_cf1_lab.py', 'CF1EnumerationLab', name)
                   for name in ('page', 'seed', 'install')]
        entries += [('_online_cf1_process_lab.py', 'ChildFrameLab', name)
                    for name in ('page', 'seed', 'install_presealed')]
        for filename, cls, name in entries:
            with self.subTest(path=filename, method=name):
                node, _ = method(filename, cls, name)
                transaction = next(n for n in node.body if isinstance(n, ast.With))
                self.assertTrue(calls(transaction.items[0].context_expr, 'transaction'))
                first = transaction.body[0]
                admission = calls(first, '_require_pin')
                self.assertEqual(len(admission), 1)
                self.assertTrue(any(k.arg == 'lock' and isinstance(k.value, ast.Constant)
                                    and k.value.value is True for k in admission[0].keywords))
                self.assertFalse(calls(first, 'execute'))

    def test_d4_shares_the_exact_admission_helper(self):
        text = (CANDIDATE / 'tests/_online_cf1_process_lab.py').read_text()
        self.assertIn('_require_pin = CF1EnumerationLab._require_pin', text)
        self.assertNotIn('def _require_pin(', text)

    def test_worker_barrier_uses_non_key_lock_and_has_no_phase_write(self):
        node, text = method('_online_cf1_lab.py', 'CF1EnumerationLab', 'preparation_worker_barrier')
        executions = calls(node, 'execute')
        self.assertEqual(len(executions), 1)
        sql = executions[0].args[0].value
        self.assertEqual(sql, 'SELECT crypto_pin,phase FROM operation WHERE singleton AND id=%s FOR NO KEY UPDATE')
        self.assertIn('if row[1] != "PREPARING":', text)
        self.assertLess(text.index('raise FixturePhaseMismatch'), text.index('yield'))
        self.assertEqual(len([n for n in ast.walk(node) if isinstance(n, ast.Yield)]), 1)
        self.assertFalse([n for n in ast.walk(node) if isinstance(n, ast.Return)])

    def test_lab_phase_domain_is_closed(self):
        _, text = method('_online_cf1_lab.py', 'CF1EnumerationLab', 'install_capture')
        self.assertIn("phase text NOT NULL DEFAULT 'PREPARING'", text)
        self.assertIn("CHECK (phase IN ('PREPARING','PAUSED','PAUSED_VERIFIED'))", text)

    def test_retained_capture_and_oracle_bytes_are_unchanged(self):
        base = ROOT / 'candidate-accel-online-cf1-convergence-20261013'
        for relative in ('tests/_online_enumeration_lab.py', 'experiments/independent_cf1_decode.py',
                         'tests/test_online_cf1_convergence.py'):
            with self.subTest(path=relative):
                self.assertEqual((CANDIDATE / relative).read_bytes(), (base / relative).read_bytes())
        _, current = method('_online_cf1_lab.py', 'CF1EnumerationLab', 'oracle')
        original_source = (base / 'tests/_online_cf1_lab.py').read_text()
        original_tree = ast.parse(original_source)
        cls = next(n for n in original_tree.body if isinstance(n, ast.ClassDef) and n.name == 'CF1EnumerationLab')
        original = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'oracle')
        self.assertEqual(current, ast.get_source_segment(original_source, original))


    def test_child_plaintext_stage_routes_refuse_before_any_effect(self):
        for name in ('install', 'drain', 'finish'):
            with self.subTest(route=name):
                node, _ = method('_online_cf1_process_lab.py', 'ChildFrameLab', name)
                self.assertEqual(len(node.body), 1)
                refusal = node.body[0]
                self.assertIsInstance(refusal, ast.Raise)
                self.assertIsInstance(refusal.exc, ast.Call)
                self.assertIsInstance(refusal.exc.func, ast.Name)
                self.assertEqual(refusal.exc.func.id, 'FixtureRouteUnsupported')
                self.assertFalse(calls(node, 'execute'))
                self.assertFalse(calls(node, 'transaction'))

    def test_full_base_api_is_classified_and_write_dispatch_is_explicit(self):
        source = (CANDIDATE / 'tests/_online_enumeration_lab.py').read_text()
        base = next(n for n in ast.parse(source).body
                    if isinstance(n, ast.ClassDef) and n.name == 'EnumerationLab')
        names = {n.name for n in base.body if isinstance(n, ast.FunctionDef)}
        read_only = {'connect', 'reconstruct', 'claim', 'oracle', 'snapshot'}
        owner_or_native = {'__init__', 'close', 'install_capture', 'write'}
        prep = {'seed', 'page', 'install', 'drain', 'finish'}
        self.assertEqual(names, read_only | owner_or_native | prep)
        child_source = (CANDIDATE / 'tests/_online_cf1_process_lab.py').read_text()
        child = next(n for n in ast.parse(child_source).body
                     if isinstance(n, ast.ClassDef) and n.name == 'ChildFrameLab')
        child_names = {n.name for n in child.body if isinstance(n, ast.FunctionDef)}
        self.assertTrue(prep <= child_names)
        # CF1's inherited composition dynamically dispatches to gated overrides.
        for name, expected_calls in (('drain', {'claim', 'install'}),
                                     ('finish', {'page', 'drain', 'oracle'})):
            node = next(n for n in base.body if isinstance(n, ast.FunctionDef) and n.name == name)
            for target in expected_calls:
                self.assertTrue(any(isinstance(c.func.value, ast.Name)
                                    and c.func.value.id == 'self' for c in calls(node, target)))

if __name__ == '__main__':
    unittest.main()

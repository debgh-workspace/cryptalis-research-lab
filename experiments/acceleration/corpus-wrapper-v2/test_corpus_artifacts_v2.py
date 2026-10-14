"""Proposed non-DB fixtures. Import only the filesystem helper, never runner."""
from pathlib import Path
import ast
import json
import tempfile
import unittest
from unittest.mock import patch

import corpus_artifacts_v2 as c


class CorpusPreservation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'shared'
        self.out = Path(self.tmp.name) / 'run'
        self.root.mkdir(); self.out.mkdir()
        self.old = self.root / 'compatibility-state-corpus-v1-sa2.1.3.json'
        self.master = self.root / 'master-s4-compatibility-flush-corpus-v1-sa2.1.3.json'
        self.old.write_bytes(b'original'); self.master.write_bytes(b'master-original')

    def snapshot(self):
        return c.snapshot(self.root, self.out)

    def test_success_archives_both_patterns_and_restores(self):
        prior = self.snapshot()
        self.old.write_bytes(b'new'); self.master.write_bytes(b'master-new')
        report = c.capture_restore(self.root, self.out, prior)
        self.assertTrue(report['primary_receipts_restored'])
        self.assertEqual(self.old.read_bytes(), b'original')
        self.assertEqual(self.master.read_bytes(), b'master-original')
        self.assertEqual((self.out/'candidate-corpus'/self.master.name).read_bytes(), b'master-new')
        self.assertEqual((self.out/'prior-corpus'/self.master.name).read_bytes(), b'master-original')

    def test_failed_operation_still_captures_and_restores(self):
        prior = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'operation failure'):
            try:
                self.master.write_bytes(b'failed-run-output')
                raise ValueError('operation failure')
            finally:
                c.capture_restore(self.root, self.out, prior)
        self.assertEqual(self.master.read_bytes(), b'master-original')
        self.assertEqual((self.out/'candidate-corpus'/self.master.name).read_bytes(), b'failed-run-output')

    def test_new_file_archived_then_removed(self):
        prior = self.snapshot()
        new = self.root/'master-s4-compatibility-new-corpus-v1-sa2.0.51.json'
        new.write_bytes(b'new file')
        c.capture_restore(self.root, self.out, prior)
        self.assertFalse(new.exists())
        self.assertEqual((self.out/'candidate-corpus'/new.name).read_bytes(), b'new file')

    def test_deleted_original_restored_and_reported(self):
        prior = self.snapshot(); self.master.unlink()
        report = c.capture_restore(self.root, self.out, prior)
        self.assertEqual(report['deleted_during_run'], [self.master.name])
        self.assertEqual(self.master.read_bytes(), b'master-original')

    def test_unchanged_file_not_relabelled_as_new_output(self):
        report = c.capture_restore(self.root, self.out, self.snapshot())
        self.assertEqual(report['archived'], [])

    def test_archive_failure_retains_output_and_restores_other_file(self):
        prior = self.snapshot()
        self.old.write_bytes(b'new'); self.master.write_bytes(b'master-new')
        real = c.save_new
        def fail(path, data):
            if path.parent.name == 'candidate-corpus' and path.name == self.old.name:
                raise OSError('injected archive failure')
            return real(path, data)
        with patch.object(c, 'save_new', fail), self.assertRaises(RuntimeError):
            c.capture_restore(self.root, self.out, prior)
        self.assertEqual(self.old.read_bytes(), b'new')
        self.assertEqual(self.master.read_bytes(), b'master-original')
        self.assertEqual((self.out/'prior-corpus'/self.old.name).read_bytes(), b'original')
        self.assertFalse(json.loads((self.out/'candidate-corpus-isolation.json').read_text())['primary_receipts_restored'])

    def test_restore_failure_preserves_both_versions(self):
        prior = self.snapshot(); self.master.write_bytes(b'master-new')
        with patch.object(c, 'restore_one', side_effect=OSError('injected restore failure')), self.assertRaises(RuntimeError):
            c.capture_restore(self.root, self.out, prior)
        self.assertEqual(self.master.read_bytes(), b'master-new')
        self.assertEqual((self.out/'candidate-corpus'/self.master.name).read_bytes(), b'master-new')
        self.assertEqual((self.out/'prior-corpus'/self.master.name).read_bytes(), b'master-original')

    def test_snapshot_failure_occurs_without_changing_shared_files(self):
        with patch.object(c, 'save_new', side_effect=OSError('injected snapshot failure')), self.assertRaises(OSError):
            self.snapshot()
        self.assertEqual(self.master.read_bytes(), b'master-original')
        self.assertEqual(self.old.read_bytes(), b'original')

    def test_nonmatching_file_untouched(self):
        other = self.root/'unrelated.json'; other.write_bytes(b'unrelated')
        c.capture_restore(self.root, self.out, self.snapshot())
        self.assertEqual(other.read_bytes(), b'unrelated')

    def test_symlink_rejected_before_snapshot(self):
        self.master.unlink(); self.master.symlink_to(self.old)
        with self.assertRaises(RuntimeError): self.snapshot()
        self.assertEqual(self.old.read_bytes(), b'original')

    def test_wrapper_stop_failure_still_restores_and_releases_lock(self):
        # Execute ONLY the parsed finally block with injected filesystem fakes.
        # Never import run_baseline, wrapper main, or any database connector.
        source = Path(__file__).with_name('lab_session_corpus_v2.py').read_text()
        main = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        final = next(n.finalbody for n in main.body if isinstance(n, ast.Try) and n.finalbody)
        events = []
        class Lock:
            def close(self): events.append('close')
        def stop(*args):
            events.append('stop')
            raise OSError('injected stop-report failure')
        def restore(*args): events.append('restore')
        scope = dict(started_server=True, run=stop, PGCTL=Path('/unused'),
                     RUNTIME=Path('/unused'), BASE=Path('/unused'), evidence=self.out,
                     prior_corpus={}, capture_restore=restore, lock=Lock())
        module = ast.fix_missing_locations(ast.Module(body=final, type_ignores=[]))
        with self.assertRaises(OSError): exec(compile(module, '<finally-only>', 'exec'), scope)
        self.assertEqual(events, ['stop', 'restore', 'close'])

    def test_wrapper_restore_failure_still_releases_lock(self):
        source = Path(__file__).with_name('lab_session_corpus_v2.py').read_text()
        main = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        final = next(n.finalbody for n in main.body if isinstance(n, ast.Try) and n.finalbody)
        events = []
        class Lock:
            def close(self): events.append('close')
        def restore(*args):
            events.append('restore')
            raise RuntimeError('injected restoration failure')
        scope = dict(started_server=False, BASE=Path('/unused'), evidence=self.out,
                     prior_corpus={}, capture_restore=restore, lock=Lock())
        module = ast.fix_missing_locations(ast.Module(body=final, type_ignores=[]))
        with self.assertRaises(RuntimeError): exec(compile(module, '<finally-only>', 'exec'), scope)
        self.assertEqual(events, ['restore', 'close'])


if __name__ == '__main__':
    unittest.main()

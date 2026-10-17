"""Inert proposal: real helper imports, deterministic doubles, no database.

Root must admit the interpreter, full package view, and dependencies before
running this standalone unittest file. It has no pytest/conftest bootstrap.
These unit oracles do not establish physical release or native ORM recovery.
"""
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import cryptalis.sqlalchemy as adapter
import cryptalis._sqlalchemy_transactions as transactions


def diagnostic_failure(kind, calls):
    class NoteOverrideFailure(BaseException):
        def add_note(self, message):
            calls.append("override")
            raise RuntimeError("synthetic note delivery failure")

    failure = NoteOverrideFailure() if kind == "override" else RuntimeError("synthetic primary")
    if kind == "unavailable":
        failure.__notes__ = ()
    return failure


class FlushDiagnosticContinuation(unittest.TestCase):
    def test_primary_survives_and_cleanup_is_attempted(self):
        for kind in ("ordinary", "override", "unavailable"):
            for outcome in ("success", "rollback_failure", "quarantine_incomplete"):
                with self.subTest(note=kind, cleanup=outcome):
                    hooks, cleanup_calls, exception_contexts = [], [], []
                    primary = diagnostic_failure(kind, hooks)
                    session = SimpleNamespace(_prepared=object())
                    cleanup = RuntimeError("synthetic cleanup failure")

                    def fail_prepared_flush(current, *, cleanup_state):
                        cleanup_calls.append(current)
                        exception_contexts.append(sys.exception())
                        if outcome != "success":
                            cleanup_state["quarantine_incomplete"] = outcome == "quarantine_incomplete"
                            raise cleanup

                    with patch.object(adapter, "fail_prepared_flush", fail_prepared_flush):
                        try:
                            try:
                                raise primary
                            except BaseException as failure:
                                adapter._failed_flush_preparation(session, failure)
                                raise
                        except BaseException as observed:
                            self.assertIs(observed, primary)
                        else:
                            self.fail("The preparation failure must remain observable")
                    self.assertIsNone(session._prepared)
                    self.assertEqual(cleanup_calls, [session])
                    self.assertEqual(len(exception_contexts), 1)
                    self.assertIs(exception_contexts[0], primary)
                    self.assertEqual(hooks, [])
                    if kind == "unavailable":
                        self.assertEqual(primary.__notes__, ())
                    else:
                        notes = primary.__notes__
                        self.assertEqual(len(notes), 1 + (outcome != "success") +
                                         (outcome == "quarantine_incomplete"))
                        self.assertIn("Roll back", notes[0])
                        if outcome == "quarantine_incomplete":
                            self.assertIn("connection outcome is unknown", notes[-1])

    def test_note_failure_cannot_skip_close_or_later_connections(self):
        for kind in ("override", "unavailable"):
            for close_fails in (False, True):
                with self.subTest(note=kind, close_fails=close_fails):
                    hooks, calls, capture_flags = [], [], []
                    primary = diagnostic_failure(kind, hooks)

                    class Driver:
                        def close(self):
                            calls.append("close_first")
                            if close_fails:
                                raise RuntimeError("synthetic close failure")

                    class Connection:
                        closed = False
                        invalidated = False

                        def __init__(self, first):
                            self.first = first
                            self.connection = SimpleNamespace(dbapi_connection=Driver())

                        def invalidate(self):
                            calls.append("invalidate_first" if self.first else "invalidate_second")
                            if self.first:
                                raise RuntimeError("synthetic invalidation failure")
                            self.invalidated = True

                    class Transaction:
                        is_active = True

                        def _begin(self):
                            calls.append("begin")
                            return self

                        def rollback(self, *, _capture_exception):
                            capture_flags.append(_capture_exception)
                            calls.append("rollback")
                            raise primary

                    transaction = Transaction()
                    first, second = Connection(True), Connection(False)
                    session = SimpleNamespace(
                        get_nested_transaction=lambda: None,
                        get_transaction=lambda: transaction,
                        _control_connections=(first, second))
                    cleanup_state = {"quarantine_incomplete": None}
                    with self.assertRaises(BaseException) as caught:
                        transactions.fail_prepared_flush(session, cleanup_state=cleanup_state)
                    self.assertIs(caught.exception, primary)
                    self.assertEqual(len(capture_flags), 1)
                    self.assertIs(capture_flags[0], True)
                    self.assertEqual(calls, ["begin", "rollback", "invalidate_first",
                                             "close_first", "invalidate_second"])
                    self.assertTrue(second.invalidated)
                    self.assertIs(cleanup_state["quarantine_incomplete"], close_fails)
                    self.assertEqual(hooks, [])
                    if kind == "unavailable":
                        self.assertEqual(primary.__notes__, ())
                    else:
                        self.assertEqual(len(primary.__notes__), 1 + close_fails)

    def test_absent_or_inactive_transaction_does_not_start_cleanup(self):
        for transaction in (None, SimpleNamespace(is_active=False)):
            with self.subTest(transaction=transaction):
                session = SimpleNamespace(get_nested_transaction=lambda: None,
                                          get_transaction=lambda: transaction)
                # No _control_connections is available. No cleanup is needed.
                transactions.fail_prepared_flush(session, cleanup_state={"quarantine_incomplete": None})


if __name__ == "__main__":
    unittest.main()

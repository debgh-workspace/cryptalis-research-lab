"""Successor-only private outcome invariants; no database or external state."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import cryptalis.sqlalchemy as adapter
import cryptalis._sqlalchemy_transactions as transactions


class CleanupStateContract(unittest.TestCase):
    def test_unknown_outcomes_preserve_primary_and_warn_without_truth_dispatch(self):
        truth_hook_calls = []
        class FalseLike:
            def __bool__(self):
                truth_hook_calls.append("bool")
                raise AssertionError("Outcome objects must not be truth-tested")

        missing = object()
        for label, value in (("unpublished", None), ("missing", missing),
                             ("integer_zero", 0), ("false_like", FalseLike())):
            with self.subTest(outcome=label):
                primary = RuntimeError("synthetic preparation failure")
                session = SimpleNamespace(_prepared=object())
                observations = []

                def interrupted(current, *, cleanup_state):
                    observations.append((current, type(cleanup_state), dict(cleanup_state)))
                    if value is missing:
                        cleanup_state.clear()
                    else:
                        cleanup_state["quarantine_incomplete"] = value
                    raise RuntimeError("synthetic interruption before publication")

                with patch.object(adapter, "fail_prepared_flush", interrupted):
                    try:
                        try:
                            raise primary
                        except BaseException as failure:
                            adapter._failed_flush_preparation(session, failure)
                            raise
                    except BaseException as caught:
                        self.assertIs(caught, primary)
                    else:
                        self.fail("Primary failure must survive unknown cleanup")
                self.assertEqual(truth_hook_calls, [])
                self.assertEqual(len(observations), 1)
                self.assertIs(observations[0][0], session)
                self.assertIs(observations[0][1], dict)
                self.assertEqual(observations[0][2], {"quarantine_incomplete": None})
                self.assertIn("incomplete or unconfirmed", primary.__notes__[-1])
                self.assertIsNone(session._prepared)

    def test_interrupted_loop_never_publishes_partial_false(self):
        calls = []
        rollback_error = RuntimeError("synthetic rollback failure")
        inspection_error = RuntimeError("synthetic connection-state interruption")
        cleanup_state = {"quarantine_incomplete": None}

        class Connection:
            invalidated = True  # No captured driver; forces the inspection branch.

            @property
            def closed(self):
                calls.append("inspect_closed")
                if calls.count("inspect_closed") > 1:
                    raise inspection_error
                return False

            def invalidate(self):
                calls.append("invalidate")
                raise RuntimeError("synthetic invalidation failure")

        class Transaction:
            is_active = True

            def _begin(self):
                return self

            def rollback(self, *, _capture_exception):
                raise rollback_error

        transaction = Transaction()
        session = SimpleNamespace(get_nested_transaction=lambda: None,
                                  get_transaction=lambda: transaction,
                                  _control_connections=(Connection(),))
        with self.assertRaises(BaseException) as caught:
            transactions.fail_prepared_flush(session, cleanup_state=cleanup_state)
        self.assertIs(caught.exception, inspection_error)
        self.assertEqual(calls, ["inspect_closed", "invalidate", "inspect_closed"])
        self.assertIsNone(cleanup_state["quarantine_incomplete"])


if __name__ == "__main__":
    unittest.main()

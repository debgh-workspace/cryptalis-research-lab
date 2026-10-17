"""Shared note-only baseline/successor oracle through the unchanged outer API.

Standalone unittest, real helper imports and explicit local doubles. No DB.
Do not run until root has admitted exact sources, imports and command.
"""
import unittest
from types import SimpleNamespace

import cryptalis.sqlalchemy as adapter


def cleanup_failure(kind, hooks):
    class MarkerFailure(RuntimeError):
        def __setattr__(self, name, value):
            if name == "_cryptalis_quarantine_incomplete":
                hooks.append("set_true" if value is True else "set_false")
                if kind == "setter" or kind == "stale_false" and value is True:
                    raise RuntimeError("synthetic marker write failure")
            return super().__setattr__(name, value)

        def __getattribute__(self, name):
            if name == "_cryptalis_quarantine_incomplete":
                hooks.append("get_marker")
                if kind == "getter":
                    raise RuntimeError("synthetic marker read failure")
            return super().__getattribute__(name)

    class NameFailureMeta(type):
        def __getattribute__(cls, name):
            if name == "__name__":
                hooks.append("get_type_name")
                raise RuntimeError("synthetic type-name lookup failure")
            return super().__getattribute__(name)

    class NameFailure(RuntimeError, metaclass=NameFailureMeta):
        pass

    if kind == "type_name":
        return NameFailure("synthetic cleanup failure")
    if kind == "ordinary":
        return RuntimeError("synthetic cleanup failure")
    return MarkerFailure("synthetic cleanup failure")


class CleanupStateFaults(unittest.TestCase):
    def test_exception_hooks_cannot_interrupt_cleanup_or_publish_stale_success(self):
        for kind in ("ordinary", "setter", "getter", "stale_false", "type_name"):
            for close_fails in (False, True):
                with self.subTest(fault=kind, close_fails=close_fails):
                    hooks, calls, capture_flags = [], [], []
                    primary = RuntimeError("synthetic preparation failure")
                    rollback_error = cleanup_failure(kind, hooks)
                    invalidation_error = cleanup_failure(kind, hooks)
                    close_error = cleanup_failure(kind, hooks)

                    class Driver:
                        def close(self):
                            calls.append("close_first")
                            if close_fails:
                                raise close_error

                    class Connection:
                        closed = False
                        invalidated = False

                        def __init__(self, first):
                            self.first = first
                            self.connection = SimpleNamespace(dbapi_connection=Driver())

                        def invalidate(self):
                            calls.append("invalidate_first" if self.first else "invalidate_second")
                            if self.first:
                                raise invalidation_error
                            self.invalidated = True

                    class Transaction:
                        is_active = True

                        def _begin(self):
                            calls.append("begin")
                            return self

                        def rollback(self, *, _capture_exception):
                            capture_flags.append(_capture_exception)
                            calls.append("rollback")
                            raise rollback_error

                    transaction = Transaction()
                    first, second = Connection(True), Connection(False)
                    session = SimpleNamespace(
                        _prepared=object(),
                        get_nested_transaction=lambda: None,
                        get_transaction=lambda: transaction,
                        _control_connections=(first, second))
                    try:
                        try:
                            raise primary
                        except BaseException as failure:
                            adapter._failed_flush_preparation(session, failure)
                            raise
                    except BaseException as caught:
                        self.assertIs(caught, primary)
                    else:
                        self.fail("Preparation failure must remain observable")
                    self.assertIsNone(session._prepared)
                    self.assertEqual(capture_flags, [True])
                    self.assertEqual(calls, ["begin", "rollback", "invalidate_first",
                                             "close_first", "invalidate_second"])
                    self.assertTrue(second.invalidated)
                    self.assertEqual(hooks, [])
                    unknown = any("connection outcome is unknown" in note
                                  for note in primary.__notes__)
                    self.assertIs(unknown, close_fails)
                    self.assertEqual(len(primary.__notes__), 2 + close_fails)


if __name__ == "__main__":
    unittest.main()

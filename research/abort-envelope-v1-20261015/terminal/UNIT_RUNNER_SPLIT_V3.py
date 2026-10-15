"""Unexecuted split selector for the sealed abort-envelope unit proof.

Root selects and enforces process limits, captures wait4/getrusage on terminal
exit, and retains fresh receipts. This launcher does not select or retry a run.
Use python -I -B -S with exactly one argument: light17 or boundary1.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time
import unittest


BASE = Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/aborted-successor-envelope-v1-20261015")
INPUTS = (
    ("envelope_reference.py", "27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c"),
    ("test_envelope_reference.py", "152f8c605be07d5a63877f09942f66c3f89045457dad051cd8b85a780aa60d6c"),
    ("correction-v2/test_deciding_vectors.py", "e631a11f36b346984cee7304d22abefa2099e61c760d08a414af93d32fccf8cc"),
)
COMPLETED_ID = "sealed_abort_envelope_vectors_0.ReferenceVectors.test_cursor_domains_and_exact_widths"
BOUNDARY_ID = "sealed_abort_envelope_vectors_0.ReferenceVectors.test_exact_canonical_and_native_candidate_budget_edges"


def emit(value):
    print(json.dumps(value, sort_keys=True, separators=(",", ":")), flush=True)


def flatten(suite):
    for member in suite:
        if isinstance(member, unittest.TestSuite):
            yield from flatten(member)
        else:
            yield member


class AccountedResult(unittest.TextTestResult):
    """Supplementary per-method observations; parent must account signaled exit."""

    def startTest(self, test):
        self.method_started = time.monotonic()
        self.method_usage = resource.getrusage(resource.RUSAGE_SELF)
        emit({"event": "method_started", "method": test.id()})
        super().startTest(test)

    def addSuccess(self, test):
        super().addSuccess(test)
        emit({"event": "method_ok", "method": test.id()})

    def stopTest(self, test):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        emit({"event": "method_returned", "method": test.id(),
              "wall_seconds": time.monotonic() - self.method_started,
              "user_cpu_seconds": usage.ru_utime - self.method_usage.ru_utime,
              "system_cpu_seconds": usage.ru_stime - self.method_usage.ru_stime,
              "process_peak_rss_kib": usage.ru_maxrss})
        super().stopTest(test)


def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise RuntimeError("required_isolated_no_site_no_bytecode_flags")
    if len(sys.argv) != 2 or sys.argv[1] not in ("light17", "boundary1"):
        raise RuntimeError("explicit_split_mode_required")
    mode = sys.argv[1]
    for relative, expected in INPUTS:
        path = BASE / relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError("unexpected_input_file_type")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("sealed_input_digest_mismatch")
    sys.path.insert(0, str(BASE))
    original = unittest.TestSuite()
    for index, (relative, _) in enumerate(INPUTS[1:]):
        name = "sealed_abort_envelope_vectors_" + str(index)
        spec = importlib.util.spec_from_file_location(name, BASE / relative)
        if spec is None or spec.loader is None:
            raise RuntimeError("test_module_spec_unavailable")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        original.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    reference = sys.modules.get("envelope_reference")
    if reference is None or Path(reference.__file__) != BASE / INPUTS[0][0]:
        raise RuntimeError("unexpected_reference_module")
    all_methods = list(flatten(original))
    all_ids = [method.id() for method in all_methods]
    if original.countTestCases() != 19 or len(all_ids) != 19 or len(set(all_ids)) != 19:
        raise RuntimeError("unexpected_original_method_count")
    if COMPLETED_ID not in all_ids or BOUNDARY_ID not in all_ids:
        raise RuntimeError("expected_partition_member_missing")
    if mode == "light17":
        selected = [method for method in all_methods
                    if method.id() not in (COMPLETED_ID, BOUNDARY_ID)]
        expected = 17
    else:
        selected = [method for method in all_methods if method.id() == BOUNDARY_ID]
        expected = 1
    selected_ids = [method.id() for method in selected]
    if len(selected_ids) != expected or COMPLETED_ID in selected_ids:
        raise RuntimeError("unexpected_selected_method_set")
    emit({"event": "selection", "mode": mode, "original_method_count": 19,
          "expected_selected_method_count": expected,
          "selected_method_ids": selected_ids,
          "excluded_completed_method": COMPLETED_ID,
          "subtests_counted_separately": False})
    result = unittest.TextTestRunner(verbosity=2, resultclass=AccountedResult).run(
        unittest.TestSuite(selected))
    passed = (result.wasSuccessful() and result.testsRun == expected
              and not result.skipped and not result.expectedFailures
              and not result.unexpectedSuccesses)
    emit({"event": "partition_terminal", "mode": mode,
          "executed_method_count": result.testsRun, "expected_method_count": expected,
          "successful": passed, "failures": len(result.failures),
          "errors": len(result.errors), "skipped": len(result.skipped)})
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

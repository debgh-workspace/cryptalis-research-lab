"""Unexecuted, stdlib-only launch selector for the sealed abort-envelope tests.

Run only after root selects this isolated unit proof. No product import or DB.
Invoke with python3 -I -B -S; stdout/stderr belong to the selecting proof receipt.
"""

import hashlib
import importlib.util
from pathlib import Path
import sys
import unittest


BASE = Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/aborted-successor-envelope-v1-20261015")
INPUTS = (
    ("envelope_reference.py", "27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c"),
    ("test_envelope_reference.py", "152f8c605be07d5a63877f09942f66c3f89045457dad051cd8b85a780aa60d6c"),
    ("correction-v2/test_deciding_vectors.py", "e631a11f36b346984cee7304d22abefa2099e61c760d08a414af93d32fccf8cc"),
)
EXPECTED_TEST_METHODS = 19


def main():
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise RuntimeError("required_isolated_no_site_no_bytecode_flags")
    for relative, expected in INPUTS:
        path = BASE / relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError("unexpected_input_file_type")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("sealed_input_digest_mismatch")
    sys.path.insert(0, str(BASE))
    suite = unittest.TestSuite()
    for index, (relative, _) in enumerate(INPUTS[1:]):
        name = "sealed_abort_envelope_vectors_" + str(index)
        spec = importlib.util.spec_from_file_location(name, BASE / relative)
        if spec is None or spec.loader is None:
            raise RuntimeError("test_module_spec_unavailable")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    reference = sys.modules.get("envelope_reference")
    if reference is None or Path(reference.__file__) != BASE / INPUTS[0][0]:
        raise RuntimeError("unexpected_reference_module")
    if suite.countTestCases() != EXPECTED_TEST_METHODS:
        raise RuntimeError("unexpected_test_method_count")
    print("Expected test methods: 19; subtests are not counted separately.", flush=True)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("Executed test methods:", result.testsRun, flush=True)
    return 0 if result.wasSuccessful() and result.testsRun == EXPECTED_TEST_METHODS else 1


if __name__ == "__main__":
    raise SystemExit(main())

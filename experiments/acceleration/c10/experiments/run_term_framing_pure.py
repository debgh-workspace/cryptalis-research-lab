"""Run only C10 pure tests and preserve an exclusive, source-bound receipt."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import cryptalis.crypto.cf1 as cf1
import cryptography
import psycopg
import pytest
import sqlalchemy


class Results:
    def __init__(self):
        self.counts = {}
        self.failed = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call" or report.failed:
            outcome = report.outcome if report.when == "call" else "errors"
            self.counts[outcome] = self.counts.get(outcome, 0) + 1
            if report.failed:
                self.failed.append(report.nodeid)


def hashes():
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for folder in ("src", "tests", "scripts", "experiments")
            for path in sorted((ROOT / folder).rglob("*.py"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    assert not args.receipt.exists(), "Receipts are immutable; choose a new path."
    assert Path(cf1.__file__).resolve() == ROOT / "src/cryptalis/crypto/cf1.py"
    for name in ("CRYPTALIS_TEST_DATABASE_URL", "CRYPTALIS_TEST_RUNTIME_DATABASE_URL"):
        os.environ.pop(name, None)
    os.chdir(ROOT)
    results = Results()
    before = hashes()
    test_args = ["-q", "-p", "no:cacheprovider", "experiments/test_term_literal_framing.py"]
    code = int(pytest.main(test_args, plugins=[results]))
    after = hashes()
    receipt = {
        "scope": "C10 pure literal framing and CF1 equivalence; no PostgreSQL, no timing comparison",
        "python_executable": sys.executable, "python": platform.python_version(),
        "sqlalchemy": sqlalchemy.__version__, "cryptography": cryptography.__version__,
        "psycopg": psycopg.__version__, "cf1_import_origin": cf1.__file__,
        "pytest_args": test_args, "exit_code": code,
        "counts": results.counts, "failed_nodes": results.failed,
        "source_test_sha256": before, "source_unchanged": before == after,
        "manifest_sha256": hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
        "database_calls": 0, "timing_admission": "NOT RUN", "promotion": "HOLD",
        "gates": {name: "UNKNOWN" for name in (
            "G-ADAPTER", "G-CRYPTO", "G-QUERY", "G-LIFECYCLE", "G-PROVIDER", "G-POLICY", "G-RELEASE")},
    }
    with args.receipt.open("x") as stream:
        stream.write(json.dumps(receipt, indent=2) + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

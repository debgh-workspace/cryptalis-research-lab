"""One independent-observer control for D3 frame/retirement atomicity.

Run unchanged on passing D3 first, then on its isolated split-retirement mutant.
Only the coordinator uses the existing dual-role PostgreSQL runner.
"""
from pathlib import Path
import sys

import pytest


if "_cryptalis_test_preflight" not in sys.modules:
    raise pytest.UsageError("Run through the existing dual-role PostgreSQL runner.")

_test_root = Path.cwd() / "tests"
sys.path.insert(0, str(_test_root))
import _online_cf1_lab as helper
assert Path(helper.__file__).resolve() == (_test_root / "_online_cf1_lab.py").resolve()


def test_independent_observer_recovers_frame_after_retirement_fault():
    with helper.opened_cf1_lab(((10, "frame must survive the failed chunk"), (30, None), (50, "later page"))) as lab:
        with lab.connect() as worker:
            assert lab.page(worker) == (10, 30)
            claim = lab.claim(worker, 10)
            with pytest.raises(RuntimeError, match="CF1 worker after retire"):
                lab.install(worker, claim, fault="after_retire")
        resumed = helper.CF1EnumerationLab.reconstruct(lab.schema, lab.operation, lab.crypto)
        with resumed.connect() as worker:
            # No caller remembers or reseeds key 10 after reconstruction. D3's
            # independent observer must establish complete committed recovery.
            resumed.finish(worker)

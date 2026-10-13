"""Independent full-observer controls for the finite D1 enumeration experiment.

Run unchanged against D1 and each isolated one-omission candidate through the
existing coordinator-owned PostgreSQL runner. No product or online admission.
"""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
from pathlib import Path
from queue import Queue
import sys
import time

import pytest


if "_cryptalis_test_preflight" not in sys.modules:
    raise pytest.UsageError("Run through the existing dual-role PostgreSQL runner.")

# Resolve the helper from the selected candidate, never from a cached sibling.
_path = Path.cwd() / "tests" / "_online_enumeration_lab.py"
_spec = importlib.util.spec_from_file_location("_enumeration_sensitivity_lab", _path)
_lab = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _lab
_spec.loader.exec_module(_lab)
assert Path(_lab.__file__).resolve() == _path.resolve()
opened_lab = _lab.opened_lab
EnumerationLab = _lab.EnumerationLab


def test_observer_covers_insert_behind_committed_cursor():
    with opened_lab() as lab, lab.connect() as scanner, lab.connect() as writer:
        assert scanner.execute("SELECT * FROM dirty").fetchall() == []
        assert lab.page(scanner) == (10, 30)
        lab.write(writer, "insert", 5, "captured behind committed cursor")
        # The source insert is committed and the writer has no further work.
        # An omitted capture leaves no marker and cannot be repaired by paging.
        lab.finish(scanner)


def test_observer_covers_page_rollback_after_reconstruction():
    with opened_lab() as lab:
        with lab.connect() as scanner:
            with pytest.raises(RuntimeError, match="after_cursor"):
                lab.page(scanner, fault="after_cursor")
        resumed = EnumerationLab.reconstruct(lab.schema, lab.operation)
        with resumed.connect() as scanner:
            # No in-memory keys or manual reseed repairs an advanced cursor.
            resumed.finish(scanner)


def test_observer_rejects_claim_from_another_operation():
    with opened_lab(((10, "earlier operation"),)) as old, opened_lab(((10, "current operation"),)) as current:
        with old.connect() as a, current.connect() as b:
            assert old.page(a) == current.page(b) == (10,)
            stale = old.claim(a, 10)
            valid = current.claim(b, 10)
            assert stale.operation != valid.operation
            assert (stale.key, stale.token) == (valid.key, valid.token)
            assert stale.value != valid.value
            current.install(b, stale)
            # Judge committed native/source/stage values, not install's return.
            current.finish(b)
            old.finish(a)


def test_observer_rejects_claim_after_lower_token_capture_commits():
    with opened_lab(((10, "old"),)) as lab, lab.connect() as scanner:
        lock = lab.operation.int % (2**31)
        scanner.execute("""CREATE FUNCTION pause_after_revision() RETURNS trigger LANGUAGE plpgsql AS $$
            BEGIN PERFORM pg_advisory_xact_lock(""" + str(lock) + """); RETURN NEW; END $$""")
        scanner.execute("CREATE TRIGGER zz_research_pause BEFORE UPDATE ON source FOR EACH ROW EXECUTE FUNCTION pause_after_revision()")
        scanner.execute("SELECT pg_advisory_lock(%s)", (lock,))
        pids = Queue()

        def write():
            with lab.connect() as writer:
                pids.put(writer.info.backend_pid)
                lab.write(writer, "update", 10, "new")

        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(write)
            try:
                pid = pids.get(timeout=2)
                deadline = time.monotonic() + 2
                while scanner.info.backend_pid not in scanner.execute("SELECT pg_blocking_pids(%s)", (pid,)).fetchone()[0]:
                    assert time.monotonic() < deadline, "writer did not reach the scheduled capture boundary"
                    time.sleep(0.005)
                assert lab.page(scanner, size=1) == (10,)
                stale = lab.claim(scanner, 10)
                assert stale.value == "old"
            finally:
                assert scanner.execute("SELECT pg_advisory_unlock(%s)", (lock,)).fetchone() == (True,)
            future.result(timeout=3)
        # The observed source revision establishes the allocation-order schedule
        # under both implementations; token order itself is not the oracle.
        revision, value = scanner.execute("SELECT rev,v FROM source WHERE id=10").fetchone()
        assert revision < stale.token and value == "new"
        lab.install(scanner, stale)
        lab.finish(scanner)

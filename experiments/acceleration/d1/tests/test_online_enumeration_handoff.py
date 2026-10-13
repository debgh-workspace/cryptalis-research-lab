"""Finite PG16 enumeration/capture schedules; no online product admission.

The unchanged CP65 tests are selected separately as provenance/reuse controls.
All connection creation stays behind the repository's existing dual-role runner.
"""
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time
import uuid

import psycopg
import pytest

from _online_enumeration_lab import EnumerationLab, opened_lab


@pytest.mark.parametrize("schedule", [
    "insert_behind", "insert_between", "insert_ahead", "update_to_null",
    "update_from_null", "delete_selected", "reinsert_selected",
])
def test_current_page_handoff_covers_concurrent_native_changes(schedule):
    with opened_lab() as lab, lab.connect() as scanner, lab.connect() as writer:
        # These rows really predate capture: neither an existing dirty marker nor
        # a staged value can hide an initial-enumeration omission.
        assert scanner.execute("SELECT * FROM dirty").fetchall() == []
        assert scanner.execute("SELECT * FROM staged").fetchall() == []
        assert scanner.execute("SELECT rev FROM source ORDER BY id").fetchall() == [(0,), (0,), (0,)]

        def interleave(keys):
            assert keys == (10, 30)
            if schedule == "insert_behind":
                lab.write(writer, "insert", 5, "behind")
            elif schedule == "insert_between":
                lab.write(writer, "insert", 20, "between selected keys")
            elif schedule == "insert_ahead":
                lab.write(writer, "insert", 40, "ahead")
            elif schedule == "update_to_null":
                lab.write(writer, "update", 10, None)
            elif schedule == "update_from_null":
                lab.write(writer, "update", 30, "no longer NULL")
            elif schedule == "delete_selected":
                lab.write(writer, "delete", 10)
            else:
                lab.write(writer, "delete", 10)
                lab.write(writer, "insert", 10, "replacement")

        assert lab.page(scanner, after_read=interleave) == (10, 30)
        assert scanner.execute("SELECT last_key,complete FROM inventory").fetchone() == (30, False)
        lab.finish(scanner)


@pytest.mark.parametrize("schedule", ["behind_completed_cursor", "ahead_completed_cursor", "initially_empty"])
@pytest.mark.parametrize("arrival", ["before_completion_commit", "after_completion_commit"])
def test_insert_after_empty_page_read_remains_captured(schedule, arrival):
    rows = () if schedule == "initially_empty" else ((10, "ten"), (30, None))
    with opened_lab(rows) as lab, lab.connect() as scanner, lab.connect() as writer:
        if rows:
            assert lab.page(scanner) == (10, 30)
            lab.drain(scanner)
        key = 40 if schedule == "ahead_completed_cursor" else 0

        def interleave(keys):
            assert keys == ()
            lab.write(writer, "insert", key, None)

        assert lab.page(scanner, after_read=interleave if arrival == "before_completion_commit" else None) == ()
        assert scanner.execute("SELECT complete FROM inventory").fetchone() == (True,)
        if arrival == "after_completion_commit":
            lab.write(writer, "insert", key, None)
        assert lab.claim(scanner, key) is not None
        lab.drain(scanner)
        lab.oracle(scanner)


@pytest.mark.parametrize("fault", ["before_cursor", "after_cursor"])
def test_page_work_and_durable_cursor_rollback_and_reconnect(fault):
    with opened_lab() as lab:
        with lab.connect() as scanner:
            before = lab.snapshot(scanner)
            with pytest.raises(RuntimeError, match=fault):
                lab.page(scanner, fault=fault)
            assert lab.snapshot(scanner) == before
            assert scanner.execute("SELECT last_value FROM work_tokens").fetchone()[0] >= 2
        # A new object and connection use only the durable operation binding.
        resumed = EnumerationLab.reconstruct(lab.schema, lab.operation)
        assert resumed is not lab
        with resumed.connect() as restarted:
            assert resumed.page(restarted) == (10, 30)
            resumed.finish(restarted)


def test_empty_page_completion_rollback_is_not_durable_success():
    with opened_lab(()) as lab:
        with lab.connect() as scanner:
            before = lab.snapshot(scanner)
            with pytest.raises(RuntimeError, match="after_cursor"):
                lab.page(scanner, fault="after_cursor")
            assert lab.snapshot(scanner) == before
        with lab.connect() as writer:
            lab.write(writer, "insert", -1, "arrived after rollback")
        resumed = EnumerationLab.reconstruct(lab.schema, lab.operation)
        with resumed.connect() as restarted:
            assert resumed.page(restarted) == (-1,)
            resumed.finish(restarted)


def test_reconstruction_preserves_committed_prefix_after_later_page_rollback():
    with opened_lab() as lab:
        with lab.connect() as scanner:
            assert lab.page(scanner) == (10, 30)
            lab.drain(scanner)
            before = lab.snapshot(scanner)
            prefix = scanner.execute("SELECT * FROM staged ORDER BY id").fetchall()
            with pytest.raises(RuntimeError, match="after_cursor"):
                lab.page(scanner, fault="after_cursor")
            assert lab.snapshot(scanner) == before
        resumed = EnumerationLab.reconstruct(lab.schema, lab.operation)
        with resumed.connect() as restarted:
            assert restarted.execute("SELECT last_key,complete FROM inventory").fetchone() == (30, False)
            assert resumed.page(restarted) == (50,)
            assert restarted.execute("SELECT * FROM staged ORDER BY id").fetchall() == prefix
            resumed.finish(restarted)
            assert restarted.execute("SELECT * FROM staged WHERE id<=30 ORDER BY id").fetchall() == prefix


def test_reconstruction_refuses_wrong_expected_operation_without_effects():
    with opened_lab() as lab, lab.connect() as observer:
        lab.page(observer)
        before = lab.snapshot(observer)
        with pytest.raises(ValueError, match="durable operation identity mismatch"):
            EnumerationLab.reconstruct(lab.schema, uuid.uuid4())
        assert lab.snapshot(observer) == before
        lab.finish(observer)


def test_claim_namespace_refuses_prior_operation_with_same_key_and_token():
    with opened_lab(((10, "old operation"),)) as old, opened_lab(((10, "new operation"),)) as new:
        with old.connect() as a, new.connect() as b:
            old.page(a)
            new.page(b)
            stale = old.claim(a, 10)
            current = new.claim(b, 10)
            assert stale.operation != current.operation
            assert (stale.key, stale.token) == (current.key, current.token)
            assert stale.value != current.value
            before = new.snapshot(b)
            assert not new.install(b, stale)
            assert new.snapshot(b) == before
            assert new.install(b, current)
            new.finish(b)
            old.finish(a)


def test_page_retired_before_late_seeding_cannot_revive_old_claim():
    with opened_lab() as lab, lab.connect() as scanner, lab.connect() as worker:
        old_claim = None

        def interleave(keys):
            nonlocal old_claim
            assert keys == (10, 30)
            lab.write(worker, "update", 10, "first")
            old_claim = lab.claim(worker, 10)
            lab.write(worker, "update", 10, "current")
            lab.drain(worker)
            assert worker.execute("SELECT id,v FROM staged WHERE live").fetchall() == [(10, "current")]

        lab.page(scanner, after_read=interleave)
        before = lab.snapshot(worker)
        assert not lab.install(worker, old_claim)
        assert lab.snapshot(worker) == before
        lab.finish(worker)


def test_worker_stage_and_retirement_rollback_together():
    with opened_lab() as lab, lab.connect() as c:
        lab.page(c)
        claimed = lab.claim(c, 10)
        before = lab.snapshot(c)
        with pytest.raises(RuntimeError, match="worker before commit"):
            lab.install(c, claimed, fault=True)
        assert lab.snapshot(c) == before
        assert lab.install(c, claimed)
        lab.finish(c)


def test_writer_rollback_does_not_leave_capture_or_native_effects():
    with opened_lab() as lab, lab.connect() as scanner, lab.connect() as writer:
        def interleave(keys):
            before = lab.snapshot(writer)
            with pytest.raises(RuntimeError, match="writer rollback"):
                with writer.transaction():
                    lab.write(writer, "insert", 5, "uncommitted")
                    lab.write(writer, "update", 10, None)
                    raise RuntimeError("writer rollback")
            assert lab.snapshot(writer) == before
        lab.page(scanner, after_read=interleave)
        lab.finish(scanner)


def test_incomplete_inventory_is_not_a_success_even_when_queue_is_empty():
    with opened_lab() as lab, lab.connect() as c:
        lab.page(c)
        lab.drain(c)
        assert c.execute("SELECT * FROM dirty").fetchall() == []
        with pytest.raises(AssertionError):
            lab.oracle(c)
        lab.finish(c)


@pytest.mark.parametrize("corruption", ["missing", "stale", "null_substitution", "extra"])
def test_full_native_comparison_detects_incorrect_stage(corruption):
    with opened_lab() as lab, lab.connect() as c:
        lab.finish(c)
        if corruption == "missing":
            c.execute("DELETE FROM staged WHERE id=10")
        elif corruption == "stale":
            c.execute("UPDATE staged SET v='old value' WHERE id=10")
        elif corruption == "null_substitution":
            c.execute("UPDATE staged SET v=NULL WHERE id=10")
        else:
            c.execute("INSERT INTO staged VALUES(%s,11,'extra',true,1)", (lab.operation,))
        with pytest.raises(AssertionError):
            lab.oracle(c)


def test_identity_move_refuses_without_source_or_coordination_effects():
    with opened_lab() as lab, lab.connect() as c:
        lab.page(c)
        before = lab.snapshot(c)
        with pytest.raises(psycopg.errors.CheckViolation):
            c.execute("UPDATE source SET id=20 WHERE id=10")
        assert lab.snapshot(c) == before
        lab.finish(c)


def test_capture_installation_waits_for_prior_writer_and_retries_known_rollback():
    with opened_lab(capture=False) as lab, lab.connect() as writer, lab.connect() as installer:
        installer.execute("SET lock_timeout='100ms'")
        with writer.transaction():
            lab.write(writer, "update", 10, "before capture committed")
            with pytest.raises(psycopg.errors.LockNotAvailable):
                lab.install_capture(installer)
            assert installer.execute("SELECT to_regclass('operation')").fetchone() == (None,)
        lab.install_capture(installer)
        assert installer.execute("SELECT * FROM dirty").fetchall() == []
        lab.finish(installer)


def test_transaction_started_before_capture_executes_new_capture_on_later_write():
    with opened_lab(capture=False) as lab, lab.connect() as writer, lab.connect() as installer:
        with writer.transaction():
            assert writer.execute("SELECT 1").fetchone() == (1,)
            lab.install_capture(installer)
            lab.write(writer, "insert", -5, "earlier transaction later write")
        assert lab.claim(installer, -5) is not None
        lab.finish(installer)


def test_late_capture_with_earlier_allocated_token_invalidates_inventory_claim():
    # Allocation order is not commit order. Only initial producers use GREATEST;
    # a real source mutation must replace an earlier inventory obligation even
    # when the mutation allocated its token before that inventory was seeded.
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
                    assert time.monotonic() < deadline, "writer never reached the scheduled capture boundary"
                    time.sleep(0.005)
                assert lab.page(scanner, size=1) == (10,)
                stale = lab.claim(scanner, 10)
                assert stale.value == "old"
            finally:
                assert scanner.execute("SELECT pg_advisory_unlock(%s)", (lock,)).fetchone() == (True,)
            future.result(timeout=3)
        current = lab.claim(scanner, 10)
        assert current.token < stale.token
        assert current.value == "new"
        before = lab.snapshot(scanner)
        assert not lab.install(scanner, stale)
        assert lab.snapshot(scanner) == before
        lab.finish(scanner)

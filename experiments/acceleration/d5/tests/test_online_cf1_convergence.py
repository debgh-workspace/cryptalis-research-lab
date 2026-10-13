"""D5 finite queue convergence and empty-observation counterexamples.

All real database execution belongs to the coordinator's unchanged wrapper.
Separate connections provide fixed overlapping native transaction schedules;
there is no product closure certificate, new phase, or deployment writer fence.
"""
import pytest

from _online_cf1_lab import TENANT, opened_cf1_lab, oracle


ROWS = ((10, "ten 雪😀"), (30, None), (50, "fifty e\u0301 é"))
MUTATIONS = ("update", "delete", "delete_reinsert", "to_null", "from_null",
             "insert_behind", "insert_between", "insert_ahead")
PATTERNS = ("same_key", "alternating_keys")
CHURN_ROUNDS = 3


def committed_observation(lab, scanner):
    """Observe complete committed state and independently decode every live row.

    Queue and values share one read-only repeatable-read snapshot. This says
    nothing about an uncommitted writer or whether another writer can arrive.
    D2's separately qualified decoder uses externally expected public fixture
    descriptor, tenant, row and root, never a product decrypt function.
    """
    with lab.connect() as observer, observer.transaction():
        assert observer.info.backend_pid != scanner.info.backend_pid
        observer.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
        lab._require_pin(observer)
        inventory = observer.execute("SELECT last_key,complete FROM inventory WHERE operation=%s",
                                     (lab.operation,)).fetchone()
        dirty = observer.execute("SELECT operation,id,token FROM dirty ORDER BY operation,id").fetchall()
        source = observer.execute("SELECT id,v FROM source ORDER BY id").fetchall()
        native = observer.execute("SELECT id,v FROM native ORDER BY id").fetchall()
        frames = observer.execute("SELECT id,frame,live,token FROM staged WHERE operation=%s ORDER BY id",
                                  (lab.operation,)).fetchall()
        assert all(frame is None or type(frame) is bytes for _, frame, _, _ in frames)
        decoded = [(key, oracle.decode_cf1(
            frame, descriptor=lab.crypto.document, descriptor_digest=lab.crypto.digest,
            tenant=TENANT, record=key, payload=lab.crypto.root,
        )) for key, frame, live, _ in frames if live]
        return {"inventory": inventory, "dirty": dirty, "source": source,
                "native": native, "frames": frames, "decoded": decoded}


def assert_full_current(observed, expected):
    assert observed["inventory"] == (50, True)
    assert observed["dirty"] == []
    assert observed["source"] == expected
    assert observed["native"] == expected
    assert observed["decoded"] == expected


def initial_complete(lab, scanner):
    # Exactly three bounded pages, including the empty terminal page. No
    # unbounded retry or finishing loop is introduced by this research slice.
    for expected in ((10, 30), (50,), ()):
        assert lab.page(scanner, size=2) == expected
    lab.drain(scanner)
    observed = committed_observation(lab, scanner)
    assert_full_current(observed, list(ROWS))
    return observed


def writes_for(action):
    if action == "update":
        return (("update", 10, "changed after empty observation"),)
    if action == "delete":
        return (("delete", 10, None),)
    if action == "delete_reinsert":
        return (("delete", 10, None), ("insert", 10, "replacement 雪"))
    if action == "to_null":
        return (("update", 10, None),)
    if action == "from_null":
        return (("update", 30, "formerly NULL"),)
    key = {"insert_behind": -5, "insert_between": 20, "insert_ahead": 70}[action]
    return (("insert", key, "arrived beyond the completed inventory"),)


@pytest.mark.parametrize("action", MUTATIONS)
def test_empty_queue_and_full_snapshots_do_not_close_over_pending_writer(action):
    with opened_cf1_lab(ROWS) as lab, lab.connect() as scanner, lab.connect() as writer:
        baseline = initial_complete(lab, scanner)
        writes = writes_for(action)
        expected = dict(ROWS)
        affected = writes[-1][1]
        with writer.transaction():
            for command, key, value in writes:
                lab.write(writer, command, key, value)
                if command == "delete":
                    del expected[key]
                else:
                    expected[key] = value
            # The other backend has applied native/source/capture work but has
            # not committed. Its own view proves the mutation reached the DB.
            assert writer.execute("SELECT id,v FROM native ORDER BY id").fetchall() == sorted(expected.items())
            assert writer.execute("SELECT id FROM dirty ORDER BY id").fetchall() == [(affected,)]
            assert scanner.info.backend_pid != writer.info.backend_pid

            # Two separately opened complete observations can both be correct
            # and empty while the overlapping writer remains able to commit.
            for _ in range(2):
                lab.drain(scanner)
                observed = committed_observation(lab, scanner)
                assert observed == baseline
                assert_full_current(observed, list(ROWS))

        # COMMIT now exposes late work behind, between or beyond the completed
        # cursor. A snapshot match above never authorized a product switch.
        late = committed_observation(lab, scanner)
        assert late["inventory"] == baseline["inventory"]
        assert [key for _, key, _ in late["dirty"]] == [affected]
        assert late["source"] == late["native"] == sorted(expected.items())
        assert late["frames"] == baseline["frames"]
        assert late["decoded"] == list(ROWS)
        assert late["decoded"] != late["native"]
        with pytest.raises(AssertionError):
            assert_full_current(late, sorted(expected.items()))

        # The finite writer schedule is now over. Exactly one pending identity
        # is drained, without resuming/reseeding the already complete inventory.
        lab.drain(scanner)
        final = committed_observation(lab, scanner)
        assert_full_current(final, sorted(expected.items()))
        assert [row for row in final["frames"] if row[0] != affected] == [
            row for row in baseline["frames"] if row[0] != affected]
        lab.oracle(scanner)


@pytest.mark.parametrize("pattern", PATTERNS)
def test_three_late_commits_leave_work_then_stopped_writers_converge(pattern, monkeypatch):
    with opened_cf1_lab(ROWS) as lab, lab.connect() as scanner, lab.connect() as writer:
        baseline = initial_complete(lab, scanner)
        expected = dict(ROWS)
        expected[10] = "first dirty value"
        lab.write(writer, "update", 10, expected[10])
        original_install = lab.install

        # Each pass selects one dirty identity, installs it successfully, then
        # another native commit arrives before the pass returns. A completed
        # batch is not a closed queue, even when every selected claim succeeds.
        for turn in range(CHURN_ROUNDS):
            affected = 10 if pattern == "same_key" else (30 if turn % 2 == 0 else 10)
            value = f"late native commit {turn} 雪"
            installed = []

            def install_then_commit(c, claimed, **options):
                assert original_install(c, claimed, **options)
                installed.append((claimed.key, claimed.token))
                assert len(installed) == 1
                lab.write(writer, "update", affected, value)
                return True

            # Only this lab instance is scheduled; inherited source and product
            # functions remain unchanged. The write occurs after install COMMIT.
            with monkeypatch.context() as schedule:
                schedule.setattr(lab, "install", install_then_commit)
                lab.drain(scanner)
            expected[affected] = value
            assert len(installed) == 1
            current = committed_observation(lab, scanner)
            assert current["inventory"] == baseline["inventory"]
            assert len(current["dirty"]) == 1
            operation, key, token = current["dirty"][0]
            assert (operation, key) == (lab.operation, affected)
            assert token != installed[0][1]
            assert current["source"] == current["native"] == sorted(expected.items())
            assert current["decoded"] != current["native"]
            with pytest.raises(AssertionError):
                assert_full_current(current, sorted(expected.items()))

        # No fourth writer is scheduled. One final pass must retire the one
        # remaining obligation and match all current values independently.
        lab.drain(scanner)
        final = committed_observation(lab, scanner)
        assert_full_current(final, sorted(expected.items()))
        assert [row for row in final["frames"] if row[0] == 50] == [
            row for row in baseline["frames"] if row[0] == 50]
        lab.oracle(scanner)

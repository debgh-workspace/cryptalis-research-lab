"""Twelve fixed D4 cases; coordinator DB execution only, no server failure."""
import signal

import pytest

from cryptalis.crypto.cf1 import seal_text

from _online_cf1_lab import CF1EnumerationLab, LOW, TENANT, opened_cf1_lab
from _online_cf1_process_lab import kill_owned_worker
from test_online_cf1_handoff import mutate


CASES = ("initial_inventory", "update", "delete", "delete_reinsert", "to_null", "from_null")
BARRIERS = ("before_commit", "after_commit")


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("barrier", BARRIERS)
def test_owned_worker_death_at_acknowledged_commit_boundary(case, barrier):
    with opened_cf1_lab() as lab:
        with lab.connect() as scanner:
            if case == "initial_inventory":
                assert lab.page(scanner) == (LOW, -42)
            else:
                lab.finish(scanner)
                # The writer uses its own connection inside this one supervised
                # test; both writer and scanner are closed before child start.
                with lab.connect() as writer:
                    mutate(lab, writer, case)
            key = -42 if case == "from_null" else LOW
            claimed = lab.claim(scanner, key)
            assert claimed is not None
            before = lab.snapshot(scanner)
        assert scanner.closed

        # The existing DevelopmentKeyProvider and PreparedKeys are process-bound.
        # Keep them in the surviving supervisor; never alter their PID checks or
        # transfer their objects/material to the child. This tests commit-work
        # process loss, not crypto-provider reconstruction after its owner's death.
        keys = lab.crypto.ring.prepare(minimum_validity=min(1, lab.crypto.ring.max_age / 2))
        frame = seal_text(claimed.value, lab.crypto.field, TENANT, key, keys) if claimed.live else None
        killed = kill_owned_worker(lab, claimed, frame, barrier=barrier)
        assert killed.exitcode == -signal.SIGKILL
        assert killed.acknowledgements == (BARRIERS if barrier == "after_commit" else ("before_commit",))

        # Reconnect only after the owned worker is reaped. Lock acquisition makes
        # the before-COMMIT check wait for PostgreSQL's disconnected-tx cleanup.
        with lab.connect() as inspector, inspector.transaction():
            pending = inspector.execute("SELECT token FROM dirty WHERE operation=%s AND id=%s FOR UPDATE",
                                        (lab.operation, key)).fetchone()
            observed = lab.snapshot(inspector)
            if barrier == "before_commit":
                assert pending == (claimed.token,)
                assert observed == before
            else:
                assert pending is None
                assert observed[:4] == before[:4]  # source/native/pin/cursor
                assert observed[4] == [row for row in before[4] if row[1] != key]
                expected_stage = sorted([row for row in before[5] if row[1] != key] +
                                        [(lab.operation, key, frame, claimed.live, claimed.token)],
                                        key=lambda row: row[1])
                assert observed[5] == expected_stage

        resumed = CF1EnumerationLab.reconstruct(lab.schema, lab.operation, lab.crypto)
        assert resumed.crypto.ring is not lab.crypto.ring
        assert resumed.crypto.provider is lab.crypto.provider
        with resumed.connect() as scanner:
            before_retry = resumed.snapshot(scanner)
            installed = resumed.install(scanner, claimed)
            assert installed is (barrier == "before_commit")
            if barrier == "after_commit":
                assert resumed.snapshot(scanner) == before_retry
            # Complete remaining pages and dirty work, with stopped scheduled
            # writers. D3's separate read-only observer decodes every live frame
            # through unchanged D2 and compares full source/native membership.
            resumed.finish(scanner)
            if barrier == "after_commit":
                assert scanner.execute("SELECT frame,live,token FROM staged WHERE operation=%s AND id=%s",
                                       (lab.operation, key)).fetchone() == (frame, claimed.live, claimed.token)

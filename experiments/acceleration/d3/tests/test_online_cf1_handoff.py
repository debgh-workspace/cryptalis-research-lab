"""Finite PG16 CF1 capture/copy evidence; no online product admission.

The coordinator alone runs this selection through the unchanged dual-role
wrapper. D1's passing controls and D2's four publication files stay unchanged.
"""
import pytest

from cryptalis.crypto import KeyUnavailable
from cryptalis.crypto.cf1 import seal_text

from _online_cf1_lab import (
    CF1EnumerationLab, FixturePinMismatch, HIGH, LOW, TENANT, opened_cf1_lab, oracle,
)


MUTATIONS = ("update", "delete", "delete_reinsert", "to_null", "from_null")


def mutate(lab, writer, action):
    key = -42 if action == "from_null" else LOW
    if action == "update":
        lab.write(writer, "update", key, "current 雪😀 e\u0301")
    elif action == "delete":
        lab.write(writer, "delete", key)
    elif action == "delete_reinsert":
        lab.write(writer, "delete", key)
        lab.write(writer, "insert", key, "replacement é")
    elif action == "to_null":
        lab.write(writer, "update", key, None)
    elif action == "from_null":
        lab.write(writer, "update", key, "formerly NULL")
    else:
        raise ValueError("unknown synthetic mutation")


@pytest.mark.parametrize("action", MUTATIONS)
def test_enumerated_cf1_frames_match_captured_current_text(action):
    with opened_cf1_lab() as lab, lab.connect() as scanner, lab.connect() as writer:
        assert scanner.execute("SELECT rev FROM source ORDER BY id").fetchall() == [(0,)] * 4
        assert scanner.execute("SELECT * FROM dirty").fetchall() == []

        def during_page(keys):
            assert keys == (LOW, -42)
            mutate(lab, writer, action)

        assert lab.page(scanner, after_read=during_page) == (LOW, -42)
        lab.finish(scanner)
        raw = scanner.execute("SELECT id,frame,pg_typeof(frame)::text FROM staged WHERE live ORDER BY id").fetchall()
        assert all(kind == "bytea" and (frame is None or frame.startswith(b"CF1\x00\x01\x00")) for _, frame, kind in raw)
        assert scanner.execute("SELECT frame IS NOT NULL FROM staged WHERE id=0").fetchone() == (True,)
        if action == "delete":
            assert scanner.execute("SELECT frame,live FROM staged WHERE id=%s", (LOW,)).fetchone() == (None, False)
        elif action == "to_null":
            assert scanner.execute("SELECT frame,live FROM staged WHERE id=%s", (LOW,)).fetchone() == (None, True)


@pytest.mark.parametrize("action", MUTATIONS)
def test_stale_claim_cannot_install_cf1_after_captured_mutation(action):
    with opened_cf1_lab() as lab, lab.connect() as scanner, lab.connect() as writer:
        lab.page(scanner)
        key = -42 if action == "from_null" else LOW
        stale = lab.claim(scanner, key)
        mutate(lab, writer, action)
        before = lab.snapshot(scanner)
        assert not lab.install(scanner, stale)
        assert lab.snapshot(scanner) == before
        lab.finish(scanner)


@pytest.mark.parametrize("fault", ["before_cursor", "after_cursor"])
def test_failed_cf1_inventory_page_reconstructs_without_reencrypting_prefix(fault):
    with opened_cf1_lab() as lab:
        with lab.connect() as scanner:
            assert lab.page(scanner) == (LOW, -42)
            lab.drain(scanner)
            prefix = scanner.execute("SELECT * FROM staged ORDER BY id").fetchall()
            before = lab.snapshot(scanner)
            with pytest.raises(RuntimeError, match=fault):
                lab.page(scanner, fault=fault)
            assert lab.snapshot(scanner) == before
        resumed = CF1EnumerationLab.reconstruct(lab.schema, lab.operation, lab.crypto)
        assert resumed.crypto.ring is not lab.crypto.ring
        with resumed.connect() as scanner:
            assert scanner.execute("SELECT last_key,complete FROM inventory").fetchone() == (-42, False)
            resumed.finish(scanner)
            assert scanner.execute("SELECT * FROM staged WHERE id<=-42 ORDER BY id").fetchall() == prefix


@pytest.mark.parametrize("fault", ["after_stage", "after_retire"])
def test_frame_and_dirty_retirement_rollback_then_reconstruct(fault):
    with opened_cf1_lab() as lab:
        with lab.connect() as scanner:
            lab.page(scanner)
            claim = lab.claim(scanner, LOW)
            before = lab.snapshot(scanner)
            with pytest.raises(RuntimeError, match="CF1 worker after"):
                lab.install(scanner, claim, fault=fault)
            assert lab.snapshot(scanner) == before
        resumed = CF1EnumerationLab.reconstruct(lab.schema, lab.operation, lab.crypto)
        with resumed.connect() as scanner:
            assert resumed.install(scanner, claim)
            resumed.finish(scanner)


def test_cold_key_failure_preserves_frames_and_pending_work(monkeypatch):
    with opened_cf1_lab() as lab, lab.connect() as scanner:
        lab.page(scanner)
        claim = lab.claim(scanner, LOW)
        resumed = CF1EnumerationLab.reconstruct(lab.schema, lab.operation, lab.crypto)
        before = lab.snapshot(scanner)

        def unavailable(*args):
            raise KeyUnavailable()

        with monkeypatch.context() as patch:
            patch.setattr(resumed.crypto.provider, "unwrap", unavailable)
            with pytest.raises(KeyUnavailable):
                resumed.install(scanner, claim)
        assert lab.snapshot(scanner) == before
        assert resumed.install(scanner, claim)
        resumed.finish(scanner)


@pytest.mark.parametrize("action", ["reconstruct", "install"])
def test_changed_durable_context_pin_refuses_without_progress(action):
    with opened_cf1_lab() as lab, lab.connect() as scanner:
        lab.page(scanner)
        claim = lab.claim(scanner, LOW)
        scanner.execute("UPDATE operation SET crypto_pin='mismatched fixture pin'")
        before = lab.snapshot(scanner)
        with pytest.raises(FixturePinMismatch, match="operation/context pin mismatch"):
            if action == "reconstruct":
                CF1EnumerationLab.reconstruct(lab.schema, lab.operation, lab.crypto)
            else:
                lab.install(scanner, claim)
        assert lab.snapshot(scanner) == before
        scanner.execute("UPDATE operation SET crypto_pin=%s", (lab.expected_pin,))
        lab.finish(scanner)


def test_foreign_operation_claim_cannot_install_a_frame():
    with opened_cf1_lab(((10, "old operation"),)) as old, opened_cf1_lab(((10, "new operation"),)) as new:
        with old.connect() as a, new.connect() as b:
            old.page(a)
            new.page(b)
            stale, current = old.claim(a, 10), new.claim(b, 10)
            assert (stale.key, stale.token) == (current.key, current.token)
            assert stale.operation != current.operation
            before = new.snapshot(b)
            assert not new.install(b, stale)
            assert new.snapshot(b) == before
            new.finish(b)
            old.finish(a)


@pytest.mark.parametrize("corruption", ["stale_valid", "wrong_row", "tag", "missing_null_row", "null_substitution", "extra"])
def test_independent_full_decoder_refuses_bad_or_incomplete_stage(corruption):
    with opened_cf1_lab() as lab, lab.connect() as scanner, lab.connect() as writer:
        lab.finish(scanner)
        original = scanner.execute("SELECT frame FROM staged WHERE id=%s", (LOW,)).fetchone()[0]
        if corruption == "stale_valid":
            lab.write(writer, "update", LOW, "current after initial stage")
            lab.drain(scanner)
            lab.oracle(scanner)
            # The old frame still authenticates for its exact row and context.
            assert lab.crypto.decode(original, LOW) == "lower 雪😀"
            scanner.execute("UPDATE staged SET frame=%s WHERE id=%s", (original, LOW))
        elif corruption == "wrong_row":
            relocated = scanner.execute("SELECT frame FROM staged WHERE id=%s", (HIGH,)).fetchone()[0]
            scanner.execute("UPDATE staged SET frame=%s WHERE id=%s", (relocated, LOW))
        elif corruption == "tag":
            corrupt = original[:-1] + bytes([original[-1] ^ 1])
            scanner.execute("UPDATE staged SET frame=%s WHERE id=%s", (corrupt, LOW))
        elif corruption == "missing_null_row":
            scanner.execute("DELETE FROM staged WHERE id=-42")
        elif corruption == "null_substitution":
            scanner.execute("UPDATE staged SET frame=NULL WHERE id=%s", (LOW,))
        else:
            frame = seal_text("extra current-looking row", lab.crypto.field, TENANT, 7, lab.crypto.ring.prepare())
            scanner.execute("INSERT INTO staged VALUES(%s,7,%s,true,1)", (lab.operation, frame))
        source = scanner.execute("SELECT id,v FROM source ORDER BY id").fetchall()
        failure = oracle.OracleRefused if corruption in ("wrong_row", "tag") else AssertionError
        with pytest.raises(failure):
            lab.oracle(scanner)
        assert scanner.execute("SELECT id,v FROM source ORDER BY id").fetchall() == source
        assert scanner.execute("SELECT id,v FROM native ORDER BY id").fetchall() == source

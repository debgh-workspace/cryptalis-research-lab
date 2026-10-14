"""Bounded B9B negative controls on synthetic, inactive-only preparation.

Root owns execution through the frozen dual-role PostgreSQL wrapper. These tests
never publish generation 2, change product code, or treat a refusal as success
without checking its exact code and unchanged persistent state. The profile
fixture independently authenticates current generation-1 values before binding.
"""
from dataclasses import replace
from types import SimpleNamespace
from uuid import UUID

import psycopg
import pytest
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

from cryptalis.crypto import Keyring
from test_migration import TENANT, PROVIDER, PublicFixtureProvider, keys, frames
from test_retained_profile_safety_oracles import native_buffer
import test_payload_rotation_journal as b9
import test_payload_rotation_profiles as profiles


BIGINT = ('bigint-equality', 'bigint-storage')
STORAGE = ('uuid-storage', 'bigint-storage')


def save_state(f, state):
    with f.app.owner.begin() as connection:
        connection.exec_driver_sql(
            f'UPDATE "{f.app.schema}"._cryptalis_journal SET state=%s::jsonb WHERE operation_id=%s',
            (b9.canonical(state).decode(), f.artifact.operation_id))


def refused_unchanged(f, code, operation):
    before = b9.native_snapshot(f)
    source = b9.source_snapshot(f)
    with pytest.raises(b9.feature().PreparationFailure) as error:
        operation()
    assert error.value.code == code
    assert b9.native_snapshot(f) == before
    assert b9.source_snapshot(f) == source
    assert f.app.pin.phase == 'ACTIVE'


# Each input is a separate executable cell, rather than a loop whose first
# refusal could hide unexercised later inputs. Values are PUBLIC test data.
BAD_BIGINT = (
    pytest.param('cursor', '', id='empty-cursor'),
    pytest.param('cursor', '+1', id='plus-cursor'),
    pytest.param('cursor', '-0100', id='leading-zero-cursor'),
    pytest.param('cursor', '-0', id='negative-zero-cursor'),
    pytest.param('cursor', ' -100', id='space-cursor'),
    pytest.param('cursor', '1.0', id='fraction-cursor'),
    pytest.param('cursor', True, id='bool-cursor'),
    pytest.param('cursor', str(2**63), id='above-int64-cursor'),
    pytest.param('cursor', str(-(2**63)-1), id='below-int64-cursor'),
    pytest.param('cursor', str(UUID(int=1)), id='uuid-cursor'),
    pytest.param('member', False, id='bool-member'),
    pytest.param('member', -(2**63), id='native-int-member'),
    pytest.param('member', str(2**63), id='above-int64-member'),
)


@pytest.mark.parametrize('profile', BIGINT)
@pytest.mark.parametrize('location,value', BAD_BIGINT)
def test_bigint_receipt_noncanonical_identity_refuses(profile, location, value, monkeypatch):
    with profiles.profile_fixture(profile) as f:
        b9.enter(f, 'start'); b9.enter(f)
        pristine = b9.state(f)
        assert pristine['batches'][0]['cursor_after'] == '-100'
        current = b9.state(f)
        if location == 'cursor':
            current['batches'][0]['cursor_after'] = value
        else:
            current['batches'][0]['rows'][0]['record_id'] = value
        save_state(f, current)
        calls = b9.count_seals(monkeypatch)
        refused_unchanged(f, 'prefix_inconsistent', lambda: b9.enter(f))
        assert calls == []
        # Restoring the exact saved receipt admits read-only inspection, proving
        # that refusal did not come from a generally unusable profile fixture.
        save_state(f, pristine)
        assert b9.enter(f, 'inspect').status == 'PREPARING'
        assert calls == []


@pytest.mark.parametrize('value', [pytest.param(1, id='native-int'),
                                   pytest.param(True, id='bool'),
                                   pytest.param('1', id='decimal-text')])
def test_uuid_receipt_native_type_mismatch_refuses(value, monkeypatch):
    with profiles.profile_fixture('uuid-storage') as f:
        b9.enter(f, 'start'); b9.enter(f)
        current = b9.state(f)
        current['batches'][0]['cursor_after'] = value
        save_state(f, current)
        calls = b9.count_seals(monkeypatch)
        refused_unchanged(f, 'prefix_inconsistent', lambda: b9.enter(f))
        assert calls == []


@pytest.mark.parametrize('profile', profiles.PROFILES)
def test_stage_opposite_native_identity_refuses(profile, monkeypatch):
    with profiles.profile_fixture(profile) as f:
        wrong_type = 'uuid' if profile.startswith('bigint-') else 'bigint'
        assert b9.staged(f) == []
        with f.app.owner.begin() as connection:
            connection.exec_driver_sql(
                f'ALTER TABLE {f.stage} ALTER COLUMN record_id TYPE {wrong_type} USING NULL::{wrong_type}')
        calls = b9.count_seals(monkeypatch)
        # Fresh bind excludes a stale artifact/catalog digest as the reason.
        refused_unchanged(f, 'unsafe_metadata_layout', lambda: b9.bind_artifact(f))
        assert calls == []


@pytest.mark.parametrize('profile', STORAGE)
@pytest.mark.parametrize('case', ['exact-fit', 'one-byte-short'])
def test_storage_exact_byte_boundary_precedes_transport(profile, case, monkeypatch):
    with profiles.profile_fixture(profile) as f:
        first = f.current[0][0]
        with f.factory(tenant_id=TENANT) as session:
            session.get(f.app.Customer, first).name = 'storage-budget-' + 'x' * 256
            session.commit()
        current = tuple(frames(f.app, True).items())
        identity_bytes = 24 if profile.startswith('bigint-') else 32
        # Independent wire recipe: 14-byte header + 12-byte nonce + 16-byte
        # tag; plaintext length is frame length minus 42 for storage only.
        body = current[0][1]
        assert body[:6] == bytes.fromhex('434631000100')
        assert body[10:14] == b'\0' * 4
        cost = identity_bytes + len(body) + (len(body) - 42) + len(body)
        f.max_bytes = cost - (case == 'one-byte-short')
        samples = []
        def capture(connection, cursor, statement, parameters, context, many):
            if cursor.description is not None:
                samples.append(native_buffer(cursor))
        calls = b9.count_seals(monkeypatch)
        before, source = b9.native_snapshot(f), b9.source_snapshot(f)
        event.listen(f.app.owner, 'after_cursor_execute', capture)
        try:
            if case == 'one-byte-short':
                with pytest.raises(b9.feature().PreparationFailure) as error:
                    b9.bind_artifact(f)
                assert error.value.code == 'row_exceeds_chunk_byte_limit'
                observed = list(samples)
                assert observed and calls == []
                assert not any(value is not None and (body in value or body.hex().encode() in value)
                    for _, rows in observed for row in rows for value in row)
            else:
                f.artifact = b9.bind_artifact(f)
                assert b9.enter(f, 'start').status == 'PREPARING'
                assert b9.enter(f).status == 'PREPARING'
                rows, receipt = b9.staged(f), b9.state(f)['batches'][0]
                assert len(rows) == 1 and rows[0][0] == first
                assert receipt['logical_bytes'] == cost
                assert calls == [first]
        finally:
            event.remove(f.app.owner, 'after_cursor_execute', capture)
        assert b9.source_snapshot(f) == source
        if case == 'one-byte-short':
            assert b9.native_snapshot(f) == before


@pytest.mark.parametrize('profile', STORAGE)
def test_storage_search_header_native_constraint_refuses(profile, monkeypatch):
    with profiles.profile_fixture(profile) as f:
        record, old = f.current[0]
        altered = bytearray(old)
        altered[10:14] = (1).to_bytes(4, 'big')
        column = f.app.plan.document['lock']['models'][0]['fields'][0]['payload_column']
        before, source = b9.native_snapshot(f), b9.source_snapshot(f)
        calls = b9.count_seals(monkeypatch)
        # Storage frames require a zero search-generation field. The existing
        # native CHECK is the earliest guard; do not disable it to reach bind.
        # Catch outside begin() so the failed statement is rolled back first.
        with pytest.raises(IntegrityError) as error:
            with f.app.owner.begin() as connection:
                connection.exec_driver_sql(
                    f'UPDATE "{f.app.schema}".customer SET "{column}"=%s WHERE id=%s',
                    (bytes(altered), record))
        native = error.value.orig
        assert isinstance(native, psycopg.errors.CheckViolation)
        assert native.sqlstate == '23514'
        assert native.diag.constraint_name == column + '_frame'
        assert native.diag.schema_name == f.app.schema
        assert native.diag.table_name == 'customer'
        assert calls == []
        assert b9.native_snapshot(f) == before
        assert b9.source_snapshot(f) == source == f.baseline
        assert f.app.pin.phase == 'ACTIVE' and b9.staged(f) == []


@pytest.mark.parametrize('profile', STORAGE)
def test_storage_payload_header_experiment_refuses(profile, monkeypatch):
    with profiles.profile_fixture(profile) as f:
        record, old = f.current[0]
        altered = bytearray(old)
        altered[6:10] = (2).to_bytes(4, 'big')
        column = f.app.plan.document['lock']['models'][0]['fields'][0]['payload_column']
        # A nonzero payload generation passes the native framing constraint.
        # The experiment must independently reject generation 2 as a source.
        with f.app.owner.begin() as connection:
            connection.exec_driver_sql(
                f'UPDATE "{f.app.schema}".customer SET "{column}"=%s WHERE id=%s',
                (bytes(altered), record))
        assert frames(f.app, True)[record] == bytes(altered)
        calls = b9.count_seals(monkeypatch)
        # Rebind validates the header directly; resume would reject the changed
        # source commitment before reaching generation authentication.
        refused_unchanged(f, 'source_generation_changed', lambda: b9.bind_artifact(f))
        assert calls == [] and b9.staged(f) == []


@pytest.mark.parametrize('profile', profiles.PROFILES)
@pytest.mark.parametrize('authority', ['pin', 'target-policy', 'maintenance'])
def test_profile_independent_external_authority_refuses(profile, authority, monkeypatch):
    with profiles.profile_fixture(profile) as f:
        b9.enter(f, 'start'); b9.enter(f)
        changes = {
            'pin': {'current_pin': replace(f.app.pin, plan_digest='0' * 64)},
            'target-policy': {'target_keys': keys(TENANT)},
            'maintenance': {'maintenance': replace(f.app.approval,
                writer_exclusion='different PUBLIC synthetic maintenance approval')},
        }
        calls = b9.count_seals(monkeypatch)
        refused_unchanged(f, 'source_authority_changed',
                          lambda: b9.enter(f, **changes[authority]))
        assert calls == []
        assert b9.enter(f, 'inspect').status == 'PREPARING'


@pytest.mark.parametrize('profile', profiles.PROFILES)
@pytest.mark.parametrize('which', ['source', 'target'])
def test_profile_independent_lease_expiry_rolls_back(profile, which, monkeypatch):
    import cryptalis.crypto.keys as key_module
    with profiles.profile_fixture(profile) as f:
        b9.enter(f, 'start'); b9.enter(f)
        now = [100.0]
        monkeypatch.setattr(key_module, 'time', SimpleNamespace(
            monotonic=lambda: now[0], monotonic_ns=lambda: int(now[0] * 1e9)))
        source = Keyring(keys(TENANT).policy, {PROVIDER: PublicFixtureProvider()},
                         max_age=10 if which == 'source' else 60)
        target = b9.target_keys(TENANT, max_age=10 if which == 'target' else 60)
        observed = []
        def expire(point, **context):
            if point == 'after_dml' and context['ordinal'] == 2:
                connection = context['connection']
                assert connection.exec_driver_sql(f'SELECT count(*) FROM {f.stage}').scalar_one() == 4
                observed.append(point)
                now[0] = 111.0
        refused_unchanged(f, 'binding_expired', lambda: b9.enter(
            f, source_keys=source, target_keys=target, observer=expire))
        assert observed == ['after_dml']
        f.source, f.target = keys(TENANT), b9.target_keys(TENANT)
        profiles.finish(f)
        profiles.assert_profile_parity(f)

"""Trusted-local diagnostic round trips; no database or cleanup-branch proof.

Only locally constructed synthetic exceptions enter pickle.loads. These tests
do not admit untrusted pickle, a public IPC API, or cross-version compatibility.
"""

import pickle
import traceback

import pytest

from cryptalis.crypto.development_file import FileCustodyUnavailable
from cryptalis.crypto.keys import (
    CryptoBackendUnavailable,
    CryptoFailure,
    KeyUnavailable,
)
from cryptalis.sqlalchemy import ProtectedSchemaMismatch


def _round_trip(error):
    payload = pickle.dumps(error, protocol=5)
    return payload, pickle.loads(payload)


def _assert_identity(restored, original, expected_code):
    assert type(restored) is type(original)
    assert restored is not original
    assert restored.code == expected_code
    assert restored.operation_id == original.operation_id
    assert restored.args == original.args
    assert restored.stage == original.stage
    assert restored.remedy == original.remedy
    assert restored.__cause__ is None
    assert restored.__context__ is None
    assert restored.__traceback__ is None


def _rendered(error):
    return "\n".join((
        str(error), repr(error), repr(vars(error)),
        "".join(traceback.format_exception(error)),
    ))


def test_fresh_key_failure_retains_safe_identity_and_class_defaults():
    original = KeyUnavailable()
    _, restored = _round_trip(original)
    _assert_identity(restored, original, "KeyUnavailable")
    assert restored.stage == "key preparation or use"
    assert restored.remedy == (
        "Check the exact provider, wrapped roots and generation policy; "
        "prepare fresh keys in this process."
    )
    assert restored.effects == "none"
    assert restored.retryable is True


@pytest.mark.parametrize("error_type, expected_code", [
    pytest.param(KeyUnavailable, "KeyUnavailable", id="key"),
    pytest.param(CryptoBackendUnavailable, "CryptoBackendUnavailable", id="backend"),
    pytest.param(CryptoFailure, "CryptoFailure", id="base"),
])
def test_cleanup_downgrade_survives_trusted_local_round_trip(error_type, expected_code):
    original = error_type()
    original.effects = "unknown"
    original.retryable = False
    _, restored = _round_trip(original)
    _assert_identity(restored, original, expected_code)
    # Literal expectations independently detect either lost downgrade field.
    assert type(restored.effects) is str
    assert restored.effects == "unknown"
    assert restored.retryable is False


@pytest.mark.parametrize("error_type, expected_code, expected_effects", [
    pytest.param(
        ProtectedSchemaMismatch, "ProtectedSchemaMismatch",
        "transaction_requires_rollback", id="schema",
    ),
    pytest.param(
        FileCustodyUnavailable, "FileCustodyUnavailable",
        "A private file may exist after failed creation; inspect before retry.",
        id="custody",
    ),
])
def test_existing_class_effects_remain_intact(error_type, expected_code, expected_effects):
    original = error_type()
    assert original.effects == expected_effects
    _, restored = _round_trip(original)
    _assert_identity(restored, original, expected_code)
    assert restored.effects == expected_effects
    assert restored.retryable is False


@pytest.mark.parametrize("attachment", ["notes", "cause", "context", "provider_data"])
def test_private_attachments_do_not_cross_the_round_trip(attachment):
    marker = "SYNTHETIC_PRIVATE_TRANSPORT_" + attachment.upper()
    marker_bytes = marker.encode("ascii")
    # Positive controls establish sensitivity of the byte and rendering checks.
    assert marker_bytes in pickle.dumps(marker, protocol=5)
    control = KeyUnavailable()
    control.add_note(marker)
    assert marker in _rendered(control)

    original = KeyUnavailable()
    original.effects = "unknown"
    original.retryable = False
    if attachment == "notes":
        original.add_note(marker)
    elif attachment == "cause":
        original.__cause__ = RuntimeError(marker)
    elif attachment == "context":
        original.__context__ = RuntimeError(marker)
    else:
        original.provider_data = marker
    assert marker in _rendered(original)

    payload, restored = _round_trip(original)
    _assert_identity(restored, original, "KeyUnavailable")
    assert marker_bytes not in payload
    assert marker not in _rendered(restored)
    assert not hasattr(restored, "__notes__")
    assert not hasattr(restored, "provider_data")
    assert restored.effects == "unknown"
    assert restored.retryable is False


class _DoNotInspect:
    def __reduce__(self):
        raise AssertionError("unrelated state must not be serialized")

    def __eq__(self, other):
        raise AssertionError("nonprimitive metadata must not be compared")

    def __bool__(self):
        raise AssertionError("nonprimitive metadata must not be coerced")

    def __str__(self):
        raise AssertionError("nonprimitive metadata must not be rendered")

    def __repr__(self):
        raise AssertionError("nonprimitive metadata must not be rendered")


def test_unrelated_state_is_not_reduced_when_cleanup_metadata_is_retained():
    original = KeyUnavailable()
    original.effects = "unknown"
    original.retryable = False
    original.provider_data = _DoNotInspect()
    _, restored = _round_trip(original)
    _assert_identity(restored, original, "KeyUnavailable")
    assert not hasattr(restored, "provider_data")
    assert restored.effects == "unknown"
    assert restored.retryable is False


class _UnknownText(str):
    def __eq__(self, other):
        raise AssertionError("string subclasses are outside the whitelist")

    def __reduce__(self):
        raise AssertionError("string subclasses must not be serialized")


@pytest.mark.parametrize("effects, retryable", [
    pytest.param("unknown", True, id="retryable-true"),
    pytest.param("unknown", 0, id="integer-zero"),
    pytest.param("none", False, id="different-effect"),
    pytest.param(_UnknownText("unknown"), False, id="string-subclass"),
    pytest.param(_DoNotInspect(), False, id="opaque-effect"),
    pytest.param("unknown", _DoNotInspect(), id="opaque-retry"),
])
def test_only_exact_cleanup_pair_is_transported(effects, retryable):
    original = KeyUnavailable()
    original.effects = effects
    original.retryable = retryable
    _, restored = _round_trip(original)
    _assert_identity(restored, original, "KeyUnavailable")
    # Unadmitted host mutations retain the existing class-default behavior.
    # This is not a promise to preserve arbitrary host-owned classifications.
    assert restored.effects == "none"
    assert restored.retryable is True

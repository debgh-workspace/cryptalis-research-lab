"""C10 pure framing, independent CF1, and original failure-boundary oracles.

Only public fixture roots are used. No engine, connection, credential read,
provider service, timing comparison, or PostgreSQL admission is performed.
"""

import ast
import asyncio
import builtins
from dataclasses import replace
import hashlib
import hmac as std_hmac
import io
import json
from pathlib import Path
import random
import struct
import sys
from types import SimpleNamespace
from uuid import UUID

import pytest

from cryptalis.crypto import cf1, keys as keymod


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "experiments/c10_baseline_cf1.py"
VECTORS = json.loads((ROOT / "tests/fixtures/cf1_vectors.json").read_text())["vectors"]
PACKED = [v for v in VECTORS if v["search_generation"]]
BASE_SOURCE = BASELINE.read_text()
BASE_NODE = next(n for n in ast.parse(BASE_SOURCE).body
                 if isinstance(n, ast.FunctionDef) and n.name == "_term")
BASE_CODE = compile(ast.get_source_segment(BASE_SOURCE, BASE_NODE), str(BASELINE), "exec")
PUBLIC_PROVIDER = UUID(int=10102026)


def original_term():
    space = dict(vars(cf1))
    exec(BASE_CODE, space)
    return space["_term"]


def wire(*parts):
    """Independent struct/stream writer; never calls a product encoder."""
    output = io.BytesIO()
    output.write(struct.pack("!I", len(parts)))
    for part in parts:
        output.write(struct.pack("!I", len(part)))
        output.write(part)
    return output.getvalue()


def independent_term(encoded, field_bytes, context, root):
    salt = hashlib.sha256(wire(b"CF1/root", context.domain_id.bytes,
        context.tenant_id.bytes, context.root_id.bytes,
        context.generation.to_bytes(4, "big"))).digest()
    info = wire(b"CF1/search-key", field_bytes, b"utf8-exact/v1", b"identity/v1", b"equality")
    # RFC 5869 extract plus one expand block, sufficient for SHA-256 / 32 bytes.
    prk = std_hmac.digest(salt, root, "sha256")
    key = std_hmac.digest(prk, info + b"\x01", "sha256")
    return std_hmac.digest(key, wire(b"equality", encoded), "sha256")


def prepared(vector):
    field = cf1.FieldDescriptor.from_compiled(vector["descriptor"], vector["descriptor_digest"])
    tenant = UUID(vector["tenant_id"])
    purposes = ("payload", "search") if field.equality else ("payload",)
    contexts = {p: keymod.KeyContext(field.domain_id, tenant, p,
        UUID(vector[p + "_root_id"]), vector[p + "_generation"]) for p in purposes}
    roots = {p: bytes.fromhex(vector[p + "_root"]) for p in purposes}

    class PublicFixtureProvider:
        provider_id = PUBLIC_PROVIDER

        def unwrap(self, wrapper, context):
            return roots[context.purpose]

    wrappers = tuple(keymod.WrappedRoot(PUBLIC_PROVIDER, c, b"PUBLIC C10 FIXTURE")
                     for c in contexts.values())
    policy = keymod.KeyPolicy(field.domain_id, tenant, wrappers,
        vector["payload_generation"], vector["search_generation"] or None)
    keys = keymod.Keyring(policy, {PUBLIC_PROVIDER: PublicFixtureProvider()}).prepare()
    return field, tenant, keys


@pytest.mark.parametrize("vector", VECTORS, ids=lambda v: v["name"])
def test_frozen_independent_cf1_frame_and_query_equivalence(vector, monkeypatch):
    field, tenant, keys = prepared(vector)
    record = UUID(vector["record_id"]) if field.record_codec == "uuid16/v1" else vector["record_id"]
    frozen = bytes.fromhex(vector["frame"])
    assert cf1.open_text(frozen, field, tenant, record, keys) == vector["text"]
    monkeypatch.setattr(cf1, "os", SimpleNamespace(urandom=lambda n: bytes.fromhex(vector["nonce"])))
    assert cf1.seal_text(vector["text"], field, tenant, record, keys) == frozen
    if field.equality:
        material = keys._resolve(field.domain_id, tenant, "search", vector["search_generation"])
        expected = independent_term(vector["text"].encode("utf8"), field.field_id.bytes,
                                    material.context, material.root)
        assert expected == bytes.fromhex(vector["term"]) == frozen[14:46]
        assert cf1.equality_term(vector["text"], field, tenant, keys) == expected
        assert cf1.equality_term(None, field, tenant, keys) is None


def test_dynamic_wire_operands_match_independent_writer(monkeypatch):
    rng = random.Random(10142026)
    cases = [(b"", b""), (bytes(16), b"\x00\xff"), (b"a", b"bc"), (b"ab", b"c")]
    cases += [(rng.randbytes(rng.randrange(0, 65)), rng.randbytes(rng.randrange(0, 2049)))
              for _ in range(64)]
    cases.append((bytes(range(16)), b"x" * cf1.MAX_TEXT_BYTES))
    seen = []

    def derive(material, info):
        seen.append(("info", info))
        return b"k" * 32

    class Mac:
        def __init__(self, key, algorithm):
            assert key == b"k" * 32

        def update(self, message):
            seen.append(("message", message))

        def finalize(self):
            return b"result"

    monkeypatch.setattr(cf1, "_derive", derive)
    monkeypatch.setattr(cf1, "hmac", SimpleNamespace(HMAC=Mac))
    for field_bytes, encoded in cases:
        field = SimpleNamespace(field_id=SimpleNamespace(bytes=field_bytes))
        assert cf1._term(encoded, field, object()) == b"result"
        assert seen.pop(0) == ("info", wire(b"CF1/search-key", field_bytes,
            b"utf8-exact/v1", b"identity/v1", b"equality"))
        assert seen.pop(0) == ("message", wire(b"equality", encoded))
    assert not seen


class BytesSubclass(bytes):
    pass


INVALID_PARTS = [None, True, 1, "text", bytearray(b"text"), memoryview(b"text"), BytesSubclass(b"text")]


@pytest.mark.parametrize("part", INVALID_PARTS, ids=lambda p: type(p).__name__)
@pytest.mark.parametrize("location", ["field", "encoded"])
def test_strict_dynamic_bytes_keep_original_failure_boundary(part, location, monkeypatch):
    traces = []

    def derive(material, info):
        traces.append("derive")
        return b"k" * 32

    class Mac:
        def __init__(self, *args):
            traces.append("hmac")

        def update(self, message):
            traces.append("update")

        def finalize(self):
            traces.append("finalize")

    monkeypatch.setattr(cf1, "_derive", derive)
    monkeypatch.setattr(cf1, "hmac", SimpleNamespace(HMAC=Mac))
    field = SimpleNamespace(field_id=SimpleNamespace(bytes=part if location == "field" else bytes(16)))
    encoded = part if location == "encoded" else b"value"
    expected = keymod.InvalidContext if location == "field" else keymod.CryptoBackendUnavailable
    for function in (original_term(), cf1._term):
        traces.clear()
        with pytest.raises(expected) as caught:
            function(encoded, field, object())
        assert type(caught.value) is expected
        assert traces == ([] if location == "field" else ["derive", "hmac"])
        assert caught.value.__suppress_context__ is (location == "encoded")


@pytest.mark.parametrize("location", ["field", "encoded"])
@pytest.mark.parametrize("size", [0xFFFFFFFF, 0x100000000])
def test_dynamic_uint32_length_boundary_without_gib_allocation(location, size, monkeypatch):
    """Inject only len(bytes) to reach the real bound check with a tiny operand."""
    dynamic = b"PUBLIC SYNTHETIC LENGTH OPERAND"
    field_bytes = dynamic if location == "field" else bytes(16)
    encoded = dynamic if location == "encoded" else b"value"
    field = SimpleNamespace(field_id=SimpleNamespace(bytes=field_bytes))
    traces = []

    def fake_len(value):
        if value is dynamic:
            traces.append("length")
            return size
        return builtins.len(value)

    def derive(material, info):
        traces.append("derive")
        if location == "field":
            assert info[22:26] == struct.pack("!I", size)
        return b"k" * 32

    class Mac:
        def __init__(self, *args):
            traces.append("hmac")

        def update(self, message):
            traces.append("update")
            if location == "encoded":
                assert message[16:20] == struct.pack("!I", size)

        def finalize(self):
            traces.append("finalize")
            return b"result"

    monkeypatch.setattr(cf1, "len", fake_len, raising=False)
    monkeypatch.setattr(keymod, "len", fake_len, raising=False)
    monkeypatch.setattr(cf1, "_derive", derive)
    monkeypatch.setattr(cf1, "hmac", SimpleNamespace(HMAC=Mac))
    outcomes = []
    for function in (original_term(), cf1._term):
        traces.clear()
        if size == 0xFFFFFFFF:
            assert function(encoded, field, object()) == b"result"
        else:
            expected = keymod.InvalidContext if location == "field" else keymod.CryptoBackendUnavailable
            with pytest.raises(expected) as caught:
                function(encoded, field, object())
            assert type(caught.value) is expected
        outcomes.append(list(traces))
    assert outcomes[0] == outcomes[1]
    assert outcomes[0].count("length") == 1


@pytest.mark.parametrize("failure", [RuntimeError, asyncio.CancelledError, KeyboardInterrupt])
@pytest.mark.parametrize("stage", ["field", "length_field", "derive", "hmac", "length_encoded", "update", "finalize"])
def test_evaluation_order_exception_class_and_suppression(stage, failure, monkeypatch):
    field_bytes, encoded = b"PUBLIC FIELD", b"PUBLIC ENCODED"
    traces = []

    def visit(name):
        traces.append(name)
        if stage == name:
            raise failure("PUBLIC C10 FAILURE")

    class Identity:
        @property
        def bytes(self):
            visit("field")
            return field_bytes

    def fake_len(value):
        if value is field_bytes:
            visit("length_field")
        elif value is encoded:
            visit("length_encoded")
        return builtins.len(value)

    def derive(material, info):
        visit("derive")
        return b"k" * 32

    class Mac:
        def __init__(self, *args):
            visit("hmac")

        def update(self, message):
            visit("update")

        def finalize(self):
            visit("finalize")

    monkeypatch.setattr(cf1, "len", fake_len, raising=False)
    monkeypatch.setattr(keymod, "len", fake_len, raising=False)
    monkeypatch.setattr(cf1, "_derive", derive)
    monkeypatch.setattr(cf1, "hmac", SimpleNamespace(HMAC=Mac))
    outcomes = []
    for function in (original_term(), cf1._term):
        traces.clear()
        expected = keymod.CryptoBackendUnavailable if failure is RuntimeError and stage in {
            "hmac", "length_encoded", "update", "finalize"} else failure
        with pytest.raises(expected) as caught:
            function(encoded, SimpleNamespace(field_id=Identity()), object())
        assert type(caught.value) is expected
        outcomes.append((list(traces), caught.value.__suppress_context__))
    assert outcomes[0] == outcomes[1]
    order = ["field", "length_field", "derive", "hmac", "length_encoded", "update", "finalize"]
    assert outcomes[0][0] == order[:order.index(stage) + 1]
    assert outcomes[0][1] is (expected is keymod.CryptoBackendUnavailable)


def test_derive_callable_is_resolved_before_field_operand(monkeypatch):
    traces = []

    def derive(material, info):
        traces.append("original derive")
        return b"k" * 32

    def changed(*args):
        raise AssertionError("derive lookup moved after operand evaluation")

    for baseline in (True, False):
        traces.clear()
        monkeypatch.setattr(cf1, "_derive", derive)
        function = original_term() if baseline else cf1._term

        class Identity:
            @property
            def bytes(self):
                function.__globals__["_derive"] = changed
                return bytes(16)

        assert len(function(b"value", SimpleNamespace(field_id=Identity()), object())) == 32
        assert traces == ["original derive"]


def test_terms_rederive_for_changed_field_material_and_value():
    field, tenant, keys = prepared(PACKED[0])
    material = keys._resolve(field.domain_id, tenant, "search", PACKED[0]["search_generation"])
    results = []
    for index in range(12):
        current_field = replace(field, field_id=UUID(int=100 + index))
        current_material = replace(material, root=bytes([index]) * 32)
        encoded = ("exact é e\u0301 雪 " + str(index)).encode("utf8")
        result = cf1._term(encoded, current_field, current_material)
        assert result == independent_term(encoded, current_field.field_id.bytes,
                                         current_material.context, current_material.root)
        results.append(result)
    assert len(set(results)) == len(results)


def test_fixed_literal_specialization_preserves_per_use_crypto_counts(monkeypatch):
    field, tenant, keys = prepared(PACKED[0])
    vector = PACKED[0]
    record = UUID(vector["record_id"])
    frame = bytes.fromhex(vector["frame"])
    actual = {name: 0 for name in ("term", "derive", "resolve", "open", "hkdf", "hmac")}
    tuple_labels = []
    original_tuple = cf1.tuple_bytes

    def counted(name, function):
        def wrapper(*args, **kwargs):
            actual[name] += 1
            return function(*args, **kwargs)
        return wrapper

    def observed_tuple(*parts):
        tuple_labels.append(parts[0])
        return original_tuple(*parts)

    for name, attribute in (("term", "_term"), ("derive", "_derive"), ("open", "open_text"), ("hkdf", "HKDF")):
        monkeypatch.setattr(cf1, attribute, counted(name, getattr(cf1, attribute)))
    monkeypatch.setattr(cf1, "hmac", SimpleNamespace(HMAC=counted("hmac", cf1.hmac.HMAC)))
    monkeypatch.setattr(keymod.PreparedKeys, "_resolve", counted("resolve", keymod.PreparedKeys._resolve))
    monkeypatch.setattr(cf1, "tuple_bytes", observed_tuple)
    m, r = 20, 3
    for _ in range(m):
        assert cf1.equality_term(vector["text"], field, tenant, keys) == frame[14:46]
    for _ in range(r):
        assert cf1.open_text(frame, field, tenant, record, keys) == vector["text"]
    assert actual == {"term": m + r, "derive": m + 2*r, "resolve": 2*m + 4*r,
                      "open": r, "hkdf": m + 2*r, "hmac": m + r}
    # The sole intended mechanism delta: remove exactly two generic encodings
    # per term. Root, payload-key, and AAD framing stay on the generic encoder.
    assert tuple_labels.count(b"CF1/search-key") == 0
    assert tuple_labels.count(b"equality") == 0
    assert tuple_labels.count(b"CF1/root") == m + 2*r
    assert tuple_labels.count(b"CF1/payload-key") == r
    assert tuple_labels.count(b"CF1/payload") == r
    assert len(tuple_labels) == m + 4*r


@pytest.mark.parametrize("fault", ["expiry", "pid"])
@pytest.mark.parametrize("operation", ["query", "open"])
def test_final_per_use_checks_still_refuse_mid_crypto_expiry_or_fork(fault, operation, monkeypatch):
    now = [100.0]
    monkeypatch.setattr(keymod, "time", SimpleNamespace(
        monotonic=lambda: now[0], monotonic_ns=lambda: int(now[0] * 1_000_000_000)))
    vector = PACKED[0]
    field, tenant, keys = prepared(vector)
    real_hmac = cf1.hmac.HMAC

    class Mac:
        def __init__(self, *args, **kwargs):
            self.native = real_hmac(*args, **kwargs)

        def update(self, message):
            self.native.update(message)

        def finalize(self):
            result = self.native.finalize()
            if fault == "expiry":
                now[0] = 161.0
            else:
                monkeypatch.setattr(keymod, "os", SimpleNamespace(getpid=lambda: keys._pid + 1))
            return result

    monkeypatch.setattr(cf1, "hmac", SimpleNamespace(HMAC=Mac))
    with pytest.raises(keymod.KeyUnavailable):
        if operation == "query":
            cf1.equality_term(vector["text"], field, tenant, keys)
        else:
            cf1.open_text(bytes.fromhex(vector["frame"]), field, tenant, UUID(vector["record_id"]), keys)

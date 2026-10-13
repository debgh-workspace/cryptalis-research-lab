"""Test-only CF1 decoder for PUBLIC FIXTURE ROOTS, never runtime cryptography.

Framing, signed identity encoding, HKDF and HMAC are independent of Cryptalis.
Only the existing library AES-GCM-SIV primitive is shared. Expected descriptor,
tenant and root pins come from the test oracle, never from frame-selected keys.
SQL NULL is represented normally; authentication does not prove its presence.
"""
from dataclasses import dataclass
import hashlib
import hmac
import io
import json
import struct
from uuid import UUID

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV


MAX_TEXT_BYTES = 16 * 1024 * 1024
_MEMBERS = {
    "schema", "domain_id", "table_id", "field_id", "text_codec", "normalizer",
    "null_policy", "record_codec", "tenant_codec", "representation",
}


class OracleRefused(ValueError):
    """Static diagnostic for an invalid public fixture or unauthenticated frame."""


@dataclass(frozen=True)
class PublicFixtureRoot:
    root_id: UUID
    generation: int
    root: bytes


def _tuple(*parts):
    output = io.BytesIO()
    output.write(struct.pack("!I", len(parts)))
    for part in parts:
        if type(part) is not bytes:
            raise OracleRefused("tuple_part")
        output.write(struct.pack("!I", len(part)))
        output.write(part)
    return output.getvalue()


def record_bytes(codec, record):
    """Typed identity bytes; bool and implicit string/integer coercion refuse."""
    if codec == "uuid16/v1" and type(record) is UUID:
        return record.bytes
    if codec == "int64-be/v1" and type(record) is int and -(1 << 63) <= record < (1 << 63):
        return _tuple(b"int64", struct.pack("!q", record))
    raise OracleRefused("record_context")


def _root(pin):
    if (type(pin) is not PublicFixtureRoot or type(pin.root_id) is not UUID or pin.root_id.int == 0
            or type(pin.generation) is not int or not 1 <= pin.generation < (1 << 32)
            or type(pin.root) is not bytes or len(pin.root) != 32):
        raise OracleRefused("root_pin")


def _derive(pin, domain, tenant, info):
    salt = hashlib.sha256(_tuple(b"CF1/root", domain.bytes, tenant.bytes,
                                pin.root_id.bytes, struct.pack("!I", pin.generation))).digest()
    extracted = hmac.digest(salt, pin.root, "sha256")
    return hmac.digest(extracted, info + b"\x01", "sha256")


def decode_cf1(frame, *, descriptor, descriptor_digest, tenant, record, payload, search=None):
    """Decode using an exact externally supplied public-fixture context and pins."""
    if type(descriptor) is not dict or set(descriptor) != _MEMBERS:
        raise OracleRefused("descriptor_members")
    if any(type(value) is not str or len(value) > 128 for value in descriptor.values()):
        raise OracleRefused("descriptor_value")
    if (descriptor["schema"], descriptor["text_codec"], descriptor["normalizer"], descriptor["null_policy"]) != (
            "cryptalis.context/v1", "utf8-exact/v1", "identity/v1", "sql-null/v1"):
        raise OracleRefused("descriptor_profile")
    try:
        domain, table, field = (UUID(descriptor[key]) for key in ("domain_id", "table_id", "field_id"))
    except (ValueError, AttributeError):
        raise OracleRefused("descriptor_identity") from None
    if any(uid.int == 0 or str(uid) != descriptor[key]
           for key, uid in (("domain_id", domain), ("table_id", table), ("field_id", field))):
        raise OracleRefused("descriptor_identity")
    canonical = json.dumps(descriptor, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"), allow_nan=False).encode("utf8")
    digest = hashlib.sha256(canonical).digest()
    if type(descriptor_digest) is not str or not hmac.compare_digest(digest.hex(), descriptor_digest):
        raise OracleRefused("descriptor_digest")
    if type(tenant) is not UUID or descriptor["tenant_codec"] not in ("uuid16/v1", "single-tenant-uuid/v1"):
        raise OracleRefused("tenant_context")
    if descriptor["tenant_codec"] == "single-tenant-uuid/v1" and tenant != table:
        raise OracleRefused("tenant_context")
    typed_record = record_bytes(descriptor["record_codec"], record)
    if descriptor["representation"] not in ("cf1-storage/v1", "cf1-packed-equality/v1"):
        raise OracleRefused("representation")
    equality = descriptor["representation"] == "cf1-packed-equality/v1"
    _root(payload)
    if equality:
        _root(search)
        if payload.root_id == search.root_id or hmac.compare_digest(payload.root, search.root):
            raise OracleRefused("independent_roots")
    elif search is not None:
        raise OracleRefused("unexpected_search_pin")
    if frame is None:
        return None
    header_size = 46 if equality else 14
    if type(frame) is not bytes or not header_size + 28 <= len(frame) <= header_size + 28 + MAX_TEXT_BYTES:
        raise OracleRefused("frame_size")
    if frame[:6] != b"CF1\x00\x01" + bytes([int(equality)]):
        raise OracleRefused("frame_profile")
    if struct.unpack("!II", frame[6:14]) != (payload.generation, search.generation if equality else 0):
        raise OracleRefused("generation_pin")
    header = frame[:header_size]
    aad = _tuple(b"CF1/payload", domain.bytes, tenant.bytes, field.bytes, typed_record, digest, header)
    key = _derive(payload, domain, tenant, _tuple(b"CF1/payload-key", field.bytes, typed_record))
    try:
        encoded = AESGCMSIV(key).decrypt(frame[header_size:header_size + 12], frame[header_size + 12:], aad)
    except InvalidTag:
        raise OracleRefused("authentication") from None
    if equality:
        key = _derive(search, domain, tenant, _tuple(b"CF1/search-key", field.bytes,
                      b"utf8-exact/v1", b"identity/v1", b"equality"))
        expected = hmac.digest(key, _tuple(b"equality", encoded), "sha256")
        if not hmac.compare_digest(header[14:46], expected):
            raise OracleRefused("equality_term")
    try:
        value = encoded.decode("utf8", errors="strict")
    except UnicodeDecodeError:
        raise OracleRefused("text_encoding") from None
    if "\x00" in value:
        raise OracleRefused("text_encoding")
    return value

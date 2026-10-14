"""SOURCE-ONLY T research wrapper. No monkeypatch of product modules.
Pre-import origin/hash verification is a future launcher's responsibility.
Only tuple assembly differs; Python crypto expressions and try regions are copied.
"""
from uuid import UUID
from cryptalis.crypto.cf1 import (
    hashlib, compare_digest, InvalidTag, hashes, hmac, AESGCMSIV, HKDF,
    AuthenticationFailed, CryptoBackendUnavailable, InvalidContext, InvalidFrame,
    InvalidText, KeyUnavailable, PreparedKeys, RepresentationMismatch,
    FieldDescriptor, MAX_TEXT_BYTES, _MAGIC, _context,
)
from native_tuple import tuple_bytes as _native_tuple_bytes


def tuple_bytes(*parts):
    try:
        return _native_tuple_bytes(*parts)
    except ValueError:
        raise InvalidContext() from None


def _derive(material, info):
    c = material.context
    salt = hashlib.sha256(tuple_bytes(b"CF1/root", c.domain_id.bytes, c.tenant_id.bytes,
                                     c.root_id.bytes, c.generation.to_bytes(4, "big"))).digest()
    try:
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info).derive(material.root)
    except Exception:
        raise CryptoBackendUnavailable() from None


def _term(encoded, field, material):
    key = _derive(material, tuple_bytes(b"CF1/search-key", field.field_id.bytes,
                                       b"utf8-exact/v1", b"identity/v1", b"equality"))
    try:
        mac = hmac.HMAC(key, hashes.SHA256())
        mac.update(tuple_bytes(b"equality", encoded))
        return mac.finalize()
    except Exception:
        raise CryptoBackendUnavailable() from None


def _aad(field, tenant, record, header):
    return tuple_bytes(b"CF1/payload", field.domain_id.bytes, tenant.bytes, field.field_id.bytes,
                       record, field.digest, header)


def open_text(frame: bytes | None, field: FieldDescriptor, tenant: UUID,
              record: UUID | int, keys: PreparedKeys) -> str | None:
    """Authenticate before decode or release. Header IDs cannot select custody."""
    typed = _context(field, tenant, record, keys)
    if frame is None:
        keys._resolve(field.domain_id, tenant, "payload", keys.policy.payload_generation)
        return None
    header_size = 46 if field.equality else 14
    overhead = header_size + 28
    if type(frame) is not bytes or not overhead <= len(frame) <= MAX_TEXT_BYTES + overhead:
        raise InvalidFrame()
    if frame[:5] != _MAGIC or frame[5] not in (0, 1):
        raise InvalidFrame()
    if frame[5] != int(field.equality):
        raise RepresentationMismatch()
    payload_generation = int.from_bytes(frame[6:10], "big")
    search_generation = int.from_bytes(frame[10:14], "big")
    if payload_generation == 0 or bool(search_generation) != field.equality:
        raise InvalidFrame()
    payload = keys._resolve(field.domain_id, tenant, "payload", payload_generation)
    search = keys._resolve(field.domain_id, tenant, "search", search_generation) if field.equality else None
    header = frame[:header_size]
    key = _derive(payload, tuple_bytes(b"CF1/payload-key", field.field_id.bytes, typed))
    try:
        encoded = AESGCMSIV(key).decrypt(frame[header_size:header_size + 12],
                                        frame[header_size + 12:], _aad(field, tenant, typed, header))
    except InvalidTag:
        raise AuthenticationFailed() from None
    except Exception:
        raise CryptoBackendUnavailable() from None
    if search is not None and not compare_digest(header[14:46], _term(encoded, field, search)):
        raise RepresentationMismatch()
    try:
        value = encoded.decode("utf8", errors="strict")
    except UnicodeError:
        raise InvalidText() from None
    if "\x00" in value:
        raise InvalidText()
    keys._resolve(field.domain_id, tenant, "payload", payload_generation)
    if field.equality:
        keys._resolve(field.domain_id, tenant, "search", search_generation)
    return value

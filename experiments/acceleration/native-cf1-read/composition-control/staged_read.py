"""Isolated S research control; Python composition, four fresh native primitives."""
from uuid import UUID
from hmac import compare_digest
from cryptalis.crypto import cf1
from cryptalis.crypto.cf1 import FieldDescriptor
from cryptalis.crypto.keys import (PreparedKeys, tuple_bytes, InvalidFrame,
    RepresentationMismatch, AuthenticationFailed, CryptoBackendUnavailable, InvalidText)
import native_primitives


def _derive(material, info):
    c = material.context
    # Tuple allocation remains Python, outside the caught native SHA operation.
    salt_input = tuple_bytes(b"CF1/root", c.domain_id.bytes, c.tenant_id.bytes,
                            c.root_id.bytes, c.generation.to_bytes(4, "big"))
    try:
        salt = native_primitives.sha256(salt_input)
    except RuntimeError:
        raise CryptoBackendUnavailable() from None
    try:
        return native_primitives.hkdf_sha256(material.root, salt, info, 32)
    except Exception:
        raise CryptoBackendUnavailable() from None


def _term(encoded, field, material):
    key = _derive(material, tuple_bytes(b"CF1/search-key", field.field_id.bytes,
                                       b"utf8-exact/v1", b"identity/v1", b"equality"))
    try:
        return native_primitives.hmac_sha256(key, tuple_bytes(b"equality", encoded))
    except Exception:
        raise CryptoBackendUnavailable() from None


def open_text_staged(frame: bytes | None, field: FieldDescriptor, tenant: UUID,
              record: UUID | int, keys: PreparedKeys) -> str | None:
    """Authenticate before decode or release. Header IDs cannot select custody."""
    typed = cf1._context(field, tenant, record, keys)
    if frame is None:
        keys._resolve(field.domain_id, tenant, "payload", keys.policy.payload_generation)
        return None
    header_size = 46 if field.equality else 14
    overhead = header_size + 28
    if type(frame) is not bytes or not overhead <= len(frame) <= cf1.MAX_TEXT_BYTES + overhead:
        raise InvalidFrame()
    if frame[:5] != cf1._MAGIC or frame[5] not in (0, 1):
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
        encoded = native_primitives.decrypt(key, frame[header_size:header_size + 12],
                                        frame[header_size + 12:], cf1._aad(field, tenant, typed, header))
    except RuntimeError as exc:
        if exc.args == ("data-processing",):
            raise AuthenticationFailed() from None
        raise CryptoBackendUnavailable() from None
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

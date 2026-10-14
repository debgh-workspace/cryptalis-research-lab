"""Separately named complete fresh read; no product monkeypatch or key cache."""
from cryptalis.crypto import cf1
from cryptalis.crypto.keys import (InvalidFrame, RepresentationMismatch, InvalidText,
                                  AuthenticationFailed, CryptoBackendUnavailable)
import native_cf1


def _bundle(material):
    c = material.context
    return (material.root, c.domain_id.bytes, c.tenant_id.bytes,
            c.root_id.bytes, c.generation.to_bytes(4, 'big'))


def _native_encoded(frame, field, tenant, typed, payload, search):
    try:
        return native_cf1.open_encoded(frame, int(field.equality), field.domain_id.bytes,
            tenant.bytes, field.field_id.bytes, field.digest, typed, _bundle(payload),
            None if search is None else _bundle(search))
    except RuntimeError as exc:
        category = exc.args[0] if len(exc.args) == 1 else None
        if category == 'data-processing':
            raise AuthenticationFailed() from None
        if category == 'term':
            raise RepresentationMismatch() from None
        raise CryptoBackendUnavailable() from None


def open_text_native(frame, field, tenant, record, keys):
    typed = cf1._context(field, tenant, record, keys)
    if frame is None:
        keys._resolve(field.domain_id, tenant, 'payload', keys.policy.payload_generation)
        return None
    header_size = 46 if field.equality else 14
    overhead = header_size + 28
    if type(frame) is not bytes or not overhead <= len(frame) <= cf1.MAX_TEXT_BYTES + overhead:
        raise InvalidFrame()
    if frame[:5] != cf1._MAGIC or frame[5] not in (0, 1):
        raise InvalidFrame()
    if frame[5] != int(field.equality):
        raise RepresentationMismatch()
    payload_generation = int.from_bytes(frame[6:10], 'big')
    search_generation = int.from_bytes(frame[10:14], 'big')
    if payload_generation == 0 or bool(search_generation) != field.equality:
        raise InvalidFrame()
    payload = keys._resolve(field.domain_id, tenant, 'payload', payload_generation)
    search = keys._resolve(field.domain_id, tenant, 'search', search_generation) if field.equality else None
    encoded = _native_encoded(frame, field, tenant, typed, payload, search)
    try:
        value = encoded.decode('utf8', errors='strict')
    except UnicodeError:
        raise InvalidText() from None
    if '\x00' in value:
        raise InvalidText()
    keys._resolve(field.domain_id, tenant, 'payload', payload_generation)
    if field.equality:
        keys._resolve(field.domain_id, tenant, 'search', search_generation)
    return value

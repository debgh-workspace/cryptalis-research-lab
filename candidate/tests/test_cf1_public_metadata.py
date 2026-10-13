"""Independent CF1 transcript and lease controls after public metadata reuse.

These tests are pure and can run directly with unittest; they never open a DB.
The normal aggregate suite still uses the unchanged PostgreSQL preflight.
"""
import hashlib
import hmac
import json
import os
import struct
import unittest
from dataclasses import asdict, replace
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

from cryptalis.crypto import cf1
from cryptalis.crypto.keys import (
    AuthenticationFailed, DevelopmentKeyProvider, KeyContext, KeyPolicy,
    Keyring, KeyUnavailable, RepresentationMismatch,
)


def _tuple(*parts):
    # Independent writer: no production encoding/helper calls.
    result = bytearray(struct.pack(">I", len(parts)))
    for part in parts:
        result.extend(struct.pack(">I", len(part)))
        result.extend(part)
    return bytes(result)


def _key(root, context, info):
    salt = hashlib.sha256(_tuple(b"CF1/root", context.domain_id.bytes,
                               context.tenant_id.bytes, context.root_id.bytes,
                               struct.pack(">I", context.generation))).digest()
    extracted = hmac.digest(salt, root, "sha256")
    # RFC 5869 SHA-256, exactly one 32-byte output block.
    return hmac.digest(extracted, info + b"\x01", "sha256")


def _reference(value, field, tenant, record, payload, search, nonce):
    encoded = value.encode("utf8")
    typed = (record.bytes if field.record_codec == "uuid16/v1" else
             _tuple(b"int64", struct.pack(">q", record)))
    root, context = payload
    term = b""
    if search:
        search_root, search_context = search
        info = _tuple(b"CF1/search-key", field.field_id.bytes,
                      b"utf8-exact/v1", b"identity/v1", b"equality")
        term = hmac.digest(_key(search_root, search_context, info),
                           _tuple(b"equality", encoded), "sha256")
    header = (b"CF1\x00\x01" + bytes([bool(search)]) + struct.pack(">I", context.generation)
              + struct.pack(">I", search[1].generation if search else 0) + term)
    key = _key(root, context, _tuple(b"CF1/payload-key", field.field_id.bytes, typed))
    aad = _tuple(b"CF1/payload", field.domain_id.bytes, tenant.bytes,
                 field.field_id.bytes, typed, field.digest, header)
    return header + nonce + AESGCMSIV(key).encrypt(nonce, encoded, aad)


def _prepared(domain, tenant, payload_root, search_root=None, generation=1, max_age=60):
    provider = DevelopmentKeyProvider()
    payload = payload_root, KeyContext(domain, tenant, "payload", UUID(int=701), generation)
    search = ((search_root, KeyContext(domain, tenant, "search", UUID(int=702), generation))
              if search_root is not None else None)
    materials = (payload, search) if search else (payload,)
    wrappers = tuple(provider.wrap(root, context) for root, context in materials)
    ring = Keyring(KeyPolicy(domain, tenant, wrappers, generation,
                            generation if search else None),
                   {provider.provider_id:provider}, max_age=max_age)
    return ring.prepare(), payload, search


class PublicMetadataControls(unittest.TestCase):
    def test_independent_transcripts_cover_context_and_exact_text_changes(self):
        nonce = bytes(range(12))
        for index in range(32):
            equality, bigint, single = bool(index & 1), bool(index & 2), bool(index & 4)
            domain, table, identity = (UUID(int=1000 + 3*index + n) for n in range(3))
            tenant = table if single else UUID(int=index)
            record = (-2**63, -1, 0, 2**63-1)[index % 4] if bigint else UUID(int=index)
            field = cf1.FieldDescriptor(domain, table, identity,
                      "int64-be/v1" if bigint else "uuid16/v1",
                      "single-tenant-uuid/v1" if single else "uuid16/v1",
                      "cf1-packed-equality/v1" if equality else "cf1-storage/v1",
                      hashlib.sha256(str(index).encode()).digest())
            roots = hashlib.sha256(b"payload" + bytes([index])).digest(), hashlib.sha256(b"search" + bytes([index])).digest()
            keys, payload, search = _prepared(domain, tenant, roots[0], roots[1] if equality else None,
                                             generation=(1, 0xffffffff)[index % 2])
            before = asdict(field), asdict(payload[1]), asdict(search[1]) if search else None
            for value in ("", "é", "e\u0301", "雪😀\n", " exact "):
                expected = _reference(value, field, tenant, record, payload, search, nonce)
                for _ in range(2):  # Cold then warm immutable metadata.
                    with patch.object(cf1.os, "urandom", return_value=nonce):
                        actual = cf1.seal_text(value, field, tenant, record, keys)
                    self.assertEqual(actual, expected)
                    self.assertEqual(cf1.open_text(expected, field, tenant, record, keys), value)
                    if equality:
                        self.assertEqual(cf1.equality_term(value, field, tenant, keys), expected[14:46])
            self.assertEqual(before, (asdict(field), asdict(payload[1]), asdict(search[1]) if search else None))
            # Dataclass serialization remains constructor-compatible after use.
            self.assertEqual(cf1.FieldDescriptor(**asdict(field)), field)
            self.assertEqual(KeyContext(**asdict(payload[1])), payload[1])

    def test_frozen_independent_vectors_remain_byte_exact_after_warming(self):
        vectors = json.loads((Path(__file__).parent / "fixtures/cf1_vectors.json").read_text())["vectors"]
        for vector in vectors:
            field = cf1.FieldDescriptor.from_compiled(vector["descriptor"], vector["descriptor_digest"])
            tenant = UUID(vector["tenant_id"])
            record = UUID(vector["record_id"]) if field.record_codec == "uuid16/v1" else vector["record_id"]
            provider = DevelopmentKeyProvider()
            wrappers = tuple(provider.wrap(bytes.fromhex(vector[purpose + "_root"]),
                      KeyContext(field.domain_id, tenant, purpose, UUID(vector[purpose + "_root_id"]),
                                 vector[purpose + "_generation"]))
                      for purpose in (("payload", "search") if field.equality else ("payload",)))
            keys = Keyring(KeyPolicy(field.domain_id, tenant, wrappers, vector["payload_generation"],
                                    vector["search_generation"] or None),
                           {provider.provider_id:provider}).prepare()
            expected = bytes.fromhex(vector["frame"])
            for _ in range(3):
                with patch.object(cf1.os, "urandom", return_value=bytes.fromhex(vector["nonce"])):
                    self.assertEqual(cf1.seal_text(vector["text"], field, tenant, record, keys), expected)
                self.assertEqual(cf1.open_text(expected, field, tenant, record, keys), vector["text"])

    def test_replaced_public_context_never_reuses_previous_transcript(self):
        domain, tenant, record = UUID(int=1), UUID(int=2), UUID(int=3)
        original = cf1.FieldDescriptor(domain, UUID(int=4), UUID(int=5), "uuid16/v1", "uuid16/v1",
                                       "cf1-packed-equality/v1", b"d"*32)
        keys, payload, search = _prepared(domain, tenant, b"p"*32, b"s"*32)
        cf1.seal_text("warm", original, tenant, record, keys)
        fields = [replace(original, field_id=UUID(int=6)), replace(original, digest=b"e"*32)]
        fields.append(replace(original, record_codec="int64-be/v1"))
        for field in fields:
            identity = 42 if field.record_codec == "int64-be/v1" else record
            expected = _reference("replacement", field, tenant, identity, payload, search, b"n"*12)
            with patch.object(cf1.os, "urandom", return_value=b"n"*12):
                self.assertEqual(cf1.seal_text("replacement", field, tenant, identity, keys), expected)
        c = payload[1]
        for changed in [replace(c, domain_id=UUID(int=8)), replace(c, tenant_id=UUID(int=0)),
                        replace(c, root_id=UUID(int=9)), replace(c, generation=0xffffffff)]:
            provider = DevelopmentKeyProvider()
            p = provider.wrap(b"p"*32, changed)
            s = provider.wrap(b"s"*32, replace(changed, purpose="search", root_id=UUID(int=702)))
            fresh = Keyring(KeyPolicy(changed.domain_id, changed.tenant_id, (p,s), changed.generation,
                                     changed.generation), {provider.provider_id:provider}).prepare()
            field = replace(original, domain_id=changed.domain_id)
            expected = _reference("changed context", field, changed.tenant_id, record,
                                  (b"p"*32, changed), (b"s"*32,s.context), b"n"*12)
            with patch.object(cf1.os, "urandom", return_value=b"n"*12):
                self.assertEqual(cf1.seal_text("changed context", field, changed.tenant_id, record, fresh), expected)

    def test_same_metadata_different_roots_does_not_reuse_a_key(self):
        domain, tenant, record = UUID(int=1), UUID(int=2), UUID(int=3)
        field = cf1.FieldDescriptor(domain, UUID(int=4), UUID(int=5), "uuid16/v1", "uuid16/v1",
                                    "cf1-packed-equality/v1", b"d"*32)
        keys, _, _ = _prepared(domain, tenant, b"p"*32, b"s"*32)
        frame = cf1.seal_text("warm", field, tenant, record, keys)
        term = cf1.equality_term("warm", field, tenant, keys)
        for roots, failure in (((b"q"*32,b"s"*32),AuthenticationFailed),
                               ((b"p"*32,b"t"*32),RepresentationMismatch)):
            fresh, _, _ = _prepared(domain, tenant, *roots)
            with self.assertRaises(failure):
                cf1.open_text(frame, field, tenant, record, fresh)
            if roots[1] != b"s"*32:
                self.assertNotEqual(cf1.equality_term("warm", field, tenant, fresh), term)

    def test_warm_metadata_cannot_bypass_expiry_or_post_crypto_expiry(self):
        domain, tenant, record = UUID(int=1), UUID(int=2), UUID(int=3)
        field = cf1.FieldDescriptor(domain, UUID(int=4), UUID(int=5), "uuid16/v1", "uuid16/v1",
                                    "cf1-packed-equality/v1", b"d"*32)
        now = [100.0]
        with patch("cryptalis.crypto.keys.time.monotonic", side_effect=lambda:now[0]):
            keys, _, _ = _prepared(domain, tenant, b"p"*32, b"s"*32, max_age=1)
            frame = cf1.seal_text("warm", field, tenant, record, keys)
            operations = [lambda:cf1.open_text(frame,field,tenant,record,keys),
                          lambda:cf1.seal_text("warm",field,tenant,record,keys),
                          lambda:cf1.equality_term("warm",field,tenant,keys)]
            for operation in operations:
                now[0] = 101
                with self.assertRaises(KeyUnavailable):
                    operation()
            original = cf1._derive
            def crosses_expiry(material, info):
                result = original(material, info)
                now[0] = 101
                return result
            for operation in operations:
                now[0] = 100
                with patch.object(cf1, "_derive", crosses_expiry):
                    with self.assertRaises(KeyUnavailable):
                        operation()

    def test_forked_warm_metadata_does_not_admit_inherited_keys(self):
        domain, tenant, record = UUID(int=1), UUID(int=2), UUID(int=3)
        field = cf1.FieldDescriptor(domain, UUID(int=4), UUID(int=5), "uuid16/v1", "uuid16/v1",
                                    "cf1-packed-equality/v1", b"d"*32)
        keys, _, _ = _prepared(domain, tenant, b"p"*32, b"s"*32)
        frame = cf1.seal_text("warm", field, tenant, record, keys)
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(read_fd)
            refused = 0
            for operation in (lambda:cf1.open_text(frame,field,tenant,record,keys),
                              lambda:cf1.equality_term("warm",field,tenant,keys)):
                try:
                    operation()
                except KeyUnavailable:
                    refused += 1
            os.write(write_fd, str(refused).encode())
            os._exit(0)
        os.close(write_fd)
        observed = os.read(read_fd, 10)
        os.close(read_fd)
        _, status = os.waitpid(pid, 0)
        self.assertEqual(os.waitstatus_to_exitcode(status), 0)
        self.assertEqual(observed, b"2")
        self.assertEqual(cf1.open_text(frame,field,tenant,record,keys), "warm")


if __name__ == "__main__":
    unittest.main(verbosity=2)

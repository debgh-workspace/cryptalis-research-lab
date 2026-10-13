"""Finite D3 research: unchanged D1 capture/pages, CF1 side-table staging.

Public synthetic text and roots only. No product capture admission or cutover.
The final complete oracle uses the separately qualified D2 decoder, never the
product decoder. Existing local test key preparation is reused unchanged.
"""
from contextlib import contextmanager
from dataclasses import dataclass, replace
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from uuid import UUID

from cryptalis.crypto import Keyring
from cryptalis.crypto.cf1 import FieldDescriptor, seal_text

from _online_enumeration_lab import EnumerationLab
from test_cf1 import DOMAIN, TABLE, FIELD, TENANT, setup_keys


_oracle_path = Path(__file__).resolve().parents[1] / "experiments" / "independent_cf1_decode.py"
_spec = importlib.util.spec_from_file_location("_d3_independent_cf1_decode", _oracle_path)
oracle = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = oracle
_spec.loader.exec_module(oracle)
assert Path(oracle.__file__).resolve() == _oracle_path.resolve()


class FixturePinMismatch(ValueError):
    pass


@dataclass(frozen=True)
class FixtureCrypto:
    provider: object
    ring: Keyring
    document: dict
    digest: str
    field: FieldDescriptor
    root: oracle.PublicFixtureRoot

    @classmethod
    def create(cls):
        # Existing fixture: public payload root bytes(range(32)), identity 6,
        # generation 1, and the existing volatile development wrapping provider.
        provider, ring = setup_keys(equality=False)
        document = {
            "schema": "cryptalis.context/v1", "domain_id": str(DOMAIN),
            "table_id": str(TABLE), "field_id": str(FIELD),
            "text_codec": "utf8-exact/v1", "normalizer": "identity/v1",
            "null_policy": "sql-null/v1", "record_codec": "int64-be/v1",
            "tenant_codec": "uuid16/v1", "representation": "cf1-storage/v1",
        }
        digest = hashlib.sha256(json.dumps(document, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        field = FieldDescriptor.from_compiled(document, digest)
        return cls(provider, ring, document, digest, field,
                   oracle.PublicFixtureRoot(UUID(int=6), 1, bytes(range(32))))

    def fresh(self):
        # Fresh local cache, same externally supplied fixture policy/provider.
        # This is not recovery of the volatile provider after process loss.
        ring = Keyring(self.ring.policy, {self.provider.provider_id: self.provider}, max_age=self.ring.max_age)
        return replace(self, ring=ring)

    def pin(self, operation):
        wrapper, = self.ring.policy.wrappers
        context = wrapper.context
        metadata = {
            "operation": str(operation), "descriptor": self.document,
            "descriptor_digest": self.digest, "tenant": str(TENANT),
            "payload_provider": str(wrapper.provider_id),
            "payload_root": str(context.root_id), "payload_generation": context.generation,
            "payload_wrapper_sha256": hashlib.sha256(wrapper.sealed).hexdigest(),
        }
        # No root or wrapping-key bytes are stored in operation metadata.
        return json.dumps(metadata, sort_keys=True, separators=(",", ":"))

    def decode(self, frame, record):
        return oracle.decode_cf1(frame, descriptor=self.document, descriptor_digest=self.digest,
                                 tenant=TENANT, record=record, payload=self.root)


class CF1EnumerationLab(EnumerationLab):
    def __init__(self, rows):
        self.crypto = FixtureCrypto.create()
        super().__init__(rows)
        self.expected_pin = self.crypto.pin(self.operation)

    def install_capture(self, c):
        # The unchanged D1 capture installation and these empty stage changes
        # share this outer transaction, including the source metadata lock.
        with c.transaction():
            super().install_capture(c)
            assert c.execute("SELECT count(*) FROM staged").fetchone() == (0,)
            c.execute("ALTER TABLE staged ALTER COLUMN v TYPE bytea USING NULL::bytea")
            c.execute("ALTER TABLE staged RENAME COLUMN v TO frame")
            c.execute("ALTER TABLE operation ADD COLUMN crypto_pin text")
            c.execute("UPDATE operation SET crypto_pin=%s WHERE id=%s", (self.expected_pin, self.operation))
            c.execute("ALTER TABLE operation ALTER COLUMN crypto_pin SET NOT NULL")

    def _require_pin(self, c, *, lock=False):
        query = "SELECT crypto_pin FROM operation WHERE singleton AND id=%s"
        if lock:
            query += " FOR SHARE"
        if c.execute(query, (self.operation,)).fetchone() != (self.expected_pin,):
            raise FixturePinMismatch("fixture operation/context pin mismatch")

    @classmethod
    def reconstruct(cls, schema, operation, crypto):
        lab = super().reconstruct(schema, operation)
        lab.crypto = crypto.fresh()
        lab.expected_pin = lab.crypto.pin(operation)
        with lab.connect() as c:
            lab._require_pin(c)
        return lab

    def page(self, c, **options):
        with c.transaction():
            self._require_pin(c, lock=True)
            return super().page(c, **options)

    def install(self, c, claimed, *, fault=None):
        if claimed.operation != self.operation:
            return False
        # Preparation outside the transaction cannot extend an issued lease.
        keys = self.crypto.ring.prepare(minimum_validity=min(1, self.crypto.ring.max_age / 2))
        with c.transaction():
            self._require_pin(c, lock=True)
            current = c.execute("SELECT token FROM dirty WHERE operation=%s AND id=%s FOR UPDATE",
                                (self.operation, claimed.key)).fetchone()
            if current != (claimed.token,):
                return False
            frame = (seal_text(claimed.value, self.crypto.field, TENANT, claimed.key, keys)
                     if claimed.live else None)
            c.execute("INSERT INTO staged(operation,id,frame,live,token) VALUES(%s,%s,%s,%s,%s) "
                      "ON CONFLICT(operation,id) DO UPDATE SET frame=EXCLUDED.frame,live=EXCLUDED.live,token=EXCLUDED.token",
                      (self.operation, claimed.key, frame, claimed.live, claimed.token))
            if fault == "after_stage":
                raise RuntimeError("CF1 worker after stage")
            retired = c.execute("DELETE FROM dirty WHERE operation=%s AND id=%s AND token=%s",
                                (self.operation, claimed.key, claimed.token))
            assert retired.rowcount == 1
            if fault == "after_retire":
                raise RuntimeError("CF1 worker after retire")
            return True

    def oracle(self, c):
        # Foreground writer schedules have finished. This read snapshot does
        # not claim to enforce writer exclusion in an actual deployment.
        with self.connect() as observer, observer.transaction():
            assert observer.info.backend_pid != c.info.backend_pid
            observer.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            self._require_pin(observer)
            assert observer.execute("SELECT complete FROM inventory WHERE operation=%s", (self.operation,)).fetchone() == (True,)
            assert observer.execute("SELECT operation,id,token FROM dirty ORDER BY operation,id").fetchall() == []
            source = observer.execute("SELECT id,v FROM source ORDER BY id").fetchall()
            native = observer.execute("SELECT id,v FROM native ORDER BY id").fetchall()
            frames = observer.execute("SELECT id,frame FROM staged WHERE operation=%s AND live ORDER BY id", (self.operation,)).fetchall()
            assert all(frame is None or type(frame) is bytes for _, frame in frames)
            decoded = [(key, self.crypto.decode(frame, key)) for key, frame in frames]
            assert source == native
            assert decoded == native
            return decoded


LOW = -(1 << 63)
HIGH = (1 << 63) - 1
ROWS = ((LOW, "lower 雪😀"), (-42, None), (0, ""), (HIGH, "upper e\u0301 é"))


@contextmanager
def opened_cf1_lab(rows=ROWS):
    lab = CF1EnumerationLab(rows)
    try:
        with lab.connect() as c:
            lab.install_capture(c)
        yield lab
    finally:
        lab.close()

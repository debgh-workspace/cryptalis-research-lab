"""Owned native coordination experiment derived from CP53/CP65.

No product API, cryptography, cutover, privilege qualification or scan removal.
The source has immutable bigint identities; the target is a synthetic side table.
The complete oracle is intentionally mandatory after the scheduled writers stop.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import os
import re
import uuid

import psycopg


@dataclass(frozen=True)
class Claim:
    operation: uuid.UUID
    key: int
    token: int
    value: str | None
    live: bool


class EnumerationLab:
    """One disposable schema and operation; all connections use the existing owner."""

    def __init__(self, rows):
        self.schema = "enumerate_" + uuid.uuid4().hex
        self.operation = uuid.uuid4()
        self.url = os.environ["CRYPTALIS_TEST_DATABASE_URL"]
        with psycopg.connect(self.url, autocommit=True) as c:
            c.execute("CREATE SCHEMA " + self.schema)
        with self.connect() as c, c.transaction():
            c.execute("CREATE TABLE source(id bigint PRIMARY KEY,v text,rev bigint NOT NULL DEFAULT 0)")
            c.execute("CREATE TABLE native(id bigint PRIMARY KEY,v text)")
            for key, value in rows:
                c.execute("INSERT INTO source(id,v) VALUES(%s,%s)", (key, value))
                c.execute("INSERT INTO native VALUES(%s,%s)", (key, value))

    def connect(self):
        c = psycopg.connect(self.url, autocommit=True)
        c.execute("SET search_path TO " + self.schema + ",pg_catalog")
        c.execute("SET statement_timeout='3s'")
        assert c.execute("SHOW transaction_isolation").fetchone() == ("read committed",)
        return c

    @classmethod
    def reconstruct(cls, schema, operation):
        """Reopen durable fixture state without creating or remembering a page."""
        if not isinstance(schema, str) or re.fullmatch(r"enumerate_[0-9a-f]{32}", schema) is None:
            raise ValueError("owned fixture schema required")
        if not isinstance(operation, uuid.UUID):
            raise ValueError("expected operation identity required")
        lab = cls.__new__(cls)
        lab.schema = schema
        lab.operation = operation
        lab.url = os.environ["CRYPTALIS_TEST_DATABASE_URL"]
        with lab.connect() as c:
            if c.execute("SELECT id FROM operation WHERE singleton").fetchone() != (operation,):
                raise ValueError("durable operation identity mismatch")
            if c.execute("SELECT operation FROM inventory").fetchone() != (operation,):
                raise ValueError("durable operation inventory mismatch")
        return lab

    def close(self):
        with psycopg.connect(self.url, autocommit=True) as c:
            c.execute("DROP SCHEMA " + self.schema + " CASCADE")

    def install_capture(self, c):
        # The lock serializes the initial capture boundary with earlier writers.
        # Operation metadata and trigger installation either all commit or none do.
        with c.transaction():
            c.execute("LOCK TABLE source IN ACCESS EXCLUSIVE MODE")
            c.execute("CREATE SEQUENCE work_tokens AS bigint NO CYCLE")
            c.execute("CREATE TABLE operation(singleton bool PRIMARY KEY CHECK(singleton),id uuid UNIQUE NOT NULL)")
            c.execute("INSERT INTO operation VALUES(true,%s)", (self.operation,))
            c.execute("CREATE TABLE inventory(operation uuid PRIMARY KEY REFERENCES operation(id),last_key bigint,complete bool NOT NULL DEFAULT false)")
            c.execute("INSERT INTO inventory(operation) VALUES(%s)", (self.operation,))
            c.execute("CREATE TABLE dirty(operation uuid NOT NULL REFERENCES operation(id),id bigint,token bigint NOT NULL,PRIMARY KEY(operation,id))")
            c.execute("CREATE TABLE staged(operation uuid NOT NULL REFERENCES operation(id),id bigint,v text,live bool NOT NULL,token bigint NOT NULL,PRIMARY KEY(operation,id))")
            c.execute("""CREATE FUNCTION assign_revision() RETURNS trigger LANGUAGE plpgsql AS $$
                BEGIN
                    IF TG_OP='UPDATE' AND NEW.id IS DISTINCT FROM OLD.id THEN
                        RAISE EXCEPTION 'immutable research identity' USING ERRCODE='23514';
                    END IF;
                    NEW.rev:=nextval('work_tokens'); RETURN NEW;
                END $$""")
            # This is a fixed internally generated UUID, never caller SQL.
            c.execute("""CREATE FUNCTION capture() RETURNS trigger LANGUAGE plpgsql AS $$
                DECLARE k bigint; t bigint;
                BEGIN
                    IF TG_OP='DELETE' THEN k:=OLD.id; t:=nextval('work_tokens');
                    ELSE k:=NEW.id; t:=NEW.rev; END IF;
                    INSERT INTO dirty VALUES('""" + str(self.operation) + """'::uuid,k,t)
                    ON CONFLICT(operation,id) DO UPDATE SET token=EXCLUDED.token;
                    IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
                END $$""")
            c.execute("CREATE TRIGGER assign_revision BEFORE INSERT OR UPDATE ON source FOR EACH ROW EXECUTE FUNCTION assign_revision()")
            c.execute("CREATE TRIGGER capture AFTER INSERT OR UPDATE OR DELETE ON source FOR EACH ROW EXECUTE FUNCTION capture()")

    def write(self, c, action, key, value=None):
        """Apply the same native statement and values in one fixture transaction."""
        with c.transaction():
            for table in ("native", "source"):
                if action == "insert":
                    c.execute("INSERT INTO " + table + "(id,v) VALUES(%s,%s)", (key, value))
                elif action == "update":
                    c.execute("UPDATE " + table + " SET v=%s WHERE id=%s", (value, key))
                elif action == "delete":
                    c.execute("DELETE FROM " + table + " WHERE id=%s", (key,))
                else:
                    raise ValueError("unknown synthetic write")

    def seed(self, c, key):
        # Reuse CP65's fresh-work-identity rule; this is not a source revision.
        token = c.execute("SELECT nextval('work_tokens')").fetchone()[0]
        c.execute("INSERT INTO dirty VALUES(%s,%s,%s) ON CONFLICT(operation,id) DO UPDATE SET token=GREATEST(dirty.token,EXCLUDED.token)",
                  (self.operation, key, token))

    def page(self, c, *, size=2, after_read=None, fault=None):
        if type(size) is not int or size < 1:
            raise ValueError("positive bounded page size required")
        with c.transaction():
            cursor = c.execute("SELECT last_key,complete FROM inventory WHERE operation=%s FOR UPDATE", (self.operation,)).fetchone()
            if cursor is None:
                raise ValueError("operation inventory missing")
            last, complete = cursor
            if complete:
                return ()
            keys = tuple(row[0] for row in c.execute(
                "SELECT id FROM source WHERE (%s::bigint IS NULL OR id>%s) ORDER BY id LIMIT %s",
                (last, last, size)).fetchall())
            if after_read is not None:
                after_read(keys)
            for key in keys:
                self.seed(c, key)
            if fault == "before_cursor":
                raise RuntimeError(fault)
            if keys:
                c.execute("UPDATE inventory SET last_key=%s WHERE operation=%s", (keys[-1], self.operation))
            else:
                c.execute("UPDATE inventory SET complete=true WHERE operation=%s", (self.operation,))
            if fault == "after_cursor":
                raise RuntimeError(fault)
            return keys

    def claim(self, c, key):
        row = c.execute("SELECT d.token,s.v,s.id IS NOT NULL FROM dirty d LEFT JOIN source s USING(id) WHERE d.operation=%s AND d.id=%s",
                        (self.operation, key)).fetchone()
        return None if row is None else Claim(self.operation, key, *row)

    def install(self, c, claimed, *, fault=False):
        with c.transaction():
            if claimed.operation != self.operation:
                return False
            if c.execute("SELECT id FROM operation WHERE singleton AND id=%s", (claimed.operation,)).fetchone() is None:
                return False
            actual = c.execute("SELECT token FROM dirty WHERE operation=%s AND id=%s FOR UPDATE", (claimed.operation, claimed.key)).fetchone()
            if actual != (claimed.token,):
                return False
            c.execute("INSERT INTO staged VALUES(%s,%s,%s,%s,%s) ON CONFLICT(operation,id) DO UPDATE SET v=EXCLUDED.v,live=EXCLUDED.live,token=EXCLUDED.token",
                      (claimed.operation, claimed.key, claimed.value, claimed.live, claimed.token))
            retired = c.execute("DELETE FROM dirty WHERE operation=%s AND id=%s AND token=%s", (claimed.operation, claimed.key, claimed.token))
            assert retired.rowcount == 1
            if fault:
                raise RuntimeError("worker before commit")
            return True

    def drain(self, c):
        # Called only after each schedule's foreground writers have stopped.
        for key, in c.execute("SELECT id FROM dirty WHERE operation=%s ORDER BY id", (self.operation,)).fetchall():
            claimed = self.claim(c, key)
            assert claimed is not None and self.install(c, claimed)

    def finish(self, c):
        while not c.execute("SELECT complete FROM inventory WHERE operation=%s", (self.operation,)).fetchone()[0]:
            self.page(c)
        self.drain(c)
        self.oracle(c)

    def oracle(self, c):
        # A separate read-only observer checks committed durable state. Scheduled
        # writers have stopped; the snapshot is no substitute for a product fence.
        with self.connect() as observer, observer.transaction():
            assert observer.info.backend_pid != c.info.backend_pid
            observer.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            assert observer.execute("SELECT complete FROM inventory WHERE operation=%s", (self.operation,)).fetchone() == (True,)
            assert observer.execute("SELECT operation,id,token FROM dirty ORDER BY operation,id").fetchall() == []
            # Complete ordered exact-value comparisons, with native NULL semantics.
            native = observer.execute("SELECT id,v FROM native ORDER BY id").fetchall()
            source = observer.execute("SELECT id,v FROM source ORDER BY id").fetchall()
            stage = observer.execute("SELECT id,v FROM staged WHERE operation=%s AND live ORDER BY id", (self.operation,)).fetchall()
            assert source == native
            assert stage == native

    def snapshot(self, c):
        return tuple(c.execute("SELECT * FROM " + table + " ORDER BY 1,2").fetchall()
                     for table in ("source", "native", "operation", "inventory", "dirty", "staged"))


@contextmanager
def opened_lab(rows=((10, "ten"), (30, None), (50, "fifty")), *, capture=True):
    lab = EnumerationLab(rows)
    try:
        if capture:
            with lab.connect() as c:
                lab.install_capture(c)
        yield lab
    finally:
        lab.close()

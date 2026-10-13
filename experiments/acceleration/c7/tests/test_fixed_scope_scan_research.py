"""Research-only fixed-scope scan; never a product query rewrite or fallback.

Run only through the coordinator's unchanged PostgreSQL preflight. Native oracle
traffic is deliberately outside the candidate privacy trace. No timing claim.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import resource
import statistics
import time
from types import SimpleNamespace
from uuid import UUID, uuid4

import psycopg
from psycopg import sql
import pytest
import sqlalchemy
from sqlalchemy import Column, Index, MetaData, Table, Text, Uuid
from sqlalchemy import bindparam, create_engine, event, select, text
from sqlalchemy.orm import registry, sessionmaker

from cryptalis.crypto import AuthenticationFailed, Keyring, KeyUnavailable
from cryptalis.manifest.compiler import Writer, WriterInventory, compile_protection
from cryptalis.sqlalchemy import attach, UnsupportedProtectedOperation
from test_migration import DOMAIN, TABLE_ID, FIELD_ID, TENANT, PROVIDER
from test_migration import PublicFixtureProvider, independent_open, keys


OTHER = UUID(int=506)
ROW_LIMIT = 10_000
BYTE_LIMIT = 64 * 1024 * 1024
PARTITION = 128
OUTPUT = Path(__file__).parents[1] / "evidence" / "c7-scan"
BASELINE = "fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str,
                                     separators=(",", ":")).encode()).hexdigest()


def clock():
    return {"wall_ns": time.perf_counter_ns(), "cpu_ns": time.thread_time_ns()}


def elapsed(start, end):
    return {key.replace("_ns", "_ms"): (end[key] - start[key]) / 1e6 for key in start}


def write_receipt(name, value):
    value["sqlalchemy"] = sqlalchemy.__version__
    value["baseline_sqlalchemy_sha256"] = BASELINE
    value["harness_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    protocol = Path(__file__).parents[1] / "experiments" / "scan-baseline" / "PROTOCOL.md"
    value["protocol_sha256"] = hashlib.sha256(protocol.read_bytes()).hexdigest()
    root = Path(__file__).parents[1]
    value["source_sha256"] = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in ("src/cryptalis/crypto/cf1.py", "src/cryptalis/crypto/keys.py",
                     "src/cryptalis/manifest/compiler.py", "src/cryptalis/manifest/declaration.py",
                     "tests/test_migration.py")}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / f"{name}-sa{sqlalchemy.__version__}.json"
    # One finite run per cell; preserve a prior result rather than overwrite it.
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, default=str)
        stream.write("\n")


def value_at(i, n, tenant):
    if i == n - 1:
        return "rare:" + str(tenant)
    special = (None, "", "é", "e\u0301", "雪😀", "hot")
    if i % 11 < len(special):
        return special[i % 11]
    return "user-" + hashlib.sha256(f"synthetic:{tenant}:{i % 137}".encode()).hexdigest()[:32] + "@example.invalid"


def fixture_rows(n, tenant):
    offset = 0 if tenant == TENANT else 100_000
    return [(UUID(int=10_000 + offset + i), tenant, value_at(i, n, tenant)) for i in range(n)]


@dataclass(frozen=True)
class Predicate:
    label: str
    kind: str
    values: tuple
    offset: int = 0
    limit: int | None = None


def corpus(tenant):
    equal = ("hot", "rare:" + str(tenant), "absent", "", "é", "e\u0301", None)
    result = [Predicate(f"eq-{i}", "eq", (value,)) for i, value in enumerate(equal)]
    terms20 = tuple(["hot", "", "é", "e\u0301", "雪😀"] + [f"absent-{i}" for i in range(15)])
    result += [Predicate("in-empty", "in", ()), Predicate("in-null", "in", (None,)),
               Predicate("in-mixed-null", "in", ("hot", None)),
               Predicate("in-duplicates", "in", ("hot", "hot", "absent", "é")),
               Predicate("in20", "in", terms20),
               Predicate("eq-page", "eq", ("hot",), 3, 7),
               Predicate("in-page", "in", terms20, 17, 11)]
    assert len(result) == 14
    return tuple(result)


def truth(value, predicate):
    if predicate.kind == "eq":
        other = predicate.values[0]
        return None if value is None or other is None else value == other
    if predicate.kind != "in":
        raise ValueError("research grammar refused")
    if not predicate.values:
        return False
    if value is not None and any(other is not None and value == other for other in predicate.values):
        return True
    return None if value is None or None in predicate.values else False


def evaluate(buffer, predicate):
    # Called only after the fixed scan's database context has exited.
    truths = [(record, truth(value, predicate)) for record, _, value in buffer]
    rows = [row for row, (_, answer) in zip(buffer, truths) if answer is True]
    stop = None if predicate.limit is None else predicate.offset + predicate.limit
    return truths, rows[predicate.offset:stop]


class ScanIncomplete(RuntimeError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def fixed_scan(session, model, tenant, *, row_limit=ROW_LIMIT, byte_limit=BYTE_LIMIT,
               after_partition=None, cancelled=None):
    """No predicate parameter: every successful invocation consumes every row."""
    if not (0 < row_limit <= ROW_LIMIT and 0 < byte_limit <= BYTE_LIMIT):
        raise ScanIncomplete("invalid_research_budget")
    statement = (select(model.id, model.tenant_id, model.name)
                 .where(model.tenant_id == tenant).order_by(model.id)
                 .execution_options(yield_per=PARTITION))
    buffer, batches, used = [], [], 0
    result = session.execute(statement)
    try:
        for index, partition in enumerate(result.partitions(PARTITION)):
            begin = clock()
            if cancelled is not None and cancelled():
                raise ScanIncomplete("cooperative_cancellation")
            for row in partition:
                record, returned_tenant, value = tuple(row)
                assert type(record) is UUID and returned_tenant == tenant
                assert value is None or type(value) is str
                # Logical frame and UUID bytes, not driver/RSS/wire accounting.
                used += 32 + (0 if value is None else 42 + len(value.encode("utf8")))
                if len(buffer) == row_limit or used > byte_limit:
                    raise ScanIncomplete("research_budget_exceeded")
                buffer.append((record, returned_tenant, value))
            batches.append({"index": index, "rows": len(partition),
                            "observed_after_fetch": begin, "processed": clock()})
            if after_partition is not None:
                after_partition(index)
        return buffer, {"rows": len(buffer), "logical_bytes": used,
                        "logical_partitions": [b["rows"] for b in batches],
                        "buffer_hash": digest(buffer), "partition_times": batches}
    finally:
        result.close()


@contextmanager
def observe(engine):
    events = []
    def before(connection, cursor, statement, parameters, context, many):
        events.append({"sql_hash": digest(statement), "bind_hash": digest(parameters),
                       "executemany": bool(many), "time": clock()})
    event.listen(engine, "before_cursor_execute", before)
    try:
        yield events
    finally:
        event.remove(engine, "before_cursor_execute", before)


def scan(app, tenant, **options):
    with observe(app.protected_engine) as events:
        with app.sessions(tenant_id=tenant) as session:
            buffer, receipt = fixed_scan(session, app.Protected, tenant, **options)
    receipt["sql_structure"] = [{k: v for k, v in e.items() if k != "time"} for e in events]
    receipt["sql_times"] = [e["time"] for e in events]
    assert receipt["sql_structure"], "observer did not see the candidate read"
    return buffer, receipt


def research_request(app, tenant, predicate, **options):
    buffer, receipt = scan(app, tenant, **options)
    # scan() has closed the result, session and transaction before evaluation.
    return evaluate(buffer, predicate), receipt


def native_predicate(model, predicate):
    if predicate.kind == "eq":
        return model.name == bindparam("needle", type_=Text()), {"needle": predicate.values[0]}
    return model.name.in_(bindparam("needles", expanding=True, type_=Text())), {"needles": list(predicate.values)}


def native_orm(app, tenant, predicate, *, with_truth=True):
    condition, params = native_predicate(app.Native, predicate)
    scope = app.Native.tenant_id == tenant
    with app.native_sessions() as session:
        truths = ([(r, t) for r, t in session.execute(select(app.Native.id, condition).where(scope).order_by(app.Native.id), params)]
                  if with_truth else None)
        statement = select(app.Native.id, app.Native.tenant_id, app.Native.name).where(scope, condition).order_by(app.Native.id).offset(predicate.offset)
        if predicate.limit is not None:
            statement = statement.limit(predicate.limit)
        rows = [tuple(row) for row in session.execute(statement, params)]
    return truths, rows


def direct_native(app, tenant, predicate):
    condition = sql.SQL("name = %s::text") if predicate.kind == "eq" else sql.SQL("name = ANY(%s::text[])")
    value = predicate.values[0] if predicate.kind == "eq" else list(predicate.values)
    table = sql.SQL("{}.native_rows").format(sql.Identifier(app.schema))
    with psycopg.connect(os.environ["CRYPTALIS_TEST_RUNTIME_DATABASE_URL"], connect_timeout=5) as connection:
        connection.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
        truths = connection.execute(sql.SQL("SELECT id, {} FROM {} WHERE tenant_id=%s ORDER BY id").format(condition, table), (value, tenant)).fetchall()
        query = sql.SQL("SELECT id,tenant_id,name FROM {} WHERE tenant_id=%s AND ({}) ORDER BY id OFFSET %s").format(table, condition)
        params = [tenant, value, predicate.offset]
        if predicate.limit is not None:
            query += sql.SQL(" LIMIT %s")
            params.append(predicate.limit)
        rows = connection.execute(query, params).fetchall()
    return truths, rows


def make_engine(variable):
    return create_engine("postgresql+psycopg://", echo=False, hide_parameters=True,
                         isolation_level="REPEATABLE READ",
                         creator=lambda: psycopg.connect(os.environ[variable], connect_timeout=5))


@pytest.fixture(scope="module", params=(1000, 10000), ids=("n1000", "n10000"))
def scan_app(request):
    import cryptalis.sqlalchemy as adapter
    assert hashlib.sha256(Path(adapter.__file__).read_bytes()).hexdigest() == BASELINE
    assert sqlalchemy.__version__ in ("2.0.51", "2.1.3")
    assert all(os.environ.get(k) for k in ("CRYPTALIS_TEST_DATABASE_URL", "CRYPTALIS_TEST_RUNTIME_DATABASE_URL"))
    n = request.param
    schema = "cryptalis_c7_" + uuid4().hex
    owner = make_engine("CRYPTALIS_TEST_DATABASE_URL")
    native_engine = make_engine("CRYPTALIS_TEST_RUNTIME_DATABASE_URL")
    protected_engine = make_engine("CRYPTALIS_TEST_RUNTIME_DATABASE_URL")
    native_mapping = registry(metadata=MetaData(schema=schema))
    protected_mapping = registry(metadata=MetaData(schema=schema))
    class Native: pass
    class Protected: pass
    for mapping, name, model in ((native_mapping, "native_rows", Native), (protected_mapping, "protected_rows", Protected)):
        table = Table(name, mapping.metadata, Column("id", Uuid, primary_key=True, autoincrement=False),
                      Column("tenant_id", Uuid, nullable=False), Column("name", Text(collation="C")))
        Index(name + "_scope", table.c.tenant_id, table.c.id)
        if model is Native:
            Index("native_equality", table.c.tenant_id, table.c.name)
        mapping.map_imperatively(model, table)
    try:
        with owner.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        native_mapping.metadata.create_all(owner)
        protected_mapping.metadata.create_all(owner)
        declaration = {"schema": "cryptalis.protection/v1", "profile": "cf1", "domain_id": str(DOMAIN),
                       "models": [{"model": "Protected", "table_id": str(TABLE_ID), "tenancy": {"column": "tenant_id"},
                                   "fields": [{"name": "name", "field_id": str(FIELD_ID), "protect": True,
                                               "queries": [], "accept_leakage": []}]}]}
        plan = compile_protection(json.dumps(declaration).encode(), protected_mapping, owner,
                                  writers=WriterInventory(True, (Writer(TABLE_ID, "c7-owned-fixture", "sqlalchemy", evidence="synthetic fixture; only this test writes"),)))
        descriptor = json.loads(plan.lock_bytes)["models"][0]["fields"][0]["descriptor"]
        assert descriptor["representation"] == "cf1-storage/v1"
        # Empty-table test setup only; no existing frame or application migration.
        with owner.begin() as connection:
            connection.execute(text(f'ALTER TABLE "{schema}".protected_rows ALTER COLUMN name TYPE bytea USING NULL::bytea'))
        with psycopg.connect(os.environ["CRYPTALIS_TEST_RUNTIME_DATABASE_URL"], connect_timeout=5) as connection:
            role = connection.execute("SELECT current_user").fetchone()[0]
            assert int(connection.execute("SHOW server_version_num").fetchone()[0]) // 10000 == 16
            assert connection.execute("SELECT NOT rolsuper AND NOT rolcreatedb AND NOT rolcreaterole AND NOT rolbypassrls FROM pg_roles WHERE rolname=current_user").fetchone() == (True,)
        with psycopg.connect(os.environ["CRYPTALIS_TEST_DATABASE_URL"], connect_timeout=5) as connection:
            connection.execute(sql.SQL("REVOKE ALL ON SCHEMA {} FROM PUBLIC, {}").format(sql.Identifier(schema), sql.Identifier(role)))
            connection.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(sql.Identifier(schema), sql.Identifier(role)))
            for table in ("native_rows", "protected_rows"):
                connection.execute(sql.SQL("REVOKE ALL ON TABLE {}.{} FROM PUBLIC, {}").format(sql.Identifier(schema), sql.Identifier(table), sql.Identifier(role)))
                connection.execute(sql.SQL("GRANT SELECT,INSERT,UPDATE,DELETE ON TABLE {}.{} TO {}").format(sql.Identifier(schema), sql.Identifier(table), sql.Identifier(role)))
        rings = {tenant: keys(tenant) for tenant in (TENANT, OTHER)}
        sessions = attach(protected_mapping, protected_engine, lock=plan.lock_bytes, keys=rings.__getitem__)
        native_sessions = sessionmaker(native_engine)
        for tenant in (TENANT, OTHER):
            values = fixture_rows(n, tenant)
            for model, factory in ((Native, lambda: native_sessions()), (Protected, lambda: sessions(tenant_id=tenant))):
                for start in range(0, n, 250):
                    with factory() as session:
                        session.add_all([model(id=i, tenant_id=t, name=v) for i, t, v in values[start:start+250]])
                        session.commit()
        with owner.connect() as connection:
            stored = connection.exec_driver_sql(f'SELECT id,tenant_id,name FROM "{schema}".protected_rows ORDER BY id').all()
        expected = fixture_rows(n, TENANT) + fixture_rows(n, OTHER)
        independently_opened = [(record, tenant, independent_open(frame, descriptor, tenant, record)) for record, tenant, frame in stored]
        assert independently_opened == expected
        assert all(frame is None or (frame[5] == 0 and frame[10:14] == b"\0"*4) for _, _, frame in stored)
        yield SimpleNamespace(n=n, schema=schema, owner=owner, Native=Native, Protected=Protected,
                              native_engine=native_engine, protected_engine=protected_engine,
                              native_sessions=native_sessions, sessions=sessions, rings=rings,
                              fixture_digest=digest(expected), descriptor=descriptor)
    finally:
        native_engine.dispose()
        protected_engine.dispose()
        with owner.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        owner.dispose()
        native_mapping.dispose()
        protected_mapping.dispose()


def test_fixed_scope_native_semantics_and_structure(scan_app):
    app = scan_app
    receipt = {"scope": "research-only structural observations; timing/wire independence not claimed",
               "n_per_tenant": app.n, "fixture_digest": app.fixture_digest, "cases": [], "outcome": "RUNNING"}
    try:
        for tenant in (TENANT, OTHER):
            structure = None
            for predicate in corpus(tenant):
                buffer, scan_receipt = scan(app, tenant)
                candidate = evaluate(buffer, predicate)
                oracle = direct_native(app, tenant, predicate)
                ordinary = native_orm(app, tenant, predicate)
                assert candidate == oracle == ordinary
                assert buffer == fixture_rows(app.n, tenant)
                assert all(type(answer) is bool or answer is None for _, answer in candidate[0])
                current = {key: scan_receipt[key] for key in ("rows", "logical_bytes", "logical_partitions", "buffer_hash", "sql_structure")}
                if structure is None:
                    structure = current
                assert current == structure
                receipt["cases"].append({"tenant": str(tenant), "case": predicate.label,
                                         "native_match": True, "truth_hash": digest(candidate[0]),
                                         "result_hash": digest(candidate[1]), "result_rows": len(candidate[1]),
                                         "scan": scan_receipt})
        receipt["outcome"] = "PASS"
    except BaseException as exc:
        receipt["outcome"] = "FAIL"
        receipt["failure_type"] = type(exc).__name__
        raise
    finally:
        write_receipt(f"semantics-n{app.n}", receipt)


def test_fixed_scope_admission_and_incomplete_results(scan_app):
    app = scan_app
    completed = []
    receipt = {"n_per_tenant": app.n, "controls": completed, "outcome": "RUNNING"}
    try:
        early_page = next(p for p in corpus(TENANT) if p.label == "eq-page")
        for options in ({"row_limit": 1}, {"byte_limit": 1}):
            with pytest.raises(ScanIncomplete, match="research_budget_exceeded"):
                research_request(app, TENANT, early_page, **options)
            completed.append({"control": list(options)[0], "partial_success": False})
        cancelled = [False]
        def cancel(index):
            cancelled[0] = True
        with pytest.raises(ScanIncomplete, match="cooperative_cancellation"):
            research_request(app, TENANT, early_page, after_partition=cancel, cancelled=lambda: cancelled[0])
        completed.append({"control": "cooperative_cancellation", "partial_success": False})
        with observe(app.protected_engine) as observed:
            with app.sessions(tenant_id=TENANT) as session:
                with pytest.raises(UnsupportedProtectedOperation):
                    session.execute(select(app.Protected.id).where(app.Protected.name == "hot"))
        assert observed == []
        completed.append({"control": "storage_only_sql_equality_refused", "driver_calls": 0})
        identity = fixture_rows(app.n, TENANT)[-1][0]  # tail frame after early page matches
        with app.owner.begin() as connection:
            frame = connection.exec_driver_sql(f'SELECT name FROM "{app.schema}".protected_rows WHERE id=%s', (identity,)).scalar_one()
            damaged = frame[:-1] + bytes([frame[-1] ^ 1])
            connection.exec_driver_sql(f'UPDATE "{app.schema}".protected_rows SET name=%s WHERE id=%s', (damaged, identity))
        try:
            for predicate in (early_page, next(p for p in corpus(TENANT) if p.label == "in-empty")):
                with pytest.raises(AuthenticationFailed):
                    research_request(app, TENANT, predicate)
                completed.append({"control": "damaged_tail_frame", "case": predicate.label,
                                  "partial_success": False})
        finally:
            with app.owner.begin() as connection:
                connection.exec_driver_sql(f'UPDATE "{app.schema}".protected_rows SET name=%s WHERE id=%s', (frame, identity))
        original = app.rings[TENANT]
        app.rings[TENANT] = Keyring(original.policy, {PROVIDER: PublicFixtureProvider()}, max_age=0.05)
        progressed = []
        def expire_after_partition(index):
            progressed.append(index)
            time.sleep(0.075)
        try:
            with pytest.raises(KeyUnavailable):
                research_request(app, TENANT, early_page, after_partition=expire_after_partition)
            completed.append({"control": "naturally_expired_short_fixture_lease", "partial_success": False,
                              "completed_partitions_before_expiry": progressed})
        finally:
            app.rings[TENANT] = original
        recovered, _ = scan(app, TENANT)
        assert recovered == fixture_rows(app.n, TENANT)
        completed.append({"control": "fresh_session_recovery", "complete_rows": len(recovered)})
        receipt["outcome"] = "PASS"
    except BaseException as exc:
        receipt["outcome"] = "FAIL"
        receipt["failure_type"] = type(exc).__name__
        raise
    finally:
        write_receipt(f"failure-controls-n{app.n}", receipt)


def p95(values):
    return sorted(values)[int((len(values) * 95 + 99) // 100) - 1]


def test_fixed_scope_finite_cost(scan_app):
    app = scan_app
    receipt = {"n_per_tenant": app.n, "warmups": 10, "pairs": 30, "observations": [],
               "context_full_native": [], "summary": {}, "outcome": "RUNNING",
               "process_maxrss_start_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "limits": "One synthetic instrumented cell; no timing privacy, production qualification, noise exclusion or gate retry."}
    try:
        predicates = (corpus(TENANT)[0], next(p for p in corpus(TENANT) if p.label == "in20"))
        for predicate in predicates:
            expected = direct_native(app, TENANT, predicate)[1]
            timings = {"native": [], "scan": []}
            for iteration in range(40):
                for kind in (("native", "scan") if iteration % 2 == 0 else ("scan", "native")):
                    start = clock()
                    if kind == "native":
                        _, result = native_orm(app, TENANT, predicate, with_truth=False)
                        logical_bytes = None
                    else:
                        buffer, metrics = scan(app, TENANT)
                        _, result = evaluate(buffer, predicate)
                        logical_bytes = metrics["logical_bytes"]
                    end = clock()
                    assert result == expected
                    record = {"case": predicate.label, "iteration": iteration, "warmup": iteration < 10,
                              "kind": kind, "start": start, "end": end, "elapsed": elapsed(start, end),
                              "result_rows": len(result), "logical_scan_bytes": logical_bytes}
                    receipt["observations"].append(record)
                    if iteration >= 10:
                        timings[kind].append(record["elapsed"]["wall_ms"])
            target = 3 if predicate.kind == "eq" else 8
            added = p95(timings["scan"]) - p95(timings["native"])
            receipt["summary"][predicate.label] = {"native_p50_ms": statistics.median(timings["native"]),
                "scan_p50_ms": statistics.median(timings["scan"]), "native_p95_ms": p95(timings["native"]),
                "scan_p95_ms": p95(timings["scan"]), "added_p95_ms": added,
                "unchanged_target_ms": target, "target_met": added <= target}
        for iteration in range(3):
            start = clock()
            with app.native_sessions() as session:
                rows = [tuple(row) for row in session.execute(select(app.Native.id, app.Native.tenant_id, app.Native.name)
                        .where(app.Native.tenant_id == TENANT).order_by(app.Native.id).execution_options(yield_per=PARTITION))]
            end = clock()
            assert rows == fixture_rows(app.n, TENANT)
            receipt["context_full_native"].append({"iteration": iteration, "elapsed": elapsed(start, end), "rows": len(rows)})
        receipt["cost_gate"] = "PASS" if all(s["target_met"] for s in receipt["summary"].values()) else "FAIL"
        receipt["outcome"] = "MEASURED"
    except BaseException as exc:
        receipt["outcome"] = "FAIL"
        receipt["failure_type"] = type(exc).__name__
        raise
    finally:
        receipt["process_maxrss_end_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        write_receipt(f"cost-n{app.n}", receipt)
    assert receipt["cost_gate"] == "PASS", "Research scan missed unchanged latency envelope; retain failed receipt"

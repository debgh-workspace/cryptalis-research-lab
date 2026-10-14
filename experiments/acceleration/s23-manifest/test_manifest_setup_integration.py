"""Real activation and query acceptance for the emitted setup template.

Prepared only. Run through the unchanged coordinator PostgreSQL wrapper.
This covers template integration, not provider custody or release qualification.
"""

import asyncio
from contextlib import contextmanager
import json
import os
import textwrap
from uuid import UUID

import psycopg
import pytest
from sqlalchemy import Text, bindparam, event, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from cryptalis.doctor import doctor
from test_migration import TENANT, application, keys, publish, run


_MARKERS = frozenset(("exact", "é", "e\u0301"))


def _queries(Customer):
    """Rebuild statements across cutover; never retain native compiled objects."""
    cases = (
        (Customer.name == bindparam("value", type_=Text()), {"value": "exact"}),
        (Customer.name == "é", {}),
        (Customer.name == "e\u0301", {}),
        (Customer.name.in_(bindparam("values", expanding=True, type_=Text())),
         {"values": [None, "", "e\u0301"]}),
        (Customer.name.in_([]), {}),
    )
    return [
        (select(Customer.id, Customer.name)
         .where(Customer.tenant_id == TENANT, predicate)
         .order_by(Customer.id), parameters)
        for predicate, parameters in cases
    ]


def _expected():
    # Independent exact outputs for test_migration.application(rows=7).
    return [
        [(UUID(int=105), "exact")],
        [(UUID(int=104), "é")],
        [(UUID(int=103), "e\u0301")],
        [(UUID(int=101), ""), (UUID(int=103), "e\u0301")],
        [],
    ]


def _values(result):
    rows = [tuple(row) for row in result.all()]
    assert all(type(identity) is UUID and type(value) is str
               for identity, value in rows)
    return rows


def _leaves(value):
    if type(value) is dict:
        for part in value.values():
            yield from _leaves(part)
    elif type(value) in (tuple, list):
        for part in value:
            yield from _leaves(part)
    else:
        yield value


@contextmanager
def _observe_query_binds(native_engine):
    # Keep only counts/booleans, never statements, binds, or connection details.
    observation = {"calls": 0, "protected_literal_seen": False}

    def observe(connection, cursor, statement, parameters, context, many):
        observation["calls"] += 1
        observation["protected_literal_seen"] |= any(
            type(value) is str and value in _MARKERS
            for value in _leaves(parameters)
        )

    event.listen(native_engine, "before_cursor_execute", observe)
    try:
        yield observation
    finally:
        event.remove(native_engine, "before_cursor_execute", observe)


@contextmanager
def _observe_connections(native_engine):
    # Cover both fresh DBAPI connections and reuse of existing pooled handles.
    observed = {"events": [], "checkout_identities": []}
    pool = native_engine.pool

    def connection_attempt(*args, **kwargs):
        observed["events"].append("do_connect")

    def engine_connect(connection):
        observed["events"].append("engine_connect")

    def checkout(dbapi_connection, connection_record, connection_proxy):
        observed["events"].append("checkout")
        # Only transient object identity, never connection properties or URLs.
        observed["checkout_identities"].append(id(dbapi_connection))

    event.listen(native_engine, "do_connect", connection_attempt)
    event.listen(native_engine, "engine_connect", engine_connect)
    event.listen(pool, "checkout", checkout)
    try:
        yield observed
    finally:
        event.remove(pool, "checkout", checkout)
        event.remove(native_engine, "engine_connect", engine_connect)
        event.remove(native_engine, "do_connect", connection_attempt)


def _check_pooled_connection_control(observed):
    assert observed["events"].count("checkout") == 2
    assert observed["events"].count("engine_connect") == 2
    identities = observed["checkout_identities"]
    assert len(identities) == 2 and identities[0] == identities[1]


def _setup(app, engine, native_engine):
    statements = []

    def sql_attempt(*args, **kwargs):
        statements.append("sql")

    before = tuple(sorted(
        (id(mapper), mapper.configured, id(mapper.local_table),
         tuple((id(column), id(column.type)) for column in mapper.local_table.columns))
        for mapper in app.mapping.mappers
    ))
    event.listen(native_engine, "before_cursor_execute", sql_attempt)
    try:
        with _observe_connections(native_engine) as observed:
            report = doctor(
                json.dumps(app.plan.document["lock"]["declaration"]).encode(),
                phase="setup", mapping=app.mapping, engine=engine,
            )
    finally:
        event.remove(native_engine, "before_cursor_execute", sql_attempt)
    after = tuple(sorted(
        (id(mapper), mapper.configured, id(mapper.local_table),
         tuple((id(column), id(column.type)) for column in mapper.local_table.columns))
        for mapper in app.mapping.mappers
    ))
    assert observed == {"events": [], "checkout_identities": []}
    assert statements == []
    assert before == after
    assert report["ready"] is False and report["complete"] is False
    assert report["effects"] == "NONE"
    for check in ("native_admission", "deployment", "roles", "provider", "ciphertext"):
        assert report["checks"][check]["status"] == "NOT_INSPECTED"
    setup = report["checks"]["setup"]
    assert setup["status"] == "CHECKED"
    assert "_experimental" not in setup["template"]
    return setup


def _host_objects(app, engine):
    assert app.pin.phase == "ACTIVE"
    return {
        "existing_registry": app.mapping,
        "existing_runtime_engine": engine,
        "trusted_lock_bytes": app.plan.lock_bytes,
        "existing_key_resolver": keys,
        "current_plan": app.plan,
        "current_active_pin": app.pin,
        "authenticated_tenant_id": TENANT,
    }


def _check_observation(native, protected):
    # Native plaintext is the collector's positive sensitivity control.
    assert native["calls"] > 0 and native["protected_literal_seen"] is True
    assert protected["calls"] > 0 and protected["protected_literal_seen"] is False


def _exercise_sync(app):
    # Two public acquisitions must observe the same pooled DBAPI identity.
    # A custom creator can also bypass do_connect on a fresh connection.
    with _observe_connections(app.runtime) as observed:
        with app.runtime.connect():
            pass
        with app.runtime.connect():
            pass
    _check_pooled_connection_control(observed)
    setup = _setup(app, app.runtime, app.runtime)
    assert setup["engine"]["mode"] == "sync"
    with _observe_query_binds(app.runtime) as native:
        with sessionmaker(app.runtime)() as session:
            before = [_values(session.execute(statement, parameters))
                      for statement, parameters in _queries(app.Customer)]
    assert before == _expected()
    assert run(app).phase == "PENDING"
    publish(app)
    namespace = _host_objects(app, app.runtime)
    # Execute the public, fixed emitted text unchanged, with the real attach.
    exec(compile(setup["template"], "<reviewed-setup-template>", "exec"), namespace)
    with _observe_query_binds(app.runtime) as protected:
        with namespace["sessions"](tenant_id=TENANT) as session:
            after = [_values(session.execute(statement, parameters))
                     for statement, parameters in _queries(app.Customer)]
    assert after == before == _expected()
    _check_observation(native, protected)


async def _exercise_async(app):
    engine = create_async_engine(
        "postgresql+psycopg://", echo=False, hide_parameters=True,
        async_creator=lambda: psycopg.AsyncConnection.connect(
            os.environ["CRYPTALIS_TEST_RUNTIME_DATABASE_URL"]),
    )
    try:
        with _observe_connections(engine.sync_engine) as observed:
            async with engine.connect():
                pass
            async with engine.connect():
                pass
        _check_pooled_connection_control(observed)
        setup = _setup(app, engine, engine.sync_engine)
        assert setup["engine"]["mode"] == "async"
        with _observe_query_binds(engine.sync_engine) as native:
            async with async_sessionmaker(engine)() as session:
                before = [_values(await session.execute(statement, parameters))
                          for statement, parameters in _queries(app.Customer)]
        assert before == _expected()
        await engine.dispose()
        assert run(app).phase == "PENDING"
        publish(app)
        namespace = _host_objects(app, engine)
        # Only the required async function wrapper and factory return are added.
        # The emitted body, real attach, and native session contexts are unchanged.
        source = ("async def bootstrap():\n"
                  + textwrap.indent(setup["template"], "    ")
                  + "    return sessions\n")
        exec(compile(source, "<reviewed-async-setup-template>", "exec"), namespace)
        factory = await namespace["bootstrap"]()
        with _observe_query_binds(engine.sync_engine) as protected:
            async with factory(tenant_id=TENANT) as session:
                after = [_values(await session.execute(statement, parameters))
                         for statement, parameters in _queries(app.Customer)]
        assert after == before == _expected()
        _check_observation(native, protected)
    finally:
        await engine.dispose()


@pytest.mark.parametrize("mode", ["sync", "async"])
def test_emitted_setup_template_preserves_activated_native_equality_and_in(mode):
    with application(rows=7) as app:
        if mode == "sync":
            _exercise_sync(app)
        else:
            asyncio.run(_exercise_async(app))

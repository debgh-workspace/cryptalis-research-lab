"""Native-only provenance observations. No protected admission or sealing.

Private SQLAlchemy monkeypatches are test-scoped observers, not runtime hooks.
Run only through unchanged scripts/test_postgres.py; coordinator owns DB runs.
"""
import asyncio
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import sys
from pathlib import Path

import sqlalchemy
from dataclasses import dataclass, field
from uuid import UUID

import pytest
from sqlalchemy import event, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import persistence
from sqlalchemy.orm.attributes import NO_VALUE
from sqlalchemy.sql.compiler import SQLCompiler

import test_sqlalchemy_client_default_boundary as native


EXPECTED_SQLALCHEMY_SOURCES = {'2.1.3': {'__init__.py': 'a9adec906730591e19e14ee9c76406d0e03e9ca0063472f0b09f6affd939d802', 'orm/persistence.py': '99788cd676a4fa3fa34c2b6c2b0f57e18a563f365c730c1e0f28a9b058778055', 'orm/dependency.py': '82a514262ecb305d91204beaee1c3fc3e59f6e95bc097cd26835b94135b93654', 'orm/sync.py': '8f5bf983433fd3f7122a2bfa5047a4f8384f5802fd792a5ce2163d675e1cf7cf', 'orm/events.py': '7e20d9472377fa292391010eca9b800e591cfc96fd35764475dff02008a292b2', 'engine/base.py': 'de49e59123dd4e6118784c1b82415127f120a8ad38ef86973ab5fc28605378d9', 'engine/default.py': '9a92107da1c58688d84c9b8c9b15a936fb6fad94d8c9b8e36690bf169e5e7958', 'sql/compiler.py': 'd862c8095e1ee74e98eb9b6e8942e98235974d2c0ee8b318c472fc8e7b46d62e'}, '2.0.51': {'__init__.py': '585a8f5acb190fc9789f4bcf821b8b53adf57bbc27344f52bcf8f6bcecaad5a5', 'orm/persistence.py': 'dd62e385ef70b3c0bc0fa9497085768c03a33418f623cc02433980d6249f9c2f', 'orm/dependency.py': '0e4bed2a0bc8c6a622403826bffd15ac315a6db40b28821a5bdbd011a16d91a2', 'orm/sync.py': 'df2726b160072b8cf051fbdf5e3d9ee2fe7c333990f4a50b5b2e1ac281b3a0c2', 'orm/events.py': '8386df91c26c4459e3cb37d61f143ce21d8608d3c72912f95f439e40137a1d24', 'engine/base.py': '53f38e544004d329ac38e243104bf4bbbaf7d0f0cecabd112b1923b78dde5614', 'engine/default.py': '43886cde55bc6ec1da223a20319c811f8d46a81282c60455691df2cb632a0c2f', 'sql/compiler.py': 'bc6ed1aafad01f1cfba799a285340021f2d0b7638a1e745eee9b494cd2bc627b'}}


def verify_observer_sources():
    version = sqlalchemy.__version__
    assert version in EXPECTED_SQLALCHEMY_SOURCES, "Unqualified SQLAlchemy version"
    source_root = Path(sqlalchemy.__file__).resolve().parent
    for relative, expected in EXPECTED_SQLALCHEMY_SOURCES[version].items():
        assert hashlib.sha256((source_root / relative).read_bytes()).hexdigest() == expected, relative
    tests_root = Path(__file__).resolve().parent
    assert Path(native.__file__).resolve() == tests_root / "test_sqlalchemy_client_default_boundary.py"
    assert Path(native.maybe.__code__.co_filename).resolve() == Path(native.__file__).resolve()
    migration = sys.modules[native.engine.__module__]
    assert Path(migration.__file__).resolve() == tests_root / "test_migration.py"
    assert Path(native.engine.__code__.co_filename).resolve() == Path(migration.__file__).resolve()
    for relative, expected in {'test_sqlalchemy_client_default_boundary.py': 'b12997edabab634c01c8b26f8f946392a70503d55389fa6cd826f979b33535e2', 'test_migration.py': '978775974fbd4bdd9447791fc89c1b0b2b99916c3937c1ea82d116afac9aa60e'}.items():
        assert hashlib.sha256((tests_root / relative).read_bytes()).hexdigest() == expected, relative


@dataclass
class RowTrace:
    uow: object
    state: object
    state_dict: dict
    mapper: object
    table: object
    connection: object
    input: dict
    initial: dict
    statement: object = None
    invocation: object = None
    compiled: object = None
    context: object = None
    completed_defaults: object = None
    default_failure: object = None
    postfetches: int = 0


@dataclass
class Emission:
    uow: object
    table: object
    rows: list = field(default_factory=list)


class NativeLineage:
    def __init__(self):
        self.active = ContextVar('synthetic_native_lineage', default=None)
        self.rows = []
        self.emissions = []
        self.finished = []
        self.defaults = []
        self.unassociated = []

    def exact_input(self, value):
        emission = self.active.get()
        if emission is None:
            return None
        matches = [row for row in emission.rows if row.input is value]
        assert len(matches) <= 1
        return matches[0] if matches else None

    def exact_compiled(self, value):
        emission = self.active.get()
        if emission is None:
            return None
        matches = [row for row in emission.rows if row.compiled is value]
        assert len(matches) <= 1
        return matches[0] if matches else None

    def associate_context(self, context):
        rows = []
        for group in context.compiled_parameters:
            row = self.exact_compiled(group)
            if row is None:
                continue
            assert row.context is None or row.context is context
            assert context.root_connection is row.connection
            assert context.invoked_statement is row.statement
            assert context.compiled.statement.table is row.table
            assert row.invocation is not None
            assert row.uow.session._contains_state(row.state)
            assert row.state in row.uow.states
            assert row.state.dict is row.state_dict
            row.context = context
            rows.append(row)
        return rows

    def check(self):
        assert self.active.get() is None
        assert len(self.emissions) == len(self.finished)
        assert self.rows
        assert all(row.compiled is not None for row in self.rows)
        assert all(row.context is not None for row in self.rows)
        # Strong references plus `is`, never value-only or integer-id matching.
        for row in self.rows:
            assert row.compiled is not row.input
            assert row.input == row.initial
            assert all(type(row.compiled[key]) is str for key in ('name', 'label')
                       if row.compiled.get(key) is not None)
            assert row.postfetches in (0, 1)
            if row.postfetches:
                assert row.compiled == row.completed_defaults


@pytest.fixture
def lineage(monkeypatch):
    verify_observer_sources()
    trace = NativeLineage()
    emit = persistence._emit_insert_statements
    construct = SQLCompiler.construct_params
    defaults = DefaultExecutionContext._process_execute_defaults
    postfetch = persistence._postfetch

    def observed_emit(base_mapper, uowtransaction, mapper, table, insert, **kwargs):
        emission = Emission(uowtransaction, table)
        trace.emissions.append(emission)
        token = trace.active.set(emission)

        def observed_records():
            # Native consumption remains lazy. Never materialize/reorder early.
            for record in insert:
                state, state_dict, params, mapper_rec, connection = record[:5]
                assert state is not None  # this test selects ordinary UOW only
                assert state.dict is state_dict
                assert state in uowtransaction.states
                row = RowTrace(uowtransaction, state, state_dict, mapper_rec,
                               table, connection, params, dict(params))
                emission.rows.append(row)
                trace.rows.append(row)
                yield record  # exact original tuple, dictionary and values

        try:
            return emit(base_mapper, uowtransaction, mapper, table,
                        observed_records(), **kwargs)
        finally:
            trace.finished.append(emission)
            trace.active.reset(token)

    def observed_before_execute(connection, statement, multiparams, params, options):
        invocation = object()
        for group in multiparams if multiparams else [params]:
            row = trace.exact_input(group)
            if row is not None:
                assert row.connection is connection
                assert row.statement is None and row.invocation is None
                assert statement.table is row.table
                row.statement = statement
                row.invocation = invocation

    def observed_construct(self, params=None, *args, **kwargs):
        row = trace.exact_input(params)
        result = construct(self, params, *args, **kwargs)
        if row is not None:
            assert row.compiled is None
            assert trace.exact_input(dict(params)) is None
            row.compiled = result  # exact return, no copied/reordered ledger
        elif trace.active.get() is not None:
            trace.unassociated.append((params, result))
        return result

    def observed_defaults(self):
        rows = trace.associate_context(self)
        if rows:
            assert len(rows) == len(self.compiled_parameters)
            for row in rows:
                if 'id' not in row.initial:
                    assert inspect(row.state.obj()).attrs.id.loaded_value is NO_VALUE
                assert type(row.compiled['name']) is str
        try:
            result = defaults(self)  # one untouched native default dispatch
        except BaseException as failure:
            for row in rows:
                row.default_failure = type(failure)
            trace.defaults.append(('failed', self, tuple(rows)))
            raise
        else:
            for row in rows:
                row.completed_defaults = dict(row.compiled)
                if 'id' not in row.initial:
                    assert inspect(row.state.obj()).attrs.id.loaded_value is NO_VALUE
            trace.defaults.append(('complete', self, tuple(rows)))
            return result

    def observed_postfetch(mapper, uow, table, state, state_dict, result,
                           params, *args, **kwargs):
        row = trace.exact_compiled(params)
        assert row is not None
        trace.associate_context(result.context)
        assert row.state is state and row.state_dict is state_dict
        assert row.uow is uow and row.table is table and row.mapper is mapper
        assert row.context is result.context
        if row.completed_defaults is None:
            # Explicit-ID/no-default execution may never call the default loop.
            row.completed_defaults = dict(params)
        assert params == row.completed_defaults
        before = dict(params)
        returned = postfetch(mapper, uow, table, state, state_dict, result,
                             params, *args, **kwargs)
        assert params == before
        assert state_dict['id'] == params['id']
        assert type(state_dict['name']) is str
        row.postfetches += 1
        return returned

    monkeypatch.setattr(persistence, '_emit_insert_statements', observed_emit)
    monkeypatch.setattr(SQLCompiler, 'construct_params', observed_construct)
    monkeypatch.setattr(DefaultExecutionContext, '_process_execute_defaults', observed_defaults)
    monkeypatch.setattr(persistence, '_postfetch', observed_postfetch)
    event.listen(Engine, 'before_execute', observed_before_execute)
    try:
        yield trace
    finally:
        event.remove(Engine, 'before_execute', observed_before_execute)
    # pytest monkeypatch restores all four methods, including failed tests.


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('callback_kind', ['noarg', 'context'])
def test_native_lineage_preserves_a5_success_and_explicit_suppression(lineage, mode, callback_kind):
    native.test_native_client_uuid_default_phase_and_explicit_id_suppression(mode, callback_kind)
    lineage.check()
    assert len(lineage.rows) == 3
    assert all(row.postfetches == 1 for row in lineage.rows)
    assert sum('id' not in row.initial for row in lineage.rows) == 2
    assert not lineage.unassociated
    for row in lineage.rows:
        assert row.state_dict['id'] == row.compiled['id']


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('failure', ['callback', 'constraint'])
def test_native_lineage_preserves_a5_error_and_retry(lineage, mode, failure):
    native.test_native_failed_client_default_batch_preserves_unassigned_ids_and_retries(mode, failure)
    lineage.check()
    assert len(lineage.rows) == 4
    failed = [row for row in lineage.rows if row.postfetches == 0]
    succeeded = [row for row in lineage.rows if row.postfetches == 1]
    assert len(failed) == len(succeeded) == 2
    assert not lineage.unassociated
    for row in succeeded:
        prior = [old for old in failed if old.state is row.state]
        assert len(prior) == 1
        assert prior[0].uow is not row.uow
        assert prior[0].input is not row.input
        assert prior[0].compiled is not row.compiled
        assert prior[0].context is not row.context
    if failure == 'callback':
        assert all(row.default_failure is native.SyntheticDefaultFailure for row in failed)
    else:
        assert all(row.default_failure is None for row in failed)
        assert {row.compiled['id'] for row in failed}.isdisjoint(
            row.compiled['id'] for row in succeeded)


@contextmanager
def observe_mixed_boundary(app, session, target, lineage, implicit, explicit):
    tracking = app.tracking
    sync_session = getattr(session, 'sync_session', session)
    seen = []

    def before_flush(*args):
        tracking.trace.append('before_flush')

    def before_insert(*args):
        tracking.trace.append('before_insert')

    def before_execute(connection, statement, multiparams, params, options):
        if getattr(statement, 'is_insert', False):
            tracking.trace.append('before_execute')

    def before_cursor(connection, cursor, statement, parameters, context, many):
        if not context.isinsert:
            return
        tracking.trace.append('before_cursor')
        tracking.cursor.append(parameters)
        current = [lineage.exact_compiled(group) for group in context.compiled_parameters]
        assert current and all(row is not None for row in current)
        for row in current:
            assert row.context is context or row.context is None
            assert row.postfetches == 0
            if row.state is inspect(explicit):
                assert row.initial['id'] == UUID(int=9999)
                assert inspect(explicit).attrs.id.loaded_value == UUID(int=9999)
                assert row.compiled['id'] == UUID(int=9999)
            else:
                assert any(row.state is inspect(obj) for obj in implicit)
                assert 'id' not in row.initial
                assert row.state.attrs.id.loaded_value is NO_VALUE
                assert type(row.compiled['id']) is UUID
            seen.append(row.state)
        # Earlier contexts may have successfully assigned IDs already. Their
        # exact producer records, rather than a blanket all-rows check, decide.
        for obj in implicit:
            prior = [row for row in lineage.rows
                     if row.state is inspect(obj) and row.postfetches == 1]
            if prior:
                assert len(prior) == 1
                assert obj.id == prior[0].compiled['id']

    registrations = [(sync_session, 'before_flush', before_flush),
                     (app.Customer, 'before_insert', before_insert),
                     (target, 'before_execute', before_execute),
                     (target, 'before_cursor_execute', before_cursor)]
    for subject, name, callback in registrations:
        event.listen(subject, name, callback)
    try:
        yield
        assert len(seen) == 3
        assert all(sum(state is inspect(obj) for state in seen) == 1
                   for obj in [*implicit, explicit])
    finally:
        for subject, name, callback in reversed(registrations):
            event.remove(subject, name, callback)


@pytest.mark.parametrize('mode', ['sync', 'async'])
def test_native_lineage_equal_rows_mixed_ids_preserves_exact_state(lineage, mode):
    with native.default_application('context') as app:
        async def scenario():
            factory, target, asynchronous = await native.make_factory(app, mode)
            session = factory(expire_on_commit=False)
            try:
                implicit = [app.Customer(tenant_id=native.TENANT, name='synthetic equal',
                                        label='equal') for _ in range(2)]
                explicit = app.Customer(id=UUID(int=9999), tenant_id=native.TENANT,
                                        name='synthetic equal', label='equal')
                app.tracking.rows = implicit
                session.add_all([*implicit, explicit])
                with observe_mixed_boundary(app, session, target, lineage, implicit, explicit):
                    await native.maybe(session.flush())
                assert len(app.tracking.calls) == 2
                for obj in [*implicit, explicit]:
                    rows = [row for row in lineage.rows if row.state is inspect(obj)]
                    assert len(rows) == 1
                    row = rows[0]
                    assert row.compiled['id'] == obj.id
                    assert row.postfetches == 1
                await native.maybe(session.commit())
                observed = {identity: (tenant, name, label)
                            for identity, tenant, name, label in native.row_values(app)}
                assert observed == {obj.id: (native.TENANT, obj.name, obj.label)
                                    for obj in [*implicit, explicit]}
            finally:
                await native.maybe(session.close())
                assert target.pool.checkedout() == 0
                if asynchronous is not None:
                    await asynchronous.dispose()
        asyncio.run(scenario())
    lineage.check()
    assert len(lineage.rows) == 3
    assert not lineage.unassociated

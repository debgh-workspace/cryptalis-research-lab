"""Native-only provenance observations. No protected admission or sealing.

Private SQLAlchemy monkeypatches are test-scoped observers, not runtime hooks.
Run only through unchanged scripts/test_postgres.py; coordinator owns DB runs.
"""
import asyncio
from contextvars import ContextVar
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
                with native.observe_native_boundary(app, session, target):
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

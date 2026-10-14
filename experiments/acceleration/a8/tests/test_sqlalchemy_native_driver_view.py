"""Exact native receipts drive a NEW synthetic driver-only TEXT view.

Test-only fork research. No cryptography, protected admission or product hook.
"""
import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
from pathlib import Path

import pytest
from sqlalchemy import event, inspect
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm.attributes import NO_VALUE

import native_slot_probes as slot_module
import test_sqlalchemy_native_slot_probes as slot_tests
import test_sqlalchemy_client_default_boundary as native
from test_sqlalchemy_native_uow_lineage import lineage


class SyntheticViewFailure(Exception):
    pass


@dataclass
class ViewReceipt:
    native: object
    original: object
    snapshot: object
    output: object
    states: tuple
    logical_snapshots: tuple
    driver_snapshots: tuple


def snapshot(value):
    return dict(value) if isinstance(value, dict) else tuple(value)


def verify_view_dependencies():
    directory = Path(__file__).resolve().parent
    expected = {
        'native_slot_probes.py': '555bc8c6a95a9785dd5c57a3106c631fe71981b1a42bb0ff6c1c5242a2814fc5',
        'test_sqlalchemy_native_slot_probes.py': '738914f67e38d7d40737e4e32929481a1aa0d9881cb04e4c7a0d2f2213bf99e7',
    }
    for module in (slot_module, slot_tests):
        path = Path(module.__file__).resolve()
        assert path.parent == directory
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected[path.name]
    assert Path(slot_tests.factory_for_style.__code__.co_filename).resolve().parent == directory


@contextmanager
def retain_actual_callback_parameters(monkeypatch, lineage):
    original = DefaultExecutionContext.get_current_parameters
    retained = []

    def observe(context, *args, **kwargs):
        values = original(context, *args, **kwargs)
        row = lineage.exact_compiled(values)
        assert row is not None
        assert values is context.current_parameters
        assert context.current_column is row.table.c.id
        retained.append((context, values, dict(values), row))
        return values  # exact object delivered to unchanged native UUID callback

    with monkeypatch.context() as patch:
        patch.setattr(DefaultExecutionContext, 'get_current_parameters', observe)
        yield retained


def check_retained(retained):
    for context, values, before, row in retained:
        assert values is row.compiled and row.context is context
        assert {key: value for key, value in values.items() if key != 'id'} == {
            key: value for key, value in before.items() if key != 'id'}
        assert values['label'] == row.initial['label']
        assert type(values['name']) is str


class DriverView:
    def __init__(self, probe, projected, failure_state=None):
        self.probe = probe
        self.projected = projected
        self.failure_state = failure_state
        self.views = []
        self.observed = []
        self.failures = 0

    def before_cursor(self, connection, cursor, statement, parameters, context, many):
        if not context.isinsert:
            return statement, parameters
        native_receipt = self.probe.pending
        # Reuse the proven exact-container/statement/slot validator unchanged.
        self.probe.before_cursor(connection, cursor, statement, parameters, context, many)
        assert native_receipt is not None
        replacement = dict(parameters) if isinstance(parameters, dict) else list(parameters)
        states, logical_snapshots, driver_snapshots = [], [], []
        touched = set()
        for _, _, source, source_slot, output_slot, _ in native_receipt.slots:
            driver = self.probe.exact_driver(source)
            origins = [slot for slot in driver.slots if slot[3] == source_slot]
            assert len(origins) == 1
            origin = origins[0]
            logical = origin[1]
            assert logical is driver.row.compiled
            assert driver.context is context and driver.row.context is context
            if origin[2] != 'label':
                continue
            assert output_slot not in touched
            touched.add(output_slot)
            state = driver.row.state
            assert state.dict is driver.row.state_dict
            assert state.attrs.id.loaded_value is NO_VALUE
            states.append(state)
            logical_snapshots.append((logical, dict(logical)))
            driver_snapshots.append((source, snapshot(source)))
            if self.failure_state is state:
                self.failures += 1
                raise SyntheticViewFailure('owned synthetic local driver-view failure')
            value = logical['label']
            if self.projected and value is not None:
                replacement[output_slot] = ('synthetic-driver-view|' + str(logical['id'])
                    + '|' + str(logical['tenant_id']) + '|' + value)
        assert len(touched) == native_receipt.batch.current_batch_size
        if self.projected:
            output = replacement if isinstance(parameters, dict) else tuple(replacement)
            assert output is not parameters
        else:
            output = parameters
        self.views.append(ViewReceipt(native_receipt, parameters, snapshot(parameters), output,
                                      tuple(states), tuple(logical_snapshots), tuple(driver_snapshots)))
        self.check_originals()
        return statement, output

    def after_transform_observer(self, connection, cursor, statement, parameters, context, many):
        if context.isinsert:
            assert self.views
            view = self.views[-1]
            assert view.native.context is context
            assert parameters is view.output
            self.observed.append(view)
            self.check_originals()

    def check_originals(self):
        for view in self.views:
            assert view.native.batch.replaced_parameters is view.original
            assert view.original == view.snapshot
            for logical, original in view.logical_snapshots:
                assert logical == original
            for driver, original in view.driver_snapshots:
                assert driver == original


def assert_persisted(app, rows, projected):
    found = {identity: (tenant, name, label)
             for identity, tenant, name, label in native.row_values(app)}
    assert set(found) == {row.id for row in rows}
    for row in rows:
        tenant, name, label = found[row.id]
        assert tenant == native.TENANT and name == row.name
        if projected:
            # Independent owner read; do not call the transformation function
            # or derive expected context from its receipt/slot order.
            parts = label.split('|', 3)
            assert parts == ['synthetic-driver-view', str(row.id), str(native.TENANT), row.label]
        else:
            assert label == row.label
    return tuple(sorted((identity, tenant, name) for identity, (tenant, name, _) in found.items()))


async def exercise(lineage, monkeypatch, mode, paramstyle, projected, failure, rewrite=None):
    with native.default_application('context') as app:
        factory, target, asynchronous = await slot_tests.factory_for_style(mode, paramstyle)
        session = factory(expire_on_commit=False)
        listeners = []
        try:
            rows = [app.Customer(tenant_id=native.TENANT, name='synthetic equal',
                                 label='logical equal') for _ in range(3)]
            app.tracking.rows = rows
            if failure == 'callback':
                app.tracking.fail_at = 2
            elif failure == 'constraint':
                rows[1].label = None
            session.add_all(rows)
            with slot_module.installed_probes(monkeypatch, lineage) as probe:
                view = DriverView(probe, projected, inspect(rows[2]) if failure == 'local' else None)
                if rewrite is not None:
                    def rewrite_cursor(connection, cursor, statement, parameters, context, many):
                        if not context.isinsert:
                            return statement, parameters
                        if isinstance(parameters, dict):
                            result = dict(parameters)
                            if rewrite == 'reordered_copy':
                                result = dict(reversed(list(result.items())))
                        else:
                            result = tuple(list(parameters))
                            if rewrite == 'reordered_copy':
                                result = tuple(reversed(result))
                        assert result is not parameters
                        return statement, result
                    event.listen(target, 'before_cursor_execute', rewrite_cursor, retval=True)
                    listeners.append(rewrite_cursor)
                event.listen(target, 'before_cursor_execute', view.before_cursor, retval=True)
                listeners.append(view.before_cursor)
                # The only later listener in this controlled chain is read-only.
                event.listen(target, 'before_cursor_execute', view.after_transform_observer)
                listeners.append(view.after_transform_observer)
                with retain_actual_callback_parameters(monkeypatch, lineage) as retained:
                    with native.observe_native_boundary(app, session, target):
                        if failure or rewrite is not None:
                            expected = (slot_module.MissingNativeReceipt if rewrite else
                                        SyntheticViewFailure if failure == 'local' else
                                        StatementError if failure == 'callback' else IntegrityError)
                            with pytest.raises(expected) as caught:
                                await native.maybe(session.flush())
                            if failure == 'callback':
                                assert type(caught.value.orig) is native.SyntheticDefaultFailure
                            elif failure == 'constraint':
                                assert caught.value.orig.sqlstate == '23502'
                        else:
                            await native.maybe(session.flush())
                    initial_calls = len(app.tracking.calls)
                    check_retained(retained)
                    view.check_originals()
                    if failure or rewrite is not None:
                        assert not session.is_active and session.in_transaction()
                        assert all(inspect(row).transient and inspect(row).identity is None
                                   and inspect(row).attrs.id.loaded_value is NO_VALUE for row in rows)
                        assert native.row_values(app) == []
                        if failure == 'callback':
                            assert not view.views and not view.observed
                        elif failure == 'local':
                            # The first native two-row batch reached the cursor;
                            # failure for the exact third state occurs before its
                            # second batch reaches the read-only final observer.
                            assert view.failures == 1 and len(view.observed) == 1
                            assert all(state is not inspect(rows[2]) for state in view.observed[0].states)
                        await native.maybe(session.rollback())
                        assert session.is_active and not session.in_transaction()
                        if rewrite is not None:
                            assert not view.views and not view.observed
                            return {'rewrite': rewrite, 'callbacks': initial_calls}
                        app.tracking.fail_at = None
                        view.failure_state = None
                        rows[1].label = 'logical equal'
                        session.add_all(rows)
                        with native.observe_native_boundary(app, session, target):
                            await native.maybe(session.flush())
                    assert len(retained) == len(app.tracking.calls)
                    assert all(inspect(row).persistent and row.label == 'logical equal' for row in rows)
                    assert {row.id for row in rows} == {value for value, _ in app.tracking.calls[-3:]}
                    assert len(view.observed) >= 2
                    assert {receipt.native.batch.current_batch_size for receipt in view.observed} == {1, 2}
                    check_retained(retained)
                    view.check_originals()
                    await native.maybe(session.commit())
                    identities = assert_persisted(app, rows, projected)
                    check_retained(retained)
                    view.check_originals()
                    assert probe.pending is None
                    return {'initial_calls': initial_calls, 'all_calls': tuple(app.tracking.calls),
                            'row_identities': identities, 'logical_labels': tuple(row.label for row in rows),
                            'local_failures': view.failures}
        finally:
            for listener in reversed(listeners):
                event.remove(target, 'before_cursor_execute', listener)
            await native.maybe(session.close())
            assert target.pool.checkedout() == 0
            if asynchronous is not None:
                await asynchronous.dispose()
            else:
                target.dispose()
            assert lineage.active.get() is None


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('paramstyle', ['pyformat', 'format'], ids=['named', 'positional'])
@pytest.mark.parametrize('failure', [None, 'callback', 'constraint', 'local'],
                         ids=['success', 'callback_retry', 'constraint_retry', 'local_retry'])
def test_driver_view_preserves_native_logical_state_and_callback_references(lineage, monkeypatch, mode, paramstyle, failure):
    verify_view_dependencies()
    async def scenario():
        original = await exercise(lineage, monkeypatch, mode, paramstyle, False, failure)
        projected = await exercise(lineage, monkeypatch, mode, paramstyle, True, failure)
        assert projected == original
    asyncio.run(scenario())
    lineage.check()
    assert not lineage.unassociated


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('paramstyle', ['pyformat', 'format'], ids=['named', 'positional'])
@pytest.mark.parametrize('rewrite', ['equal_copy', 'reordered_copy'])
def test_driver_view_refuses_prior_rewrite_without_value_matching(lineage, monkeypatch, mode, paramstyle, rewrite):
    verify_view_dependencies()
    result = asyncio.run(exercise(lineage, monkeypatch, mode, paramstyle, True, None, rewrite))
    assert result == {'rewrite': rewrite, 'callbacks': 3}
    assert all(row.postfetches == 0 for row in lineage.rows)

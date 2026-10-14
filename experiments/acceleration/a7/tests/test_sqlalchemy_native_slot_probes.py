"""Native differential probes for actual driver/IMV slot creation.

Only synthetic plain TEXT. Coordinator alone runs the PostgreSQL wrapper.
"""
import asyncio
from contextlib import nullcontext
import os

import psycopg
import pytest
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import NO_VALUE
from sqlalchemy.sql.compiler import SQLCompiler

import test_sqlalchemy_client_default_boundary as native
from test_sqlalchemy_native_uow_lineage import lineage
from native_slot_probes import MissingNativeReceipt, installed_probes


async def factory_for_style(mode, paramstyle):
    options = dict(paramstyle=paramstyle, hide_parameters=True, insertmanyvalues_page_size=2)
    if mode == 'async':
        engine = create_async_engine('postgresql+psycopg://',
            async_creator=lambda: psycopg.AsyncConnection.connect(
                os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']), **options)
        return async_sessionmaker(engine), engine.sync_engine, engine
    engine = create_engine('postgresql+psycopg://',
        creator=lambda: psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']), **options)
    return sessionmaker(engine), engine, None


async def exercise(lineage, monkeypatch, mode, paramstyle, failure, instrumented, rewrite=None):
    first_row = len(lineage.rows)
    with native.default_application('context') as app:
        factory, target, asynchronous = await factory_for_style(mode, paramstyle)
        session = factory(expire_on_commit=False)
        original_context = DefaultExecutionContext._init_compiled.__func__
        original_imv = SQLCompiler._deliver_insertmanyvalues_batches
        probe = None
        registered = []
        try:
            rows = [app.Customer(tenant_id=native.TENANT, name='synthetic equal',
                                 label='equal label') for _ in range(3)]
            app.tracking.rows = rows
            if failure == 'callback':
                app.tracking.fail_at = 2
            elif failure == 'constraint':
                rows[1].label = None
            session.add_all(rows)
            scope = installed_probes(monkeypatch, lineage) if instrumented else nullcontext(None)
            with scope as probe:
                if rewrite is not None:
                    def rewrite_cursor(connection, cursor, statement, parameters, context, many):
                        if not context.isinsert:
                            return statement, parameters
                        if isinstance(parameters, dict):
                            copied = dict(parameters)
                            if rewrite == 'reordered_copy':
                                copied = dict(reversed(list(copied.items())))
                        else:
                            copied = tuple(list(parameters))
                            if rewrite == 'reordered_copy':
                                copied = tuple(reversed(copied))
                        assert copied is not parameters
                        return statement, copied
                    event.listen(target, 'before_cursor_execute', rewrite_cursor, retval=True)
                    registered.append(('before_cursor_execute', rewrite_cursor))
                if probe is not None:
                    event.listen(target, 'before_cursor_execute', probe.before_cursor)
                    registered.append(('before_cursor_execute', probe.before_cursor))
                with native.observe_native_boundary(app, session, target):
                    if rewrite is not None:
                        with pytest.raises(MissingNativeReceipt):
                            await native.maybe(session.flush())
                    elif failure:
                        with pytest.raises(StatementError if failure == 'callback' else IntegrityError) as caught:
                            await native.maybe(session.flush())
                        if failure == 'callback':
                            assert type(caught.value.orig) is native.SyntheticDefaultFailure
                        else:
                            assert caught.value.orig.sqlstate == '23502'
                    else:
                        await native.maybe(session.flush())
                if failure or rewrite is not None:
                    assert not session.is_active and session.in_transaction()
                    assert all(inspect(row).transient and inspect(row).identity is None
                               and inspect(row).attrs.id.loaded_value is NO_VALUE for row in rows)
                    assert native.row_values(app) == []
                    first_attempt_calls = len(app.tracking.calls)
                    await native.maybe(session.rollback())
                    assert session.is_active and not session.in_transaction()
                    if rewrite is not None:
                        assert probe is not None and not probe.cursor_calls
                        return {'refused_rewrite': rewrite, 'callbacks': first_attempt_calls}
                    app.tracking.fail_at = None
                    rows[1].label = 'equal label'
                    session.add_all(rows)
                    with native.observe_native_boundary(app, session, target):
                        await native.maybe(session.flush())
                else:
                    first_attempt_calls = len(app.tracking.calls)
                assert all(inspect(row).persistent for row in rows)
                assert all(row.name == 'synthetic equal' and row.label == 'equal label' for row in rows)
                await native.maybe(session.commit())
                persisted = sorted(native.row_values(app), key=lambda row: row[0])
                assert persisted == sorted([(row.id, native.TENANT, row.name, row.label)
                                            for row in rows], key=lambda row: row[0])
                if probe is not None:
                    assert probe.cursor_calls and probe.batches
                    assert probe.pending is None and not probe.bind_slots and not probe.imv_slots
                    # At least one genuine two-row batch and one final one-row
                    # batch: producer receipts, not an inferred event counter.
                    sizes = {receipt.batch.current_batch_size for receipt in probe.cursor_calls}
                    assert sizes == {1, 2}
                    assert all(receipt.context.compiled.positional == (paramstyle == 'format')
                               for receipt in probe.cursor_calls)
                    for receipt in probe.cursor_calls:
                        mapped_states = [probe.exact_driver(driver).row.state
                                         for driver in receipt.batch.batch]
                        assert len({id(state) for state in mapped_states}) == len(mapped_states)
                return {'initial_calls': first_attempt_calls,
                        'all_calls': tuple(app.tracking.calls), 'persisted': persisted,
                        'state_identity': tuple(row.id for row in rows),
                        'logical_labels': tuple(row.label for row in rows)}
        finally:
            for event_name, listener in reversed(registered):
                event.remove(target, event_name, listener)
            assert DefaultExecutionContext._init_compiled.__func__ is original_context
            assert SQLCompiler._deliver_insertmanyvalues_batches is original_imv
            await native.maybe(session.close())
            assert target.pool.checkedout() == 0
            if asynchronous is not None:
                await asynchronous.dispose()
            else:
                target.dispose()
            assert lineage.active.get() is None
            # Provenance objects are retained for evidence, not live authorization.
            assert all(row.input == row.initial for row in lineage.rows[first_row:])


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('paramstyle', ['pyformat', 'format'], ids=['named', 'positional'])
@pytest.mark.parametrize('failure', [None, 'callback', 'constraint'], ids=['success', 'callback_retry', 'constraint_retry'])
def test_source_probes_preserve_original_native_outcomes(lineage, monkeypatch, mode, paramstyle, failure):
    async def scenario():
        original = await exercise(lineage, monkeypatch, mode, paramstyle, failure, False)
        instrumented = await exercise(lineage, monkeypatch, mode, paramstyle, failure, True)
        assert instrumented == original
    asyncio.run(scenario())
    lineage.check()
    assert not lineage.unassociated


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('paramstyle', ['pyformat', 'format'], ids=['named', 'positional'])
@pytest.mark.parametrize('rewrite', ['equal_copy', 'reordered_copy'])
def test_source_probes_refuse_lost_cursor_container_identity(lineage, monkeypatch, mode, paramstyle, rewrite):
    result = asyncio.run(exercise(lineage, monkeypatch, mode, paramstyle, None, True, rewrite))
    assert result == {'refused_rewrite': rewrite, 'callbacks': 3}
    assert lineage.active.get() is None
    assert all(row.postfetches == 0 for row in lineage.rows)

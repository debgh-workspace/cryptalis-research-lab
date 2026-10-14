"""Native expiry/reload behavior for the existing integer-version ORM mapper.

Test-only extension of A3/A4. No default producer, bulk DML or new query grammar.
Coordinator must execute on both pinned PostgreSQL cells before interpretation.
"""
import asyncio

import pytest
from sqlalchemy import inspect

from test_migration import TENANT, publish, run
from test_sqlalchemy_optimistic_versioning import (
    RECORD, factory_for, maybe, storage_snapshot, versioned_application,
)


def public_state(session, row):
    state = inspect(row)
    return (session.is_active, session.in_transaction(),
            session.in_nested_transaction(), row in session,
            state.pending, state.persistent, state.deleted, state.detached,
            state.expired, tuple(sorted(state.expired_attributes)),
            len(session.new), len(session.dirty), len(session.deleted))


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('action', ['update', 'delete'])
@pytest.mark.parametrize('expiry', ['version_only', 'whole_row'])
def test_expired_version_flush_rollback_retry_matches_native(mode, action, expiry):
    observations = []
    for attached in (False, True):
        with versioned_application() as app:
            if attached:
                run(app)
                publish(app)
            baseline = storage_snapshot(app, attached)
            assert baseline[0] == ('initial alpha', 'public unchanged', 1)

            async def scenario():
                factory, async_engine = await factory_for(app, mode, attached)
                options = {'expire_on_commit': False}
                if attached:
                    options['tenant_id'] = TENANT
                session = factory(**options)
                states = []
                try:
                    row = await maybe(session.get(app.Customer, RECORD))
                    assert row.version_id == 1
                    for outcome in ('rollback', 'commit'):
                        # expire is a synchronous public API on both Session types.
                        session.expire(row, ['version_id'] if expiry == 'version_only' else None)
                        assert 'version_id' in inspect(row).expired_attributes
                        states.append(public_state(session, row))
                        if action == 'update':
                            row.name = 'expiry replacement'
                        else:
                            await maybe(session.delete(row))
                        await maybe(session.flush())
                        states.append(public_state(session, row))
                        if action == 'update':
                            assert row.version_id == 2
                        else:
                            assert inspect(row).deleted
                        # Independent reader sees the old committed value/frame.
                        assert storage_snapshot(app, attached) == baseline
                        if outcome == 'rollback':
                            await maybe(session.rollback())
                            states.append(public_state(session, row))
                            assert storage_snapshot(app, attached) == baseline
                            # Explicit I/O: never trigger async attribute lazy I/O.
                            await maybe(session.refresh(row))
                            assert (row.name, row.label, row.version_id) == baseline[0]
                            assert inspect(row).persistent
                        else:
                            await maybe(session.commit())
                            states.append(public_state(session, row))
                    final = storage_snapshot(app, attached)[0]
                    assert final == (('expiry replacement', 'public unchanged', 2)
                                     if action == 'update' else None)
                    async_fresh = factory(**options)
                    try:
                        fresh = await maybe(async_fresh.get(app.Customer, RECORD))
                        if action == 'delete':
                            assert fresh is None
                        else:
                            assert (fresh.name, fresh.label, fresh.version_id) == final
                    finally:
                        await maybe(async_fresh.close())
                    return states, final
                finally:
                    await maybe(session.close())
                    if async_engine is not None:
                        await async_engine.dispose()

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], 'Native/attached expiry-version state differs'

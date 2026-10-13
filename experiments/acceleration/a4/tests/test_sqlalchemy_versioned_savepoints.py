"""Native optimistic-versioning behavior at ordinary SAVEPOINT boundaries.

Integer versioning, protected text, and native Session transactions only. The
oracle neither enables private bulk DML nor asserts hostile-database freshness.
"""
import asyncio
import json
from uuid import UUID

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import StaleDataError

from test_migration import FIELD_ID, TENANT, independent_open, publish, run
from test_sqlalchemy_optimistic_versioning import (
    RECORD, factory_for, maybe, versioned_application,
)


SIBLING = UUID(int=102)
OUTER = UUID(int=103)


def stored_rows(app, attached, *, unlocked_sibling=False):
    """Observe committed values, versions, and frames outside ORM sessions.

The optional lock probe proves that rollback released the sibling row lock
while the loser's outer transaction is still open. The probe never waits.
"""
    payload = '_cryptalis_' + FIELD_ID.hex
    columns = 'id, tenant_id, name, label, version_id'
    if attached:
        columns += f', "{payload}"'
    statement = f'SELECT {columns} FROM "{app.schema}".customer'
    if unlocked_sibling:
        statement += ' WHERE id=%s FOR UPDATE NOWAIT'
        parameters = (SIBLING,)
    else:
        statement += ' ORDER BY id'
        parameters = ()
    with app.owner.begin() as connection:
        rows = connection.exec_driver_sql(statement, parameters).all()
    descriptor = json.loads(app.plan.lock_bytes)['models'][0]['fields'][0]['descriptor']
    decoded, frames = {}, {}
    for identity, tenant, native, label, version, *protected in rows:
        assert tenant == TENANT
        assert type(version) is int
        if attached:
            assert native is None
            frame = bytes(protected[0]) if protected[0] is not None else None
            value = independent_open(frame, descriptor, TENANT, identity)
            frames[identity] = frame
        else:
            value = native
        decoded[identity] = (value, label, version)
    return decoded, frames


def orm_state(session, *rows):
    """Record public state without triggering an expired attribute reload."""
    return (
        session.is_active, session.in_transaction(), session.in_nested_transaction(),
        len(session.new), len(session.dirty), len(session.deleted),
        tuple((row in session, state.persistent, state.pending, state.deleted,
               state.detached, state.expired, tuple(sorted(state.expired_attributes)))
              for row in rows for state in (inspect(row),)),
    )


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('action', ['update', 'delete'])
@pytest.mark.parametrize('outer_outcome', ['commit', 'rollback'])
def test_stale_savepoint_preserves_outer_work_and_native_version_retry(mode, action, outer_outcome):
    """A stale nested flush rolls back just the nested unit and can retry."""
    observations = []
    for attached in (False, True):
        with versioned_application() as app:
            with sessionmaker(app.runtime)() as seed:
                seed.add(app.Customer(id=SIBLING, tenant_id=TENANT,
                    name='sibling initial', label='sibling label'))
                seed.commit()
            if attached:
                run(app)
                publish(app)

            async def scenario():
                factory, async_engine = await factory_for(app, mode, attached)
                options = {'expire_on_commit': False}
                if attached:
                    options['tenant_id'] = TENANT
                winner, loser = factory(**options), factory(**options)
                states = []
                try:
                    stale = await maybe(loser.get(app.Customer, RECORD))
                    sibling = await maybe(loser.get(app.Customer, SIBLING))
                    current = await maybe(winner.get(app.Customer, RECORD))
                    assert (stale.name, stale.version_id) == ('initial alpha', 1)
                    assert (sibling.name, sibling.version_id) == ('sibling initial', 1)
                    current.name = 'winner beta'
                    await maybe(winner.commit())
                    baseline = stored_rows(app, attached)
                    assert baseline[0] == {
                        RECORD: ('winner beta', 'public unchanged', 2),
                        SIBLING: ('sibling initial', 'sibling label', 1),
                    }

                    outer = app.Customer(id=OUTER, tenant_id=TENANT,
                        name='outer survives', label='outer label')
                    loser.add(outer)
                    await maybe(loser.flush())
                    root = loser.get_transaction()
                    assert outer.version_id == 1 and root.is_active
                    nested = await maybe(loser.begin_nested())

                    # A successful protected version bump precedes the stale
                    # flush. It must be undone with the failed nested unit.
                    sibling.name = 'nested discarded'
                    await maybe(loser.flush())
                    assert sibling.version_id == 2
                    if action == 'update':
                        stale.name = 'stale discarded'
                    else:
                        await maybe(loser.delete(stale))
                    with pytest.raises(StaleDataError) as caught:
                        await maybe(loser.flush())
                    assert type(caught.value) is StaleDataError
                    states.append(orm_state(loser, stale, sibling, outer))
                    assert not loser.is_active and not nested.is_active
                    assert root.is_active and loser.in_nested_transaction()

                    # Explicitly close only the failed SAVEPOINT. No full
                    # Session rollback is allowed to hide loss of outer work.
                    await maybe(nested.rollback())
                    assert loser.is_active and root.is_active
                    assert loser.in_transaction() and not loser.in_nested_transaction()
                    assert inspect(outer).persistent and not inspect(outer).expired
                    states.append(orm_state(loser, stale, sibling, outer))
                    assert stored_rows(app, attached) == baseline
                    lock_probe = stored_rows(app, attached, unlocked_sibling=True)
                    assert lock_probe[0] == {SIBLING: baseline[0][SIBLING]}
                    if attached:
                        assert lock_probe[1] == {SIBLING: baseline[1][SIBLING]}

                    # Explicit refresh respects async's ordinary no-implicit-I/O
                    # rule and must restore both native optimistic versions.
                    await maybe(loser.refresh(stale))
                    await maybe(loser.refresh(sibling))
                    assert (stale.name, stale.version_id) == ('winner beta', 2)
                    assert (sibling.name, sibling.version_id) == ('sibling initial', 1)
                    retry = await maybe(loser.begin_nested())
                    sibling.name = 'sibling accepted'
                    if action == 'update':
                        stale.name = 'retry accepted'
                    else:
                        await maybe(loser.delete(stale))
                    await maybe(loser.flush())
                    assert sibling.version_id == 2
                    if action == 'update':
                        assert stale.version_id == 3
                    else:
                        assert inspect(stale).deleted
                    await maybe(retry.commit())
                    assert loser.is_active and root.is_active
                    assert loser.in_transaction() and not loser.in_nested_transaction()
                    states.append(orm_state(loser, stale, sibling, outer))

                    if outer_outcome == 'commit':
                        await maybe(loser.commit())
                        expected = {
                            SIBLING: ('sibling accepted', 'sibling label', 2),
                            OUTER: ('outer survives', 'outer label', 1),
                        }
                        if action == 'update':
                            expected[RECORD] = ('retry accepted', 'public unchanged', 3)
                    else:
                        await maybe(loser.rollback())
                        expected = baseline[0]
                    assert loser.is_active and not loser.in_transaction()
                    states.append(orm_state(loser, stale, sibling, outer))
                    final = stored_rows(app, attached)
                    assert final[0] == expected
                    if outer_outcome == 'rollback':
                        assert final == baseline
                    elif attached:
                        assert final[1][SIBLING] != baseline[1][SIBLING]
                        if action == 'update':
                            assert final[1][RECORD] != baseline[1][RECORD]
                    check = factory(**options)
                    try:
                        rows = list(await maybe(check.scalars(
                            select(app.Customer).order_by(app.Customer.id))))
                        assert {row.id: (row.name, row.label, row.version_id)
                                for row in rows} == expected
                    finally:
                        await maybe(check.close())
                    return states, final[0]
                finally:
                    await maybe(winner.close())
                    await maybe(loser.close())
                    if async_engine is not None:
                        assert async_engine.sync_engine.pool.checkedout() == 0
                        await async_engine.dispose()
                    assert app.runtime.pool.checkedout() == 0

            observations.append(asyncio.run(scenario()))
    assert observations[0] == observations[1], (
        f'Native/attached SAVEPOINT versioning state differs: {observations}')

"""Native PostgreSQL oracles for admitted IS NULL on null-extended aliases.

The physical conversion in search_application is fixture setup, not a lifecycle
qualification. Application statements use the separate restricted runtime role.
"""

import asyncio

import pytest
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import aliased

from test_sqlalchemy_search import OTHER, _async_factory, _row, search_application


def _seed(app, duplicate):
    rows = [_row(app, "left", rank) for rank in range(1, 6)]
    rows.extend(_row(app, value, rank) for rank, value in
                ((101, None), (102, ""), (103, "right")))
    if duplicate:
        rows.append(_row(app, None, 101))
    return rows


def _query(app, shape, duplicate):
    left, right = aliased(app.Customer), aliased(app.Customer)
    on = left.rank + 100 == right.rank
    scope = left.rank.between(1, 5)
    if not app.single_tenant:
        on = and_(on, right.tenant_id == app.tenant)
        scope = and_(scope, left.tenant_id == app.tenant)
    null = right.name.is_(None)
    columns = (left.rank, null, right.name) if shape == "projection" else (left.rank, right.name)
    statement = select(*columns).select_from(left).outerjoin(right, on).where(scope).order_by(left.rank)
    base = [(1, None), (2, ""), (3, "right"), (4, None), (5, None)]
    if duplicate:
        base.insert(1, (1, None))
    if shape == "projection":
        return statement, [(rank, value is None, value) for rank, value in base]
    if shape == "or":
        return statement.where(or_(null, left.rank == 3)), [row for row in base if row[0] != 2]
    statement = statement.where(null)
    expected = [row for row in base if row[1] is None]
    if shape == "and":
        return statement.where(left.rank >= 4), [row for row in expected if row[0] >= 4]
    if shape == "page":
        # Skip the rank-1 bag so ties cannot make the page nondeterministic.
        offset = 2 if duplicate else 1
        return statement.offset(offset).limit(1), [(4, None)]
    return statement, expected


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
@pytest.mark.parametrize("mode", ["sync", "async"])
@pytest.mark.parametrize("single_tenant", [False, True], ids=["multi", "single"])
@pytest.mark.parametrize("duplicate", [False, True], ids=["one", "bag"])
@pytest.mark.parametrize("shape", ["projection", "filter", "and", "or", "page"])
def test_outer_join_null_predicate_preserves_native_results(protected, mode, single_tenant, duplicate, shape):
    with search_application(protected, single_tenant=single_tenant, attach_now=mode == "sync") as app:
        if mode == "sync":
            statement, expected = _query(app, shape, duplicate)
            with app.sessions(tenant_id=app.tenant) as session:
                session.add_all(_seed(app, duplicate))
                session.commit()
            if not single_tenant:
                with app.sessions(tenant_id=OTHER) as session:
                    session.add(_row(app, None, 105, tenant=OTHER))
                    session.commit()
            with app.sessions(tenant_id=app.tenant) as session:
                assert [tuple(row) for row in session.execute(statement)] == expected
        else:
            async def run():
                engine, sessions = await _async_factory(app)
                try:
                    statement, expected = _query(app, shape, duplicate)
                    async with sessions(tenant_id=app.tenant) as session:
                        session.add_all(_seed(app, duplicate))
                        await session.commit()
                    if not single_tenant:
                        async with sessions(tenant_id=OTHER) as session:
                            session.add(_row(app, None, 105, tenant=OTHER))
                            await session.commit()
                    async with sessions(tenant_id=app.tenant) as session:
                        assert [tuple(row) for row in await session.execute(statement)] == expected
                finally:
                    await engine.dispose()
            asyncio.run(run())


@pytest.mark.parametrize("protected", [False, True], ids=["native-control", "guarded"])
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_present_foreign_tenant_null_does_not_gain_absent_row_permission(protected, mode):
    """Security control, not a native-equivalence claim for unauthorized input.

    Project no payload: authentication must not mask a weakened search guard.
    The native control independently proves that the actual NULL row exists.
    """
    with search_application(protected, attach_now=mode == "sync") as app:
        def query():
            model = aliased(app.Customer)
            return select(model.rank).where(model.rank == 105, model.name.is_(None))
        expected = [] if protected else [105]
        if mode == "sync":
            with app.sessions(tenant_id=OTHER) as session:
                session.add(_row(app, None, 105, tenant=OTHER))
                session.commit()
            with app.sessions(tenant_id=app.tenant) as session:
                assert list(session.scalars(query())) == expected
        else:
            async def run():
                engine, sessions = await _async_factory(app)
                try:
                    async with sessions(tenant_id=OTHER) as session:
                        session.add(_row(app, None, 105, tenant=OTHER))
                        await session.commit()
                    async with sessions(tenant_id=app.tenant) as session:
                        assert list(await session.scalars(query())) == expected
                finally:
                    await engine.dispose()
            asyncio.run(run())


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
@pytest.mark.parametrize("mode", ["sync", "async"])
@pytest.mark.parametrize("topology", ["reversed", "full", "chained-alias"])
def test_null_extended_left_side_and_chained_aliases(protected, mode, topology):
    """Reverse join direction and full joins must use the matching row identity."""
    with search_application(protected, attach_now=mode == "sync") as app:
        def query():
            left = aliased(app.Customer)
            if topology == "chained-alias":
                left = aliased(left)
            right = aliased(app.Customer)
            on = and_(left.rank + 10 == right.rank,
                      left.tenant_id == app.tenant, right.tenant_id == app.tenant)
            statement = select(left.rank, right.rank, left.name.is_(None), right.name.is_(None))
            if topology == "full":
                statement = statement.select_from(left).join(right, on, full=True)
            else:
                statement = statement.select_from(right).outerjoin(left, on)
            return statement.where(right.rank.between(11, 13), right.tenant_id == app.tenant).order_by(right.rank)
        expected = [(1, 11, True, True), (None, 13, True, False)]
        def rows():
            return [_row(app, None, 1), _row(app, "unmatched-left", 2),
                    _row(app, None, 11), _row(app, "unmatched-right", 13)]
        if mode == "sync":
            with app.sessions(tenant_id=app.tenant) as session:
                session.add_all(rows())
                session.commit()
            with app.sessions(tenant_id=app.tenant) as session:
                assert [tuple(row) for row in session.execute(query())] == expected
        else:
            async def run():
                engine, sessions = await _async_factory(app)
                try:
                    async with sessions(tenant_id=app.tenant) as session:
                        session.add_all(rows())
                        await session.commit()
                    async with sessions(tenant_id=app.tenant) as session:
                        assert [tuple(row) for row in await session.execute(query())] == expected
                finally:
                    await engine.dispose()
            asyncio.run(run())

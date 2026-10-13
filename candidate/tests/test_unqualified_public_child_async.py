"""Async native-oracle coverage for attachment-time public table binding."""
import asyncio
import os
import psycopg
import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from cryptalis.sqlalchemy import attach
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import run, publish, keys, TABLE_ID

@pytest.mark.parametrize('target', ['child', 'parent_cascade'])
@pytest.mark.parametrize('outcome', ['commit', 'rollback', 'savepoint'])
def test_async_unqualified_child_matches_native(target, outcome):
    results = []
    for protected in [False, True]:
        with single_tenant_public_cascade_application() as app:
            if protected: run(app); publish(app)
            app.public_item.schema = None
            C, P = app.Customer, app.PublicItem
            async def scenario():
                path = [app.schema + ',pg_catalog']
                engine = create_async_engine('postgresql+psycopg://', hide_parameters=True,
                    async_creator=lambda: psycopg.AsyncConnection.connect(
                        os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL'],
                        options='-csearch_path='+path[0]))
                try:
                    if protected:
                        factory = await attach(app.mapping, engine, lock=app.plan.lock_bytes,
                                               keys=keys, deployment=(app.plan,app.pin))
                        factory._owner._experimental_public_delete_tables = (app.table,app.public_item)
                        factory._owner._experimental_protected_equality_delete = True
                        factory._owner._experimental_public_child_cascade_delete = True
                        path[0] = 'pg_catalog'
                    else:
                        factory = async_sessionmaker(engine)
                    async with factory(**({'tenant_id':TABLE_ID} if protected else {})) as session:
                        nested = await session.begin_nested() if outcome == 'savepoint' else None
                        statement = (delete(P).where(P.label == 'child-1') if target == 'child'
                                     else delete(C).where(C.label == 'label-101'))
                        count = (await session.execute(statement)).rowcount
                        if outcome == 'commit': await session.commit()
                        elif nested is not None: await nested.rollback(); await session.commit()
                        else: await session.rollback()
                        parents = list((await session.execute(select(C.id,C.name,C.label).order_by(C.id))).all())
                        children = list((await session.execute(select(P.id,P.label,P.parent_id).order_by(P.id))).all())
                    return count, parents, children
                finally:
                    await engine.dispose()
            results.append(asyncio.run(scenario()))
    assert results[0] == results[1]
    assert results[0][0] == 1
    assert len(results[0][2]) == (6 if outcome == 'commit' else 7)

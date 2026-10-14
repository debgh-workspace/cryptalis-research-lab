"""Finite async counterpart of eight historical synchronous warm-mapper IDs.

Real database execution requires the approved role-preflight wrapper. There are
no private mapper/cache hooks, concurrent sessions or performance assertions.
"""
import asyncio
import json
import os
from pathlib import Path
import sys
from uuid import UUID

import psycopg
import pytest
import sqlalchemy
from sqlalchemy import String, Text, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'candidate-s23-planning-20261014/tests'))
from test_migration import application, run, publish, keys, TENANT, frames, independent_open
from cryptalis.sqlalchemy import attach


@pytest.mark.parametrize('kind', ['text', 'varchar'])
@pytest.mark.parametrize('count', [1, 3])
@pytest.mark.parametrize('action', ['insert', 'update'])
def test_native_protected_async_warm_mapper_differential(kind, count, action):
    outcomes = []
    for protected in (False, True):
        field_type = Text(collation='C') if kind == 'text' else String(24, collation='C')
        with application(rows=count, field_type=field_type) as app:
            async def scenario():
                engine = create_async_engine('postgresql+psycopg://', echo=False, hide_parameters=True,
                    async_creator=lambda: psycopg.AsyncConnection.connect(
                        os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
                native_sessions = async_sessionmaker(engine)
                try:
                    # Warm the actual async operation through public ORM calls.
                    # INSERT warm-up is rolled back so historical input rows stay
                    # unchanged. UPDATE uses the historical warm-N values.
                    async with native_sessions() as session:
                        for n in range(count):
                            if action == 'insert':
                                session.add(app.Customer(id=UUID(int=800+n), tenant_id=TENANT,
                                    name=f'warm-insert-{n}', label='public'))
                            else:
                                row = await session.get(app.Customer, UUID(int=100+n))
                                row.name = f'warm-{n}'
                        if action == 'insert':
                            await session.flush()
                            await session.rollback()
                        else:
                            await session.commit()

                    # No application session is open during maintenance cutover.
                    # Keep the already-used registry and engine for attachment.
                    if protected:
                        assert run(app).phase == 'PENDING'
                        publish(app)
                        factory = await attach(app.mapping, engine, lock=app.plan.lock_bytes,
                            keys=keys, deployment=(app.plan, app.pin))
                    else:
                        factory = lambda **kwargs: native_sessions()

                    identities = []
                    async with factory(tenant_id=TENANT) as session:
                        for n in range(count):
                            if action == 'insert':
                                row = app.Customer(id=UUID(int=900+n), tenant_id=TENANT,
                                    name=f'after-{n}', label='public')
                                session.add(row)
                            else:
                                row = await session.get(app.Customer, UUID(int=100+n))
                                row.name = f'after-{n}'
                            identities.append(row.id)
                        await session.commit()
                        result = await session.scalars(select(app.Customer).order_by(app.Customer.id))
                        observed = [(str(row.id), str(row.tenant_id), row.name, row.label)
                                    for row in result]
                    if protected:
                        descriptor = json.loads(app.plan.lock_bytes)['models'][0]['fields'][0]['descriptor']
                        stored = frames(app, True)
                        for n, identity in enumerate(identities):
                            assert independent_open(stored[identity], descriptor, TENANT, identity) == f'after-{n}'
                    return observed
                finally:
                    await engine.dispose()

            outcomes.append(asyncio.run(scenario()))

    assert outcomes[0] == outcomes[1]
    # No fallback classification: an exception, decode mismatch or differential
    # mismatch fails the test and leaves this corpus cell unclassified.
    receipt = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent / 'warm-mapper-async-corpus.jsonl'
    with receipt.open('a') as stream:
        stream.write(json.dumps({'id': f'warm_mapper_{action}_{count}_{kind}',
            'mode': 'async', 'sqlalchemy': sqlalchemy.__version__,
            'classification': 'IDENTICAL', 'native': outcomes[0], 'protected': outcomes[1],
            'scope': 'Finite public async ORM warm-up and same-registry attachment; no concurrency or speed claim.'}) + '\n')

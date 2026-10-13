"""Queued writes from warmed attachments cannot cross an existing reverse pause.

Owned synthetic data only. This is the durable database maintenance guard, not
an active-rotation protocol or proof of host termination/credential turnover.
"""
import asyncio
import inspect as python_inspect
import os
from uuid import UUID

import psycopg
import pytest
from sqlalchemy import event, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine

from cryptalis.crypto import Keyring
from cryptalis.sqlalchemy import attach
from test_deprotection import execute, prepared
from test_migration import (
    PROVIDER, TENANT, PublicFixtureProvider, application, frames,
    independent_open, keys,
)
from test_retained_profile_safety_oracles import snapshot


RECORD = UUID(int=102)
INSERTED = UUID(int=999)
VALUE = 'queued before reverse pause 雪'


class CountingPublicProvider(PublicFixtureProvider):
    """Public fixture roots only; counts actual local unwraps, not cache hits."""

    def __init__(self):
        self.calls = 0

    def unwrap(self, wrapper, context):
        self.calls += 1
        return super().unwrap(wrapper, context)


async def maybe(value):
    return await value if python_inspect.isawaitable(value) else value


def decoded_values(app):
    descriptor = app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
    bodies = frames(app, True)
    return bodies, {
        identity: independent_open(body, descriptor, TENANT, identity)
        for identity, body in bodies.items()
    }


async def queue(session, app, action):
    if action == 'insert':
        session.add(app.Customer(id=INSERTED, tenant_id=TENANT,
                                 name=VALUE, label='queued insert'))
    else:
        row = await maybe(session.get(app.Customer, RECORD))
        if action == 'update':
            row.name = VALUE
        else:
            await maybe(session.delete(row))


@pytest.mark.parametrize('mode', ['sync', 'async'])
@pytest.mark.parametrize('action', ['insert', 'update', 'delete'])
@pytest.mark.parametrize('phase', ['EXPANDED', 'VERIFIED'])
def test_warm_queued_write_is_fenced_and_same_attachment_recovers_after_abort(
        mode, action, phase):
    """Exercise first durable pause and final pre-switch pause, then valid abort."""
    with application() as app:
        with app.owner.connect() as connection:
            native = connection.exec_driver_sql(
                f'SELECT id,tenant_id,name,label FROM "{app.schema}".customer ORDER BY id').all()
        d, plan, pin, consent = prepared(app)
        before_frames, before_values = decoded_values(app)
        assert before_values == {row[0]: row[2] for row in native}

        async def scenario():
            provider = CountingPublicProvider()
            ring = Keyring(keys(TENANT).policy, {PROVIDER: provider}, max_age=300)
            async_engine = None
            if mode == 'async':
                async_engine = create_async_engine(
                    'postgresql+psycopg://', hide_parameters=True,
                    async_creator=lambda: psycopg.AsyncConnection.connect(
                        os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
                factory = await attach(app.mapping, async_engine,
                    lock=app.plan.lock_bytes, keys=ring, deployment=(app.plan, app.pin))
                observed_engine = async_engine.sync_engine
            else:
                factory = attach(app.mapping, app.runtime,
                    lock=app.plan.lock_bytes, keys=ring, deployment=(app.plan, app.pin))
                observed_engine = app.runtime
            session = factory(tenant_id=TENANT, expire_on_commit=False)
            calls = []

            def observe(connection, cursor, statement, parameters, context, many):
                # Count executions without retaining SQL, binds or row values.
                calls.append(context.isinsert or context.isupdate or context.isdelete)

            event.listen(observed_engine, 'before_cursor_execute', observe)
            try:
                rows = list(await maybe(session.scalars(
                    select(app.Customer).order_by(app.Customer.id))))
                assert [(r.id, r.tenant_id, r.name, r.label) for r in rows] == native
                # Keep the mapped objects and root cache, but finish the actual
                # database transaction before the operator installs the guard.
                await maybe(session.commit())
                assert not session.in_transaction()
                assert provider.calls == 2
                warm_calls = provider.calls
                executed = len(calls)
                await queue(session, app, action)
                assert len(calls) == executed, 'Queueing dispatched work before the pause'

                assert execute(app, d, plan, pin, consent, phase).phase == phase
                paused = snapshot(app)
                assert decoded_values(app) == (before_frames, before_values)

                with pytest.raises(DBAPIError) as failure:
                    await maybe(session.flush())
                # Actual PostgreSQL maintenance trigger, not a rejected query,
                # expired key, missing column, or an invented local success.
                assert failure.value.orig.sqlstate == '55000'
                assert calls[executed:] == [True]
                assert not session.is_active and session.in_transaction()
                assert provider.calls == warm_calls
                assert snapshot(app) == paused
                await maybe(session.rollback())
                assert session.is_active and not session.in_transaction()
                assert snapshot(app) == paused

                result = d.abort(plan, app.owner, pin=pin, approval=app.approval,
                                 plaintext_approval=consent)
                assert result.phase == 'ABORTED'
                app.m.check_deployment(app.plan, app.owner, pin=app.pin)
                assert decoded_values(app) == (before_frames, before_values)

                # Sensitivity control: precisely the same attachment and DML
                # succeed after legitimate abort restores the same authority.
                await queue(session, app, action)
                await maybe(session.commit())
                assert provider.calls == warm_calls
                expected = dict(before_values)
                if action == 'insert':
                    expected[INSERTED] = VALUE
                elif action == 'update':
                    expected[RECORD] = VALUE
                else:
                    del expected[RECORD]
                final_frames, final_values = decoded_values(app)
                assert final_values == expected
                changed = {INSERTED if action == 'insert' else RECORD}
                assert {key: value for key, value in final_frames.items() if key not in changed} == {
                    key: value for key, value in before_frames.items() if key not in changed}
                result = await maybe(session.execute(select(
                    app.Customer.id, app.Customer.name).order_by(app.Customer.id)))
                assert result.all() == sorted(expected.items())
            finally:
                await maybe(session.close())
                event.remove(observed_engine, 'before_cursor_execute', observe)
                if async_engine is not None:
                    await async_engine.dispose()

        asyncio.run(scenario())

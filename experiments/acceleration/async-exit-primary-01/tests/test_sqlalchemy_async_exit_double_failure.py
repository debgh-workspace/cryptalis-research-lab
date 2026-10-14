"""Adapter-owned pre-exit failure precedence; real PostgreSQL oracles.

NOT EXECUTED during source preparation. Use the unchanged PostgreSQL wrapper.
One-shot public engine callbacks inject rollback failure before its SQL/driver
call. They do not simulate a broken physical transport. Protected preparation
uses a genuinely cold Keyring and the existing development provider boundary.
"""

import asyncio
import sys
import traceback

import pytest
from sqlalchemy import event, select

from cryptalis.crypto import Keyring, KeyUnavailable
from test_sqlalchemy_search import _async_factory, _row, search_application


_CLEANUP_MARKER = "SYNTHETIC_PRIVATE_EXIT_CLEANUP"
_QUARANTINE_MARKER = "SYNTHETIC_PRIVATE_EXIT_QUARANTINE"
_CLEANUP_NOTE = (
    "Cryptalis transaction cleanup failed. Discard this failed unit; "
    "the connection outcome is unknown. Do not retry until inspection.")
_QUARANTINE_NOTE = (
    "Cryptalis connection quarantine failed. Keep the workload "
    "stopped and inspect the database session before retrying.")


def _bound_owner_transaction(connection):
    # Keep this public fixture-local listener through fixture teardown, so a
    # leaked lock cannot leave DROP SCHEMA or independent inspection unbounded.
    connection.exec_driver_sql("SET LOCAL lock_timeout = '1s'")
    connection.exec_driver_sql("SET LOCAL statement_timeout = '5s'")


async def _finish_async(session, engine, task, primary):
    """Explicit bounded lab cleanup; never replace an earlier test failure."""
    failures = []
    if task is not None and not task.done():
        task.cancel()
        try:
            await asyncio.wait_for(task, timeout=5)
        except asyncio.CancelledError:
            pass
        except BaseException:
            failures.append("task_completion")
    actions = []
    if session is not None:
        actions.extend((("session_invalidate", session.invalidate),
                        ("session_close", session.close)))
    actions.append(("engine_dispose", engine.dispose))
    for label, action in actions:
        try:
            await asyncio.wait_for(action(), timeout=5)
        except BaseException:
            failures.append(label)
    if failures:
        note = "Bounded laboratory cleanup failed at " + ", ".join(failures) + "; inspect the lab before continuation."
        if primary is not None:
            try:
                BaseException.add_note(primary, note)
            except BaseException:
                pass  # Keep the original failure observable if output fails.
        else:
            raise AssertionError(note)


def _rollback_fault(engine, nested, failure, calls):
    """Public callback, armed once; no private native methods are replaced."""
    event_name = "before_cursor_execute" if nested else "rollback"

    def inject(*args):
        if nested and not args[2].startswith("ROLLBACK TO SAVEPOINT"):
            return
        if not calls:
            calls.append("nested" if nested else "root")
            raise failure

    event.listen(engine, event_name, inject)
    return event_name, inject


def _observe_stored_and_unlocked(app, identity):
    """Independent observer must acquire the row lock before fixture close."""
    with app.owner_engine.begin() as connection:
        connection.exec_driver_sql("SET LOCAL lock_timeout = '100ms'")
        return connection.exec_driver_sql(
            f'SELECT rank FROM "{app.schema}".customer WHERE id = %s FOR UPDATE',
            (identity,),
        ).scalar_one()


async def _exercise_async(app, nested, fault, *, quarantine_failure=False):
    engine, sessions = await _async_factory(app)
    native = engine.sync_engine
    healthy, original_unwrap = app.rings[app.tenant], app.provider.unwrap_async
    session, task, hook = None, None, None
    original_invalidate = None
    captured_primary, provider_calls, rollback_calls, invalidation_calls = [], [], [], []
    primary_metadata = []
    cleanup_error = RuntimeError(_CLEANUP_MARKER)
    provider_error = KeyUnavailable() if fault == "provider" else asyncio.CancelledError()
    note_hook_calls = []

    class NoteOverrideCancellation(asyncio.CancelledError):
        def add_note(self, note):
            note_hook_calls.append("custom_add_note")
            raise RuntimeError("SYNTHETIC_PRIVATE_NOTE_OUTPUT")

    if fault == "note_override":
        provider_error = NoteOverrideCancellation()
    elif fault == "note_unavailable":
        provider_error.__notes__ = ()  # Builtin add_note requires a list.
    entered, never = asyncio.Event(), asyncio.Event()

    class ObservedKeyring(Keyring):
        async def prepare_async(self, **options):
            try:
                return await super().prepare_async(**options)
            except BaseException as failure:
                # Observe the error leaving the public Keyring boundary. In
                # particular, provider errors are fresh sanitized exceptions.
                captured_primary.append(failure)
                primary_metadata.append(tuple(getattr(failure, name, None)
                                              for name in ("operation_id", "code", "stage")))
                raise

    async def fail_provider(*args):
        provider_calls.append("unwrap")
        if fault == "task_cancel":
            entered.set()
            await never.wait()
            raise AssertionError("The blocked provider must be cancelled")
        raise provider_error

    def fail_native_commit(*args):
        captured_primary.append(provider_error)
        raise provider_error

    async def observe_invalidation():
        invalidation_calls.append("invalidate")
        if quarantine_failure:
            raise RuntimeError(_QUARANTINE_MARKER)
        assert original_invalidate is not None
        await original_invalidate()

    try:
        row = _row(app, "before", 1)
        identity = row.id
        async with sessions(tenant_id=app.tenant) as seed:
            seed.add(row)
            await seed.commit()
        session = sessions(tenant_id=app.tenant)
        if nested:
            # Leave an externally owned outer transaction. A failed inner
            # cleanup must not allow it to publish unrolled-back inner work.
            await session.begin()
            session.add(_row(app, "outer prefix", 0))
            await session.flush()

        async def work():
            nonlocal hook, original_invalidate
            target = session.begin_nested() if nested else session.begin()
            async with target:
                current = await session.get(app.Customer, identity)
                current.name, current.rank = "pending", 2
                await session.flush()
                if app.protected:
                    app.provider.unwrap_async = fail_provider
                    app.rings[app.tenant] = ObservedKeyring(
                        healthy.policy, {app.provider.provider_id: app.provider})
                else:
                    event.listen(session.sync_session, "before_commit", fail_native_commit, once=True)
                hook = _rollback_fault(native, nested, cleanup_error, rollback_calls)
                if app.protected:
                    original_invalidate = session.invalidate
                    session.invalidate = observe_invalidation

        if fault == "task_cancel":
            assert app.protected
            task = asyncio.create_task(work())
            await asyncio.wait_for(entered.wait(), timeout=5)
            task.cancel()
            with pytest.raises(BaseException) as caught:
                await task
        else:
            with pytest.raises(BaseException) as caught:
                await work()

        assert len(captured_primary) == 1
        assert rollback_calls == ["nested" if nested else "root"]
        if app.protected:
            assert provider_calls == ["unwrap"]
            assert caught.value is captured_primary[0]
            assert invalidation_calls == ["invalidate"]
            assert tuple(getattr(caught.value, name, None)
                         for name in ("operation_id", "code", "stage")) == primary_metadata[0]
            if fault == "provider":
                assert type(caught.value) is KeyUnavailable
                assert caught.value is not provider_error
                assert caught.value.effects == "unknown"
                assert caught.value.retryable is False
            else:
                assert isinstance(caught.value, asyncio.CancelledError)
                if task is not None:
                    assert task.cancelled()
            expected_notes = [_CLEANUP_NOTE]
            if quarantine_failure:
                expected_notes.append(_QUARANTINE_NOTE)
                assert invalidation_calls == ["invalidate"]
            if fault == "note_unavailable":
                assert caught.value.__notes__ == ()
            else:
                assert getattr(caught.value, "__notes__", []) == expected_notes
            assert note_hook_calls == []
            rendered = "".join(traceback.format_exception(caught.value))
            assert _CLEANUP_MARKER not in rendered
            assert _QUARANTINE_MARKER not in rendered
            assert "SYNTHETIC_PRIVATE_NOTE_OUTPUT" not in rendered
            assert session.sync_session._prepared is None
        else:
            # Pinned native cleanup gives the secondary error precedence.
            # Protected precedence is deliberate policy, not native equality.
            assert caught.value is cleanup_error
            assert provider_calls == []

        if hook is not None:
            event.remove(native, *hook)
            hook = None
        app.provider.unwrap_async = original_unwrap
        app.rings[app.tenant] = healthy
        if original_invalidate is not None:
            session.invalidate = original_invalidate
            original_invalidate = None

        if not app.protected or quarantine_failure:
            # Explicit lab cleanup. These arms do not claim that the failed
            # exit quarantined/released the connection before this point.
            await session.invalidate()
        else:
            # These assertions precede any test-driven invalidate/close or
            # fixture cleanup. The method call alone is not the oracle.
            assert not session.in_transaction()
            assert not session.in_nested_transaction()
            assert native.pool.checkedout() == 0
            assert _observe_stored_and_unlocked(app, identity) == 1

        # A fresh checkout and real commit cannot publish the prior unit.
        async with sessions(tenant_id=app.tenant) as fresh:
            assert await fresh.scalar(select(app.Customer.rank).where(app.Customer.id == identity)) == 1
            assert await fresh.scalar(select(app.Customer.name).where(app.Customer.id == identity)) == "before"
            assert list(await fresh.scalars(select(app.Customer.rank).order_by(app.Customer.rank))) == [1]
            await fresh.commit()
        assert _observe_stored_and_unlocked(app, identity) == 1
    finally:
        primary = sys.exc_info()[1]
        if hook is not None:
            event.remove(native, *hook)
        app.provider.unwrap_async = original_unwrap
        app.rings[app.tenant] = healthy
        if session is not None:
            if original_invalidate is not None:
                session.invalidate = original_invalidate
        await _finish_async(session, engine, task, primary)


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
@pytest.mark.parametrize("nested", [False, True], ids=["root", "savepoint"])
@pytest.mark.parametrize("fault", ["provider", "cancel"])
def test_async_preparation_exit_double_failure_preserves_primary_policy(protected, nested, fault):
    with search_application(protected, attach_now=False) as app:
        event.listen(app.owner_engine, "begin", _bound_owner_transaction)
        asyncio.run(_exercise_async(app, nested, fault))


@pytest.mark.parametrize("nested", [False, True], ids=["root", "savepoint"])
def test_async_exit_invalidation_failure_is_reported_without_replacing_primary(nested):
    with search_application(True, attach_now=False) as app:
        event.listen(app.owner_engine, "begin", _bound_owner_transaction)
        asyncio.run(_exercise_async(app, nested, "provider", quarantine_failure=True))


@pytest.mark.parametrize("nested", [False, True], ids=["root", "savepoint"])
def test_actual_task_cancellation_survives_exit_cleanup_failure(nested):
    with search_application(True, attach_now=False) as app:
        event.listen(app.owner_engine, "begin", _bound_owner_transaction)
        asyncio.run(_exercise_async(app, nested, "task_cancel"))


@pytest.mark.parametrize("nested", [False, True], ids=["root", "savepoint"])
@pytest.mark.parametrize("fault", ["note_override", "note_unavailable"])
def test_exception_note_failure_cannot_replace_primary_or_skip_cleanup(nested, fault):
    with search_application(True, attach_now=False) as app:
        event.listen(app.owner_engine, "begin", _bound_owner_transaction)
        asyncio.run(_exercise_async(app, nested, fault))


@pytest.mark.parametrize("nested", [False, True], ids=["root", "savepoint"])
def test_pending_only_preparation_failure_clears_prior_material_without_sql(nested):
    """Successful cleanup keeps the existing no-I/O/outer-unit contract."""
    with search_application(True, attach_now=False) as app:
        event.listen(app.owner_engine, "begin", _bound_owner_transaction)

        async def run():
            engine, sessions = await _async_factory(app)
            session = sessions(tenant_id=app.tenant)
            original_unwrap, healthy = app.provider.unwrap_async, app.rings[app.tenant]
            calls, statements = [], []

            def observe_sql(*args):
                statements.append("SQL")

            async def fail_provider(*args):
                calls.append("unwrap")
                raise KeyUnavailable()

            try:
                # Native clean commit performs no SQL; the adapter prepares
                # local authority, leaving prior material to clear on failure.
                await session.commit()
                assert session.sync_session._prepared is not None
                if nested:
                    await session.begin()
                app.provider.unwrap_async = fail_provider
                app.rings[app.tenant] = Keyring(healthy.policy, {app.provider.provider_id: app.provider})
                event.listen(engine.sync_engine, "before_cursor_execute", observe_sql)
                target = session.begin_nested() if nested else session.begin()
                with pytest.raises(KeyUnavailable) as caught:
                    async with target:
                        session.add(_row(app, "never flushed", 3))
                assert calls == ["unwrap"]
                assert statements == []
                assert session.sync_session._prepared is None
                assert session.in_transaction() is nested
                assert not session.in_nested_transaction()
                assert not session.new
                assert _CLEANUP_NOTE not in getattr(caught.value, "__notes__", [])
                assert caught.value.effects == "none"
            finally:
                primary = sys.exc_info()[1]
                app.provider.unwrap_async = original_unwrap
                app.rings[app.tenant] = healthy
                if event.contains(engine.sync_engine, "before_cursor_execute", observe_sql):
                    event.remove(engine.sync_engine, "before_cursor_execute", observe_sql)
                await _finish_async(session, engine, None, primary)

        asyncio.run(run())


@pytest.mark.parametrize("protected", [False, True], ids=["native", "attached"])
@pytest.mark.parametrize("nested", [False, True], ids=["root", "savepoint"])
def test_sync_body_double_failure_keeps_native_exception_policy(protected, nested):
    """Related sync/body exit stays native; it has no async pre-exit prepare."""
    with search_application(protected) as app:
        event.listen(app.owner_engine, "begin", _bound_owner_transaction)
        session = app.sessions(tenant_id=app.tenant)
        hook = None
        calls = []
        cleanup_error = RuntimeError(_CLEANUP_MARKER)
        primary = KeyUnavailable()
        try:
            if nested:
                session.begin()
            target = session.begin_nested() if nested else session.begin()
            with pytest.raises(BaseException) as caught:
                with target:
                    session.add(_row(app, "pending", 2))
                    session.flush()
                    hook = _rollback_fault(app.engine, nested, cleanup_error, calls)
                    raise primary
            assert calls == ["nested" if nested else "root"]
            assert caught.value is cleanup_error
            assert not getattr(caught.value, "__notes__", [])
        finally:
            if hook is not None:
                event.remove(app.engine, *hook)
            session.invalidate()
            session.close()

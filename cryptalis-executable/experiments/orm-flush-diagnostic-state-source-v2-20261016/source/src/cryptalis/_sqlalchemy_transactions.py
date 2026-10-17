"""Scoped native SAVEPOINT execution; no caller-supplied SQL authority.

Public Session transaction events retain native transaction objects. Short-lived
method scopes authorize only the dialect's exact control clause on the owning
connection. Ordinary statements still require ordinary operation admission.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps

from sqlalchemy.sql.expression import SavepointClause, ReleaseSavepointClause, RollbackToSavepointClause

_scope = ContextVar('cryptalis_native_transaction_scope', default=None)
_clause = ContextVar('cryptalis_native_control_clause', default=None)


@dataclass
class _ClausePermit:
    owner: object
    session: object
    transaction: object
    connection: object
    statement: object
    stage: str = 'new'


@contextmanager
def native_scope(session, transaction=None):
    transaction = transaction or session.get_nested_transaction() or session.get_transaction()
    token = _scope.set((session, transaction))
    try:
        yield
    finally:
        _scope.reset(token)


def inspect_control(owner, connection, statement, *, driver=False):
    """Return false for ordinary SQL; fail closed for any unowned control."""
    if not isinstance(statement, (SavepointClause, ReleaseSavepointClause, RollbackToSavepointClause)):
        return False
    permit = _clause.get()
    if (permit is None or permit.owner is not owner or permit.connection is not connection
            or permit.statement is not statement or permit.session._owner is not owner
            or _scope.get() != (permit.session, permit.transaction)
            or permit.stage != ('prepared' if driver else 'new')):
        raise owner._control_error()
    permit.stage = 'used' if driver else 'prepared'
    return True


def track_transaction(session, transaction):
    # Keep the native object/type and context manager. No global class patch.
    for name in ('connection', 'commit', 'rollback', 'close'):
        native = getattr(transaction, name)
        def wrap(native):
            @wraps(native)
            def scoped(*args, **kwargs):
                with native_scope(session, transaction):
                    return native(*args, **kwargs)
            return scoped
        setattr(transaction, name, wrap(native))


def after_begin(session, transaction, connection):
    session._control_connections.add(connection)
    if transaction.nested:
        pending = session._control_pending.pop(transaction, None)
        native = connection.get_nested_transaction()
        if pending is None or pending[0] is not connection or native is None:
            raise session._owner._control_error()
        session._control_records[transaction] = (connection, native, pending[1])


def after_end(session, transaction):
    session._control_pending.pop(transaction, None)
    session._control_records.pop(transaction, None)
    if transaction.nested:
        session._prepared = None
    if transaction.parent is None:
        session._control_connections.clear()
        session._control_pending.clear()
        session._control_records.clear()


def install_control(owner, engine):
    """Bind fixed dialect control methods to this attachment only."""
    def execute(kind, connection, name):
        active = _scope.get()
        if active is None:
            raise owner._control_error()
        session, scope_transaction = active
        if (session._owner is not owner or scope_transaction is None
                or connection not in session._control_connections
                or connection.engine is not engine):
            raise owner._control_error()
        if kind == 'create':
            transaction = session.get_nested_transaction()
            # Flush subtransactions have the nested transaction as an ancestor.
            ancestor = scope_transaction
            while ancestor is not None and ancestor is not transaction:
                ancestor = ancestor.parent
            if (transaction is None or ancestor is None
                    or transaction in session._control_records
                    or transaction in session._control_pending):
                raise owner._control_error()
            statement = SavepointClause(name)
        else:
            matches = [(tx, record) for tx, record in session._control_records.items()
                       if record[0] is connection and record[2] == name
                       and record[1] is connection.get_nested_transaction()]
            if len(matches) != 1:
                raise owner._control_error()
            transaction, record = matches[0]
            ancestor = transaction
            while ancestor is not None and ancestor is not scope_transaction:
                ancestor = ancestor.parent
            if ancestor is None:
                # A failed flush rolls back through its native non-nested
                # subtransaction to the enclosing SAVEPOINT boundary.
                ancestor = scope_transaction
                while ancestor is not None and not ancestor.nested and ancestor is not transaction:
                    ancestor = ancestor.parent
                if ancestor is not transaction:
                    raise owner._control_error()
            statement = ReleaseSavepointClause(name) if kind == 'release' else RollbackToSavepointClause(name)
        permit = _ClausePermit(owner, session, scope_transaction, connection, statement)
        token = _clause.set(permit)
        try:
            connection.execute(statement)
            if permit.stage != 'used':
                raise owner._control_error()
            if kind == 'create':
                session._control_pending[transaction] = (connection, name)
        except BaseException:
            # Native rollback failure can leave inner writes pending while
            # the Session restores its in-memory snapshot. Quarantine this
            # physical connection: a later outer commit must not publish them.
            connection.invalidate()
            raise
        finally:
            _clause.reset(token)
    engine.dialect.do_savepoint = lambda connection, name: execute('create', connection, name)
    engine.dialect.do_release_savepoint = lambda connection, name: execute('release', connection, name)
    engine.dialect.do_rollback_to_savepoint = lambda connection, name: execute('rollback', connection, name)


def fail_prepared_flush(session, *, cleanup_state):
    """Use the native failed-flush child boundary for early preparation errors.

    Version-qualified against SQLAlchemy 2.0.51 and 2.1.3. Their own _flush
    uses _begin/rollback(_capture_exception=True) for the same state transition.
    The internal caller owns an exact dict initialized to an unknown outcome.
    Publish only after all fallback attempts; never store state on an exception.
    """
    transaction = session.get_nested_transaction() or session.get_transaction()
    if transaction is None or not transaction.is_active:
        return
    connections = tuple(session._control_connections)
    drivers = {}
    for connection in connections:
        if not connection.closed and not connection.invalidated:
            drivers[connection] = connection.connection.dbapi_connection
    try:
        with native_scope(session, transaction):
            transaction._begin().rollback(_capture_exception=True)
    except BaseException as failure:
        incomplete = False
        def note(message):
            try:
                BaseException.add_note(failure, message)
            except BaseException:
                # Keep physical fallback and later connection cleanup running
                # even when the rollback error cannot accept a safe note.
                pass
        # Failed rollback cannot leave a committable prefix in a pooled socket.
        for connection in connections:
            try:
                connection.invalidate()
            except BaseException:
                note("Connection quarantine failed; physical close will be attempted when a captured driver is available.")
                driver = drivers.get(connection)
                if driver is not None:
                    try:
                        driver.close()
                    except BaseException:
                        incomplete = True
                        note("Physical close failed; connection outcome is unknown.")
                elif not connection.closed and not connection.invalidated:
                    incomplete = True
        cleanup_state["quarantine_incomplete"] = incomplete
        raise

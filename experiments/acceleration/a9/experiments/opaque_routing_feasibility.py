"""Pure in-memory Engine/UOW experiment. No network, credentials or database.

Synthetic safe bytes are NOT ciphertext. No current Cryptalis hook is imported.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import io
import json
import logging
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

import sqlalchemy
from sqlalchemy import Column, LargeBinary, MetaData, Table, Text, Uuid, event, inspect
from sqlalchemy.engine import Engine, default
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, persistence, registry
from sqlalchemy.orm.attributes import NO_VALUE
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.types import TypeDecorator


PLAINTEXT = 'SYNTHETIC_PRIVATE_LOGICAL_VALUE_opaque_route'


class Pending:
    __slots__ = ()
    def __repr__(self):
        return '<pending-protected-input>'


@dataclass(repr=False)
class SyntheticSafe:
    body: bytes
    def __repr__(self):
        return '<synthetic-safe-bind>'


class OwnedDefaultFailure(Exception):
    pass


class OwnedProcessorFailure(Exception):
    pass


class OwnedConstructorFailure(Exception):
    pass


class FakeDriverFailure(Exception):
    pass


def leaves(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from leaves(item)
    elif isinstance(value, (tuple, list)):
        for item in value:
            yield from leaves(item)
    else:
        yield value


def assert_opaque(value):
    assert all(item != PLAINTEXT for item in leaves(value))
    assert PLAINTEXT not in repr(value)


def run_case(routed, callback_kind, failure=None):
    mapping = registry(metadata=MetaData())
    reports, callbacks, retained, executions = [], [], [], []
    producer_rows, compiled_rows, private = [], [], {}
    state = SimpleNamespace()

    class FakeCursor:
        description = None
        rowcount = 1
        lastrowid = None
        def execute(self, statement, parameters):
            assert not any(isinstance(item, (Pending, SyntheticSafe)) for item in leaves(parameters))
            if routed:
                assert_opaque(parameters)
            executions.append((statement, parameters))
            if failure == 'driver':
                raise FakeDriverFailure('owned fake driver failure')
        def executemany(self, statement, parameters):
            for group in parameters:
                self.execute(statement, group)
        def close(self):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()
        def rollback(self):
            pass
        def commit(self):
            pass
        def close(self):
            pass

    class FakeDBAPI:
        paramstyle = 'named'
        Error = FakeDriverFailure
        Binary = staticmethod(bytes)

    def call_default(context=None):
        callbacks.append('default')
        assert inspect(state.row).attrs.id.loaded_value is NO_VALUE
        if context is not None:
            values = context.get_current_parameters()
            assert values['secret'] == PLAINTEXT
            retained.append((context, values, context.compiled_parameters))
        if failure == 'default':
            raise OwnedDefaultFailure('owned default failure')
        return UUID(int=7001)

    def noarg_default():
        return call_default()

    def context_default(context):
        return call_default(context)

    class SafeOnly(TypeDecorator):
        impl = LargeBinary
        cache_ok = False
        def process_bind_param(self, value, dialect):
            assert isinstance(value, SyntheticSafe), 'Pending/plaintext cannot bind'
            if failure == 'processor':
                raise OwnedProcessorFailure('owned processor failure')
            return value.body

    table = Table('synthetic_row', mapping.metadata,
                  Column('id', Uuid, primary_key=True, autoincrement=False,
                         default=noarg_default if callback_kind == 'noarg' else context_default),
                  Column('secret', SafeOnly() if routed else Text(), nullable=False))
    class Row:
        pass
    mapping.map_imperatively(Row, table)
    state.row = Row(secret=PLAINTEXT)
    dialect = default.DefaultDialect(dbapi=FakeDBAPI(), paramstyle='named')

    original_defaults = default.DefaultExecutionContext._process_execute_defaults

    class RoutingContext(default.DefaultExecutionContext):
        @classmethod
        def _init_compiled(cls, *args, **kwargs):
            if failure == 'constructor':
                raise OwnedConstructorFailure('owned constructor failure')
            return super()._init_compiled(*args, **kwargs)

        def _process_execute_defaults(self):
            safe_groups = self.compiled_parameters
            logical_groups = []
            logical_pairs = []
            for group in safe_groups:
                matches = [entry for entry in compiled_rows if entry[1] is group]
                assert len(matches) == 1
                if callback_kind == 'context':
                    logical = dict(group)
                    logical['secret'] = private[group['secret']]
                    logical_groups.append(logical)
                    logical_pairs.append((group, logical))
            try:
                if callback_kind == 'context':
                    self.compiled_parameters = logical_groups
                return original_defaults(self)
            finally:
                # Restore opaque public context before constructor error handling.
                # Native callback-owned dictionaries stay ordinary and intact.
                if callback_kind == 'context':
                    for safe, logical in logical_pairs:
                        # These pairs were created together here, not an authority
                        # reconstruction: authority was captured at actual input
                        # and compiled output creation. No driver-row inference.
                        safe.update({key: value for key, value in logical.items() if key != 'secret'})
                    self.compiled_parameters = safe_groups
                if 'current_parameters' in self.__dict__:
                    del self.current_parameters
                for group in safe_groups:
                    if group.get('id') is not None:
                        group['secret'] = SyntheticSafe(b'PUBLIC_SYNTHETIC_SAFE:' + group['id'].bytes)

    if routed or failure == 'constructor':
        dialect.execution_ctx_cls = RoutingContext
    engine = Engine(StaticPool(creator=FakeConnection), dialect, URL.create('in-memory-probe'),
                    echo=False, hide_parameters=True)

    def inspect_surface(name, parameters, context=None):
        if routed:
            assert_opaque(parameters)
            if context is not None:
                assert_opaque(getattr(context, 'compiled_parameters', ()))
                assert context.__dict__.get('current_parameters') is None
        elif name in ('before_execute', 'before_cursor', 'after_execute'):
            assert PLAINTEXT in list(leaves(parameters)), 'Native collector calibration failed'
        reports.append(name)

    def before_execute(conn, statement, multiparams, params, options):
        inspect_surface('before_execute', multiparams or params)
    def before_cursor(conn, cursor, statement, parameters, context, many):
        inspect_surface('before_cursor', parameters, context)
    def after_execute(conn, statement, multiparams, params, options, result):
        inspect_surface('after_execute', multiparams or params, result.context)
    def handle_error(error_context):
        inspect_surface('handle_error', error_context.parameters, error_context.execution_context)
        statement_error = error_context.sqlalchemy_exception
        if statement_error is not None:
            inspect_surface('exception.params', getattr(statement_error, 'params', ()))

    for name, callback in [('before_execute', before_execute), ('before_cursor_execute', before_cursor),
                           ('after_execute', after_execute), ('handle_error', handle_error)]:
        event.listen(engine, name, callback)

    original_emit = persistence._emit_insert_statements
    original_construct = SQLCompiler.construct_params
    def emit(base_mapper, uow, mapper, target, insert, **kwargs):
        def records():
            for record in insert:
                marker = Pending()
                value = record[2]['secret']
                assert value == PLAINTEXT
                private[marker] = value
                record[2]['secret'] = marker
                producer_rows.append(record)
                yield record
        return original_emit(base_mapper, uow, mapper, target, records(), **kwargs)
    def construct(compiler, params=None, *args, **kwargs):
        result = original_construct(compiler, params, *args, **kwargs)
        matches = [record for record in producer_rows if record[2] is params]
        assert len(matches) == 1
        compiled_rows.append((matches[0], result))
        return result

    capture = io.StringIO()
    handler = logging.StreamHandler(capture)
    logger = logging.getLogger('sqlalchemy.engine')
    old_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    caught = None
    session = Session(engine, expire_on_commit=False)
    try:
        if routed:
            persistence._emit_insert_statements = emit
            SQLCompiler.construct_params = construct
        session.add(state.row)
        try:
            session.flush()
        except Exception as error:
            caught = error
            if routed:
                assert_opaque(getattr(error, 'params', ()))
                assert PLAINTEXT not in str(error)
            assert failure is not None, type(error).__name__
            assert not session.is_active
            assert inspect(state.row).attrs.id.loaded_value is NO_VALUE
            session.rollback()
        else:
            assert failure is None
            assert state.row.id == UUID(int=7001)
            assert inspect(state.row).persistent
        assert state.row.secret == PLAINTEXT
        if routed:
            assert PLAINTEXT not in capture.getvalue()
        retained_plain = all(values['secret'] == PLAINTEXT for _, values, _ in retained)
        dynamic_context_identity = [context.compiled_parameters is groups for context, _, groups in retained]
        if routed and callback_kind == 'context':
            assert retained_plain
            assert dynamic_context_identity == [False] * len(retained)
        elif callback_kind == 'context' and failure is None:
            assert dynamic_context_identity == [True]
        return {'routed': routed, 'callback': callback_kind, 'failure': failure,
                'callbacks': len(callbacks), 'driver_calls': len(executions),
                'surfaces': reports, 'error': None if caught is None else type(caught).__name__,
                'retained_callback_plain': retained_plain,
                'retained_context_list_identity': dynamic_context_identity}
    finally:
        persistence._emit_insert_statements = original_emit
        SQLCompiler.construct_params = original_construct
        session.close()
        engine.dispose()
        mapping.dispose()
        private.clear()
        logger.removeHandler(handler)
        logger.setLevel(old_level)


def main():
    # Both versions must be one of the exact inspected installed releases.
    expected = json.loads(Path(__file__).with_name('opaque_source_hashes.json').read_text())
    assert sqlalchemy.__version__ in expected
    source_root = Path(sqlalchemy.__file__).resolve().parent
    for relative, digest in expected[sqlalchemy.__version__].items():
        assert hashlib.sha256((source_root / relative).read_bytes()).hexdigest() == digest, relative
    rows = [run_case(False, kind) for kind in ('noarg', 'context')]
    rows += [run_case(True, kind, failure) for kind in ('noarg', 'context')
             for failure in (None, 'constructor', 'default', 'processor', 'driver')]
    print(json.dumps({'sqlalchemy': sqlalchemy.__version__, 'database': 'NONE: local fake DBAPI only',
                      'cases': rows, 'status': 'BOUNDED FEASIBILITY; context-reflection incompatibility observed'}, indent=2))


if __name__ == '__main__':
    main()

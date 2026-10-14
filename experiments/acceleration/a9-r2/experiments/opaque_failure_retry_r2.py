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
from sqlalchemy.exc import StatementError, DBAPIError
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


def run_case(routed, callback_kind, failure=None, two_rows=False):
    assert not two_rows or (callback_kind == "noarg" and failure is None)
    logical_value = PLAINTEXT + '|' + callback_kind + '|' + (failure or 'success')
    associations = []
    mapping = registry(metadata=MetaData())
    reports, callbacks, retained, executions = [], [], [], []
    producer_rows, compiled_rows, private = [], [], {}
    state = SimpleNamespace()
    stages, errors = [], []
    fault_types = {'constructor': OwnedConstructorFailure, 'default': OwnedDefaultFailure,
                   'processor': OwnedProcessorFailure, 'driver': FakeDriverFailure}
    fault = fault_types[failure]('owned ' + failure + ' failure') if failure else None
    fault_enabled = True
    def stage(name):
        stages.append(name)
        if failure == name and fault_enabled:
            raise fault

    class FakeCursor:
        description = None
        rowcount = 1
        lastrowid = None
        def execute(self, statement, parameters):
            assert not any(isinstance(item, (Pending, SyntheticSafe)) for item in leaves(parameters))
            if routed:
                assert_opaque(parameters)
            executions.append((statement, parameters))
            stage('driver')
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
        assert inspect(state.rows[len(callbacks) - 1] if two_rows else state.row).attrs.id.loaded_value is NO_VALUE
        if context is not None:
            values = context.get_current_parameters()
            assert values['secret'] == logical_value
            retained.append((context, values, context.compiled_parameters))
        stage('default')
        return UUID(int=7000 + len(callbacks)) if two_rows else UUID(int=7001)

    def noarg_default():
        return call_default()

    def context_default(context):
        return call_default(context)

    class SafeOnly(TypeDecorator):
        impl = LargeBinary
        cache_ok = False
        def process_bind_param(self, value, dialect):
            assert isinstance(value, SyntheticSafe), 'Pending/plaintext cannot bind'
            stage('processor')
            return value.body

    class NativeProcessor(TypeDecorator):
        impl = Text
        cache_ok = False
        def process_bind_param(self, value, dialect):
            assert any(value is row.secret for row in state.rows)
            stage('processor')
            return value

    table = Table('synthetic_row', mapping.metadata,
                  Column('id', Uuid, primary_key=True, autoincrement=False,
                         default=noarg_default if callback_kind == 'noarg' else context_default),
                  Column('secret', SafeOnly() if routed else NativeProcessor(), nullable=False))
    class Row:
        pass
    mapping.map_imperatively(Row, table)
    state.row = Row(secret=logical_value)
    state.rows = [state.row] + ([Row(secret=logical_value + '|second-distinct-marker')] if two_rows else [])
    dialect = default.DefaultDialect(dbapi=FakeDBAPI(), paramstyle='named')

    original_defaults = default.DefaultExecutionContext._process_execute_defaults

    class RoutingContext(default.DefaultExecutionContext):
        @classmethod
        def _init_compiled(cls, *args, **kwargs):
            stage('constructor')
            return super()._init_compiled(*args, **kwargs)

        def _process_execute_defaults(self):
            if not routed:
                return original_defaults(self)
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
                        matched = [entry for entry in compiled_rows if entry[1] is group]
                        assert len(matched) == 1
                        record = matched[0][0]
                        owners = [row for row in state.rows if inspect(row) is record[0]]
                        assert len(owners) == 1
                        token = group['secret']
                        assert token is record[2]['secret']
                        logical = private[token]  # Identity-keyed exact native input.
                        assert logical is owners[0].secret
                        body = b'PUBLIC_SYNTHETIC_SAFE:' + group['id'].bytes + b'|' + logical.encode()
                        # This public marker is intentionally visible in this NO-CRYPTO
                        # oracle. Encode as hex bytes to keep the logical string
                        # absent from ordinary event/parameter repr surfaces.
                        group['secret'] = SyntheticSafe(body.hex().encode('ascii'))
                        associations.append((record[0], token, group, logical))

    dialect.execution_ctx_cls = RoutingContext
    engine = Engine(StaticPool(creator=FakeConnection), dialect, URL.create('in-memory-probe'),
                    echo=False, hide_parameters=True)

    def inspect_surface(name, parameters, context=None):
        if routed:
            assert_opaque(parameters)
            if context is not None:
                assert_opaque(getattr(context, 'compiled_parameters', ()))
                assert context.__dict__.get('current_parameters') is None
        elif name in ('before_execute', 'before_cursor', 'after_execute', 'handle_error', 'exception.params'):
            assert any(row.secret in list(leaves(parameters)) for row in state.rows), 'Native collector calibration failed'
        reports.append(name)

    def before_execute(conn, statement, multiparams, params, options):
        inspect_surface('before_execute', multiparams or params)
    def before_cursor(conn, cursor, statement, parameters, context, many):
        inspect_surface('before_cursor', parameters, context)
    def after_execute(conn, statement, multiparams, params, options, result):
        inspect_surface('after_execute', multiparams or params, result.context)
    def handle_error(error_context):
        assert failure is not None and fault_enabled
        assert error_context.original_exception is fault
        assert error_context.sqlalchemy_exception.orig is fault
        errors.append(error_context)
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
                assert any(value is row.secret for row in state.rows)
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
    diagnostic_marker = 'PUBLIC_LOG_COLLECTOR_CALIBRATION'
    logger.info(diagnostic_marker)
    assert diagnostic_marker in capture.getvalue()
    capture.seek(0)
    capture.truncate(0)
    caught = None
    session = Session(engine, expire_on_commit=False)
    try:
        if routed:
            persistence._emit_insert_statements = emit
            SQLCompiler.construct_params = construct
        session.add_all(state.rows)
        failed_stages = []
        rollback_transient = None
        stale_tokens = []
        try:
            session.flush()
        except Exception as error:
            # An unrelated exception must fail this experiment, never count as
            # the requested injected failure.
            caught = error
            assert fault is not None
            assert type(error) is (DBAPIError if failure == 'driver' else StatementError)
            assert error.orig is fault
            assert error.__cause__ is fault
            assert len(errors) == 1
            assert errors[0].sqlalchemy_exception is error
            expected = ['constructor', 'default', 'processor', 'driver']
            assert stages == expected[:expected.index(failure) + 1], stages
            failed_stages = list(stages)
            assert len(callbacks) == (0 if failure == 'constructor' else 1)
            assert len(executions) == (1 if failure == 'driver' else 0)
            assert 'after_execute' not in reports
            assert ('before_cursor' in reports) == (failure == 'driver')
            if routed:
                assert_opaque(error.params)
                assert logical_value not in str(error)
            assert not session.is_active
            assert session.in_transaction()
            assert inspect(state.row).attrs.id.loaded_value is NO_VALUE
            assert inspect(state.row).transient
            assert state.row.secret == logical_value
            session.rollback()
            assert session.is_active and not session.in_transaction()
            assert inspect(state.row).transient
            rollback_transient = True
            # Explicit experiment operation teardown, not a runtime lifecycle claim.
            stale_tokens = list(private)
            private.clear()
            producer_rows.clear()
            compiled_rows.clear()
            fault_enabled = False
            stages.clear()
            session.add(state.row)
            session.flush()  # Must actually succeed; no exception-catching here.
            assert stages == ['constructor', 'default', 'processor', 'driver']
            assert all(new is not old for new in private for old in stale_tokens)
            assert len(private) == (1 if routed else 0)
            if routed:
                assert len(producer_rows) == len(compiled_rows) == 1
                assert producer_rows[0][0] is inspect(state.row)
                assert isinstance(producer_rows[0][2]['secret'], Pending)
                assert producer_rows[0][2]['secret'] in private
                assert isinstance(compiled_rows[0][1]['secret'], SyntheticSafe)
        else:
            assert failure is None
            assert stages == (['constructor', 'default', 'processor', 'driver'] * 2 if two_rows else ['constructor', 'default', 'processor', 'driver'])
        assert session.is_active
        assert state.row.id == UUID(int=7001)
        assert inspect(state.row).persistent
        assert state.row.secret == logical_value
        assert len(executions) == (2 if failure == 'driver' or two_rows else 1)
        assert reports.count('after_execute') == len(state.rows)
        assert capture.getvalue(), 'Ordinary logging collector must be nonempty'
        assert 'INSERT INTO synthetic_row' in capture.getvalue()
        assert 'hidden due to hide_parameters=True' in capture.getvalue()
        assert logical_value not in capture.getvalue()
        if routed:
            expected_by_id = {row.id.hex: b'PUBLIC_SYNTHETIC_SAFE:' + row.id.bytes + b'|' + row.secret.encode() for row in state.rows}
            assert len(expected_by_id) == len(state.rows)
            # Independent owner-derived expected output; does not use the private
            # lookup or receipt list to infer which row a driver value belongs to.
            for statement, parameters in executions:
                assert bytes.fromhex(parameters['secret'].decode('ascii')) == expected_by_id[parameters['id']]
            assert associations
            assert all(any(owner is inspect(row) for row in state.rows) for owner, _, _, _ in associations)
            assert {id(owner) for owner, _, _, _ in associations} == {id(inspect(row)) for row in state.rows}
        retained_plain = all(values['secret'] == logical_value for _, values, _ in retained)
        dynamic_context_identity = [context.compiled_parameters is groups for context, _, groups in retained]
        if routed and callback_kind == 'context':
            assert retained_plain
            assert dynamic_context_identity == [False] * len(retained)
        elif callback_kind == 'context' and failure is None:
            assert dynamic_context_identity == [True]
        return {'routed': routed, 'callback': callback_kind, 'failure': failure, 'row_count': len(state.rows),
                'callbacks': len(callbacks), 'driver_calls': len(executions),
                'surfaces': reports, 'error': None if caught is None else type(caught).__name__,
                'retained_callback_plain': retained_plain,
                'failed_stages': failed_stages, 'retry_stages': stages if failure else [],
                'exact_original_exception_identity': caught.orig is fault if caught else None,
                'rollback_transient': rollback_transient,
                'public_marker_association_checked': bool(associations),
                'log_capture_nonempty': bool(capture.getvalue()),
                'diagnostic_marker_detected': True,
                'native_error_parameters_calibrated': not routed and failure is not None,
                'retry_fresh_tokens': len(stale_tokens) == 1 and len(private) == 1 if routed and failure else None,
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
    rows = []
    for failure in ('constructor', 'default', 'processor', 'driver'):
        native = run_case(False, 'noarg', failure)
        routed = run_case(True, 'noarg', failure)
        for key in ('callbacks', 'driver_calls', 'surfaces', 'error', 'failed_stages',
                    'retry_stages', 'exact_original_exception_identity', 'rollback_transient'):
            assert native[key] == routed[key], (failure, key, native[key], routed[key])
        rows.extend([native, routed])
    rows.extend([run_case(False, 'noarg', two_rows=True), run_case(True, 'noarg', two_rows=True)])
    # Preserve the explicit broader-context identity counterexample separately.
    rows.extend([run_case(False, 'context'), run_case(True, 'context')])
    print(json.dumps({'sqlalchemy': sqlalchemy.__version__, 'database': 'NONE: local fake DBAPI only',
                      'cases': rows, 'status': 'BOUNDED FEASIBILITY; context-reflection incompatibility observed'}, indent=2))


if __name__ == '__main__':
    main()

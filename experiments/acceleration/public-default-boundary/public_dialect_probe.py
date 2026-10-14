"""Public event/type diagnostic only. Public markers; no encryption claim or database."""
import hashlib, json
from pathlib import Path
from uuid import UUID
import sqlalchemy
from sqlalchemy import Column, MetaData, Table, Text, Uuid, event, inspect
from sqlalchemy.engine import Engine, default
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, registry
from sqlalchemy.pool import StaticPool
from sqlalchemy.types import TypeDecorator
from sqlalchemy.exc import StatementError
from sqlalchemy.orm.attributes import NO_VALUE

MARKER = 'PUBLIC_DIAGNOSTIC_MARKER'
class Fault(Exception): pass
class DriverError(Exception): pass
class Cursor:
    description = None
    rowcount = 1
    lastrowid = None
    def __init__(self, seen): self.seen = seen
    def execute(self, statement, parameters): self.seen.append(dict(parameters))
    def executemany(self, statement, parameters):
        for p in parameters: self.execute(statement, p)
    def close(self): pass
class Connection:
    def __init__(self, seen): self.seen = seen
    def cursor(self): return Cursor(self.seen)
    def rollback(self): pass
    def commit(self): pass
    def close(self): pass
class DBAPI:
    paramstyle = 'named'
    Error = DriverError

def run(kind, many):
    seen, retained, stages, errors = [], [], [], []
    fault = (DriverError if kind == 'dbapi' else Fault)('public diagnostic fault')
    failing = True
    def stamp(ctx):
        stages.append('default')
        retained.append((ctx, ctx.compiled_parameters, ctx.get_current_parameters()))
        return len(retained)
    class Value(TypeDecorator):
        impl = Text
        cache_ok = False
        def process_bind_param(self, value, dialect):
            stages.append('bind')
            return value
    mapping = registry(metadata=MetaData())
    from sqlalchemy import Integer
    table = Table('probe', mapping.metadata, Column('id', Uuid, primary_key=True), Column('stamp', Integer, default=stamp), Column('value', Value()))
    class Row: pass
    mapping.map_imperatively(Row, table)
    engine = Engine(StaticPool(creator=lambda: Connection(seen)), default.DefaultDialect(dbapi=DBAPI()), URL.create('public_fake'), hide_parameters=True)
    @event.listens_for(engine, 'before_cursor_execute')
    def before(conn, cursor, statement, params, context, many): stages.append('cursor')
    @event.listens_for(engine, 'do_executemany' if many else 'do_execute')
    def execute(cursor, statement, params, context):
        stages.append('dialect_event')
        if failing: raise fault
    @event.listens_for(engine, 'handle_error')
    def error(ctx):
        stages.append('handle_error')
        errors.append({'exact_original':ctx.original_exception is fault, 'outer_type':type(ctx.sqlalchemy_exception).__name__, 'marker_visible':MARKER in repr(ctx.parameters)})
    @event.listens_for(engine, 'after_cursor_execute')
    def after(conn, cursor, statement, params, context, many): stages.append('after_cursor')
    rows = [Row(id=UUID(int=i+1), value=MARKER) for i in range(2 if many else 1)]
    session = Session(engine)
    session.add_all(rows)
    try: session.flush()
    except Exception as exc:
        result = {'event':'do_executemany' if many else 'do_execute', 'fault_class':kind, 'stages':list(stages), 'error_type':type(exc).__name__, 'exact_raw_fault':exc is fault, 'wrapped_exact_fault':isinstance(exc,StatementError) and exc.orig is fault, 'cause_exact':exc.__cause__ is fault, 'handle_error':list(errors), 'inactive':not session.is_active, 'transaction':session.in_transaction(), 'stamp_absent':all(inspect(row).attrs.stamp.loaded_value is NO_VALUE for row in rows), 'driver_calls':len(seen), 'retained_list_identity':all(ctx.compiled_parameters is groups for ctx,groups,group in retained)}
        assert result['inactive'] and result['transaction'] and result['stamp_absent'] and not seen
        assert len(errors) == 1 and errors[0]['exact_original']
        assert result['retained_list_identity']
        if kind == 'dbapi':
            assert result['error_type'] == 'DBAPIError' and result['wrapped_exact_fault'] and result['cause_exact']
        else: assert result['exact_raw_fault'] and not result['wrapped_exact_fault']
        session.rollback()
        assert session.is_active and not session.in_transaction()
        failing = False
        session.add_all(rows)
        session.flush()
        result['retry_persistent'] = all(inspect(row).persistent for row in rows)
        result['callback_count_after_retry'] = len(retained)
        result['all_stages'] = stages
        assert result['retry_persistent'] and len(retained) == 2*len(rows)
        assert len(seen) == len(rows)
    else: raise AssertionError('fault not reached')
    session.close()
    engine.dispose()
    mapping.dispose()
    return result

pins = json.loads((Path(__file__).resolve().parent.parent / 'candidate-opaque-routing-feasibility-r2-20261014/experiments/opaque_source_hashes.json').read_text())[sqlalchemy.__version__]
root = Path(sqlalchemy.__file__).parent
assert all(hashlib.sha256((root / p).read_bytes()).hexdigest() == digest for p,digest in pins.items())
results = [run(kind,many) for kind in ('ordinary','dbapi') for many in (False,True)]
print(json.dumps({'sqlalchemy':sqlalchemy.__version__,'source_pins_verified':len(pins),'cases':results},indent=2))

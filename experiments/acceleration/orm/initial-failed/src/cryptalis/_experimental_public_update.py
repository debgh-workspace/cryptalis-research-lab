"""Off-by-default, owned-lab UPDATE of fully public mapped tables only.

This is not protected-field bulk UPDATE or a production-qualified capability.
Native SQLAlchemy owns mutation, RETURNING, synchronization and transactions.
The experiment admits only explicit assignments and public single-table
predicates after a locked conservative catalog inventory. It neither changes
query scope nor grants database privileges.
"""
from contextvars import ContextVar
from dataclasses import dataclass

from sqlalchemy import (BigInteger, Boolean, Date, DateTime, Integer, Interval,
                        SmallInteger, String, Table, Text, Time, Uuid, text)
from sqlalchemy.sql import operators, visitors
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.elements import (BinaryExpression, BindParameter,
    BooleanClauseList, ColumnClause, False_, Grouping, Null, True_)
from sqlalchemy.sql.sqltypes import NullType

from . import _experimental_public_delete as _inventory_helpers


# Exact ordinary SQLAlchemy types exclude user-defined bind/result behavior.
_TYPES = (BigInteger, Boolean, Date, DateTime, Integer, Interval, SmallInteger,
          String, Text, Time, Uuid)
_ASSIGNMENT_TYPES = (BigInteger, Boolean, Integer, SmallInteger, String, Text)
_permit = ContextVar('cryptalis_experimental_public_update', default=None)


@dataclass
class UpdatePermit:
    owner: object
    session: object
    connection: object
    statement: object
    table: object
    parameters: dict
    stage: str = 'new'
    executed_statement: object = None


def _assignment_columns(statement, table):
    values = statement._values
    if not values or statement._ordered_values is not None:
        return None
    columns = []
    for key, value in values.items():
        column = table.c.get(key) if type(key) is str else next(
            (c for c in table.c if isinstance(key, ColumnClause) and key.shares_lineage(c)), None)
        if (column is None or column.primary_key or column.foreign_keys or
                type(column.type) not in _ASSIGNMENT_TYPES or
                not isinstance(value, (BindParameter, Null))):
            return None
        columns.append(column)
    return tuple(columns)


def target(owner, statement):
    if not isinstance(statement, Update):
        return None
    table = statement.table._deannotate()
    if (not isinstance(table, Table) or not table.schema or
            not any(table is item for item in getattr(owner, '_experimental_public_update_tables', ())) or
            table.name.startswith('_cryptalis') or table.schema.startswith('pg_') or
            table.schema == 'information_schema' or
            table.schema not in {model['schema'] for model in owner.document['models']}):
        return None
    mappers = [mapper for mapper in owner.mapping.mappers if mapper.local_table is table]
    if (len(mappers) != 1 or mappers[0].inherits is not None or
            mappers[0].persist_selectable is not table or mappers[0].version_id_col is not None or
            any((table.schema, table.name) == (b.column.table.schema, b.column.table.name) for b in owner.bindings)):
        return None
    if (statement._prefixes or statement._hints or statement._independent_ctes or
            statement._with_options or statement._return_defaults or statement.dialect_kwargs):
        return None
    if any(type(c.type) not in _TYPES or c.onupdate is not None or
           c.server_onupdate is not None or c.computed is not None for c in table.c):
        return None
    if _assignment_columns(statement, table) is None:
        return None
    allowed_binary = (operators.eq, operators.ne, operators.lt, operators.le,
                      operators.gt, operators.ge, operators.in_op,
                      operators.not_in_op, operators.is_, operators.is_not)
    for node in visitors.iterate(statement):
        if node is statement:
            continue
        if isinstance(node, Table):
            if node._deannotate() is not table:
                return None
        elif isinstance(node, ColumnClause):
            if (node.is_literal or node.table is None or node.table._deannotate() is not table or
                    not any(node.shares_lineage(c) for c in table.c) or type(node.type) not in _TYPES):
                return None
        elif isinstance(node, BindParameter):
            if node.callable is not None or node.literal_execute or type(node.type) not in (*_TYPES, NullType):
                return None
        elif isinstance(node, BinaryExpression):
            if node.operator not in allowed_binary:
                return None
        elif isinstance(node, BooleanClauseList):
            if node.operator not in (operators.and_, operators.or_):
                return None
        elif not isinstance(node, (Grouping, Null, True_, False_)):
            return None
    return table


# DELETE's inventory already refuses custom types, expressions, rules, RLS,
# inheritance and unreviewed indexes. UPDATE additionally excludes effects
# that DELETE does not invoke: checks, outgoing FKs and generated columns.
_UPDATE_INVENTORY_SQL = """
SELECT baseline.qualified
 AND c.oid=:expected_oid
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_constraint k
     WHERE (k.conrelid=c.oid AND k.contype IN ('c','f','x'))
        OR (k.confrelid=c.oid AND k.contype='f'))
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_attribute a
     WHERE a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped
       AND (a.attgenerated<>'' OR a.attidentity<>''))
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_index i
     JOIN pg_catalog.pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=ANY(i.indkey)
     WHERE i.indrelid=c.oid AND i.indisprimary
       AND a.attname::text=ANY(CAST(:assigned_columns AS text[])))
FROM (""" + _inventory_helpers._INVENTORY_SQL + """) AS baseline(qualified)
CROSS JOIN pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname=:schema AND c.relname=:table
"""


def prepare(session, statement, parameters):
    owner = session._owner
    table = target(owner, statement)
    if table is None or (parameters is not None and type(parameters) is not dict):
        raise owner._control_error()
    parameters = {} if parameters is None else dict(parameters)
    names = {node.key for node in visitors.iterate(statement) if isinstance(node, BindParameter)}
    # Connection.execute may derive extra SET columns from parameter keys.
    # Only explicitly present statement binds may be supplied by this profile.
    if any(type(key) is not str or key not in names for key in parameters):
        raise owner._control_error()
    connection = session.connection()
    oid = _inventory_helpers._relation_oid(session, connection, table)
    quote = connection.dialect.identifier_preparer.quote_identifier
    lock = text('LOCK TABLE ONLY ' + quote(table.schema) + '.' + quote(table.name) +
                ' IN SHARE ROW EXCLUSIVE MODE NOWAIT')
    _inventory_helpers._execute_inventory(session, connection, lock, {}).close()
    verdict = _inventory_helpers._execute_inventory(session, connection, text(_UPDATE_INVENTORY_SQL), {
        'schema': table.schema, 'table': table.name, 'expected_oid': oid,
        'owned_payload_columns': [], 'owned_search_indexes': [], 'allowed_incoming_fks': [],
        'assigned_columns': [c.name for c in _assignment_columns(statement, table)],
    }).scalar_one_or_none()
    if verdict is not True:
        raise owner._control_error()
    return UpdatePermit(owner, session, connection, statement._deannotate(), table, parameters)


def admitted(owner, statement):
    permit = _permit.get()
    if permit is None or not isinstance(statement, Update):
        return False
    operation = owner._check()
    return (permit.owner is owner and permit.session is operation.session and
            not operation.flushing and statement._deannotate() is permit.statement and
            target(owner, statement) is permit.table)


def before_execute(owner, connection, statement, multiparams, parameters):
    if not admitted(owner, statement):
        raise owner._control_error()
    permit = _permit.get()
    if (permit.connection is not connection or permit.stage != 'new' or
            multiparams or dict(parameters) != permit.parameters):
        raise owner._control_error()
    permit.executed_statement = statement
    permit.stage = 'prepared'


def check_cursor(owner, context):
    permit = _permit.get()
    if (permit is None or permit.stage != 'prepared' or
            permit.connection is not context.root_connection or
            context.compiled is None or context.compiled.statement is not permit.executed_statement or
            context.executemany or not admitted(owner, context.compiled.statement)):
        raise owner._control_error()
    permit.stage = 'used'

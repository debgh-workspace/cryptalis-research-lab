"""Private, off-by-default public DELETE experiment. Not a qualified capability.

Only explicit owned-lab table objects can opt in. No caller execution option
creates authority. Broad bulk DML, protected predicates/results and effectful schemas remain
outside this experiment until separately proved. A separate private opt-in
permits only compiled single-tenant storage-only payload columns under the
same explicit table allowlist and conservative effect inventory. A separate
private equality-only opt-in validates exact owned search indexes. A further
private one-hop public-child CASCADE profile uses explicit table allowlists,
strong NOWAIT locks and a savepoint-contained inventory. All other effects
remain refused; this module is not production-qualified.
"""
from contextvars import ContextVar
from dataclasses import dataclass
from uuid import uuid4
from sqlalchemy import Table,text
from sqlalchemy.sql import visitors,operators
from sqlalchemy.sql.dml import Delete
from sqlalchemy.sql.elements import (ColumnClause,BindParameter,BinaryExpression,
    BooleanClauseList,Grouping,Null,True_,False_)
from sqlalchemy.types import TypeDecorator

_inventory = ContextVar('cryptalis_experimental_delete_inventory',default=None)
_result_boundary = ContextVar('cryptalis_experimental_delete_result_boundary',default=None)

@dataclass
class InventoryPermit:
    owner: object
    session: object
    connection: object
    statement: object
    parameters: dict
    stage: str='new'

@dataclass
class ResultBoundary:
    session: object
    attempted: bool=False
    cleaned: bool=False



def resolve_public_schema_pins(owner, connection):
    """Freeze native attachment-time resolution, without granting DML authority.

    Only direct, ordinary public tables in an already compiled schema qualify.
    Private DELETE allowlists and locked effect inventories remain mandatory.
    No guessing by table name or schema translation is allowed.
    """
    schemas = {model["schema"] for model in owner.document["models"]}
    protected = {(model["schema"], model["table"]) for model in owner.document["models"]}
    protected_models = {model["model"] for model in owner.document["models"]}
    pins = []
    for mapper in owner.mapping.mappers:
        table = mapper.local_table
        if (mapper.class_.__name__ in protected_models or not isinstance(table, Table) or
                table.schema is not None or mapper.inherits is not None or
                mapper.persist_selectable is not table):
            continue
        quoted = connection.dialect.identifier_preparer.quote_identifier(table.name)
        row = connection.execute(text("""
            SELECT n.nspname, c.relname, c.relkind
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
            WHERE c.oid=pg_catalog.to_regclass(:name)
        """), {"name": quoted}).one_or_none()
        if (row is None or row[0] not in schemas or row[2] != 'r' or
                (row[0], row[1]) in protected or table.name.startswith('_cryptalis')):
            continue
        pins.append((table, row[0], row[1]))
    return tuple(pins)


def _protected_payload_columns(owner, table):
    bindings = [b for b in owner.bindings
                if (table.schema, table.name) == (b.column.table.schema, b.column.table.name)]
    equality_profile = getattr(owner, "_experimental_protected_equality_delete", False) is True
    storage_profile = getattr(owner, "_experimental_protected_storage_delete", False) is True
    if (not bindings or not (equality_profile or storage_profile)
            or any((b.descriptor.equality and not equality_profile)
                   or b.descriptor.tenant_codec != "single-tenant-uuid/v1" for b in bindings)
            or len({b.descriptor.table_id for b in bindings}) != 1):
        return None
    return tuple(b.storage_column or b.column.name for b in bindings)


def target(owner,statement):
    if not isinstance(statement,Delete):return None
    configured=getattr(owner,'_experimental_public_delete_tables',())
    table=statement.table._deannotate()
    if not any(table is item for item in configured):return None
    if not isinstance(table,Table) or not table.schema:return None
    if table.name.startswith('_cryptalis') or table.schema.startswith('pg_') or table.schema=='information_schema':return None
    if table.schema not in {model['schema'] for model in owner.document['models']}:return None
    if not any(mapper.local_table is table and mapper.inherits is None and
               mapper.persist_selectable is table for mapper in owner.mapping.mappers):return None
    if (any((table.schema,table.name)==(b.column.table.schema,b.column.table.name) for b in owner.bindings)
            and _protected_payload_columns(owner, table) is None):return None
    if owner.protected(statement) or any(owner.protected(column) for column in statement.exported_columns):return None
    allowed_binary=(operators.eq,operators.ne,operators.lt,operators.le,operators.gt,
                    operators.ge,operators.in_op,operators.not_in_op,operators.is_,operators.is_not)
    for node in visitors.iterate(statement):
        if node is statement:continue
        if isinstance(node,Table):
            if node._deannotate() is not table:return None
        elif isinstance(node,ColumnClause):
            if node.is_literal or node.table is None or node.table._deannotate() is not table:return None
            if not any(node.shares_lineage(c) for c in table.c):return None
            if isinstance(node.type,TypeDecorator):return None
        elif isinstance(node,BindParameter):
            if node.callable is not None or isinstance(node.type,TypeDecorator):return None
        elif isinstance(node,BinaryExpression):
            if node.operator not in allowed_binary:return None
        elif isinstance(node,BooleanClauseList):
            if node.operator not in (operators.and_,operators.or_):return None
        elif not isinstance(node,(Grouping,Null,True_,False_)):return None
    return table


def inspect_inventory(owner,connection,statement,parameters=None,*,driver=False):
    permit=_inventory.get()
    if permit is None:return False
    operation=owner._check()
    if (permit.owner is not owner or permit.connection is not connection or
        permit.statement is not statement or permit.session is not operation.session or
        permit.stage!=('prepared' if driver else 'new') or
        (not driver and parameters!=permit.parameters)):
        raise owner._control_error()
    permit.stage='used' if driver else 'prepared'
    return True


def _execute_inventory(session,connection,statement,parameters):
    permit=InventoryPermit(session._owner,session,connection,statement,parameters)
    token=_inventory.set(permit)
    try:
        result=connection.execute(statement,parameters,execution_options={"compiled_cache":None})
        if permit.stage!='used':raise session._owner._control_error()
        return result
    finally:_inventory.reset(token)



class _SearchInventoryConnection:
    """Bridge only the existing internal validator's static, bound catalog SQL."""
    def __init__(self, session, connection):
        self.session = session
        self.connection = connection
        self.dialect = connection.dialect

    def exec_driver_sql(self, statement, parameters=()):
        parts = statement.split("%s")
        if len(parts) != len(parameters) + 1:
            raise self.session._owner._control_error()
        compiled = parts[0]
        for number, part in enumerate(parts[1:]):
            compiled += ":catalog_" + str(number) + part
        binds = {"catalog_" + str(number): value for number, value in enumerate(parameters)}
        return _execute_inventory(self.session, self.connection, text(compiled), binds)


def _validated_search_index_oids(session, connection, table):
    owner = session._owner
    bindings = [b for b in owner.bindings if b.descriptor.equality
                and (table.schema, table.name) == (b.column.table.schema, b.column.table.name)]
    if not bindings:
        return []
    if getattr(owner, "_experimental_protected_equality_delete", False) is not True:
        raise owner._control_error()
    from ._sqlalchemy_search import validate_search_storage
    models = [m for m in owner.document["models"]
              if (m["schema"], m["table"]) == (table.schema, table.name)]
    if len(models) != 1:
        raise owner._control_error()
    model = models[0]
    path = _execute_inventory(session, connection,
                              text("SELECT pg_catalog.current_setting('search_path')"), {}).scalar_one()
    result = []
    try:
        proxy = _SearchInventoryConnection(session, connection)
        for binding in bindings:
            fields = [f for f in model["fields"] if f["column"] == binding.column.name]
            if len(fields) != 1:
                raise owner._control_error()
            field = fields[0]
            physical = {**field, "column": binding.storage_column or binding.column.name}
            try:
                validate_search_storage(proxy, model, physical)
            except ValueError:
                raise owner._control_error() from None
            index_name = "_cryptalis_" + field["field_id"].replace("-", "") + "_eq"
            oid = _execute_inventory(session, connection, text("""
                SELECT i.indexrelid::bigint FROM pg_catalog.pg_index i
                JOIN pg_catalog.pg_class t ON t.oid=i.indrelid
                JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
                JOIN pg_catalog.pg_class ix ON ix.oid=i.indexrelid
                WHERE n.nspname=:schema AND t.relname=:table AND ix.relname=:index
                """), {"schema": table.schema, "table": table.name, "index": index_name}).scalar_one()
            result.append(oid)
    finally:
        restored = _execute_inventory(session, connection,
                                      text("SELECT pg_catalog.set_config('search_path', :prior_path, true)"),
                                      {"prior_path": path}).scalar_one()
        if restored != path:
            raise owner._control_error()
    return result


_INVENTORY_SQL="""
SELECT pg_catalog.current_setting('transaction_isolation')='read committed'
 AND c.relkind='r' AND NOT c.relispartition AND NOT c.relrowsecurity AND NOT c.relforcerowsecurity
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_inherits i WHERE i.inhrelid=c.oid OR i.inhparent=c.oid)
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_trigger t WHERE t.tgrelid=c.oid AND NOT t.tgisinternal)
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_rewrite r WHERE r.ev_class=c.oid)
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_constraint f WHERE f.contype='f' AND f.confrelid=c.oid AND NOT (f.oid=ANY(CAST(:allowed_incoming_fks AS oid[]))))
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_attribute a
   JOIN pg_catalog.pg_type t ON t.oid=a.atttypid
   JOIN pg_catalog.pg_namespace tn ON tn.oid=t.typnamespace
   WHERE a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped
   AND (tn.nspname<>'pg_catalog' OR t.typtype<>'b' OR
        (t.typname NOT IN ('uuid','text','varchar','int2','int4','int8','bool','date','timestamp','timestamptz','time','timetz','interval')
        AND NOT (t.typname='bytea' AND a.attname::text=ANY(CAST(:owned_payload_columns AS text[]))))))
 AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_index i
   JOIN pg_catalog.pg_class ic ON ic.oid=i.indexrelid
   JOIN pg_catalog.pg_am am ON am.oid=ic.relam
   WHERE i.indrelid=c.oid AND ((i.indexprs IS NOT NULL AND NOT (i.indexrelid=ANY(CAST(:owned_search_indexes AS oid[])))) OR i.indpred IS NOT NULL
       OR NOT i.indisvalid OR am.amname<>'btree'
       OR EXISTS(SELECT 1 FROM pg_catalog.unnest(i.indclass) oc(oid)
           JOIN pg_catalog.pg_opclass o ON o.oid=oc.oid
           JOIN pg_catalog.pg_namespace onsp ON onsp.oid=o.opcnamespace
           WHERE onsp.nspname<>'pg_catalog')))
FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
WHERE n.nspname=:schema AND c.relname=:table
"""



_CASCADE_EDGES = text("""
SELECT f.oid::bigint AS oid, f.conrelid::bigint AS child_oid,
       n.nspname AS child_schema, c.relname AS child_table,
       pg_catalog.pg_get_constraintdef(f.oid, true) AS definition,
       (f.confdeltype='c' AND f.confupdtype='a' AND f.confmatchtype='s'
        AND NOT f.condeferrable AND NOT f.condeferred AND f.convalidated
        AND pg_catalog.cardinality(f.conkey)=1 AND pg_catalog.cardinality(f.confkey)=1
        AND a.atttypid='pg_catalog.uuid'::pg_catalog.regtype
        AND p.atttypid='pg_catalog.uuid'::pg_catalog.regtype AND p.attname=:record_column
        AND f.conpfeqop=ARRAY['pg_catalog.=(uuid,uuid)'::pg_catalog.regoperator::oid]
        AND f.conppeqop=ARRAY['pg_catalog.=(uuid,uuid)'::pg_catalog.regoperator::oid]
        AND f.conffeqop=ARRAY['pg_catalog.=(uuid,uuid)'::pg_catalog.regoperator::oid]) AS qualified
FROM pg_catalog.pg_constraint f JOIN pg_catalog.pg_class c ON c.oid=f.conrelid
JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
LEFT JOIN pg_catalog.pg_attribute a ON a.attrelid=f.conrelid AND a.attnum=f.conkey[1]
LEFT JOIN pg_catalog.pg_attribute p ON p.attrelid=f.confrelid AND p.attnum=f.confkey[1]
WHERE f.contype='f' AND f.confrelid=:root_oid ORDER BY f.oid
""")


def _relation_oid(session, connection, table):
    return _execute_inventory(session, connection, text("""
        SELECT c.oid::bigint FROM pg_catalog.pg_class c
        JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
        WHERE n.nspname=:schema AND c.relname=:table
        """), {"schema": table.schema, "table": table.name}).scalar_one()


def _prepare_public_children(session, connection, root):
    owner = session._owner
    models = [m for m in owner.document["models"]
              if (m["schema"], m["table"]) == (root.schema, root.name)]
    if len(models) != 1 or models[0]["record"]["codec"] != "uuid16/v1":
        raise owner._control_error()
    savepoint = "_cryptalis_delete_" + uuid4().hex
    _execute_inventory(session, connection, text("SAVEPOINT " + savepoint), {}).close()
    try:
        root_oid = _relation_oid(session, connection, root)
        parameters = {"root_oid": root_oid, "record_column": models[0]["record"]["column"]}
        edges = [dict(row) for row in _execute_inventory(session, connection, _CASCADE_EDGES, parameters).mappings()]
        if len(edges) > 16 or len({edge["child_oid"] for edge in edges}) != len(edges):
            raise owner._control_error()
        tables = {root_oid: root}
        for edge in edges:
            if edge["qualified"] is not True or edge["child_oid"] == root_oid or edge["child_schema"] != root.schema:
                raise owner._control_error()
            configured = [t for t in getattr(owner, "_experimental_public_delete_tables", ())
                          if isinstance(t, Table) and (t.schema, t.name) == (edge["child_schema"], edge["child_table"])]
            if len(configured) != 1:
                raise owner._control_error()
            child = configured[0]
            if (child.name.startswith('_cryptalis') or any((b.column.table.schema, b.column.table.name) == (child.schema, child.name)
                    for b in owner.bindings) or not any(m.local_table is child and m.inherits is None and m.persist_selectable is child
                                                       for m in owner.mapping.mappers)):
                raise owner._control_error()
            tables[edge["child_oid"]] = child
        quote = connection.dialect.identifier_preparer.quote
        for oid, table in sorted(tables.items()):
            lock = text('LOCK TABLE ONLY ' + quote(table.schema) + '.' + quote(table.name) + ' IN SHARE ROW EXCLUSIVE MODE NOWAIT')
            _execute_inventory(session, connection, lock, {}).close()
        if any(_relation_oid(session, connection, table) != oid for oid, table in tables.items()):
            raise owner._control_error()
        repeated = [dict(row) for row in _execute_inventory(session, connection, _CASCADE_EDGES, parameters).mappings()]
        if repeated != edges:
            raise owner._control_error()
        for oid, table in sorted(tables.items()):
            is_root = oid == root_oid
            index_oids = _validated_search_index_oids(session, connection, table) if is_root else []
            verdict = _execute_inventory(session, connection, text(_INVENTORY_SQL), {
                "schema": table.schema, "table": table.name,
                "owned_payload_columns": list(_protected_payload_columns(owner, table) or ()) if is_root else [],
                "owned_search_indexes": index_oids,
                "allowed_incoming_fks": [edge["oid"] for edge in edges] if is_root else [],
            }).scalar_one_or_none()
            if verdict is not True:
                raise owner._control_error()
    except BaseException:
        _execute_inventory(session, connection, text("ROLLBACK TO SAVEPOINT " + savepoint), {}).close()
        _execute_inventory(session, connection, text("RELEASE SAVEPOINT " + savepoint), {}).close()
        raise
    _execute_inventory(session, connection, text("RELEASE SAVEPOINT " + savepoint), {}).close()
    return root


def prepare(session,statement):
    table=target(session._owner,statement)
    if table is None:raise session._owner._control_error()
    connection=session.connection()
    if (getattr(session._owner, "_experimental_public_child_cascade_delete", False) is True
            and _protected_payload_columns(session._owner, table) is not None):
        return _prepare_public_children(session, connection, table)
    quote=connection.dialect.identifier_preparer.quote
    lock=text('LOCK TABLE ONLY '+quote(table.schema)+'.'+quote(table.name)+' IN ROW EXCLUSIVE MODE NOWAIT')
    _execute_inventory(session,connection,lock,{}).close()
    search_indexes = _validated_search_index_oids(session, connection, table)
    verdict=_execute_inventory(session,connection,text(_INVENTORY_SQL),
                               {'schema':table.schema,'table':table.name,
                                'owned_payload_columns':list(_protected_payload_columns(session._owner, table) or ()),
                                'owned_search_indexes':search_indexes,'allowed_incoming_fks':[]}).scalar_one_or_none()
    if verdict is not True:raise session._owner._control_error()
    return table

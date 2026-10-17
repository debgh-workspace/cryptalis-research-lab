from copy import copy
"""Bounded text storage and equality through public SQLAlchemy hooks.

The host supplies a trusted lock and authenticated tenant scope. This module
does not migrate schemas or qualify external writers. Research prototype.
"""

from contextvars import ContextVar
from dataclasses import dataclass, field
from functools import wraps
from hashlib import sha256
import json
import re
from uuid import UUID

from sqlalchemy import __version__ as _sqlalchemy_version
from sqlalchemy import BigInteger, LargeBinary, Text, Uuid, event, func, inspect, type_coerce
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncSessionTransaction
from sqlalchemy.util.concurrency import await_only
from sqlalchemy.orm import Session, registry
from sqlalchemy.orm.attributes import NO_VALUE
from sqlalchemy.sql import operators, visitors
from sqlalchemy.sql.elements import BinaryExpression, BindParameter, BooleanClauseList, Cast, ColumnClause, Grouping, Label, TextClause, TypeCoerce, UnaryExpression
from sqlalchemy.sql.functions import FunctionElement
from sqlalchemy.sql.selectable import Alias, CTE, FromClause, Select, Join, Subquery
from sqlalchemy.sql.dml import Insert, Update, Delete
from sqlalchemy.types import JSON, NullType, TypeDecorator

from . import _experimental_public_delete as _delete_experiment
from . import _experimental_public_update as _update_experiment
from ._sqlalchemy_guard import install_guard
from ._sqlalchemy_transactions import (install_control, inspect_control, native_scope,
    track_transaction, fail_prepared_flush, after_begin as control_after_begin, after_end as control_after_end)
from ._sqlalchemy_search import rewrite_search, search_shape, validate_search_storage
from .crypto import CryptoFailure, AuthenticationFailed, FieldDescriptor, Keyring, KeyUnavailable, MAX_TEXT_BYTES, open_text, seal_text
from .manifest.parser import decode_manifest_json
from ._native_text import mapped_text_type, assign_text
from ._sqlmodel_support import sync_session_class, async_session_class


class UnsupportedProtectedOperation(CryptoFailure):
    stage = "SQLAlchemy admission"
    remedy = "Use the attached factory, ordinary ORM writes, direct projections, and declared equality/IN with ordinary text binds. Remove unsupported SQL or bind codecs."


class UnsupportedUUIDRecordBind(UnsupportedProtectedOperation):
    remedy = "Use a UUID object or PostgreSQL 16 UUID text with ordinary typed record binds. Custom codecs and callable binds are not supported. No application SQL was executed."


_UUID_RECORD_TEXT = re.compile(r"(?:[0-9a-fA-F]{4}-?){7}[0-9a-fA-F]{4}", re.ASCII)


def _uuid_record_context(value):
    # Derive expected authentication context only; never modify SQL binds.
    if value is None or type(value) is UUID:
        return value
    if type(value) is not str or not 32 <= len(value) <= 41:
        raise UnsupportedUUIDRecordBind()
    body = value[1:-1] if value.startswith("{") and value.endswith("}") else value
    if _UUID_RECORD_TEXT.fullmatch(body) is None:
        raise UnsupportedUUIDRecordBind()
    return UUID(hex=body.replace("-", ""))


class PolicyMismatch(CryptoFailure):
    stage = "attachment validation"
    remedy = "Check the trusted lock, bytea target, search index/check, tenant key policy, mapping, and guarded engine configuration. Attach before application use."


class UnsafeEngineLogging(PolicyMismatch):
    stage = "engine logging admission"
    remedy = "Create the runtime engine with echo=False and hide_parameters=True. Keep those settings for the attached engine and review host logging separately."


class ProtectedSchemaMismatch(PolicyMismatch):
    stage = "protected SELECT execution"
    effects = "transaction_requires_rollback"
    remedy = "Roll back the transaction. Check the current deployment lock and database schema; replace a stale attachment before retrying."


class UnsupportedSQLModelRuntime(PolicyMismatch):
    stage = "SQLModel runtime admission"
    remedy = "Use the qualified SQLModel 0.0.47 synchronous factory on SQLAlchemy 2.0; async SQLModel qualification is pending."

@dataclass(frozen=True)
class _Binding:
    column: object
    attribute: str
    descriptor: FieldDescriptor
    record: object
    record_attribute: str
    tenant: object | None
    tenant_attribute: str | None
    model: type
    character_limit: int | None = None
    storage_column: str | None = None


@dataclass(frozen=True)
class _Sealed:
    body: bytes | None = field(repr=False)
    permit: object = field(repr=False)
    binding: _Binding = field(repr=False)


@dataclass
class _Operation:
    owner: object
    keys: object = field(repr=False)
    tenant: UUID
    session: object
    flushing: bool = False
    flush_context: object = field(default=None, repr=False)
    delete_packet: object = field(default=None, repr=False)
    deleted_seen: set = field(default_factory=set, repr=False)
    prepared: dict = field(default_factory=dict, repr=False)
    rows: dict = field(default_factory=dict, repr=False)
    points: tuple = ()
    search_nodes: list = field(default_factory=list, repr=False)
    search_identities: dict = field(default_factory=dict, repr=False)
    parameters: dict = field(default_factory=dict, repr=False)

    def generated(self, node):
        if self.search_identities.get(id(node)) is node:
            return True
        for permitted in self.search_nodes:
            if isinstance(node, type(permitted)) and node.compare(permitted):
                # Keep the reference alive until the operation ends; an object
                # ID alone could be reused after garbage collection.
                self.search_identities[id(node)] = node
                return True
        return False


_operation = ContextVar("cryptalis_sqlalchemy_operation", default=None)


class _ReadText(TypeDecorator):
    impl = JSON
    cache_ok = False

    def __init__(self, binding, operation, record_column):
        super().__init__()
        self.binding = binding
        self.keys = operation.keys
        self.tenant = operation.tenant
        # Cache only an exact UUID; identity gates reuse after any rebinding.
        self._tenant_fastpath = ((self.tenant, str(self.tenant))
                                 if type(self.tenant) is UUID else None)
        self.points = tuple(value for column, value in operation.points if column.compare(record_column))

    def process_result_value(self, value, dialect):
        if type(value) is not list or len(value) != 3:
            raise AuthenticationFailed()
        payload, record, tenant = value
        descriptor = self.binding.descriptor
        if record is None:
            valid_null_scope = (tenant is None if descriptor.tenant_codec == "uuid16/v1" else
                                tenant == str(descriptor.table_id) == str(self.tenant))
            if payload is not None or not valid_null_scope:
                raise AuthenticationFailed()
            return None  # Native NULL side of an outer join.
        try:
            if descriptor.record_codec == "uuid16/v1":
                record = UUID(record)
            elif type(record) is not int:
                raise AuthenticationFailed()
            cached = self._tenant_fastpath
            if (cached is not None and type(tenant) is str and
                    tenant == cached[1]):
                tenant = self.tenant
            else:
                tenant = UUID(tenant)
            if tenant != self.tenant or any(
                    record not in expected if isinstance(expected, frozenset) else record != expected
                    for expected in self.points):
                raise AuthenticationFailed()
            if payload is not None:
                if type(payload) is not str or len(payload) > 2 * (MAX_TEXT_BYTES + 74):
                    raise AuthenticationFailed()
                payload = bytes.fromhex(payload)
        except CryptoFailure:
            raise
        except Exception:
            raise AuthenticationFailed() from None
        return open_text(payload, descriptor, tenant, record, self.keys)


class _Payload(TypeDecorator):
    impl = LargeBinary
    # Protected projections capture an operation's keys. They MUST be compiled
    # afresh. Native unprotected statements can still use the engine cache.
    cache_ok = False

    def __init__(self, binding, owner):
        super().__init__()
        self.binding, self.owner = binding, owner

    def process_bind_param(self, value, dialect):
        operation = _operation.get()
        if (not isinstance(value, _Sealed) or operation is None or value.permit is not operation or
                value.binding is not self.binding or not operation.flushing):
            raise UnsupportedProtectedOperation()
        return value.body

    def process_result_value(self, value, dialect):
        # Raw bytea is never a public protected result.
        raise UnsupportedProtectedOperation()

    def column_expression(self, column):
        operation = _operation.get()
        if operation is None or operation.owner is not self.owner:
            raise UnsupportedProtectedOperation()
        original = column
        while isinstance(original, Label):
            original = original.element
        table = getattr(original, "table", None)
        if table is None or self.binding.record.key not in table.c:
            raise UnsupportedProtectedOperation()
        record = table.c[self.binding.record.key]
        if self.binding.tenant is not None:
            if self.binding.tenant.key not in table.c:
                raise UnsupportedProtectedOperation()
            tenant = table.c[self.binding.tenant.key]
        else:
            tenant = str(self.binding.descriptor.table_id)
        packed = func.pg_catalog.jsonb_build_array(
            func.pg_catalog.encode(type_coerce(column, LargeBinary()), "hex"), record, tenant)
        return type_coerce(packed, _ReadText(self.binding, operation, record))


def _protected(expression):
    return any(isinstance(getattr(node, "type", None), _Payload) for node in visitors.iterate(expression))


def _points(statement, parameters):
    """Capture row constraints before SQL; never let absent bind data waive one.

    A callable default, transformed identity, or compiler-specific override is
    outside this bounded grammar. Explicit public binds remain native values.
    IN captures the admitted set, including relationship-loader batches.
    """
    result = []
    inputs = {}
    for node in visitors.iterate(statement):
        if isinstance(node, BindParameter):
            inputs.setdefault(node.key, {})[id(node)] = node

    def ungroup(expression):
        while isinstance(expression, Grouping):
            expression = expression.element
        return expression

    def primary(expression):
        return any(isinstance(node, ColumnClause) and node.primary_key
                   for node in visitors.iterate(expression))

    def value_of(bind, column):
        if (type(column.type) not in (Uuid, BigInteger) or
                type(bind.type) not in (type(column.type), NullType) or
                any(type(other.type) not in (type(column.type), NullType)
                    for other in inputs[bind.key].values()) or
                isinstance(statement, Select) and any(key not in inputs for key in parameters)):
            raise UnsupportedProtectedOperation()
        if bind.key in parameters:
            value = parameters[bind.key]
        else:
            if bind.callable is not None or bind.required or len(inputs[bind.key]) != 1:
                raise UnsupportedProtectedOperation()
            value = bind.value
        # Other occurrences of this placeholder can change its compiled
        # semantics. Refuse callable collisions even if this occurrence is plain.
        if bind.key not in parameters and any(other.callable is not None for other in inputs[bind.key].values()):
            raise UnsupportedProtectedOperation()
        values = value if bind.expanding else [value]
        if not isinstance(values, (list, tuple)):
            raise UnsupportedProtectedOperation()
        if type(column.type) is Uuid:
            expected = [_uuid_record_context(item) for item in values]
        else:
            if any(item is not None and type(item) is not int for item in values):
                raise UnsupportedProtectedOperation()
            expected = values
        return frozenset(item for item in expected if item is not None) if bind.expanding else expected[0]

    def visit(expression):
        expression = ungroup(expression)
        if isinstance(expression, BooleanClauseList) and expression.operator is operators.and_:
            for clause in expression.clauses:
                visit(clause)
            return
        if not primary(expression):
            return
        if isinstance(expression, BinaryExpression) and expression.operator in (operators.eq, operators.in_op):
            left, right = ungroup(expression.left), ungroup(expression.right)
            if isinstance(left, BindParameter):
                left, right = right, left
            if (isinstance(left, ColumnClause) and left.primary_key and isinstance(right, BindParameter) and
                    right.expanding == (expression.operator is operators.in_op)):
                result.append((left, value_of(right, left)))
                return
        # A primary-key predicate cannot silently lose requested-row validation.
        # Tuple, OR, cast/function, subquery, and opaque forms need admission.
        raise UnsupportedProtectedOperation()
    if statement.whereclause is not None:
        visit(statement.whereclause)
    if isinstance(statement, Select):
        where_nodes = {id(node) for node in visitors.iterate(statement.whereclause)} if statement.whereclause is not None else set()
        for node in visitors.iterate(statement):
            if (isinstance(node, BinaryExpression) and id(node) not in where_nodes and primary(node) and
                    any(isinstance(child, BindParameter) for child in visitors.iterate(node))):
                # ON and HAVING are not unconditional WHERE constraints. Do not
                # drop them or turn an outer join's nullable side into a point.
                raise UnsupportedProtectedOperation()
    return tuple(result)


class _Attachment:
    def __init__(self, mapping, engine, document, keys, deployment=None):
        self.mapping, self.engine, self.document, self.keys = mapping, engine, document, keys
        self.deployment = deployment
        self.bindings = []
        self.models = {}
        self.fingerprint = ()
        self.search_pins = {}
        self.public_schema_pins = ()

    def protected(self, expression):
        # ORM annotations can retain a native type from mapping construction.
        # Stable column lineage is authoritative, not a mutable type hint.
        return any(isinstance(node, ColumnClause) and any(node.shares_lineage(b.column) for b in self.bindings)
                   for node in visitors.iterate(expression))

    def _admit_textual_references(self, statement):
        # Label references have no column lineage. Check every local occurrence,
        # not just outer ORDER/GROUP clauses; nested SELECTs own their namespace.
        selected_roots = tuple(statement._all_selected_columns)
        order_roots = tuple(statement._order_by_clauses)
        group_roots = tuple(statement._group_by_clauses)
        distinct_roots = tuple(statement._distinct_on)
        roots = [(c, True, True) for c in selected_roots]
        roots += [(c, False, False) for c in order_roots + distinct_roots]
        roots += [(c, False, True) for c in group_roots]
        assigned = {id(c) for c in selected_roots + order_roots + group_roots + distinct_roots}
        roots += [(c, False, True) for c in statement.get_children() if id(c) not in assigned]
        resolution = None

        def references(part, within_columns, input_first):
            if isinstance(part, Select):
                return
            visit = getattr(part, "__visit_name__", None)
            if visit == "postgresql_distinct_on":
                # SQLAlchemy 2.1 syntax extension; 2.0 uses _distinct_on above.
                for child in part._distinct_on:
                    yield from references(child, False, False)
                return
            if visit == "textual_label_reference":
                yield part.element, within_columns, input_first
                return
            transparent = isinstance(part, (Grouping, TypeCoerce)) or (
                isinstance(part, UnaryExpression) and part.modifier in (
                    operators.asc_op, operators.desc_op,
                    operators.nulls_first_op, operators.nulls_last_op))
            # A comma-separated ORDER BY list preserves each bare label.
            transparent = transparent or visit == "order_by_list"
            for child in part.get_children():
                yield from references(child, within_columns, input_first or not transparent)

        for root, within_columns, input_first in roots:
            if any(root is clause for clause in order_roots + group_roots) and self.protected(root):
                raise UnsupportedProtectedOperation()
            for textual, within_columns, input_first in references(root, within_columns, input_first):
                if resolution is None:
                    try:
                        # Empty compilation state supplies the native namespaces
                        # without rendering protected columns or capturing keys.
                        dialect = self.engine.dialect
                        state = statement._compile_state_factory(
                            statement, dialect.statement_compiler(dialect, None))
                        combined, from_only, _ = state._label_resolve_dict
                        selected = tuple(state.statement._all_selected_columns)
                        sources = tuple(c for source in state.froms for c in source.c)
                        resolution = combined, from_only, selected, sources
                    except Exception:
                        raise UnsupportedProtectedOperation() from None
                combined, from_only, selected, sources = resolution
                resolved = (from_only if within_columns else combined).get(textual)
                if resolved is None:
                    raise UnsupportedProtectedOperation()
                if within_columns:
                    candidates = tuple(c for c in sources if c._allow_label_resolve and c.key == textual)
                else:
                    # Labels render unqualified. GROUP BY and names embedded in
                    # expressions use PostgreSQL input-name precedence; bare
                    # ORDER BY / DISTINCT ON output labels retain precedence.
                    inputs = tuple(c for c in sources if c.name == resolved.name)
                    if isinstance(resolved, Label) and input_first and inputs:
                        candidates = inputs
                    else:
                        candidates = tuple(c for c in selected if c._allow_label_resolve and
                                           (c._tq_label or c.key) == textual)
                        if not candidates:
                            candidates = tuple(c for c in sources if c._allow_label_resolve and c.key == textual)
                if not candidates or any(self.protected(c) for c in candidates):
                    raise UnsupportedProtectedOperation()

    def _ring(self, tenant):
        if not isinstance(tenant, UUID):
            raise PolicyMismatch()
        try:
            ring = self.keys if isinstance(self.keys, Keyring) else self.keys(tenant)
        except Exception:
            raise KeyUnavailable() from None
        if (not isinstance(ring, Keyring) or ring.policy.tenant_id != tenant or
                str(ring.policy.domain_id) != self.document["domain_id"]):
            raise PolicyMismatch()
        if self.deployment is not None:
            from cryptalis.migration import _policy
            plan, _ = self.deployment
            if _policy(ring) != plan.document["key_policies"].get(str(tenant)):
                raise PolicyMismatch()
        if any(binding.descriptor.equality for binding in self.bindings):
            roots = [wrapper for wrapper in ring.policy.wrappers if wrapper.context.purpose == "search"]
            if len(roots) != 1 or roots[0].context.generation != ring.policy.search_generation:
                raise PolicyMismatch()
            root = roots[0]
            pin = (root.provider_id, root.context, sha256(root.sealed).digest())
            if self.search_pins.setdefault(tenant, pin) != pin:
                raise PolicyMismatch()
        return ring

    def prepare(self, tenant):
        return self._ring(tenant).prepare()

    async def prepare_async(self, tenant):
        return await self._ring(tenant).prepare_async()

    def validate(self, connection):
        from cryptalis.migration import check_attachment
        # Resolve before lifecycle inspection narrows the transaction search path.
        public_schema_pins = _delete_experiment.resolve_public_schema_pins(self, connection)
        check_attachment(connection, json.dumps(self.document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(), self.deployment)
        if connection.dialect.name != "postgresql" or connection.dialect.driver != "psycopg":
            raise PolicyMismatch()
        if (connection.get_execution_options().get("schema_translate_map") or
                int(connection.exec_driver_sql("show server_version_num").scalar_one()) // 10000 != 16 or
                connection.exec_driver_sql("show server_encoding").scalar_one() != "UTF8"):
            raise PolicyMismatch()
        retained = bool(self.deployment and self.deployment[0].document.get('format') in ('cryptalis.transition/retained-native-research-v0', 'cryptalis.transition/retained-native-comments-research-v1', 'cryptalis.transition/retained-native-comments-cluster-research-v2'))
        native = inspect(connection)
        for model in self.document["models"]:
            mappers = [m for m in self.mapping.mappers if m.class_.__name__ == model["model"]]
            if len(mappers) != 1:
                raise PolicyMismatch()
            mapper = mappers[0]
            table = mapper.local_table
            if (mapper.inherits is not None or mapper.persist_selectable is not table or table.name != model["table"] or
                    table.schema not in (None, model["schema"]) or len(mapper.primary_key) != 1):
                raise PolicyMismatch()
            columns = {c["name"]: c for c in native.get_columns(model["table"], schema=model["schema"])}
            record = table.c[model["record"]["column"]]
            tenant = table.c[model["tenancy"]["column"]] if "column" in model["tenancy"] else None
            codec_type = {"uuid16/v1": Uuid, "int64-be/v1": BigInteger}[model["record"]["codec"]]
            if (mapper.primary_key != (record,) or
                    native.get_pk_constraint(model["table"], schema=model["schema"])["constrained_columns"] != [record.name] or
                    not isinstance(record.type, codec_type) or not isinstance(columns[record.name]["type"], codec_type)):
                raise PolicyMismatch()
            for column in (record, tenant):
                if column is None:
                    continue
                actual = columns[column.name]
                generated_default = column.default is not None and not (column.default.is_callable or column.default.is_scalar)
                if (column.nullable or actual["nullable"] or generated_default or column.server_default is not None or
                        column.onupdate is not None or column.server_onupdate is not None or actual.get("default") is not None or
                        actual.get("identity") is not None or actual.get("computed") is not None):
                    raise PolicyMismatch()
                if isinstance(column.type, Uuid) and not column.type.as_uuid:
                    raise PolicyMismatch()
            if tenant is not None and (not isinstance(tenant.type, Uuid) or not isinstance(columns[tenant.name]["type"], Uuid)):
                raise PolicyMismatch()
            for field in model["fields"]:
                column = table.c[field["column"]]
                actual = columns[field["payload_column"] if retained else field["column"]]
                source = next((item for item in model.get("source_schema", {}).get("columns", ())
                               if item.get("name") == field["column"]), None)
                native_text = mapped_text_type(column.type, source)
                if (not isinstance(actual["type"], LargeBinary) or native_text is None or
                        actual["nullable"] != field["source"]["nullable"] or column.nullable != actual["nullable"] or
                        column.default is not None or column.server_default is not None or column.onupdate is not None or
                        column.server_onupdate is not None or actual.get("default") is not None or actual.get("computed") is not None):
                    raise PolicyMismatch()
                if field["queries"]:
                    if (not isinstance(field["queries"], list) or not field["queries"] or
                            not set(field["queries"]) <= {"equality", "unique"}):
                        raise PolicyMismatch()
                    validate_search_storage(connection, model, {**field, "column": field["payload_column"]} if retained else field)
                descriptor = FieldDescriptor.from_compiled(field["descriptor"], field["descriptor_digest"])
                if (str(descriptor.domain_id), str(descriptor.table_id), str(descriptor.field_id)) != (
                        self.document["domain_id"], model["table_id"], field["field_id"]):
                    raise PolicyMismatch()
                if (descriptor.record_codec != model["record"]["codec"] or
                        descriptor.tenant_codec != ("uuid16/v1" if tenant is not None else "single-tenant-uuid/v1") or
                        descriptor.representation != field["representation"] or descriptor.equality != bool(field["queries"])):
                    raise PolicyMismatch()
                binding = _Binding(column, mapper.get_property_by_column(column).key, descriptor,
                                   record, mapper.get_property_by_column(record).key, tenant,
                                   mapper.get_property_by_column(tenant).key if tenant is not None else None, mapper.class_, native_text[1], field["payload_column"] if retained else None)
                self.bindings.append(binding)
            self.models[mapper.class_] = tuple(b for b in self.bindings if b.model is mapper.class_)
        self.public_schema_pins = public_schema_pins

    def schema_error(self, context):
        # Normalize only an owned retained-profile SELECT schema error. Never
        # create a driver permit, retry SQL, or override a host error policy.
        operation = _operation.get()
        execution = getattr(context, "execution_context", None)
        compiled = getattr(execution, "compiled", None)
        if (operation is None or operation.owner is not self or operation.flushing
                or getattr(context.original_exception, "sqlstate", None) != "42703"
                or getattr(context, "chained_exception", None) is not None
                or compiled is None or not isinstance(compiled.statement, Select)
                or not any(b.storage_column is not None for b in self.bindings)):
            return None
        if self.protected(compiled.statement):
            return ProtectedSchemaMismatch()
        return None

    def activate(self):
        engine = self.engine.sync_engine if isinstance(self.engine, AsyncEngine) else self.engine
        if engine.echo or not engine.hide_parameters or engine.pool.checkedout():
            raise PolicyMismatch()
        self.mapping.configure()
        for binding in self.bindings:
            # Freeze physical schema resolution, including initially unqualified
            # mappings. Existing FK columns are already resolved by configure().
            model = next(m for m in self.document["models"] if m["model"] == binding.model.__name__)
            binding.column.table.schema = model["schema"]
            binding.column.type = _Payload(binding, self)
        for table, schema, name in self.public_schema_pins:
            table.schema = schema
        _update_experiment.freeze_mappings(self)
        self.fingerprint = self._fingerprint()
        engine.clear_compiled_cache()
        # ORM flush uses mapper-owned caches, separate from the engine cache.
        # Discard native storage processors before any protected SQL can run.
        for mapper in self.mapping.mappers:
            mapper.base_mapper._compiled_cache.clear()
        self._control_error = UnsupportedProtectedOperation
        install_control(self, engine)
        install_guard(engine, UnsupportedProtectedOperation, self.before_execute, self.check_cursor)
        event.listen(engine, "handle_error", self.schema_error, retval=True)
        def storage_name(column):
            matches=[b.storage_column for b in self.bindings if b.storage_column is not None
                     and hasattr(column, 'shares_lineage') and column.shares_lineage(b.column)]
            if len(matches)>1:raise PolicyMismatch()
            return matches[0] if matches else None
        if any(b.storage_column is not None for b in self.bindings):
            native_preparer=type(engine.dialect.identifier_preparer)
            class RetainedPreparer(native_preparer):
                def format_column(preparer,column,*args,**kwargs):
                    physical=storage_name(column)
                    if physical is not None and kwargs.get('name') in (None,column.name):
                        kwargs['name']=physical
                    return super().format_column(column,*args,**kwargs)
            engine.dialect.identifier_preparer=RetainedPreparer(engine.dialect)
        native_compiler = engine.dialect.statement_compiler
        class StorageCompiler(native_compiler):
            def _label_select_column(compiler, select, column, *args, **kwargs):
                # Pre-attachment labels/aliases may retain the original text
                # type even after their source Column receives _Payload.
                # Correct the local compiler view without mutating user ASTs.
                original = column
                source = column.element if isinstance(column, Label) else column
                matches = [b for b in self.bindings if b.storage_column is not None
                           and isinstance(source, ColumnClause)
                           and source.shares_lineage(b.column)]
                if len(matches) > 1:
                    raise PolicyMismatch()
                if matches and not isinstance(column.type, _Payload):
                    column = copy(column)
                    column.type = _Payload(matches[0], self)
                    add = compiler._add_to_result_map
                    def preserve_original(keyname, name, objects, type_):
                        return add(keyname, name, (original,) + objects, type_)
                    compiler._add_to_result_map = preserve_original
                    try:
                        return super()._label_select_column(select, column, *args, **kwargs)
                    finally:
                        compiler._add_to_result_map = add
                return super()._label_select_column(select, column, *args, **kwargs)
            def visit_column(compiler,column,add_to_result_map=None,**kwargs):
                rendered=super().visit_column(column,add_to_result_map=add_to_result_map,**kwargs)
                physical=storage_name(column)
                if physical is None:return rendered
                surrogate=copy(column)
                surrogate.name=physical
                return super().visit_column(surrogate,add_to_result_map=None,**kwargs)
            def get_select_precolumns(compiler, select, **kw):
                modifier = super().get_select_precolumns(select, **kw)
                # PostgreSQL's public compiler hook emits only DISTINCT here.
                # Check its modifier, not arbitrary user SQL text.
                if modifier and (any(self.protected(c) for c in select.selected_columns) or self.protected(select)):
                    raise UnsupportedProtectedOperation()
                return modifier
        engine.dialect.statement_compiler = StorageCompiler

    def _fingerprint(self):
        def column(c):
            if c is None:
                return None
            return (c.name, c.key, c.type, c.nullable, c.primary_key, c.default, c.server_default,
                    c.onupdate, c.server_onupdate, c.identity, c.computed,
                    c.type.as_uuid if isinstance(c.type, Uuid) else None)
        try:
            return tuple((b.column.table.schema, b.column.table.name, column(b.column), column(b.record), column(b.tenant),
                          inspect(b.model).primary_key, inspect(b.model).get_property_by_column(b.column).key,
                          b.column.type.binding, b.column.type.owner) for b in self.bindings)
        except Exception:
            raise PolicyMismatch() from None

    def _check(self):
        engine = self.engine.sync_engine if isinstance(self.engine, AsyncEngine) else self.engine
        if (any((table.schema, table.name) != (schema, name)
                for table, schema, name in self.public_schema_pins) or
                self._fingerprint() != self.fingerprint or engine.echo or not engine.hide_parameters or
                engine.get_execution_options().get("schema_translate_map")):
            raise PolicyMismatch()
        operation = _operation.get()
        if operation is None or operation.owner is not self:
            raise UnsupportedProtectedOperation()
        return operation

    def _native_delete_rows(self, statement, operation):
        """Invocation authority comes from native UOW states, never a cache hit."""
        context = operation.flush_context
        table = statement.table
        if (not operation.flushing or context is None or
                context.session is not operation.session):
            raise UnsupportedProtectedOperation()
        matching = [m for m in self.mapping.mappers
                    if m.local_table is table and m.inherits is None and
                    m.base_mapper._memoized_values.get(("delete", table)) is statement]
        if not matching:
            raise UnsupportedProtectedOperation()
        allowed = []
        for state, flags in tuple(context.states.items()):
            if not flags[0] or state.mapper not in matching or state.identity is None:
                continue
            mapper = state.mapper
            row = {column.key: value for column, value in zip(mapper.primary_key, state.identity)}
            version = mapper.version_id_col
            if version is not None:
                value = state.attrs[mapper.get_property_by_column(version).key].loaded_value
                if value is NO_VALUE:
                    raise UnsupportedProtectedOperation()
                row[version.key] = value
            bindings = self.models.get(state.class_)
            if bindings:
                first = bindings[0]
                key = (table.schema, table.name, row[first.record.key])
                if operation.rows.get(key) != operation.tenant:
                    raise UnsupportedProtectedOperation()
            allowed.append(row)
        return allowed

    def _prepare_native_delete(self, connection, statement, groups, operation):
        if operation.delete_packet is not None:
            raise UnsupportedProtectedOperation()
        allowed = self._native_delete_rows(statement, operation)
        copied = tuple(dict(group) for group in groups)
        if not copied:
            raise UnsupportedProtectedOperation()
        reservations = set()
        for row in copied:
            if row not in allowed:
                raise UnsupportedProtectedOperation()
            identity = (statement.table, tuple(row[c.key] for c in statement.table.primary_key))
            if identity in operation.deleted_seen or identity in reservations:
                raise UnsupportedProtectedOperation()
            reservations.add(identity)
        operation.deleted_seen.update(reservations)
        operation.delete_packet = (connection, statement, copied)

    def _check_native_delete_cursor(self, context, operation):
        packet = operation.delete_packet
        if (packet is None or packet[0] is not context.root_connection or
                packet[1] is not context.compiled.statement or
                tuple(context.compiled_parameters) != packet[2]):
            raise UnsupportedProtectedOperation()
        operation.delete_packet = None

    def admit(self, statement, flushing=False):
        if flushing and isinstance(statement, Delete):
            self._native_delete_rows(statement, self._check())
            return
        if _delete_experiment.target(self, statement) is not None:
            return
        if _update_experiment.admitted(self, statement):
            return
        if flushing and isinstance(statement, (Insert, Update, Delete)):
            return
        if not isinstance(statement, Select):
            raise UnsupportedProtectedOperation()
        safe_count_stars = set()
        for node in visitors.iterate(statement):
            operation = _operation.get()
            generated = operation is not None and operation.owner is self and operation.generated(node)
            if generated:
                continue
            if isinstance(node, FunctionElement) and node.name == "count":
                arguments = list(node.clauses)
                if len(arguments) == 1 and isinstance(arguments[0], ColumnClause) and arguments[0].name == "*":
                    safe_count_stars.add(id(arguments[0]))
        for node in visitors.iterate(statement):
            if isinstance(node, TextClause):
                raise UnsupportedProtectedOperation()
            if isinstance(node, Join) and self.protected(node.onclause):
                raise UnsupportedProtectedOperation()
            operation = _operation.get()
            if operation is not None and operation.owner is self and operation.generated(node):
                continue
            if isinstance(node, ColumnClause) and node.is_literal and id(node) not in safe_count_stars:
                raise UnsupportedProtectedOperation()
            if isinstance(node, ColumnClause) and id(node) not in safe_count_stars:
                table = node.table
                source = table
                while isinstance(source, Alias):
                    source = source.element
                if isinstance(source, (Subquery, CTE)) and self.protected(node):
                    raise UnsupportedProtectedOperation()
                if table is None:
                    raise UnsupportedProtectedOperation()
                for binding in self.bindings:
                    target = binding.column.table
                    for origin in node.base_columns:
                        physical = getattr(origin, "table", None)
                        if (physical is not None and origin.name == binding.column.name and physical.name == target.name and
                                physical.schema in (None, target.schema) and not origin.shares_lineage(binding.column)):
                            raise UnsupportedProtectedOperation()
            # Parentheses carry no new operation. Their children still pass
            # every admission check below; do not reject native AND/OR grouping.
            if self.protected(node) and not isinstance(node, (Select, FromClause, ColumnClause, Label, Grouping)):
                boolean = isinstance(node, BooleanClauseList) and node.operator in (operators.and_, operators.or_)
                if not boolean and search_shape(self, node) is None:
                    raise UnsupportedProtectedOperation()
            if isinstance(node, Select):
                def ungroup(expression):
                    while isinstance(expression, Grouping):
                        expression = expression.element
                    return expression
                # ORM join predicates appear as direct public children before
                # they become Join objects. Consume only WHERE/projection
                # occurrences; an additional protected ON occurrence refuses.
                eligible = list(node.selected_columns)
                children = tuple(node.get_children())
                where = node.whereclause
                if where is not None:
                    # Multiple .where() criteria form a new AND wrapper. Its
                    # direct clauses are the SELECT children; descendants of
                    # an explicit AND/OR must never become spare ON permits.
                    root = ungroup(where)
                    if any(where is child for child in children):
                        eligible.append(where)
                    elif any(root is child for child in children):
                        eligible.append(root)
                    elif isinstance(root, BooleanClauseList) and root.operator is operators.and_:
                        eligible.extend(ungroup(clause) for clause in root.clauses)
                    elif self.protected(root):
                        raise UnsupportedProtectedOperation()
                    predicates = [where]
                    while predicates:
                        predicate = predicates.pop()
                        predicate = ungroup(predicate)
                        if operation is not None and operation.owner is self and operation.generated(predicate):
                            continue
                        if isinstance(predicate, BooleanClauseList) and predicate.operator in (operators.and_, operators.or_):
                            predicates.extend(predicate.clauses)
                        elif self.protected(predicate) and search_shape(self, predicate) is None:
                            raise UnsupportedProtectedOperation()
                for child in children:
                    if self.protected(child) and not isinstance(child, FromClause):
                        match = next((i for i, allowed in enumerate(eligible) if ungroup(child) is ungroup(allowed)), None)
                        if match is None:
                            raise UnsupportedProtectedOperation()
                        eligible.pop(match)
                self._admit_textual_references(node)

    def prepare_rows(self, session, operation):
        for obj in tuple(session.new) + tuple(session.dirty) + tuple(session.deleted):
            bindings = self.models.get(type(obj))
            if not bindings:
                continue
            state = inspect(obj)
            first = bindings[0]
            if state.persistent and (state.attrs[first.record_attribute].history.has_changes() or
                                    first.tenant_attribute is not None and state.attrs[first.tenant_attribute].history.has_changes()):
                raise UnsupportedProtectedOperation()
            record = state.attrs[first.record_attribute].loaded_value
            tenant = state.attrs[first.tenant_attribute].loaded_value if first.tenant is not None else first.descriptor.table_id
            if state.persistent:
                if record is NO_VALUE:
                    record = state.identity[0]
                if tenant is NO_VALUE:
                    # Native expiration reloads context within the flush's
                    # greenlet on async paths; never infer tenant from the host.
                    tenant = getattr(obj, first.tenant_attribute)
            if record is NO_VALUE or record is None or tenant is NO_VALUE:
                raise UnsupportedProtectedOperation()
            if tenant != operation.tenant:
                raise AuthenticationFailed()
            operation.rows[(first.column.table.schema, first.column.table.name, record)] = tenant
            if obj in session.deleted:
                continue
            for binding in bindings:
                attribute = state.attrs[binding.attribute]
                if state.persistent and not attribute.history.has_changes():
                    continue
                value = attribute.loaded_value
                if value is NO_VALUE:
                    value = None if state.pending and binding.column.nullable else NO_VALUE
                if value is NO_VALUE:
                    raise UnsupportedProtectedOperation()
                stored_value = assign_text(value, binding.character_limit)
                body = seal_text(stored_value, binding.descriptor, tenant, record, operation.keys)
                operation.prepared[(binding.column.table.schema, binding.column.table.name, record, binding.column.key)] = (value, _Sealed(body, operation, binding))

    def before_execute(self, connection, statement, multiparams, params, execution_options):
        if _delete_experiment.inspect_inventory(self, connection, statement, params):
            if multiparams or execution_options.get("schema_translate_map"):
                raise UnsupportedProtectedOperation()
            return statement, multiparams, params
        if inspect_control(self, connection, statement):
            if multiparams or params or execution_options.get("schema_translate_map"):
                raise UnsupportedProtectedOperation()
            return statement, multiparams, params
        operation = self._check()
        if execution_options.get("schema_translate_map"):
            raise PolicyMismatch()
        self.admit(statement, operation.flushing)
        if isinstance(statement, Update) and not operation.flushing:
            _update_experiment.before_execute(self, connection, statement, multiparams, params)
        if operation.flushing and isinstance(statement, Delete):
            self._prepare_native_delete(connection, statement, multiparams if multiparams else [params], operation)
        if isinstance(statement, (Insert, Update)):
            groups = multiparams if multiparams else [params]
            changed = []
            bindings = [b for b in self.bindings if b.column.table.name == statement.table.name and b.column.table.schema == statement.table.schema]
            for group in groups:
                output = dict(group)
                if bindings:
                    first = bindings[0]
                    if isinstance(statement, Insert):
                        record = output.get(first.record.key)
                    else:
                        points = _points(statement, output)
                        matches = [value for column, value in points if column.shares_lineage(first.record)]
                        if len(matches) != 1:
                            raise UnsupportedProtectedOperation()
                        record = matches[0]
                    if (statement.table.schema, statement.table.name, record) not in operation.rows:
                        raise UnsupportedProtectedOperation()
                    for binding in bindings:
                        if binding.column.key not in output:
                            continue
                        prepared = operation.prepared.get((statement.table.schema, statement.table.name, record, binding.column.key))
                        if prepared is None or output[binding.column.key] != prepared[0]:
                            raise UnsupportedProtectedOperation()
                        output[binding.column.key] = prepared[1]
                changed.append(output)
            return statement, changed if multiparams else [], {} if multiparams else changed[0]
        return statement, multiparams, params

    def check_cursor(self, context):
        if context.compiled is not None and _delete_experiment.inspect_inventory(
                self, context.root_connection, context.compiled.statement, driver=True):
            return
        if context.compiled is not None and inspect_control(self, context.root_connection, context.compiled.statement, driver=True):
            return
        operation = self._check()
        if context.compiled is None:
            raise UnsupportedProtectedOperation()
        self.admit(context.compiled.statement, operation.flushing)
        if isinstance(context.compiled.statement, Update) and not operation.flushing:
            _update_experiment.check_cursor(self, context)
        if operation.flushing and isinstance(context.compiled.statement, Delete):
            self._check_native_delete_cursor(context, operation)


class _Session(Session):
    def __init__(self, *args, _owner, tenant_id, _asynchronous=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._owner, self._tenant, self._asynchronous = _owner, tenant_id, _asynchronous
        self._prepared = None
        self._control_connections = set()
        self._control_pending = {}
        self._control_records = {}

    def connection(self, *args, **kwargs):
        with native_scope(self):
            return super().connection(*args, **kwargs)

    def _keys(self):
        if self._asynchronous:
            # Native dispatch reaches this boundary only for actual query/flush
            # work. Prepare in its greenlet; never perform IO in bind processors.
            return await_only(self._owner.prepare_async(self._tenant))
        return self._owner.prepare(self._tenant)

    def flush(self, objects=None):
        if not (self.new or self.dirty or self.deleted):
            with native_scope(self):
                return super().flush(objects)
        try:
            prepared = self._keys()
        except BaseException as failure:
            _failed_flush_preparation(self, failure)
            raise
        operation = _Operation(self._owner, prepared, self._tenant, self, flushing=True)
        token = _operation.set(operation)
        try:
            with native_scope(self):
                return super().flush(objects)
        finally:
            operation.prepared.clear()
            operation.rows.clear()
            operation.delete_packet = None
            operation.deleted_seen.clear()
            operation.flush_context = None
            _operation.reset(token)


event.listen(_Session, "after_transaction_create", track_transaction)
event.listen(_Session, "after_begin", control_after_begin)
event.listen(_Session, "after_transaction_end", control_after_end)


@event.listens_for(_Session, "before_flush")
def _before_flush(session, context, instances):
    operation = _operation.get()
    if operation is None or operation.session is not session:
        raise UnsupportedProtectedOperation()
    try:
        operation.flush_context = context
        session._owner.prepare_rows(session, operation)
    except BaseException as failure:
        _failed_flush_preparation(session, failure)
        raise


def _failed_flush_preparation(session, failure):
    session._prepared = None
    cleanup_state = {"quarantine_incomplete": None}
    def note(message):
        try:
            BaseException.add_note(failure, message)
        except BaseException:
            # Diagnostic delivery must not replace the primary failure or
            # prevent the native failed-flush cleanup attempt.
            pass
    note('Roll back the failed Session or SAVEPOINT before retrying.')
    try:
        # A fresh async cleanup greenlet has no active exception state.
        # Native rollback captures sys.exc_info(), so restore that context
        # without assigning SQLAlchemy transaction-state fields ourselves.
        raise failure
    except BaseException:
        try:
            fail_prepared_flush(session, cleanup_state=cleanup_state)
        except BaseException:
            note("Cryptalis flush rollback failed; discard this failed unit and inspect cleanup.")
            if cleanup_state.get("quarantine_incomplete") is not False:
                note("Physical quarantine is incomplete or unconfirmed; connection outcome is unknown. "
                                 "Keep the workload stopped and inspect the database session.")


def _query_would_autoflush(session, statement, execution_options):
    """Match the supported native SELECT/private DML flush boundary.

    SQLAlchemy 2.1 adds Core autoflush, independent of ORM execution options.
    Session.autoflush/no_autoflush still control it. ORM option precedence is
    session-wide (2.1), then statement, then the individual execution call.
    """
    if (not isinstance(statement, (Select, Delete, Update)) or not session.autoflush
            or not (session.new or session.dirty or session.deleted)):
        return False
    if statement._propagate_attrs.get("compile_state_plugin") != "orm":
        return _sqlalchemy_version.startswith("2.1.")
    options = dict(getattr(session, "execution_options", {}))
    options.update(statement.get_execution_options())
    options.update(execution_options)
    return bool(options.get("autoflush", True))


@event.listens_for(_Session, "do_orm_execute", retval=True)
def _execute(state):
    session = state.session
    public_update = _update_experiment.target(session._owner, state.statement) is not None
    if public_update or _delete_experiment.target(session._owner, state.statement) is not None:
        if state.parameters is not None and not isinstance(state.parameters, dict):
            raise UnsupportedProtectedOperation()
        try:
            prepared = session._keys()
        except BaseException as failure:
            if _query_would_autoflush(session, state.statement, state.execution_options):
                _failed_flush_preparation(session, failure)
            raise
        operation = _Operation(session._owner, prepared, session._tenant, session)
        token = _operation.set(operation)
        update_token = None
        try:
            if public_update:
                permit = _update_experiment.prepare(session, state.statement, state.parameters)
                update_token = _update_experiment._permit.set(permit)
                # Exact one-operation statement identity must survive to the driver.
                # No cached UPDATE may retain or substitute invocation authority.
                state.update_execution_options(compiled_cache=None)
            else:
                _delete_experiment.prepare(session, state.statement)
            boundary = _delete_experiment._result_boundary.get()
            if session._asynchronous and (boundary is None or boundary.session is not session):
                raise UnsupportedProtectedOperation()
            if boundary is not None and boundary.session is session:
                boundary.attempted = True
            try:
                with native_scope(session):
                    return state.invoke_statement()
            except BaseException as failure:
                if boundary is not None and boundary.session is session:
                    boundary.cleaned = True
                # A native driver error in bulk DML is not a failed ORM flush.
                # SQLAlchemy already owns its transaction state (including any
                # real autoflush failure); do not replace it with flush state.
                if not isinstance(failure, DBAPIError):
                    _failed_flush_preparation(session, failure)
                raise
        except ProtectedSchemaMismatch as failure:
            raise failure from None
        finally:
            if update_token is not None:
                _update_experiment._permit.reset(update_token)
            _operation.reset(token)
    session._owner.admit(state.statement)
    parameters = state.parameters if isinstance(state.parameters, dict) else {}
    protected_read = any(session._owner.protected(c) for c in state.statement.selected_columns)
    try:
        prepared = session._keys()
    except BaseException as failure:
        if _query_would_autoflush(session, state.statement, state.execution_options):
            _failed_flush_preparation(session, failure)
        raise
    operation = _Operation(session._owner, prepared, session._tenant, session,
                           points=_points(state.statement, parameters) if protected_read else (), parameters=parameters)
    if protected_read or session._owner.protected(state.statement):
        # Entity SELECT cache keys can name the Table without its column types.
        # Disable the ORM's cache too, so no compiled processor retains another
        # operation's tenant, requested point or prepared material.
        state.update_execution_options(compiled_cache=None)
    token = _operation.set(operation)
    try:
        state.statement = rewrite_search(session._owner, state.statement, operation)
        with native_scope(session):
            return state.invoke_statement()
    except ProtectedSchemaMismatch as failure:
        # SQLAlchemy preserves native cleanup, then chains the DBAPI cause.
        # Keep that raw database text out of the public exception rendering.
        raise failure from None
    finally:
        _operation.reset(token)


class _AsyncTransaction(AsyncSessionTransaction):
    async def __aexit__(self, *args):
        if args[0] is None:
            try:
                await self.session._prepare()
            except BaseException as failure:
                # Preparation runs before SQLAlchemy's commit/rollback context.
                # Give that context the failure, including cancellation, so
                # native rollback is attempted while the Session stays open.
                self.session.sync_session._prepared = None
                try:
                    await super().__aexit__(type(failure), failure, failure.__traceback__)
                except BaseException:
                    # Native exit can itself fail. Preserve the preparation
                    # failure; a cleanup attempt is not proof of rollback or
                    # physical connection release.
                    if isinstance(failure, CryptoFailure):
                        failure.effects = "unknown"
                        failure.retryable = False

                    def note(message):
                        try:
                            # Do not dispatch an exception subclass's custom
                            # output hook while handling the primary failure.
                            BaseException.add_note(failure, message)
                        except BaseException:
                            # Note delivery can fail too. The primary must
                            # remain observable and quarantine must be tried;
                            # this path makes no diagnostic-delivery claim.
                            pass

                    note(
                        "Cryptalis transaction cleanup failed. Discard this failed unit; "
                        "the connection outcome is unknown. Do not retry until inspection.")
                    try:
                        # Public best-effort cleanup only. Native exit may have
                        # already released its Connection, so do not retain or
                        # close a raw driver handle after pool ownership changes.
                        await self.session.invalidate()
                    except BaseException:
                        note(
                            "Cryptalis connection quarantine failed. Keep the workload "
                            "stopped and inspect the database session before retrying.")
                    raise failure from None
                raise
        return await super().__aexit__(*args)

    async def commit(self):
        try:
            await self.session._prepare()
        except BaseException as failure:
            session = self.session.sync_session
            if session.new or session.dirty or session.deleted:
                await AsyncSession.run_sync(self.session, _failed_flush_preparation, failure)
            raise
        return await super().commit()


class _AsyncSession(AsyncSession):
    sync_session_class = _Session

    def __init__(self, *args, **kwargs):
        super().__init__(*args, _asynchronous=True, **kwargs)

    async def _prepare(self):
        session = self.sync_session
        session._prepared = await session._owner.prepare_async(session._tenant)

    def begin(self):
        return _AsyncTransaction(self)

    def begin_nested(self):
        return _AsyncTransaction(self, nested=True)


def _async_method(name):
    native = getattr(AsyncSession, name)
    @wraps(native)
    async def method(self, *args, **kwargs):
        try:
            await self._prepare()
        except BaseException as failure:
            session = self.sync_session
            pending = bool(session.new or session.dirty or session.deleted)
            statement = args[0] if args else kwargs.get("statement")
            query_flush = (name in ("execute", "scalar", "scalars", "stream", "stream_scalars")
                           and _query_would_autoflush(session, statement, kwargs.get("execution_options", {})))
            if (name in ("flush", "commit") and pending) or query_flush:
                # Cleanup must run in the native greenlet without requesting
                # keys again from the failing or cancelled provider.
                await AsyncSession.run_sync(self, _failed_flush_preparation, failure)
            raise
        return await native(self, *args, **kwargs)
    return method


def _async_delete_result_boundary(name):
    native = getattr(AsyncSession, name)
    return _async_result_boundary(native)


def _async_result_boundary(native):
    @wraps(native)
    async def method(self, *args, **kwargs):
        boundary = _delete_experiment.ResultBoundary(self.sync_session)
        token = _delete_experiment._result_boundary.set(boundary)
        try:
            return await native(self, *args, **kwargs)
        except BaseException as failure:
            if boundary.attempted and not boundary.cleaned:
                boundary.cleaned = True
                await AsyncSession.run_sync(self, _failed_flush_preparation, failure)
            raise
        finally:
            _delete_experiment._result_boundary.reset(token)
    return method


# Native scalars() calls self.execute(); scalar() has its own native boundary.
# This marker identifies an admitted mutation only; it grants no SQL authority.
_AsyncSession.execute = _async_delete_result_boundary("execute")
_AsyncSession.scalar = _async_delete_result_boundary("scalar")


# A clean commit still rechecks key authority. Other operations retain native
# dispatch and prepare only at the actual query/flush boundary.
_AsyncSession.commit = _async_method("commit")


class _Factory:
    def __init__(self, owner):
        self._owner = owner

    def __call__(self, *, tenant_id, **options):
        if any(k in options for k in ("bind", "binds", "class_", "sync_session_class", "_owner", "_asynchronous")):
            raise UnsupportedProtectedOperation()
        self._owner._ring(tenant_id)
        cls = self._owner.session_class
        return cls(bind=self._owner.engine, _owner=self._owner, tenant_id=tenant_id, **options)


def attach(mapping: registry, engine: Engine | AsyncEngine, *, lock: bytes, keys, deployment=None):
    """Attach an already protected target. Await this call for an AsyncEngine.

    Schema transition is not performed. The host authenticates the lock and the
    tenant passed to the returned factory. Only ORM flush writes are admitted.
    """
    try:
        document = decode_manifest_json(lock)
        if (not isinstance(mapping, registry) or not isinstance(engine, (Engine, AsyncEngine)) or
                document["schema"] != "cryptalis.lock/v1" or document["profile"] != "cf1"):
            raise PolicyMismatch()
        native_engine = engine.sync_engine if isinstance(engine, AsyncEngine) else engine
        if native_engine.echo or not native_engine.hide_parameters:
            raise UnsafeEngineLogging()
        owner = _Attachment(mapping, engine, document, keys, deployment)
        if isinstance(engine, AsyncEngine):
            try:
                owner.session_class = async_session_class(
                    _AsyncSession, _Session, mapping, _async_result_boundary)
            except ValueError:
                raise UnsupportedSQLModelRuntime() from None
        else:
            try:
                owner.session_class = sync_session_class(_Session, mapping)
            except ValueError:
                raise UnsupportedSQLModelRuntime() from None
    except CryptoFailure:
        raise
    except Exception:
        raise PolicyMismatch() from None
    if isinstance(engine, AsyncEngine):
        async def asynchronous():
            try:
                if engine.sync_engine.pool.checkedout():
                    raise PolicyMismatch()
                async with engine.connect() as connection:
                    await connection.run_sync(owner.validate)
                await engine.dispose()
                owner.activate()
                return _Factory(owner)
            except CryptoFailure:
                raise
            except Exception:
                raise PolicyMismatch() from None
        return asynchronous()
    try:
        if engine.pool.checkedout():
            raise PolicyMismatch()
        with engine.connect() as connection:
            owner.validate(connection)
        engine.dispose()
        owner.activate()
        return _Factory(owner)
    except CryptoFailure:
        raise
    except Exception:
        raise PolicyMismatch() from None

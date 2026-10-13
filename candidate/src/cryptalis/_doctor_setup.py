"""Offline manifest bindings and review-only integration text; no DB authority."""

from importlib.metadata import PackageNotFoundError

from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg, PGDialectAsync_psycopg
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import ColumnProperty, MappedSQLExpression, Mapper, registry

from cryptalis._sqlmodel_support import qualified_version, uses_sqlmodel


_MAX_MAPPERS = 2048
_MAX_PROPERTIES = 16384

_SYNC_TEMPLATE = """# Review only: run after protection and external ACTIVE publication.
# Bind these names to existing trusted host objects. Do not log key material.
# The trusted lock and current plan must match the reviewed manifest.
from cryptalis.sqlalchemy import attach
sessions = attach(
    existing_registry, existing_runtime_engine,
    lock=trusted_lock_bytes, keys=existing_key_resolver,
    deployment=(current_plan, current_active_pin),
)
with sessions(tenant_id=authenticated_tenant_id) as session:
    pass  # Use the existing application operation here.
"""
_ASYNC_TEMPLATE = _SYNC_TEMPLATE.replace("sessions = attach(", "sessions = await attach(").replace(
    "with sessions(", "async with sessions(")


def _issue(code, remedy, model=None, field=None):
    return {"code": code, "remedy": remedy, "model_index": model, "field_index": field}


def _engine(engine):
    if engine is None:
        return {"status": "NOT_INSPECTED", "code": "existing_runtime_engine_required"}
    if type(engine) not in (Engine, AsyncEngine):
        return {"status": "UNAVAILABLE", "code": "ordinary_runtime_engine_required",
                "remedy": "Supply an ordinary existing SQLAlchemy Engine or AsyncEngine for this offline check."}
    native = engine.sync_engine if type(engine) is AsyncEngine else engine
    if type(native) is not Engine:
        return {"status": "UNAVAILABLE", "code": "ordinary_runtime_engine_required"}
    if type(native.dialect) not in (PGDialect_psycopg, PGDialectAsync_psycopg):
        if isinstance(native.dialect, PGDialect_psycopg):
            return {"status": "UNAVAILABLE", "code": "ordinary_runtime_dialect_required",
                    "remedy": "Custom dialect hooks are outside this offline inspection; use the ordinary PostgreSQL psycopg dialect."}
        return {"status": "REJECTED", "code": "unsupported_engine_driver",
                "remedy": "Use the existing PostgreSQL psycopg engine; no connection or server version was inspected."}
    echo, hide_parameters = native.echo, native.hide_parameters
    if type(echo) not in (bool, str, type(None)) or type(hide_parameters) is not bool:
        return {"status": "UNAVAILABLE", "code": "ordinary_logging_settings_required",
                "remedy": "Review the existing engine's logging settings without custom value hooks."}
    if echo or not hide_parameters:
        return {"status": "REJECTED", "code": "unsafe_engine_logging",
                "remedy": "Construct the runtime engine with echo=False and hide_parameters=True. No setting was changed."}
    translation = Engine.get_execution_options(native).get("schema_translate_map")
    if translation is not None and type(translation) is not dict:
        return {"status": "UNAVAILABLE", "code": "ordinary_translation_settings_required",
                "remedy": "Review custom schema translation outside this offline inspection."}
    if translation:
        return {"status": "REJECTED", "code": "schema_translation_not_admitted",
                "remedy": "Use the authoritative physical mapping; review schema translation separately."}
    return {"status": "CHECKED", "scope": "driver_logging_and_translation_settings_only",
            "mode": "async" if type(engine) is AsyncEngine else "sync"}


def inspect_setup(declaration, mapping, engine):
    result = {
        "status": "UNAVAILABLE", "scope": "manifest_bindings_and_local_engine_settings_only",
        "model_count": len(declaration.models),
        "field_count": sum(len(model.fields) for model in declaration.models),
        "bindings": {"status": "NOT_INSPECTED"}, "engine": {"status": "NOT_INSPECTED"},
        "issue_index_basis": "zero_based_canonical_declaration_order",
        "issues": [],
        "limits": [
            "No database, keys, source imports, migration, mapping configuration or privilege changes occur.",
            "Only manifest references to existing ordinary mapper columns are resolved; types, defaults, constraints and database state are not admitted.",
            "This text neither authenticates host objects nor grants query/profile permission; private application profile flags are not generated.",
            "Registry/property bounds limit this inspection, not host-object construction, total memory or elapsed time.",
        ],
    }
    if type(mapping) is not registry:
        result["code"] = "existing_registry_required"
        result["remedy"] = "Supply the application's existing SQLAlchemy registry. No model import or schema copy is performed."
        return result
    wanted = {model.model for model in declaration.models}
    matches = {name: [] for name in wanted}
    for count, mapper in enumerate(mapping.mappers, start=1):
        if count > _MAX_MAPPERS or type(mapper) is not Mapper:
            result["code"] = "mapping_inspection_unavailable"
            result["remedy"] = "This bounded offline check requires ordinary mappers; use the existing compiler for complete admission."
            return result
        # Call the built-in name descriptor directly, not a custom metaclass hook.
        name = type.__dict__["__name__"].__get__(mapper.class_)
        if name in matches:
            matches[name].append(mapper)
    issues, tables, property_count = result["issues"], set(), 0
    for model_index, model in enumerate(declaration.models):
        selected = matches[model.model]
        if len(selected) != 1:
            issues.append(_issue("model_reference_unresolved",
                                 "Select one unambiguous existing mapped model name in the manifest.", model_index))
            continue
        mapper = selected[0]
        table = mapper.local_table
        if type(table) is not Table or mapper.inherits is not None or mapper.persist_selectable is not table:
            issues.append(_issue("direct_table_mapping_required",
                                 "Use an existing direct ordinary-table mapping; do not recreate the model for setup.", model_index))
            continue
        if table in tables:
            issues.append(_issue("duplicate_table_reference",
                                 "Declare each protected mapped table once.", model_index))
        tables.add(table)
        mapped = {}
        # iterate_properties does not configure mappers or evaluate class
        # descriptors. attrs/column_attrs can trigger relationship configuration.
        for prop in mapper.iterate_properties:
            property_count += 1
            if property_count > _MAX_PROPERTIES:
                result["code"] = "mapping_inspection_unavailable"
                result["remedy"] = "The offline property budget was exceeded; use the existing compiler for complete admission."
                return result
            if type(prop) in (ColumnProperty, MappedSQLExpression) and len(prop.columns) == 1:
                column = prop.columns[0]
                if type(column) is Column and column.table is table:
                    mapped[prop.key] = column
        tenant = mapped.get(model.tenant_column) if model.tenant_column is not None else None
        if model.tenant_column is not None and tenant is None:
            issues.append(_issue("tenant_reference_unresolved",
                                 "Reference an existing ordinary mapped tenant attribute.", model_index))
        if len(mapper.primary_key) != 1:
            issues.append(_issue("single_primary_key_required",
                                 "Review the existing mapping against the compiler's single application-assigned key contract.", model_index))
        used = set()
        for field_index, field in enumerate(model.fields):
            column = mapped.get(field.name)
            if column is None:
                issues.append(_issue("field_reference_unresolved",
                                     "Use the existing mapped attribute name for one ordinary table column; expressions, relationships and synonyms are not direct field references.", model_index, field_index))
                continue
            if column in used:
                issues.append(_issue("duplicate_field_reference",
                                     "Declare each protected mapped column once.", model_index, field_index))
            used.add(column)
            if column is tenant or any(column is primary for primary in mapper.primary_key):
                issues.append(_issue("protected_context_reference",
                                     "Keep primary-key and tenant-context attributes unprotected.", model_index, field_index))
    result["bindings"] = {"status": "REJECTED" if issues else "CHECKED"}
    result["engine"] = _engine(engine)
    if issues or result["engine"]["status"] == "REJECTED":
        result["status"] = "REJECTED"
        return result
    if result["engine"]["status"] != "CHECKED":
        result["status"] = "PARTIAL" if engine is None else "UNAVAILABLE"
        return result
    if uses_sqlmodel(mapping):
        try:
            qualified = qualified_version()
        except PackageNotFoundError:
            qualified = False
        if not qualified or result["engine"]["mode"] == "async":
            result["status"] = "REJECTED"
            result["code"] = "unsupported_sqlmodel_runtime"
            result["remedy"] = "Use the qualified SQLModel 0.0.47 synchronous factory on SQLAlchemy 2.0; async SQLModel qualification is pending."
            return result
    result["status"] = "CHECKED"
    result["required_host_objects"] = [
        "existing_registry", "existing_runtime_engine", "trusted_lock_bytes",
        "existing_key_resolver", "current_plan", "current_active_pin", "authenticated_tenant_id",
    ]
    result["template"] = _ASYNC_TEMPLATE if result["engine"]["mode"] == "async" else _SYNC_TEMPLATE
    return result

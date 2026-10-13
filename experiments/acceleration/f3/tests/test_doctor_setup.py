"""Manifest-first setup uses existing mapping objects without DB or key access."""

import asyncio
import ast
from contextlib import asynccontextmanager, contextmanager
import json
import textwrap
from unittest import TestCase, main
from unittest.mock import patch
from uuid import UUID

from sqlalchemy import Column, MetaData, Table, Text, Uuid, create_engine, event
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, registry, relationship, synonym
from sqlalchemy.types import TypeDecorator

from cryptalis.doctor import doctor


def declaration(field="email", *, model="User", tenancy=None):
    return json.dumps({
        "schema": "cryptalis.protection/v1", "profile": "cf1", "domain_id": str(UUID(int=1)),
        "models": [{"model": model, "table_id": str(UUID(int=2)),
                    "tenancy": tenancy or {"single_tenant": True},
                    "fields": [{"name": field, "field_id": str(UUID(int=3)), "protect": True,
                                "queries": [], "accept_leakage": []}]}],
    }).encode()


class DoctorSetupTests(TestCase):
    def setUp(self):
        self.mapping = registry(metadata=MetaData())
        self.calls = []

        class SensitiveType(TypeDecorator):
            impl = Text
            cache_ok = False

            def __repr__(inner):
                self.calls.append("type_repr")
                raise RuntimeError("PRIVATE_TYPE_DEFAULT")

        def sensitive_default():
            self.calls.append("default")
            raise RuntimeError("PRIVATE_TYPE_DEFAULT")

        self.table = Table(
            "user", self.mapping.metadata,
            Column("id", Uuid, primary_key=True),
            Column("email_address", Text),
            Column("tenant", Uuid),
            Column("public_default", SensitiveType(), default=sensitive_default),
        )

        class User:
            @hybrid_property
            def evaluated(inner):
                self.calls.append("hybrid")
                raise RuntimeError("PRIVATE_TYPE_DEFAULT")

        self.User = User
        self.mapper = self.mapping.map_imperatively(
            User, self.table,
            properties={"email": self.table.c.email_address,
                        "email_alias": synonym("email"),
                        "computed": column_property(self.table.c.email_address + "PRIVATE_TYPE_DEFAULT"),
                        "unresolved_relationship": relationship("NotImportedBySetup")},
        )
        self.engines = []

    def tearDown(self):
        for engine in self.engines:
            if hasattr(engine, "sync_engine"):
                asyncio.run(engine.dispose())
            else:
                engine.dispose()
        self.mapping.dispose()

    def engine(self, *, asynchronous=False, **options):
        factory = create_async_engine if asynchronous else create_engine
        engine = factory(
            "postgresql+psycopg://synthetic:PRIVATE_ENGINE_URL@invalid.example/example",
            **{"echo": False, "hide_parameters": True, **options},
        )
        native = engine.sync_engine if asynchronous else engine

        def forbidden(*args, **kwargs):
            self.calls.append("connection")
            raise RuntimeError("PRIVATE_ENGINE_URL")

        event.listen(native, "do_connect", forbidden)
        self.engines.append(engine)
        return engine

    def inspect(self, raw=None, **options):
        report = doctor(raw or declaration(), phase="setup", mapping=self.mapping, **options)
        self.assertFalse(report["ready"])
        self.assertFalse(report["complete"])
        self.assertEqual(report["effects"], "NONE")
        for check in ("native_admission", "deployment", "roles", "provider", "ciphertext"):
            self.assertEqual(report["checks"][check]["status"], "NOT_INSPECTED")
        encoded = json.dumps(report)
        self.assertNotIn("PRIVATE_TYPE_DEFAULT", encoded)
        self.assertNotIn("PRIVATE_ENGINE_URL", encoded)
        self.assertEqual(self.calls, [])
        return report["checks"]["setup"]

    def test_existing_attribute_bindings_check_without_configuring_or_copying_schema(self):
        before = (self.mapper.configured, self.table.schema, tuple(self.table.columns))
        setup = self.inspect(engine=self.engine())
        self.assertEqual(setup["status"], "CHECKED")
        self.assertEqual(setup["scope"], "manifest_bindings_and_local_engine_settings_only")
        self.assertEqual(setup["model_count"], 1)
        self.assertEqual(setup["field_count"], 1)
        self.assertEqual(before, (self.mapper.configured, self.table.schema, tuple(self.table.columns)))
        self.assertFalse(self.mapper.configured)
        self.assertEqual(setup["issues"], [])
        self.assertIn("template", setup)
        self.assertNotIn("email_address", setup["template"])
        self.assertNotIn("CREATE", setup["template"])

    def test_mapping_only_check_is_partial_with_no_implied_engine_admission(self):
        setup = self.inspect()
        self.assertEqual(setup["status"], "PARTIAL")
        self.assertEqual(setup["bindings"]["status"], "CHECKED")
        self.assertEqual(setup["engine"]["status"], "NOT_INSPECTED")
        self.assertNotIn("template", setup)

    def test_missing_models_fields_and_noncolumn_descriptors_are_actionable(self):
        cases = (
            (declaration(model="Missing"), "model_reference_unresolved"),
            (declaration("emial"), "field_reference_unresolved"),
            (declaration("email_address"), "field_reference_unresolved"),
            (declaration("email_alias"), "field_reference_unresolved"),
            (declaration("computed"), "field_reference_unresolved"),
            (declaration("evaluated"), "field_reference_unresolved"),
            (declaration("unresolved_relationship"), "field_reference_unresolved"),
            (declaration(tenancy={"column": "missing_tenant"}), "tenant_reference_unresolved"),
            (declaration("id"), "protected_context_reference"),
        )
        for raw, code in cases:
            with self.subTest(code=code, raw=raw):
                setup = self.inspect(raw, engine=self.engine())
                self.assertEqual(setup["status"], "REJECTED")
                self.assertIn(code, {issue["code"] for issue in setup["issues"]})
                self.assertTrue(all(issue["remedy"] for issue in setup["issues"]))
                self.assertNotIn("template", setup)
                self.assertFalse(self.mapper.configured)

    def test_engine_settings_are_checked_without_repair_or_connection(self):
        for options in ({"hide_parameters": False}, {"echo": True}, {"echo": "debug"}):
            with self.subTest(options=options):
                engine = self.engine(**options)
                before = (engine.echo, engine.hide_parameters)
                setup = self.inspect(engine=engine)
                self.assertEqual(setup["status"], "REJECTED")
                self.assertEqual(setup["engine"]["code"], "unsafe_engine_logging")
                self.assertEqual(before, (engine.echo, engine.hide_parameters))
                self.assertNotIn("template", setup)

    def test_no_engine_or_key_lookup_is_attempted_on_invalid_manifest(self):
        class Trap:
            def __getattribute__(self, name):
                raise AssertionError("Host object was inspected before parser refusal")

        report = doctor(b'{"PRIVATE_TYPE_DEFAULT":', phase="setup", mapping=Trap(), engine=Trap())
        self.assertEqual(report["checks"]["manifest"]["status"], "REJECTED")
        self.assertNotIn("PRIVATE_TYPE_DEFAULT", json.dumps(report))

    def test_setup_does_not_silently_accept_dynamic_authority_inputs(self):
        for options in ({"writers": object()}, {"deployment": object()}, {"sources": {}},
                        {"search_reviews": (object(),)}):
            with self.subTest(option=next(iter(options))):
                setup = self.inspect(engine=self.engine(), **options)
                self.assertEqual(setup["status"], "REJECTED")
                self.assertEqual(setup["code"], "setup_accepts_mapping_and_engine_only")

    def test_template_is_fixed_review_only_and_references_caller_objects(self):
        setup = self.inspect(engine=self.engine())
        tree = ast.parse(setup["template"])
        self.assertFalse(any(isinstance(node, ast.ClassDef) for node in ast.walk(tree)))
        self.assertNotIn("_experimental", setup["template"])
        self.assertNotIn("create_engine", setup["template"])
        self.assertNotIn("create_all", setup["template"])
        self.assertNotIn("apply(", setup["template"])
        self.assertNotIn("hide_parameters =", setup["template"])
        lock, keys, plan, pin, tenant = (object() for _ in range(5))
        observed = []

        @contextmanager
        def sessions(**kwargs):
            observed.append(kwargs)
            yield object()

        scope = dict(existing_registry=self.mapping, existing_runtime_engine=self.engines[0],
                     trusted_lock_bytes=lock, existing_key_resolver=keys,
                     current_plan=plan, current_active_pin=pin, authenticated_tenant_id=tenant)
        with patch("cryptalis.sqlalchemy.attach", return_value=sessions) as attach:
            exec(compile(tree, "<reviewed-setup-template>", "exec"), scope)
        attach.assert_called_once_with(self.mapping, self.engines[0], lock=lock, keys=keys,
                                       deployment=(plan, pin))
        self.assertEqual(observed, [{"tenant_id": tenant}])
        self.assertEqual(self.calls, [])

    def test_async_engine_prints_awaited_native_attachment(self):
        setup = self.inspect(engine=self.engine(asynchronous=True))
        self.assertEqual(setup["status"], "CHECKED")
        self.assertEqual(setup["engine"]["mode"], "async")
        tree = ast.parse(setup["template"])
        self.assertTrue(any(isinstance(node, ast.Await) for node in ast.walk(tree)))
        self.assertTrue(any(isinstance(node, ast.AsyncWith) for node in ast.walk(tree)))
        observed = []

        @asynccontextmanager
        async def sessions(**kwargs):
            observed.append(kwargs)
            yield object()

        async def fake_attach(*args, **kwargs):
            observed.append((args, kwargs))
            return sessions

        scope = {name: object() for name in setup["required_host_objects"]}
        source = "async def bootstrap():\n" + textwrap.indent(setup["template"], "    ")
        with patch("cryptalis.sqlalchemy.attach", side_effect=fake_attach):
            exec(compile(source, "<reviewed-async-setup-template>", "exec"), scope)
            asyncio.run(scope["bootstrap"]())
        self.assertEqual(observed, [
            ((scope["existing_registry"], scope["existing_runtime_engine"]),
             {"lock": scope["trusted_lock_bytes"], "keys": scope["existing_key_resolver"],
              "deployment": (scope["current_plan"], scope["current_active_pin"])}),
            {"tenant_id": scope["authenticated_tenant_id"]},
        ])

    def test_bounds_fail_partial_inspection_without_a_template(self):
        for name in ("_MAX_MAPPERS", "_MAX_PROPERTIES"):
            with self.subTest(name=name), patch("cryptalis._doctor_setup." + name, 0):
                setup = self.inspect(engine=self.engine())
                self.assertEqual(setup["status"], "UNAVAILABLE")
                self.assertEqual(setup["code"], "mapping_inspection_unavailable")
                self.assertNotIn("template", setup)
                self.assertFalse(self.mapper.configured)

    def test_custom_dialect_hooks_are_not_evaluated(self):
        calls = self.calls
        enabled = False

        class CustomDialect(PGDialect_psycopg):
            @property
            def name(self):
                if enabled:
                    calls.append("dialect_name")
                    raise AssertionError("PRIVATE_TYPE_DEFAULT")
                return "postgresql"

        engine = self.engine()
        engine.dialect = CustomDialect(dbapi=engine.dialect.dbapi)
        enabled = True
        try:
            setup = self.inspect(engine=engine)
        finally:
            enabled = False
        self.assertEqual(setup["status"], "UNAVAILABLE")
        self.assertEqual(setup["engine"]["code"], "ordinary_runtime_dialect_required")
        self.assertNotIn("template", setup)

    def test_model_metaclass_name_hook_is_not_evaluated(self):
        calls = self.calls
        enabled = False

        class CustomMeta(type):
            @property
            def __name__(cls):
                if enabled:
                    calls.append("model_name")
                    raise AssertionError("PRIVATE_TYPE_DEFAULT")
                return type.__dict__["__name__"].__get__(cls)

        class Other(metaclass=CustomMeta):
            pass

        other = Table("other", self.mapping.metadata, Column("id", Uuid, primary_key=True))
        # Mapping is host work. The setup checker must not repeat name hooks.
        mapper = self.mapping.map_imperatively(Other, other)
        enabled = True
        self.calls.clear()
        try:
            setup = self.inspect(engine=self.engine())
        finally:
            enabled = False
        self.assertEqual(setup["status"], "CHECKED")
        self.assertFalse(mapper.configured)

    def test_default_mode_and_key_refusal_precedence_are_preserved(self):
        report = doctor(declaration(), mapping=self.mapping)
        self.assertEqual(report["checks"]["native_admission"]["code"], "incomplete_dynamic_inputs")
        self.assertEqual(report["checks"]["setup"]["status"], "NOT_INSPECTED")
        for options, code in (({"keys": object()}, "ciphertext_audit_opt_in_required"),
                              ({"keys": object(), "audit_ciphertext": True}, "active_phase_and_explicit_keys_required"),
                              ({"audit_row_limit": False}, "invalid_audit_bounds")):
            with self.subTest(code=code):
                report = doctor(declaration(), phase="setup", mapping=object(), engine=object(), **options)
                self.assertEqual(report["checks"]["ciphertext"]["code"], code)
                self.assertEqual(report["checks"]["setup"]["status"], "NOT_INSPECTED")

    def test_unsupported_driver_and_schema_translation_do_not_connect(self):
        engine = create_engine("sqlite://", hide_parameters=True)
        self.engines.append(engine)
        event.listen(engine, "do_connect", lambda *args: self.fail("Connection attempted"))
        setup = self.inspect(engine=engine)
        self.assertEqual(setup["status"], "REJECTED")
        self.assertEqual(setup["engine"]["code"], "unsupported_engine_driver")
        setup = self.inspect(engine=self.engine(execution_options={"schema_translate_map": {None: "private_schema"}}))
        self.assertEqual(setup["status"], "REJECTED")
        self.assertEqual(setup["engine"]["code"], "schema_translation_not_admitted")
        self.assertNotIn("private_schema", json.dumps(setup))

    def test_setup_inputs_do_not_evaluate_custom_truth_hooks(self):
        class Trap:
            def __bool__(inner):
                self.calls.append("truth_hook")
                raise AssertionError("PRIVATE_TYPE_DEFAULT")

        report = doctor(declaration(), phase="setup", mapping=self.mapping,
                        engine=self.engine(), search_reviews=Trap())
        self.assertEqual(report["checks"]["setup"]["code"], "setup_accepts_mapping_and_engine_only")
        for attribute in ("echo", "hide_parameters"):
            engine = self.engine()
            # Invalid host configuration must remain a static refusal.
            setattr(engine, "_echo" if attribute == "echo" else attribute, Trap())
            setup = self.inspect(engine=engine)
            self.assertEqual(setup["status"], "UNAVAILABLE")
            self.assertEqual(setup["engine"]["code"], "ordinary_logging_settings_required")
        setup = self.inspect(engine=self.engine(execution_options={"schema_translate_map": Trap()}))
        self.assertEqual(setup["status"], "UNAVAILABLE")
        self.assertEqual(setup["engine"]["code"], "ordinary_translation_settings_required")


if __name__ == "__main__":
    main(verbosity=2)

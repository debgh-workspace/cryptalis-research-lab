"""Offline selector oracle for pinned FastAPI-template models, not an app replay.

Run with the existing SQLModel 0.0.47 / SQLAlchemy 2.0 environment and supply the
pinned checkout's backend directory. Only app.models is imported. No settings,
database harness, credential files, application server or connection is used.
"""

import asyncio
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from uuid import UUID

from sqlalchemy import create_engine, event, inspect
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy
import sqlmodel

from cryptalis.doctor import doctor


MODEL_SHA256 = "4696396c84832a50ca9d60337c2b6ba24e961f2ee5b5e660d8081fb929ebf459"
UPSTREAM_COMMIT = "7257e606cb94eada1dca40173e2b7f99dd549bc6"


def main():
    backend = Path(sys.argv[1]).resolve(strict=True)
    source = backend / "app" / "models.py"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == MODEL_SHA256
    sys.path.insert(0, str(backend))
    from app.models import Item, User

    mapping = inspect(User).registry
    mappers = tuple(mapping.mappers)
    before = [(id(mapper), mapper.configured, id(mapper.local_table),
               tuple((id(column), id(column.type), id(column.default))
                     for column in mapper.local_table.columns)) for mapper in mappers]
    assert inspect(Item).registry is mapping
    connections = []

    def forbidden(*args, **kwargs):
        connections.append(True)
        raise AssertionError("Offline setup attempted connection")

    engines = [create_engine("postgresql+psycopg://synthetic@invalid.example/synthetic", hide_parameters=True),
               create_engine("postgresql+psycopg://synthetic@invalid.example/synthetic", hide_parameters=False),
               create_async_engine("postgresql+psycopg://synthetic@invalid.example/synthetic", hide_parameters=True)]
    for engine in engines:
        event.listen(engine.sync_engine if hasattr(engine, "sync_engine") else engine, "do_connect", forbidden)
    declaration = {
        "schema": "cryptalis.protection/v1", "profile": "cf1", "domain_id": str(UUID(int=1)),
        "models": [{"model": "User", "table_id": str(UUID(int=71001)),
                    "tenancy": {"single_tenant": True},
                    "fields": [{"name": name, "field_id": str(UUID(int=71002 + index)),
                                "protect": True, "queries": [], "accept_leakage": []}
                               for index, name in enumerate(("full_name", "email"))]}],
    }

    def check(document, engine):
        report = doctor(json.dumps(document).encode(), phase="setup", mapping=mapping, engine=engine)
        assert report["ready"] is False and report["complete"] is False
        assert report["effects"] == "NONE"
        for name in ("native_admission", "deployment", "roles", "provider", "ciphertext"):
            assert report["checks"][name]["status"] == "NOT_INSPECTED"
        return report["checks"]["setup"]

    try:
        checked = check(declaration, engines[0])
        assert checked["status"] == "CHECKED", checked
        assert (checked["model_count"], checked["field_count"]) == (1, 2)
        assert "class " not in checked["template"]
        assert "email" not in checked["template"] and "full_name" not in checked["template"]
        variants = []
        wrong = deepcopy(declaration)
        wrong["models"][0]["model"] = "Missing"
        variants.append((wrong, "model_reference_unresolved"))
        for name in ("emial", "items"):
            wrong = deepcopy(declaration)
            wrong["models"][0]["fields"][1]["name"] = name
            variants.append((wrong, "field_reference_unresolved"))
        wrong = deepcopy(declaration)
        wrong["models"][0]["tenancy"] = {"column": "missing_tenant"}
        variants.append((wrong, "tenant_reference_unresolved"))
        wrong = deepcopy(declaration)
        wrong["models"][0]["fields"][1]["name"] = "id"
        variants.append((wrong, "protected_context_reference"))
        for wrong, code in variants:
            rejected = check(wrong, engines[0])
            assert rejected["status"] == "REJECTED"
            assert code in {issue["code"] for issue in rejected["issues"]}
            assert "template" not in rejected
        rejected = check(declaration, engines[1])
        assert rejected["engine"]["code"] == "unsafe_engine_logging"
        rejected = check(declaration, engines[2])
        assert rejected["code"] == "unsupported_sqlmodel_runtime"
        assert "template" not in rejected
    finally:
        engines[0].dispose()
        engines[1].dispose()
        asyncio.run(engines[2].dispose())
    after = [(id(mapper), mapper.configured, id(mapper.local_table),
              tuple((id(column), id(column.type), id(column.default))
                    for column in mapper.local_table.columns)) for mapper in mappers]
    assert before == after
    assert not connections
    assert "app.core.db" not in sys.modules and "app.main" not in sys.modules
    assert hashlib.sha256(source.read_bytes()).hexdigest() == MODEL_SHA256
    print(json.dumps({"result": "PASS", "scope": "pinned_actual_models_offline_selector_oracle_only",
                      "upstream_commit": UPSTREAM_COMMIT, "model_source_sha256": MODEL_SHA256,
                      "sqlalchemy": sqlalchemy.__version__, "sqlmodel": sqlmodel.__version__,
                      "positive_cells": 1, "defect_cells": 7, "declared_models": 1,
                      "declared_fields": 2, "existing_mappers": len(mappers), "schema_copies": 0,
                      "source_edits": 0, "mapping_mutations": 0, "connection_attempts": 0,
                      "ready": False, "complete": False}, sort_keys=True))


if __name__ == "__main__":
    main()

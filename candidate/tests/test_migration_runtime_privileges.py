"""Prove effective database privileges before testing lifecycle refusal."""

import json
from uuid import uuid4

import pytest
from sqlalchemy.exc import DBAPIError

from cryptalis.manifest.compiler import SearchReview, Writer, WriterInventory
from cryptalis.sqlalchemy import PolicyMismatch, attach
from test_migration import DOMAIN, FIELD_ID, TABLE_ID, application, keys, publish, run


def _replan(app):
    declaration = {"schema": "cryptalis.protection/v1", "profile": "cf1", "domain_id": str(DOMAIN),
        "models": [{"model": "Customer", "table_id": str(TABLE_ID), "tenancy": {"column": "tenant_id"},
                    "fields": [{"name": "name", "field_id": str(FIELD_ID), "protect": True,
                                "queries": ["equality", "unique"], "accept_leakage": ["equality", "unique"]}]}]}
    return app.m.plan(json.dumps(declaration).encode(), app.mapping, app.owner,
        writers=WriterInventory(True, (Writer(TABLE_ID, "app", "sqlalchemy", evidence="owned synthetic application"),)),
        search_reviews=(SearchReview(FIELD_ID, False, "synthetic unbounded names"),), keys=keys,
        runtime_role=app.role, target_id=uuid4(), backfill_rows_per_second=1000,
        verify_rows_per_second=1000, temporary_bytes_per_row=700, wal_bytes_per_row=2000)


def _probe(app, statement, permitted):
    """Independent raw runtime connection; roll back even a successful probe."""
    with app.runtime.connect() as connection:
        try:
            connection.exec_driver_sql(statement)
        except DBAPIError as exc:
            assert not permitted
            assert getattr(exc.orig, "sqlstate", None) == "42501"
        else:
            assert permitted
        finally:
            connection.rollback()


@pytest.mark.parametrize("boundary", ["plan", "apply", "attach"])
@pytest.mark.parametrize("grant", ["none", "runtime", "public"])
def test_effective_schema_create_privilege_blocks_lifecycle(boundary, grant):
    with application(rows=3) as app:
        if boundary == "attach":
            run(app)
            publish(app)
        with app.owner.begin() as connection:
            role = connection.dialect.identifier_preparer.quote_identifier(app.role)
            if grant != "none":
                recipient = "PUBLIC" if grant == "public" else role
                connection.exec_driver_sql(f'GRANT CREATE ON SCHEMA "{app.schema}" TO {recipient}')
        _probe(app, f'CREATE TABLE "{app.schema}".runtime_privilege_probe (id integer)', grant != "none")

        def operation():
            if boundary == "plan":
                return _replan(app)
            if boundary == "apply":
                return run(app, "EXPANDED")
            return attach(app.mapping, app.runtime, lock=app.plan.lock_bytes, keys=keys,
                          deployment=(app.plan, app.pin))
        if grant == "none":
            operation()
        else:
            with pytest.raises((app.m.TransitionFailure, PolicyMismatch)):
                operation()
            if boundary != "attach":
                with app.owner.connect() as connection:
                    assert connection.exec_driver_sql('SELECT to_regclass(%s)',
                        (f'"{app.schema}"._cryptalis_journal',)).scalar_one() is None


@pytest.mark.parametrize("boundary", ["resume", "attach"])
@pytest.mark.parametrize("grant", ["runtime", "public"])
def test_effective_journal_write_privilege_blocks_lifecycle(boundary, grant):
    with application(rows=3) as app:
        run(app, "EXPANDED" if boundary == "resume" else "PENDING")
        if boundary == "attach":
            publish(app)
        with app.owner.begin() as connection:
            role = connection.dialect.identifier_preparer.quote_identifier(app.role)
            recipient = "PUBLIC" if grant == "public" else role
            connection.exec_driver_sql(f'GRANT UPDATE ON "{app.schema}"._cryptalis_journal TO {recipient}')
        _probe(app, f'UPDATE "{app.schema}"._cryptalis_journal SET state = state', True)
        with pytest.raises((app.m.TransitionFailure, PolicyMismatch)):
            if boundary == "resume":
                run(app, "BACKFILLED")
            else:
                attach(app.mapping, app.runtime, lock=app.plan.lock_bytes, keys=keys,
                       deployment=(app.plan, app.pin))


@pytest.mark.parametrize("privilege", ["column-update", "select-grant"])
def test_journal_column_and_delegation_privileges_are_not_hidden_by_table_acl(privilege):
    with application(rows=3) as app:
        run(app, "EXPANDED")
        with app.owner.begin() as connection:
            role = connection.dialect.identifier_preparer.quote_identifier(app.role)
            if privilege == "column-update":
                connection.exec_driver_sql(f'GRANT UPDATE (state) ON "{app.schema}"._cryptalis_journal TO {role}')
            else:
                connection.exec_driver_sql(f'GRANT SELECT ON "{app.schema}"._cryptalis_journal TO {role} WITH GRANT OPTION')
        statement = (f'UPDATE "{app.schema}"._cryptalis_journal SET state = state' if privilege == "column-update"
                     else f'GRANT SELECT ON "{app.schema}"._cryptalis_journal TO PUBLIC')
        _probe(app, statement, True)
        with pytest.raises(app.m.TransitionFailure) as caught:
            run(app, "BACKFILLED")
        assert caught.value.code == "unsafe_runtime_journal_privileges"
        with app.owner.connect() as connection:
            assert connection.exec_driver_sql(f'SELECT state->>\'phase\' FROM "{app.schema}"._cryptalis_journal').scalar_one() == "EXPANDED"


@pytest.mark.parametrize("privilege,recipient,refused", [
    ("UPDATE", "runtime", True), ("SELECT", "runtime", False), ("UPDATE", "public", False)])
def test_default_grants_are_checked_before_journal_publication(privilege, recipient, refused):
    with application(rows=3) as app:
        with app.owner.begin() as connection:
            role = connection.dialect.identifier_preparer.quote_identifier(app.role)
            target = "PUBLIC" if recipient == "public" else role
            connection.exec_driver_sql(f'ALTER DEFAULT PRIVILEGES IN SCHEMA "{app.schema}" GRANT {privilege} ON TABLES TO {target}')
        if refused:
            with pytest.raises(app.m.TransitionFailure) as caught:
                run(app, "EXPANDED")
            assert caught.value.code == "unsafe_runtime_journal_privileges"
            with app.owner.connect() as connection:
                assert connection.exec_driver_sql('SELECT to_regclass(%s)',
                    (f'"{app.schema}"._cryptalis_journal',)).scalar_one() is None
        else:
            # Existing expansion explicitly revokes PUBLIC journal privileges.
            # A safe default SELECT must also remain admitted.
            assert run(app, "EXPANDED").phase == "EXPANDED"
            _probe(app, f'UPDATE "{app.schema}"._cryptalis_journal SET state = state', False)

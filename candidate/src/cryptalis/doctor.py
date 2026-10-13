"""Bounded read-only diagnostics; never an authorization or release gate."""
import hashlib
import json
import re

from cryptalis.manifest.compiler import compile_protection, PlanningRejected, InspectionUnavailable
from cryptalis.manifest.compatibility import CompatibilityInspectionUnavailable
from cryptalis.manifest.declaration import parse_protection_declaration
from cryptalis.manifest.parser import ManifestInvalid


def doctor(manifest: bytes, *, mapping=None, engine=None, writers=None,
           search_reviews=(), sources=None, phase="pre_adoption", deployment=None):
    """Inspect declaration and, when explicitly supplied, a native PostgreSQL schema.

    The caller supplies trusted application objects; no modules or source files
    are imported by name. No provider or application row values are accessed.
    Active mode requires a host-authenticated plan/pin and the existing runtime
    engine; only deployment metadata and effective permissions are inspected. The report cannot qualify deployment even when checks succeed.
    """
    checks = {name: {"status": "NOT_INSPECTED"} for name in (
        "manifest", "native_admission", "deployment", "compatibility", "roles", "provider", "ciphertext")}
    report = {"format": "cryptalis.doctor/v1", "phase": phase if phase in ("pre_adoption", "active") else "unknown",
              "effects": "NONE", "authority": "ADVISORY_NOT_AUTHENTICATED",
              "complete": False, "ready": False, "checks": checks,
              "limits": [
                  "Native pre-adoption and active deployment metadata use distinct inspection modes.",
                  "Writer completeness and value-domain reviews are host assertions, not independent discovery.",
                  "Provider custody and ciphertext authentication are not inspected; role checks apply only to explicit active mode.",
                  "Read-only database inspection is not a sandbox for trusted host objects or engine callbacks.",
                  "All seven production gates and actual query routing require separate qualification."]}
    if phase not in ("pre_adoption", "active"):
        checks["native_admission"] = {"status": "REJECTED", "code": "unsupported_diagnostic_phase"}
        return report
    if type(manifest) is not bytes:
        checks["manifest"] = {"status": "REJECTED", "code": "manifest_bytes_required"}
        return report
    try:
        declaration = parse_protection_declaration(manifest)
    except ManifestInvalid:
        checks["manifest"] = {"status": "REJECTED", "code": "invalid_protection_declaration",
                              "remedy": "Supply a valid bounded cryptalis.protection/v1 declaration."}
        return report
    checks["manifest"] = {"status": "CHECKED", "scope": "declaration_grammar_only",
                          "sha256": hashlib.sha256(manifest).hexdigest(),
                          "model_count": len(declaration.models)}
    if phase == "active":
        return _active_report(report, declaration, engine, deployment, mapping, sources)
    if deployment is not None:
        checks["deployment"] = {"status": "REJECTED", "code": "deployment_requires_active_phase"}
        return report
    supplied = (mapping is not None, engine is not None, writers is not None)
    if not all(supplied):
        if any(supplied):
            checks["native_admission"] = {"status": "UNAVAILABLE", "code": "incomplete_dynamic_inputs"}
        if sources is not None:
            checks["compatibility"] = {"status": "NOT_INSPECTED", "code": "compiled_mapping_required"}
        return report
    try:
        plan = compile_protection(manifest, mapping, engine, writers=writers,
                                  search_reviews=search_reviews)
    except PlanningRejected as failure:
        # Stable issue codes only: avoid echoing host/catalog identifiers and evidence.
        checks["native_admission"] = {"status": "REJECTED",
                                      "codes": sorted({issue.code for issue in failure.issues}),
                                      "remedy": "Review the native schema and host inventory with the protection planner."}
        return report
    except InspectionUnavailable as failure:
        checks["native_admission"] = {"status": "UNAVAILABLE", "code": failure.code,
                                      "sqlstate": failure.sqlstate if type(failure.sqlstate) is str and re.fullmatch(r"[0-9A-Z]{5}", failure.sqlstate) else None,
                                      "remedy": "Restore inspection access; no schema admission was established."}
        return report
    checks["native_admission"] = {"status": "CHECKED", "scope": "native_compiler_admission",
                                  "lock_digest": plan.lock_digest}
    try:
        compatibility = plan.compatibility_report(mapping, sources=sources)
    except CompatibilityInspectionUnavailable as failure:
        checks["compatibility"] = {"status": "UNAVAILABLE", "code": failure.code}
    else:
        checks["compatibility"] = {"status": compatibility["coverage"], "report": compatibility}
    return report


def _active_report(report, declaration, engine, deployment, mapping, sources):
    from sqlalchemy.engine import Engine
    from sqlalchemy.exc import SQLAlchemyError
    from psycopg import Error as PsycopgError
    from cryptalis.migration import MigrationPlan, DeploymentPin, TransitionFailure, check_attachment, _admit

    checks = report["checks"]
    if (type(deployment) is not tuple or len(deployment) != 2
            or type(deployment[0]) is not MigrationPlan or type(deployment[1]) is not DeploymentPin
            or not isinstance(engine, Engine)):
        checks["deployment"] = {"status": "UNAVAILABLE", "code": "explicit_deployment_and_engine_required"}
        return report
    if engine.dialect.name != "postgresql" or engine.dialect.driver != "psycopg":
        checks["deployment"] = {"status": "REJECTED", "code": "unsupported_stack"}
        return report
    plan, pin = deployment
    try:
        _admit(plan, pin)
        if pin.phase != "ACTIVE":
            raise TransitionFailure("active_deployment_pin_required")
    except TransitionFailure as failure:
        checks["deployment"] = {"status": "REJECTED", "code": failure.code}
        return report
    try:
        recorded = parse_protection_declaration(json.dumps(plan.document["lock"]["declaration"]).encode())
        lock = plan.lock_bytes
    except (KeyError, TypeError, ValueError):
        checks["deployment"] = {"status": "REJECTED", "code": "invalid_deployment_declaration"}
        return report
    if recorded.canonical_bytes() != declaration.canonical_bytes():
        checks["deployment"] = {"status": "REJECTED", "code": "deployment_declaration_mismatch"}
        return report
    try:
        with engine.connect().execution_options(isolation_level="REPEATABLE READ", postgresql_readonly=True) as connection, connection.begin():
            if connection.exec_driver_sql("SHOW transaction_read_only").scalar_one() != "on":
                raise InspectionUnavailable(None)
            connection.exec_driver_sql("SET LOCAL search_path = pg_catalog")
            check_attachment(connection, lock, deployment)
    except TransitionFailure as failure:
        checks["deployment"] = {"status": "REJECTED", "code": failure.code,
                                "remedy": "Inspect the external pin, deployment state and planned runtime permissions; no repair was attempted."}
        return report
    except (SQLAlchemyError, PsycopgError, InspectionUnavailable) as failure:
        state = getattr(getattr(failure, "orig", failure), "sqlstate", None)
        checks["deployment"] = {"status": "UNAVAILABLE", "code": "deployment_inspection_unavailable",
                                "sqlstate": state if type(state) is str and re.fullmatch(r"[0-9A-Z]{5}", state) else None}
        return report
    except (KeyError, TypeError, ValueError):
        checks["deployment"] = {"status": "REJECTED", "code": "invalid_deployment_state"}
        return report
    checks["deployment"] = {"status": "CHECKED", "scope": "active_schema_journal_and_external_pin_consistency",
                            "plan_digest": plan.digest}
    checks["roles"] = {"status": "CHECKED", "scope": "planned_runtime_effective_permissions_and_routine_policy_at_snapshot"}
    report["limits"].append("The host authenticates the external pin; this report does not authenticate its origin or cover later permission/schema changes.")
    if mapping is not None:
        try:
            compatibility = plan.compatibility_report(mapping, sources=sources)
        except CompatibilityInspectionUnavailable as failure:
            checks["compatibility"] = {"status": "UNAVAILABLE", "code": failure.code}
        else:
            checks["compatibility"] = {"status": compatibility["coverage"], "report": compatibility}
    elif sources is not None:
        checks["compatibility"] = {"status": "NOT_INSPECTED", "code": "compiled_mapping_required"}
    return report

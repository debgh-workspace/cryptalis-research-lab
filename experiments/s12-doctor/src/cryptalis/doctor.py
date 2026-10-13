"""Bounded pre-adoption diagnostics; never an authorization or release gate."""
import hashlib
import re

from cryptalis.manifest.compiler import compile_protection, PlanningRejected, InspectionUnavailable
from cryptalis.manifest.compatibility import CompatibilityInspectionUnavailable
from cryptalis.manifest.declaration import parse_protection_declaration
from cryptalis.manifest.parser import ManifestInvalid


def doctor(manifest: bytes, *, mapping=None, engine=None, writers=None,
           search_reviews=(), sources=None, phase="pre_adoption"):
    """Inspect declaration and, when explicitly supplied, a native PostgreSQL schema.

    The caller supplies trusted application objects; no modules or source files
    are imported by name. No provider or application row values are accessed.
    Active encrypted deployments require different checks and are not admitted
    as this mode. The report cannot qualify deployment even when checks succeed.
    """
    checks = {name: {"status": "NOT_INSPECTED"} for name in (
        "manifest", "native_admission", "compatibility", "roles", "provider", "ciphertext")}
    report = {"format": "cryptalis.doctor/v1", "phase": "pre_adoption",
              "effects": "NONE", "authority": "ADVISORY_NOT_AUTHENTICATED",
              "complete": False, "ready": False, "checks": checks,
              "limits": [
                  "Only native pre-adoption schema admission and supplied source snapshots are supported.",
                  "Writer completeness and value-domain reviews are host assertions, not independent discovery.",
                  "Effective-role coverage, provider custody and ciphertext authentication are not inspected.",
                  "Read-only database inspection is not a sandbox for trusted host objects or engine callbacks.",
                  "All seven production gates and actual query routing require separate qualification."]}
    if phase != "pre_adoption":
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

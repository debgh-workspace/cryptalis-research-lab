"""Public removal input recovery refuses before host access or lifecycle work."""

from dataclasses import replace
import hashlib
import json
import traceback
from unittest import TestCase, main
from uuid import UUID

from cryptalis.deprotection import DeprotectionPlan, RemovalApproval, remove
from cryptalis.migration import DeploymentPin, MaintenanceApproval, TransitionFailure


def canonical(document):
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def syntactic_plan():
    """Synthetic decoded artifact only; no compiler/database admission is claimed."""
    source = {"format": "cryptalis.transition/retained-native-research-v0", "kind": "protect",
              "operation_id": str(UUID(int=1)), "target_id": str(UUID(int=2)),
              "lock": {"models": []}, "target": ["synthetic", "1", None, None, "synthetic_owner"],
              "runtime_role": "synthetic_protected", "journal_schema": "synthetic"}
    source_pin = {"target_id": source["target_id"], "operation_id": source["operation_id"],
                  "plan_digest": hashlib.sha256(canonical(source)).hexdigest(), "phase": "ACTIVE"}
    reverse = {"format": "cryptalis.reverse/retained-native-research-v0", "kind": "deprotect",
               "operation_id": str(UUID(int=3)), "target_id": source["target_id"],
               "source_plan": source, "source_pin": source_pin,
               "lock": source["lock"], "target": source["target"],
               "runtime_role": source["runtime_role"], "journal_schema": source["journal_schema"],
               "key_policies": {}, "active_schemas": {}, "retirable_aborted": [],
               "estimates": {"backfill_rows_per_second": 1, "verify_rows_per_second": 1,
                             "writer_pause_seconds_estimate": 1},
               "plaintext_runtime_role": "synthetic_plaintext", "cutover_readiness": {}}
    return DeprotectionPlan(canonical(reverse))


class RemovalInputDiagnostics(TestCase):
    def setUp(self):
        self.accesses = []
        accesses = self.accesses

        class HostTrap:
            def __getattribute__(self, name):
                accesses.append(name)
                raise AssertionError("PRIVATE_HOST_SENTINEL")

        self.trap = HostTrap()
        self.plan = syntactic_plan()
        class PlanSubclass(DeprotectionPlan):
            @property
            def digest(self):
                accesses.append("subclass_digest")
                raise AssertionError("PRIVATE_HOST_SENTINEL")

            @property
            def operation_id(self):
                accesses.append("subclass_operation")
                raise AssertionError("PRIVATE_HOST_SENTINEL")

        self.subclass = PlanSubclass(self.plan.artifact)
        self.pin = DeploymentPin(self.plan.target_id, self.plan.operation_id, self.plan.digest, "REMOVING")
        self.evidence = RemovalApproval(self.plan.digest, "synthetic workload receipt",
                                       "synthetic retained reader receipt", True)

    def reject(self, plan, *, code, **options):
        kwargs = dict(pin=self.pin, approval=None, plaintext_approval=None,
                      removal_approval=self.evidence)
        kwargs.update(options)
        with self.assertRaises(TransitionFailure) as raised:
            remove(plan, self.trap, **kwargs)
        failure = raised.exception
        self.assertEqual(failure.code, code)
        self.assertNotIn("PRIVATE_HOST_SENTINEL", str(failure))
        rendered = "".join(traceback.format_exception_only(type(failure), failure))
        self.assertNotIn("PRIVATE_HOST_SENTINEL", rendered)
        self.assertEqual(self.accesses, [])
        return failure

    def test_missing_and_wrong_plan_are_typed_without_host_property_access(self):
        for plan in (None, object(), b"PRIVATE_HOST_SENTINEL", {}, self.trap, self.subclass):
            for evidence in (None, self.evidence):
                with self.subTest(plan_type=type(plan).__name__, evidence_present=evidence is not None):
                    failure = self.reject(plan, code="external_reverse_policy_mismatch",
                                          removal_approval=evidence)
                    self.assertIsNone(failure.operation_id)

    def test_corrected_plan_reaches_existing_explicit_approval_refusals(self):
        self.reject(None, code="external_reverse_policy_mismatch")
        self.reject(self.plan, code="removal_evidence_required", removal_approval=None)
        self.reject(self.plan, code="removal_publication_required", pin=replace(self.pin, phase="PLAINTEXT_ACTIVE"))
        self.reject(self.plan, code="maintenance_approval_required")
        self.reject(self.plan, code="plaintext_approval_required",
                    approval=MaintenanceApproval("synthetic writer exclusion", 1))

    def test_valid_plan_preserves_evidence_before_publication_refusal(self):
        for evidence in (None, replace(self.evidence, old_workers_stopped=False),
                         replace(self.evidence, package_free_workload_evidence=""),
                         replace(self.evidence, retained_backup_recovery_evidence=""),
                         replace(self.evidence, plan_digest="0" * 64)):
            with self.subTest(evidence=evidence):
                failure = self.reject(self.plan, code="removal_evidence_required",
                                      removal_approval=evidence, pin=None)
                self.assertEqual(failure.operation_id, self.plan.operation_id)


if __name__ == "__main__":
    main(verbosity=2)

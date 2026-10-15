# Maintenance, recovery and removal handoff

**Source-checked procedure; not executed by this documentation task.** Use approved synthetic data until the open qualifications are resolved. This guide does not authorize maintenance, grants, plaintext exposure or key retirement.

## Preserve the recovery packet first

Retain the exact forward/reverse artifacts and digests, authenticated current pins outside database restore, source/package/reader identities, native schema/metadata inventory, exact key policy/wrappers and custody recovery, writer inventory, approvals, raw operation outcomes and backup lineage. Keep secrets out of reports and source control.

## Protection and uncertain outcomes

1. Inspect schema, writers, roles, collations, indexes/comments and remembered CLUSTER designation. Resolve all planning refusals. Save the read-only `cryptalis.migration.plan(...)` result's `artifact`.
2. Stop/drain writers and exclude alternate credentials. Use an actual `MaintenanceApproval` and host-authenticated PREPARED pin for the exact plan.
3. Call `cryptalis.migration.apply(...)`. Default `PENDING` means the database awaits external publication. Keep writers stopped.
4. Publish the exact artifact, use the matching ACTIVATING pin with `until="ACTIVE"`, and retain the authoritative ACTIVE pin. Restart fresh attached workers only after successful activation and host checks.

`cryptalis.migration.verify(p, engine, keys=..., pin=..., approval=...)` is an original-versus-decrypted **pre-switch** comparison, valid only at BACKFILLED or VERIFIED. Stop apply at one of those phases if explicitly invoking verify. At PENDING/ACTIVE it raises `source_verification_unavailable`. Normal switching already verifies. An active bounded doctor ciphertext audit is a different operation and cannot compare against former plaintext.

`cryptalis.migration.abort(p, engine, pin=..., approval=...)` is pre-switch only and retains its durable abort journal. A switched operation requires current-data decrypt-back; do not restore an old snapshot as lossless rollback.

After a lost COMMIT reply or cleanup failure, preserve the original operation identity and safe diagnostics. Inspect its actual journal/transaction outcome on the trusted target and reconcile current external policy before an approved resume. An absent reply or an absent marker while the transaction can still commit is UNKNOWN. Do not retry business writes automatically, delete journals or manufacture a new pin.

## Remembered designation and older artifacts

New plans default to `preserve_cluster_designation=True`, selecting `cryptalis.transition/retained-native-comments-cluster-research-v2`; reversal uses `cryptalis.reverse/retained-native-comments-cluster-research-v2`. The separate inventory binds original index names, constraint linkage and explicit true/false designation. OIDs are not durable artifact identities. This records remembered designation, not physical heap order; it does not run CLUSTER.

Older v0/v1 artifacts remain `NOT_INVENTORIED`, never “verified absent.” Their bytes are not rewritten:

- Before effects, create a fresh inventoried plan while the original native catalog still exists and obtain new external authority.
- Before switch, use the existing safe abort path when admitted. Preserve the ABORTED journal; automatic journal deletion/replanning is not supplied.
- If no original indexes could be retired, the bounded survivor path observes and preserves the complete surviving native map under transition locks. A designated disposable companion refuses destructive removal pending review.
- If original indexes could be retired, missing designation evidence blocks destructive switch, reverse, incomplete plaintext activation and removal. Preserve current protection/read access, ciphertext, keys, manifests, journal and backups.
- After retirement, independently authenticated pre-transition evidence must bind the target and exact source artifact, complete original index/table identities, definitions, links and explicit designation with provenance/timeline. Current missing flags, comments alone or arbitrary JSON are insufficient. **No general evidence importer or post-loss repair protocol is implemented.**

The path-aware reverse abort preserves the full current retained-index map and returns the source to ACTIVE in the same transaction after validation. It does not recover missing historical metadata or authorize a later destructive switch.

## Decrypt current values back

Stop/drain workers, retain the ACTIVE protection pin, and use a **distinct** separately provisioned plaintext runtime role.

```python
from cryptalis import deprotection as reverse

reverse_plan = reverse.plan(
    p, owner_engine, source_pin=active_pin, keys=tenant_keyrings,
    plaintext_runtime_role=plaintext_runtime_role,
    backfill_rows_per_second=measured_backfill_rate,
    verify_rows_per_second=measured_verify_rate,
    temporary_bytes_per_row=measured_storage_cost,
    wal_bytes_per_row=measured_wal_cost,
)
```

Save the reverse artifact and obtain its own PREPARED authority. `reverse.PlaintextApproval(target_id, operation_id, plan_digest, accept_plaintext_at_rest, retained_backup_recovery)` must name the reverse identity, explicit consent and actual recovery ownership. Consent covers plaintext in live storage, WAL, replicas and backups; never copy a fixture's attestation as consent.

```python
progress = reverse.apply(
    reverse_plan, owner_engine, keys=tenant_keyrings,
    pin=reverse_prepared_pin, approval=approval,
    plaintext_approval=consent, until="PLAINTEXT_PENDING",
)
```

Keep writers fenced. Independently compare current edited values, types, NULLs, membership and admitted metadata. Review `reverse_plan.cutover_procedure(create_role=False)` and `reverse.check_cutover(reverse_plan, owner_engine)`. They do not grant permissions or terminate workers. Execute only explicitly approved operator steps, including any additional public-table grants required by the application.

After publication, call the same `reverse.apply` with the matching PLAINTEXT_ACTIVATING pin and `until="PLAINTEXT_ACTIVE"`. Run a fresh package-free process under the intended plaintext role. Check current values before workload teardown can delete the fixture. Pre-switch `reverse.abort(..., pin=..., approval=..., plaintext_approval=...)` discards only staging; keep its evidence.

## Removal and retained obligations

1. Obtain actual package-free workload results and retained encrypted-backup recovery evidence. Historical same-host recovery is not a fresh-host disaster drill.
2. Construct `reverse.RemovalApproval(plan_digest, package_free_workload_evidence, retained_backup_recovery_evidence, old_workers_stopped)` with the reverse digest and actual evidence.
3. Obtain external REMOVING authority, then call:

```python
retired = reverse.remove(
    reverse_plan, owner_engine, pin=removing_pin, approval=approval,
    plaintext_approval=consent, removal_approval=removal,
)
```

4. Publish REMOVED, retain the reverse artifact, and call `reverse.check_removed(reverse_plan, owner_engine, pin=removed_pin)` through a trusted restore/startup gate outside the package-free application.
5. Remove the live application dependency last. Keep isolated recovery readers/keys and old-format dependencies for retained backups until explicit retirement.

Removal retires only inventoried operation metadata. Unknown dependencies/journal rows refuse it. It does not verify the host's backup service, delete all keys or erase historical bytes.

## Actionable failures

| Signal | Safe next step |
|---|---|
| `PlanningRejected` / `InspectionUnavailable` | Inspect code/location/remedy and restore approved inspection/admission prerequisites; no unavailable check becomes PASS |
| `unsafe_engine_logging` / `PolicyMismatch` | Correct logging and inspect exact target/lock/pin/mapping/privileges; never fall back to plaintext |
| `KeyUnavailable` / `FileCustodyUnavailable` | Inspect exact custody/policy and approved recovery copies; never regenerate missing material |
| `AuthenticationFailed` / `InvalidFrame` | Stop the affected operation, withhold the failing value and inspect trusted context/recovery. Already returned authenticated values are not recalled |
| `legacy_profile_creation_disabled` | Omit the option or select true for a new inventoried plan; do not relabel old artifacts |
| `legacy_designation_evidence_required` / `legacy_transient_designation_requires_review` | Preserve all protection/recovery material and obtain the separately reviewed metadata recovery procedure |
| `source_verification_unavailable` | Explicit source verification is pre-switch only; do not treat an active audit as original-value comparison |
| `missing_measured_rates` / `missing_measured_storage_or_wal_costs` | Measure the staging workload and re-plan; fixture constants are not budgets |
| `row_exceeds_chunk_byte_limit` | Keep writers stopped and inspect capacity/field sizes; never skip or truncate a row |
| `external_reverse_policy_mismatch` / `plaintext_approval_required` | Obtain the correct external authority/consent; a journal cannot approve recovery |
| Unknown effects, lost reply or cleanup failure | Preserve evidence; reconcile the original operation, transaction, pool and deployment before retry |

Never log plaintext, key bytes, private custody files, raw credentials/provider exceptions or unsanitized database URLs.

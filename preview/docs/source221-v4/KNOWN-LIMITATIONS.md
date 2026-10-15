# Known limitations and production gates

## Security limits

- Storage exposes row linkage, ciphertext length, NULL presence, write timing, access patterns and result volumes. Equality additionally exposes equal-value classes/frequencies, repeated queries and membership sets. Uniqueness conflicts expose membership within the declared scope.
- Auxiliary knowledge and chosen inputs can identify searchable values. No opaque-search, forward/backward privacy, ORAM or query-privacy claim is made.
- The host authenticates users, supplies trusted tenant scope and authorizes queries. Encryption does not prevent application compromise, broken authorization, or plaintext leakage from host logs/caches/exports.
- Returned-value authentication does not prevent valid same-context replay, hostile omission, nullable substitution with SQL NULL, corrupted unreturned search terms or privileged schema changes. It is not freshness, completeness or adversarial global uniqueness.
- Full-width equality terms rely on the stated HMAC collision assumption. Independent composition review, aggregate usage bounds and production key custody remain open.
- Plaintext/ciphertext may remain in old heap bytes, WAL, replicas, snapshots and backups. Protection, deletion and uninstall do not establish secure erasure. Keep required readers/keys until explicit approved retirement.

## Engineering and delivery gaps

Source221 resolves the seven historical layout expectations through retained-native oracles and integrates bounded remembered-designation handling. Its distribution audit is accepted within the bounded same-host scope. Installed221 acceptance and exact public-example smoke remain pending. Transport218 remains the installed baseline and retains seven historical failures per main cell. Neither result may be relabeled as the other.

Conditional legacy recovery cannot invent designation metadata for indexes an old artifact could retire. A post-loss evidence importer and generic legacy-layout repair are not implemented. Complete metadata fidelity, new-format/old-reader compatibility and fresh-host disaster recovery remain open.

All three complete active rotations, production KMS, online/concurrent-write migration, adaptive parallelism, stronger search privacy and broader native SQL remain unfinished. The operational CLI is incomplete; the guide uses actual Python APIs. Do not infer `cryptalis plan/apply/verify/remove/keys rotate` commands from intended architecture examples.

The historical real application needs 13 bootstrap lines, four fixture lines, explicit C collation, runtime/maintenance/plaintext roles, operator grants and private bounded delete/cascade opt-ins. These counts omit key custody, manifest, publication and recovery work. Second-app and general framework compatibility remain open.

## Performance

Approved targets remain added p95 <=3 ms for point/equality, <=8 ms for IN-20, and <=2x protected-column-plus-equality-index storage against matched native baselines. These are **targets, not source221 achievements**. Historical results belong to their recorded revisions/workloads. A source regression count is not a performance result.

Write-throughput and pause budgets require explicit decisions. CPU/RSS/WAL/concurrency budgets must not be invented or silently relaxed. Fresh matched native ORM, driver-only, prior-candidate and source221 measurements are still needed. Historical page-query overhead and scaling questions remain tracked.

## Seven qualification gates

| Gate | Status | Remaining qualification boundary |
|---|---|---|
| G-ADAPTER | UNKNOWN | Complete admitted behavior, exact environment cells, independent writer exclusion and least-privilege deployment |
| G-CRYPTO | UNKNOWN | Independent composition/usage/collision review and all applicable vectors/failure proofs |
| G-QUERY | UNKNOWN | Complete admitted semantics/leakage/performance evidence; separately admitted advanced profiles |
| G-LIFECYCLE | UNKNOWN | Independent recovery, retained backups/readers, resource faults, broader metadata/legacy/upgrade paths |
| G-PROVIDER | UNKNOWN | Selected real provider, workload identity, outage/cancellation/recovery/deletion evidence |
| G-POLICY | UNKNOWN | Actual trusted publication, target binding, stale-worker exclusion and restore quarantine |
| G-RELEASE | UNKNOWN | Applicable gates, independent reviews, exact artifact/dependency provenance, fresh-host reproduction and release ownership |

A finite independent test audit is not independent human security certification. Do not deploy to production, publish to PyPI or distribute as security-qualified software without the required evidence and explicit authorization.

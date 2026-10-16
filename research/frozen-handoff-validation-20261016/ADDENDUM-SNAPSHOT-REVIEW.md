# Independent snapshot-drain operator clarification review

2026-10-16 04:10 UTC. **ACCEPTED_SOURCE_SUPPORTED_OPERATOR_CLARIFICATION.** No correction to the proposed paragraph is required. This is a static documentation finding, not a new executed defect or external qualification result.

Reviewed the finding and proposed paragraph in `experiments/migration-operator-order-static-20261016/REVIEW.md`, SHA256 `6f6b265a42468020a88a2980ba86e3770e67274dd2bf1d2efa153655fc880b10`.

The exact relationship is independently confirmed:

- Published QUICKSTART.md step 3 (lines 41–62) and RECOVERY.md lines 11–14 describe affected-writer drain without the same-database snapshot-holder prerequisite.
- Selected source `src/cryptalis/migration.py` lines 744–762 checks other account-bearing backends in the current database with nonnull backend_xmin, without a protected-table or writer-role filter. `_switch` calls this before destructive field/index work (765–775). `apply` commits expansion/backfill in separate transactions before the switch (825–850), so this refusal need not mean nothing has happened.
- Existing `tests/test_migration_snapshot_boundary.py` specifies refusal/resume for repeatable-read/serializable transactions, server cursors and exported snapshots; idle connections without snapshots do not block. The cursor case uses generate_series, not a protected-table writer. A snapshot started after the guard can see committed staging. These are source assertions only in this review; no fresh per-case execution receipt or continuous-quiescence guarantee is inferred.
- The proposed paragraph correctly arranges authorized completion/rollback of relevant snapshot holders, keeps writer exclusion, retains the original operation/artifact/staging and checks actual progress/current authority before approved resume. It excludes blanket disconnects, guard bypass, journal deletion, blind business-write replay and unapproved session termination. Scheduling a dependable cutover window is not presented as online-migration qualification.

Root may carry this paragraph in a new external supplement, cross-referenced before first default apply and in recovery. Preserve frozen product/guide bytes and historical acceptance; no helper, query or automatic remediation is needed. Public smoke remains unexecuted and all objectives/gates retain their prior open/UNKNOWN status.

Scope: finite source/test text, safe guide and report inspection only. No imports, product/helper execution, test rerun, database/status command, network, Git action, private input or live payload inspection. This report does not re-review the author's separate compiler/policy analysis.

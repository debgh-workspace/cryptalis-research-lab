# Migration/activation operator ordering: static review

16 October 2026, 04:09 UTC. Selected candidate: `candidate-doctor-remedy-integrated221-v1-20261015`, source221 manifest `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7`. Static source/docs review only.

## Finding: writer-only drain instructions omit the database-wide snapshot barrier

**Actionable documentation gap, fail-closed operational consequence.** The published quickstart tells the evaluator to stop/drain affected writers before the first default `apply`; it never tells them to arrange completion/rollback of other snapshot-holding transactions across the same database. The selected implementation requires this before switching, including read-only transactions and account-bearing background workers unrelated to a protected table. The evaluator can follow the listed writer instructions and still stop before PENDING, after earlier staged progress has committed. This is a concrete missing pre-cutover step, not a demand for online migration or a demonstrated protection bypass.

### Exact support

Let `S = cryptalis-executable/candidate-doctor-remedy-integrated221-v1-20261015` and `G = cryptalis-executable/preview-docs-v4-source221-20261015`.

- `G/QUICKSTART.md:41–53`: step 3 says “Stop/drain every affected writer and exclude alternate writers first,” constructs maintenance approval, then invokes default apply to PENDING. It names no read-only/database-wide snapshot drain.
- `G/HOST-INPUTS.md:24,69–74`: inventories writers and supplies maintenance/authority inputs; no snapshot-holder exclusion step is supplied.
- `G/RECOVERY.md:11–14`: repeats writer drain then default apply and activation; its later general uncertain-outcome guidance does not state this particular prerequisite.
- `S/src/cryptalis/migration.py:744–762`: `_require_no_other_snapshots` clears the statistics snapshot, then checks the entire current database for any other backend with `backend_xmin IS NOT NULL` and `usesysid IS NOT NULL`. There is no protected-table, writer-role or query-kind filter. Comments explicitly include account-bearing background workers. It refuses with `other_database_snapshots_active`.
- `migration.py:765–775`: switch performs verification, obtains the switch lock, then calls that barrier before destructive field/index work. Table locks alone do not solve the old-snapshot issue (`747–751`).
- `migration.py:825–850`: default apply targets PENDING; expansion and loop iterations use separate transactions. The refusal can therefore occur after expansion/backfill, not merely before all effects. Exact progress must be inspected rather than guessed.
- `migration.py:34–52`: the existing error already directs “Finish or roll back other database transactions, then inspect and resume the same operation,” keeping writers stopped and current external policy reconciled.

### Existing source evidence, without a new execution claim

`S/tests/test_migration_snapshot_boundary.py` supplies the exact behavioral cases:
- `8–25`: REPEATABLE READ/SERIALIZABLE snapshot refusal and same-operation resume after rollback, in both protection and reversal directions.
- `28–32`: an idle connection without a snapshot does **not** block; a blanket “disconnect every connection” instruction would overstate the requirement.
- `35–49`: a snapshot begun after the guard can see committed staging; the barrier is not proof of continuous database quiescence or an online-migration guarantee.
- `52–65`: statistics-cache refresh case.
- `68–76`: READ COMMITTED server cursor over `generate_series`, unrelated to protected-table writes, refuses until its transaction drains.
- `79–86`: exported snapshot refusal and resume after rollback.

These test sources are present in the selected tree. Current pointer broader suites remain historical original-Integrated221 results; only seven doctor cases per current installed cell were newly executed. This review did not inspect per-case execution receipts or rerun any test, so it does not manufacture a fresh runtime proof for these cases.

### Smallest external documentation clarification

Insert before the quickstart's first default apply (and cross-reference it in recovery), subject to root review:

> Alongside actual exclusion of every affected writer, arrange an authorized cutover window in which other account-bearing transactions holding snapshots in this database can finish or roll back. This includes read-only repeatable-read/serializable transactions, exported snapshots, server-side cursors and account-bearing background workers, even when they do not access protected tables. Idle connections without a snapshot need not be disconnected. The library checks this barrier at switch; a planning result or maintenance-approval record does not prove it. If `other_database_snapshots_active` occurs, keep writers stopped, preserve the original operation/artifact and staging, have the responsible operators finish or roll back the relevant transactions, inspect actual progress and current external authority, then resume the same operation only within approval. Do not bypass the guard, delete the journal, terminate sessions without separate authority, or blindly replay business writes.

No new helper, database query, termination command, product change or automatic remediation is proposed. Preventing new snapshot holders through the existing authorized host procedure can make a cutover window dependable; this is an operator scheduling prerequisite, not a new correctness/online capability claim.

## Assertions versus proof: existing guidance is substantially explicit

No additional concrete current-authority ordering defect was established in the reviewed sequence:

| Boundary | Documentation | Selected API enforcement / remaining host responsibility |
|---|---|---|
| Writer inventory | `HOST-INPUTS.md:14–24` explicitly says example strings are assertions, real evidence and exclusion enforcement are required. | `manifest/compiler.py:309–331,348–349` validates record structure/routes/evidence strings and labels inventory `host_assertion`; it cannot discover all writers. |
| Maintenance approval | `QUICKSTART.md:43–49`; `HOST-INPUTS.md:70–71` require real exclusion and approved pause; constructors are not approvals. | `migration.py:391–398` checks a nonempty exclusion string and sufficient finite pause value, not the truth of exclusion. `644–647` expressly leaves owner/DDL-capable writers to the operator; the trigger exempts the owner. |
| Current external authority | `QUICKSTART.md:43,53–62`; `HOST-INPUTS.md:72–74` require trusted exact PREPARED, publication/ACTIVATING, then ACTIVE outside database restore; no automatic publisher. | `migration.py:384–388,471–486` matches identities and state ordering, not external authenticity. `805–812` demands ACTIVATING then removes guards; `904–912,926–931` requires planned role and matching ACTIVE database/pin at attachment. |
| Restart/order | `QUICKSTART.md:62–75` places ACTIVE authority before attachment; `RECOVERY.md:14` says restart fresh attached workers only after successful activation and host checks. | Retain host writer exclusion across publication/activation and attach. Dropped database guards are not permission to restart old unattached workers. This is already required by the combined instructions, not a newly found omission. |
| Pause estimates | `QUICKSTART.md:39`; `HOST-INPUTS.md:70` require measured inputs and disclose omitted delays. | `migration.py:314–317,368–371` labels host estimates, excluding lock drain/DDL/index/publication and capacity guarantees. An approved numeric estimate is not a deadline or measured pause SLO. |

**Answer:** An attentive evaluator is explicitly warned against treating supplied strings/pins as proof, and the documented authority phases are ordered consistently with the selected API. Nevertheless, the writer-only drain recipe is operationally incomplete because it omits the database-wide snapshot-holder step. Correct that narrowly in an external supplement; preserve current gates and historical evidence.

All 34 final objectives remain active and all seven qualification gates UNKNOWN. Public smoke remains unexecuted unless separately established by a later accepted receipt. No implementation exploit or newly executed defect reproduction is asserted.

## Read-set identity

- `CURRENT_CANDIDATE.json`: SHA-256 `96970253998d2f86b7eb58d11778093629e19994b078bb1dfd1175d98b9d16a3`.
- `cryptalis-executable/preview-docs-v4-source221-20261015/QUICKSTART.md`: SHA-256 `50c5369684bb1b3abd9fa8969a5131a82e47ba7909478ec6c52ac01c93d90e9d`.
- `cryptalis-executable/preview-docs-v4-source221-20261015/HOST-INPUTS.md`: SHA-256 `a02e7e5306825d479681bbf804213f0035fca25492afa377b2c220ea63330c18`.
- `cryptalis-executable/preview-docs-v4-source221-20261015/RECOVERY.md`: SHA-256 `5b6818a3abdee4f603934870922a575c150b35d436d1fc1b67548073687b64e6`.
- `cryptalis-executable/candidate-doctor-remedy-integrated221-v1-20261015/src/cryptalis/migration.py`: SHA-256 `94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014`.
- `cryptalis-executable/candidate-doctor-remedy-integrated221-v1-20261015/src/cryptalis/manifest/compiler.py`: SHA-256 `dca174cba23517abfcb03e8a1df7ef12f9f7e1171b765e3c1b2da26edb23951b`.
- `cryptalis-executable/candidate-doctor-remedy-integrated221-v1-20261015/tests/test_migration_snapshot_boundary.py`: SHA-256 `ec0d5fa61fdc5e14e81763ad07b5cdd8581411e31602250069b228249df2487a`.

Only this isolated report was written. No product/documentation/handoff/root edits, imports, helper/product execution, tests, live state/status/database inspection, private bodies, credentials or Git operations occurred.

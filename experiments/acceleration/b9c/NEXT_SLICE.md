# Next integration slice: database switch with publication still pending

Status: source-inspected proposal. This pass did not run tests, connect to PostgreSQL, change executable files, or use Git. It does not authorize an effect. Root reported 22 profile/journal cells in each SQLAlchemy cell and 55 new negative cells in SA21; those are parent-supplied results, not independently rerun here.

## Conditional switch design, not the immediately authorized increment

Read ADMISSION_FIRST.md first. The exact source-row handoff, retained lineage and reverse route below are not specified executable contracts. They require root/owner resolution before implementation or payload replacement. This design is the next bounded switch candidate only after that resolution.

The next meaningful switch slice is a bounded **transactional payload replacement that stops at database-switched / external-policy-pending**, with native proof that the old attachment is denied. Do not build a generic rotation API, publish generation 2, or repeat inactive profile expansion first.

Use one UUID/equality, one-model/one-field/one-tenant synthetic fixture first. Consume a verified B9B inactive preparation, retain every committed target byte, repeat full verification under the switch transaction's source lock, atomically install the prepared bytes and a fail-closed source-operation handoff, then stop. Existing product admission must remain closed. This is a research-only implementation of the existing lifecycle switch boundary, not active rotation or deployment qualification.

The previous inactive artifact grants **preparation only**. It cannot authorize this switch. An independently supplied, operation-bound switch approval is required before the first source mutation. Root must establish whether its existing owner authorization covers this exact synthetic switch and test-owned journal changes; this review supplies no such authority.

## Why this slice

The inactive experiment's `_authority` and `_journal_rows` require an ACTIVE original protection operation. Its terminal operation phase is PREPARED_INACTIVE, and its original source journal digest must remain unchanged (experiment lines 250–275, 399–409, 673–805). That is the correct inactive boundary.

`migration._state` fetches only the original operation UUID. `_check_connection` checks original ACTIVE phase, target, runtime permissions and active schema (lines 414–431, 826–836). A second pending row by itself does not invalidate that original ACTIVE row. Replacing a bytea column's values does not necessarily change `_facts`. Therefore a switch that only changes payloads and the preparation row would leave the old deployment's structural admission open. The adapter does bind its Keyring policy to the original plan (`sqlalchemy.py:405–436`), so this observation does **not** establish wrong-key plaintext release. It establishes that a rotation needs an explicit source-admission handoff.

Use existing fail-closed phase admission to close the source. Do not fabricate a new protection MigrationPlan, change the old plan's key_policies, relabel a preparation row ACTIVE, or broaden PHASES to make a generation-2 attachment pass. A dedicated explicit source handoff state is clearer than reusing protection's PENDING phase, whose meaning is protection publication.

## Exact proposed state transitions

The names below are proposed research encoding, not new public commands or canonical phase requirements.

1. Initial: original source row ACTIVE; preparation row PREPARED_INACTIVE; live selected field generation 1; stage generation 2; current external source pin unchanged.
2. Read-only plan: external switch artifact names both operations/digests, exact source plan/current pin, preparation artifact and terminal state digest, target identity, scope, source and target policies, desired external artifact digest, retained stage identity, approved pause/writer exclusion, implementation revision and exact allowed journal/data deltas. It creates nothing. The desired artifact is host-supplied, not reconstructed from PostgreSQL or silently manufactured by the executor.
3. Switch transaction: under the same source-plan advisory lock and write-excluding table lock, verify all current facts and target bytes. Then replace only the selected live payload values, conditionally change the preparation row to SWITCHED_DATABASE_POLICY_PENDING, and conditionally change the original source row to ROTATION_POLICY_PENDING with an exact successor binding. All three effects commit together. Preserve the original source state's other members and bind its exact pre-switch digest; preserve the preparation batch receipts. The source row's operation UUID and plan digest remain unchanged.
4. Committed pending: live selected field contains exactly the already staged generation-2 frames; both rows identify the same handoff; external pin remains source generation 1; all application admission remains denied; writers remain host-stopped. No ACTIVE target state exists in this slice. Stage is retained, not retired.
5. Failed transaction: original ACTIVE source row, PREPARED_INACTIVE preparation row, generation-1 live bytes and stage bytes all remain exact. No intermediate durable combination is valid.
6. Unknown reply: UNKNOWN / inspection required. A new process takes the same advisory lock and inspects both rows and live/staged exact bytes on the trusted current primary after the original backend is terminal. Valid pre-switch state means the switch did not commit; valid coupled pending state means it did. Any mixed combination refuses, with no repair. An absent marker while the original transaction can still commit remains UNKNOWN.

The existing migration reader rejects ROTATION_POLICY_PENDING because it is not an admitted protection phase. Keep that denial. A test-local pending inspector must inspect the new state without calling inactive `enter` or pretending the source is still ACTIVE. Do not add the new phase to migration.PHASES merely to share its ordinal phase comparison.

## Required invariants and implementation boundaries

- Existing B9B artifact/state parsing remains exact and unchanged. Put this next slice in a separate experimental switch module. A new immutable switch artifact may reference the preparation; it does not reinterpret inactive approval.
- Every entry independently receives current source authority, exact target policy, prepared keys and maintenance/switch approval. Journal evidence never selects current host policy. Target publication and startup admission are absent.
- Keep one PostgreSQL journal. No second journal, lease service, worker registry, marker table, automatic publisher or credential change.
- Require the existing one-model/one-field source plan and complete selected tenant scope. Reject unsupported scope expansion. An operation cannot change a tenant/domain key policy for untransformed fields elsewhere and claim that policy active. This slice does not make such a claim.
- Full terminal verification must run inside the switch transaction, not as a completed prior call to `enter(action='inspect')`. Refactor a bounded internal inspector if necessary in the derivative; never release the table lock between the deciding scan and DML.
- Verify exact typed membership, current source revision, source/target authenticated values/types/NULLs, target payload generation, unchanged search policy/header/term bytes, valid unchanged indexes/constraints, source schema and role/ACL facts. Existing `_prefix` and `_source` are reusable mechanisms, not substitutes for post-copy native observation.
- Copy bytes by exact typed record and tenant identities with exact affected-row counts. Do not call seal for any row at switch. Do not build an unbounded joined result, weaken logical source/target transport bounds or replace NULL with an empty frame. The first fixture is bounded to the existing 64-row/4-MiB source limits.
- After copying, independently rescan live membership and exact target bytes, check index validity/definitions and NULL parity, and compare with the just-verified stage. Then conditionally update both journal rows against their exact prior values. A stale or missing rowcount rolls back everything.
- Recheck both prepared bindings after verification, after all DML, and immediately before COMMIT. Keep existing lease limits; no TTL extension or server-commit-time revocation claim.
- The source row changes only in this explicitly approved switch. This does not revise B9B's guarantee that inactive preparation preserves it. Inactive entry after the switch must refuse.
- Preserve all nonselected fields, identities, unrelated tenants, stage bytes, journal receipts, source/index ownership and grants. No plaintext enters a staging relation or SQL bind. Do not drop old reader/key dependencies or call provider-admin operations.
- Host writer exclusion remains necessary throughout pending downtime. An attachment error or advisory lock does not stop an independent driver, old transaction, reconnecting worker or owner. Require the existing snapshot/transaction checks where applicable; do not claim a database-wide durable fence.
- No source snapshot rollback after switch. Resuming pending is inspection-only in this slice. A later rollback must transform current data under a separately approved transition.

## Frozen deciding tests for the first RED/GREEN increment

Run root's unchanged PostgreSQL wrapper with the existing dual-role preflight in each pinned dependency cell. Root owns all execution. No count below is a claimed result.

1. `test_switch_stops_pending_preserving_exact_prepared_bytes`: current edited/inserted/deleted source fixture, Unicode/empty/NULL, at least three committed preparation chunks. Independently decode expected values and observe exact stage-to-live byte equality, generation 2, unchanged terms/indexes/nonselected values, coupled journal states, unchanged external pin and zero sealing calls. Assert no target attachment/publication is invoked.
2. `test_pending_denies_original_deployment`: normal generation-1 application read works immediately before switch. After pending commit, fresh startup/check_deployment and a warm attachment's next newly begun operation fail with a typed admission error before business SELECT/write. Inspect live bytes independently. No claim about already returned values or transactions the host failed to stop.
3. `test_switch_kill_before_commit_rolls_back_all_effects`: SIGKILL a real exec worker after payload writes plus both journal updates, before COMMIT; wait for backend terminal. Independently see exact original live bytes and journal states, unchanged stage; new worker can perform the same approved switch once.
4. `test_switch_lost_reply_requires_coupled_inspection`: use the existing real transport COMMIT-reply-loss mechanism with an explicit barrier. Report UNKNOWN until original terminal state is observed. Fresh process recognizes committed pending, performs zero seals/data DML, preserves all bytes and remains pending.
5. `test_switch_revalidates_terminal_preparation`: source changed after PREPARED_INACTIVE (valid same-value reseal); staged authenticated wrong value with a correspondingly edited stored commitment; missing source or stage row; changed exact index definition/validity. Each blocks source/journal DML and preserves previously committed preparation.
6. `test_switch_authority_and_lease_refusals`: missing/mismatched switch approval, changed current source pin, changed target policy/desired-artifact digest and source/target lease expiry at final before-commit observer. Pre-entry failures issue no DML; final expiry rolls back all in-flight effects.
7. `test_pending_inspection_refuses_mixed_or_foreign_lineage`: wrong operation/digest/target, missing one handoff, live bytes inconsistent with pending commitment, or unknown phase refuses without repair. A live competing executor is pending/busy, never inferred rollback.
8. Mutation sensitivity in a disposable derivative: omit only the source-row admission handoff and test 2 must fail; split journal update from payload transaction and test 3 must fail; omit the fresh full verification and test 5 must fail. These are controlled local correctness mutants, not third-party exploitation.

Retain B9B journal/profile and final-binding regressions. Do not claim all-profile switch coverage from UUID/equality. Expand to UUID/storage and BIGINT profiles only after this exact boundary passes both cells.

## Authority and stopping point

Already selected high-level design, not approval of the proposed state encoding: A4 isolated rotations; one journal; maintenance pause; full verification; atomic PostgreSQL switch; separate host publication; no mismatched admission. The canonical contract supports the pending outcome, but does not select this proposal's ROTATION_POLICY_PENDING source-row encoding, successor representation, or reverse-plan admission. Do not call those details already approved.

Authorized in this review: read source/contracts, recommend the slice and write these notes only. No implementation, database switch, policy publication, source-row rewrite or production effect was performed.

Before implementation/execution, root must resolve exact scope against the owner's existing instructions. If not already covered, obtain permission for a synthetic database-only generation-2 payload replacement and the coupled source/preparation journal changes, explicitly stopping pending with no generation-2 publication. This is an effect approval, not a request to select a new production authority architecture.

Still owner/deployment decisions: the actual trusted publication tool/provenance; exact desired policy artifact and recovery custody; concrete pause estimate/approval; real writer stop/reconnect exclusion; any role/credential changes. Do not invent these. A public fixture artifact establishes local functional behavior only.

Next stopping condition: both dependency cells prove the coupled database-pending boundary and denial tests; source is reviewed; no active target exists. A later, separately bounded slice must establish actual generation-2 deployment admission, restart/fresh-key behavior, current-data reverse recovery and retained-reader obligations. All full gates remain UNKNOWN.

## Source anchors

- docs/lifecycle.md: Maintenance and ownership; Plan and phases; Changes and rotation; Restore and authority loss; Supported deployment candidate.
- docs/decisions.md: selected lifecycle/current-authority choices and owner A4/A5 amendments.
- docs/build-guide.md: slices 5 and 7, no mismatched policy admission.
- experiments/payload_rotation_journal.py SHA-256 ac09b3c0f70c3089aada5bf584d64487072d7b8ea7083292e543773e03a4a8df.
- src/cryptalis/migration.py SHA-256 64c9ff601a36352f5cee74d6d11b4ff8a469f10475816b2fac335327f7afe1b8.
- src/cryptalis/sqlalchemy.py SHA-256 fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe.
- Prior corrected same-journal preparation contract and B9B independent profile review.

# Smallest test-only slice: B9A same-journal inactive preparation

Status: PROPOSED implementation contract, not executable evidence. Root owns database execution, promotion and publication. Source, tests and credentials remain unchanged by this review.

## One observable claim

For one bounded UUID/equality field and one tenant in an already-active generation-1 fixture, a worker can prepare generation-2 ciphertext in an inactive table, atomically record each chunk in the existing single journal, and resume in a fresh process without replacing any committed target bytes. Changed source, authority or durable prefix refuses before dependent DML. Active readers/writers remain generation 1. No active rotation, production recovery or global exactly-once claim follows.

## Files and order

1. In a fresh S20 derivative, add only `tests/test_payload_rotation_journal.py` first. Use a lazy import of the absent `experiments.payload_rotation_journal` at call time, so the initial RED is an explicit missing-feature outcome rather than an unexplained collection failure. Root runs the named positive native scenario through the unchanged `scripts/test_postgres.py` and records RED.
2. After root accepts RED, add `experiments/payload_rotation_journal.py`. Keep the worker entry in this same test-only module for this slice: a bounded command receives the nonsecret artifact path and an operation action. Avoid an extra worker framework. Public fixture setup/oracles remain in the test file. Use the existing subprocess/database fixture mechanisms; do not inherit key material.
3. Do not modify `src/`, existing tests, canonical docs, wrappers, dependencies, packaging, role setup or migrations. Record all 208 base-file hashes before and after. These new files are research only and must remain outside package exports and wheels.

## Frozen fixture

- One source-plan model, one selected equality field, explicit UUID tenant and UUID record codec. Refuse other profiles in this first slice.
- Five selected rows, ordered by native PostgreSQL UUID order, chunk size two; three committed batch receipts. Include NULL, empty text, Unicode and a current post-protection edit. Include pre-plan insertion/deletion so the expected map differs from the historical pre-protection map.
- Hard cap 64 selected rows and 4 MiB total source-frame bytes. Use a small explicit B8 logical-byte budget in tests. The whole bounded state document contains at most 64 row entries and 64 batch receipts; reject excess/unknown structures before mutating anything.
- Start with an authorized existing ACTIVE generation-1 source plan, source journal row and externally supplied current source pin. Use an unchanged generation-1 attached runtime read as a control. Root owns any initial setup needed to establish this fixture; the experiment does not activate it.
- One uniquely named test-owned stage relation created before artifact binding. Its columns are operation UUID, native UUID record ID, UUID tenant, positive batch ordinal, 32-byte source-row commitment and nullable bytea target frame. Primary key `(operation_id, record_id)`.
- Exactly one canonical `_cryptalis_journal` exists in the bound schema. Reuse its existing definition and ACLs. No new grants, routines, triggers or journal relation.

## Artifact and journal row

Canonical artifact fields must bind: version/kind, operation UUID, source operation UUID and source plan digest, target UUID and observed database/owner identity, original model list, source relation and stage/journal OIDs, exact descriptor digest/record codec/tenant, external source-pin digest, exact source-row JSON commitment, source/target key-policy fingerprints, source membership/content commitments and count, relevant source schema/object owner/ACL commitments, row/byte bounds, maintenance assertion, implementation revision hashes and precise allowed object inventory.

Keep external authority inputs independent from the stored row. Never reconstruct expected source policy or artifact from database contents. Artifact path receives no credentials or secret roots. Its digest is lowercase SHA-256 hex, matching the existing journal's text `plan_digest` column.

The new operation has one journal row. Its `state` has exactly these top-level members:

- `schema`: `cryptalis.experiment.inactive-payload-preparation/v1`
- `kind`: `INACTIVE_PAYLOAD_PREPARATION`
- `source_operation_id`, `source_plan_digest`, `artifact_digest`
- `phase`: `PREPARING` or `PREPARED_INACTIVE`
- `source_revision`: the bound count, membership and content commitments
- `batches`: ordered receipts, initially empty
- `verification`: null until terminal commit, then a bounded commitment/count receipt

No free-form exception, provider object, key material, ciphertext or plaintext belongs in state. Each batch has ordinal, cursor-before/after, ordered record identities with source-row commitments and NULL discriminators, target commitment, row count and B8 logical-byte count. The format binds policy/descriptor via the immutable artifact digest rather than inventing per-batch authority. Counters are derived from `batches`, not an independently mutable authority. A duplicate, gap, wrong type, unknown member, noncanonical UUID or inconsistent cursor rejects.

Preserve the source journal row exactly in canonical logical value, including its ACTIVE phase. Do not claim PostgreSQL physical JSONB/page byte preservation. The experiment inspects the exact allowed journal row set: source alone before explicit start; source plus this exact preparation operation afterward. Unrecognized rows refuse. A new operation UUID cannot adopt an old stage. Root may use separate fixtures for competing-operation tests.

## Entry algorithm

1. Validate artifact/current host inputs and module hashes before any target or journal DML. Require one-model source plan and explicit maintenance assertion. Construct fresh public fixture provider/keyrings; check exact policy fingerprints.
2. Open the existing owner engine with safe logging and the existing cleanup discipline. Match `_target` identity. Set finite lock timeout and synchronous commit. Acquire the exact source-plan advisory lock formula used by S20; invalidate the physical session at exit. Do not fabricate a MigrationPlan for `_executor`.
3. Begin the chunk transaction, acquire EXCLUSIVE lock on the source table and row lock on the preparation journal row when present. Validate source ACTIVE admission using the real original source plan/pin; test-local validation owns the new row. Compare exact stage/journal/source OIDs, definitions, owner and effective privileges. Inspect existing runtime permissions without changing them.
4. Select only identities, NULL state and octet lengths first. Reject count/aggregate size excess and any single-row logical cost above the batch bound. Only then retrieve the bounded source frames and compute exact native-ordered source commitments. A NULL record advances identity membership; absence is different.
5. Explicit start requires no preparation row or stage rows and exact source baseline. Insert the empty preparation row in a bounded transaction; resume requires that exact row. Missing state never grants permission to recreate it. Initialization must be fault-testable: source/stage observations cannot silently survive without the expected preparation row.
6. Independently inspect the complete persisted prefix: exact batch sequence, ordered source prefix, source commitments, stage membership, target commitments, NULL parity and authentic decoded source/target value parity. Compare exact search header/term bytes. Do not invoke sealing on a committed member. Refuse orphan rows, extra rows, missing rows, unknown state or changed source/authority before new DML.
7. Choose the next prefix under row and B8 logical-byte bounds. Call unchanged `prepare_payload_rotation_batch` with an immutable tuple. Check returned exact identities, descriptor and source/target binding. Insert new stage rows; append their batch receipt with a conditional update of the same operation row constrained by operation UUID, plan digest and exact previous state. Require expected affected counts. Recheck both prepared bindings immediately before commit.
8. A successful commit establishes this chunk only. Any commit exception or lost reply returns inspection-required with last independently observed progress. Do not auto-retry inside the uncertain session. A fresh worker must acquire the same scope lock; busy means pending. After it acquires the lock and reconciles the original row/stage, preserve the committed prefix or prepare only the proven uncommitted next batch.
9. With no rows remaining, hold the source lock for full source/stage membership, values/types/NULLs, target generation, exact search preservation and binding/catalog verification. Atomically update only this operation row to PREPARED_INACTIVE with the terminal receipt. Return inactive success only after commit. Repeat terminal inspection is read-only and revalidates current facts.

No durable writer fence is installed. The host fixture has no concurrent source writers except controlled tests. Table locks exclude writes only while held; exact source reinspection detects intervening changes. This experiment does not qualify deployment-wide pause enforcement between chunks.

## Minimum deciding tests for this slice

Freeze concrete selectors before GREEN. These are required behaviors, not a claim that tests already exist.

1. `test_current_values_same_journal_inactive`: five-row fixture, three exact batches, independent decode against native expected map, source-to-stage and reverse membership, exact term preservation, unchanged original source row/pin/catalog, generation-1 attachment still reads, precisely one journal relation. Repeat terminal inspection has zero seals and zero mutations.
2. `test_restart_preserves_committed_prefix`: real exec worker killed after first chunk commit; confirm old backend is terminal, start fresh provider/keyring process, inspect original state, preserve exact first two target frames and first batch receipt, seal only remaining rows, then full independent parity.
3. `test_uncommitted_chunk_rows_and_marker_rollback`: kill after second batch's stage writes and journal UPDATE but before COMMIT. Independent observation after backend termination finds first batch intact and no second-batch rows/receipt. Fresh resume completes normally. This is the minimal atomicity deciding fault.
4. `test_lost_reply_requires_inspection`: use the existing actual COMMIT-reply-loss fixture, targeted by a deliberate transaction/barrier rather than a magic commit count. Original result is UNKNOWN; fresh process inspects terminal outcome and preserves committed bytes. Do not claim lost-reply recovery without this real transport case.
5. `test_busy_executor_is_pending`: first worker held live before its second commit; second cannot acquire the same lock, performs no DML and does not infer rollback. Release the first normally and inspect its actual outcome.
6. `test_source_change_refuses_resume`: two parameters, a valid fresh reseal of the same value and insertion behind saved cursor. Both refuse with prior stage/preparation row unchanged; membership-only or last-key logic must not pass.
7. `test_changed_external_pin_refuses`: changed supplied current pin refuses before journal/stage DML even if stored progress is internally consistent.
8. `test_inconsistent_prefix_refuses`: two parameters, missing stage row and changed valid target value with its recorded hash adjusted. Both refuse without repair; the latter must exercise value comparison beyond stored hashes.
9. `test_expiry_before_commit_rolls_back`: expire source or target lease after stage/journal DML and before final binding check; actual rollback preserves prior prefix and removes entire in-flight chunk. Fresh same-policy preparation can resume.
10. `test_existing_runtime_cannot_mutate_metadata`: native existing-runtime operations cannot mutate/own/truncate stage or journal; actual denials and unchanged permissions are recorded. Source runtime reads remain admitted with generation 1.
11. `test_chunk_budget_precedes_frame_transport`: exact-fit and first-row-over-budget cases. Observe projections/crypto calls so the oversized frame never reaches the client and creates no empty marker.
12. `test_safe_output_collector`: calibrate the diagnostic collector with an unprotected sentinel before asserting protected plaintext/root/credential/raw-exception absence. Frame/term bodies remain permitted only as intended stage storage/transport, never in diagnostics.

Run unchanged B8 final-binding controls and the directly affected crypto/key-lease/migration cleanup controls. Root selects exact existing node IDs from source and runs both pinned dependency cells. Report the smaller scope separately from the original four-profile 48-cell matrix; bigint/storage profiles, terminal-output failure variants, expanded artifact/layout/corruption matrix and sensitivity controls remain later work.

A missing-module RED proves only feature absence. An implementation PASS is meaningful only with real PostgreSQL 16 dual-role preflight, source-bound receipts, independent observations and the actual failure cases. A failed preflight stops the run; no alternate role/database/cluster or credential repair is permitted by this slice. Root alone runs these checks and decides whether the bounded result can be integrated.

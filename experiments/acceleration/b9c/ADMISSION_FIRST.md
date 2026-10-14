# Immediate implementable increment: native admission characterization

Status: review recommendation only. No executable file, database row or product behavior was changed.

## Result and contract boundary

The lifecycle explicitly requires a database-switched / policy-pending interval with stopped writers and mismatched startup denied. It also requires transform-back from current active data until explicit finalization. It does not explicitly select a rotation successor plan format, a source-operation supersession state, retention/removal handling for that successor, or how deprotection accepts its current target policy.

Consequently, the proposed ROTATION_POLICY_PENDING state in NEXT_SLICE.md is not an approved existing contract. Do not implement the proposed active payload replacement yet. A4 permits isolated rotation investigation, but this review must not turn that broad authorization into approval of a particular source-journal rewrite or complete reversal design. Root must resolve the exact authority before those effects.

The narrow next executable work can be a test-only PostgreSQL admission characterization. Leave every live payload at generation 1 and publish nothing. Use the already authorized synthetic fixture and existing owner/runtime roles. Test-only metadata mutation still needs to be within root's fixture authorization. This increment establishes exactly which existing admission calls close and which leave a new successor invisible; it does not install a new state machine.

## Minimal test file and observations

Proposed new file in a fresh derivative: tests/test_payload_rotation_admission_boundary.py. Reuse B9B fixture setup and cleanup; do not alter product source, the preparation protocol or its artifact. Freeze the experiment/source hashes and native expected byte/journal snapshots.

1. `test_inactive_preparation_keeps_source_admitted`: before preparation, after a committed PREPARING chunk, and after PREPARED_INACTIVE, use real check_deployment plus fresh source attachment to read exact current values with the original generation-1 policy. Confirm the original source row/pin/live bytes are unchanged. Include terminal inspection with zero seals/DML. This protects the currently approved inactive compatibility boundary.
2. `test_successor_row_alone_does_not_close_original_admission`: in a disposable fixture transaction, present a strictly test-labelled synthetic successor pending row while preserving original source ACTIVE and all payloads. Observe actual check_deployment and fresh attachment behavior. Current source indicates they remain admitted because `_state` selects only source operation UUID. Record that as a characterization/gap, never PASS for pending safety. Restore via fixture rollback/teardown. Do not invoke real publication or fake a generation-2 active pin.
3. `test_nonactive_source_phase_closes_original_admission`: in a separate disposable fixture, set the source row to an explicit unknown research-pending phase while retaining generation-1 bytes. Native source deployment inspection and fresh attachment must reject. This verifies current fail-closed behavior, not approval of that phase or a future switch protocol. Add an existing documented protection PENDING case if the fixture can supply it without fabricating plan authority; label the distinction.
4. `test_target_keys_cannot_reuse_source_deployment`: use unchanged original plan/pin with the generation-2 target key policy and normal adapter entry. It must reject policy mismatch before protected business SQL. This establishes the separate `_ring` policy binding and prevents a misleading wrong-key plaintext-release conclusion.
5. `test_warm_source_attachment_rechecks_new_operation`: create the attachment under original ACTIVE state; finish its transaction; apply only the fixture metadata pending change; start a fresh operation on that warm attachment. Record whether it denies before business SQL. Do not infer stale-worker termination or denial for already running transactions from this result. If it does not deny, report the exact execution path as a future correction prerequisite.

Tests 2 and 3 use owner-authored test state solely to characterize existing code. They must not be described as valid lifecycle operations. If root requires a pure valid-state suite first, run tests 1 and 4 alone; the remaining metadata probes are a separate expressly approved fixture action.

## Expected RED/GREEN discipline

The positive inactive and source/target-policy mismatch tests should exercise existing behavior without a product patch. The successor-only test should expose the missing handoff as an observed limitation. A frozen desired test saying "pending successor denies source admission" would be RED today, but do not make it GREEN by admitting arbitrary journal phases or inventing a generic successor reader. First choose the legitimate lineage contract and effect boundary.

An implementation that leaves the original source row ACTIVE and writes only a pending preparation row is insufficient for the desired startup boundary. This conclusion is limited to source admission: adapter policy and frame authentication remain separate protections. There is no demonstrated plaintext release under wrong-generation keys.

Run each selected native test in both existing dependency cells through root's unchanged wrapper/preflight. No new cluster, grants, credentials, triggers, provider calls, public API, package export or active payload DML. Root owns execution and stopping on failed preflight. No database call was made by this review.

## Decisions needed before the subsequent switch candidate

- Select an exact immutable rotation operation/desired policy artifact and source-to-successor handoff. A pending outcome is already specified; the concrete encoding is not.
- State which source and preparation records remain authoritative evidence after switch and how existing readers refuse stale source admission without adopting target authority from the journal.
- Preserve the original plan/reader/key recovery lineage. Specify how a future current-data reverse transition identifies generation-2 source policy and admission; do not trick deprotection.plan into treating the original generation-1 plan as current. Current deprotection.plan rejects unreviewed extra journal rows (lines 138–144).
- Define safe pending inspection and interruption outcome, with a matching external artifact still absent. Stopped writers and unambiguous operator recovery are required; indefinite pending is not active rotation completion.
- Obtain effect approval if existing authorization does not explicitly cover source payload replacement and source-journal handoff. Production publication/provenance, retirement, new roles, grant changes and real provider actions remain separate owner decisions.

The immediate stop is a source-bound native admission receipt with no active replacement. NEXT_SLICE.md preserves the detailed conditional switch proposal and deciding fault tests for review; it is not implementation authorization.

## Delivered test-only candidate

At root's later explicit request, prepared `candidate-rotation-admission-characterization-20261014` with five frozen native tests and no product source changes. The two gap tests deliberately assert current limited behavior; they are not desired-safety tests. In particular the warm attachment case is frozen as expected continued generation-1 reads, based on attach-time validation source inspection. Only root's native run can establish the actual behavior. AST syntax checked; no imports, collection, tests or PostgreSQL performed. All 213 inherited noncache files match the base.

Smallest owner/design decision before active handoff: select and explicitly approve one bounded research lineage contract that (a) makes the original operation non-admitting at the same commit as payload replacement, (b) binds the exact successor/current target policy without database self-authorization, and (c) keeps a documented path for decrypt-back/transform-back from that successor's current values while retaining needed old keys/readers. This does not require selecting a production cloud provider or inventing a new publication service. Until that decision and its tests, stop at admission characterization; do not implement the conditional state encoding in NEXT_SLICE.md.

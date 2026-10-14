# Independent post-run audit: v3 G1 / SQLAlchemy 2.1.3

Date: 2026-10-14 UTC.
Disposition: FAILED / HOLD. Keep every other statistics group and SA20 stopped. Preserve the complete v3 result; no failed case becomes a pass through this diagnosis.

## Deciding result

The selected G1 run reports 20 failed, 9 passed, 66 deselected in 7.79 seconds; JUnit records 29 selected cases, 20 failures, zero errors and zero skips. The wrapper exit is 1. All reported failures terminate in the external test's own final cleanup calling `real.invalidate()` on an already closed SQLAlchemy Connection.

This is a concrete test-packet cleanup defect. The evidence does not identify a new observer-product defect. However, a failing finally block can mask an earlier assertion/cancellation failure, so the 20 failed cases remain failed and product behavior protected by them remains unqualified. No earlier assertion chain is displayed in the retained safe log; that is not replacement evidence for a successful test.

The earlier source/command CLEAR did not detect this test cleanup defect. Actual native evidence now blocks continuation. Original, v2 and v3 review/candidate/packet/run artifacts remain unchanged.

## Exact failure groups

All locations below are in `experiments/s24-statistics-diagnostic-v3-20261014/test_statistics_boundary.py`.

- 10 failures: `test_primary_and_cancellation_survive_rollback_failure`, all five driver/wrapped/callback/permission/cancel variants with rollback false/true; final cleanup line 156.
- 1 failure: `test_no_sqlstate_failure_is_unavailable_without_retry_or_owner_fallback[False]`, the acquired-connection case; line 228.
- 5 failures: `test_fixed_refusal_allowlist_and_malformed_sqlstate`, all four known rejection codes and the unexpected synthetic marker code; line 256.
- 1 failure: `test_collectors_and_supported_host_output_boundary`; line 310.
- 2 failures: `test_cleanup_sqlstate_never_replaces_primary_and_cleanup_cancellation_propagates`, cleanup-cancellation false/true; line 354.
- 1 failure: `test_body_cancellation_wins_over_simultaneous_cleanup_cancellation`; line 375.

Every displayed terminal exception is `sqlalchemy.exc.ResourceClosedError: This Connection is closed`. SQLAlchemy 2.1.3 `engine/base.py:755-759` explicitly checks invalidated/closed and raises from invalidate on a closed Connection. The local 2.0.51 source has the same closed-connection refusal, so trying the uncorrected SA20 packet is not a remedy.

The observer owns the injected Connection, rolls it back and closes it. The test then invokes unconditional fallback invalidation on the real Connection in finally. The test must recognize an already closed object as completed ownership cleanup rather than trying to invalidate it again.

The same unrun defect exists in `test_statistics_metadata.py:76` and `:124`, which affect G2's metadata and aggregate parameterized controls. Do not run G2 merely because only G1 produced the current failure receipt.

## Nine actual passes and their limits

JUnit records passes for:

- Both `test_close_before_cleanup_failure_quarantines_physical_session` variants: 2.
- `test_failed_quarantine_is_explicit_not_release_proof`: 1.
- The acquisition-failure variant of `test_no_sqlstate_failure_is_unavailable_without_retry_or_owner_fallback[True]`: 1.
- All five unsafe-logging refusal variants: echo true/debug, pool.echo true/debug, hide_parameters false: 5.

The close/quarantine cases intentionally leave the real Connection available for the test fallback, so their cleanup does not hit the already-closed error. The acquisition-failure variant owns no real connection. Logging refusal happens before observer acquisition. This explains the pass/fail split without implying the failed controls passed their substantive assertions.

The collector has a further coverage limit: its loop visits `before_statistics=True` first. The failing finally at the end of that iteration prevents its `before_statistics=False` iteration from running. Therefore this run provides no completed statistics-stage negative-output collector result. The warnings containing the known synthetic marker in failure output are the collector's deliberately emitted positive controls, not evidence of a product data leak.

## Required correction boundary

Use an isolated external-test-only successor. Preserve v3 product bytes, tests, all failures and the captured packet. Do not relax observer assertions or change the implementation to accommodate a test-owned error.

Correct every test fallback cleanup with these properties:

1. Inspect actual real-connection closed state. Do not invalidate an already closed Connection or obtain a new connection to clean the old one.
2. Still release/quarantine a genuinely open session after an injected failure, including failed product cleanup; skipping all final cleanup would hide a resource problem.
3. Attempt remaining required cleanup even if an earlier cleanup step fails. Preserve the original assertion/cancellation as primary while recording cleanup failure separately. Do not blanket-suppress ResourceClosedError or other failures.
4. Add safe completion markers only after the substantive assertions actually finish and separately after fallback cleanup succeeds. For the output collector, distinguish each loop iteration. An absent marker remains incomplete; a marker is not permission to relabel the historical v3 outcome.
5. Freeze and independently review corrected test/helper/capture/selector bytes before a fresh coordinator-selected G1 run. Do not retry automatically or advance other groups on the nine passes.

## Source, packet, and corpus integrity

Verified from safe receipts and fresh file-only checks:

- All before actions (new capture, copy, byte comparison and 253-pin check) returned 0; the final 253-pin check returned 0 after the failed runner.
- Both captured before/after pin logs contain 253 OK entries. A fresh independent check of the same full input list still passes.
- All 215 candidate-manifest files pass a fresh independent check.
- The wrapper source stability receipt reports identical 154 scoped source/test/config files before/after.
- External stability reports all six external Python files unchanged. Their archived bytes independently match recorded hashes.
- Thirty pinned external packet files in the full packet capture independently match their original hashes. The capture also retains its manifests/check outputs.
- Corpus isolation reports no archived changes, no deletions, `primary_receipts_restored=true`, and an empty errors list. All 26 pre-run corpus files independently match their prior-manifest hashes now.
- The safe package-origin log identifies the intended v3 candidate import.

The coordinator's separate safe guard-correction record states that an initial hash-filename assertion compared the JSON-manifest hash against INPUTS.sha256, failed before actions/evidence creation, and was corrected to the appropriate separately verified manifests before the unchanged group was run. Preserve that record. It is a coordinator guard error, not one of the 20 test failures or a product defect.

## Shutdown and receipt-handling boundary

Only safe logs and explicitly non-environment receipts were read. No raw phase JSON was opened, extracted, hashed, archived, or published during this audit.

The retained `wrapper.log` contains exact terminal lines:

- postgres-start exit 0
- readiness exit 0
- package-origin exit 0
- tests exit 1
- postgres-stop exit 0

`postgres-stop.log` states that the server stopped. This is shutdown evidence from the safe source-backed wrapper output and shutdown log; it is not an independently read raw phase exit. The prior review's suggestion to inspect a raw phase JSON field is superseded by this safe-log-only handling rule. No sanitizer or wrapper change is needed.

Fresh source/pin/corpus checks do not turn the failed run into success. Preserve the 20 failures, nine passes, selection/deselection counts, cleanup defect, initial guard mistake and every remaining visibility, native-cancellation, UNOBSERVED, mutation, privilege and lifecycle limit.

## Audit scope

The worker performed only safe receipt/source reads, text searches, file comparisons and checksums. No interpreter, candidate import, collection, tests, database commands, installation, remote action, source correction or rerun occurred. The only writes are these additive audit files.

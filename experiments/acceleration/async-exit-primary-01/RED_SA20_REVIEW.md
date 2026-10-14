# Independent RED SA20 terminal audit: ASYNC-EXIT-PRIMARY-01

Date: 2026-10-14 UTC. Decision: **ACCEPT_EXPECTED_RED**, confined to the completed RED SA20 cell.

The expected failing experiment is accepted. This is not a correction, GREEN result, physical-quarantine qualification, installed-package admission, aggregate regression result, release approval, or production-support claim. No further cell was run by this reviewer.

## Identity and terminal outcome

- Evidence: `evidence/next-correctness-red-sa20-20261014` and its `-packet` sibling.
- Frozen proposal: `experiments/next-unblocked-correctness-20261014`.
- External PACKET SHA256 anchor: `6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a`.
- Captured exact RED SA20 command SHA256: `7ce7c6b5552c5ef509876b6b47cf8dd3bd1a225c588b8c0872a46eeea2dbd331`. Captured bytes match the separately reviewed RED SA20 command.
- Captured coordinator driver SHA256: `717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f`. Captured bytes match the reviewed driver. Status records exactly the requested RED/SA20 selection and one captured outer argv.
- Exactly 22 unique source-expanded node IDs match the frozen list, exact command, sanitized runner args, progress start order, and JUnit order.
- Pytest reports **13 failed, 9 passed in 2.57 seconds**. The separately measured runner elapsed time is 2.8794524779950734 seconds. These are different timing boundaries.
- JUnit reports 22 tests, 13 failures, zero errors, and zero skipped. All failures are assertion failures, as established by their message and body. This JUnit format does not provide a failure `type` attribute.
- The 88 progress records are 22 starts and 22 each setup/call/teardown reports. Every setup and teardown passes. Calls are exactly the expected 13 failures and nine passes.
- Runner and wrapper exit 1. Outer shell exit 0 reflects the final successful checks; it is not a passing test result. All coordinator before/after copy and pin statuses are 0.
- The safe outer capture separately reports start 0, readiness 0, package-origin 0, tests 1, and explicit stop 0. The safe stop log ends with `server stopped`.

The first RED SA21 audit and the remaining-command review were read before this audit. The latter's conditional review is not treated as an execution result or automatic progression authority.

## Exact 22-node classification

The complete IDs below are reproduced from the independently reconciled selection. All belong to `tests/test_sqlalchemy_async_exit_double_failure.py`.

1. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[provider-root-native]`
   - **PASSED**: Full selected control passed.
2. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[provider-root-attached]`
   - **FAILED**: Cleanup RuntimeError replaced sanitized KeyUnavailable at line 195; subsequent protected checks unreached.
3. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[provider-savepoint-native]`
   - **PASSED**: Full selected control passed.
4. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[provider-savepoint-attached]`
   - **FAILED**: Cleanup RuntimeError replaced sanitized KeyUnavailable at line 195; subsequent protected checks unreached.
5. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[cancel-root-native]`
   - **PASSED**: Full selected control passed.
6. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[cancel-root-attached]`
   - **FAILED**: Cleanup RuntimeError replaced CancelledError at line 195; subsequent protected checks unreached.
7. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[cancel-savepoint-native]`
   - **PASSED**: Full selected control passed.
8. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_preparation_exit_double_failure_preserves_primary_policy[cancel-savepoint-attached]`
   - **FAILED**: Cleanup RuntimeError replaced CancelledError at line 195; subsequent protected checks unreached.
9. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_exit_invalidation_failure_is_reported_without_replacing_primary[root]`
   - **FAILED**: Cleanup RuntimeError replaced sanitized KeyUnavailable at line 195; subsequent protected checks unreached.
10. `tests/test_sqlalchemy_async_exit_double_failure.py::test_async_exit_invalidation_failure_is_reported_without_replacing_primary[savepoint]`
   - **FAILED**: Cleanup RuntimeError replaced sanitized KeyUnavailable at line 195; subsequent protected checks unreached.
11. `tests/test_sqlalchemy_async_exit_double_failure.py::test_actual_task_cancellation_survives_exit_cleanup_failure[root]`
   - **FAILED**: Cleanup RuntimeError replaced CancelledError at line 195; subsequent protected checks unreached.
12. `tests/test_sqlalchemy_async_exit_double_failure.py::test_actual_task_cancellation_survives_exit_cleanup_failure[savepoint]`
   - **FAILED**: Cleanup RuntimeError replaced CancelledError at line 195; subsequent protected checks unreached.
13. `tests/test_sqlalchemy_async_exit_double_failure.py::test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_override-root]`
   - **FAILED**: Cleanup RuntimeError replaced NoteOverrideCancellation at line 195; subsequent protected checks unreached.
14. `tests/test_sqlalchemy_async_exit_double_failure.py::test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_override-savepoint]`
   - **FAILED**: Cleanup RuntimeError replaced NoteOverrideCancellation at line 195; subsequent protected checks unreached.
15. `tests/test_sqlalchemy_async_exit_double_failure.py::test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_unavailable-root]`
   - **FAILED**: Cleanup RuntimeError replaced CancelledError at line 195; subsequent protected checks unreached.
16. `tests/test_sqlalchemy_async_exit_double_failure.py::test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_unavailable-savepoint]`
   - **FAILED**: Cleanup RuntimeError replaced CancelledError at line 195; subsequent protected checks unreached.
17. `tests/test_sqlalchemy_async_exit_double_failure.py::test_pending_only_preparation_failure_clears_prior_material_without_sql[root]`
   - **FAILED**: Retained PreparedKeys at line 334; reached provider-once/no-SQL checks; later state/effects checks unreached.
18. `tests/test_sqlalchemy_async_exit_double_failure.py::test_pending_only_preparation_failure_clears_prior_material_without_sql[savepoint]`
   - **PASSED**: Full selected control passed.
19. `tests/test_sqlalchemy_async_exit_double_failure.py::test_sync_body_double_failure_keeps_native_exception_policy[root-native]`
   - **PASSED**: Full selected control passed.
20. `tests/test_sqlalchemy_async_exit_double_failure.py::test_sync_body_double_failure_keeps_native_exception_policy[root-attached]`
   - **PASSED**: Full selected control passed.
21. `tests/test_sqlalchemy_async_exit_double_failure.py::test_sync_body_double_failure_keeps_native_exception_policy[savepoint-native]`
   - **PASSED**: Full selected control passed.
22. `tests/test_sqlalchemy_async_exit_double_failure.py::test_sync_body_double_failure_keeps_native_exception_policy[savepoint-attached]`
   - **PASSED**: Full selected control passed.

## Failure mechanisms and what actually ran

Twelve protected double-failure arms fail at test line 195, `caught.value is captured_primary[0]`. Their escaping exception is the deliberately injected cleanup RuntimeError. Four expected primaries are sanitized KeyUnavailable objects, six are CancelledError objects, and two are NoteOverrideCancellation objects.

For each of these twelve arms, the assertions before line 195 establish exactly one captured primary, one intended root/SAVEPOINT rollback callback, and one provider unwrap. The two actual-task-cancellation arms additionally reached provider suspension, returned from the bounded wait for that suspension, called `task.cancel()`, and awaited the resulting replacement exception. They do not establish the later `task.cancelled()` assertion.

This matches the unchanged baseline runtime: `_AsyncTransaction.__aexit__` catches the preparation primary and then awaits native exit without a secondary-failure guard (`src/cryptalis/sqlalchemy.py:1058-1069`). A cleanup exception at that await prevents the following bare re-raise from restoring the original primary. `_AsyncSession._prepare` assigns retained material only after its await returns (`:1088-1090`), so a preparation exception can leave earlier material present.

The thirteenth failure is the pending-only root arm, at test line 334, `_prepared is None`. Its safe failure output shows retained PreparedKeys. The earlier checks establish prior prepared material, one provider unwrap, and no observed SQL after hook installation. The later transaction-state, nested-state, pending-new-state, cleanup-note, and effects checks were not reached.

The audit classified the actual JUnit assertion bodies and full safe test log, not only test names or counts. No runtime source was imported or executed.

## Comparison with RED SA21

The 22 exact outcomes and the 13 failing assertion locations are identical to SA21. A case-by-case comparison of full JUnit failure bodies and messages is equal after normalizing synthetic operation IDs, random `root_id` UUIDs, object addresses, and recorded exception traceback depth. Stable UUID fields were not normalized.

All six failing SAVEPOINT arms display `tblen=24` on SA20 versus `tblen=26` on SA21. Root arms retain `tblen=18`. The version-dependent traceback-length difference is preserved in `sa21-comparison.json`; it is not mistaken for a different failure mechanism. Test assertion, escaping exception, captured primary class, and test source frames match. Synthetic ID and memory-address differences likewise do not imply separate defects.

SA21's 2.50-second pytest timing versus this cell's 2.57 seconds is not a correctness or performance conclusion.

## Assertions still unreached in the twelve double-failure arms

The line-195 failures precede the assertions about:

- Public invalidation attempts, preserved operation/code/stage metadata, exact protected primary type, local effects `unknown`, and retryability false.
- Actual task cancellation state, cleanup/quarantine notes, bypass of custom note hooks, and behavior when note storage is unavailable.
- Sanitized traceback rendering and clearing retained preparation material.
- Session/nested-transaction flags, pool checkout count, independent stored-value and row-lock observations before laboratory rescue.
- Fresh checkout, real commit, and nonpublication of failed inner work or the preflushed outer prefix.

In particular, the invalidation-failure-named arms do not prove that their injected invalidation failure was reached. The note-path arms do not establish corrected note handling. Cleanup in `finally` is laboratory rescue, not a substitute for the unreached protected pre-rescue oracles. Passing setup or teardown does not fill that gap.

## Nine passing controls and their limits

1. Four native asynchronous arms: provider/cancel crossed with root/SAVEPOINT. These establish native secondary-error precedence for the selected primary and one-shot public callback fault. Explicit laboratory invalidation occurs before their successful fresh-checkout/commit, stored-value, and row-lock observations. They do not establish pre-rescue effects equality or physical quarantine.
2. The protected pending-only SAVEPOINT arm: prior material clears; the observed operation emits no SQL; the outer transaction remains; nested transaction and pending-new state are absent; there is no cleanup-failure note; local effects are `none`. Its complete selected test body and cleanup pass.
3. Four synchronous body-error arms: native/protected crossed with root/SAVEPOINT. They preserve existing secondary-error precedence, add no notes, and complete their cleanup. They are not full asynchronous regression coverage.

The callback fault occurs before the selected rollback SQL/driver call. This is not a broken transport or universal hostile-driver experiment.

## Cleanup, origin, and safe evidence

The safe test log, JUnit, and outer log contain no bounded-laboratory-cleanup failure note, wrapper timeout, RuntimeWarning, SAWarning, unraisable/thread warning, or warnings summary. All collection and selected test phases completed; there are no skipped cases, setup/teardown failures, or unexpected assertion locations.

The fixture-local owner transaction limits and final cleanup helper were read as source. The helper restores deliberate hooks before rescue and bounds task completion, Session invalidation/close, and Engine disposal to five seconds each. With an existing assertion failure, any detected cleanup failure is attached to that ordinary AssertionError; with no prior failure it raises an assertion. Neither signal appears. This is bounded evidence for these runs, not a universal cleanup/liveness guarantee. The main task await, explicit rescue invalidation, synchronous cleanup, and cooperative timeout behavior retain the limitations in the prior source review.

The safe package-origin log byte-matches the outer safe origin record: expected RED `src/cryptalis/__init__.py`, expected RED source directory, `verified: true`. It remains a separate-process check, not continuous attestation of every import. Wrapper readiness, test log preflight, and runner receipt agree that both fresh role probes passed with digest prefixes `76053d5b` and `a38ab71b`.

No raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, `postgres-stop.json`, environment, secret, or credential file was read, hashed, or copied. Filenames were enumerated without reading those payloads. Manifest-selected targets were validated before reading/hashing, including restricted source-root/class allowlists, path traversal rejection, and symlink checks. Existing pinned interpreter links were hash-checked only against their already reviewed Python 3.12 target; none was executed. Generated caches were identified by filenames only and never read or hashed.

## Pin, source, capture, and corpus preservation

The data-only verifier confirms:

- All 672 INPUTS, 18 PACKET, and 14 native-source pins match current bytes. Before/after pin logs contain exactly the expected listed path sets in order, with every entry successful.
- All 19 files in the packet copy, including PACKET.sha256 itself, byte-match the frozen packet. The exact full filename sets agree and both copy-diff logs are empty.
- Baseline, RED, and GREEN source manifests equal their 216/217/217 source pin listings. All current source bytes match the listings.
- RED preserves all 216 baseline source files and adds only the 379-line test. The preserved baseline runtime copy matches RED.
- Relative to RED, the source-only GREEN comparison differs only at `src/cryptalis/sqlalchemy.py`; its new test is byte-identical. This observation is no GREEN result or execution instruction.
- Baseline has 170 cache-only extra filenames, RED 29, and GREEN zero at audit time. No source path is missing and no extra non-cache source path exists.
- The RED runtime before/after snapshot has 156 identical entries. Its source-repository evidence copy contains exactly those paths and every copied hash matches RED. The standalone before snapshot agrees. All 155 runner source/test entries match RED.
- The external-source snapshot is empty and unchanged; this provides no broader dependency attestation. The source-root receipt identifies the expected RED candidate.
- The pre-run corpus manifest contains exactly 26 authorized ordinary corpus filenames. Every current corpus and durable pre-run copy matches the recorded hash. The current complete matching filename set equals the pre-run set. The isolation receipt reports restoration true, zero errors, and no archived/deleted entries; the candidate-corpus directory is empty. No corpus drift or new matching file remains.

## Audit artifacts and verifier-only incidents

- `audit_evidence.py`: reviewed data-only checker using standard-library parsing, AST expansion, and hash comparisons; no reviewed module import/execution.
- `audit-checks.txt`, `audit-summary.json`, and `pin-name-validation.txt`: successful verification results.
- `node-audit.json`: all 22 exact node outcomes and reached/unreached classification.
- `sa21-comparison.json`: all 22 counterpart outcomes, normalization patterns, and preserved traceback depths.

Two conservative verifier assumptions were corrected during this audit: this pytest JUnit output omits the optional failure type attribute, so assertion kind is verified from its explicit message/body; native-version traceback depths differ for SAVEPOINT arms, so that incidental difference is recorded rather than equated to a new assertion mechanism. Both initial verifier stops were data-only; no test or product action was retried. The final full verifier completed successfully.

## Continuation boundary

This accepts only the actual RED SA20 terminal evidence. Any proposed GREEN SA21 execution remains the coordinator's separate, gated decision under its reviewed exact command, current authorization, fresh destination checks, unchanged pins/preflights, and stop-for-audit requirements. This report starts no next cell and supplies no automatic GREEN execution authority.

The seven historical acceptance failures remain unchanged. The runner reports all seven production gates UNKNOWN. No fix, physical-quarantine, release, aggregate-suite, installed-package, or production claim follows.

Only `reviewer-notes/async-cleanup-red-sa20-independent-20261014` was written. No product/runtime imports, test collection/execution, database/server operations, network, remote actions, installation, or secret/environment access occurred.

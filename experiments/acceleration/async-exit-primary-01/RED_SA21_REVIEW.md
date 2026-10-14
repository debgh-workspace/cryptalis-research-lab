# Independent first RED SA2.1 terminal audit

Date: 2026-10-14 UTC.
Decision: **ACCEPT_EXPECTED_RED**, confined to the first ASYNC-EXIT-PRIMARY-01 RED SA2.1 cell.

The run reproduces the proposed primary-exception precedence defect and the separate root pending-only retained-preparation defect on the unchanged baseline runtime. This is acceptance of the intended failing experiment, not acceptance of a correction, GREEN clearance, production support, release qualification, or universal physical quarantine.

## Identity and terminal outcome

- Evidence: `evidence/next-correctness-red-sa21-20261014` and its sibling `-packet` directory.
- Frozen packet: `experiments/next-unblocked-correctness-20261014`.
- External PACKET SHA256 anchor: `6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a`.
- Exact first command SHA256: `8e9d48e071ac8d3de5cfe2ac61f615c5c4b11df5f45b1373db0bcbd6561ca9f9`. The captured command byte-matches the prior independently reviewed first RED SA2.1 command.
- Exactly 22 unique selected nodes agree in the packet node list, exact command, sanitized runner arguments, progress start order and JUnit order.
- 13 failed, 9 passed in pytest's 2.50 seconds. Runner elapsed time is separately reported as 2.810428992001107 seconds. These are different timing boundaries, not a discrepancy.
- JUnit reports 22 tests, 13 failures, zero errors and zero skips. The 88 progress records contain 22 starts plus 22 each setup, call and teardown reports. All setups and teardowns pass; call outcomes are exactly 13 failed and 9 passed.
- Wrapper and runner exit 1. Outer shell exit 0 is expected because the reviewed command records the wrapper result and finishes with successful pin commands. It must not be reported as a passing test result.
- Safe outer capture reports start 0, readiness 0, package-origin 0, tests 1 and stop 0. The safe shutdown log ends with `server stopped`. No tests, imports, database status calls or server commands were performed by this audit.

## Exact failure classification

All twelve protected double-failure nodes fail at `tests/test_sqlalchemy_async_exit_double_failure.py:195`, on `caught.value is captured_primary[0]`. Each observed escaping exception is the injected cleanup RuntimeError. The required captured primary is:

1. `test_async_preparation_exit_double_failure_preserves_primary_policy[provider-root-attached]`: sanitized KeyUnavailable.
2. `test_async_preparation_exit_double_failure_preserves_primary_policy[provider-savepoint-attached]`: sanitized KeyUnavailable.
3. `test_async_preparation_exit_double_failure_preserves_primary_policy[cancel-root-attached]`: CancelledError.
4. `test_async_preparation_exit_double_failure_preserves_primary_policy[cancel-savepoint-attached]`: CancelledError.
5. `test_async_exit_invalidation_failure_is_reported_without_replacing_primary[root]`: sanitized KeyUnavailable.
6. `test_async_exit_invalidation_failure_is_reported_without_replacing_primary[savepoint]`: sanitized KeyUnavailable.
7. `test_actual_task_cancellation_survives_exit_cleanup_failure[root]`: CancelledError captured after the suspended-provider cancellation path.
8. `test_actual_task_cancellation_survives_exit_cleanup_failure[savepoint]`: CancelledError captured after the suspended-provider cancellation path.
9. `test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_override-root]`: NoteOverrideCancellation.
10. `test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_override-savepoint]`: NoteOverrideCancellation.
11. `test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_unavailable-root]`: CancelledError.
12. `test_exception_note_failure_cannot_replace_primary_or_skip_cleanup[note_unavailable-savepoint]`: CancelledError.

For these twelve nodes, the preceding assertions establish one captured primary, one intended root/SAVEPOINT rollback callback, and one provider unwrap. The real-task arms reached provider suspension and `task.cancel()` before capturing the replacement error. The assertion requiring `task.cancelled()` was not reached.

The thirteenth failure is `test_pending_only_preparation_failure_clears_prior_material_without_sql[root]`, at line 334, on `_prepared is None`. The failure shows retained PreparedKeys. The earlier checks established prior prepared material, one provider unwrap and no SQL after the installed observation hook. Later transaction-state, nested-state, pending-state, cleanup-note and effects assertions were not reached.

This classification is verified against each JUnit failure body and the full safe test log, not inferred solely from failure counts or test names. `node-audit.json` retains the exact node-level classification.

## Assertions that remain unproved by RED

The twelve double-failure tests stop before line 196. Their following checks are not counted as passed: invalidation attempts, preserved metadata, exact primary type and local effects/retryability, real-task cancellation state, cleanup/quarantine notes, exception-note override behavior, unavailable-note handling, sanitized traceback output, retained-preparation clearing, transaction/pool state, independent row-lock/data observations, and later checkout/commit nonpublication.

In particular, the two tests named for failed invalidation do not establish that the injected invalidation failure was reached. The four note-path tests do not establish the correction's note-handling behavior. The later protected pre-rescue oracles are still unexecuted in this RED cell. Laboratory cleanup in `finally` is not substituted for those oracles.

## Nine passing controls and their limits

- Four native async controls pass: provider/cancel crossed with root/SAVEPOINT. They establish native secondary-error precedence for their explicit pre-commit primary and one-shot public callback fault. They then use explicit laboratory invalidation before their successful fresh-checkout/commit and stored-value/row-lock observations. They do not establish pre-rescue effects equality with a protected adapter.
- The protected pending-only SAVEPOINT control passes the full selected body: retained material clears; the observed path performs no SQL; an outer transaction remains valid; no nested transaction or pending new objects remain; no cleanup-failure note is present; local effects are `none`.
- Four synchronous body-error controls pass: native/protected crossed with root/SAVEPOINT. They preserve the existing secondary-error precedence and absence of added notes. Their cleanup completes. They are not full asynchronous regression or physical-quarantine qualification.

## Cleanup and evidence hygiene

The full safe test log, JUnit and outer log contain no bounded-laboratory-cleanup failure note, wrapper timeout, runtime/SQLAlchemy/unraisable/thread warning, or warnings summary. No setup, teardown, collection, skip or unexpected failure appears. The intentional assertion failures carry ordinary AssertionError primaries, so bounded helper cleanup failures would be visible as the helper's fixed notes; passing async cleanup would instead fail the node if its helper detected a failure.

The safe origin record identifies the RED candidate's `src/cryptalis/__init__.py`, with the expected RED source directory and `verified: true`. This is a separate-process origin check, not continuous attestation of every import. The runner scope remains isolated authorized research. Its fresh dual-role preflight reports both roles passed with the same two safe digest prefixes as the wrapper readiness log.

All selected filenames were validated before reading or hashing their listed payloads. No raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, `postgres-stop.json`, environment or secret files were read, hashed or copied. Source files were parsed only as text or hashed as data. Existing pinned interpreter symlinks were hash-checked without executing them; all resolve to the same previously reviewed Python 3.12 binary. Generated cache files were identified by filenames only and not read or hashed.

## Source, pins and corpus preservation

The independent data-only audit verifies:

- All 672 INPUTS, 18 PACKET and 14 native-source pins match current bytes. Every before/after pin log contains exactly its expected listed path set and successful entries.
- The entire 19-file packet copy byte-matches the frozen packet, including PACKET.sha256 itself. Both captured copy-diff logs are empty, and coordinator statuses are zero.
- Baseline/RED/GREEN manifests equal their respective 216/217/217 source pin listings. Current source bytes match all listings.
- Every one of the baseline's 216 source files is unchanged in RED. The sole added source file is the new 379-line test. The preserved baseline runtime copy also matches RED.
- GREEN remains a source-only candidate for this audit: relative to RED, only `src/cryptalis/sqlalchemy.py` differs; the new test is byte-identical. This observation is not execution permission.
- RED has 29 generated pytest/bytecode cache filenames beyond its 217 manifest paths. Baseline has 170 existing cache-only extras; GREEN has none. There are no extra non-cache source paths or missing manifest paths.
- The runtime before/after snapshot contains 156 identical entries. The source-repository evidence copy contains exactly those 156 paths and byte-matches their RED hashes. All 155 runner source/test entries match RED. The external-source snapshot is empty and unchanged; it is not claimed to provide broader dependency attestation.
- The corpus manifest has exactly 26 authorized corpus filenames. Every current corpus file and its durable pre-run copy matches its manifest hash. Current matching filenames equal the complete pre-run set. The wrapper isolation report records restoration true, no errors and no archived/deleted entries; the candidate corpus directory is empty. No corpus drift or new corpus file remains.

The safe parsing and independent hash checks are retained in `audit_evidence.py`, `audit-checks.txt`, `pin-name-validation.txt`, `node-audit.json` and `audit-summary.json` within this review directory.

## Continuation boundary

This result closes only the terminal audit of the first RED SA2.1 experiment. A source-cleared RED SA2.0 candidate may be considered next, but its exact command must be separately reviewed before the coordinator executes it. Neither RED SA2.0 nor either GREEN cell is automatically authorized or qualified by this result.

The seven historical acceptance failures remain unchanged. All seven production gates remain UNKNOWN. No correction, physical-quarantine, release, aggregate-suite, installed-package or production claim follows.

The reviewer made only filesystem reads, standard-library parsing and hash comparisons, and wrote only this owned review directory. No product/runtime import, test, database, network, remote, installation, credential or raw-phase-JSON action was performed.

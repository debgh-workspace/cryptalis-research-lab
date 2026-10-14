# Independent GREEN SA21 terminal audit: ASYNC-EXIT-PRIMARY-01

Date: 2026-10-14 UTC. Decision: **ACCEPT_BOUNDED_GREEN**, confined to the completed GREEN SA21 cell and its frozen candidate.

All **46 exact selected cases passed in 4.43 seconds**, including the 22 new cases and 24 retained regressions. Every selected setup, call, and teardown passed. The prior 13 RED SA21 failures now pass and its nine passing controls remain passing. There is no unexpected failure, skip, collection error, observed cleanup warning, timeout, pin drift, or corpus-restoration error. PostgreSQL shutdown is explicitly recorded as exit 0, and the stop log ends with `server stopped`.

This is bounded research-candidate evidence. It does not establish general physical quarantine, a broken-transport guarantee, installed-package qualification, full-suite admission, release approval, or production support. The seven historical acceptance failures remain unchanged; all seven production gates remain UNKNOWN. No next cell was executed by this reviewer.

## Identity and exact results

- Evidence: `evidence/next-correctness-green-sa21-20261014` and its `-packet` sibling.
- Frozen proposal: `experiments/next-unblocked-correctness-20261014`.
- Candidate: `candidate-next-unblocked-correctness-20261014`.
- External PACKET SHA256 anchor: `6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a`.
- Exact command SHA256: `4b18107da668c6ca1345fab3ed75cb7711ca91e2ae29f48122c0469fc2819818`.
- Captured coordinator driver SHA256: `717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f`.

The captured command byte-matches both the independent command-review copy and the single GREEN SA21 BEGIN/END block in the anchored packet. The captured driver byte-matches the reviewed driver. The coordinator status records exactly GREEN/SA21, one outer shell argv, all six before/after checks at exit 0, outer exit 0, and wrapper exit 0. This audit does not substitute those aggregate exits for the phase-specific checks.

Literal AST expansion of the frozen test decorators yields the exact 22 new and 24 retained node IDs, with no overlap or duplicate. Those 46 IDs match the packet lists, command selectors, runner arguments, progress start order, and JUnit order. The 184 progress entries comprise 46 starts and 138 reports: exactly one passing setup, call, and teardown for each node. JUnit has 46 tests, zero failures, zero errors, and zero skipped. `node-audit.json` lists each full ID and its phases; the first 22 also record their RED SA21 counterpart outcome.

The module distribution is:

- `test_sqlalchemy_async_exit_double_failure.py`: 22 passed.
- `test_sqlalchemy_async_cleanup.py`: 10 passed.
- `test_sqlalchemy_savepoint_faults.py`: 6 passed.
- `test_sqlalchemy_savepoints.py`: 2 passed.
- `test_sqlalchemy_flush_preparation_failure.py`: 6 passed.

The 4.43-second pytest result and 4.763212235993706-second runner receipt measure different boundaries. Neither is used as a performance conclusion.

## What the 22 new passing cases establish

The unchanged, pinned 379-line test was read directly. Its protected path uses a genuinely cold Keyring and observes the actual exception leaving `Keyring.prepare_async`, rather than substituting only the adapter's `_prepare` method.

### Twelve protected double-failure cases

These cover root/SAVEPOINT variants of provider error, injected cancellation, separately initiated real task cancellation, custom `add_note` override, unavailable note storage, and failed public invalidation.

All twelve reach and pass the previously blocked assertions at lines 191-221:

- Exactly one captured primary, one intended rollback callback, and one provider unwrap.
- The escaping exception is the exact primary object observed at the Keyring boundary.
- Exactly one public invalidation attempt in the failed-cleanup path.
- Original `operation_id`, `code`, and `stage` values are preserved.
- For the four provider-error cases, the escaping object is exactly `KeyUnavailable`, is a new sanitized object rather than the injected provider object, has local effects `unknown`, and has retryability false.
- The cancellation cases remain `CancelledError` instances. The two real-task cases suspend in the provider, receive `task.cancel()`, and establish `task.cancelled()` afterward.
- Fixed cleanup notes are exact. Failed-invalidation cases also retain the fixed quarantine-failure note. The custom note hook is never invoked. For the two unavailable-note-storage cases, the original tuple storage remains unchanged; these cases make no claim of delivered notes.
- Formatted exception output contains none of the three synthetic private cleanup/quarantine/note markers.
- Retained preparation material is cleared: `_prepared is None`.

The two failed-public-invalidation cases establish that the injection is actually reached and the original primary still escapes; they then perform explicit lab rescue. They do not establish data/lock release before rescue.

### Ten protected pre-rescue observations

The other ten protected double-failure cases pass lines 241-255 before any test-driven invalidate, close, or fixture disposal. Hooks/provider fixtures have been restored, but no rescue action is taken before these assertions:

- Neither root nor nested transaction remains active.
- Pool checked-out count is zero.
- An independent owner connection obtains the row lock with a 100 ms lock timeout and sees rank 1.
- A fresh checkout sees rank 1 and name `before`, sees only the original row, and commits.
- A later independent row-lock observation still sees rank 1.

The nested cases first flush an outer-prefix row before entering the failing nested unit (lines 155-168). The `[1]` whole-table observation after failure proves the selected failed unit and preflushed outer prefix were not published. These data and lock assertions are stronger than merely observing an invalidate call or transaction flags.

They remain bounded observations of one-shot public callback failures before the selected rollback SQL/driver call. They do not prove physical connection destruction or comprehensive transport-failure behavior.

### Ten remaining new controls

- Four native async root/SAVEPOINT provider/cancel arms preserve native secondary cleanup-error precedence. They explicitly invalidate before their successful fresh-checkout/commit, data, and lock checks. They do not establish pre-rescue effects parity with the protected arms.
- Two pending-only protected root/SAVEPOINT cases establish prior material before the attempt, one provider call, no observed SQL, cleared prior material, discarded pending-new state, no nested transaction, no cleanup-failure note, and local effects `none`. The SAVEPOINT case preserves its valid outer transaction after successful cleanup; the root case has none (lines 318-339).
- Four sync body-error native/protected root/SAVEPOINT cases preserve native secondary-error precedence and add no notes. Their scope is related sync/body behavior, not the new async pre-exit failure policy.

## Retained regression coverage and limits

All four selected regression source files are byte-identical to the baseline and RED candidate. All 24 selected cases pass:

- Ten root async body/exit error and real-cancellation cases retain transaction-state, pool, stored-value, and pre-close row-lock observations.
- Six nested cleanup/cancellation cases retain successful inner rollback, continued valid outer work where required, nonpublication, and pool reuse.
- Two failed SAVEPOINT control cases require a later commit to reject the failed unit and ultimately observe an empty table. They preserve whole-unit nonpublication for their separate failure policy; the real-backend-termination functions elsewhere in that module were not selected.
- Four failed-flush preparation rollback cases check `connection.invalidated` and no persisted work at the earlier failed-flush boundary. Two failed-invalidation cases check that the retained DBAPI adapter is closed and that private diagnostics are absent; explicit lab bookkeeping precedes their subsequent database observation. These older boundary-specific physical-handle assertions must not be transferred to the new context-exit policy.

## Runtime and native-source limits

The GREEN runtime differs from RED only in `src/cryptalis/sqlalchemy.py`. It clears retained material before native exit, preserves the preparation primary on a second failure, marks typed failure effects unknown/nonretryable, attempts best-effort public invalidation, and uses fixed notes with `BaseException.add_note`. The failure path suppresses display chaining with `raise failure from None`; it does not erase all in-memory exception context/cause references.

Pinned SA2.1 native source confirms that async transaction exit delegates to sync transaction exit, and public async invalidate delegates to public sync Session invalidation. Native rollback records a rollback error, restores state, closes the transaction, then re-raises. Root close removes Session ownership before a later invalidate call. Consequently, that later public call can return without acting on the earlier physical connection. Zero checked-out connections and successful invalidation alone do not prove physical quarantine. Ordinary pool reset is a plausible release route for this callback fault; this run does not identify it as a universal mechanism.

The new helper bounds pending-task completion and final invalidate/close/dispose awaits to five seconds each. The owner begin listener keeps 1-second lock and 5-second statement limits through fixture teardown. These are not universal per-operation bounds: the main task await, explicit native/failed-invalidation rescue, synchronous cleanup, and older regression teardown have no individual five-second wrapper; asyncio timeouts depend on cancellation cooperation. Repeated cancellation, hostile drivers, arbitrary host event behavior, and diagnostic transport across process boundaries remain unqualified.

## Capture, source, corpus, and shutdown integrity

The data-only verifier confirms:

- All 672 INPUTS, 18 PACKET, 14 native-source, 216 baseline, 217 RED, and 217 GREEN source pins match current bytes.
- Both before/after pin logs have exactly the expected filename sets and order, all successful. Both copy-diff logs are empty.
- All 19 packet-copy files, including PACKET.sha256 itself, byte-match the anchored packet, with complete equal filename sets.
- RED retains every baseline source byte and adds only the new test. GREEN retains the same new test and changes only the runtime file specified above.
- Candidate extra files are cache-only: 170 baseline, 29 RED, and 33 GREEN at audit time. These were identified by filename and never read or hashed.
- All 156 runtime before/after snapshot entries are identical, and all copied evidence-source bytes match GREEN. All 155 runner source/test hashes match GREEN. The external-source snapshot is empty and unchanged, which is not a broader dependency attestation.
- The source-root receipt identifies GREEN. The safe outer origin record identifies its expected `src/cryptalis/__init__.py` and source directory with `verified: true`. This separate-process origin check is not continuous attestation of every import.
- Readiness, test log, and runner receipt agree on successful fresh two-role preflight with digest prefixes `76053d5b` and `a38ab71b`.
- All 26 pre-run corpus files and durable prior copies match their recorded hashes. The complete current matching filename set is restored. One candidate SA2.1.3 flush corpus is archived with its matching hash and empty `results` list; no deleted entries or restoration errors exist. That empty-results file is a module-fixture artifact, not missing selected pytest results or extra compatibility coverage.
- Safe outer records separately report start, readiness, package-origin, tests, and stop each at exit 0 exactly once. The safe stop log ends `server stopped`.

The safe test log, JUnit, and outer log contain no bounded-laboratory-cleanup failure note, wrapper timeout, RuntimeWarning, SAWarning, unraisable/thread warning, or warnings summary. Passing teardown and the absence of those signals support successful cleanup for this cell; they do not broaden the native or rescue-arm oracles.

## Audit method, incidents, and continuation boundary

The prior RED SA20 terminal audit and remaining-command source review were read. This review used only standard-library text/AST/XML/JSON parsing, filename validation, and SHA256 comparisons. Manifest-selected filenames were validated against safe roots/classes before any selected payload was read or hashed. Interpreter links were hash-checked only against the previously reviewed Python 3.12 target, never executed.

No raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, or `postgres-stop.json` was read, hashed, or copied. No environment values, credentials, or secret files were accessed. No product/native/wrapper imports, pytest collection, tests, database/server operations, network/remote actions, installs, or next-cell execution occurred.

Two conservative verifier assumptions stopped the data-only checker and were corrected: the command header includes a colon and description, and the source snapshot includes the already pinned `uv.lock` alongside source/tests/configuration. Neither incident involved a failed test retry, product action, denied access, or changes outside this review directory. The final complete verifier succeeded.

Artifacts: `audit_evidence.py`, `audit-checks.txt`, `audit-summary.json`, `pin-name-validation.txt`, and `node-audit.json`.

Only `reviewer-notes/async-cleanup-green-sa21-independent-20261014` was written. Acceptance applies only to the completed GREEN SA21 cell. Any GREEN SA20 continuation remains the coordinator's separate gated decision, requiring current authorization, the exact reviewed command, fresh destinations, unchanged pins/preflights, exclusive lab ownership, corpus preservation, and its own terminal audit. This report gives no automatic execution authority or stronger qualification.

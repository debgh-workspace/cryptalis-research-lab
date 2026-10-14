# Independent GREEN SA20 terminal audit: ASYNC-EXIT-PRIMARY-01

Date: 2026-10-14 UTC. Decision: **ACCEPT_BOUNDED_GREEN**, confined to the completed GREEN SA20 cell and frozen research candidate.

All **46 exact selected cases passed in 4.55 seconds**, with all **138 setup/call/teardown phases passing**. The exact 13 prior RED SA20 failures now pass; its nine passing controls remain passing; all 24 retained regressions pass. No selected case is missing, duplicated, skipped, or extra. No failure, error, selected cleanup warning, timeout signal, source/pin drift, or corpus-restoration error was found. Wrapper and outer exits are 0. The separately captured server-stop exit is 0 and the safe stop log ends with `server stopped`.

This is bounded candidate evidence. It does not establish universal physical quarantine, broken-transport handling, installed-package qualification, full-suite admission, release approval, or production support. The seven historical acceptance failures remain outside this cell and unchanged in disposition. All seven production gates remain UNKNOWN. The reviewer ran no test, product code, database/server action, or subsequent cell.

## Evidence identity and exact reconciliation

- Evidence: `evidence/next-correctness-green-sa20-20261014` and its `-packet` sibling.
- Frozen proposal: `experiments/next-unblocked-correctness-20261014`.
- Candidate: `candidate-next-unblocked-correctness-20261014`.
- External PACKET SHA256 anchor: `6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a`.
- Exact GREEN SA20 command SHA256: `f5f9de68128cc5f6e142bda7222dbd7ab89c86e9ec769d9d4216dc572ac31712`.
- Captured coordinator driver SHA256: `717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f`.

The command is byte-identical to the independently reviewed GREEN SA20 command and the one GREEN SA20 BEGIN/END block in the anchored packet. It selects the pinned SA20 interpreter, GREEN candidate/configuration, fresh cell evidence destination, unchanged corpus-v2 wrapper, and 46 explicit selectors. The driver byte-matches its reviewed copy. Coordinator status records GREEN/SA20, exactly one outer shell argv, all six before/after checks at 0, wrapper exit 0, and outer exit 0. Aggregate shell success was not substituted for phase or stop verification.

Literal AST expansion of source decorators independently yields the 22 new IDs plus 24 retained IDs, with no overlap. Those 46 ordered IDs match the frozen lists, command selectors, runner arguments, progress start order, and JUnit order. Progress contains exactly 184 records: 46 starts and 138 phase reports, one passing setup, call, and teardown per ID. JUnit records 46 tests, zero failures, zero errors, and zero skipped. `node-audit.json` records every full ID and phase result, plus the RED SA20 counterpart outcome for the 22 new cases.

The module distribution is 22 new double-failure tests, 10 async-cleanup regressions, six SAVEPOINT-fault regressions, two failed-SAVEPOINT-control regressions, and six failed-flush-preparation regressions. The runner elapsed time is 4.8888780230190605 seconds; it measures a different boundary from pytest's 4.55 seconds. Neither is a performance claim.

Direct comparison with GREEN SA21 confirms the same 46 ordered IDs, all 138 passing phase outcomes, the same 156 source-snapshot hashes, and the same 26 prior-corpus hashes. The SA21 audit was read as prerequisite context; this SA20 decision was established from SA20 evidence rather than inherited from that decision.

## Exact RED-to-GREEN result

The 13 former failures are independently classified by full ID and matched against RED SA20 JUnit:

- Four protected provider/injected-cancellation root/SAVEPOINT double-failure arms.
- Two protected public-invalidation-failure root/SAVEPOINT arms.
- Two separately initiated real-task-cancellation root/SAVEPOINT arms.
- Four custom-note-hook/unavailable-note-storage root/SAVEPOINT arms.
- The pending-only protected root arm.

The first twelve previously stopped at primary-object identity, line 195. They now pass that assertion and their later applicable oracles. The pending-only root arm previously stopped at retained-material clearing, line 334; it now passes the whole test.

The nine retained new-test controls are four native async arms, the pending-only protected SAVEPOINT arm, and four sync body-error arms. All nine still pass. The 24 additional pre-existing regression IDs are distinct from these controls and all pass.

## Primary, cancellation, note, and effects observations

The frozen 379-line new test and changed runtime were read directly. The protected path uses a cold public Keyring and observes the actual exception leaving `Keyring.prepare_async`; it does not merely substitute the adapter's `_prepare` method.

The twelve protected double-failure arms establish one captured primary, one intended rollback callback, one provider unwrap, exact identity of the escaping primary, exactly one attempted public invalidation, and preservation of the captured `(operation_id, code, stage)` tuple (`test_sqlalchemy_async_exit_double_failure.py:191-221`).

For the four provider-error cases, the object is exactly `KeyUnavailable`, distinct from the injected provider object, with local effects `unknown` and retryability false. Injected cancellation remains a `CancelledError`. The two separate real-task cases wait until the provider is suspended, call `task.cancel()`, await that task, and establish `task.cancelled()` afterward (`:129-135,180-207`). These are separate observations; injected cancellation alone would not prove task cancellation state.

The exact fixed cleanup note is checked where note storage is available. Both deliberately failed-invalidation arms also check the fixed quarantine-failure note. Custom `add_note` dispatch is not invoked. In the two unavailable-note-storage arms, the original tuple remains unchanged; no note-delivery claim is made. Formatted exception output excludes all three synthetic private cleanup/quarantine/note markers. Every protected double-failure arm clears retained `_prepared` material.

Runtime scope remains `_AsyncTransaction.__aexit__` during preparation failure after a normal body (`src/cryptalis/sqlalchemy.py:1058-1103`). It clears prior material before native cleanup, preserves the preparation primary if cleanup also fails, marks typed failure effects unknown/nonretryable, attempts public invalidation, uses guarded direct `BaseException.add_note`, and suppresses display chaining with `raise failure from None`. It does not erase all in-memory cause/context references, retain a raw connection after ownership changes, or change ordinary body-error/native-success behavior. Cross-process transport of these local effects/notes remains unqualified.

## Pre-rescue observations and their limits

For ten protected double-failure arms, lines 241-255 execute before any test-driven invalidate, close, or fixture disposal. Fault hooks and provider fixtures are restored, but there is no laboratory rescue before these observations:

- No active root or nested transaction.
- Pool checked-out count zero.
- An independent owner connection obtains the row lock under a 100 ms lock timeout and observes rank 1.
- A fresh checkout observes rank 1 and name `before`, sees the whole rank list `[1]`, and commits.
- A later independent row-lock observation again sees rank 1.

The nested setup explicitly flushes an outer-prefix row before the failing nested unit (`:155-168`). Whole-table `[1]` proves nonpublication of that prefix as well as the failed inner edit in this experiment. Stored-value and independent lock observations are stronger than a successful invalidate call or transaction flags alone.

The two deliberately failed-public-invalidation arms instead establish that the injected invalidation failure was reached while primary identity and safe notes survive. They explicitly invalidate after removing the fault, before later database observations (`:237-240`). They do not establish pre-rescue data/lock release. The four native async arms also explicitly rescue before fresh-checkout/commit and lock observations; their passing secondary-cleanup-error precedence does not establish effects parity with the protected arms.

All these new faults are one-shot public callbacks before the selected rollback SQL/driver call. They are not broken-transport simulations. The pinned SA2.0.51 native source shows async transaction exit and invalidation delegating to sync public behavior (`ext/asyncio/session.py:1047-1052,1885-1888`). Rollback captures an error, restores state, closes the transaction, then re-raises (`orm/session.py:1344-1398`). Root close removes Session ownership before a later public invalidate can inspect it (`:1408-1424,2592-2598`). Therefore, that later call can succeed without acting on the earlier physical connection. This cell does not prove physical destruction or a universal quarantine mechanism; ordinary pool cleanup remains a possible release route.

Two pending-only cases independently establish prior material, one provider call, no observed SQL, cleared material, no pending-new state, no nested transaction, no cleanup-failure note, and effects `none`. The valid outer transaction remains only for the SAVEPOINT arm (`:318-339`). Four sync body-error controls retain native secondary-error precedence with no added notes (`:351-379`).

## Retained regressions

All four selected source files are byte-identical to baseline and RED. Direct source review confirms their existing oracles remain intact:

- Ten root async body/exit and real-cancellation cases preserve state, pool, stored-value, and independent row-lock observations before Session close; applicable cases also reuse the surviving Session.
- Six nested failure/cancellation cases preserve successful inner rollback, permitted outer continuation, nonpublication, and pool reuse.
- Two failed-SAVEPOINT-control cases require a later commit to reject the failed unit and ultimately observe an empty table, preserving the separate whole-unit nonpublication policy. The actual backend-termination tests elsewhere in that module were not selected.
- Four failed-flush-preparation rollback cases assert `connection.invalidated`, sanitized output, and no persisted work at the earlier failed-flush boundary. Two failed-invalidation cases assert that the retained DBAPI adapter is closed and private details are absent; explicit laboratory bookkeeping precedes their later database observation. Those boundary-specific physical-handle assertions must not be transferred to the new context-exit policy.

The new final cleanup helper bounds unfinished-task completion and each final invalidate/close/dispose await to five seconds. The owner transaction listener retains 1-second lock and 5-second statement limits through fixture teardown. These are not universal per-operation guarantees: the main task await, explicit native/failed-invalidation rescue, sync cleanup, and older regression teardown have no individual five-second wrapper, and asyncio timeouts require cancellation cooperation. Repeated cancellation, hostile drivers, and arbitrary host-event behavior remain unqualified. No bounded-laboratory-cleanup failure note or selected warning/timeout signal appears in test log, JUnit, or outer log; all teardown phases pass.

## Source, packet, corpus, and shutdown integrity

The data-only checker validates selected manifest filenames and symlink targets before reading/hashing listed payloads, then verifies:

- All 672 INPUTS, 18 PACKET, 14 native-source, 216 baseline-source, 217 RED-source, and 217 GREEN-source entries match current bytes.
- Both before/after pin logs contain exactly the expected paths in order, all successful. Both packet-copy diff logs are empty.
- All 19 copied packet files, including PACKET.sha256 itself, have equal complete filename sets and byte-identical contents.
- RED retains all 216 baseline files and adds only the new test. GREEN retains that same test and differs from RED only in `src/cryptalis/sqlalchemy.py`.
- No source path is missing and no non-cache extra file appears. The 170/29/33 baseline/RED/GREEN extra filenames are cache-only and were never read or hashed.
- All 156 runtime before/after source entries are identical; evidence source copies match those exact paths and GREEN hashes. All 155 runner source/test hashes agree. External snapshots are empty and unchanged, not broader dependency attestation.
- Source-root receipt identifies GREEN. Safe package-origin log and its outer-log record identify the expected candidate `src/cryptalis/__init__.py` with verified true. This is a separate-process check, not continuous attestation of every import.
- Readiness log, test log, and runner receipt agree on successful fresh two-role preflight and digest prefixes `76053d5b` and `a38ab71b`.
- Every one of the 26 pre-run corpus files and durable backups matches its recorded hash. Current matching filename set exactly equals the pre-run set. The isolated candidate SA2.0.51 flush-corpus file is archived with the recorded hash and an empty `results` list. There are no deletion entries or restoration errors. The empty module-fixture artifact does not replace or add selected test results or compatibility coverage.
- Safe outer records separately report start, readiness, package-origin, tests, and stop at exit 0 exactly once. The stop log explicitly records `server stopped`; `coordinator-wrapper-exit.txt` is 0.

## Method, artifacts, and stopping boundary

The earlier RED SA20 and GREEN SA21 terminal reviews and the remaining-command review were read. The data checker was adapted from the reviewed SA21 checker, reviewed for this cell, and extended to classify exact RED SA20 failures, verify safe readiness/origin logs, and compare all GREEN SA21 counterpart IDs/phases/source/corpus hashes. Its complete first execution succeeded. Only standard-library data parsing, literal AST analysis, and hashing were executed; no reviewed module was imported or run.

No raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, or `postgres-stop.json` was read, hashed, or copied. No credentials, secret files, or environment values were accessed. Existing pinned interpreter links were hash-checked against their previously reviewed Python 3.12 target, never executed. There were no denied actions, product retries, pytest collection/execution, database/server operations, network actions, installs, or next execution.

Artifacts: `review.md`, `audit_evidence.py`, `audit-checks.txt`, `audit-summary.json`, `pin-name-validation.txt`, `node-audit.json`, and `sa21-comparison.json`.

Only `reviewer-notes/async-cleanup-green-sa20-independent-20261014` was written. This accepts the completed GREEN SA20 cell and provides no automatic authority for another experiment, integration, release, or qualification step. The lab remains stopped at this cell's recorded terminal boundary.

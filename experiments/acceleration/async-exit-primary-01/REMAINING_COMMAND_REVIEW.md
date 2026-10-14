# ASYNC-EXIT-PRIMARY-01: remaining command source review

Date: 2026-10-14 UTC. Result: **CLEAR_SOURCE_COMMAND_CONDITIONAL** for each exact block below. This is source clearance to conduct a bounded experiment after its prerequisite audit. It is not a runtime result, automatic progression authority, installed-package qualification, physical-quarantine qualification, or production admission.

## Per-block decision and stopping conditions

- **RED SA20**, `ROOT_COMMANDS.txt:54-99`: conditionally clear for its 22 exact nodes with the pinned SA2.0 interpreter and RED tree. Requires independent acceptance of the actual RED SA21 terminal evidence first. The coordinator reported that acceptance at 22:44 UTC: 13 intended failures, 9 passes, stable pins/source/corpus, stop exit 0, and no cleanup issues. This reviewer did not inspect that run's evidence. Run once and STOP for its own independent terminal audit.
- **GREEN SA21**, `ROOT_COMMANDS.txt:102-171`: conditionally clear for its 46 exact nodes with the pinned SA2.1 interpreter and GREEN tree. Requires accepted RED SA20 terminal evidence, including intended failure identities and no unexpected failures or cleanup problems. Run once and STOP for its own independent terminal audit.
- **GREEN SA20**, `ROOT_COMMANDS.txt:174-243`: conditionally clear for its 46 exact nodes with the pinned SA2.0 interpreter and GREEN tree. Requires accepted GREEN SA21 terminal evidence. Run once and STOP for its own independent terminal audit.

All three decisions require unchanged external packet identity, current successful pre/post pin checks, fresh evidence and companion packet destinations, unchanged wrapper/preflights, exclusive lab ownership, verified package origin, and preserved corpus receipts. Any mismatch, missing observation, collection error, timeout, unexpected outcome, cleanup warning, unstable input, stop failure, or failed restoration means HOLD for diagnosis. A previous cell's acceptable test counts alone are insufficient. Do not execute the full command file. No automatic retry, alternate database, cluster repair, credential substitution, or stronger-oracle weakening follows from this review.

The shell STOP markers are comments, not enforced inter-block gates. The coordinator must enforce those gates. Every GREEN acceptance needs all 46 exact calls plus clean setup/teardown; no skipped, extra, duplicate, or missing node is equivalent to that result.

## Independently verified identity and selectors

- External `PACKET.sha256` anchor matches `6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a`.
- All filenames in all six pin lists were validated before any listed file was hashed. All 672 INPUTS, 18 PACKET, 14 native-source, 216 baseline, 217 RED, and 217 GREEN entries match their pins.
- The three exact existing interpreter symlinks resolve to `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`; hash-only verification of that authorized target matched the pin. None of those interpreters was executed.
- RED retains every baseline source byte and adds only the new test. GREEN changes only `src/cryptalis/sqlalchemy.py` and adds the byte-identical new test. Both candidate runners byte-match the pinned repository runner.
- AST-only expansion of the literal decorators independently yields all 22 new IDs in their declared order. Expansion of the selected functions in the four existing regression modules yields the 24 regression IDs in their declared order. The sets are unique and disjoint. No reviewed source was imported, compiled for execution, or collected by pytest.
- Both RED command blocks select exactly those 22 IDs. Both GREEN blocks select exactly their concatenation, 46 IDs. All selectors are explicit, correctly quoted absolute paths under the selected candidate root; the `-c` configuration matches that root.
- RED SA21 versus RED SA20, and GREEN SA21 versus GREEN SA20, become byte-identical after normalizing only headers, dependency-cell paths, and evidence destinations. With candidate roots also normalized, the RED-to-GREEN difference contains only the 24 regression selector lines.
- Bash syntax checks passed for all four extracted command copies. Those checks did not execute the blocks.
- The three remaining evidence directories were absent, including symlink checks. The three companion packet directories used by the optional coordinator driver were also absent. These are point-in-time observations; exclusive creation remains required at execution.
- Exactly 26 ordinary corpus filenames matched the wrapper's preservation patterns. This review inspected those filenames only; it did not read or hash corpus contents.

Supporting artifacts are `static-check-summary.txt`, `pin-name-validation.txt`, the six `*.verified.txt` files, the extracted command copies, source-expanded ID lists, selected-ID lists, and normalized differences. `static_review.py` is the independent standard-library text/AST/hash verifier, not a product or test runner.

## Version/API and source scope

Pinned native source reports SQLAlchemy 2.0.51 and 2.1.3. These are source observations, not a new runtime version attestation. In both versions, `AsyncSessionTransaction.__aexit__` greenlet-delegates to native sync transaction exit; `AsyncSession.invalidate` greenlet-delegates to the public sync Session operation. See SA2.0 `ext/asyncio/session.py:1047-1053,1885-1888` and SA2.1 `:1356-1362,2205-2208`.

Both native transaction-context implementations call rollback on exceptional exit and restore context in `finally`. Both SessionTransaction rollback implementations capture rollback failure, restore state, close the transaction, then re-raise that failure. The root close path removes Session ownership before the later public invalidate call. See SA2.0 `engine/util.py:130-167`, `orm/session.py:1344-1437,2592-2598`; SA2.1 `engine/util.py:127-164`, `orm/session.py:1358-1451,2705-2711`.

Consequently, public invalidate returning successfully after failed root exit may be a no-op for the previous physical connection. Transaction flags and zero checked-out connections are not sufficient evidence of rollback or physical closure. The root Connection cleanup also clears its transaction in `finally`; later ordinary pool return can call dialect rollback directly without the injected Connection rollback callback. This is a plausible release path for the bounded callback fault, not a transport-failure result.

The GREEN change remains confined to preparation failure during normal-body async context exit. It clears `_prepared` before native cleanup; if cleanup also fails, it preserves the original sanitized primary object, keeps its operation/code/stage, sets typed CryptoFailure effects to unknown and retryability to false, attempts public Session invalidation, and raises the primary with display chaining suppressed. It does not detach a connection, retain and close a driver after pool ownership changes, modify body-error/native success handling, or replace failed-flush/SAVEPOINT-control policies.

The fixed diagnostic notes use `BaseException.add_note` directly, bypassing a subclass override. A failure in that note channel is caught before public invalidation. The note-override and malformed-note-storage cases check original exception identity, absence of custom hook invocation, the invalidation attempt, and safe formatted output. They do not claim that an unavailable note was delivered. `raise ... from None` suppresses traceback display chaining; it does not erase every in-memory cause/context reference. Repeated cancellation, arbitrary host event behavior, and cross-process transport of new local diagnostic attributes/notes remain unqualified.

## Required stronger observations remain intact

The new tests observe the primary leaving the real cold Keyring preparation boundary; ordinary provider failure is normalized to a fresh KeyUnavailable, whereas injected cancellation retains identity. Separate real task cancellation cancels a suspended provider await and checks `task.cancelled()`.

The protected ordinary arms assert no active transaction/nested transaction, zero pool checkouts, the original stored value, and successful independent row-lock acquisition before test-driven invalidation/close/disposal. The nested setup includes preflushed outer-prefix work. Fresh checkout and commit must see only the original row. These assertions must remain unchanged even if a weaker primary-only fix could pass without them (`test_sqlalchemy_async_exit_double_failure.py:155-168,241-255`).

Native and deliberately failed-invalidation arms explicitly rescue before their later database observations (`:237-240`); they do not establish pre-rescue effects parity or physical quarantine. Pending-only cases verify no SQL, cleared prior material, discarded pending state, and preservation of a valid outer transaction after successful nested cleanup. Related sync body cases retain native secondary-error precedence.

The 24 unchanged regressions retain root/nested successful cleanup and real cancellation controls, pre-close row-lock observations, failed SAVEPOINT whole-unit nonpublication, and the earlier failed-flush rollback/invalidation boundary. In particular, selected SAVEPOINT failure tests preserve the existing requirement that the outer unit cannot commit a failed inner or outer prefix. They do not broaden the new context-exit claim into complete physical-quarantine coverage.

## Wrapper, preflights, isolation, and cleanup bounds

The unchanged corpus-v2 wrapper validates the candidate root and byte-identical runner, creates a fresh evidence directory, then obtains nonblocking exclusive `flock` before corpus snapshot or database action. It keeps that lock through stop and corpus restoration. Candidate PYTHONPATH and origin checks select the requested source tree; this separate-process check is not continuous attestation of every import.

The unchanged runner drops inherited test URL values, reloads both private files, and probes both roles freshly. The wrapper performs readiness first; the actual test invocation repeats the runner preflight and creates its in-process admission marker. A failed preflight stops before tests. The reviewer read runner source only and never read credentials or environment values.

The wrapper records before/after source snapshots, progress events, JUnit, sanitized logs, and the runner receipt. Its test subprocess is limited to 600 seconds; other subprocess phases have a 90-second bound. Shutdown runs in `finally`, then corpus-v2 captures changed receipts before restoring originals and checking no new matching files remain. Its explicit archive/restore error checks preserve a failed preservation result. The selected failed-flush module has an autouse corpus writer, so isolation is necessary even when its selected functions add no records.

Important limit: the wrapper does not promote the server-stop return code into its main return code. Independent terminal stop verification is mandatory. Likewise, the exact shell stores `wrapper_exit` and then runs postchecks; the shell can finish successfully after an expected RED or an unexpected nonzero wrapper result. Neither shell success nor driver success is acceptance.

The new final cleanup helper bounds pending task completion, Session invalidation, Session close, and Engine disposal to five seconds each, restores deliberate hooks before rescue, and records fixed cleanup-stage notes without replacing an existing failure. With no earlier failure, cleanup failure raises an assertion. The fixture-lifetime owner begin listener applies 1-second lock and 5-second statement limits through schema teardown, while the explicit lock oracle uses 100 ms.

Those five-second bounds are **not universal**: the main task await (`:186`), explicit native/failed-invalidation rescue invalidate (`:240`), synchronous cleanup (`:378-379`), and older regression teardown awaits have no individual five-second wrapper. They rely on cooperative behavior and the outer process bound. Async timeout itself requires cancellation cooperation. No hostile-driver, repeated-cancellation, arbitrary-event, or absolute per-operation liveness guarantee follows. Any timeout or cleanup note is unexpected and requires HOLD; never count it as an intended RED precedence failure.

## Optional coordinator-driver source review

The coordinator additionally requested source review of `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/run-async-exit-reviewed-block.py`. Conditional source clearance applies to SHA256 `717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f` only, after validating that exact file and resolved path before hashing.

The driver validates its two selector arguments, checks the external packet anchor, extracts one exact BEGIN/END block, creates a fresh companion directory, and copies the complete packet plus exact command and its own source. The current packet contains exactly its 18 listed members plus PACKET.sha256, all safe and nonsymlink. It checks the original anchor, full packet-copy equality, PACKET pins, and INPUTS pins before and after the single outer shell invocation. It captures full outer output, outer argv/exit, exact command hash, and the separate wrapper exit. Its loop does not invoke another RED/GREEN block.

Its final status file is written only if all prior checks reach completion. Intermediate assertion failure can leave the individual logs without `coordinator-status.json`; missing status is not acceptance. It does not itself enforce prior-cell terminal-audit decisions, and its process exit is not an automatic propagation of wrapper failure. The coordinator must interpret both exits and enforce the stopping conditions above. Freshness checks must still reject any newly introduced symlink or occupied destination. The driver was not executed by this reviewer.

## Review boundary and incidents

Read the first RED source/command review and original primary contract review before reviewing these remaining blocks. The earlier contract review's preliminary 16-case/no-outer-prefix draft description is superseded by the current frozen 22-case test source; the stronger frozen assertions are preserved here.

One conservative filename guard in the independent verifier stopped before any pinned content hashing because it omitted the known source file `experiments/manifest_setup_fastapi_models.py`. Filename inspection confirmed that sole experiment source entry; the guard was extended for that exact relative path and all validation then completed before hashing. No product command, denied access, or failed test was retried.

Only this reviewer-notes directory was written. No reviewed product/native/wrapper module was executed or imported; no pytest collection, tests, database calls, network/remote actions, installs, credential/environment reads, or raw phase JSON reads/hashes/copies were performed. The review did not inspect first RED terminal evidence. Physical quarantine remains UNKNOWN outside exact observed future assertions; seven historical acceptance failures and all seven production gates remain unchanged/UNKNOWN.

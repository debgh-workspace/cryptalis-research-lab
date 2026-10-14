# Independent source and first RED command review

Date: 2026-10-14 UTC. Decision: **CLEAR_SOURCE_AND_RED_COMMAND** for the exact first `RED SA21` block only. This is static experiment clearance, not a reproduced failure, runtime success, GREEN clearance, production admission or physical-quarantine qualification.

## Identity and completed static checks

- Packet SHA256: `6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a`.
- RED manifest SHA256: `592a2a0e4f386e8da188e10c3a5d530e675e16c6ec30d78505b66a27fd7a4c3d`.
- GREEN manifest SHA256: `4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649`.
- All pin filenames in all six SHA256 lists validated before reading any listed content for hashing. Verified 672 INPUTS, 18 PACKET entries, 14 native-source pins, and the 216/217/217 source listings. Hash-check outputs are retained in this review directory.
- RED and GREEN each contain exactly the 217 listed files, with no extra files at review time. RED retains every original S25 source byte and adds only `tests/test_sqlalchemy_async_exit_double_failure.py`. GREEN changes only `src/cryptalis/sqlalchemy.py` and adds the byte-identical new test. Original baseline runtime copy also matches RED.
- The original baseline directory additionally has 170 existing pytest/bytecode cache paths. These were identified by filenames only, not read or hashed. They are not part of its 216-file source manifest and are absent from the fresh RED/GREEN trees.
- Three existing interpreter symlinks resolve to `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`. An initial conservative path guard stopped before hashing this target; the coordinator explicitly authorized hash-only verification through those existing pinned symlinks. No interpreter was executed and no environment was substituted.
- Bash syntax checks passed. The extracted first RED command selects exactly the 22 unique entries in NEW_NODE_IDS.txt, in the same order. The packet also retains 24 existing regression nodes for separately reviewed later GREEN execution.
- All four proposed evidence directories were absent at the freshness check. Exactly 26 existing corpus filenames matched the corpus-v2 preservation patterns.

## Source and contract review

Read the complete 379-line new test, complete runtime delta, current surrounding adapter/native control flow, the approved primary contract review, and the owning failure rules in ENGINEERING_PLAYBOOK.md:32-48 and docs/security.md:307-341.

The adapter change remains confined to preparation failure on normal-body async transaction exit. It clears retained preparation before native cleanup, retains the exact primary exception, sets typed CryptoFailure effects to unknown and retryable to False after secondary cleanup failure, and supplies fixed discard/inspect notes. It attempts public Session invalidation and raises the primary from None. It does not detach a Connection, retain or close a raw driver after pool ownership changes, alter body-error exit handling, change native successful exit, or modify failed-flush/SAVEPOINT-control policies.

BaseException.add_note is called directly, bypassing a subclass override. Its own failure is caught before the public invalidation attempt. The test covers both an overriding cancellation exception and invalid builtin note storage; it checks primary identity, no custom output-hook invocation, the invalidation attempt, and absence of synthetic raw cleanup/quarantine/output text from formatted tracebacks. This preserves primary failure when note delivery fails without falsely claiming note delivery succeeded. Cross-process transport of the new local attributes/notes remains unqualified.

Protected preparation uses a cold real Keyring and observes the exception leaving its public preparation boundary. Ordinary provider exceptions are normalized to a fresh KeyUnavailable; the assertion correctly compares identity to the sanitized boundary exception, not the provider's original error. Injected cancellation retains its object. Separate suspended-provider cancellation uses task.cancel() and asserts task.cancelled(), rather than treating an injected exception as equivalent evidence.

The native comparison deliberately injects a primary before commit and observes the same public one-shot root/SAVEPOINT cleanup fault. Native secondary-error precedence follows the pinned native exit and safe_reraise control flow. Protected primary precedence is the independent Cryptalis diagnostic contract, not a false native exception-parity assertion. Native and deliberately failed-invalidation arms explicitly rescue before their later database observations, so they do not establish pre-rescue effects parity.

The protected ordinary arms require transaction/pool state and an independent stored-value plus bounded row-lock observation before test-driven invalidation, close or dispose. Nested setup includes flushed outer-prefix work; a fresh checkout/commit must observe only the previously committed original row. These are meaningful stronger oracles and must not be weakened merely because a primary-only fix could pass weaker assertions.

The successful-cleanup pending-only tests retain prior prepared material, force cold preparation failure, assert no SQL after the observation hook is installed, verify material clearing and pending-state removal, and preserve an otherwise valid outer unit for the nested case. Existing body-error behavior and retained cleanup regressions remain separate controls.

## Bounded cleanup and interpretation limits

The fixture-lifetime owner Engine begin listener applies lock_timeout=1s and statement_timeout=5s to inspection and schema teardown transactions; the explicit row-lock oracle uses 100ms. Intentional rollback hooks and provider/invalidation substitutions are restored before laboratory rescue. Async task, session invalidation, session close and engine disposal are each awaited with a 5-second bound. The cleanup helper records fixed stage names without replacing an already active test failure; if no prior failure exists, it raises its own cleanup assertion.

Those bounds cover the proposed cooperative callback-fault experiment. They are not a guarantee against a hostile driver, repeated cancellation or arbitrary host event extensions. The wrapper's process timeout and server shutdown remain necessary. An underlying fixture teardown or cleanup failure is a separate unexpected result and requires STOP; it must never be relabeled as an intended primary-precedence RED result. Inspect cleanup notes as well as test counts.

For the root callback, pinned native source provides a plausible release path: RootTransaction._close_impl clears Connection._transaction in finally (SA2.1 engine/base.py:2687-2707; equivalent SA2.0:2720-2740). SessionTransaction.close then calls Connection.close. With no active Connection transaction, that close uses ordinary pool close; rollback-on-return calls dialect.do_rollback directly, bypassing the Connection rollback event (SA2.1 engine/base.py:1260-1276; pool/base.py:1424-1471). This explains why the synthetic callback need not imply a real transport rollback failure. It is static rationale only. A successful later Session.invalidate can still be a no-op for a previously returned physical connection. Runtime lock/nonpublication evidence is required, and no complete physical-quarantine claim follows.

## Exact first command and capture boundary

Reviewed command copy: `red-sa21-reviewed-command.sh`. Its authority is the first RED SA21 block of the above frozen packet, not this copied file alone.

The command uses the unchanged corpus-v2 wrapper with the existing SA2.1 interpreter and RED candidate root; the candidate runner byte-matches repo/scripts/test_postgres.py. It checks PACKET and INPUTS before and after the wrapper and records the wrapper exit separately. The final shell success may therefore coexist with an expected nonzero RED wrapper result: coordinator-wrapper-exit.txt, tests.log, progress.jsonl, JUnit and the sanitized runner receipt are the outcome sources, not the shell's final exit alone.

Wrapper inspection confirms exclusive nonblocking lab locking, evidence mkdir(exist_ok=False), fresh dual-role readiness plus the runner's fresh dual-role preflight, candidate-origin check, before/after source snapshots, progress/JUnit/runner receipts, 600-second test process bound, 90-second other phases, fast server stop in finally, and corpus snapshot/capture/restoration under the lock. Server-stop failure is not promoted into the main return code, so independent stop verification remains mandatory. All 26 original corpus entries and restoration/no-new-file status require terminal audit.

The coordinator will additionally freeze the complete packet, preserve external pins and capture full wrapper output. No raw phase JSON is needed for this source clearance. Do not read, hash or copy tests.json, readiness.json, package-origin.json, postgres-start.json, postgres-stop.json, or credentials; use the authorized safe logs and receipts.

Only the first RED SA21 block is cleared. Stop afterward for independent exact-node, intended/unexpected failure, source/origin, server-stop and corpus-restoration review. The source predicts 12 protected double-failure primary-precedence failures plus the root pending-only stale-material failure, but that prediction is not an observed outcome or an acceptance rule. Any collection problem, timeout, unexpected failure, cleanup warning, origin mismatch or unstable input requires diagnosis. Do not proceed automatically to RED SA2.0 or either GREEN cell.

## Reviewer execution boundary

No product/runtime imports, tests, database calls, network actions, remote operations, installs, credential reads or raw phase JSON reads/hashes/copies were performed. Only the owned reviewer-notes/async-cleanup-red-plan-independent-20261014 directory was written. Seven historical acceptance failures and all seven production gates remain unchanged/UNKNOWN.

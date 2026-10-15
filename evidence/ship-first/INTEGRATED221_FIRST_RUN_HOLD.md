# Integrated221 focused111 SA21: failed-run terminal review

Verdict: FAILED_RUN_PRESERVED / CLOSED_BOUNDARY_VERIFIED. Do not promote this run, continue to SA20, or report integrated111 PASS. The terminal boundary is clean enough for separately reviewed and explicitly selected next work; this is not rerun authorization.

## Exact outcome

Selected: focused111-sa21, exact frozen111 explicit IDs, SQLAlchemy2.1.3 cell.
Coordinator: persistence-recovery-20261013/integrated221-focused111-sa21-coordinator.
Evidence: evidence/cluster-retained-integrated-v2-focused111-sa21-20261015.

JUnit starts2026-10-15T12:14:13.387984+00:00 and records42.687seconds suite time. Exactly78 cases executed in the precise selected prefix:77PASS and1FAIL, zero skips/errors. All78 setup and78 teardown reports pass. There are234 phase reports, not the planned333. The sole failing call is test_genuine_old_native_recovery[v0-schema_abort-link], at native_legacy/test_native_legacy.py:362: DID NOT RAISE TransitionFailure.

Completed PASS partitions: followon23, successor38 non-positive-activation, native metadata5, and11 genuine v0 native cases. The twelfth native case failed. Thirty-three selected cases were not reached:16 native cases, all16 contract cases, and the final successor positive activation. The28 planned subordinate producers must not be claimed as executed; exactly12 producer cases actually ran.

Launcher and runner exit1 agree with JUnit/progress. The exact outer argv matches the frozen action, including -x; runner pytest arguments preserve that selection plus the unchanged wrapper-added progress/JUnit options. No skipped or deselected safety case was substituted for the failure. All completed external observation records have true asserted checks:23 follow-on,23 primary cluster and15 supplementary. Native observations have12 records; the failed case contains only its five successfully reached preliminary checks and cleanup evidence, not the absent mutation/refusal oracle.

## Genuine producer and cleanup closure

Every one of the12 reached child processes has:

- Archived exact argv/cwd/non-secret routing, shell=False and old v0 source route.
- Fresh preflight success in safe stdout, empty stderr, exit0.
- Exactly one named test_genuine_historical_producer JUnit case passing, no skip/failure/error.
- Actual release.json equal to consumer_engines_closed=true and consumer_database_work_finished=true.
- Actual cleaned.json equal to fixture_cleanup_completed=true, producer_source_verified_after=true and helper_input_pins_verified_after=true.
- Matching cleanup_verified and child-inventory assertions in the outer native observation record.

The failed outer case's child also completes this protocol. These files were read individually from the precise temporary handoff directories named in the pinned safe launch receipts. ready.json, request/artifact snapshots and other temporary raw material were not read or copied. The reviewed process source waits for child completion before recording returncode; the zero exits, one-case receipts and cleanup acknowledgements establish completed producer ownership/cleanup for all12, including failure teardown. No child from an unexecuted case is implied.

## Source/runtime identity and safe preservation

All2352 selected runtime pins equal the final reviewed SA21 map in actual admission, immediate post-input capture, and independent current rehash. The221 source and17 control post maps match exactly. Source/external before-after maps remain unchanged; accepted CLUSTER, contract GREEN, integration, runtime-cell review and bounded activation-authority hashes still match. The safe root selection records the fixed HOME/PATH/LANG/TZ mapping; no environment dump was read.

SAFE_SOURCE_ARCHIVE.json records1717 exact safe input-source copies: the complete221 candidate,17 controls, preparation packet, both pinned old producer source trees, and all additionally pinned ordinary Python source/type stubs including admitted dependency source. Each copied file was checked against its admitted hash. No .pyc, compiled binary payload, raw phase JSON, credentials, environment values or key material was copied. Exact admitted nonproduct dependency bytecode was hash-read only as allowed by the freeze, never imported/deserialized/copied. Installed product cache identity remains unqualified.

## Stopped and restored boundary

The safe wrapper output records postgres-stop exit0. postgres-stop.log says server stopped. Root's separately captured post pg_ctl status is3 with no server running; pre status was also3. Pre/post interpreter-link checks exit0 and confirm both selected links. All26 corpus pre/post/prior-corpus maps are equal and every current permitted corpus file independently hashes to that map. Isolation reports primary_receipts_restored=true, archived=[], deleted_during_run=[] and errors=[].

This establishes the recorded terminal boundary, not a standing assertion against later authorized activity. The reviewer started no tests, server or database query and did not inspect live DB state. Review waited for root's terminal notification before reading closure and current allowed hashes. No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json was read, hashed, copied or printed.

## Failure reachability and semantic interpretation

The failed native case had already proved genuine old source/preflight, absent producer backends before consumer work, complete snapshot continuity, unchanged source key references, and successful current-consumer staging at VERIFIED. In run_case, the intended link mutation is installed as a test-only wrapper around migration._inspect_paused, then normal deprotection.abort is invoked inside pytest.raises(TransitionFailure).

The link wrapper first issues ALTER TABLE RENAME CONSTRAINT retained_public_unique TO changed_public_unique, then ALTER INDEX changed_public_unique RENAME TO retained_public_unique. It appends reached and calls the real inspector. The raised-failure expectation is not met. No test assertion independently verifies the intended catalog name/link mismatch between those two DDL statements and the real inspector; reached validation lies after pytest.raises and therefore is never recorded in this failing run.

Strong source-level fixture hypothesis: renaming a constraint-backed index also renames its owning constraint, so the second DDL can restore the original constraint name and leave no intended observable schema drift. The paired rename sequence therefore may be a no-op for the actual contract. This review has not queried the failed fixture, run a reproduction, or obtained a surviving post-DDL catalog snapshot, so that mechanism is not presented as a separately proven native fact from this receipt. The receipt proves the expected refusal did not occur; it alone does not prove product acceptance of a genuinely changed constraint linkage.

Do not change the expected refusal merely to make this test green. The necessary narrow correction is to make the intended native invariant demonstrably different before calling the real inspector, retain the specific TransitionFailure expectation, and retain exact rollback/recovery/access oracles. A source-reviewed fixture can use a single native constraint rename and independently assert the resulting name/identity/linkage facts, without a second rename that may undo it; if a different linkage invariant is intended, design its real native mutation explicitly. Record a reachability/precondition boolean before the validator and require it. Preserve this failed run and exact source/control bytes. Any revised test must be a separately sealed successor with explicit coordinator selection, not an edit/retry represented as the same evidence.

This is a missed fixture-precondition check in the earlier source admission: the initial review accepted the claimed linkage mutation without a native assertion establishing it. Product safety expectations must remain intact while the fixture is corrected or the product defect is demonstrated.

## What this does and does not establish

The eleven passing genuine v0 cases include safe companion abort across the three staged phases, real affected ACTIVE/read/write/refusal, affected reverse staging abort across three phases, two changed-current-survivor cases, two-table atomic rollback/recovery, and native definition-drift refusal/abort recovery. They do not qualify the remaining v0 controls or any genuine v1 controls. No contract mutation case or positive activation ran in this failed campaign. Existing independent historical receipts remain separate.

The integrated feature result, both-cell111 completion, full source suite, installed validation, post-loss evidence importer, durable ABORTED replan, wider legacy plaintext/removal and production gates remain incomplete. Source hashes and successful preliminary cases cannot replace the failed or unexecuted invariants.

No failed lookup or reviewer assertion occurred in this terminal audit. All safe-read hashes and individual child/closure checks are in TERMINAL_CHECKS.json. The source archive manifest records exactly what was copied and what was excluded.

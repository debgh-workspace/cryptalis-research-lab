# V4 statistics G2 metadata SA21: independent post-run review

Date: 2026-10-14 UTC.
Disposition: **ACCEPTED_BOUNDED_METADATA_RESULT**.

The completed SA21 cell is accepted for the frozen G2 deterministic metadata and aggregate contract only. The G2 SA20 counterpart may be selected next by the coordinator under the existing authorization, unchanged frozen proposal, fresh destinations and idle serialized database queue. This review executes nothing, does not automatically advance any cell and does not clear G3 or later groups.

## Observed result and decisive case evidence

The safe tests log reports **16 passed, 83 deselected, 16 warnings in 5.05 s**. JUnit records 16 tests, zero failures/errors/skips, and 5.046 s; the runner receipt reports 16 passes and exit 0. Its elapsed 5.279 s is runner elapsed rather than pytest's rounded test duration. Both records select only the metadata module. No result is inferred from aggregate counts alone.

The source expansion is 10 ambiguous metadata cases, 5 aggregate/remedy cases and 1 private-import source scan. `EXPECTED_CASE_NAMES.txt` enumerates all exact source-derived parameter IDs. Independent comparison with JUnit and the progress stream confirms exactly those 16 unique cases. Every case has one start and exactly one passing setup, call and teardown report. No selected case skipped, failed or merely reached an early assertion.

For all 15 proxy cases, the exact function-specific properties occur in the required order:

1. `statistics_assertions = <function>:COMPLETED`
2. `statistics_fallback_cleanup = [{"stage": "release", "status": "ALREADY_CLOSED"}]`
3. `statistics_fallback_cleanup_completion = <function>:COMPLETED`
4. `statistics_test_completion = <function>:assertions_and_explicit_cleanup_completed`

The final markers are after the explicit native fixture contexts, not inside them. The fallback-completion markers follow successful helper return. The fixed trace establishes that the resource was already closed when fallback ran; G2 does not newly exercise the helper's invalidate/close or failure-preservation branches.

The private-import case has its one exact final completion marker after the entire source loop. Its framework teardown also passes. A second independent text-only search of the candidate package, excluding the private observer file, found neither private observer import/reference string. This is a source-boundary check, not proof about all dynamic execution or public behavior.

Evidence: `CASE_VALIDATION.json`, `JUNIT_CASES.json`, `PROGRESS_CASES.json`, `MARKER_SOURCE_LOCATIONS.txt`, and `PRIVATE_IMPORT_SOURCE_SCAN.txt`. JUnit was inspected as the emitted XML text and its escaped property values, with the extraction/validation queries saved. Readable properties are not a claim of strict xunit2 schema conformance. All 16 record_property/xunit2 compatibility warnings remain preserved in the original logs.

## Qualified behavior and limits

The ten metadata transformations exercise unavailable target, invalid metadata, changed-owner flag, both visibility flags, both expression-target qualification flags, invalid statistic targets and disabled collection. Each passes the complete expected PARTIAL/INCOMPLETE/UNAVAILABLE report, unchanged deployment CHECKED result, exactly one transformed catalog result and unchanged frames.

The five two-field aggregate cases exercise PRESENT (0 missing/0 unavailable), MISSING (1/0 and 2/0), and INCOMPLETE (1/1 and 0/2). Their full assertions qualify exact statuses, ordinals, counts, advisory/unauthenticated authority, effects NONE, ready/complete false, remedy presence only when a field is missing, bounded remedy wording and absent schema identifiers.

These transformations replace selected metadata returned from real fixtures. In particular, the owner/visibility test names do **not** establish native changed ownership, native permission denial, RLS or real visibility restrictions. Likewise proxy MISSING states are not natural initial missing-state observations. No production, security, freshness, planner/performance, maintenance, release, lifecycle-removal or package-free continuation gate is qualified. All seven production gates remain UNKNOWN in the runner receipt. Twelve mutation controls remain unexecuted and separately gated.

## Frozen inputs, complete capture and restoration

All checks below were recomputed from allowed files:

- All **261 pinned inputs** match their checksum list. The anchored JSON filename/hash map exactly equals that list. Both recorded before/after pin logs contain all 261 exact expected `filename: OK` lines, without extras or omissions.
- All **215 candidate files** match the externally anchored source manifest. No candidate/source change was made by this review.
- All three filename/hash anchors match the prior independent review, the original packet, the captured packet and both recorded guard maps:
  - `CANDIDATE_SOURCE_MANIFEST.json`: `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`
  - `INPUTS_MANIFEST.json`: `42cd5f099225512db69b30a6df1ac4277a2c618fbfc3715ad8601e01539080fd`
  - `INPUTS.sha256`: `0e2df963b8acf4dce4b119ab45c72255e1cf1833a3d5be53abb4bed75e405bbf`
- The complete original and captured packet directory trees compare equal at review time (diff exit 0), including generated caches. All **38 authored files** also compare equal with caches excluded. Cache equality does not source-qualify generated bytecode.
- The runner source-before map and both stability maps agree on **154 files**. Every file hashes correctly in both the current candidate and its source-repository archive. Both `unchanged` and actual before/after map equality are verified.
- All **six external Python sources** have identical recorded before/after maps and correct current and archived hashes. The external archive filename set is exactly the six expected files, including conftest and every packet test module, rather than only selected metadata tests.
- All **153 source/test hashes** in the safe runner receipt match current candidate files. The existing repository runner/preflight bytes are unchanged, and packet conftest equals the candidate baseline conftest.
- All **26 prior corpus files** hash correctly both in the immutable prior-corpus archive and the restored live evidence directory. Both filename sets equal the prior manifest. Candidate-corpus is empty; isolation reports no archived changes, no deletions, no errors and `primary_receipts_restored: true`.

Details are in the `*_CHECK.txt`, `*.sha256`, filename-list and comparison artifacts in this review directory. Original evidence and the frozen packet were not altered.

## Execution and shutdown guards

`filesystem-status.json` records before `[0,0,0,0]`, after `[0]`, runner exit 0 and matching external anchors both before and after. The first three action logs are empty, as expected for successful mkdir/copy/byte comparison. Pin action outputs are complete.

The safe runner receipt exactly matches the frozen G2 SA21 pytest arguments, including the explicit full external packet directory, the three-function selector expression and the candidate test pythonpath. The only appended arguments are the unchanged progress plugin, faulthandler timeout and exact JUnit destination. Safe source-root and package-origin receipts identify the intended V4 candidate. Dual-role preflight passed with both recorded prefixes.

The outer wrapper argv is established by the coordinator's explicit execution attestation and source-only inspection of its direct frozen-entry lookup. The attestation identifies the invocation `python persistence-recovery-20261013/run-statistics-v4-group.py g2-metadata sa21` and shell exit 0. Its script calls the selected `runner_argv` without substitutions and verifies all three anchors on both sides. This provenance is documented separately; no raw phase JSON was needed. The script's own shell exit alone is not relied upon: wrapper and post-action statuses were independently read and checked.

The wrapper's five safe phase lines are all exit 0, including the specifically required **`postgres-stop exit 0`**. `postgres-stop.log` confirms `server stopped`. This is independently required because the unchanged runner does not promote postgres-stop status into its overall return. There is no shutdown or corpus-restoration blocker.

## Counterpart decision and remaining boundaries

**No G2 SA21 evidence blocker remains.** G2 SA20 may be selected as the next bounded counterpart under the existing authorization and serialization rules. Both frozen SA20 destinations were absent when checked. Recheck queue idleness and destination freshness at selection; use the exact frozen wrapper/proposal, all three external anchors before/after, complete capture, source-stability receipts, explicit stop exit 0 and restoration checks. Review that actual result before any further advancement. This report supplies no additional credential, role, grant, ownership/RLS, privileged-removal, maintenance or remote-change authority.

## Review safety

Review actions were text/JSON/XML-text reads, comparisons, filename enumeration and SHA-256 checks only. There were no package imports, Python execution, compilation, collection, tests, database calls, database/role changes, installation or remote actions. Raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json` and `postgres-stop.json` were neither read nor processed; the input filename list was checked for these forbidden names before hashing pinned files. Writes are restricted to this newly created independent review directory.

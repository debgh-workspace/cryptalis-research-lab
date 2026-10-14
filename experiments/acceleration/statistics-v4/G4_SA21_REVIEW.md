# V4 statistics G4 snapshot and bounds SA21: independent post-run review

Date: 2026-10-14 UTC.
Disposition: **ACCEPTED_BOUNDED_SNAPSHOT_BOUNDS_RESULT**.

The completed SA21 cell is accepted for the frozen G4 controls only. No SA21 evidence blocker remains for coordinator selection of the exact frozen SA20 counterpart under existing authorization, fresh destinations and an idle serialized database queue. This review runs no cell and grants no automatic advancement to later groups.

## Actual result and complete case evidence

The safe test log records **15 passed, 84 deselected, 15 warnings in 3.57 s**. JUnit reports 15 tests, zero failures/errors/skips and 3.568 s. The safe runner receipt agrees on 15 passes and exit 0; its 3.821859340998344 s is runner elapsed, not pytest duration. Only `test_statistics_snapshot_bounds.py` is selected.

The five frozen source functions expand into exactly **1 snapshot + 8 settings + 1 statement-timeout + 4 parser/admission + 1 lock-timeout = 15 cases**. The saved text-only AWK extractor derives each name and parameter value from source. JUnit contains exactly that ordered list. The independent progress stream contains the same 15 unique cases, each with one start and exactly one passing setup, call and teardown in monotonic order. Every case has exactly one function-specific final `statistics_test_completion` property. Its source site is after deciding assertions and exit from the explicit native fixture context; framework teardown also passes.

All 15 record_property/xunit2 warnings are preserved. The XML is inspected as emitted text and decoded with the saved jq extractor. Readable properties do not establish strict xunit2 schema conformance. See `EXPECTED_CASE_NAMES.txt`, `CASE_VALIDATION.json`, `JUNIT_CASES.json`, `PROGRESS_CASES.json`, `JUNIT_HEADER.json` and `MARKER_AND_ASSERTION_SOURCE_LOCATIONS.txt`.

## Deciding G4 boundaries

### Native snapshot branch is observed

The snapshot case records **`snapshot_missing_branch=OBSERVED_NATIVE_MISSING`**, reaches final completion and passes teardown. It is not an UNOBSERVED or skipped branch.

Source lines 23–69 require the selected second-table index to be naturally absent before intervention. After the first observer pg_stats query executes, a second physical connection checks that absence again, performs one explicit table-only fixture ANALYZE with local 3000 ms statement and 250 ms lock limits, commits, and a further independent connection requires presence. The observer must issue exactly two target queries, keep deployment CHECKED, report statistics PARTIAL, and retain the exact second-field MISSING result. The listener is removed in finally and the fixture exits before final completion.

This supplies bounded native snapshot consistency evidence for the tested two-target fixture, including a committed presence change outside the observer snapshot. No forced absence or auto-analyze disabling is used. The two natural prerequisite-loss paths remain explicit skips in source but were not taken in this cell. The removed-snapshot sensitivity mutation is still unexecuted; this base pass alone does not qualify that mutation control, all catalog scenarios, freshness or performance.

### All eight settings/restoration combinations pass

The source expands `query_failure × lower × autocommit` over False/True. Every combination has final completion and passing framework teardown. At the pg_stats boundary, the callback requires exactly one observed settings tuple: repeatable read, read-only on, pg_catalog search path, and either the default 3 s/250 ms bounds or the already stricter 100 ms/50 ms bounds. This covers ordinary and AUTOCOMMIT engine modes, both with and without a synthetic post-settings query failure.

Every case requires deployment CHECKED. Failure variants additionally require statistics UNAVAILABLE. After observation, all five settings are read again and must equal their pre-observation values. A finally block restores and commits the original statement/lock settings used by the fixture setup. Final completion establishes that this restoration block and fixture context exit returned successfully; there is no separate post-finally read asserting the original values again. No role, database or server default is changed by these controls. Connection acquisition, arbitrary callbacks, total elapsed work and I/O remain outside the statement-bound claim.

### Native statement timeout: 57014

The selected callback lowers the observer transaction's statement timeout to 30 ms, then performs a bounded pg_sleep(0.1). The source requires exactly one callback, statistics UNAVAILABLE with native SQLSTATE **57014**, `cleanup_failed=false`, and every returned observer cleanup item SUCCEEDED. Frames must remain unchanged and `check_deployment()` must still return None. The event listener is removed in finally, and final completion occurs after fixture teardown. These assertions, completion and the framework teardown all passed.

### Native lock timeout: 55P03, with distinct blocker cleanup evidence

The independent blocker connection acquires ACCESS EXCLUSIVE only on this fixture's customer table at the first statistics-query boundary, after deployment checks. It uses bounded local settings. The observer-side ACCESS SHARE probe then produces native **55P03**.

The actual case records, in source order:

1. Fixed fallback trace: invalidate SUCCEEDED, close SUCCEEDED, verify_closed SUCCEEDED.
2. `statistics_fallback_cleanup_completion=<function>:COMPLETED`.
3. `statistics_assertions=<function>:COMPLETED`.
4. Final function-specific `statistics_test_completion`.

The fallback marker alone is not credited as lock behavior. Source lines 204–209 separately require exactly `[True, "blocker_acquired"]`, statistics UNAVAILABLE with 55P03, no observer cleanup failure, unchanged frames and valid deployment returning None. The body and final markers follow those assertions and the explicit fixture teardown. Passing setup/call/teardown independently corroborate completion.

The helper acts only on the independently test-owned blocker, handles already-closed resources, verifies closed state and preserves any outstanding failure if fallback also fails. The successful fixed trace in this cell is not coverage of every helper failure branch or an independent backend-session inventory. Native lock refusal, tested cleanup completion and subsequent fixture consistency are the bounded result.

### Four deterministic parser/admission proxies remain separate from native inventory

The exact source tuples are `(64,4,True)`, `(65,1,False)`, `(1,256,True)` and `(1,257,False)`. Each modifies an in-memory research-plan document, uses an ACTIVE-shaped matching pin, and replaces engine connection acquisition with a synthetic stop. It does not build the corresponding native inventory.

The two within-limit plans must attempt acquisition exactly once and then report deployment UNAVAILABLE/statistics NOT_INSPECTED. Both one-over plans must refuse before any acquisition, with deployment NOT_INSPECTED and statistics UNAVAILABLE/`statistics_inventory_bound`. The monkeypatch context, native baseline fixture context and final completion all finish for each case.

These are deterministic parser/admission controls only. They do not establish G6's exact 64-table/256-index native inventory, planner acceptance, one-over native fixture behavior, execution costs or maximum-inventory cleanup.

## Frozen input, capture and restoration verification

The data-only integrity checks recomputed all of the following before the counterpart's activity:

- **261 pinned inputs** hash correctly. The checksum filename/hash map exactly equals the anchored JSON manifest. Each recorded before/after pin log contains exactly all 261 expected OK lines, with no extra or omitted line.
- **215 candidate source files** hash correctly against the anchored source manifest.
- All three exact filename/hash anchors match the remaining-groups gate, current packet, captured packet and both recorded guard maps:
  - CANDIDATE_SOURCE_MANIFEST.json: `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`
  - INPUTS_MANIFEST.json: `42cd5f099225512db69b30a6df1ac4277a2c618fbfc3715ad8601e01539080fd`
  - INPUTS.sha256: `0e2df963b8acf4dce4b119ab45c72255e1cf1833a3d5be53abb4bed75e405bbf`
- Entire current/captured packet trees compare equal, diff exit 0, including caches. All **38 authored files** also have exact matching relative names and bytes. Cache equality is not bytecode source qualification.
- Runner source-before and before/after stability maps agree on **154 files** with unchanged=true. Current and archived bytes hash correctly and the archive filename set is exact.
- All **six external Python files** have identical before/after maps, correct current/archive hashes and exact archive names, including conftest and all five test modules.
- All **153 safe runner receipt source/test entries** hash correctly. Its map intentionally substitutes scripts/test_postgres.py for the capture map's pyproject.toml and uv.lock; every shared hash agrees. The initial review-only subset assumption and its correction are retained in `REVIEW_METHOD_CORRECTION.txt`. Repository/candidate preflight scripts and packet/candidate conftest are byte-identical.
- All **26 prior corpus files** hash correctly in both preserved archive and restored live evidence. Both filename sets exactly match the prior manifest. Candidate-corpus is empty; its receipt records no archived changes, deletions or errors, and primary_receipts_restored=true.

`VERIFY_INTEGRITY.sh` is a review-only shell/jq/hash reproduction of these data checks. It neither imports nor executes project Python. Check outputs and exact filename lists are retained beside this report. Frozen evidence and packet files were not changed.

## Provenance, stop and counterpart gate

Filesystem status records before `[0,0,0,0]`, runner exit 0 and after `[0]`, with all three anchors on both sides. The first three preparation logs are empty. The safe receipt exactly matches the frozen selected pytest arguments, full external packet directory and candidate test pythonpath, plus only the unchanged progress plugin, faulthandler setting and exact JUnit destination. Safe package-origin/source-root evidence identifies the V4 candidate. Dual-role preflight passed with the recorded prefixes.

The parent explicitly confirms the exact invocation of the unchanged coordinator script with `g4-snapshot-bounds sa21`, frozen lookup/argv, outer exit 0 and no substitutions. Text-only inspection and a saved script hash confirm direct use of that entry's runner_argv and both anchor guards. This attestation is distinct from independent actual pytest-argument and status checks. Outer script success alone would not establish runner or after-action success because those exits are not promoted into the script's terminal exit.

All five safe wrapper phase lines report exit 0. Crucially, the exact **`postgres-stop exit 0`** line is present and postgres-stop.log confirms **server stopped**. This is independently required because the unchanged runner does not promote stop failure into its overall exit. Corpus restoration and post-pins passed; no stop/restoration blocker remains.

The two SA20 destinations were absent at the review's initial check (approximately 22:17 UTC). They were present at the later check after the parent selected the counterpart following the successful guard update. `SA20_DESTINATION_STATUS.txt` retains that later state, not a freshness assertion. This report qualifies SA21 only; it does not inspect or accept the counterpart, and further advancement requires its own actual-result review.

All seven production gates in the safe runner receipt remain UNKNOWN. Native ownership/permission/RLS and broader visibility conditions, privileged removal, package-free continuation, production/security/performance/release qualification and all twelve mutation controls remain outside this result. No credentials, roles, grants, maintenance, remote work or later-cell authority is added.

Review actions were file reads, filename enumeration, text/JSON/XML-text inspection, comparisons and SHA-256 checks only. No Python execution/imports, collection, tests, database actions, installation, network or remote work occurred. Raw phase JSON and secrets were not read or processed. Pinned filenames were screened for forbidden raw phase and secret-style names before hashing. Writes are limited to this independent review directory.

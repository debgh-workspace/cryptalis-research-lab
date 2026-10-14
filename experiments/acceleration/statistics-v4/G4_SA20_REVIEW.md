# V4 statistics G4 snapshot and bounds SA20: independent post-run review

Date: 2026-10-14 UTC.
Disposition: **ACCEPTED_BOUNDED_SNAPSHOT_BOUNDS_RESULT**.

The frozen SA20 G4 counterpart is accepted within the same boundaries as the separately reviewed SA21 cell. No G4 SA20 evidence blocker remains. This is a data-only review, not execution or authorization for a later group, mutation, broader fixture, or production gate.

## Actual result and all selected cases

The safe test log records **15 passed, 84 deselected, 15 warnings in 3.65 s**. JUnit independently reports 15 tests, no failures/errors/skips and 3.649 s. The safe runner receipt reports 15 passes and exit 0; its 3.906529594998574 s is runner elapsed, not pytest duration. Only `test_statistics_snapshot_bounds.py` contributed selected cases.

The five source functions expand to exactly **1 snapshot + 8 settings/restoration + 1 statement-timeout + 4 parser/admission + 1 lock-timeout = 15**. Text-only source extraction generates all 15 exact parameter IDs; JUnit has the same ordered list. The independent progress stream has exactly those 15 unique cases, each with one start followed by one passing setup, call and teardown, in monotonic order. Every case has exactly one function-specific final `statistics_test_completion` property. No extra properties, failures or skips are present. See `EXPECTED_CASE_NAMES.txt`, `JUNIT_CASES.json`, `PROGRESS_CASES.json`, `CASE_VALIDATION.json` and `JUNIT_HEADER.json`.

All 15 record_property/xunit2 warnings remain in the original log. XML was read as emitted text and decoded with the saved jq extractor. Readable properties do not establish strict xunit2 schema conformance; no warning metadata was changed.

## Deciding boundaries

### Native snapshot branch actually observed

The actual snapshot property is **`snapshot_missing_branch=OBSERVED_NATIVE_MISSING`**, followed by final completion and passing framework teardown. Neither UNOBSERVED/skip route was taken.

Source lines 23–69 require natural absence for the second-table index before observation. Immediately after the first target query executes, a second physical connection rechecks absence, performs one explicit table-only fixture ANALYZE with local 3000 ms statement and 250 ms lock bounds, and commits. A further independent connection must then see presence. The observer must issue exactly two target queries, keep deployment CHECKED, report statistics PARTIAL and retain the exact second-field MISSING result. The listener is removed in finally, and the explicit native fixture context exits before the final marker.

This establishes the tested two-target native snapshot behavior across that committed outside change. It does not establish all catalog cases, freshness, performance, forced absence, or mutation sensitivity. The already-present and prerequisite-lost paths remain explicit UNOBSERVED skips in frozen source; the removed-snapshot mutation remains unexecuted.

### All eight settings/restoration cases

All combinations of `query_failure × lower × autocommit`, each False/True, reach final completion and passing teardown. At the pg_stats boundary the source requires exactly one tuple: repeatable read, read-only on, pg_catalog search path, and either 3 s/250 ms default bounds or already stricter 100 ms/50 ms bounds. Both ordinary and AUTOCOMMIT modes are covered, with and without synthetic post-settings query failure.

All variants require deployment CHECKED; injected-failure variants require statistics UNAVAILABLE. After observation, all five settings must equal their pre-observation values. The finally block separately restores and commits the original statement/lock settings used by fixture setup. The final marker establishes successful return from that restoration and the enclosing fixture context; source does not separately reread the original settings after finally. No role/database/server default change is credited. Connection acquisition, arbitrary callbacks, total elapsed work and I/O remain outside this statement-bound claim.

### Native statement timeout and observer cleanup

The selected callback sets the observer transaction's statement timeout to 30 ms, then performs the bounded sleep probe. Passing source assertions require one callback, statistics UNAVAILABLE with native SQLSTATE **57014**, `cleanup_failed=false`, every returned cleanup item SUCCEEDED, unchanged frames and `check_deployment()` returning None. The listener is removed in finally and the native fixture context exits before final completion. These assertions, the marker and framework teardown all passed. This is the specific statement-timeout control, not arbitrary cancellation coverage or an independent backend-session inventory.

### Native lock timeout, independent blocker and distinct markers

At the first statistics boundary, after deployment checks, a separately test-owned connection acquires ACCESS EXCLUSIVE on this fixture's customer table using local bounded settings. The observer's ACCESS SHARE probe must then yield native **55P03**.

The actual properties occur in the frozen source order:

1. `statistics_fallback_cleanup`: invalidate SUCCEEDED, close SUCCEEDED, verify_closed SUCCEEDED.
2. Function-specific `statistics_fallback_cleanup_completion=:COMPLETED`.
3. Function-specific `statistics_assertions=:COMPLETED`.
4. Function-specific final `statistics_test_completion`.

The fallback marker is before the deciding lock assertions and is not accepted as proof of lock behavior by itself. Lines 204–209 separately require exactly `[True, "blocker_acquired"]`, statistics UNAVAILABLE/55P03, no observer cleanup failure, unchanged frames and valid deployment returning None. Body/final markers occur after those assertions and native fixture teardown. Each setup/call/teardown also passes.

The shared helper acts only on the independently test-owned blocker, skips already-closed resources, verifies closed state, and preserves an outstanding primary failure when fallback also fails. The successful fixed trace here does not cover all helper-failure branches. Bounded lock refusal, the tested observer/blocker cleanup and subsequent fixture consistency are supported; broader session-release or native cancellation claims are not.

### Four parser/admission proxies remain proxies

The exact tuples are `(64,4,True)`, `(65,1,False)`, `(1,256,True)` and `(1,257,False)`. They modify an in-memory research-plan document, supply a matching ACTIVE-shaped pin and replace connection acquisition with a synthetic stop. They do not construct the corresponding native inventory.

Both within-limit plans must attempt acquisition once, then report deployment UNAVAILABLE/statistics NOT_INSPECTED. Both one-over plans must refuse without acquiring any connection, with deployment NOT_INSPECTED and statistics UNAVAILABLE/`statistics_inventory_bound`. Monkeypatch context exit, native baseline fixture context exit, final completion and framework teardown all passed.

These controls do not establish G6's exact native 64-table/256-index inventory, native one-over fixtures, planner acceptance, execution costs or maximum-inventory cleanup.

## Frozen inputs, captures and corpus restoration

The reviewer recomputed and checked:

- **261 pinned inputs**, with exact filename/hash equality between the checksum list and anchored JSON manifest. Before/after pin logs contain exactly the complete expected OK lines, without omitted or extra lines.
- **215 candidate source files** against the anchored candidate manifest.
- All three filename/hash anchors against the source-only gate, current packet, captured packet and both recorded guard maps:
  - CANDIDATE_SOURCE_MANIFEST.json: `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`
  - INPUTS_MANIFEST.json: `42cd5f099225512db69b30a6df1ac4277a2c618fbfc3715ad8601e01539080fd`
  - INPUTS.sha256: `0e2df963b8acf4dce4b119ab45c72255e1cf1833a3d5be53abb4bed75e405bbf`
- Exact current/captured packet-tree equality, diff exit 0, including caches; exact relative-name equality and bytes for all **38 authored packet files**. Cache equality does not qualify bytecode as source.
- **154 runner source files** with identical source-before and stability-before/after maps and unchanged=true; current/archive hashes and exact archive names all pass.
- All **six external Python files**, including conftest and all five test modules: identical before/after maps, correct live/archive hashes and exact archive names.
- All **153 safe runner receipt source/test entries**. This map substitutes scripts/test_postgres.py for the capture map's pyproject.toml and uv.lock; all shared entries agree. Repository/candidate preflight scripts and packet/candidate conftest are byte-identical.
- All **26 prior corpus files** in preserved archive and restored live evidence, with exact filename sets and hashes. Candidate corpus is empty; its safe receipt records no archived changes, deletions or errors and primary_receipts_restored=true.

`VERIFY_INTEGRITY.sh` is a review-only shell/jq/hash reproduction, adapted from the inspected SA21 review checker for the exact SA20 paths and duration. It does not execute or import project Python. Outputs, hash lists and exact filename lists are retained. Frozen input/evidence files were not changed.

## Command provenance and safe terminal checks

The frozen SA20 group selects its exact `toolchain/sa20-venv/bin/python` at both interpreter positions, the unchanged corpus wrapper, the V4 candidate, full external packet directory and frozen five-function OR selector. Safe receipt pytest arguments exactly match those selected arguments plus only the expected progress plugin, faulthandler setting and exact JUnit destination. Safe package-origin/source-root evidence identifies the V4 candidate; dual-role preflight passed with its recorded prefixes.

The parent confirms the exact outer command `python persistence-recovery-20261013/run-statistics-v4-group.py g4-snapshot-bounds sa20`, unchanged JSON lookup/argv, no substitutions and outer exit 0. That attestation is retained separately from independent safe-receipt and status verification. Read-only coordinator source inspection confirms direct frozen entry selection, absent-destination checks, before-actions, runner invocation, after-actions and both anchor guards. Its own terminal exit does not promote runner/after failures, so outer success alone is insufficient.

Filesystem status independently records before `[0,0,0,0]`, runner exit 0, after `[0]` and all three anchors on both sides. The first three preparation logs are empty; the successful non-`-p` mkdir and coordinator absence checks support freshness at launch. All five safe wrapper phase lines are exit 0. The exact **`postgres-stop exit 0`** line is present and postgres-stop.log confirms **server stopped**. Stop verification is independently required because the unchanged runner does not promote stop failure into its overall exit. Corpus restoration and post-pins pass. No stop/restoration blocker remains.

## Exact comparison with SA21

Both cells have the same 15 exact source-derived cases, properties and successful statuses, including OBSERVED_NATIVE_MISSING and the full lock fallback/body/final sequence. The independently re-extracted JUnit case objects compare exactly. Both have no skips/errors/failures and 15 retained warnings. SA21 pytest/JUnit durations were 3.57/3.568 s; SA20 durations are 3.65/3.649 s. These differences are not a performance qualification.

The entire frozen group objects compare exactly after normalizing only the exact interpreter difference and dependency-cell paths. Both interpreter paths are explicitly checked before normalization: SA21 uses `release-lab/s23-installed-20261014/sa21/bin/python`; SA20 uses `toolchain/sa20-venv/bin/python`. Actual safe pytest arguments similarly match except the cell-specific JUnit path. Source/test hash maps, runner source stability maps, external stability maps, prior corpus maps, counts/module sets, preflight and seven UNKNOWN gates are identical. Both captured packet trees compare byte-for-byte equal, diff exit 0.

The initial review-only comparator normalized the cell token but omitted the full interpreter-directory difference; its expected false result and correction are preserved in `REVIEW_METHOD_CORRECTION.txt`. No input, test, wrapper or execution was changed. `SA21_CASE_COMPARISON.json` and `SA21_BOUNDARY_COMPARISON.json` retain the successful exact comparisons.

The counterpart therefore adds SA20 support for the same bounded native snapshot/settings/timeout and deterministic admission controls. It supplies no expanded claim relative to SA21. Native ownership/permission/RLS and broader visibility, privileged removal, package-free continuation, all twelve sensitivity mutations and production/security/performance/release qualification remain outside both results. All seven production gates remain UNKNOWN. G5/G6 require their own coordinator selection and actual-result review; no automatic advancement is granted here.

## Review discipline

Review actions were file reads, filename enumeration, text/JSON/XML-text inspection, comparisons and SHA-256 checks only. No Python execution/imports, compilation, collection, tests, database actions, installation, network or remote work occurred. Raw phase JSON and secrets were neither read nor processed. Pinned filenames were screened for forbidden raw-phase and secret-style names before hashing. Writes are confined to `reviewer-notes/s24-statistics-v4-g4-sa20-independent-20261014`.

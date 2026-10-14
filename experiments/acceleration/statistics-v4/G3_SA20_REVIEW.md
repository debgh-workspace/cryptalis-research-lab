# V4 statistics G3 contract SA20: independent post-run review

Date: 2026-10-14 UTC.
Disposition: **ACCEPTED_BOUNDED_CONTRACT_RESULT**.

The completed SA20 result is accepted for the exact frozen G3 contract. Together with the accepted SA21 counterpart, both dependency cells now have matching bounded contract evidence. No G3 evidence blocker remains. This review performs no execution and authorizes no automatic advancement, broader group, mutation, maintenance, role change or production gate.

## Actual cases and completion

The safe tests and wrapper logs agree on **11 passed, 88 deselected, 11 warnings in 2.93 s**. JUnit records 11 tests, zero failures/errors/skips and 2.929 s. The safe runner receipt records 11 passes, exit 0 and 3.1489706200081855 s elapsed; this is runner elapsed, not pytest duration.

The nine frozen source functions expand to exactly eleven cases: owner-before/after and PostgreSQL read-only enforcement each have False/True variants. A text-only source extractor independently generated `EXPECTED_CASE_NAMES.txt`. JUnit and progress contain exactly those eleven unique IDs, all from test_statistics_diagnostic.py, without omissions or additional cases. Each case has exactly one start, passing setup, passing call and passing teardown in monotonic order.

Every case has exactly its function-specific `statistics_test_completion` property with the value `<function>:assertions_and_explicit_cleanup_completed`. All nine marker sites are after the deciding assertions and outside their explicit fixture context, so the markers establish completed explicit cleanup before the passing framework teardown. G3 has no corrected G2/G4 body/fallback site requiring extra properties. No partial execution or skip is credited as a pass.

Supporting files: `CASE_VALIDATION.json`, `EXPECTED_CASE_NAMES.txt`, `JUNIT_CASES.json`, `PROGRESS_CASES.json`, `JUNIT_HEADER.json`, `MARKER_SOURCE_LOCATIONS.txt`. All eleven record_property/xunit2 compatibility warnings remain preserved. Reading the emitted XML properties is not strict xunit2 schema validation; no warning metadata was changed.

## Qualified behavior and limits

- Both unique/nonunique owner cases compare the private observer with independent native statistics-presence reads. After explicit fixture ANALYZE, they require native presence and the exact PRESENT report, including fields/counts/scope, advisory unauthenticated authority, effects NONE and incomplete/not-ready status. **Natural initial MISSING is not established.** The source permits auto-analysis or an intervening presence change and records no initial-absence branch property.
- Existing check_deployment() still returns None. Active owner doctor refuses with attachment_requires_planned_runtime_role and roles NOT_INSPECTED. The planned runtime observer gives the exact explicit-owner-required NOT_INSPECTED result without captured pg_stats access or SET ROLE. The stale pin case requires refusal before any observer engine connection and no statistics inspection.
- **Native PostgreSQL read-only enforcement passes in ordinary and AUTOCOMMIT modes.** The control first proves a zero-row DELETE succeeds on an ordinary owner connection and rolls it back. Injecting the same probe at the observer statistics-query boundary must produce UNAVAILABLE with actual SQLSTATE **25006**, retain deployment CHECKED, preserve frames and leave deployment validation returning None. This is native server refusal in a synthetic fixture, not only a proxy/read-only flag assertion.
- Setting the native expression-column statistics target to zero produces INCOMPLETE/statistics_collection_disabled, no ANALYZE remedy and valid deployment. The observer trace excludes the tested maintenance/DDL/DML/role-switch prefixes, application-table spelling and distribution-value column names; frames, plan artifact and pin remain unchanged. Report serialization excludes fixture schema and field identifiers. Optional missing-remedy wording is checked only when missing_fields is present.
- **The driver-error case is deliberately induced.** A synthetic non-integer sentinel cast at the pg_stats boundary produces actual SQLSTATE **22P02**. The pass requires statistics UNAVAILABLE, deployment CHECKED, no sentinel in report JSON/string/repr or subsequent captured stdout/stderr, no writers-stopped advice and valid deployment afterward. Positive exposure controls precede capture reset. This does not establish every driver exception, permission/RLS failure or logging/telemetry destination.
- The selected planner, setup doctor, check_deployment, active runtime doctor and attach flow completes with zero calls to a failing replacement of the private observer. A separate text-only scan finds no private-observer module/name reference elsewhere in candidate Python product source. This qualifies the tested current routes and source boundary, not all possible future routes or a new public API.

Fixture ANALYZE remains explicit owner-only, table-only, without a column list, with local lock_timeout 250 ms and statement_timeout 3000 ms, and no retry. These results do not authorize automatic maintenance, persistent setting changes, role/grant/ownership/RLS changes or privileged lifecycle work. Changed ownership, native permission/visibility/RLS conditions and same-fixture missing-state deprotection/package-free continuation remain unqualified. The twelve sensitivity mutations remain separately gated and unexecuted. Performance, freshness, production, security and release are not qualified; all seven production gates remain UNKNOWN.

## Independent integrity, capture and restoration checks

All checks below were recomputed from allowed local files:

- **261 pinned inputs** hash correctly; their exact filename/hash map equals the anchored INPUTS_MANIFEST.json. Both captured pre/post pin logs equal all 261 expected successful lines with no extras or omissions.
- **215 candidate files** match CANDIDATE_SOURCE_MANIFEST.json.
- All three filename/hash anchors match the remaining-groups review, current packet, captured packet and before/after guard maps:
  - CANDIDATE_SOURCE_MANIFEST.json: `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`
  - INPUTS_MANIFEST.json: `42cd5f099225512db69b30a6df1ac4277a2c618fbfc3715ad8601e01539080fd`
  - INPUTS.sha256: `0e2df963b8acf4dce4b119ab45c72255e1cf1833a3d5be53abb4bed75e405bbf`
- The entire current and captured packet trees compare equal, diff exit 0, including caches and all **38 authored files**. Cache equality does not source-qualify bytecode.
- All **154 runner source-before entries** match both current candidate and source-repository archive bytes. The archive filename set is exact. Source-stability before/after maps equal the source-before map and unchanged is true.
- All **six external Python files** match current and archived bytes, exact archive names and equal before/after stability maps. This includes conftest and all five test modules.
- All **153 safe runner source/test entries** hash correctly. Its overlap with the 154-entry archive map agrees; the archive additionally contains pyproject.toml and uv.lock, while the safe receipt additionally contains scripts/test_postgres.py. The repository runner/preflight is byte-identical to its candidate copy, and external conftest is byte-identical to candidate tests/conftest.py. Pinned wrapper/helper inputs are unchanged.
- All **26 prior corpus receipts** hash correctly in both the preserved archive and live restored evidence directory. Both filename sets match the prior manifest exactly. Candidate-corpus is empty. The isolation receipt records no archived changes, deletions or errors and primary_receipts_restored=true.

The three successful preparation logs are empty. All source, packet and original evidence files remain unchanged; additive review artifacts are confined to this directory.

## Exact command, process and shutdown boundary

Filesystem status records before `[0,0,0,0]`, after `[0]` and runner exit 0, with all three anchors correct before and after. The safe runner receipt exactly matches the frozen G3 SA20 selected pytest arguments: full external packet directory, all nine selectors and candidate test pythonpath. Only the unchanged progress plugin, faulthandler timeout and exact JUnit destination were added. Safe source-root/package-origin evidence identifies the intended V4 candidate; dual-role preflight passed.

The coordinator explicitly attests direct selection of frozen `g3-contract sa20` through `persistence-recovery-20261013/run-statistics-v4-group.py`, with outer exit 0. Text inspection confirms direct frozen group/cell lookup, runner_argv invocation and pre/post anchor verification; the inspected script hash is retained. Outer exit 0 is coordinator-attested, not independently encoded in filesystem-status.json. That script does not promote failed runner/post-action statuses to its shell exit, so the recorded statuses were checked separately.

All five safe wrapper phase lines are exit 0, including **postgres-stop exit 0**. The safe shutdown log says **server stopped**. This separate shutdown check is necessary because the unchanged runner does not promote a failed postgres-stop return to its own exit. Post-pins and corpus restoration also pass, so no shutdown/restoration blocker remains.

## SA21 comparison

The accepted SA21 report was read and its hash retained in `SA21_REPORT.sha256`. `SA21_COMPARISON.json` verifies identical expected cases and final properties, equal runner/external source maps, equal safe-receipt source maps, equal restored corpus and preflight, and identical UNKNOWN gates. Frozen wrapper commands normalize identically after replacing only dependency interpreter paths and cell-specific evidence destinations; actual pytest arguments normalize identically too. Both case-validation artifacts agree exactly.

SA21 recorded 11 passed, 88 deselected, 11 warnings in 3.13 s; SA20 recorded the same counts in 2.93 s. This duration difference is not a performance result. Both cells retain the same no-natural-MISSING, synthetic-driver and tested-route qualification limits.

Any next group still requires coordinator selection, its exact frozen proposal, fresh destinations, an idle serialized database queue and the existing capture/anchor/pin/shutdown/restoration gates. This report supplies no additional authority.

## Review safety

Only local file reads, text/JSON/XML-text inspection, filename enumeration, comparisons and SHA-256 checks were used. No Python execution, imports, compilation, collection, tests, database actions, installation, network or remote operations occurred. Raw tests.json, readiness.json, package-origin.json, postgres-start.json and postgres-stop.json were neither read nor processed. Only the safe package-origin.log, tests.log, postgres-stop.log and selected wrapper lines were inspected for phase results. Pinned names contain none of the excluded phase filenames or checked secret-style paths. No credentials or secrets were accessed. Writes are limited to reviewer-notes/s24-statistics-v4-g3-sa20-independent-20261014.

# V4 statistics G3 contract SA21: independent post-run review

Date: 2026-10-14 UTC.
Disposition: **ACCEPTED_BOUNDED_CONTRACT_RESULT**.

The completed SA21 cell is accepted for the frozen G3 contract only. No evidence blocker remains for coordinator selection of the G3 SA20 counterpart under the existing authorization, exact frozen proposal, fresh destinations and idle serialized database queue. This review executes nothing and does not automatically advance the counterpart, G4 or later groups.

## Actual result and complete case evidence

The safe tests log records **11 passed, 88 deselected, 11 warnings in 3.13 s**. JUnit records 11 tests, zero failures/errors/skips and 3.134 s. The safe runner receipt agrees on 11 passes and exit 0; its 3.4043025609862525 s is runner elapsed, not pytest duration. Only the diagnostic module was selected.

Nine source functions expand to eleven exact cases: the owner-before/after and PostgreSQL read-only functions each have False/True parameter variants. `EXPECTED_CASE_NAMES.txt` is derived from the frozen source with the saved text-only AWK extractor. Independent JUnit and progress comparisons confirm exactly those eleven unique cases, with no extra or omitted case. Every case has one start followed by exactly one passing setup, call and teardown report in monotonic order.

Every JUnit case has exactly one property:

`statistics_test_completion = <function>:assertions_and_explicit_cleanup_completed`

The nine function-specific marker sites are outside and after their explicit native fixture contexts, after all deciding assertions. Thus every recorded pass completed both the assertions and explicit context teardown, and its subsequent framework teardown passed. G3 has no corrected G2/G4 fallback site requiring additional body/fallback properties. No skip or partial execution is credited as success.

See `CASE_VALIDATION.json`, `EXPECTED_CASE_NAMES.txt`, `JUNIT_CASES.json`, `PROGRESS_CASES.json`, `JUNIT_HEADER.txt` and `MARKER_SOURCE_LOCATIONS.txt`. The XML was read and parsed as emitted text; this is not strict xunit2 schema validation. All eleven record_property/xunit2 compatibility warnings remain preserved without metadata changes.

## What the result qualifies

- Both unique/nonunique owner cases compare the observer with independent native presence checks, then require native presence and exact PRESENT report after explicit fixture ANALYZE. The report assertions cover exact fields/counts/scope, advisory unauthenticated authority, effects NONE, incomplete/not-ready status and remedy presence conditional on absence. **These passes do not establish natural initial MISSING.** Source intentionally tolerates auto-analysis or a presence change between observations, and this cell records no initial-absence branch property.
- Existing `check_deployment()` still returns None, and active owner doctor still refuses with `attachment_requires_planned_runtime_role`, leaving roles NOT_INSPECTED.
- The planned runtime observer returns the exact NOT_INSPECTED/explicit-owner-required result, with no captured pg_stats read or SET ROLE. The stale pin case requires rejection before any observer engine connection and no statistics inspection.
- **Native PostgreSQL read-only enforcement is exercised in both ordinary and AUTOCOMMIT modes.** Each case first proves a zero-row DELETE can execute through an ordinary owner connection, rolls it back, then injects that probe at the statistics-query boundary. The observer must report UNAVAILABLE with SQLSTATE **25006**, keep deployment CHECKED, preserve frames and leave deployment validation returning None. These are native refusal checks in the isolated synthetic fixture, not merely a proxy flag or SQL-text check.
- Native expression-column statistics target zero yields INCOMPLETE with `statistics_collection_disabled`, no ANALYZE remedy and unchanged valid deployment.
- The observed owner-query trace excludes the tested maintenance/DDL/DML/role-switch prefixes, application-table spelling and distribution-value column names. Frames, plan artifact and pin remain unchanged; report serialization excludes fixture schema/field identifiers. The optional remedy wording check runs only when missing_fields is present. This does not establish every possible statement route or authorize maintenance.
- **The driver-error case is a deliberately induced failure boundary.** A synthetic non-integer sentinel is passed through an integer cast at the pg_stats boundary, producing actual database SQLSTATE **22P02**. The accepted assertions require statistics UNAVAILABLE, deployment CHECKED, no sentinel in the returned report's JSON/string/repr or subsequent captured stdout/stderr, no writers-stopped advice and valid deployment afterward. Its positive exposure controls prove the sentinel can be observed before the capture reset. This does not qualify all driver exceptions, native permission/RLS conditions or all logging/telemetry destinations.
- The selected current planner/setup-doctor/check-deployment/active-runtime-doctor/attach flow completes while a failing spy replaces the private observer entry, with zero calls. An independent text-only candidate scan also finds no private-observer module/name reference outside its own module. Current public-route separation is preserved for this tested flow and source boundary; it is not a universal or future-route guarantee and does not add a public observer API.

The fixture ANALYZE remains explicit, owner-only, table-only without a column list, with local 250 ms lock and 3000 ms statement limits and no retry. Production/security/performance/freshness/release gates remain unqualified. All seven production gates in the safe runner receipt remain UNKNOWN. Native changed ownership, permission denial, RLS, broader visibility conditions, privileged removal and package-free continuation are not established here. Twelve mutation controls remain unexecuted and separately gated.

## Frozen inputs, full capture and restoration

All of the following checks were recomputed from allowed files:

- **261 pinned inputs** match the frozen checksum list. Its filename/hash map exactly matches the externally anchored INPUTS_MANIFEST.json. Before and after pin logs each contain exactly all 261 expected `filename: OK` lines, without extras or omissions.
- **215 candidate files** match the anchored source manifest.
- All three exact filename/hash anchors match the prior remaining-groups review, current original packet, captured packet and recorded before/after guard maps:
  - CANDIDATE_SOURCE_MANIFEST.json: `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`
  - INPUTS_MANIFEST.json: `42cd5f099225512db69b30a6df1ac4277a2c618fbfc3715ad8601e01539080fd`
  - INPUTS.sha256: `0e2df963b8acf4dce4b119ab45c72255e1cf1833a3d5be53abb4bed75e405bbf`
- The entire original and captured packet trees compare equal at review time, diff exit 0, including generated caches. All **38 authored packet files** also compare equal with caches excluded. Cache equality does not source-qualify bytecode.
- The runner source-before map and both source-stability maps agree on **154 files**. Each current candidate and source-repository archive file hashes correctly. The archive filename set is exact, and both actual before/after equality and unchanged=true are checked.
- All **six external Python files** have identical recorded before/after maps and correct current/archive hashes. The external archive contains exactly the expected six names, including conftest and all five packet test modules.
- All **153 source/test entries** in the safe runner receipt match current candidate files. The repository runner/preflight remains byte-identical to the candidate copy, and packet conftest remains byte-identical to candidate tests/conftest.py. The wrapper, corpus helper and pinned runner inputs also pass the 261-input check.
- All **26 prior corpus files** hash correctly in both the preserved archive and restored live evidence directory. Both filename sets match the prior manifest exactly. Candidate-corpus is empty; the isolation receipt has no archived changes, no deletions, no errors and primary_receipts_restored=true.

Supporting checks, manifests and filename comparisons are in this review directory. No original evidence or frozen inputs were changed.

## Command provenance, exits and stop boundary

The filesystem receipt records before `[0,0,0,0]`, after `[0]` and runner exit 0, with all three anchors correct on both sides. The first three successful action logs are empty; pin logs are complete.

The safe runner receipt exactly matches the frozen G3 SA21 pytest arguments, including the full external packet directory, all nine selector names and candidate test pythonpath. Its only additional arguments are the unchanged progress plugin, faulthandler timeout and exact JUnit destination. Safe package-origin/source-root receipts identify the intended V4 candidate, and dual-role preflight passed with both recorded prefixes.

The outer invocation is established by the coordinator's explicit direct-frozen-entry/outer-exit-0 attestation and text-only inspection of `persistence-recovery-20261013/run-statistics-v4-group.py`. That script directly selects the frozen group/cell entry and calls its runner_argv; the inspected script hash is retained. This provenance is separate from the safe receipt's actual pytest argv and does not depend on reading raw phase JSON. The coordinator script's shell exit alone is insufficient because runner/after statuses are not promoted to that exit; this review checks those recorded statuses independently.

All five safe wrapper phase lines are exit 0. In particular, **postgres-stop exit 0** is present and postgres-stop.log confirms **server stopped**. This explicit shutdown check is required because the unchanged runner does not promote postgres-stop return into its overall exit. Clean corpus restoration and post-pins are independently verified, so no shutdown/restoration blocker remains.

## Counterpart gate and review safety

The two frozen G3 SA20 destinations were absent during review. Recheck their freshness and queue idleness at selection; use the exact frozen counterpart proposal and all existing capture, external-anchor, pin, stop and restoration guards. Review its actual result before further advancement. This acceptance adds no credential, role, grant, ownership/RLS, maintenance, privileged-removal, remote or release authority.

This review used only file reads, text/JSON/XML-text inspection, filename enumeration, comparisons and SHA-256 checks. No Python execution, package imports, compilation, collection, tests, database connection/actions, installation, network or remote actions occurred. Raw tests.json, readiness.json, package-origin.json, postgres-start.json and postgres-stop.json were neither read nor processed. Pinned filenames were checked for those forbidden names and secret-style paths before hashing. Writes are restricted to this independent review directory.

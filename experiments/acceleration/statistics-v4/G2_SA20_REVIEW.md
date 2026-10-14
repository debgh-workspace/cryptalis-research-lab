# V4 statistics G2 metadata SA20: independent post-run review

Date: 2026-10-14 UTC.
Disposition: **ACCEPTED_BOUNDED_METADATA_RESULT**.

The completed SA20 counterpart is accepted for the same frozen G2 deterministic metadata and aggregate contract as the accepted SA21 cell. No G2 evidence blocker remains. This is a data-only post-run audit, not another execution, later-group authorization or blanket advancement. G3 and later cells retain their own coordinator selection, source/command, serialization and actual-result review gates.

## Exact selected cases and completion evidence

The safe tests log reports **16 passed, 83 deselected, 16 warnings in 4.59 s**. JUnit records 16 tests, zero failures/errors/skips and 4.593 s. The safe runner receipt records 16 passes, exit 0 and 4.815 s runner elapsed. The two durations cover different intervals and do not establish a performance result.

Independent source inspection confirms 10 ambiguous-metadata parameter variants, 5 exact aggregate/remedy variants and 1 complete private-import source scan. The source-derived exact parameter IDs in `EXPECTED_CASE_NAMES.txt` match all 16 unique JUnit names and progress node IDs. Only the metadata module was selected. Every case has exactly one start and passing setup, call and teardown in order. No case was skipped or accepted on a partial assertion sequence.

All 15 proxy cases have the exact function-specific properties in this order:

1. `statistics_assertions = <function>:COMPLETED`
2. `statistics_fallback_cleanup = [{"stage": "release", "status": "ALREADY_CLOSED"}]`
3. `statistics_fallback_cleanup_completion = <function>:COMPLETED`
4. `statistics_test_completion = <function>:assertions_and_explicit_cleanup_completed`

Source lines 75–79 and 126–130 place the body marker after substantive assertions, fallback-completion after successful helper return, and final completion after the native fixture context exits. The helper's already-closed branch explains the fixed trace; this G2 run does not newly qualify invalidate/close failure branches or primary-failure preservation. The private-import case has one exact final marker after the whole source loop at line 142 and a passing framework teardown. An independent static text scan of every other candidate package Python file found no `_statistics_diagnostic` or `_observe_statistics` reference.

`CASE_VALIDATION.json`, `JUNIT_CASES.json`, `PROGRESS_CASES.json` and `MARKER_SOURCE_LOCATIONS.txt` preserve the deciding checks. JUnit was read as emitted XML text and its escaped property values. Its readable properties do not establish strict xunit2 schema conformance. All 16 existing record_property/xunit2 compatibility warnings remain preserved; no warning metadata was changed.

## Behavior supported and excluded

The 10 transformed metadata cases establish the exact PARTIAL/INCOMPLETE/UNAVAILABLE report, unchanged deployment CHECKED status, exactly one transformed statistics result and unchanged application frames for unavailable target, invalid metadata, changed-owner flag, both visibility flags, both expression-target qualification flags, invalid target values and disabled collection.

The 5 two-field aggregate cases establish PRESENT (0 missing/0 unavailable), MISSING (1/0 and 2/0), and INCOMPLETE (1/1 and 0/2). Their complete assertions cover exact statuses, field ordinals and counts; advisory/unauthenticated authority; effects NONE; ready/complete false; remedy present only when missing; bounded remedy wording; no schema identifiers; and two transformed catalog results.

These are deterministic transformations of metadata returned by real fixtures. The owner/visibility names do not establish native changed ownership, native permission denial, real visibility restrictions or RLS. Transformed MISSING is not a natural missing-state observation. The source-import check is bounded static evidence, not proof of all dynamic routes. No native ownership, security, freshness, planner/performance, maintenance, lifecycle-removal, package-free continuation, production or release claim follows. All seven production gates remain UNKNOWN. The 12 mutation controls remain unexecuted and separately gated.

## Frozen inputs, capture and corpus integrity

Recomputed checks all pass:

- **261 pinned inputs** match current bytes. The externally anchored JSON filename/hash map exactly equals the checksum list. Both recorded pin logs match all 261 expected `filename: OK` lines in checksum-list order, without extras or omissions.
- **215 candidate source files** match the external source manifest.
- The original packet and captured packet compare byte-equal as full directory trees at review time, with diff exit 0. All **38 authored files** separately compare equal with cache files excluded. Generated cache equality is not source qualification.
- The runner before map and both source-stability maps agree on **154 files**, with exact before/after equality and `unchanged: true`. Every file hashes correctly in the current candidate and source-repository archive, and the archived filename set is exact.
- All **6 external Python sources**, including conftest and every packet test module, have matching before/after maps and correct current/archive hashes. The external archive filename set has no omission or addition.
- All **153 source/test hashes** in the safe runner receipt match current candidate files. The pinned wrapper, runner and dual-role preflight bytes remain unchanged. Packet conftest equals the candidate baseline conftest.
- All **26 prior corpus files** match their hashes in both prior-corpus archive and restored live evidence directory. Both filename sets exactly equal the prior manifest. Candidate-corpus is empty. Isolation reports no archived changes, deletions or errors, and `primary_receipts_restored: true`.

The three deciding filename/hash anchors match the prior review, source packet, captured packet and both recorded guard maps:

- `CANDIDATE_SOURCE_MANIFEST.json`: `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`
- `INPUTS_MANIFEST.json`: `42cd5f099225512db69b30a6df1ac4277a2c618fbfc3715ad8601e01539080fd`
- `INPUTS.sha256`: `0e2df963b8acf4dce4b119ab45c72255e1cf1833a3d5be53abb4bed75e405bbf`

The `*_CHECK.txt`, checksum maps, filename lists and comparison artifacts preserve these checks. No frozen source or evidence was edited.

## Execution provenance, preflight and shutdown

`filesystem-status.json` records before `[0,0,0,0]`, after `[0]`, runner exit 0 and all three exact external anchors on both sides. The first three action logs are empty as expected for successful mkdir/copy/comparison. Complete pre/post pin output was checked separately.

The safe runner receipt matches the frozen G2 SA20 pytest arguments, with the complete external packet directory, exact three-function selector and candidate tests pythonpath. Its only appended arguments are the unchanged progress plugin, faulthandler timeout and exact JUnit output destination. Safe source-root and package-origin receipts identify the intended V4 candidate. Dual-role preflight passes with both expected recorded prefixes.

The outer frozen-wrapper argv and shell exit 0 are established by the coordinator's explicit execution attestation plus source-only inspection of its exact group/cell lookup and direct runner_argv call. `COORDINATOR_EXECUTION_ATTESTATION.txt` records that evidence boundary; the script hash matches the SA21 audit. No execution replay or raw phase JSON was used. The independently inspected status and safe logs, not outer shell success alone, establish the required internal success conditions.

All five safe wrapper phase lines are exactly exit 0. In particular, **`postgres-stop exit 0`** is explicit and the shutdown log says **`server stopped`**. This is independently required because the unchanged runner does not promote postgres-stop failure into its overall return. No shutdown or corpus-restoration blocker remains.

## Comparison with SA21 and next boundary

`SA21_COMPARISON.json` confirms exact equality of the case names, class names, property sequences and no-failure status; progress starts and setup/call/teardown outcomes; runner source map; and external source map. External anchors also match. SA20 therefore supplies the same bounded evidence as SA21, with its own preserved receipts, source archives, packet capture, corpus verification and safe shutdown. Timing differences do not broaden that result.

Both G2 cells are now accepted within this evidence boundary. A later group still requires the coordinator's applicable existing authority, fresh destinations, an idle serialized queue, unchanged frozen commands/anchors and independent review of its actual result. This report grants no credential, role, ownership/RLS, persistent-grant, maintenance, privileged-removal or remote-change authority.

## Review safety

Review actions were permitted text/JSON/XML-text reads, filename enumeration, comparisons and SHA-256 checks only. No package import, Python execution, compilation, test collection/test execution, database action, installation, network or remote action occurred. Raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json` and `postgres-stop.json` were neither read nor processed; their filenames were excluded from the pinned-input check before hashing. No secrets were read. All writes are confined to this new independent review directory.

# Statistics forced-present V4: independent terminal-result audit

Date: 2026-10-15 UTC.

Disposition: **ACCEPT the bounded V4 actual mutation result and corrected command-capture evidence contract. Actual exit remains 1. Historical V3 complete evidence-contract acceptance remains HOLD.**

This is acceptance of the specified deterministic transformed-metadata sensitivity experiment, not production qualification, a full gate pass, or authorization for another run.

## Shared boundary closed first

Before notifying the coordinator that installer snapshot work could proceed, `boundary-v1.py` independently verified exactly 26 live shared compatibility-corpus names and hashes against the retained prior-corpus manifest and archive. The archive has no extra names; candidate-corpus is empty. The isolation receipt has no generated archives, deleted-during-run entries, or restoration errors and reports original receipts restored. The independent name/hash check corroborates that report.

Safe wrapper stdout has exactly one postgres-stop exit line, specifically `postgres-stop exit 0`; the admitted safe stop log contains `server stopped`. Wrapper stderr and coordinator entry log are empty. Terminal log equals stdout followed by stderr. Wrapper and coordinator exits are actual 1.

The exact ordered action sequence is 21 before actions, one runner action with exit 1, and 15 after actions. Every before/after action exits 0; all 72 expected non-runner output names exist as ordinary single-link files, with empty stderr. The filesystem summary records no interruption and zero before/after failures. Its `mutation_accepted:false` is the launcher's intentional stop-for-independent-review state, not a negative test result.

The boundary notification preceded all remaining audit work. No live shared payloads, interpreter targets, or tools were rehashed after that handoff. Recorded clean shutdown is not a fresh server/process-state probe; none was made.

## Actual command capture and control

The nonempty `outer-wrapper-argv.json` parses as exactly 16 strings. It equals both an independently written literal vector and the captured execution manifest, retaining the fixed SA21 interpreter, unchanged corpus-v2 wrapper, V4 derivative and evidence roots, original external packet, exact selector and flags. The coordinator selection separately contains the exact reviewed launcher command and anchor digest; the coordinator log contains no jq error.

Captured direct identities equal the independently reviewed values:

- Launcher: `2dd5890f2b81e69adf12eae7150cafff8bafe57d042ba8e442856a4eea6ec080`
- Guard: `a82f663c2bb90d1ac799f8f83105d6d8a74009c33758d8764015668ff41d5620`
- Anchors: `f860257879d57b3f8739346a382b27fe29b542816146fd5aa75983d5c411e40f`
- Source-review report: `fdc0dbc38ba46d15c7abdc1385ae5b2898df999ff04fcdc203fd3f25782e24f4`

The actual ordered `before/wrapper-argv` receipt is exit 0 and precedes the runner. Captured launcher source uses jq's `--` delimiter and a checked run_action gate before wrapper invocation. A capture or status-writer failure exits before reachability; failed after-actions are counted without skipping later checks; nonzero runner exit is preserved. The prior pinned source review supplies bounded synthetic failure-case evidence. This successful actual run itself does not exercise those failure branches.

V3's empty required argv file and unchecked jq failure are not repaired, replaced, reconstructed or waived. Its historical complete evidence-contract HOLD remains intact.

## Exact outcome and lifecycle

JUnit and progress evidence agree on five exact parameter identities:

- states0 CHECKED/PRESENT: complete PASS control.
- states1 PARTIAL/MISSING: expected assertion failure at line 104, CHECKED instead of PARTIAL.
- states2 PARTIAL/MISSING: expected assertion failure at line 104, CHECKED instead of PARTIAL.
- states3 PARTIAL/INCOMPLETE: expected assertion failure at line 106, missing-fields 0 instead of 1 with observed-fields 2.
- states4 PARTIAL/INCOMPLETE: complete PASS control.

The complete three failure texts match the expected source-location and assertion bodies exactly. Actual summary is 3 failed, 2 passed, 94 deselected, 5 warnings; JUnit has zero errors and skips. Exact 20 ordered events are five start/setup/call/teardown groups, with all setup and teardown phases passing and only the three specified calls failing. The runner exit is 1, not normalized.

All five cases record fallback `release / ALREADY_CLOSED`. Both controls contain assertions-completed, fallback-completed and post-context final-completion properties. Failed bodies contain only their fallback receipt, as expected after their deciding assertion; later assertions and completion markers are not claimed for them. The unchanged source puts setup/publication and CHECKED deployment assertions before the deciding assertions. No new probe independently proves schema absence.

All five warnings are the existing record_property/xunit2 warning. Actual JUnit properties are retained and verified. No import, collection, SQL, timeout, skip, teardown or unexpected exception is counted as a mutation effect. Safe origin records the V4 derivative; safe readiness and runner preflight record both unchanged role checks passed.

## Captured provenance and pin evidence

Exact admitted immutable inventories are original source 215, derivative source 215, original authored packet 38, frozen original authored packet 38, and V4 packet 69. Source maps and payload hashes agree. Exactly `_statistics_diagnostic.py` changes; 214 files are unchanged. The independently generated diff equals both the captured original forced_present patch and V4 SOURCE_DELTA.patch. All frozen authored bytes equal the captured original packet.

All 30 direct anchor targets independently hash correctly. The 548 safe and 261 original pin names, SHA maps and JSON maps agree; the original checksum map remains byte-identical to the captured original packet. Independently rehashed 534 safe-input targets available in the immutable captures. The 14 external tools, interpreters and historical evidence targets are not duplicated by these captures and were deliberately not reread after the boundary handoff. Their evidence is the exact successful before/final-before/after 548-pin receipts, exact before/after 261-pin receipts, and the pinned earlier source review, not a claim of new independent post-run hashing. Names of these 14 targets are retained in UNCAPTURED_PIN_NAMES.json.

Before-copy and after-compare outputs exactly enumerate source215, derivative215, original38 and packet69 names and success markers, with admitted inventory summaries and only metadata cache-name exclusions. The archived wrapper154 and runner153 sets were independently derived from source categories; external6 comes from authored Python membership. Archived wrapper154/external6 payloads agree with captured derivative/original source, runner153 hashes agree, and before/after source maps are identical. Runner pytest arguments equal the planned arguments plus unchanged progress, timeout and JUnit options.

Validator labels inherited from the V3 checker that say CURRENT or CURRENT_AND_BEFORE_AFTER refer here to physical immutable captured roots. They do not mean a post-handoff live-source reread. Redundant self-comparisons in the adapted validator are not relied on as proof of live/capture equality; that conclusion is supported by the exact recorded before-copy and after-compare receipts and independent captured hashes.

## Retained reviewer attempts

- `boundary-v1.py` and outputs: passed the immediate live corpus/recorded stop boundary and command/action checks.
- `validate-v1.py` and outputs: preserved failure at a too-short literal all-pins stdout expectation. The checker omitted the legitimate fixed `ALL_INPUT_NAMES_TYPES_VALIDATED 548 before payload hashes` marker between 30 anchor lines and 548 pin lines.
- Coordinator authorized only inserting that exact marker in three all-pins comparisons. `validate-v2.py` and outputs pass. Original-safe-pins expectations were unchanged, since those outputs have no marker. No source or evidence was altered or normalized.
- `crosscheck-v1.py` and outputs: passed archive completeness, 72 exact action outputs, safe origin/preflight, byte-exact failure bodies and warnings.
- `capture-check-v1.py` and outputs: passed exact before/after named capture receipts and coordinator command/exit evidence.

Data-only validators admit conservative names/categories, full parent chains, ordinary single-link types and inventories before payload parsing/hashing. Hash manifests are not used as standalone read allowlists. No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json payload was read, copied or hashed. No secret, cache payload or environment payload was inspected. No launcher, guard, product, helper, database/status/queue probe, tests, installation, Git operation or network request was executed; only standard-library reviewer validators were run.

## Stop and scope

Stop at this terminal audit. No retry, SA20 cell, other mutant, ordinary G1–G6 rerun, privileged action, ownership/RLS change, ANALYZE, deprotection, role retirement or Group D follows. Ordinary accepted G1–G6 remain unchanged. All seven full gates remain UNKNOWN. This finding does not establish natural missing-statistics behavior, freshness, native ownership/permission/RLS guarantees, performance, public integration or production qualification.

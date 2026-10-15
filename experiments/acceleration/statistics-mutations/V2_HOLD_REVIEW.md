# Statistics forced-present V2: independent source and command review

Date: 2026-10-15 UTC.
Disposition: **HOLD — source mutation, oracle and current safe pins pass; the V2 launcher is not admitted.**

## Result

The current V2 derivative is the intended 215-file source-only mutation. Exactly one file changes, its actual diff is byte-identical to the already existing `forced_present.patch`, and the other 214 files are unchanged. All 548 V2 safe pins and all 261 original safe pins pass after independent filename/category/type validation. The exact original/derivative source inventories are 215/215; original/frozen authored packets are 38/38; the V2 overlay is 69 files. All preparation direct digests match.

The existing unchanged oracle independently predicts three assertion failures and two fully passing controls. No mutation execution, test collection, import, database action or launch occurred. Both proposed evidence destinations remain absent.

The V2 source materially corrects the prior cache-copy and unfrozen-capturer problems. However, one independently scheduled guard action can read an input after earlier guards have already rejected its path type. This is a source-level fail-closed defect. No launch vector is accepted from this version. Preserve this packet and review evidence unchanged; a separately authorized fresh correction and independent review are required.

## Blocking finding H1: a failed inventory does not prevent a later unvalidated payload read

`scope_guard.sh:124–129` implements `original-safe-pins` as follows:

1. Load and validate the V2 `ORIGINAL_SAFE_INPUT_PATHS.txt` list of 261 original targets.
2. Validate each of those targets with `input_target`.
3. Check the local original-safe checksum-list names.
4. At line 128, run `cmp "$P/ORIGINAL_SAFE_INPUTS.sha256" "$O/INPUTS.sha256"`.
5. Hash the original 261 targets.

The original packet's `experiments/s24-statistics-diagnostic-v4-20261014/INPUTS.sha256` is **not** one of those 261 targets. All 30 anchor targets are inside the V2 overlay, so the anchor check also does not establish the original map's type. The original map is one of the V2 548 inputs, but that is checked in a separate action.

`launch_sa21.sh:127–132` deliberately continues from failed inventory/all-pins actions to `original-safe-pins`, and `after_all` does the same for the independent final audits. Consequently, if the original map is already a symlink or otherwise disallowed linked file when the launcher begins, original-packet inventory and all-pins can fail correctly, yet line 128 still opens the disallowed target before the accumulated failure stops launch. The same issue applies to post-run drift. This requires no concurrent race. A differing comparison still reads payload bytes and therefore does not make the access safe.

This finding is static source analysis. The current original map is an ordinary single-link file and passed independent validation. No symlink, hardlink, raw-phase, cache or secret test target was created, and no unsafe path was opened to demonstrate the finding.

A corrected version must locally validate the original map's complete path, ordinary-file and link properties before this comparison, rather than relying on another action's success. All independent final actions should retain their independent execution while performing their own necessary safety checks before payload access. This review does not authorize or implement a correction.

## Verified safe data and source preservation

The review did not treat any hash manifest as a sufficient safety allowlist. It independently classified every target by conservative relative syntax, forbidden-name exclusions, approved source/packet categories or explicitly named external targets; checked path components and ordinary/single-link file types; and compared complete safe inventories before hashing input payloads. Generated cache directory names were excluded before traversal into payloads. The two exact previously identified interpreter links were checked as narrow hash-only exceptions, with resolved Python 3.12 identity; neither interpreter was invoked.

Verified results:

- The V2 JSON map exactly matches its 548-name checksum list and safe path list. All 548 hashes pass.
- The original JSON filename/hash map equals the original checksum map after sorting by filename. All 261 original pins are present unchanged in V2 and all pass.
- Original and derivative manifests have the same exact 215 names. Each source manifest's hashes match its actual source files.
- The original source manifest retains its external digest `2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1`.
- The sole changed file is `src/cryptalis/_statistics_diagnostic.py`: original `6534250833d3a2362f838a1574a5b0bdd028b8016a8502167539b6a41140f962`; derivative `f2e8c43fcaf604c7be1d9dea63d1df30a4735daa643afbbbc9095eec66ec7568`.
- The actual labeled unified diff equals both V2 `SOURCE_DELTA.patch` and the existing original `mutations/forced_present.patch` byte-for-byte. Only the final presence-dependent CHECKED/PARTIAL and PRESENT/MISSING return changes. Earlier UNAVAILABLE branches remain intact.
- Every one of the 38 original authored files equals its frozen preservation copy. The authored-name list also equals the prior independent review's list. No cache payload is included in that claim.
- Static wrapper, safe runner and external Python filename sets independently reproduce the expected 154, 153 and 6 names.
- Original external conftest and the derivative baseline conftest are equal. The derivative preflight runner and repository runner are equal.
- A text-only scan of the other package Python sources finds neither private observer reference string; the observer remains private and unhooked.
- Both proposed V2 evidence destinations remain absent. No queue, database or environment execution was attempted.

`VALIDATION-v2.txt`, its separate `attempt-v2/` evidence, `CROSSCHECKS-v1.txt`, `ACTUAL_SOURCE_DELTA.patch` under `attempt-v2/`, and the source/map artifacts record these checks.

The first reviewer attempt is preserved as `verify-v1.sh`, `VALIDATION-v1.txt` and its files. It stopped before payload hashing because the reviewer incorrectly compared the sorted original JSON map against the original checksum list's historical order. This is a reviewer comparison-order error, not product drift. The separately preserved V2 reviewer attempt corrected only that comparison, sorted the original checksum map and passed. No failed reviewer artifact was replaced.

## Oracle review

`test_statistics_metadata.py:24–33` first obtains a real seven-field catalog row. The selected transform changes only boolean presence, or sets the collection target to zero for `None`. It does not replace the observer report. The exact expected states are independently hard-coded at lines 82–87. Normal multiple-table fixture planning, application and publication precede the assertions, and deployment CHECKED is asserted at lines 102–103.

The independently predicted results are:

- `states0-CHECKED-PRESENT-0-0`: passing control.
- `states1-PARTIAL-MISSING-1-0`: deciding assertion failure at line 104.
- `states2-PARTIAL-MISSING-2-0`: deciding assertion failure at line 104.
- `states3-PARTIAL-INCOMPLETE-1-1`: deciding assertion failure at line 106. Earlier unavailable handling preserves INCOMPLETE, but the mutant missing count becomes zero.
- `states4-PARTIAL-INCOMPLETE-0-2`: passing control because both earlier unavailable returns remain effective.

All five full identities agree across the expected-name list, execution manifest, oracle manifest, baseline references and accepted G2 case names. The prediction is five selected cases, 94 deselected, three assertion failures, two passes, and pytest/wrapper exit 1. The accepted G2 reports establish prior baseline passes in both cells; no ordinary rerun is needed or selected.

Actual-result acceptance would require exactly those failures after completed setup and prior deployment checks; passing framework teardown for every case; both controls completing all assertions, fallback and final completion markers; and safe fallback outcomes for every case with no FAILED status or cleanup-failure note. Import, collection, setup, SQL-type, timeout, skip or cleanup problems are not kills. Failed bodies ordinarily cannot reach lines 125–126, 129 or 130; the later assertions and completion markers must not be claimed executed for them.

## Outer launcher and retained execution boundary

The reviewed V2 launcher is a real frozen capturer. It checks fresh destinations, directly binds the guard source and independent anchor digest, validates exact inventories and safe pins, performs named-only source and packet copies and comparisons, repeats inventories/pins before the wrapper, and probes the existing queue nonblockingly. The wrapper must then acquire its unchanged existing lock. No waiting, retry or alternate cell is selected.

The frozen wrapper array in source matches `MUTATION_EXECUTION.json`. It uses the unchanged SA21 interpreter and corpus-v2 wrapper; the V2 derivative; fixed V2 evidence; derivative test pythonpath; the original explicit external packet directory; and only `test_exact_aggregate_and_remedy_contract`. The frozen archival packet is not the pytest argument, and the derivative's ordinary tests are not selected. All six external Python sources remain capture targets.

The unchanged wrapper retains dual private-file SELECT 1 preflights, package-origin verification, a 600-second test limit, progress/JUnit output, source/external maps and archives, stop and corpus restoration. Wrapper phase text is redacted by the unchanged existing helper before being printed. The outer launcher captures stdout/stderr separately, preserves the actual wrapper status and records per-action outputs/statuses. `terminal.log` is stdout followed by stderr, not temporal interleaving. `set -e` is not used by the launcher; final checks are separate, and expected exit 1 is not normalized. Catchable interruption remains incomplete evidence, and available final audits are attempted.

These improvements do not cure H1. Independent final actions must be safe even after a preceding failure. A future corrected version must still stop after its single SA21 result for actual-result review. That review must verify complete current/archived 154-file wrapper maps, 153-file runner map, six external maps, 215-file derivative identity and every hash; exact prior-corpus names and archive/live hashes with no new matching files or restoration errors; exactly one `postgres-stop exit 0` and `server stopped`; and the complete five-case oracle evidence. Status booleans alone remain insufficient. Raw phase JSON is never an audit fallback.

## Exact reviewed identities; no accepted launch command

The following independently recomputed direct digests identify the held V2 packet. They are not execution approval:

- `ANCHORS.sha256`: `9a7b5eac996b2dbb3de239b13ea4bb7fcd3b460d04ee5b85901ca6b66ba572c7`
- `launch_sa21.sh`: `8ac7d360bb01fad52667b80befcdc330126e005b22917ef4fee32b3604dc91ba`
- `scope_guard.sh`: `034271db2807cfd13f4b4499dff7b236fd4a26a1db109cfc619c292c35d55beb`
- `INPUTS.sha256`: `106c1f48d89df3908c4b5f85ce3dfa192d926d3e2b6d585afe643240d2c59414`
- `INPUTS_MANIFEST.json`: `2df41e46d6e8e3f91523c2253ecd6c7039d5cca918d237e2070b3afdf3f8fa6d`
- `CANDIDATE_SOURCE_MANIFEST.json`: `852adb5084923980a5d85cd0921916f83ea3752cd4811f027b87c4602c7957b3`

The proposed command below was reviewed as data and is **rejected for launch from this version**:

```sh
bash /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/statistics-forced-present-v2-20261015/launch_sa21.sh --coordinator-selected-sa21 --anchors-sha256 9a7b5eac996b2dbb3de239b13ea4bb7fcd3b460d04ee5b85901ca6b66ba572c7
```

## Safety and remaining holds

All review actions were shell text/JSON processing, filename/type inspection, allowed-file SHA-256, byte comparisons and bash syntax parsing. Neither reviewed script was run. No Python/package/test import, compilation, collection, test, database/server/status/probe, network, Git, installation or runtime action occurred. Original S23 dependency environments were neither edited nor executed. The two previously pinned interpreter links were only metadata-checked and hashed.

No raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, `postgres-stop.json`, secret, environment-dump or cache payload was read, copied or hashed. Writes were confined to this new independent review directory. Original candidate/packet, first failed preparation, V2 derivative/packet, dependencies and accepted evidence were unchanged.

Accepted ordinary G1–G6 remain 99 cases per cell / 198 total. All seven full gates remain UNKNOWN. SA20, other mutants, ordinary reruns, privileged Group D, new clusters/roles, ownership/RLS changes, ANALYZE, package-free execution, deprotection, role retirement and other privileged holds remain held. This source review also does not release the installer's S23 environment reservation or independently select any execution.

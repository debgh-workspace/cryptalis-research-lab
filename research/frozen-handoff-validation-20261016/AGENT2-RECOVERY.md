# Frozen recovery/removal instructions: finite source validation

2026-10-16 04:10 UTC. **No new concrete undocumented mismatch or operationally misleading step found in the reviewed public recovery/removal route.** This is source/document reconciliation only. It does not accept a new smoke, disaster drill, legacy importer, durable forward-ABORTED replan, or production safety claim.

## Bound inputs

Paths below are relative to `cryptalis-executable/` unless stated otherwise.

- Selected source: `candidate-doctor-remedy-integrated221-v1-20261015/` (C below), source221 manifest identity `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7`, as declared in the current selection record. `../CURRENT_CANDIDATE.json` hashes to `96970253998d2f86b7eb58d11778093629e19994b078bb1dfd1175d98b9d16a3`. This review checks a finite source subset, not the whole manifest again.
- Public guide: `preview-docs-v4-source221-20261015/RECOVERY.md` (R below), SHA256 `5b6818a3abdee4f603934870922a575c150b35d436d1fc1b67548073687b64e6`.
- Current handoff: `experiments/frozen-preview-handoff-v1-20261016/INDEX.md:18–28` supersedes historical selected-artifact/pending labels and preserves the guide's procedural limits.
- All cited file hashes are in `CITED_INPUTS.sha256`. The four reviewed runtime files migration.py, deprotection.py, _legacy_designation.py and cutover.py were also byte-compared to original Integrated221; they are unchanged. Historical accepted evidence is attributed to its original candidate.

## Checked operational boundaries

1. **Current edited values, not old snapshots.** R:18, 53–65 correctly separates pre-switch abort from decrypt-back and calls for independent current-value/type/NULL/membership comparison. C/src/cryptalis/deprotection.py:253–272 reads retained CF1 payload slots and stages only protected fields; 327–378 authenticates/decrypts current frames and checks staged values/membership; 398–424 restores protected values into original native slots and retires the two staging/payload columns. Public columns are not copied into a historical suffix reconstruction. Source-level oracles at C/tests/test_deprotection.py:93–115 and test_deprotection_ordinals.py:34–74,81–113 exercise current edits and native metadata; their presence is not a new execution result.

2. **Forward verification and abort phase limits.** R:16–20 matches C/src/cryptalis/migration.py:857–867,881–900. Explicit verify admits only BACKFILLED/VERIFIED; abort refuses PENDING/ACTIVE. Ordinary apply verifies before switching. A switched but not yet ACTIVE operation cannot jump directly into reverse planning: R:38 requires the ACTIVE source pin; deprotection.py:150–163 delegates to migration.py:904–913, which requires the actual source ACTIVE state.

3. **Reverse approval, publication and fencing.** R:38–65 matches deprotection.py:129–144,147–163,203–249,439–478. Separate reverse identity/consent and a distinct plaintext role are required. PLAINTEXT_PENDING retains the fence; PLAINTEXT_ACTIVATING and current cutover readiness precede PLAINTEXT_ACTIVE. R:63 leaves actual grants/worker termination to separately approved operator actions. cutover.py:14–101,105–150 confirms inspection/templates are not execution or automatic permission repair.

4. **Retained-native and legacy failures.** R:24–34 correctly treats missing legacy designation as NOT_INVENTORIED, never false. _legacy_designation.py:15–58 classifies the authenticated retirement set, blocks destructive recovery where original indexes could be retired, and preserves the surviving map only in the admitted no-retirement case. Reverse abort still performs full staged-schema/fence inspection, preserves the full current retained-index map, and atomically restores the source ACTIVE state (deprotection.py:481–507; migration.py:676–687; _legacy_designation.py:61–79). It does not manufacture lost historical flags. Old/unversioned reverse staging and incompatible original visible column layouts refuse at deprotection.py:227–230,275–282. The general legacy-layout/importer limitation is already disclosed in KNOWN-LIMITATIONS.md:16 and R:32.

5. **Forward and reverse ABORTED are distinct.** R:29 already says to preserve the forward ABORTED journal and that automatic deletion/replanning is not supplied. migration.py:360–362 blocks a new plan while the journal exists; 479–481 blocks apply of the aborted identity. Reverse abort instead retains a source-linked descendant record and returns the source to ACTIVE. A separately proposed reverse plan may inventory matching ABORTED descendants (deprotection.py:164–169); removal rechecks their identities and ancestry (559–569). This bounded reverse path does not close forward ABORTED-replan qualification or authorize journal deletion. No new missing-feature finding is opened.

6. **Removal retains external recovery duties.** R:69–83 matches deprotection.py:524–573: actual externally checked workload/backup evidence, old-worker stop attestation, REMOVING authority, PLAINTEXT_ACTIVE, exact inventoried journal set and dependency-safe retirement precede completion. REMOVED authority is required for the separate trusted restore/startup check. Package removal occurs last; backup readers/keys and exact artifacts remain obligations. The source expressly does not authenticate the backup service on the caller's behalf.

## Evidence and scope

The accepted substantive guide review is `reviewer-notes/preview-docs-v3-independent-20261015T1435/review.md`, SHA256 `2b40f6cc372b3a498f5f362e566e4eda0d9fa720bcefb50b44c66e998e3d5689`; v4's link-only acceptance is `reviewer-notes/preview-docs-v4-independent-20261015T1445/review.md`, SHA256 `d9fdb19bfbce8e436a644891d50858c57fb4381b48a62346bb2f1775be152ef4`.

The accepted original-Integrated221 focused terminal reviews are `reviewer-notes/integrated221-installed-focused111-sa21-v2-independent-20261015/REVIEW.md` (`f8d89657d61ce621515351dc818ef5872c11f0d1161472cd642f4bc54b30fba6`) and the SA20 counterpart (`7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678`). Their genuine historical-producer/native-mutation observations support their finite stated boundary; neither claims generic lost-metadata repair or full durable ABORTED replan. No test counts are reissued as fresh evidence.

Inherited source lifecycle/walkthrough prose contains historical descriptions of unimplemented decrypt-back and dropped original columns. EVIDENCE.md:50–52 already warns that inherited descriptions do not override current source and accepted receipts. The reviewed public RECOVERY route does not instruct operators to use that historical storage model; this is not reported as a new defect.

Only source/document/review bytes and local hashes/comparisons were used. No product/module import, test/collection, database/status operation, installation, private runtime/cache/corpus body, provider action or Git write occurred. Only this isolated report directory was created. Existing approvals, pending public-smoke permission and current-role continuity requirements are unchanged.

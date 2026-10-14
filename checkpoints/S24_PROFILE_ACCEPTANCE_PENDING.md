# S24: disposition of the seven historical reverse failures

Date: 2026-10-14. Status: SOURCE/DOCUMENT REVIEW ONLY. No tests, database actions, executable edits, Git actions, or remote actions were performed. This review does not approve a contract change. Its only output is this review directory.

Candidate reviewed: `candidate-s24-test-oracles-r3-20261014`, identified in the root checklist by manifest `6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d`. The manifest identity is reported from the checklist, not independently recomputed here. The unchanged historical test file was independently hashed: `4855458d1b0847c353accab010b8521cc7374601f272340df8b2367ea8ea9cd5`.

## Decision-ready result

No missing retained-profile implementation algorithm is demonstrated by these seven failures alone. The exact historical assertions belong to the earlier suffix-reconstruction mechanism. The current retained mechanism preserves public columns in place. The two mechanisms have different legitimate safety checks, while their required end results are the same: exact current values, native visible order/types/metadata, bounded actual transport, and loud refusal before unsafe changes.

The current test selection contains mutually incompatible expectations for the same retained fixture:

- Five old tests require reverse planning to refuse a public metadata attribute. The retained metadata tests require reverse planning to succeed with that attribute and prove exact preservation.
- The old tamper test requires a public `_copy_` column. Retained current-edit controls require that no such column exists.
- The old wide-public test requires a 512-byte chunk to refuse an untouched wide public label. The retained transport control requires the same kind of value to stay outside the fetched projection and the bounded operation to succeed.

A runtime change cannot meet both sets on the same exact profile without artificial test-dependent behavior or a material mechanism change. Reintroducing public copying solely to turn the old assertions green would add work and metadata/permission risks. Adding blanket metadata refusal would regress currently tested retained admission and still would not resolve the two copy expectations. Neither is a justified correction.

The safety contract itself does not need weakening or an invented new byte-budget definition. What remains unresolved is the explicit acceptance/compatibility boundary: which versioned executor/profile must satisfy the literal suffix assertions, and which exact retained-profile proof satisfies the corresponding obligations. The reviewed local contract/decision trail does not contain an owner ratification of that boundary. This is not a claim that no approval exists elsewhere; an exact existing owner decision could resolve the authority gap.

## Authoritative requirements and historical mechanism

1. `candidate-s24-test-oracles-r3-20261014/docs/lifecycle.md:173-195` requires authenticated current-value reconstruction, ordinary SQL types, writer exclusion, package-free application behavior, reviewed generated-object retirement, and retained-backup recovery or approved disposition. It does not require copying an untouched public column.
2. `docs/lifecycle.md:242-246` defines a logical maintenance-data bound, first-remaining-row refusal, no skip/truncation, preserved committed prefixes, and explicit adequate-budget resume. It expressly does not establish RSS bounds. The protected values actually fetched/transformed must remain bounded; bytes that never enter the transition projection cannot be counted as if transported. This does not exempt PostgreSQL server, WAL, rewrite, disk, or pause costs from separate measurement.
3. `docs/decisions.md:3-5,29-42` distinguishes selected contracts from research mechanisms and chooses current-data transform-back. The document does not make historical mechanism IDs permanent implementation obligations.
4. `checkpoints/CP45-ordinal-repair-integration-spec.md` is explicitly PROPOSED. It requires exact public-copy verification, byte accounting, full metadata inventory, and safe permission handling when suffix columns are reconstructed. Its retained-slot alternative was explicitly not selected at that checkpoint; later research cannot be retroactively described as approved there.
5. `checkpoints/CP46-bounded-ordinal-correction.md:5-15` scopes the five metadata refusals to copied ordinary-text public suffix columns and layout 2. It requires public-copy byte accounting and exact UTF-8 comparison because this implementation actually copies those fields. It also says the temporary restriction does not reduce final product scope.
6. `checkpoints/CP42-ordinal-strategy-research.md` retains the old-snapshot hazard of the early retained-slot proposal. Merely resolving the seven test applicability questions cannot qualify the later retained forward snapshot/reader boundary, performance, or promotion.
7. `inputs/CRYPTALIS_DOT_CONTINUOUS_RESEARCH_ENGINEERING_MANDATE.md:29-30,107-115` permits isolated competing prototypes and proven invariant-preserving fixes, requires approval for material contract change, preserves broad metadata/legacy repair ambitions, and does not silently authorize new rights or ACL replay.
8. Root `CRYPTALIS_BUILD_CHECKLIST.md`, S1W/S2/S5 and later S15/S17 entries, expressly preserves the seven failures, distinguishes native metadata counterparts from acceptance, and keeps broader legacy compatibility open. The 19:39 interruption entry is not a terminal R3 qualification result.

Canonical README/lifecycle prose still contains historical drop-column/ordinal limitations. It is not an exact profile dispatch specification for the present research candidates. That documentation mismatch must be reconciled through a reviewed versioned disposition; neither old prose nor present code silently approves the other.

## Current source mechanism

In `src/cryptalis/deprotection.py`:

- `plan`, lines 136-185, is read-only, checks current authority/schema and calls `_admit_suffix` before producing the reverse artifact.
- `_model`, lines 240-259, selects only protected original columns as targets. Its `copied_columns` is empty on this path. Protected reads use the retained physical payload slots.
- `_admit_suffix`, lines 262-269, requires the original visible order and raises `inplace_research_legacy_layout_refused` for reordered layouts. It does not implement generic original-suffix recovery.
- `_backfill` and `_verify`, lines 335-365, use the actual protected stream and verify transformed values. The retained path has no public copy to publish or authenticate.
- `_switch`, lines 382-407, re-verifies, locks, checks snapshots, updates original protected slots, drops private staging/payload columns, restores admitted protected objects/comments, and checks ordinary schema. It does not recreate the public label column.

This source explains the failures. It is not executable proof of preservation, bounds, snapshot safety, or full compatibility.

## Exact disposition for each failure

1. `test_reverse_refuses_unhandled_public_suffix_comment_before_staging`
   - Original suffix/layout-2 executor: keep exact `unsupported_reverse_suffix_metadata` refusal, no added journal/staging effect, and the original failure test.
   - Retained executor: allow only an admitted shape that preserves the current comment and native column identity/metadata. Require read-only planning and exact current values through reverse and final removal. If the actual transform cannot preserve the attribute, typed pre-effect refusal remains mandatory.
   - Counterparts: `test_retained_public_metadata_survives_current_data_reverse[comment]` and `test_native_public_metadata_survives_final_removal[comment]`.
2. `test_reverse_refuses_unhandled_suffix_attributes[column_grant]`
   - Legacy refusal remains required for unsupported copied-column reconstruction.
   - Retained acceptance requires exact ACL identity and effective intended reads, while retired writer privileges remain absent. No new GRANT, recipient, right, grant option, or automatic ACL restoration is implied.
   - Counterparts: retained metadata `[column_grant]` and `test_retained_public_select_acl_survives_removal_without_relaxing_retired_writes`.
3. `test_reverse_refuses_unhandled_suffix_attributes[statistics]`
   - Legacy refusal remains. Retained proof must preserve `attstattarget=100`, native identity/full metadata and current values through final removal.
   - Counterparts: retained metadata and final-removal `[statistics]`.
4. `test_reverse_refuses_unhandled_suffix_attributes[storage]`
   - Legacy refusal remains. Retained proof must preserve the configured `attstorage` after `SET STORAGE EXTERNAL`, full metadata and current values.
   - Counterparts: retained metadata and final-removal `[storage]`.
5. `test_reverse_refuses_unhandled_suffix_attributes[compression]`
   - Legacy refusal remains. Retained proof must preserve configured `attcompression` after `SET COMPRESSION pglz`, full metadata and current values. This does not prove physical recompression or every server build.
   - Counterparts: retained metadata and final-removal `[compression]`.
6. `test_changed_public_staging_refuses_switch`
   - Legacy executor must still detect actual public-copy corruption, refuse switch, and retain protected data/state.
   - Retained executor must prove absence of public copies and preservation of post-backfill current public edits, including wide values; it must still refuse corrupted actual protected staging, frames, membership, fences, and generations before switch.
   - Counterparts: both `test_retained_reverse_preserves_public_edits_without_copy_staging` variants; all five `test_changed_verified_data_never_switches` variants; original NULL/Unicode/order and abort controls.
   - The current historical failure is `NoResultFound` before the decisive tamper assertion, not evidence that a corrupted copy was accepted.
7. `test_public_copy_participates_in_chunk_byte_bound`
   - Legacy executor must include required copied public bytes in the bound and preserve exact refusal/resume behavior.
   - Retained executor must independently prove untouched public bytes never enter actual backfill/verify transport, while actual protected projection bytes obey no-oversized-return, no-skip, unchanged-repeat-refusal, committed-prefix and same-operation adequate-budget-resume obligations.
   - Counterparts: `test_retained_reverse_never_projects_untouched_wide_public_value_into_chunk_transport`; both `test_retained_reverse_protected_byte_refusal_preserves_exact_state_and_recovers` variants; both native transport observer sensitivity controls.

These are individual obligations, not permission to replace a refusal assertion with a blanket success assertion.

## Smallest owner decision, if no exact prior approval can be produced

Proposed decision label: `D-REVERSE-PROFILE-ACCEPTANCE`. It is a proposal, not an approved ID or implemented change.

Ask:

> Approve this version-specific acceptance rule for the research candidate: preserve and execute the seven original suffix-copy/refusal assertions unchanged against the genuine original suffix/layout-2 executor; qualify the exact retained-native v0 and comments-v1 profiles with mandatory independent current-data, metadata, actual-byte-bound and refusal controls, without requiring a public copy or a blanket refusal when the original column is preserved in place. Keep every historical failed run visible and keep generic legacy conversion, unsupported metadata/dependencies, and all production gates open. No automatic format conversion or new permission action is authorized.

Exact profile identities to bind in the disposition:

- Historical suffix: `cryptalis.transition/v1`, `cryptalis.reverse/v1`, reverse staging layout 2; separate genuine version-pinned executor.
- Retained v0: `cryptalis.transition/retained-native-research-v0`, `cryptalis.reverse/retained-native-research-v0`, reverse layout 101.
- Retained comments-v1: `cryptalis.transition/retained-native-comments-research-v1`, `cryptalis.reverse/retained-native-comments-research-v1`; exact current constructor/layout checks remain required. Do not infer unknown-format admission from a name prefix.

The decision should explicitly say whether the separate original-layout executor is only a retained, bounded recovery tool or a supported compatibility product. This review recommends the former existing evidence boundary unless broader support is deliberately selected. No broad ACL/default/view/FK scope decision is needed merely to preserve these five attributes in place; generic reconstruction remains a separate requirement and approval/qualification track.

If the owner requires one current executor to support both original suffix and retained inputs, that is a separate compatibility implementation slice. It needs exact dispatch, authentic predecessor/reader/format admission, genuine old producer states, metadata/refusal/tamper/byte oracles, crash and recovery evidence, and dual-version installed qualification. Silently treating old artifacts as retained is not a valid fix. Restoring original suffix behavior for all retained inputs would be a mechanism redesign, not an ordinary seven-test correction.

## What can proceed without changing scope

- Complete exact R3 retained-profile behavioral evidence and investigate any substantive oracle failure. A proved value, metadata, bound, authority, or refusal defect warrants an ordinary contract-preserving correction in an isolated derivative.
- Preserve all original test bytes and failed receipts. Inspect/prepare a version-pinned dual-profile campaign without changing acceptance status.
- Verify the existing genuine legacy package and unchanged historical assertions separately. Existing legacy results are historical evidence until source and result identity are reconciled; they do not qualify S24.
- Prepare the versioned contract/test-applicability diff for review. Do not implement it as a skip, xfail, relaxed assertion, broad format allowlist, or special case keyed to the test.

## Completion and reporting requirements after a disposition

1. Record the exact owner decision or existing authority before changing literal test applicability or calling these failures resolved.
2. Retain the old ten-test file unchanged and execute its actual assertions against the genuine suffix executor, with explicit source/runtime/artifact identity. A mocked copy column or retained runtime that pretends to be old is insufficient.
3. Require the listed retained counterpart controls against the exact S24 installed candidate on both SQLAlchemy cells, with terminal JUnit, wrapper/preflight/shutdown receipts, source stability and corpus restoration. Reuse existing matching evidence where fully audited; do not repeat tests solely for documentation.
4. Preserve the current aggregate result verbatim. A dual-profile campaign can report distinct profile-qualified outcomes; it must not rewrite a prior `7 FAIL` aggregate as PASS or claim that S24 itself executed the old suffix algorithm.
5. A new aggregate selection must be explicit, complete for its declared profile, and reviewed. Profile-specific testing cannot erase broader legacy/generic-metadata requirements or convert UNKNOWN production gates to PASS.

The prior triage's `OBLIGATIONS_v1.md` remains useful and is not superseded as evidence. Its pre-R3 observations are not current terminal results. The root checklist records R3's aggregate interruption; this review makes no new test-pass claim.

## Reviewed source locations

- Root `CRYPTALIS_BUILD_CHECKLIST.md`, objective rows, S1W/S2/S5, S15/S17 and S24 entries.
- `reviewer-notes/s24-seven-baseline-failure-triage-20261014/OBLIGATIONS_v1.md`.
- `candidate-accel-retained-profile-observer-20261013/RETAINED_PROFILE_QUALIFICATION_MAP.md`.
- `checkpoints/CP40-positional-lifecycle-defect.md`, CP42, CP45, CP46, CP47, CP51 and CP73.
- Current candidate `AGENTS.md`, relevant README/canonical architecture/security/lifecycle/compatibility/status/decisions/build-guide/playbook sections, `src/cryptalis/deprotection.py`, and the original and retained test modules listed above.
- Original executable research mandate and continuous research mandate, authority and lifecycle sections.

No environment variables, credential files, raw configuration JSON, real data, keys, or secrets were read for this review.

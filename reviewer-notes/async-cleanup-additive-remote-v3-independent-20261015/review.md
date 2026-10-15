# Independent paired restore V3 source-only correction review

Date: 2026-10-15 UTC.

Decision: **ACCEPT_NARROW_V3_SOURCE_CORRECTION_FOR_SEPARATELY_AUTHORIZED_FRESH_RETRY**.

The exact V3 source is accepted for the coordinator's separately authorized retry into fresh suffix-v2. Independent static/data verification passed on its first attempt: 29 checks, exit0. No reviewed source, copied helper or preparation harness was imported, executed or called by this reviewer. No archive or failed-output payload was opened, and no actual restore was performed.

## Exact accepted artifacts

- Source: `reviewer-notes/async-cleanup-additive-remote-v3-preparation-20261015/restore_authenticated_paired_v3.py`
- Source length: 243,303 bytes
- Source SHA256: `60b7666952832ac2e1aba155d70cc1cb38c02968d71a5352c0e3281381640c59`
- Minimal diff: 1,877 bytes; SHA256 `2f14425231244e293352bf99ff3b16ec1c7858e1b6756e94b4fd81a4f13c8667`
- Sealed preparation `REVIEW_ARTIFACTS.sha256`: 1,307 bytes; SHA256 `29db67eba757d5cca33c990781ae5bc68f094d11aab78e0214756de06d265ceb`
- Supplied synthetic classification record: SHA256 `6f5b10064ac9648ed909aef1bdb9a174774f1c7f3c694362a39b86299d16029f`
- Preparation final-continuity record: SHA256 `38178249db4b28a03f63429062e6f345540bfd0396ae288c5be817dc4823b1d7`

The sealed preparation contains exactly the independently authored 14 files plus its checksum seal and two expected synthetic-fixture directories. All filenames, file kinds, bounded sizes, link counts, metadata and hashes were admitted. No checksum record expanded the read scope. All 22 review inputs remained unchanged through final continuity.

## Actual V2 failure and earlier review limitation

The coordinator's recorded execution observation is pinned at SHA256 `4ba463eede702af97e932ede435526cbc4979a3bb75a22f7c8a7e34ae751d2e1`. It identifies V2 source SHA256 `25a09641fe61a49d212fa8ce90f99a3d65af006ea394969d306da8c15086eee7`, tool session9646/chunk45e0ad, exit1, and `ValueError: Unadmitted toolchain path` in `verify_tree -> safe_name`. No success receipt was created.

V2 incorrectly sent the required real directory `logical-workspace/workspace/cryptalis-executable/toolchain` through the file-leaf name gate before inspecting its observed type. The prior independent static review did not identify that directory-classification defect. Its source/part and archive identity checks remain preserved; its static acceptance did not establish successful runtime restore execution.

Original stdout/stderr were returned by the execution tools and were not persisted as original local raw streams. The observation and incident record are expressly later attributed records, not fabricated raw logs. This reviewer did not inspect the preserved failed suffix-v1 output. The original source, original preparation seal and prior review/seal retain their exact hashes; none was rewritten. The failed attempt remains failed and preserved.

## Exact three-change boundary

An independent byte-level transformation and regenerated unified diff establish that the entire V3 source differs from the pinned V2 source only as follows:

1. `OUT` changes from `async-cleanup-full-source-additive-remote-paired-restore-v1` to the fresh `async-cleanup-full-source-additive-remote-paired-restore-v2` root.
2. `verify_tree` obtains `path.lstat()` before name classification and calls the new context-aware helper with the already computed expected directory set.
3. New `validate_restored_entry_name` contains one exact directory-only exception.

AST comparison independently confirms every existing assignment except `OUT` and every existing function except the narrow `verify_tree` call-site change is unchanged. In particular, `safe_name`, `nameset`, all part/member/provenance pins, authentication, archive header admission, payload checks, paired logical reconstruction, I/O safeguards, source views and `main` are identical to V2. No import or extra execution path was introduced.

The source remains subject to the prior accepted scope: exact additive355 and base516 members, 2,386 logical files, complete headers before member bodies, archive-only resolution, inert outputs and preserved qualification limits. The exact archive identities, all 24 remote-file identities, paired base provenance and all five external CLI-pin requirements remain unchanged.

## Directory-specific correction and complete expected closure

V3 lines2126–2134 implement the new helper. Its early return requires all three conditions:

- The supplied `lstat` mode is a real directory type
- The exact name belongs to the expected directory closure
- The exact name is `logical-workspace/workspace/cryptalis-executable/toolchain`

A regular file at that directory name reaches the unchanged `safe_name` gate and is rejected. Non-directory kinds cannot take the directory exception. An expected directory missing from the closure is rejected before any special handling. A different prefix, case variant, toolchain sibling or child cannot take the exact-name branch and still reaches the original prohibition. The exception does not change `safe_name` itself or admit live toolchain access.

`verify_tree` lines2246–2269 computes its expected directory set from the exact accepted filenames before walking outputs. It uses the actual observed `lstat` result. After the name helper, directory mode0700, single-link regular-file mode0600, every file body, exact file/directory closure and explicit empty-directory checks remain unchanged. Passing the name helper alone is not complete file or directory acceptance.

The reviewer independently derived the entire expected output namespace from the pinned 2,386-record logical resolution metadata and unchanged embedded member dictionaries, without opening archives or restored bodies. It contains exactly 3,909 data filenames and 358 directories, with no exact/casefold file/directory collision. The only directory containing a `toolchain` component is the one required parent. The only such files are the original two exact leaves:

- `logical-workspace/workspace/cryptalis-executable/toolchain/lab_progress.py`
- `logical-workspace/workspace/cryptalis-executable/toolchain/run_baseline.py`

The parent is absent from the file set, and both leaf names are absent from the directory set. No additional toolchain directory needs an exception. `EXPECTED_NAME_CLOSURE-v1.json` preserves the independently derived names.

## Supplied bounded classification evidence

The supplied harness was inspected as source, not rerun. AST comparison establishes that it copies precisely the four reviewed helpers `require`, `safe_name`, `nameset` and `validate_restored_entry_name`, plus the exact two deny sets. Its inert fixture is an ordinary file and a real directory, verified by metadata.

All 18 recorded cases match the corresponding harness case names and expected outcomes: the exact required directory with closure membership succeeds; file-at-parent and missing membership fail; both original leaf files succeed but cannot become directories; arbitrary toolchain siblings/children, unprefixed parent, case variation and extra prefix fail; ordinary expected file/directory cases succeed; unexpected directories and raw-phase, environment and traversal names remain rejected. Two additional recorded generic-gate checks keep both parent forms rejected as file names. Source preparation and classification exits are both0.

These are bounded helper classifications recorded by the preparer, not a new full restore test. The source preparation's historical `SYNTHETIC_TEST_PENDING` status correctly predates the separately preserved passing harness record and final-continuity receipt.

## Provenance continuity and retry conditions

The coordinator reports verification of all 24 actual remote bodies at final immutable commit `0c74347b6d89cfc82d766973e14d2450fd294032`. This review hash-checked its exact completed local provenance receipt at `3c822410850b54d23a83e468151bcf4d2af5f951585eba8d862f21436e4378e0`, reconciled the final commit/authenticated markers and all 24 individual size/SHA256/Git-blob identities against the unchanged source pins. It did not repeat network authentication or read/relabel the remote body files. The coordinator's actual-readback verification remains the external trust prerequisite.

The accepted base commit remains `86fb0e26ac4032a405b8c077939eb3e288e69db5`; its provenance and restore-receipt pins remain unchanged. No new base authentication claim is made.

At the read-only review check, the new suffix-v2 output root was absent. Before executing, the coordinator must recheck absence, exact reviewed source hash, the existing external provenance/commit pins and its execution authority. Preserve failed suffix-v1, use only fresh suffix-v2 and retain the new run's actual stdout/stderr and exit. A receipt alone is insufficient: require exit0 and the final output/input closure checks. Any further failure must remain preserved; pause before another checker repair or retry.

## Boundaries and review artifacts

Writes were confined to `reviewer-notes/async-cleanup-additive-remote-v3-independent-20261015`. No reviewed/archive code, actual restore, product/runtime test, build, install, database/server operation, Git operation, network call, publication or live-origin resolution occurred. No raw phase, secret, environment/cache or failed-output payload was read. Seven historical failures remain unresolved and all seven production gates remain UNKNOWN. This acceptance does not establish runtime qualification, a runnable environment, fresh-host/independent-builder reproducibility, physical release, release approval or production readiness.

The independently authored source-only checker, its first-attempt log and exit, exact external metadata admission, full expected-name closure, final continuity and 29-check summary are preserved here. `REVIEW_FILES.sha256` binds the final review artifact set, excluding itself. The previous review is unchanged; this review narrowly supersedes its V2 directory-classification acceptance for the fresh V3 retry.

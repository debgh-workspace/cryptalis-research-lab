# Statistics forced-present V3: source-only admission correction

Date: 2026-10-15 UTC.
Disposition: **PREPARED_SOURCE_ONLY_INDEPENDENT_REVIEW_HOLD. No execution admission.**

## Result

A fresh V3 packet corrects the V2 independent-action read-admission defect and strengthens analogous reads. V2 and the earlier failed packet remain unchanged. The final V3 requires a new independent source review before any coordinator selection or runtime action. Neither V3 `scope_guard.sh` nor `launch_sa21.sh` was invoked. Only shell source/data preparation, metadata inspection, named-file comparisons/hashing, JSON processing and bash syntax parsing occurred.

Authorized new roots:

- `experiments/statistics-forced-present-v3-20261015`
- `candidate-statistics-forced-present-v3-20261015`
- `reviewer-notes/statistics-forced-present-v3-preparation-20261015`

Immutable predecessor finding: `reviewer-notes/statistics-forced-present-v2-independent-20261015/REPORT.md`, SHA-256 `a3765ce4ac81a86cc3edececc81ea5d4a2284fa58f321723865b89d8195d41a6`. Its exact current bytes match the coordinator-confirmed final HOLD report. It identifies the original `INPUTS.sha256` comparison without local admission. That historical finding and packet were not edited.

## Correction and analogous independent reads

`scope_guard.sh` now has explicit full directory-component admission. Every ordinary payload target requires non-symlink directory parents and an ordinary, non-symlink, single-link file. The narrow two existing interpreter-symlink exceptions remain hash-only; their full parent chains and exact resolved target are checked. No interpreter was invoked.

- `original-safe-pins`, lines 136–146: locally admits both `ORIGINAL_SAFE_INPUTS.sha256` and the original packet's `INPUTS.sha256`, then the 261 targets, before awk, cmp or target hashes. It no longer depends on the success of another inventory/pin action.
- `overlay`: uses the independently frozen exact count 69, removing the separate pre-inventory `wc` read.
- Safe-input count is exactly 548. All target names/types are admitted before any target checksum verification.
- Enumeration failures emit a rejected metadata record rather than disappearing through process substitution.

`launch_sa21.sh` gives each independent read its own admission:

- `guard_action`: complete guard-source parent/type/single-link admission before hashing or invoking the guard.
- `queue_idle`: complete admission of the one fixed existing lock file before opening it. The unchanged wrapper still must acquire the real lock and fails closed on a race.
- `admit_named_source`: binds the exact source/list/destination tuple, independently runs that source's full inventory check, then admits the list and every source target. This happens separately for every copy or comparison.
- `admit_named_capture`: admits every expected destination file and all parents, then verifies the complete destination filename/type inventory before the first byte comparison. Extra files, extra directories, cache entries, links and unsupported types reject the action.
- `copy_named`: all source metadata is admitted before its first copy; copies only explicit named files; destination metadata is fully admitted before comparisons. Each immediate copy/comparison repeats relevant path checks.
- `compare_named`: completes source and destination metadata admission before its first comparison, then repeats immediate per-file admission. An earlier failed inventory cannot grant permission to this action.
- `capture_terminal`: admits both safe wrapper streams and the output destination before concatenation. It is now a separately captured, unconditional final action. The old unguarded terminal concatenation is removed.
- `check_safe_stop`: admits both complete safe receipt paths before either grep.
- `check_safe_corpus`: admits the full corpus-status receipt path before jq.
- Capture outputs, action-status appends, and summary writes check their destination parents and any existing file type. Invalid capture destinations fail closed. Each final action remains separately attempted; one failure does not short-circuit later final actions.
- A real nonzero runner exit remains the final exit even if later capture/admission fails. No expected failure is normalized to success.

`READ_ADMISSION_SOURCE_INDEX.txt` gives the final function/action locations. The six `*.delta.patch` files record the V2-to-V3 source/document changes. These are static source corrections, not dynamic fault-injection results. No unsafe target was created or opened to demonstrate a failure. Shell check/read sequences do not claim atomic containment against a concurrently hostile filesystem.

## Verified preservation and exact scope

Preparation independently admitted complete filename/type/parent inventories before any source copy or payload hash. It used the explicit authored path lists whose identities match V2's independent review; a checksum manifest was not treated as a payload read allowlist. External inputs were classified by exact named targets. Cache directories were inspected only as metadata and pruned; cache payloads were never read, copied or hashed.

Verified source/data checks:

- Original and V3 derivative source inventories: exactly 215 files each. V3 derivative is byte-identical to V2's derivative.
- Exactly one file differs from the original: `src/cryptalis/_statistics_diagnostic.py`; 214 are unchanged.
- Original changed-file SHA-256: `6534250833d3a2362f838a1574a5b0bdd028b8016a8502167539b6a41140f962`.
- Derivative changed-file SHA-256: `f2e8c43fcaf604c7be1d9dea63d1df30a4735daa643afbbbc9095eec66ec7568`.
- Actual labeled diff equals the original existing `mutations/forced_present.patch` and V3 `SOURCE_DELTA.patch` byte-for-byte.
- Original and frozen authored packets: exactly 38 files; each frozen copy equals its original.
- V3 packet inventory: exactly 69 files, with no cache payload.
- Original 261 safe pins pass; all V2 548 safe pins pass; all V3 548 safe pins pass; all V3 30 anchors pass. V3 JSON and checksum maps agree exactly.
- V3 candidate JSON/source maps equal actual source bytes. Original source/packet bytes are checked through their retained pins.
- All 215 V2 candidate files and all 69 V2 packet files match the before-preparation hashes.
- Oracle, five exact expected case identities and baseline evidence are byte-identical to V2. Expected wrapper154, runner153 and external6 path lists are also unchanged.
- Launcher `ARGV` source block is identical to V2. Its execution manifest differs only in V3 candidate/capture/evidence paths. Existing wrapper, roles, preflights, timeout, original external test packet, and sole function selector are unchanged.
- Both fixed V3 evidence destinations are absent. No queue, database or runtime action occurred.

The existing five-case prediction remains three assertion failures and two controls, 94 deselected, and actual pytest/wrapper exit 1. This preparation creates no runtime evidence or mutation kill. Complete setup/teardown, fallback, safe receipts, archive identities, explicit stop and corpus restoration still need independent actual-result review after any separately admitted execution.

## Exact frozen identities

These direct hashes identify the packet for independent review, not launch approval:

- `ANCHORS.sha256`: `1cf03b3b5ab0e806caf25cc24b5a60f4120991061e928ee02e56386fc6ff879c`
- `launch_sa21.sh`: `c41bb83e232de92d5285e94643cd2cfea04a54017cff27ea55810f54add4bb63`
- `scope_guard.sh`: `867c67cb6f4500e132302ce8777cf00fd59591178d58fcc3c28b8ffa10d35ca0`
- `INPUTS.sha256`: `0101954c27e1ee51f185e3290d537ab7cc60fccd8a1a69ed612e42690e5d4068`
- `INPUTS_MANIFEST.json`: `978a7f5f43f0e12c731b14d7c0b22cd4a572d404e55bfc9a3499ee293fa590f2`
- `CANDIDATE_SOURCE_MANIFEST.json`: `daa1117f5904a0a2d764797e69d050bf0c69af9ce3f02aed88ec46459a846a7b`

Proposed literal command, recorded only as review data:

```sh
bash /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/statistics-forced-present-v3-20261015/launch_sa21.sh --coordinator-selected-sa21 --anchors-sha256 1cf03b3b5ab0e806caf25cc24b5a60f4120991061e928ee02e56386fc6ff879c
```

Working directory: `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

## Preparation evidence and remaining holds

`prepare-v1.sh`, `PREPARATION-v1.stdout/stderr`, `freeze-v1.sh`, and `FREEZE-v1.stdout/stderr` are preserved. Both preparation helpers completed with exit 0. No failed preparation artifact was overwritten. The freeze output's `BASH_SYNTAX_PASS_NO_SCRIPTS_EXECUTED` shorthand refers to the two prepared packet scripts; the named preparation helpers themselves performed the documented shell data operations.

Supporting artifacts include the metadata inventories, V2 before/preservation hashes, original/V2/V3 safe-pin verification, anchor verification, actual source diff, source map, immutable V2 report digest, final direct digests and source-index/delta files. No post-freeze packet edit occurred.

No Python/package import, compilation, test collection, test, launcher, database/server/status/probe, network, Git, installation or runtime operation occurred. No raw `tests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, `postgres-stop.json`, secret, environment-dump or cache payload was read, copied or hashed. Original S23 and optional dependency environments remain reserved and were neither edited nor executed.

Independent source review is still required for these exact bytes. SA21 execution is not admitted by this preparation. No SA20, retry, other mutant, ordinary rerun, new privilege, cluster/role, ownership/RLS change, ANALYZE, package-free operation, deprotection, role retirement or Group D action is selected. Accepted ordinary G1–G6 remain 99 cases per cell / 198 total. All seven full gates remain UNKNOWN.

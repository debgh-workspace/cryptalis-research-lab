# Independent terminal review: ambiguous-COMMIT model V1

2026-10-16. **ACCEPT_CAPTURED_SYNTHETIC_RESULT_WITH_ENTRY_RECORD_LIMITS.** The retained, actually executed result passes the finite 22-case oracle. This is a terminal result review, distinct from the earlier source-only acceptance. The reviewer read captured files and parsed synthetic JSON as data; no model, driver, product, test, import, DB command or rerun was executed.

## Observed terminal result

Capture O = `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/online-ambiguous-commit-model-v1-root-20261016`.

- `exit-code.txt`: literal `0` plus newline, SHA256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`.
- `stdout.json`: **7,441 bytes**, SHA256 `324ca51267c55c0224556cb334fca46854c119e2f8c2aca0df551dd3fdf1ae53`. Byte-for-byte equal to the independently prepared pre-execution `EXPECTED_RESULT.json` in `reviewer-notes/online-ambiguous-commit-model-v1-source-independent-20261016`.
- `stderr.txt`: **0 bytes**, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Independently parsed exactly **22 distinct ordered result objects**, with the exact IDs, expected outcomes and actual outcomes of that prior oracle; all 22 `pass` values are literal true. All **66** `retry_authorized`, `closure_established` and `publication_authorized` values are literal false.
- Both exact negative controls have `rejected=true`: `empty_queue_means_success` rejects `CLAIM_EFFECT_OBSERVED` for `empty_without_stage`; `dirty_token_means_transaction_finished` rejects `ORIGINAL_OBLIGATION_OBSERVED` for `unresolved_original_dirty`.
- `inputs_unchanged=true`, `failures=[]`, and the reported model/case hashes exactly match the reviewed source. Acceptance is independently based on the complete oracle comparison, not only those driver's self-reported flags.
- Empty observations without a matching staged effect remain UNKNOWN; all three unresolved-original-transaction cases remain UNKNOWN even when dirty state or matching stage exists. The lower-token case makes no token-order inference.

## Selection, invocation and identity receipts

`selection.json` SHA256 `bcede541e91fca40ded0df869d1912fe2554b32d271ec1e5cbb51fe191af4969` records root selection, the exact source-review hash `feb1b40d0bf862968f9449ad7685878589aea5282af62f22fe8819aa921b050a`, synthetic-only scope, 10-second timeout and 128-KiB output limit.

`argv.txt` SHA256 `0415d1649d718754b29754dd91faefeca5dfa28a552d4d72d2d5ed552e8ef6a8` records precisely the reviewed host `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`, flags `-I -B -S -X`, `pycache_prefix=O/bytecode-absent`, and the one reviewed `experiments/online-ambiguous-commit-model-v1-20261016/driver.py` entry. No extra arguments appear. `cwd.txt` binds `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable` (SHA256 `dae0c590337cf29e1da98829552fd2ea5af13b6f2210767f1d1ed7eabb467331`).

`expected.sha256` (SHA256 `130e4cbe2868b0e136bc21b6e53d7817ba702edc323dcc3b649f2e93915fb464`) has exactly five admissions: interpreter plus `model.py`, `CASES.json`, `driver.py`, `MANIFEST.json`. Their expected hashes match the prior review. Both admission receipts contain exactly those five `OK` rows and are byte-identical, SHA256 `53f8d7e004e990c08075fe6fe0d444883f36b428cc49a646235d671eceac381a`. The reviewer also hashed the current five packet files; each matches the source-review identity. `O/bytecode-absent` was absent at this review.

## Limits on entry-control claims

The capture records four packet-file checks plus the interpreter, **not five packet-file checks plus the interpreter**. `PROPOSAL.md` is included by digest in the pinned manifest and still matches its original digest at review, but has no separate before/after admission row. It is not executed by the driver. This does not change the finite result, but the broader all-five-packet-files pre/post condition from the source review is not fully recorded.

Root subsequently retained `invocation-transcript-record.json`, SHA256 `2ee63ff9fe72f170ead5dda428f478f224a6ea614235347f5e04d8b58d2cd4d7`. It is explicitly a post-run transcription of tool chunk `439487`, not new execution or in-process telemetry. It records `env -i` with exactly the reviewed HOME/PATH/LANG/TZ values, the exact interpreter flags/entry/cwd, external `timeout 10s`, shell `ulimit -f 128`, returned exit 0 and tool wall time 0.099437494 seconds. Those values reconcile with the retained capture. The actual command uses a shell wrapper with quoted named-path variables, rather than the source review's proposed shell=false call. The file-size ulimit is not a combined-stream capture limiter; the actually retained combined output is nevertheless only 7,441 bytes, below the declared 128-KiB bound.

No renewed host-stdlib admission, separate timeout/overflow telemetry, or initial output-directory/prefix-absence receipt appears in these files. Root reports one run and absent prefix; this reviewer independently establishes current prefix absence, not its whole history. The transcript supplies recorded invocation evidence with its stated provenance, rather than an independent runtime monitor. These qualifications are not silently converted into full source-entry-control closure. No corrective rerun is requested by this review.

## Supported conclusion

The selected deterministic synthetic classifier produced the exact independently expected 22-case result and rejected both counterfeit conclusions. This establishes neither an actual lost COMMIT acknowledgement nor native transaction resolution, native isolation/concurrency, trustworthy observation/identity attestations, retry safety, liveness, closure or publication authority. No candidate promotion or change to the frozen preview follows. Existing native/permission/contract gates remain separate.

`INPUTS.sha256` binds the ten captured/transcribed files, prior source review and pre-oracle, and five current packet files. Only this fresh reviewer directory was written.

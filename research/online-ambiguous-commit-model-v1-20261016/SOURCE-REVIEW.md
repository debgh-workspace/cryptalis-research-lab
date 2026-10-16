# Independent source review: ambiguous-COMMIT observation model V1

2026-10-16. **ACCEPT_SOURCE_ONLY_FOR_FINITE_ROOT_SELECTION**, subject to the exact root entry/capture conditions below. No source correction is required for the sealed 22-case synthetic model. No model, driver, test, Python import, DB/status command or native concurrency experiment was executed by this reviewer.

## Exact packet and finite semantics

Packet: `experiments/online-ambiguous-commit-model-v1-20261016`, relative to cryptalis-executable.
- MANIFEST.json: `dd613ff24bfc213546e055150809d4efa0d5eee369437302b24f778c61349d9a`.
- model.py: 3524 bytes, `0e2a079102c496e613ef69ab4473a365e6373ff926c81cdc369be0dd414f5bc0`.
- driver.py: 2292 bytes, `1ead060d1505f9dacc9f542eb7c3fdb7707d66a610c67fa3e37f927192847638`.
- CASES.json: 14784 bytes, `bd46e233af1fb6c69983e1443bf9e3ef327d60b46df454f1d4ae687f3381d352`.
- PROPOSAL.md: 10078 bytes, `5ddf72cc43f3d1a5f02f338ac5a869c55dd706408c54b56b5700e58721a74cd4`.

All four manifest rows match actual named source/data bytes. CASES.json contains exactly 22 unique IDs. The reviewer read every input and manually reconciled each branch/expected outcome; parsing and arithmetic used only the synthetic JSON as data. EXPECTED_RESULT.json is a pre-execution oracle, never an actual result.

model.py:22–44 rejects incorrect exact members/types, bool tokens, nonpositive tokens, and inconsistent stage-presence evidence. :45–49 checks modeled operation/key/attempt identity and pin/PREPARING. :52–55 preserves UNKNOWN until original-transaction terminality and a coherent committed observation are assumed verified.

At :60–65, matching token plus matching intended effect and absence of that same dirty obligation yields only an observed claim effect; another dirty obligation remains named. It does not identify which worker committed, or resolve the original attempt as committed. :66–71 reports still-observed original/different obligations without token-order inference, and keeps empty state without matching effect UNKNOWN.

Every return uses result(): retry_authorized=false, closure_established=false, publication_authorized=false (:18–20). No path emits a retry, publication, switch, writer-admission or closure command.

The 22-case outcome partition is: two effect-observation cases; one original obligation; two different obligations including a lower token; two unmatched empty observations; three unresolved-original-transaction cases (dirty, empty, matching stage); four identity cases; two pin/phase blocks; one incoherent observation; two contradictions; three malformed evidence cases. Exact ordered IDs/outcomes are retained in EXPECTED_RESULT.json.

driver.py:28–41 has two negative-oracle controls. empty_without_stage must not become CLAIM_EFFECT_OBSERVED; unresolved_original_dirty must not become ORIGINAL_OBLIGATION_OBSERVED. These are comparisons against fixed counterfeit conclusions, not product mutants or fresh reproduction of a concurrent database schedule.

The modeled booleans are assumptions supplied by fixtures. No code establishes transaction identity/terminality, trustworthy pins, coherent/fresh native observations, intended frame/live/NULL/tombstone effects or isolation. A success cannot establish those assumptions.

## Driver effects and bounds

driver.py imports only hashlib/json/pathlib/runpy/sys. Its packet reads are model.py and CASES.json, with repeated reads for the final comparison. runpy executes exactly the named sibling model source, which has no imports/I/O. The finite loop creates in-memory result records, prints one JSON document to stdout, and exits 0/1. There is no network, DB, subprocess, file-write, provider or environment-read call in the driver/model. Interpreter/stdlib startup reads remain separate admitted host inputs.

The driver does not enforce the proposed 10-second or 128-KiB capture limits. Root must enforce them externally, retaining partial output and actual status on timeout/overflow. The independently assembled expected successful stdout is **7441 ASCII bytes including its final newline**. This is a source-derived expected size, not a measured runtime/RSS bound. Expected stderr is empty. Exceptions must remain failures, never be converted into expected outcomes.

The driver checks only the two input bodies after work, not its own identity, the manifest, or a continuous read trace. Root must pin and recheck all five packet files and freeze them against concurrent edits. Hash equality is scoped identity evidence, not supply-chain or continuous loaded-code attestation. No new custom audit guard is requested.

## Exact safe root entry/input/output scope

Definitions:
- W = /workspace/scratch/cb28ee9f5f4a
- B = W/cryptalis-executable
- D = B/experiments/online-ambiguous-commit-model-v1-20261016
- O = W/persistence-recovery-20261013/online-ambiguous-commit-model-v1-root-20261016

O is a proposed fresh exclusive capture path, not created by this review. Root must require it and its bytecode-absent child absent before selection; preserve any collision and choose a separately bound successor rather than overwrite.

Exact proposed argv, shell=false:
[
 "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12",
 "-I", "-B", "-S", "-X",
 "pycache_prefix=/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/online-ambiguous-commit-model-v1-root-20261016/bytecode-absent",
 "/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/online-ambiguous-commit-model-v1-20261016/driver.py"
]

cwd = B. Supply only this literal scrubbed environment, with no ambient merge:
HOME=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/runtime/home
PATH=/usr/bin:/bin
LANG=C.UTF-8
TZ=UTC

This reuses the previously reviewed direct-host startup pattern, not repo/.venv startup. The named interpreter's recorded SHA256 is fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7, exact size 30894944. Existing inert stdlib map: B/experiments/preview-doctor-dx-slice-20261015/proof-v2/STDLIB_SHA256.txt, SHA256 a57c71aec1c9ddaeda162e088e4b18d94fa1bf978d7ae506f20906abcf6a6132. Root must renew the applicable host-file admission before use; this reviewer read the map/pattern source, not live host payloads. The old proof's later HOLD is not acceptance of that proof route.

Root selection binds this review hash, all five packet hashes/sizes, host admission, exact argv/cwd/environment, limits and fresh O. The only new writes belong to O: immutable selection/invocation record, packet-before/after identity receipts, raw stdout.json, raw stderr.txt, actual exit/timeout/output-overflow and elapsed-resource capture. The model itself creates none. No toolchain/database wrapper, installed-cell namespace, corpus, credentials, fixture, source tree, dependency installation or old serializer probe is an execution input.

Keep bytecode-absent absent before/after. No -O, shell interpolation, site startup, PYTHONPATH, inherited package environment or additional argv. After one selected run, retain the first actual outcome. Failure/HOLD stops this selection; no automatic retry or repair follows from this review.

Terminal acceptance requires actual exit 0; no timeout/overflow; empty stderr; one complete JSON document with exactly the expected ordered 22 result objects, exact input hashes, both rejected controls, all 66 authority booleans false, inputs_unchanged=true and empty failures; external before/after packet and host checks; and absent bytecode prefix. Compare independently to EXPECTED_RESULT.json; do not trust only case_count or the driver's pass flags.

## Prior-source question and retained limits

The inspected unchanged fixture installers atomically stage and retire the exact token (_online_cf1_lab.py:160–183; _online_cf1_process_lab.py:75–97). The D4 process source:107–124 acknowledges only after outer COMMIT returns, explicitly excluding the ambiguous reply window. D5 documentation:10–26,60–76 explicitly separates empty observations from writer-schedule completion. Their named hashes match the proposal. This makes the new model question distinct; it does not transfer native transaction proof into this classifier.

No old serializer, native probe, D4/D5 or closure test is selected. No exact DB target/role authority, actual transaction observation adapter, native isolation/lock/concurrency behavior, closure, liveness, retry safety or online publication is established. Existing pending capture/handoff and PAUSED/finisher decisions remain outside this finite source acceptance.

Only this reviewer directory was written. Author packet, selected preview, product source and prior evidence remain unchanged.

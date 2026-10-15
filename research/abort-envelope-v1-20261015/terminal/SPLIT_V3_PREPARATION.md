# Split unit continuation v3: source preparation only

Status: READY FOR ROOT'S SELECTED ISOLATED UNIT ATTEMPTS. No worker launch, import, compilation, collection or test run occurred.

The incomplete original attempt and its terminal audit remain preserved. The audit is `UNIT_ATTEMPT_V2_AUDIT.md`, SHA-256 `fe3e942d2610220b6c4f3fec0058bb0de6dc3b2f411a613b451a73d63bf1f455`. One cursor method completed there; the boundary method was incomplete and seventeen methods did not start. SIGKILL did not establish a specific kernel cause.

## Fresh exact launcher

File: `UNIT_RUNNER_SPLIT_V3.py`.

SHA-256: `f9b36facdb5d208fd217f243152ac79642aa5bd5fb4b80fb33d63b1d1bd1e546`.

The launcher is 5,580 bytes. It is a new file; the original reference, original and correction tests, original nineteen-method launcher, and source acceptance are unchanged. Root must pin this new launcher and the three existing source hashes in each fresh execution receipt.

Source inspection confirms:

- Requires `-I -B -S` and exactly one explicit mode, `light17` or `boundary1`.
- Hash-checks and explicitly imports the same three sealed reference/test inputs, with no product, helper, plugin, database or network import.
- Loads the original nineteen methods before selecting, requiring nineteen total and unique full method IDs and the two expected partition members.
- `light17` selects exactly seventeen methods, excluding both the already completed cursor method and the incomplete boundary method.
- `boundary1` selects exactly the one incomplete boundary method. It also excludes the completed cursor method.
- Emits selected IDs and exact expected count before running; emits per-method start, successful-method, and return records. Return records include monotonic elapsed time, user/system CPU deltas and process peak RSS in KiB for the selected Linux runtime.
- A method-return resource record is not independently labeled a passing result. Passing requires the normal unittest success outcome. Partition success also requires its exact expected count, with no skips or expected/unexpected failures.
- Writes only stdout/stderr, makes no source writes, reduces no vector or data limit, performs no automatic retry, and does not impose its own resource limits. Parent terminal accounting remains necessary if the child is killed before it can emit a return record.

## Exact selected commands

Root selected interpreter remains:

`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`

Prior selected interpreter SHA-256:

`fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7`.

The reviewer did not reread or execute that interpreter. Root verifies it under its current selected execution contract.

Light command:

    /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 -I -B -S /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/reviewer-notes/aborted-successor-envelope-independent-20261015/UNIT_RUNNER_SPLIT_V3.py light17

Boundary command:

    /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 -I -B -S /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/reviewer-notes/aborted-successor-envelope-independent-20261015/UNIT_RUNNER_SPLIT_V3.py boundary1

## Root's selected resource questions

Root selected these bounds for preparation:

- light17: 30 CPU seconds, 60 wall seconds, 2 MiB per stdout/stderr file.
- boundary1: 240 CPU seconds, 300 wall seconds, 2 MiB per stdout/stderr file.

This selection supersedes the larger illustrative stopping-budget proposal in the prior audit. The bounds are finite selected-resource questions, not performance evidence or guarantees of completion. Root must record the exact CPU soft/hard settings it actually applies. If both equal the selected CPU value, a subsequent SIGKILL still requires careful interpretation with the captured resource accounting.

Use a fresh per-partition parent receipt and per-child wait4/getrusage accounting, retaining user CPU, system CPU, peak RSS and units even after signaled exit. Retain parent wall elapsed time, timeout flag, exit signal/status, exact stdout/stderr and source pre/post hashes. Do not infer memory consumption from JSON size, or infer a per-child peak by subtracting cumulative RSS maxima across unrelated children.

## Exact source-derived boundary work estimate

For the unchanged sizing fixture before adding filler, the schema is 58 compact bytes, the guard is 47, and the complete maximum is 489 canonical bytes with 27 candidate separator spaces. Thus the native-candidate base is 516 bytes. These values are hand-derived source arithmetic, not measured runtime observations.

The three native-candidate filler lengths are `16,777,216 - 516 + margin`, where margin is -1, 0 or 1. Each receives six full `string_width` scans: three through the outer maximum/measurement expression and three through the reservation check. The native group contributes `6 * 3 * 16,776,700 = 301,980,600` filler-character visits; the three margins cancel in the sum.

The three canonical filler lengths are `16,777,216 - 489 + margin`. Each receives three scans. This group contributes `3 * 3 * 16,776,727 = 150,990,543` filler-character visits.

The method therefore performs 27 near-16-MiB scans totaling 452,971,143 filler-character visits, plus small structural and baseline work. This explains why six boundary values are not six cheap length checks. It does not predict the exact CPU duration on the selected interpreter or prove why the previous process was killed.

## Terminal interpretation

If all seventeen light methods and the one boundary method complete successfully with unchanged pins, combine those receipts with the one completed cursor method from the preserved original attempt. Report nineteen individually successful methods across attempts, not a successful original nineteen-method invocation.

Any assertion failure requires preservation and a fresh authored correction. Any signal/timeout leaves that method incomplete; use the measured CPU/RSS and selected limits to assess the next decision without silently retrying, reducing inputs, or changing expected values.

No product, PostgreSQL, physical-journal/PK/ACL mutation, cutover helper, or v3 execution is admitted by this source preparation.

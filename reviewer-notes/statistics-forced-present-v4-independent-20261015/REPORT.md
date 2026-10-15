# Statistics forced-present V4: independent source-only review

Date: 2026-10-15 UTC.

Disposition: **ACCEPT the exact V4 source-only capture correction and command below for separate coordinator selection. No runtime selection, launch, or mutation-result acceptance is made by this review.**

The final pinned launcher fixes the missing jq option delimiter, makes required argv capture and its status logging fail closed before wrapper reachability, preserves primary failures, and prevents a filesystem-status output-admission failure from becoming false success. The initially missing synthetic admission-failure evidence was supplied and independently checked without changing V4 source. The completed V3 evidence-contract HOLD remains unchanged.

## Exact identities and accepted command

Working directory: `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

Independently computed final SHA-256 values:

- `experiments/statistics-forced-present-v4-20261015/launch_sa21.sh`: `2dd5890f2b81e69adf12eae7150cafff8bafe57d042ba8e442856a4eea6ec080`
- `experiments/statistics-forced-present-v4-20261015/scope_guard.sh`: `a82f663c2bb90d1ac799f8f83105d6d8a74009c33758d8764015668ff41d5620`
- `experiments/statistics-forced-present-v4-20261015/ANCHORS.sha256`: `f860257879d57b3f8739346a382b27fe29b542816146fd5aa75983d5c411e40f`

The exact accepted command, conditional on a later explicit coordinator selection and rechecking all three direct identities, is:

```sh
bash /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/statistics-forced-present-v4-20261015/launch_sa21.sh --coordinator-selected-sa21 --anchors-sha256 f860257879d57b3f8739346a382b27fe29b542816146fd5aa75983d5c411e40f
```

No substitutions, extra flags, alternate interpreter, broadened selector, retry, or second cell are accepted by this review. Both fixed V4 evidence destinations were absent at the independent source-verification snapshot. The command's own freshness and lock checks remain required at any selected invocation.

## Verified source and scope

Independent standard-library inspection established:

- Exact current inventories: V4 packet 69; V3 packet 69; V4 derivative 215; V3 derivative 215; original candidate 215; original authored packet 38; frozen original packet 38. Generated cache names were metadata-only exclusions. No cache payload was read.
- All 30 direct anchor targets match. All 548 safe input names, target types, SHA pins and JSON-map entries agree. All 261 original safe pins match and their checksum map remains byte-identical to the original packet's map.
- The 69-file V3 packet and 215-file V3 candidate preservation maps still verify. Every V4 candidate file is byte-identical to its V3 counterpart.
- Relative to the original candidate, exactly `src/cryptalis/_statistics_diagnostic.py` changes; 214 files are unchanged. The generated source diff is byte-identical to the existing original `mutations/forced_present.patch` and V4 `SOURCE_DELTA.patch`. Earlier UNAVAILABLE branches remain unchanged.
- All 38 frozen authored files equal the original packet. The V4 oracle is byte-identical to V3 and its external test source has the pinned hash. Exactly five unique parameterized identities agree across the case list, execution manifest and oracle: three expected assertion failures, two passing controls, 94 deselected and expected actual exit 1.
- The launcher has exactly the 16-element wrapper vector recorded in `MUTATION_EXECUTION.json`: unchanged corpus-v2 wrapper, fixed SA21 Python, V4 derivative and evidence paths, derivative test pythonpath, the original explicit external packet directory, and only `test_exact_aggregate_and_remedy_contract` with the existing flags. No role, runner, oracle or mutation change is introduced.
- The final launcher and guard deltas equal the supplied delta artifacts. The guard differs from V3 only in V4 version paths.

Filename, full parent-chain, ordinary-file and single-link admission preceded hashes. The only symlink exceptions are the two exact already-pinned interpreter links, checked against their literal and resolved ordinary target solely for hashing. Neither interpreter was invoked. Source inventories were admitted before candidate comparisons; all safe-input targets were admitted before their payload hashes.

## Capture correction and failure handling

The reviewed launcher has these properties:

1. At lines 178–182, `capture_wrapper_argv` locally admits its output and runs `jq -n --args '$ARGS.positional' -- "${ARGV[@]}"`. The delimiter keeps option-like elements as data and the quoted array preserves argument boundaries.
2. At lines 276–282, a separately recorded `before/wrapper-argv` action gates the wrapper. A capture/action-status failure increments `before_failures` and exits with the returned nonzero code before line 283 can invoke the array.
3. `run_action` retains each action's own code. A failed status writer emits a visible diagnostic; it returns the primary action failure when both fail, otherwise the status-writer failure. Initial capture writes and the direct runner-status write are also checked.
4. Every after-action has its own invocation and failure increment. An earlier failure does not short-circuit the remaining calls. Each real action retains its local admission requirements; failed earlier validation is not permission to read another payload.
5. At lines 217–220, filesystem-status output-admission failure increments `post_failures`, emits a HOLD diagnostic, and returns 2. A subsequent summary-write failure also increments the counter and reports its actual code.
6. The normal completion tail rejects nonzero `post_failures`. The EXIT handler likewise changes an otherwise zero outer result to 2, while preserving any actual nonzero runner code. Expected runner exit 1 is never normalized to success.

This is source review of the bounded correction, not a claim that a complete V4 invocation has succeeded.

## Synthetic evidence independently checked

The final argv/action-status harness is pinned to the exact final launcher. Its copied admission, `run_action`, capture function and gate fragments equal the live source. The persisted outputs are consistent with the five reported cases:

- Corrected success: exit 0, exact JSON array equals the standard-library baseline, inert wrapper marker present.
- Legacy missing delimiter: exit 2, `Unknown option --candidate-root`, empty argv output, no marker.
- Forced capture failure: exit 37, recorded action exit 37, no marker.
- Forced action-status writer failure: exit 41, valid argv JSON but visible logging failure, no marker.
- Primary and logging failure: original 37 retained over logging 41, diagnostic includes both, no marker.

This initial harness did not contain `after_all` or `finish`. That missing required admission-failure proof was raised before acceptance. The author then supplied a separate whole-function inert supplement. Its independently checked direct identities are:

- `SUPPLEMENTAL_COMPLETE_STATUS_RESULTS.json`: `ac82b81740f5b8a46076e454a7649eed8986b4fc520c1bfac4d283932f3995c0`
- `SUPPLEMENTAL_COMPLETE_STATUS.sha256`: `31cbcc96be7946641f401b27aa8f579af73d6e80f82ff38e4b8cfb940439c514`
- `SUPPLEMENTAL_COMPLETE_STATUS_HARNESS.sh`: `a01a7f9acf564ab805af57c92460d95de45c0c021fc1ad8f4e3dcf2b1d2bf626`

All 17 supplemental targets match. Complete copied `after_all` and `finish` bodies exactly equal the pinned final launcher. The sole callback replacement counts calls and returns zero without executing callbacks or dereferencing their path arguments. The output-admission replacement returns controlled 2 or 0; roots and runner statuses are synthetic data.

The four persisted cases show all 15 inert after-action calls, followed by:

- Success/runner 0: `after_all` 0, `post_failures` 0, shell 0.
- Admission failure/runner 0: `after_all` 2, `post_failures` 1, shell 2.
- Admission failure/runner 1: `after_all` 2, `post_failures` 1, shell 1.
- Admission failure/runner 37: `after_all` 2, `post_failures` 1, shell 37.

The failure cases retain the exact visible admission diagnostic and have no filesystem-status output. The real EXIT trap feeds outer status zero into the unchanged `finish` body. This closes the required counter/false-success/primary-preservation evidence gap. The normal completion tail and filesystem-status writer-failure branch were inspected statically; the supplement does not claim separate synthetic coverage of those branches.

The reviewer did not rerun either harness. Reported shell exits come from the author's retained subprocess results, whose generator source, assertions, body identities, manifests and persisted state/diagnostics were checked independently. No synthetic result is treated as a new mutation outcome.

## V3 remains completed and held

The existing V3 terminal report remains authoritative for that historical run: actual 3 failures at lines 104, 104 and 106; 2 complete controls; 94 deselections; 5 warnings; actual exit 1; recorded clean setup/teardown, fallback, stop and corpus preservation. Its required outer argv JSON is empty because jq rejected `--candidate-root`, and the prior launcher ignored that capture exit.

V4 does not reconstruct, replace, waive or retroactively repair the missing V3 receipt. V3's complete planned evidence-contract acceptance stays HOLD. The independently reviewed V3 source report is context only. This review read the retained V3 summary/report and verified its current packet/candidate preservation maps; it did not repeat the historical terminal-result audit or inspect raw-phase JSON.

## Reviewer evidence and limits

Reviewer outputs are confined to this directory:

- `verify_source.py`, `SOURCE_VERIFICATION.json`, `ADMITTED_METADATA.json`, and `attempt-03.*`: successful source/pin/scope and initial synthetic receipt verification. Its recorded evidence-gap status is the preserved pre-supplement snapshot, resolved only by the later supplement review below.
- `verify_supplement.py`, `SUPPLEMENT_REVIEW.json`, and `supplement-review.*`: successful final supplement review.
- `attempt-01.*` and `verify_source-attempt01.py`: preserved failure caused by the reviewer's wrong BASE assumption for the two relative V3 preservation maps. The coordinator authorized only the P3/C3 root correction.
- `attempt-02.*` and `verify_source-attempt02.py`: preserved failure caused by applying filesystem-name syntax to bracketed pytest identities. The coordinator authorized only parsing five unique exact case strings and comparing them to the original oracle. Actual file admission was not weakened.

No reviewed packet, candidate, historical evidence or source was edited. No full launcher, guard, product, wrapper, helper, test, database, server-status command, lock probe, network request, Git command or installation was executed. No product was imported. No raw-phase JSON, credential, environment or cache payload was inspected, copied or hashed.

If the coordinator separately selects the exact accepted invocation, stop after its one SA21 result for independent actual-result review. Require the complete argv and status captures, exact five-case outcome, current/archive wrapper154 and runner153 maps, external6, full source/capture equality, exactly one safe postgres-stop exit 0 plus `server stopped`, and independent prior-corpus restoration checks. Any missing receipt, capture, guard, setup, cleanup, shutdown or restoration failure remains HOLD. No retry or further cell follows automatically. Accepted ordinary G1–G6 and all privileged holds remain unchanged; all seven full gates remain UNKNOWN.

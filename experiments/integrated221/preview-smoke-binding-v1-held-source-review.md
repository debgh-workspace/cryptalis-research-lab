# Original installed221 public-smoke binding V1: independent source review

2026-10-15 UTC. Decision: **HOLD_SOURCE_ARCHIVE_GATE_NOT_FAIL_CLOSED**.

The exact new composition is not accepted for execution. One blocking source defect affects the required pre-execution archive. The cold-wrapper adaptation itself preserves the reviewed execution and authority boundaries. No prepared helper, shell entry, product import, test, database/status command, installation, credential/key operation, Git or network operation was performed by this reviewer.

## Exact reviewed identity

Packet: `experiments/preview-smoke-installed221-binding-v1-20261015`.
SHA256 of `SHA256SUMS.txt`: `479338f91be40df002e07c8656c92545440adfc10381320c625137e66da742f5`.

All 10 sealed packet members and all 39 `SOURCE-INPUTS.json` entries match their declared bytes after finite ordinary-file/no-symlink metadata admission. The packet has exactly 11 existing files including its seal. V5 has exactly the 15 files named in the safe source-input map; its four Python sources and all other declared files are unchanged. Accepted V5 source review remains `e8b49c407e0ece7a7ae8d92678908a9c509a816fba94179d8517ed3a8c665199`. Two additional exact safe files, selected from the already anchored main43 manifests, also verify: the accepted main-runtime source review `0ce0a286dbf8fbd049976dc37f8c8624043a70d03b5c34d9389b34f1f1296169` and unchanged runner `118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12`.

Reviewer-owned `SAFE-INPUT-VERIFICATION.json` and `ADDITIONAL-SAFE-INPUTS.json` record those checks. Metadata checks show `SELECTION.json`, `selection-support`, and `run` are absent. That observation is not future executable admission or quiescence proof.

## Blocking finding: archive construction is not a checked gate

`run-smoke.sh` lines 65–76 run `/usr/bin/jq` and `/usr/bin/awk` as process-substitution producers for three `while` loops. A producer's exit status is not the loop's exit status. A producer can fail with no output, or fail after partial output, and the loop can finish without the entry refusing. The existing `cp ... || exit` checks only copies for names actually emitted.

Lines 64–77 also lack a final exact destination inventory, file count and copied-byte verification. The unchanged runtime verifier checks the source files and its original packet, not the new archive directories. Consequently an incomplete or wrong-byte archive can precede independent status and the wrapper even when the original before/after runtime checks pass. Later independent terminal review could reject that evidence, but it would not restore the missing pre-mutation archive gate.

The intended V1 archive scope is finite:

- `source221`: all 221 source-manifest files.
- `v5-packet`: all 14 V5 sealed members plus its seal, 15 files.
- `smoke-packet`: all 10 V1 sealed members plus its seal and actual root selection, 12 files.
- `selection-support`: the two exact approved safe text records.

Total intended payload count: 250 files. This does not purport to archive every transitive member of the 39-input map or the full installed runtime. The unchanged original main43 maps/reviews remain separately pinned.

### Minimal required correction

Preserve V1 unchanged and prepare a fresh sealed successor. Use one admitted, hash-anchored data-only archive helper, or otherwise explicitly check each list producer. Require the exact approved archive sets/counts and each source/copy hash before any `pg_ctl` status or wrapper invocation. Admit all finite source paths/types before reading them; create new destinations exclusively; reject links, extra/missing members and byte mismatch. A helper must archive only declared safe source/manifests/selection evidence, never installed/corpus/cache/raw-phase bodies. Derive the successor's own packet count from its exact sealed membership rather than blindly copying V1's count.

Adding `set -e` or `pipefail` alone does not check process-substitution producer success. Terminal-only archive validation is insufficient for the pre-execution gate. Keep the separate unchanged runtime validator and its original binding unmodified.

## Shell utility scope

The new entry uses `/usr/bin/jq`, `/usr/bin/awk`, and PATH-resolved `mkdir`, `cp`, and `dirname`, as well as `/bin/bash` and `/usr/bin/env`. None of those host executable paths appears in the unchanged 3025-input union. The four-field root fixed environment makes PATH selection prescribed, but does not hash or admit those utility bytes. The accepted main43 report already excludes a complete host-process/stdlib attestation; this new utility dependency must be stated explicitly, not represented as a complete host freeze.

The simplest correction avoids the archive utility expansion by using a fixed-Python, reviewed finite archive helper. Any remaining host bootstrap tools stay an explicitly bounded host-tool limitation. Do not silently broaden the historic runtime binding or read unadmitted host/runtime/cache inputs to fabricate a stronger claim.

## Cold launcher and actual composition

The actual diff against accepted main43 `launch_cold_wrapper.py` matches the packet's declared delta. It preserves exact ordinary wrapper source/path/hash admission, source-loads it through `runpy.run_path` with a non-main name, reconstructs its script path/argv, verifies shared ENV object identity with both main globals and loaded `run_baseline`, and requires the original HOME/PATH/LANG/TZ key set. It requires `-B`, rejects assertion-disabling optimization, and adds bytecode suppression.

It adds exactly V5's existing three finite acknowledgement strings, then requires and propagates exactly the two accepted non-secret identity variables. These strings are not consent. The old V5 `coordinator_driver.py` remains unchanged and archived but is not invoked. The new route selects the whole exact V5 directory, preserving the four-file external Python snapshot and one intended test. Shell and COMMAND.json agree on coordinator, installed interpreter, candidate source, identity, evidence/private base, `--installed-candidate`, pytest config/directory, short traceback and fail-fast arguments. No direct pytest bypass, source overlay, `-s`, debugger, profiler or showlocals option was added.

Unchanged wrapper source retains the existing nonblocking exclusive lock, same provisioned server, two-role readiness and runner routes, installed-origin probe, progress/JUnit recording, and finally-path stop/corpus restoration. The runner refreshes its private role URLs and establishes the in-process preflight marker; the adapter still requires that marker. No new role/helper/admin route is introduced by this composition. No claim is made that source-file hashes continuously attest every loaded module or eliminate inherited host/startup limits.

## Finite runtime and corpus binding

The new route selects unchanged `verify_runtime_binding.py` hash `c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861` with exact SA21 binding `669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54`, in before/after read-only modes and without its old archive argument. No old suite entry/selection is invoked.

Independent data-only reconciliation of its accepted maps confirms 3025 unique targets, source221, 43 product modules per cell, 2506 ordinary installed files, 2402 complete nonproduct files and corpus26. It retains both main installed cells: SA21 111 directories/1255 regular files/four links; SA20 113 directories/1253 regular files/four links. Each has one opaque installer marker, metadata only. The maps retain the exact coordinator and two installed-interpreter chains. No current installed/corpus/cache payload was opened to derive those facts.

The unchanged guard checks complete installed names before expanded hashing, retains exact link and source sets, rejects new installed/cache names, and covers the complete candidate test/helper closure including `test_deprotection` -> `test_migration` -> `migration_commit_proxy`. The unchanged corpus helper includes both accepted receipt families and restores all declared primary identities. V5's stronger complete imported module-set/byte check remains in addition to the supervisor's installed-origin check. Package-free native `-I -S` workers retain the accepted exception.

Only original wheel `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6` is selected. The documentation successor is a distinct artifact and this route supplies no installed claim for it.

## Authority and execution remain HOLD

`AUTHORITY-PENDING.json` is still PENDING with `approval: null` for `Sentinel_d4be0bfc407881d19ce0ef871aa5304d`. The old cutover approval does not fill the fresh fixture-ACL slot. The identity receipt establishes owner/runtime/backend identity only; it does not establish plaintext-role provenance or lab_admin/helper authority.

Source admission verifies exact recorded root-selection/evidence identities and required booleans. It does not authenticate the approval, reviewer semantics, immediately preceding terminal closure, or exclusive lab ownership. Those remain root decisions requiring real source/command acceptance, actual fixture approval and exact scope reconciliation, safe existing-role/helper provenance, accepted preceding terminal evidence and fresh stopped/no-overlap admission. No selection/support files should be manufactured to make the template pass.

The source entry refuses before live runtime/corpus/database/status access when genuine selection is absent. Once corrected and separately authorized, it must still independently prove absent outputs/private base immediately before launch, preserve umask077/core0, perform one wrapper invocation, retain a failed exit, and accept no success that hides post-check failure. Stop success and empty-stderr independent post-status3 remain terminal-review requirements, not assumptions inferred from wrapper0.

No automatic retry, privilege repair, failed-fixture cleanup, private-file disposal, install or next-stage chaining is authorized. The V5 schema-scoped dump includes fixture data and is restored twice; its finite fixture effects remain those already reviewed. Failure may retain fixture grants and private recovery material. One future passing smoke could establish only a synthetic synchronous original-installed221 public-API composition, same-host/schema restore and same-process custody reopen. All 34 objectives and all seven broad UNKNOWN gates remain unchanged.

## Review custody

Only the nominated sealed packet, finite safe source/manifests/reviews, and accepted safe identity/authority text were read or hashed. No live installed tree, primary-corpus payload, raw phase JSON, environment/URL/credential body, cache body, private fixture artifact or database/status was read. Inert manifest parsing was not execution of prepared validation/archive/launcher code. The actual launcher delta was inspected without running it. Only additive reviewer-owned files in this directory were written. V1, V5 and all historical sources/evidence/authority remain unchanged.

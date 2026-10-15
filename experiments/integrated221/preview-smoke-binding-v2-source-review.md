# Installed221 public-smoke binding V2: independent source acceptance

2026-10-15 UTC.

Decision: **ACCEPT_SCOPED_INSTALLED221_PUBLIC_SMOKE_BINDING_V2_SOURCE**.
Execution remains **HOLD**. This is source/command acceptance only, not approval or an observed runtime result.

## Exact identity and preserved predecessor

Accepted packet: `experiments/preview-smoke-installed221-binding-v2-20261015`.
Packet seal, SHA256 of `SHA256SUMS.txt`: `9c18b202040b75219264b0e17a32d0ed09dc63a8c99b745d71291b4bdc6cdbec`.

All 11 sealed members and 42 explicit safe `SOURCE-INPUTS.json` entries match their declared hashes after complete finite ordinary-file/no-symlink metadata admission. The current packet has exactly its 11 members plus seal. V5 has exactly its 14 members plus seal. No `SELECTION.json`, `selection-support` or `run` is present.

All 10 V1 sealed members were independently reverified unchanged. V1 seal remains `479338f91be40df002e07c8656c92545440adfc10381320c625137e66da742f5`; its HOLD report remains `9af1c98b4833548c9eb3fd48a953c36852d6bc9cc8cd03ec6cdfeff461708860`. This report does not relabel V1 as accepted. All 39 prior safe input pins are retained unchanged; V2 adds only the V1 seal, V1 HOLD review and exact latest terminal review.

Critical V2 source hashes:

- `admit_smoke.py`: `c135fb94da3d011a1a7fb2a97c2d6abe0f3fcde6d8909d0c7eb17dfb8c7ed8ba`.
- `archive_smoke.py`: `87f34db5691695b71a75c203f5ddf9f3b0ae8eff3b1a0420595ad175522a7ff0`.
- `launch_cold_smoke.py`: `d8896e68795b5a50d7e49ce399adc4a5a82f71b1f6149b1d5511ef3528f7c9cc`, byte-identical to V1.

## V1 archive defect is corrected

V2 removes every jq/awk archive producer, cp/dirname archive operation and process substitution from the root entry. `run-smoke.sh` lines 61–65 admit the exact new helper before interpretation, invoke it once under fixed host Python `-I -B`, record its actual exit, and refuse on nonzero. This gate precedes the live runtime helper admission/invocation, independent pg_ctl status, and wrapper. It does not depend on `set -e` or unchecked producer exit propagation.

The new helper statically establishes the required fail-closed sequence:

1. Anchor the exact packet seal, exact V5 seal, source221 manifest and actual externally anchored root selection. Require exact packet/V5 member names.
2. Construct finite archive paths only for source221, the complete smoke packet, complete V5 packet and the two exact selection-support records. No installed/corpus/cache/raw-phase body is included.
3. Admit every expanded input path and all ancestors as ordinary files/directories, without links, before reading those payloads. Verify every original against its bound hash and retain its verified bytes.
4. Require the new archive root absent and its ancestor chain ordinary directories; create the new root and files exclusively. Existing output refuses; partial output remains retained on failure.
5. Enumerate actual directories/files without following links; reject links/special files and require complete exact directory/file-set equality. Verify every copied byte hash.
6. Only after those checks, write the exclusive safe `archive-receipt.json` and return success. A failed copy, inventory, hash or receipt write cannot produce a successful entry gate.

Independent inert-map reconciliation gives exactly:

- source221: 221 payload files.
- smoke packet: 13 payload files, comprising 11 sealed members, the seal and actual selection.
- V5 packet: 15 payload files, comprising 14 members and the seal.
- selection support: 2 payload files.
- Total: 251 payload files in 25 declared relative directories.

The receipt is outside `run/frozen-inputs`; it is not miscounted as a 252nd archived payload. This is a source-level verification of the prospective recipe. No helper was executed and no real archive was produced by this review.

The archive scope remains the declared safe source/selection scope, not a copy of the entire 3025-target runtime union. Terminal acceptance must independently inspect the actual archive receipt, exact sets and copied hashes. The helper does not authorize retries, cleanup or output replacement.

## Remaining host-tool boundary is explicit

The shell now uses absolute `/bin/mkdir` for fresh audit-directory creation. README explicitly retains fixed host Python/stdlib, Bash/env and mkdir as the bounded bootstrap/host-tool boundary and states that the 3025-target map is not a complete host-binary freeze. No new jq/awk/cp/dirname dependency remains. This addresses the V1 utility-scope finding without silently enlarging or rewriting the historic runtime binding.

## Composition and baseline remain unchanged

The actual V1-to-V2 source differences are the fresh packet/evidence/private paths, new archive member/helper and its checked gate, source-input history/predecessor additions, and exact latest-terminal enforcement. The launcher and pending authority document are byte-identical to V1. The actual shell and COMMAND.json retain the same coordinator, original installed SA21 interpreter, candidate source, installed mode, complete V5 selection, fixed identity variables and pytest options, with only fresh V2 destinations.

The cold source-loading launcher retains the reviewed main43 wrapper hash/path checks, `-B`, enabled assertions, shared ENV object identity and original four-key schema. It adds exactly the existing three V5 acknowledgement strings and two exact accepted non-secret identity values. The V5 coordinator driver remains preserved but is not the selected entry. No test, proposal, target guard, role helper or supervisor source is changed.

Unchanged runtime verifier `c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861` and SA21 binding `669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54` remain the original finite identity baseline, invoked before/after without their old archive option or suite entry. Their accepted inert maps still bind 3025 unique inputs, both main cold namespaces, 2506 ordinary installed files, 2402 nonproduct files, source221/clean source221, 43 product modules per cell, interpreter chains and corpus26. The full helper closure remains covered. This review did not refresh those facts by reading live installed/corpus payloads.

Existing wrapper lock, dual-role readiness/preflight, installed-origin checks, V5 full module-set/byte equality, progress/JUnit route and finally-stop/corpus restoration are retained. No direct pytest bypass, source overlay, debugger, profiler, showlocals, `-s`, installation, alternate database or new authority route is introduced. Inherited host/startup/loaded-code limitations and the two package-free native `-I -S` worker exception remain unchanged.

Only original221 wheel `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6` is selected. The documentation successor is not installed or qualified by this packet.

## Latest terminal is separate from runtime identity

The exact focused111 SA20 terminal review is independently hash-checked and semantically accepts its bounded installed run and closed stopped/restored boundary:

`reviewer-notes/integrated221-installed-focused111-sa20-v2-independent-20261015/REVIEW.md`
SHA256 `7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678`.

V2 binds it in SOURCE-INPUTS, RUNTIME-BINDING and the selection template, and explicitly enforces its exact path/hash at admission lines 113–114. The main43 SA21 binding remains an identity baseline and is not mislabeled as this current terminal. Root must verify no intervening task before actual selection and supply its semantic-verdict confirmation. A later terminal needs a fresh exact source binding, not silent substitution. The dated predecessor report alone is not future quiescence or permission.

## Unresolved execution gates

The fixture request `Sentinel_d4be0bfc407881d19ce0ef871aa5304d` remains PENDING with `approval: null`; its acknowledgement fields are not filled by this source acceptance. Old cutover approval cannot replace fresh fixture-ACL approval. Safe existing plaintext-role and lab_admin/helper provenance and exact approved scope still require root reconciliation; the accepted identity receipt proves only its recorded backend/owner/runtime identity.

Root must separately bind real approval/request message evidence, both exact safe support files, this actual source verdict, the exact current terminal and its semantic acceptance, and exclusive selection. Hashes and recorded booleans cannot authenticate consent or semantics. The pending template is not executable authority.

The entry still requires the actual selection before any audit/live-runtime/database/status activity, fresh absent audit/evidence/private-base paths including dangling links, umask077/core0, the checked archive, unchanged full runtime before checks, fresh independent pre-status3, and an immediate evidence/private-base absence recheck before the one wrapper call. Post-status and source/runtime checks run after a returned wrapper; wrapper failure is retained and success cannot hide failed post-checks.

Later terminal acceptance still requires exactly one intended node with passing setup/call/teardown, JUnit1/0/0/0, wrapper/readiness/origin success, exact unchanged source/runtime maps and safe archive, corpus26 restoration/no errors, explicit stop0/server-stopped and independent post-status3 with empty stderr. No automatic retry, privilege repair, failed-fixture cleanup, private-file disposal or subsequent stage is authorized. Raw phase/environment/credential/custody/policy/dump/cache bodies remain outside review.

The finite V5 fixture effects, schema-scoped data-containing dump restored twice, successful guarded drops and 22 retained private files are unchanged. Maximum future claim remains one synthetic synchronous original-installed221 public-API composition, same-host/schema restore and same-process custody reopen. All 34 objectives and seven broad UNKNOWN gates remain unchanged.

## Independent review record

`SAFE-INPUT-VERIFICATION.json` records the 53 packet/safe-input hash checks. `STATIC-CLOSURE-CHECKS.json` records the preserved input map, V1/member/launcher/authority identities, exact namespace sets, prospective archive counts and gate order. These are reviewer-created data-only checks, not execution of any prepared helper.

Only finite safe source/manifests/reviews, accepted safe identity and authority text were read. No prepared helper, shell entry, compilation, candidate import, test, database/status, install, key/credential operation, network or Git was performed. No live installed/corpus/cache or raw-phase/environment/private-fixture bodies were read. Only additive files in this distinct reviewer directory were written. V1, its HOLD review, V2 and all underlying sources/evidence remain unchanged.

# Original installed221 public smoke: concrete source binding, execution HOLD

Prepared 2026-10-15 UTC. This is an additive source-only packet. It neither runs
the smoke nor records approval. `SELECTION.json` does not exist. The fixture ACL
request `Sentinel_d4be0bfc407881d19ce0ef871aa5304d` remains PENDING.

## Preserved V1 HOLD and exact V2 correction

Sealed V1 is preserved at `experiments/preview-smoke-installed221-binding-v1-20261015`,
seal SHA256 `479338f91be40df002e07c8656c92545440adfc10381320c625137e66da742f5`.
Its independent review is
`reviewer-notes/preview-smoke-installed221-binding-independent-20261015/SOURCE-REVIEW.md`,
SHA256 `9af1c98b4833548c9eb3fd48a953c36852d6bc9cc8cd03ec6cdfeff461708860`.
The verdict remains HOLD_SOURCE_ARCHIVE_GATE_NOT_FAIL_CLOSED. V1 was not executed.

V1's three process-substitution producers could fail without propagating their
exit, and its copy loops did not verify final archive inventories or bytes.
V2 removes those pipelines and all jq/awk/cp/dirname archive utility use. A new
separately source-pinned `archive_smoke.py`, under the fixed host Python -I -B,
metadata-admits all finite source paths, verifies their hashes, creates the fresh
archive, verifies the exact directory/file inventory and every copied hash, then
writes a success receipt. The shell captures its real exit and refuses on any
nonzero result before live runtime validation, pg_ctl or the wrapper. Partial
archives remain retained; no automatic retry, deletion or success claim follows.

V2's exact archive has source221=221, complete V5=15, smoke packet=13 (11 sealed
members plus SHA256SUMS and actual SELECTION), support=2: 251 files total. Counts
are checked from the exact sealed sets, not accepted from a producer's output.
All expected destination directories are checked too, and symlinks/special files,
extra/missing files and byte mismatches refuse. No installed/corpus/cache/raw phase
payload enters the archive. The unchanged launcher bytes, runtime validator,
original221 identity and every approval/selection HOLD are preserved.

The entry still trusts the admitted host Python/stdlib, Bash/env and /bin/mkdir
for bootstrap/audit-directory creation, as the bounded host-runtime route does.
The 3025-target map is not a complete host-binary freeze. V2 adds no jq/awk/cp/
dirname archive dependency and makes no wider host-integrity claim.

## Exact target and minimal correction

The selected prospective runtime is the already-qualified original221 SA21 cell:
`release-lab/integrated221-installed-20261015/sa21/bin/python`. Original wheel SHA256
is `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6`.
The newer README-only package has different artifact identity and is not substituted.
This packet cannot establish an installed run of that later documentation successor.

The accepted V5 packet remains unchanged, including all four Python files. Its
source review is `reviewer-notes/preview-v5-installed221-independent-20261015/SOURCE-REVIEW.md`,
SHA256 `e8b49c407e0ece7a7ae8d92678908a9c509a816fba94179d8517ed3a8c665199`.
The same entire V5 directory, not just its test file, is selected for pytest.
Exactly one test is expected. The V5 driver is preserved and archived but is not
the executable entry selected by this new packet.

Simply filling V5's held command fields was insufficient: its driver calls the
older `toolchain/lab_session.py`, whose fixed ENV does not propagate bytecode
suppression and whose corpus family excludes the accepted master-s4 receipts.
The new `launch_cold_smoke.py` reuses the accepted main43 cold source-loading
pattern and unchanged `candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py`.
It requires -B and enabled assertions, keeps the shared four-field fixed ENV
identity check, adds PYTHONDONTWRITEBYTECODE=1, adds precisely the same three V5
acknowledgement strings and binds precisely the same two non-secret identity
variables to the accepted receipt. `SOURCE-DELTA.patch` compares it with main43's
accepted launcher and records the V1-to-V2 admission/entry correction. No supervisor, corpus helper, exclusive lock, role preflight,
test runner, smoke proposal, target guard or installed221 package source is edited.

This is a changed composition requiring its own independent source/command review.
The original main43 acceptance alone does not accept the added smoke guards or
authorize the finite fixture action. The unchanged corpus wrapper deliberately
protects both admitted corpus families rather than inheriting the older driver's
narrower scope. No new corpus target or alternate database is introduced.

## Concrete finite runtime admission

`RUNTIME-BINDING.json` binds exact accepted map/report identities, not new live
observations. `SOURCE-INPUTS.json` contains finite safe source/manifests/reviews
and the accepted non-secret identity. It contains no installed-cell payload or
primary-corpus payload. No live cell or corpus was read in this preparation.

The source route reuses, unchanged, main43 `verify_runtime_binding.py`, hash
`c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861`, with its exact
existing SA21 binding hash
`669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54`.
It is invoked only as a read-only validator, before/after the smoke, without its
old archive option. No main-suite stage entry or old execution selection is run.

That validator checks its complete 3025-target input union, both installed cold
namespaces, all 2506 ordinary installed files including 2402 nonproduct files,
both exact interpreter chains, source221 and clean-source221 sets, 43 product
modules per installed cell, RECORD/payload receipts, unchanged accepted harness
and all 26 declared corpus identities. Its current semantic conditions are not
weakened. An extra installed path/cache, changed file/link, changed corpus or
changed source fails. Product-owned uv_cache.json stays metadata-only. Installed
origin and full module set/byte equality are additionally asserted by unchanged
supervisor/V5 code at execution. No source-overlay installation claim is possible.

This intentionally retains the main43 validator's SA20 check as well as SA21;
it avoids inventing a reduced freeze. The complete exact test/helper closure,
including test_deprotection -> test_migration -> migration_commit_proxy, is covered.
Same-host dependency provenance and the accepted startup/host-stdlib limitations
remain. The two package-free -I -S native workers retain their existing exception;
there is no continuous loaded-code or clean-host attestation claim.

## Three separate gates

1. Independent source/command acceptance of this exact new seal and route.
2. Real explicit fixture-ACL approval to the still-pending request, plus root's
   reconciliation of the separately approved unchanged cutover helper and safe
   provenance of the existing plaintext role and lab_admin route. The old cutover
   approval cannot fill the fresh-fixture approval slot. The historical identity
   receipt only proves owner/runtime/backend, not plaintext/admin provenance.
3. Root's actual exclusive selection after the immediately preceding task's
   accepted terminal closure, fresh stopped-server proof and absence of outputs.

The current terminal prerequisite, supplied by root after independent closure, is
`reviewer-notes/integrated221-installed-focused111-sa20-v2-independent-20261015/REVIEW.md`,
SHA256 `7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678`.
It is bound separately in the safe source map, selection template and admission
check. The original main43 SA21 binding remains the installed identity baseline;
it is not represented as the latest terminal. Root must confirm no intervening
task before actual selection. A later terminal requires a fresh source binding,
not silent substitution in this exact prerequisite. Fixture approval remains null.

`AUTHORITY-PENDING.json` preserves the unresolved approval honestly.
`SELECTION-TEMPLATE.json` is not executable admission. After real evidence exists,
root may create a separate additive `SELECTION.json` plus the two exact safe text
files under `selection-support/`. Preserve the template and every sealed input.
The ACL evidence file must contain the actual request and affirmative user reply,
with exact message IDs; never credentials. The provenance file must identify the
existing roles/helper and source evidence without URLs/passwords or private files.
Bind the actual independent source review and immediately preceding terminal review
by safe path and SHA256, with explicit root semantic-verdict confirmation.

The selected status is `SELECTED_BY_ROOT_AFTER_EXPLICIT_APPROVAL`; all nulls and
false acknowledgements must be resolved from genuine evidence, not copied from
historical unrelated successes. The verifier only checks recorded selection and
file identities. It cannot authenticate user consent or infer reviewer semantics.
Those decisions belong to root and its independent reviewer. No driver token,
digest, manifest or README assertion supplies permission.

## Exact root handoff, not an instruction to execute now

`COMMAND.json` gives fixed environment, cwd, exact interpreter/argv, original wheel,
identity, evidence, audit and private-base destinations. The only unresolved entry
arguments are the actual external SELECTION.json and packet-seal hashes. Root must
verify this exact shell path/type/hash before invoking it. Capture the outer entry
stdout/stderr and exit independently; an early refusal is retained there.

`run-smoke.sh` first admits the finite helper source, seal and genuine selection.
Without SELECTION.json or with the pending template it stops before any live cell,
corpus, database/status or new audit activity. It then enforces private umask077,
core-size0 and absent audit/evidence/private-basetemp (including dangling links).
The checked archive producer must complete its exact 251-file source archive before
the unchanged complete runtime guard is invoked. It records independent exact-target pre-status3 and rechecks absence
immediately before one wrapper invocation. It uses --installed-candidate, enabled
assertions, no source overlay, no -s, no debugger/profiler/showlocals and no direct
pytest bypass. The supervisor supplies the existing runner/preflight/progress/JUnit
routes. It acquires the unchanged exclusive lock and stops the same provisioned
server in its finally path. Root alone controls no-overlap task selection.

After a returned wrapper, the entry records independent post-status, readmits its
source/selection and unchanged runtime helper, and performs the full after check.
Any wrapper failure is retained; a success cannot suppress a post-check failure.
There is no retry, automatic privilege repair, cleanup after failure, corpus edit
outside the unchanged wrapper, new install or subsequent task chaining.

If the source/namespace/corpus baseline has changed after focused111, stop for a
new exact admission. Do not edit the historical main43 binding to accommodate it.
Current fixture permission, exclusive selection and the preceding boundary must
be reassessed at selection time; today's stopped state is not a future guarantee.

## Required terminal review and bounded claim

Accept only one exact node with setup/call/teardown PASS, JUnit1/0/0/0, wrapper0,
dual-role readiness0, installed-origin0, exact unchanged before/after maps and
source archives (archive-exit0 and exact251-file receipt independently verified),
corpus26 restoration/no errors, explicit postgres-stop0 with
server-stopped log and independent post-status3/empty stderr. Review safe receipts
only, never raw phase JSON/environment/credentials/custody/policy/dump/cache bodies.
Passing capture may hide the proposal's safe print; do not add -s or invent it.

Clarification retained from V5 review: the one backup is a schema-scoped pg_dump
including fixture data, not pg_dump --schema-only. It is restored twice. On full
success, three guarded fixture schema drops occur (two restores and cleanup).
The 22 private retained files remain outside evidence; disposal is not authorized.
Failure may leave fixture grants and private recovery material; preserve the
stopped boundary and seek the exact recovery decision rather than rerun or repair.

Maximum future claim: one synthetic synchronous original installed221 public-API
composition, same-host/schema restore and same-process custody reopen. This is
not fresh-process/provider/full-application/production qualification. All34
objectives and all seven UNKNOWN broad gates remain active.

## Preparation custody

Only additive files in this fresh packet were written. Work consisted of safe
source/map/report reads, static source construction and hashes/diffs. No prepared
Python or shell helper, candidate import, compile, test, package build/install,
database/status command, key creation, credential read, network or Git action was
performed. No live installed-cell or primary-corpus payload was read. Runtime
absence/quiescence and all executable validation remain future root gates.

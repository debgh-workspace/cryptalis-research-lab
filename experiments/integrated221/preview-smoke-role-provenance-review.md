# Smoke V2: bounded role and helper provenance

2026-10-15 UTC. Source/evidence-only reconciliation.

## Result

**HISTORICAL_EXISTING_ROLE_ROUTE_CORROBORATED; CURRENT_PLAINTEXT_IDENTITY_CONTINUITY_NOT_ESTABLISHED.**

The exact helper and existing-role reader selected by accepted smoke V2 were used by the accepted installed-focused111 SA20 positive-activation case. The helper is source-bound to `lab_admin`, loopback port 55432, and `cutover_procedure(create_role=False)`. This is evidence of a previously exercised existing-role route. It is not a current database observation, an exact historical plaintext-role-name receipt, or approval for the smoke.

V2 execution remains HOLD. No approval, selection, selection-support file, runtime output, role/grant/cluster change or live check was produced. `SUGGESTED-PROVENANCE.txt` is proposed safe wording outside the sealed packet, not an executed selection support record.

## Accepted anchors

- Smoke V2 seal: `experiments/preview-smoke-installed221-binding-v2-20261015/SHA256SUMS.txt`, SHA256 `9c18b202040b75219264b0e17a32d0ed09dc63a8c99b745d71291b4bdc6cdbec`.
- Accepted V2 source review: `reviewer-notes/preview-smoke-installed221-binding-v2-independent-20261015/SOURCE-REVIEW.md`, SHA256 `a185aefc69cd3f89f52ca70c356e93067fe8abc0ab3e0995946ec1326e61fdad`. It accepts source/command composition and explicitly preserves authority/provenance/selection HOLDs.
- Latest supplied terminal: `reviewer-notes/integrated221-installed-focused111-sa20-v2-independent-20261015/REVIEW.md`, SHA256 `7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678`, verdict `ACCEPT_SCOPED_INSTALLED221_FOCUSED111_SA20_TERMINAL`.
- Its immutable binding: `experiments/integrated221-installed-focused111-runtime-v2-20261015/BINDING_SA20.json`, SHA256 `b6bf904e2efe3e9a5ec28118e8ed2d3b0f76cf4085153e6bcaad1024263daec5`.
- Existing cutover approval: `experiments/cluster-designation-correction-supplement-v2-20261015/ACTIVATION_APPROVAL.txt`, SHA256 `ce641ec0edb672f4350060cf75ebbd08a9ccd89cee818c107a4a02039980489d`. It preserves request `Sentinel_a0257be8536481d19adf0f2b6dc52ede` and reply `Sentinel_3ffede9ae0a081d1bedf0655efef54bd`. It describes the unchanged helper, existing test roles, local 55432, grant changes and possible termination of sessions able to assume the old runtime role; no new role or credential. This review does not reinterpret it as generic or standing grant authority.

All paths here are relative to the supplied B unless stated otherwise. `SAFE-READSET.json` records exact current safe-file hashes. `SOURCE-EVIDENCE-CHECKS.json` records the bounded joins; no manifest was expanded into runtime, corpus or private files.

## What the source proves

1. Current candidate `tests/test_deprotection.py`, SHA256 `c6efb4e2643551f746390288e91eda1fcbd896bf811bfe0f830cc33c65073ca6`, contains the unchanged reader `plaintext_url` / `plaintext_role` (lines 37–44), helper `retire_old_role` (47–56), and `execute` dispatch (71–74). The helper derives database options from the owner runner route, requires literal host 127.0.0.1 and port 55432, substitutes the existing `lab_admin` authentication route, connects with autocommit, and executes the plan's procedure with `create_role=False`. No private reader target was opened in this review.
2. Current `src/cryptalis/deprotection.py`, SHA256 `de1a3dadd276cfce204c18d74aa62dff3828caff2eef7ef8103f316d4880e6d6`, lines 86–88 forwards that flag, the plan's plaintext role and frozen inventory to `cutover.procedure`. Current `src/cryptalis/cutover.py`, SHA256 `bef95a5d97b256ea1fa56565fcb9e1a1d2786748757777cf366b453d3cf42783`, lines 105–150 omits role creation when that flag is false. Its branch emits existing-role fixture grants, old-runtime/PUBLIC write revocations and the disclosed same-database session-termination query. The general generator can also render inventory-driven remediation; V5's stricter inventory filter is essential and cannot be dropped.
3. V5 `test_public_preview_smoke.py`, SHA256 `2d52d488649c7a34332b8cf6aa363a7c6fd1802d53f2a4fd63313bd17843513b`, imports that exact reader/helper (75–87). Its cutover callback (255–297) checks frozen and fresh scope, allows exactly one keyword-only autocommit admin connection, requires user `lab_admin` and the accepted database, proves actual connection identity before privileged SQL, restores the intercepted connect function, checks unchanged non-fixture security facts, and requires fresh readiness.
4. V5 `target_guard.py`, SHA256 `6deaa0ff8b94c043ca742df0ffffe56fc5a5bc66709e2ede6ea8fcd7e4439ac4`, admits exactly five connection-option fields, literal loopback 55432 and the accepted backend identity. It binds owner/runtime names to the accepted identity file. It derives the plaintext name from the existing reader, requires it distinct from owner/runtime, and verifies current/session identity through Python and psql. Its cutover filter (179–195) admits only the exact fixture customer-table old-runtime write path and missing plaintext CRUD. Direct memberships and every other finding, including administrative/ownership/routine/default-ACL paths or old-role sessions, refuse before the helper.

These are static findings. None of these helpers, identity queries, database connections or SQL statements was executed by this review.

## What actual prior evidence proves

The installed-focused111 SA20 case is exactly:

`successor39/test_designation_supplement.py::test_approved_plaintext_activation_and_active_recheck_preserve_designation`.

It is the final ordered case. The control source SHA256 is `3011858804c44d47046cd278240a17358cbe5c0951dc56f4f720cc7719a5341b`; its support source SHA256 is `603012b83c1942ce5c100543e378e4f552ce07201530ce1badfbea8f537cdb7a`. The support imports the current candidate `test_deprotection`; the autouse source/origin fixture checks that exact module path. Lines 270–295 call `backward.execute` once with `PLAINTEXT_ACTIVE`, which invokes the helper, then use direct public apply for completed-state rechecks rather than repeating cutover.

The accepted safe receipts were rehashed and joined to the accepted review's audit maps:

- Progress SHA256 `e35e3496b82a23ca9ee614de9ee997fee7385cd820b0d3ba1fafc667bae49e71`: exactly one start and passing setup/call/teardown for this case, in the final position.
- JUnit SHA256 `ee87cd0b78c4cb9efbce3a80e20b31773737f006c61070992e7905b2b6c9a15f`: exactly one passing testcase for this name. Its classname is empty; the full source path comes from the pinned ordered selection and source/origin checks, not from a path in the raw testcase.
- Supplement observations SHA256 `1cca5ca5c6139f5eee204ce414918854821dbd53b4aaacc0189d518d7c10aac8`: the matching final record has SQLAlchemy 2.0.51 and ten strictly true checks. These include reaching PLAINTEXT_ACTIVE through the approved existing helper, exact current values/native metadata, retired reverse fence and successful completed-state/recovery checks. They are boolean observations, not raw identity/catalog dumps.
- The accepted `TERMINAL_CHECKS.json` SHA256 `aa7a84d4c29c2fa8d3f90d3918e9a86cb720c4e660c9e4708646f6f6d5474e55` binds source, selection, progress/JUnit and readiness hashes. `CHILD_OBSERVATION_CHECKS.json` SHA256 `1fce14d43107aa9a8ed1b1885192d48d2dff1e99bf0b0105fa7f0d22c42e7bf8` and `CHILD_READSET_SHA256.json` SHA256 `fa45c7e7d50ab2fb95b3cdb70c272894293118214f4263c04c9debed230c81a0` bind the exact supplement observation bytes.

Earlier source-focused corroboration is separate: `reviewer-notes/cluster-designation-correction-independent-20261015/supplement-v2/REVIEW.md`, SHA256 `0052a0ba168267cb3dfb13052cffda5483cc94259cba811db2d036910772e7fa`, explicitly reviews the same bounded helper route and once-only positive call. Its `terminal-sa21/REVIEW.md`, SHA256 `ed83c4bccd6b42b66180df61103e9adcfd28dba1101e867f89d3a5d36cf0effd`, accepts 39 source-candidate cases and explicitly reports that helper reaching PLAINTEXT_ACTIVE. This older source result is not substituted for the current installed terminal or for current identity proof.

## What the preflight and identity receipt do not prove

The selected installed-focused111 and earlier installed-main SA21 readiness logs both have SHA256 `650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08`. They report successful probes with fingerprints `76053d5b` and `a38ab71b`. Pinned `scripts/test_postgres.py`, SHA256 `118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12`, reloads and probes only owner/runtime routes. Those fingerprints are truncated URL fingerprints, not plaintext/admin identity attestations, and matching fingerprints are not full credential-continuity proof.

`evidence/preview-identity-capture-v3-sa21-20261015/safe-identity.json`, SHA256 `089bac088003d7921f755409509afed5544741ebfee8af66faea0776fbfbb92c`, records 127.0.0.1:55432, database `cryptalis_lab`, database OID 16388, owner `cryptalis_owner` and runtime `cryptalis_runtime`. It contains no plaintext or admin role entry. Historical successful helper execution corroborates a functioning `lab_admin` route then; no current admin-role attributes, credential provenance, role OID or uninterrupted role identity are independently attested here.

No admitted exact plaintext-role-name receipt was found in this finite selected evidence set. No name is guessed. The fact that the same reader source is selected does not prove its private input is unchanged. V5's current plaintext identity comparison uses the value read for that run; it does not compare it to a historically pinned plaintext name or role OID. Fresh authentication and readiness prove the current selected role exists and satisfies the checked conditions; they cannot retroactively establish historical continuity or supply consent.

## Limited use and remaining gates

This evidence can support the narrow statement: “The smoke reuses the exact previously exercised existing-role reader and lab_admin helper route; actual current backend/users and the permitted fixture-only effects remain subject to fresh checks.” It cannot support “the historically named plaintext role has been independently proven unchanged and currently authorized.” Whether the narrow route-based provenance meets the specific existing-role referent of the prior approval is root's explicit scope decision. This document does not make that decision or turn a broader provenance acknowledgement true.

Before any eventual action, root must still resolve:

1. Real explicit approval for the fresh fixture ACL request `Sentinel_d4be0bfc407881d19ce0ef871aa5304d`. Its packet status remains PENDING with approval null. The old cutover approval does not fill it.
2. Exact reconciliation of the old helper approval with the proposed one-smoke action and the existing role targets. If exact role-name continuity is required, obtain admissible non-secret evidence under separately authorized safe observation; do not infer it from these logs, inspect private files, or silently accept a changed target. A material target or privilege change requires its own action-time permission.
3. Fresh unchanged input admission, root-only exclusive selection, no intervening task after the exact supplied terminal, stopped-server proof and absence of outputs. Historical stopped-state evidence is dated, not future quiescence.
4. On an authorized run, unchanged dual-role preflight plus all owner/runtime/plaintext Python/psql identity checks; the sole `lab_admin` connection identity check before privileged SQL; frozen/fresh inventory and no-live-old-session checks; same non-fixture security boundary before/after; fresh post-helper readiness. No automatic remediation, role creation, reconnect race acceptance or retry follows a failed check.

Any later completion claim must still pass V2's exact terminal/archive/runtime/corpus/stopped-boundary review. Original installed221 only; no wider capability or release claim. All 34 objectives and seven broad UNKNOWN gates remain unchanged.

## Review custody

Only finite selected safe source, inert maps, accepted reviews, safe logs/progress/JUnit and boolean observation records were read. Ancestors and files were metadata-admitted as ordinary paths before expanded reads. No private reader target, credential, URL, runtime-home content, raw readiness/tests/package-origin/postgres-start/stop JSON, live installed cell, corpus, cache, ambient environment or private fixture was read or hashed. No prepared helper, import, compile, test, status/query, package operation, network or Git action was performed. Only this new reviewer directory was written; the sealed packet and all prior evidence remain unchanged.

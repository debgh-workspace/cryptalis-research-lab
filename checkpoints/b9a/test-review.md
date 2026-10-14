# B9A frozen-test review

Status: SOURCE-INSPECTED. No PostgreSQL connection, test execution, Git command, implementation-module read, or candidate edit. Only this review directory was written. The root reports the initial RED as one expected ModuleNotFoundError in 0.39 seconds; that establishes feature absence only.

Frozen test: `tests/test_payload_rotation_journal.py`, SHA-256 `5e8db1d91ed20cfd2856d2107d2969eea091f5340e2abc3e897941d8091c322e`. All 208 base-file hashes match the supplied S20 provenance inventory. See EVIDENCE.json for the exact 16-case inventory.

## Decision

The frozen file is a useful minimum integration harness with independent native observations, an independently implemented decoder, real process death, and an actual transport fault. It does not by itself establish every entry-algorithm invariant in NEXT_SLICE.md. A GREEN report must retain the narrower evidence boundaries below. Do not treat an implementation that merely satisfies the tests as a complete implementation of the reviewed contract.

Root should address the deciding-oracle and bounded-cleanup gaps before declaring the full bounded contract VERIFIED. The implementation review remains separate: this review intentionally did not inspect the changing experiment module.

## Priority and execution recommendation

No deterministic executable failure is established by this source-only review. The frozen tests can proceed to the root's limited in-process positive GREEN. Do not read this report as a finding that the unseen implementation is defective.

- Blocking full subprocess containment qualification: the partial-line timeout and exceptional cleanup gaps in finding 3. Correct containment separately before treating the crash/restart family as safely bounded.
- Implementation-boundary caution: finding 2 requires trusted test-callback scoping or a post-callback final check. The supplied callbacks do not demonstrate an actual bypass, and arbitrary hostile host callbacks are not an admitted threat model.
- Narrower evidence limitations: findings 1 and 4–7. Do not inflate claims; additional deciding tests are necessary only for the stronger claims. For UUID equality, a valid changed plaintext normally changes its term. No valid same-term/different-text fixture is demanded. An explicitly declared diagnostic omission control is one possible way to isolate verifier causality, outside this frozen review's execution scope.

The exact-fit budget case already repairs the initial-NULL concern: lines 485–490 change UUID100 to a 263-character ASCII string before computing its cost. The first row is deliberately the maximum-cost frame; its budget is not the NULL identity-only cost of 32 bytes. Later shorter non-NULL rows can satisfy conservative per-row admission. This case is not an identified failure.

## Important findings

1. **Value-comparison causality is incomplete (lines 418–436).** The valid-value mutation adjusts the stored target commitment, which correctly defeats a stored-hash-only check. However, sealing a different equality value changes its search term too. Exact source/target search-header comparison alone can reject it, without exercising decrypted value comparison. Thus this is evidence beyond the receipt hash, but not decisive evidence for the distinct authenticated value-comparison check. Keep those claims separate and add an independent deciding control if claiming the latter. The normal positive parity oracle does independently authenticate and decode staged frames; that tests output correctness, not which resume refusal caused this negative result.

2. **The callback boundary is trusted test code, not a security boundary (lines 338–340, 450–457, 541–576).** The documented before_commit callback occurs after the final binding check and receives the live connection. An arbitrary caller-controlled callback can change facts or consume lease time after that check. The comment that callbacks cannot bypass validation must be scoped to the supplied passive/trusted harness callbacks. Prefer no untrusted callback between the last check and COMMIT, or recheck after callbacks. Tests do not justify an adversarial-callback guarantee. The after_dml expiry test correctly places its expiry before the expected final binding check.

3. **Worker waits and failure cleanup are not fully bounded (lines 250–288).** select(15) bounds waiting for the first readable byte, but the following text readline can block on a partial line. It does not drain stderr during the barrier. communicate(timeout=30) and kill/wait are bounded, but stop_worker does not close/drain pipes or verify the backend is terminal on every exceptional path. The explicit successful kill cases do perform a fresh pg_stat_activity check before resume, which is good. Database connects/queries inside terminal_backend and native snapshots have no test-local deadline; the Python deadline alone cannot bound a blocked query. Fixture DROP SCHEMA can also wait if cleanup fails. Harden the test harness before calling process timeout/cleanup fully verified. Preserve existing wrapper and role policy.

4. **Current-pin negative coverage is narrow (lines 408–415).** The pin is independently supplied by the host and serialized separately from artifact/progress, which is correct. The negative case only changes plan_digest to zeros. It does not distinguish using the independently current ACTIVE pin from checking internal consistency against the original plan. Other pin fields, an internally coherent stale host input, and current source ACTIVE-state drift are not independently exercised. Positive controls preserve the original pin and original ACTIVE source row, but cannot substitute for those refusal tests. Do not infer stronger external current-authority qualification.

5. **No-durable-change is not no-DML (multiple refusal cases, terminal inspection).** native_snapshot equality establishes unchanged observed journal/stage/catalog state. It cannot rule out an attempted write followed by rollback, a same-value update, or a write restored before the observation. Terminal inspect also counts B8 seals, but zero observed seals plus equal snapshots does not prove a read-only SQL trace. Use SQL-operation observations for claims that refusal precedes all dependent DML or terminal inspection issues zero mutations. Source changes are deliberately outside the snapshot in source-change cases.

6. **Output/artifact confidentiality evidence is incomplete (lines 239–247, 279–283, 515–538).** The collector is calibrated for print and warning logging. It inspects the in-process failure string and captured output/logs for two edited plaintexts, exact full credential URLs, source frames/search terms in hex/repr, and deterministic fixture roots. It does not inspect emitted bundle/artifact bytes, serialized JSON escaping, target frames, subprocess diagnostic paths, exception causes/tracebacks, or other formatting/encoding variants. assert stderr == '' can itself expose nonempty stderr through pytest assertion rendering; a worker failure traceback could contain provider text. Existing conftest redacts database failures and exact credential URL appearances, not arbitrary provider/plaintext/frame data. Public fixture roots avoid real custody exposure but do not make the broader output claim proven. Keep safe-output claims to the calibrated tested path, and use bounded safe diagnostic assertions if strengthening the harness.

7. **Budget evidence is bounded to bind and one complete frame (lines 482–512).** The libpq result-buffer observation is independent and does not advance the cursor. Oversize refusal checks that the known first frame, in raw or hex form, is absent from observed results and that no B8 seal occurred. It does not constrain projection field metadata, reject any transported source frame, observe every connection route, or recheck this property on resume. It does not establish aggregate 4 MiB/64-row admission, bounded state parsing, or every-row early admission. The exact-fit cell checks one batch with one row. Do not call it a complete source-transport/resource qualification.

## Strong independent evidence in the frozen design

- Current expected values are explicit native UUID identities, not reconstructed from the new journal. The fixture includes NULL, empty string, Unicode, post-protection edit, deletion and insertion. It verifies this map differs from historical app.source and independently decodes the current source before binding.
- PublicFixtureProvider uses deterministic public fixture roots and exact PUBLIC TEST WRAPPER descriptors. target_keys retains the search wrapper and adds a distinct generation-2 payload context. Exec workers construct new keyrings/providers and receive no keyring objects or roots in the bundle. Credential environment inheritance is separate from the nonsecret bundle; it is not a secret-free process claim.
- independent_open uses a separate HKDF/HMAC/framing path plus the common qualified AEAD primitive. Target context is supplied independently. Positive parity checks exact target generation, source/target identity membership, NULL parity, decoded current values and exact search-generation/term bytes [10:46].
- Prefix snapshots retain actual target-frame byte strings. Restart and lost-reply cases compare committed target bytes and receipt logical values after fresh-process continuation. Source journal JSON is compared as logical values, not physical JSONB/page bytes. That matches the contract.
- The restart worker is killed with SIGKILL after an acknowledged first commit. The rollback worker is killed after second-batch DML; worker-side native counts establish four stage rows/two receipts in its own transaction, while independent observations see only the first durable prefix before and after backend termination. This is meaningful atomicity evidence if executed successfully.
- Busy-executor test probes the canonical full-source-model-list advisory-lock key independently, confirms the competing lock is held, demands PENDING, observes unchanged durable state, then releases the first process normally.
- Lost-reply test uses the unchanged migration_commit_proxy.lost_commit_reply. The observer arms the actual proxy at ordinal 1 before COMMIT. The proxy forwards COMMIT, receives backend ReadyForQuery, discards that reply, signals dropped and closes the transport. The test demands UNKNOWN plus the dropped event and actual committed stage/receipt rows before a fresh worker resumes. It is not a mocked exception or fake classification-only test. Proxy completion provides terminal COMMIT evidence; it does not independently attest remote primary provenance.
- Actual existing-runtime INSERT/UPDATE/DELETE/TRUNCATE/ownership attempts against stage and journal must receive InsufficientPrivilege, and the journal remains SELECT-readable. Runtime generation-1 source reads remain admitted. This establishes the specific native denials if run; it does not exhaust effective defaults, grants, transitive roles or every reachable permission.
- Source catalog oracle independently includes columns, defaults, indexes and triggers. Broader native_snapshot covers owner/ACL fields for schema relations. Main positive test compares these before/after. No generation-2 publication is requested by the test. Generation-1 publish occurs only in explicitly authorized fixture setup.

## Case coverage and omissions

There are 12 functions and 16 expanded cases, not the original four-profile 48-cell matrix:

1. Current values/same journal/inactive terminal: one case.
2. Fresh-process committed-prefix restart: one.
3. In-flight second chunk killed and rolled back: one.
4. Actual lost COMMIT reply and fresh inspection: one.
5. Busy competing executor: one.
6. Source change: same-value reseal; insertion behind cursor.
7. External pin change: plan digest only.
8. Inconsistent prefix: missing row; valid different value with receipt hash adjusted.
9. Lease expiry: source; target.
10. Existing runtime metadata denials: one case containing ten DML/DDL attempts.
11. Byte budget: exact fit; first-row over budget.
12. Calibrated safe-output provider-failure path: one.

Not established by this file: startup transaction failure and missing-row recreation refusal; malformed/oversized/unknown journal structures; orphan/extra/misordered stage members; conditional-update lost race; catalog/ACL/OID changes; unsupported profiles or multi-model refusal; target/policy/revision mismatch matrix; terminal reinspection after source drift; generation-1 writes after preparation; trusted-primary provenance; physical session invalidation after every exit; statement/lock timeout behavior; output delivery failure; aggregate bounds; no-attempted-DML assertions. Some are obligations in the entry contract, others belong to the explicitly deferred expanded matrix. They must not silently become PASS from these 16 cases.

## Role and execution boundary

scripts/test_postgres.py and tests/conftest.py are byte-identical to S20. The wrapper clears inherited URLs, reads its existing private files, probes both endpoints with SELECT 1, then sets an in-process attestation required by pytest. This review neither read private credential files nor ran the wrapper. The wrapper's SELECT 1 probes alone do not assert PostgreSQL major version or every role attribute. Root owns separate exact environment/role evidence and both pinned dependency cells. No role, credential, cluster or wrapper changes are recommended or authorized here.

All seven full gates remain UNKNOWN. This is test-source review, not native verification, production recovery, product rotation, or an independent human security audit.

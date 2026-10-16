# Quantitative deadline audit fact sheet: 09:22 UTC draft

Evidence cutoff: 2026-10-16 09:22 UTC. Prepared from safe recorded evidence on 2026-10-16; this is a synthesis, not a new test, hash audit, qualification or deadline-completion certificate. The governing 72-hour sprint runs from 2026-10-13 12:36:00 UTC to 2026-10-16 12:36:00 UTC (18:06 IST). The baseline record timestamp is 2026-10-13 12:36:11 UTC; that recording timestamp does not shift the governing start or deadline. At the draft cutoff, approximately 68h46m had elapsed and 3h14m remained. Product source froze at 00:36 UTC on October 16.

## 1. Identities and measurable inventory change

| Boundary | S14 acceleration baseline | Selected frozen doctor preview |
|---|---|---|
| Identity | Recorded checkpoint `2065cb78f3c7126f207fc62c35887ddd204925af` | `candidate-doctor-remedy-integrated221-v1-20261015`, selected in `CURRENT_CANDIDATE.json` |
| Source manifest SHA256 | `7d0fbca30b4cf09e784ac06fbf2afeeee9a71180316aa6c5465a8087913f8121` | `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7` |
| Source files / installed runtime modules | 183 / 37 | 221 / 43 |
| Wheel SHA256 | `43c98cb0128c0a8cfda090febc8f485bd9b4883f3c9c047aefd155fe263ac080` | `053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965` |
| Sdist SHA256 | `535e554d1df9e3fe59e59b4653e24d3c5ec6bbc1c86cf56ca598d8ae78209109` | `2e2a3cfc266602b958e4f4b2206c4d7ccc9e8d1de154ef0412141f529446a330` |

Net inventory growth is 38 source files and six runtime modules. Neither is a count of completed features. Current wheel/sdist sizes are 140,953 / 150,427 bytes; three wheels and two sdists respectively match in the accepted same-host builds. Current full source recovery contains 221 files / 4,451,072 bytes. Baseline archive sizes and complete source byte total were not established by the selected baseline summary; no size-reduction or storage-efficiency delta is claimed.

The original Integrated221 full-suite artifact is distinct: source manifest `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`, wheel `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6`. The current doctor differs from it at README plus CLI. Its 42 other runtime modules are identical; the CLI has the bounded plain-text remedy correction. Byte identity does not turn predecessor full-suite executions into current-artifact executions. No main-branch promotion or production deployment occurred.

## 2. Integrated functional delta since S14

These are bounded lineage changes, not a scored feature-completion total. S14 already included opt-in bounded ciphertext authentication and read-only snapshot observation; that capability is not new sprint credit.

| Integrated lineage | Actual addition/correction | Boundary retained |
|---|---|---|
| S17, correcting held S16 | Off-by-default public-table UPDATE; reverse operation/digest/predecessor checks; protected textual-reference refusals; native DBAPI transaction-state and post-result quarantine corrections; unsafe engine-logging preflight rejection | Does not admit protected bulk UPDATE, ordering, ranges or aggregates |
| S18 | Offline mapped-selector/setup diagnostics and logging checks without connection/key access; versioning/public-metadata controls | Advisory finite diagnostics, not exhaustive application admission |
| S19 | Typed malformed-removal-plan refusal; versioned SAVEPOINT/maintenance-fence controls | Broader DML and lifecycle qualification remain open |
| S20 | Private inactive payload-batch preparation; final-return lease/PID and reverse-policy-drift/native-default controls | No completed active rotation or general implicit-default support |
| S21 | Exact-integer maintenance-budget comparisons while preserving typed refusal; scanner string-binding correction; uv.lock inclusion in sdist | No conversion of estimated-byte bounds into RSS/network/WAL/time bounds |
| S22 | Scanner NamedExpr/shared-target/evaluation-order fixes, including loop/with/augmented-assignment/delete handling | Partial static scanner, not runtime or dynamic-query admission |
| S23 | Remove an extra host key-resolver callback outside the sanitized boundary; retain wrapper counts beside policy fingerprints | No additional provider/key-unwrapping authority |
| S24 | Automatic new-plan index/constraint/backing-index comment inventory; bounded safe plan displays; retained constructor-local UUID reuse | Related history-parsing optimization was not integrated; no general speedup claim |
| S25 | Default-off, internal laboratory-enabled SQLModel async-session composition via its public sync-session-class hook | Exact SQLModel 0.0.47 / SQLAlchemy 2.0.51 boundary; default async refusal remains |
| Cleanup217 and Transport218 | Preserve the sanitized primary preparation failure when rollback also fails; clear preparation; safe UNKNOWN/no-retry diagnostics and best-effort public invalidation; preserve the exact UNKNOWN/False pair through trusted-local exception reduction | No universal physical quarantine, public IPC, arbitrary exception-state transport or untrusted-pickle safety claim |
| Original Integrated221 | Native CLUSTER designation preservation; safe-default/conditional historical-plan handling; reviewed retained-native contract/oracle replacements | No physical heap-order promise, generic lost-metadata reconstruction or durable ABORTED replan |
| Current doctor successor and external handoff | One safe plain-text remedy line for invalid declarations; corrected current-status/attach/snapshot-drain/CLI-exit guidance | JSON/exits/other outputs retained; broader doctor and public end-to-end smoke remain open |

S15's complete-package legacy-to-plaintext-to-retained-native journey added evidence, not a promoted runtime feature. Isolated native accelerators, search-privacy alternatives, online closure research, the private statistics observer and its 99-case campaigns are not integrated product additions. Root/ payload/search-key rotation workflows, online migration and real KMS remain incomplete. Wrapper/admission/recovery tooling improvements are evidence controls, not product capability counts.

## 3. Test results: separate artifact, profile and scope

P/F/E/S means ordinary pass/fail/error/skip counts. Rows must not be summed. Setup/call/teardown phases and subtests are not additional ordinary tests.

| Artifact and executed scope | Profile | P / F / E / S | Separate accounting |
|---|---|---|---|
| S14 full installed | SA 2.1.3 | 1831 / 7 / 0 / 0 | 1,838 ordinary outcomes; subtest count not recorded |
| S14 full installed | SA 2.0.51 | 1813 / 7 / 0 / 18 | 1,838 ordinary outcomes; subtest count not recorded |
| S14 six later snapshot/projection/boundary cases | Each profile, separately | 6 / 0 / 0 / 0 | Excluded from both preceding full totals |
| Original Integrated221 full installed | SA 2.1.3 | 2684 / 0 / 0 / 0 | 56 passing subtests separately |
| Original Integrated221 full installed | SA 2.0.51 | 2638 / 0 / 0 / 46 | 56 passing subtests separately |
| Original Integrated221 installed lifecycle-focused111 | Each profile, separately | 111 / 0 / 0 / 0 | 333 phases; 28 historical producer receipts and 508 native checks per profile, not extra ordinary tests |
| Original Integrated221 installed optional SQLModel | Exact internal enabled profile | 38 / 0 / 0 / 0 | 114 phases; separate optional environment and admission |
| Doctor source RED / GREEN | Source regression boundary | RED 4 / 2 / 0 / 0; GREEN 6 / 0 / 0 / 0 | Intentional reproduced remedy failures; six GREEN cases overlap the installed regression |
| **Current doctor installed seven-case regression** | **SA 2.1.3** | **7 / 0 / 0 / 0** | **21 phases; 1.62s test-suite elapsed** |
| **Current doctor installed seven-case regression** | **SA 2.0.51** | **7 / 0 / 0 / 0** | **21 phases; 1.59s test-suite elapsed** |

Arithmetic S14-to-original-Integrated221 differences are +853 passing outcomes on SA21 and +825 on SA20. Each ordinary inventory rises from 1,838 to 2,684 (+846); SA20 skips increase by 28. These are changed-suite count comparisons, not 846 independently identified new unique coverage cases, a defect-rate improvement or additive evidence across profiles. The 46 exact SA20 native-version skips comprise 10 collection-API, eight session-wide execution-option, 16 distinct_on and 12 aggregate_order_by cases. No new skip or failure waiver was accepted in the Integrated221 run.

The seven original failures are retained historically. Five old refusal expectations concerned metadata now preserved by retained-native storage; two tests were routed to actual protected staging and actual bounded transport. Independent PostgreSQL oracles and six post-apply mutation controls supported the replacements. This is not seven generic data-loss bugs patched, nor product detection of arbitrary corruption after completed apply. Earlier failed candidates and reviewer/harness preparation failures remain preserved separately.

No current full-suite, current optional38 or current lifecycle111 rerun is claimed. Repeated source/installed/focused runs, producer children, compatibility keys and setup/teardown reports are not combined into a headline pass total. Historical S24's 600-key compatibility result does not become a fresh current 600-key classification; current recorded currency is 32 generated keys plus 568 historical-only entries.

## 4. Performance: no comparable S14-to-current delta

The baseline explicitly records audit performance NOT_MEASURED. No matched S14/current workload, scale, hardware control and measurement protocol establishes a product latency, throughput, memory, WAL, pause, cost or recovery-time percentage change. Therefore all such deltas are **UNKNOWN**.

S14 full-suite elapsed times of 315.40/315.98s, original Integrated221's 500.87/499.47s, and current seven-case times of 1.62/1.59s measure different test selections and must not be used as product-performance comparisons. No accepted broad product speed improvement was integrated. Retained research failures stay failures: C1/C5 consistency failures, C7's four overall cost-gate failures, and C9/C10 relative/absolute failures. Isolated component timings and the bounded constructor timeout correction do not establish a matched S14-to-current performance result.

## 5. Restore and delivery scope

- **S14:** recorded 183-file composite same-host candidate recovery from verified S13's 180-file restore plus seven exact remote updates, three new. No clean-machine, fresh-cluster, credential or operational disaster-recovery claim.
- **Current source:** accepted inert 221-file restoration, 4,451,072 bytes, from a reverified previously independently restored README-v2 baseline plus freshly fetched immutable doctor overlay. Exactly 220 files, including all 116 test-tree files, are unchanged from README-v2. This is not a wholly new full remote environment download.
- **Current package:** accepted immutable delivery at `220d35ce796b913c0cced2bd19b416cf287011c9`; 48 wheel payloads and 49 sdist payloads; all 43 runtime modules match. The packages are not the full 221-file source tree. Their same-host reproducibility and inert recovery do not qualify a clean install.
- **Current installed cells:** accepted copied-donor payload/namespace/inode/RECORD audits and the seven-case runs, with unchanged input/corpus closure and safe stopped receipts. The opaque installer-marker body and bytecode were excluded; no broader payload-inspection claim is added here. These are not original dependency-archive or clean-host reproduction proofs.
- **Portability remains blocked:** eight runtime wheels plus five test additions per profile; 14 distinct dependency archives across profiles plus uv inventoried, not acquired as an authentic complete bundle. Tested pycparser 3.11 / iniconfig 2.3.1 differ from locked 3.0 / 2.3.0. A lock-faithful install is a new validation boundary. The original optional environment's 41 inherited noncache RECORD omissions remain disclosed.
- **External handoff:** accepted six-file publication at `6709c967d368d413f2bd669feb0d0f763ffa95cf`; operator/dependency supplements at `d0e071bda74ddf40227319bcb668d56026647003`. Two original compressed recovery uploads remain separately approval-dependent. Current standalone deliveries do not authorize or complete those uploads.
- **Public smoke:** still UNEXECUTED. Exact synthetic-fixture ACL approval, current role identity and reviewed concrete command/binding remain required. Prior cutover-helper authority does not substitute. Native timing-policy approval is separately pending. No current dependency acquisition success is recorded; the bounded official cffi probes failed DNS resolution with zero bytes.

## 6. Remaining objectives and qualification gates

All 34 objective requirements remain active and unchecked. No percentage-complete score follows from test or inventory counts. All seven gates remain **UNKNOWN**:

| Gate | Remaining evidence or decision |
|---|---|
| G-ADAPTER | Complete admitted matrix/unsupported routes, independent adapter review and clean second application |
| G-CRYPTO | Independent composition, nonce/context and key-lifetime review beyond local controls |
| G-QUERY | Profile-specific semantics/leakage admission, calibrated workloads and scanner coverage |
| G-LIFECYCLE | Broader legacy recovery, independent fresh-cluster disaster restore, online/rotation protocols and pause budgets |
| G-PROVIDER | Authorized real KMS custody, credential/region/outage/revocation/throttling/cost evidence |
| G-POLICY | Deployment-owned writer/auth inventory, external pin authority, stale-worker fencing and recovery decisions |
| G-RELEASE | Release criteria, provenance/SBOM/licenses, clean build/install/upgrade and independent reviews |

Automated/native-agent source and evidence reviews are not independent external product qualification. Missing baseline quantities include subtest counts, matched performance distributions and operational RPO/RTO; current source/runtime inventory growth cannot fill them. Genuine original dependency archives/equivalence and a clean independent environment are also unavailable in the accepted boundary.

## Evidence used

Paths are relative to W unless prefixed B (`cryptalis-executable/`). Hashes below are copied from accepted records, not freshly re-audited for this synthesis.

- `persistence-recovery-20261013/{ACCELERATION_BASELINE_20261013.md,s14-qualification-summary.json,s14-recovery-receipt.json,ACCELERATION_24H_AUDIT_20261014.md}`.
- `CURRENT_CANDIDATE.json`, reconciled front/objective/gate tables and dated lineage in `CRYPTALIS_BUILD_CHECKLIST.md`, and `CRYPTALIS_DEFECT_REGISTER.md`.
- B `checkpoints/{S24_S25_CORRECTNESS_ADDENDUM_20261014.md,S24_S25_BLUEPRINT_EVIDENCE_ADDENDUM_20261014.md}`; bounded cleanup/transport contract reports.
- B `reviewer-notes/integrated221-installed-full-sa21-v3-independent-20261015/REVIEW.md`: `9c87be5cef0fbede3ce78ae8b0534b202b4e70455394d261c62a0d99f45b1223`.
- B `reviewer-notes/integrated221-installed-full-sa20-v3-independent-20261015/REVIEW.md`: `d685131a3818ed9cafb74810505af53fe723d47f12ce296b6c126e14f5021ee0`.
- B `reviewer-notes/integrated221-installed-optional38-v2-independent-20261015/REVIEW.md`: `b035f5acb36931515a11adfaa25dc5aa69c3634c85f08eaa683edf0b813f3c1d`.
- B `reviewer-notes/doctor-remedy-real-installed-sa21-v2-terminal-independent-20261016/REVIEW.md`: `4633efb83069dbbaa8ffd45c1b910b1d0a9ae968069d594adbbe7cc43def9a6c`.
- B `reviewer-notes/doctor-remedy-real-installed-sa20-v2-terminal-independent-20261016/REVIEW.md`: `9019b66466a94c67e559fcfccd2eda07f73a0ca89d76c85a123b1b121e9522a9`.
- B `reviewer-notes/doctor-full-source-restore-independent-20261016/REVIEW.md`: `fea27c96519f3f9c52b6e6722f4e5f052df858b294a94cdbd9d1fca0df35fc38`.
- Prior scoped handoff/portability reviews in this isolated reviewer directory: `FROZEN_HANDOFF_V1_REVIEW.md`, `OPERATOR_RECOVERY_STATIC_V1_REVIEW.md`, `PORTABILITY_STATIC_V1_REVIEW.md`, `ROOT_FRONT_CORRECTIONS_REVIEW_20261016.md`.

Only safe recorded documents and receipts were read. No tests, hash-audit reruns, product imports/execution, source edits, installations, network acquisition, database/status or Git actions were performed. This report is suitable as an attributed 09:22 draft input; the final deadline audit must reconcile any later accepted result or decision explicitly rather than silently relabel this cutoff.

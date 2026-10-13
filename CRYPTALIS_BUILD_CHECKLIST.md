# CRYPTALIS — LIVING BUILD CHECKLIST

> **ACTIVE ENGINEERING LEDGER — integrated qualification in progress.** Dot must populate this file from the actual repository, newest recovered candidate, approved decisions and executable evidence before changing any statuses. Do not overwrite without first merging evidence.

## Identity and recovery

- Last updated UTC: `2026-10-13T13:53Z`
- Public GitHub SHA (read-only rechecked): `2ff72ea4fe7871f31a9fabbbf63f19a5cc714e43` via git ls-remote,2026-10-12T20:14Z
- Integrated candidate: `candidate-ciphertext-doctor-20261013` (S14); source-inventory SHA-256 `7d0fbca30b4cf09e784ac06fbf2afeeee9a71180316aa6c5465a8087913f8121` (183 files). Remote integration ad0e6fbff8b6f8fcb565ea45915a442f0c61fa28 byte-verified;183-file composite restore PASS.
- Preserved 15-commit mailbox SHA-256: `9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd` (freshly checked)
- Runtime versions / PG16 config / runtime role preflights: Python3.12.14, SQLAlchemy2.1.3, psycopg3.3.6, cryptography50.0.2, PostgreSQL16.15; unchanged dual-role preflight PASS; full durable-config inspection pending
- Last verifiably restorable recovery archive and SHA-256: `CRYPTALIS_MASTER_S5_COMPLETE_CORPUS_20261012T2156Z.tar.xz`, `2fd2baf252fd2be66d75b39d2ff279202fc40792f6072b3b9d6f5311b7e06fad`;3579file checksums verified; extracted293PASS44.18s plusSQLModel12PASS1.86s. Existing isolated database only; fresh-cluster proof pending permission.
- Durable recovery: S5 GitHub archive restores3579 files; S13 composite180-file restore verified at3006595ee443c629c646e4d7fdd844767985d78d. S14 composite183-file restore verified after exact remote integration readback. Older Library IDs and chronological entries below are historical.
- Execution wrapper: unchanged toolchain/lab_session.py and scripts/test_postgres.py dual-role preflight; exclusive lab lock. S14 full1831/1813PASS with same7 legacy failures;18 native-version skips on2.0.51. Six subsequent installed snapshot controls pass separately per cell.

Correction checkpoints named S6–S14 below are date-local engineering slices. They are **not** completion of the seven named integration work units; in particular `S6-ONLINE-MIGRATION` remains open. Append-only entries retain history; the front tables below are the current reconciled status.

## 72-hour acceleration baseline (2026-10-13 12:36 UTC)

Target: 2026-10-16 12:36 UTC (18:06 IST). Preserve every original objective; the deadline does not qualify unfinished features or waive independent gates. Quantitative audits are scheduled at24/48/72hours. At60hours, stop speculative work and prioritize integration, recovery and final validation.

Frozen integrated baseline: S14, remote2065cb78f3c7126f207fc62c35887ddd204925af,183-file recovery verified. Native internal parallelism is authorized by the new mandate; no Codex tasks/external AI services. Three workers actually launched with separate183-file source snapshots and private branches:
- A: candidate-accel-orm-20261013 / accel/orm-20261013; bounded off-by-default public-table UPDATE prototype, not protected-field bulk UPDATE.
- B: candidate-accel-lifecycle-20261013 / accel/lifecycle-20261013; strict root-equivalence/successor artifact prerequisite; active publication protocol requires review, no automatic policy acceptance.
- C: candidate-accel-search-20261013 / accel/search-20261013; profile-directed immutable public-metadata optimization, no root/derived-key/processor caching.

Coordinator alone promotes, edits the authoritative checklist and publishes verified batches. Workers own separate source copies; no shared active-tree edits. Existing PostgreSQL cluster tests are exclusively coordinator-serialized through unchanged role preflights. Separate cluster/credential approval remains pending. One task is an isolated source snapshot, not a separate machine or independent security review.

Observed resources:9 online CPU threads,9967MiB total memory,8641MiB available atinspection,25GiB disk free. Effective cgroup quotas were not exposed at the expected paths. Agent allowance/billing separation is UNKNOWN; no external paid service started. Available orchestration supports up to7 total slots; initially3 engineering workers plus coordinator are used.

Critical path: actual compatibility/correctness, reversible lifecycle/rotation, online migration, integrated regression/recovery, then genuine external security/provider qualification. Shared DB tests, main promotion and contract decisions cannot be independently parallelized safely on the one approved cluster. Complete production qualification remains unpromised.

## Core promise, non-negotiable rules

- [ ] Authenticated application-side protection; no protected plaintext reaches PostgreSQL on admitted routes
- [ ] Exact native behavior for every SUPPORTED query/transaction/state transition; reject unsupported behavior loudly
- [ ] No silent plaintext fallback, cross-tenant/row leakage, partial commit, missing recovery or authentication bypass
- [ ] Every full product objective below remains visible until qualified; experimental progress does not equal release
- [ ] No production deployments, Git pushes, new Git commits or modified historical mailbox without explicit authorization

## Authoritative requirement mapping

Populate each `Original R01–R07` cross-reference by **reading the actual research blueprint**, not guessing. Replace `UNKNOWN/TO TRIAGE` stages only after checking current source and evidence. All checkboxes remain unchecked until the named acceptance tests pass in an integrated candidate.

| Done | ID | Objective (non-negotiable) | Stage / actual source evidence | Original R01–R07 | Owner slice | Test IDs / native oracle | Performance/security result | Blocker and NEXT action |
|---|---|---|---|---|---|---|---|---|
| [ ] | `OBJ-SEC-01` | Encrypt sensitive values in the trusted application **before PostgreSQL receives plaintext**, with proof at SQL/driver boundaries and independent connections. | PARTIALLY VERIFIED — bounded CF1/adapter/role tests; full threat coverage open | R01 | Security qualification | S9 installed full cells; retained real-app/frame oracle on S8 | No external security/custody qualification; all gates UNKNOWN | Audit untested writer/auth/provider boundaries; do not treat encryption as host authorization |
| [ ] | `OBJ-SEC-02` | Preserve confidentiality and authenticated integrity under declared tenant/field/row/key-generation context, detect swapped or malformed frames and unauthorized release. | PARTIALLY VERIFIED — bounded CF1/adapter/role tests; full threat coverage open | R01 | Security qualification | S9 installed full cells; retained real-app/frame oracle on S8 | No external security/custody qualification; all gates UNKNOWN | Audit untested writer/auth/provider boundaries; do not treat encryption as host authorization |
| [ ] | `OBJ-SEC-03` | Enforce application authorization, result lineage and tenant boundaries; handle SQL injection through parameterization, guarded operations and least privilege without falsely claiming that encryption prevents arbitrary application authorization flaws. | PARTIALLY VERIFIED — bounded CF1/adapter/role tests; full threat coverage open | R01/R06 | Security qualification | S9 installed full cells; retained real-app/frame oracle on S8 | No external security/custody qualification; all gates UNKNOWN | Audit untested writer/auth/provider boundaries; do not treat encryption as host authorization |
| [ ] | `OBJ-SEC-04` | Detect plaintext bypasses via ORM, bulk DML, direct SQL, COPY, external writers, migrations, sessions, background jobs, triggers, caches, logs, exports, backups and privilege paths. | PARTIALLY VERIFIED — bounded CF1/adapter/role tests; full threat coverage open | R01/R06 | Security qualification | S9 installed full cells; retained real-app/frame oracle on S8 | No external security/custody qualification; all gates UNKNOWN | Audit untested writer/auth/provider boundaries; do not treat encryption as host authorization |
| [ ] | `OBJ-SEC-05` | Keep payload/search keys isolated, never silently choose fallback keys, bound nonces/usage/leases, test memory/fork/cancellation/rotation and use robust existing cryptography. | PARTIALLY VERIFIED — bounded CF1/adapter/role tests; full threat coverage open | R01/R03 | Security qualification | S9 installed full cells; retained real-app/frame oracle on S8 | No external security/custody qualification; all gates UNKNOWN | Audit untested writer/auth/provider boundaries; do not treat encryption as host authorization |
| [ ] | `OBJ-SEC-06` | Reduce equality, frequency and access-pattern leakage with a threat-modelled, independently benchmarked search-profile design; document residual leakage, low-entropy domains, adaptive leakage and query-pattern trade-offs. | RESEARCHED — current equality/frequency/access leakage explicit; improved privacy not integrated | R05 | S5-QUERY-PRIVACY | S5 prior-art/research archive and declared leakage profiles | No demonstrated lower-leakage product profile | Compare threat/semantics/performance alternatives before approved admission |
| [ ] | `OBJ-SEC-07` | Independent red-team/security, cryptography, SQL adapter, provider and supply-chain qualification; the seven gates pass only with real evidence. | EXTERNAL QUALIFICATION OPEN | R07 | Seven gates | Gate table below | No independent reviewer approval recorded | Obtain independent reviewers and required resources; do not self-certify |
| [ ] | `OBJ-QUERY-01` | Exact protected equality, `IN`, scoped uniqueness, SQL NULL/three-valued logic, empty lists, bound types, collision resistance/verification and concurrency races. | PARTIALLY VERIFIED — admitted finite semantics; unadmitted grammar rejects | R01/R05 | Query compatibility | Frozen S5 corpus159IDs/554cells; current S9 regression receipts | 398IDENTICAL156REJECTED-LOUD0DEFECT at frozen S5; not blanket SQL support | Reconcile any new grammar against exact native oracles and security contracts |
| [ ] | `OBJ-QUERY-02` | Ordinary SQL correctness: `IS NULL`, `IS NOT NULL`, `!=`, `NOT IN`, `IS DISTINCT FROM`, `IS NOT DISTINCT FROM`, nested Boolean expressions, aliases, outer joins, scalar/entity projections, relationships, subqueries. | PARTIALLY VERIFIED — admitted finite semantics; unadmitted grammar rejects | R01/R06 | Query compatibility | Frozen S5 corpus159IDs/554cells; current S9 regression receipts | 398IDENTICAL156REJECTED-LOUD0DEFECT at frozen S5; not blanket SQL support | Reconcile any new grammar against exact native oracles and security contracts |
| [ ] | `OBJ-QUERY-03` | Advanced SQL: ordering, keyset/offset pagination, ranges/comparisons, `LIKE`/`ILIKE`, prefix, suffix, substring, fuzzy, regex, full-text, `DISTINCT`, aggregates, `GROUP BY`, joins, JSON/array/numeric/datetime and other protected types. Each gets native semantics, a viable scheme/profile or an explicit, researched `REJECTED-LOUD` alternative—never silent omission. | RESEARCH/ADMISSION OPEN — advanced objectives retained | R01/R05/R06 | S5-QUERY-PRIVACY | Explicit core-profile refusals and archived alternatives | No new advanced capability or protected-type promotion | Research viable profiles and leakage/semantic contracts; keep loud refusals meanwhile |
| [ ] | `OBJ-QUERY-04` | ORM/Core and data-modification coverage: INSERT/UPSERT/UPDATE/DELETE, bulk DML, `RETURNING`, triggers, cascades, FKs, savepoints, retries, autocommit/isolation, idempotency and connection/transaction state. | PARTIALLY VERIFIED — ORM routes and private bounded DELETE/cascade profile | R01/R06 | S1-BULK-DELETE | S8 native sync/async35 added cases and58 protected FastAPI tests | General bulk/trigger/UPSERT capability not qualified | Preserve exact effect inventory; qualify each broader operation separately |
| [ ] | `OBJ-QUERY-05` | Full, versioned compatibility corpus and pre-adoption read-only scanner, with exact native-versus-protected classification and reproducible cases. | FINITE CORPUS VERIFIED; pre-adoption scanner incomplete | R01/R06/R07 | Compatibility corpus | S5 exact159IDs/554cells plus separate S8 delta | Frozen corpus hash in corpus section; no current all-cells reclassification | Build meaningful read-only scanner and explicitly reconcile later source revisions |
| [ ] | `OBJ-LIFE-01` | Declarative, deterministic, safe plan → apply → verify; schema/writer/permission inventory; irreversible-step preview and actionable diagnostics. | PARTIALLY VERIFIED — maintenance protocol and numeric/diagnostic corrections | R02 | S3-REVERSIBLE-LIFECYCLE | Current S9 lifecycle/crash/byte-bound tests; S6/S7/S9 public planner cases | Maintenance fallback retained; not online qualification | Keep legacy failures visible and qualify missing failure/recovery boundaries |
| [ ] | `OBJ-LIFE-02` | Resumable, byte-bounded backfill, full final integrity/metadata verification, journaling, restart and crash-safe atomic chunks, failure fencing. | PARTIALLY VERIFIED — maintenance protocol and numeric/diagnostic corrections | R02 | S3-REVERSIBLE-LIFECYCLE | Current S9 lifecycle/crash/byte-bound tests; S6/S7/S9 public planner cases | Maintenance fallback retained; not online qualification | Keep legacy failures visible and qualify missing failure/recovery boundaries |
| [ ] | `OBJ-LIFE-03` | **Near-zero-writer-downtime migration**: concurrent writes, captured changes, ordered catch-up, deletion/PK-change handling, stale-worker fencing, verification, short publish/cutover, recoverability and measured pause SLO. Preserve native semantics and current secure maintenance fallback until this is proven. | DESIGN/IMPLEMENTATION OPEN — maintenance fallback only | R04 | S6-ONLINE-MIGRATION | Archived online/parallel research; no admitted integrated concurrent-write protocol | No near-zero-downtime or adaptive-worker claim | Design and review capture/fencing/catch-up/recovery; define pause budget with owner |
| [ ] | `OBJ-LIFE-04` | Parallel/adaptive migration and verification without double processing, lost updates, unsafe memory, or unbounded locks/WAL. | DESIGN/IMPLEMENTATION OPEN — maintenance fallback only | R02/R04 | S6-ONLINE-MIGRATION | Archived online/parallel research; no admitted integrated concurrent-write protocol | No near-zero-downtime or adaptive-worker claim | Design and review capture/fencing/catch-up/recovery; define pause budget with owner |
| [ ] | `OBJ-LIFE-05` | Exact decrypt-back of **current edited data**, constraints, types, defaults, order, indexes, FKs, views, ACLs, owners and permissions; complete metadata removal; fresh application operation with Cryptalis uninstalled. | PARTIALLY VERIFIED — retained-layout same-host current-value recovery | R02 | S3-REVERSIBLE-LIFECYCLE | S8 FastAPI58x4 suites;7-user/7-item independent backup/decrypt oracle | Fresh-cluster approval pending; legacy conversion unresolved | Qualify independent fresh restore and broader metadata/old-layout paths |
| [ ] | `OBJ-LIFE-06` | Safe rollback, restore, redeployment, stale snapshot/pin refusal, retained encrypted-backup readers, RPO/RTO and deployment-disaster drills; no false secure-erasure claim. | PARTIALLY VERIFIED — retained-layout same-host current-value recovery | R02 | S3-REVERSIBLE-LIFECYCLE | S8 FastAPI58x4 suites;7-user/7-item independent backup/decrypt oracle | Fresh-cluster approval pending; legacy conversion unresolved | Qualify independent fresh restore and broader metadata/old-layout paths |
| [ ] | `OBJ-LIFE-07` | Three separate key operations: root/wrapping rewrap, payload-key rotation/re-encryption and search-root reindex/rotation, with separate correctness and recovery proofs. | PARTIAL EXPERIMENT — rewrap preparation; all three full workflows open | R02/R03 | S4-ROTATIONS-KMS | Existing REWRAP-01 preparation tests and approved experimental boundary | No completed payload rotation/search reindex qualification | Separate protocols, stale-policy/pin recovery and acceptance proof for each operation |
| [ ] | `OBJ-LIFE-08` | Real production KMS, initially AWS KMS where authorized, robust credential/region/outage/throttling/revocation/cost testing, with a provider-independent contract and no hard dependency on AWS for local functionality. | EXTERNAL AUTHORIZATION/PROVIDER QUALIFICATION OPEN | R03 | S4-ROTATIONS-KMS | Local provider evidence only; no authorized production KMS cell | Credentials/cloud account/outage/cost tests not claimed | Use authorized real provider resources only; never generate new access implicitly |
| [ ] | `OBJ-LIFE-09` | Safe install, upgrades, compatibility across versions, decommission and explicit clean uninstall, including unsupported legacy-layout repair or a tracked safe alternative. | PARTIALLY VERIFIED — installed artifacts and retained removal; bounded S15 legacy plaintext bridge, generic repair open | R02/R07 | Lifecycle/release | S8 package-free before/after removal; S9 two offline builds | Seven legacy-profile assertions remain unchanged; S15 two bounded bridge cases pass per cell | Qualify broader legacy/version routes and fresh restore; preserve old mailbox |
| [ ] | `OBJ-DX-01` | Almost zero business/model/query changes; one manifest, named profiles, one attach call, usable status/plan/apply/verify/deprotect/rotate operations and precise startup feedback. | PARTIALLY VERIFIED — manifest/attach path; complete operations CLI incomplete | R06 | S7-PERF-DX-ADOPTION | S8 unqualified upstream app;13 bootstrap/4 fixture lines; C profile/operator steps | No business-source edits in pinned app; remaining setup costs explicit | Unify safe public operational entrypoints without claiming prototype flags as product API |
| [ ] | `OBJ-DX-02` | `cryptalis doctor`: meaningful read-only static **and** dynamic diagnostics, policy/manifest/schema/ciphertext/role/provider/compatibility checks, with clear limits and no silent repair of privileges. | PARTIALLY VERIFIED — S14 bounded declaration/schema/planned-role/ciphertext/source diagnostics; provider and full coverage OPEN | R01/R06 | Doctor/scanner slice | S12 doctor composes native read-only compiler and bounded source inspection; installed suites recorded below | S14 explicit bounded frame authentication; snapshot/projection controls6PASS per cell; provider custody uninspected | Design/read-only implement doctor with explicit checked/unknown outcomes and no privilege repair |
| [ ] | `OBJ-DX-03` | Fully working independent FastAPI/SQLModel integration; a second unrelated application; measure source edit lines, dependency and deployment requirements. Extend thoughtfully to Flask and Django via actually suitable adapters. | PARTIALLY VERIFIED — one pinned real app; second app unresolved | R06 | S2-FASTAPI-E2E | S8 FastAPI58x4PASS with original unqualified tables | FlaskBB native harness failures are not Cryptalis defects | Establish clean unrelated PostgreSQL app baseline; choose suitable adapters honestly |
| [ ] | `OBJ-DX-04` | Normal SQLAlchemy semantics: ORM identity map, lazy/eager loading, `Session.exec`, sync/async, pooling, migrations, background jobs, serializers, errors and result metadata. | PARTIALLY VERIFIED — bounded sync/async SQLAlchemy/SQLModel | R01/R06 | Adapter qualification | Frozen corpus plus current installed2.0.51/2.1.3 suites | No universal ORM/framework qualification | Cover remaining supported semantics and real application boundaries |
| [ ] | `OBJ-DX-05` | Accessible, complete docs: one small quickstart, profiles, threat model, leakage, boundaries, operations, recovery, practical examples, diagnostic errors and learning walkthroughs explaining what/why/how for each slice. | PARTIAL DOCUMENTATION; authoritative front tables reconciled | R06/R07 | Documentation integration | Current checklist, checkpoint/defect docs and recovery receipts | Historical entries retained; no stale template values used as current facts | Finish concise quickstart/diagnostics/recovery docs tied to integrated APIs |
| [ ] | `OBJ-PERF-01` | Continuous native ORM vs driver-only vs protected measurements of p50/p95/p99, write rate, steady-state throughput, CPU, RSS/allocations, WAL, storage/index sizes, query plans, provider RPC and recovery costs. | MEASURED LIMITED — warm retained baseline and isolated allocation prototype | R01/R04/R05/R06 | S7-PERF-DX-ADOPTION | S9 native/driver/protected1800 observations/cell; S10 profile/paired experiment | Material overhead remains; S10 not yet integrated; no point-speedup demonstrated | Finish qualification; measure cold/concurrent/tail/resource/storage/provider effects |
| [ ] | `OBJ-PERF-02` | Profile-guided optimizations in Python, SQLAlchemy, PostgreSQL and crypto: batching, psycopg pipeline/executemany, pooling, safe cache use, allocations, projections, indexing, native accelerators and bounded key caching. | MEASURED LIMITED — warm retained baseline and isolated allocation prototype | R01/R04/R06 | S7-PERF-DX-ADOPTION | S9 native/driver/protected1800 observations/cell; S10 profile/paired experiment | Material overhead remains; S10 not yet integrated; no point-speedup demonstrated | Finish qualification; measure cold/concurrent/tail/resource/storage/provider effects |
| [ ] | `OBJ-PERF-03` | Multithreading, multiprocessing, async and adaptive worker processing with 1/4/16/saturation tests, isolation, retries, process/fork safety, backpressure, cancellation and measured speedup **or regression**. | QUALIFICATION OPEN — prescribed budgets retained | R01/R04/R06 | Performance/scale | Historical scale records plus current bounded warm observations | No1/4/16/saturation or billion-row qualification; no invented pause/write targets | Reconcile matched scale evidence and agreed budgets; keep regressions visible |
| [ ] | `OBJ-PERF-04` | Performance targets on agreed comparable conditions: repository's current added read p95 ≤3 ms for point/equality, ≤8 ms for `IN`-20 and ≤2× protected-column-plus-equality-index storage. Define write-throughput and pause SLOs through a documented stakeholder decision; do not invent an approved target or relax an existing target because a test fails. Evaluate million-row scale and a documented growth path to billion-row workloads without claiming the latter has already been tested. | QUALIFICATION OPEN — prescribed budgets retained | R01/R06 | Performance/scale | Historical scale records plus current bounded warm observations | No1/4/16/saturation or billion-row qualification; no invented pause/write targets | Reconcile matched scale evidence and agreed budgets; keep regressions visible |
| [ ] | `OBJ-OPS-01` | Reproducible installed wheels/source releases, verified license, SBOM, dependencies/provenance, locked builds, supported-version matrix, rollback documentation and independent reviewers. | PARTIALLY VERIFIED — repeated local builds and installed matrix | R07 | Release qualification | S9 identical offline wheel/sdist;39 RECORD entries;35 installed modules | No independent clean-machine build/signing/supply-chain approval | Complete SBOM/licensing/reviewer/fresh-environment requirements |
| [ ] | `OBJ-OPS-02` | Recoverable research environment, immutable evidence hashes, source-to-test traceability, live Markdown checklist and durable local/authorized remote snapshots. | VERIFIED LIMITED — remote byte persistence and composite file recovery | R07 | Recovery | S5 GitHub3579-file restore; S9 composite174-file hashes; original history bundle | Fresh-machine/credentials recovery not established; older excluded archives not all synced | Continue small verified batches and test fresh restore only with required approval |
| [ ] | `OBJ-RESEARCH-01` | Comparative, source-backed reverse engineering and potential novel mechanism research; demonstrate independent novelty/prior art and repeatable advantages rather than claiming novelty from an interesting idea. | ONGOING — source-backed alternatives and finite experiments | R01/R02/R03/R04/R05/R06/R07 | Research integration | Archived CipherStash/public-source review; current profile-directed alternatives | No novelty claim or vendor behavior reproduction implied | Triangulate mechanisms and preserve failed alternatives before product integration |
| [ ] | `OBJ-RESEARCH-02` | One finished, coherently integrated **working software candidate** that passes its admitted native-compatibility contract, end-to-end reversible lifecycle, real-app adoption proof and all relevant acceptance gates before a qualified release. | INTEGRATED EXPERIMENTAL CANDIDATE; COMPLETE PRODUCT OPEN | R01/R02/R03/R04/R05/R06/R07 | All work units | S9 current candidate + independent native/lifecycle evidence | Seven legacy failures and all seven full gates remain open | Continue correctness/integration work; obtain external resources only for dependent gaps |

## Ordered integration run board

These are the original seven integration workstreams, distinct from dated corrective checkpoint IDs.

| Work unit | Dependencies | RED reproduction | Candidate change | Native/real-PostgreSQL comparison | SQLAlchemy 2.0 / 2.1 | Mutation proof | Installed-wheel / real app | Before/after performance | Checkpoint archive | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `S0-RECOVER` | Authorized archives | Recovered rollback/missing-file state | S5 remote restore + incremental candidates | Unchanged role preflights; installed suites | Both recorded | Hash mismatch detected before earlier publication | S9 installed;174-file composite restore | N/A | S5 archive + Git history + exact remote overlays | LIMITED VERIFIED; fresh-machine/cluster still open |
| `S1-BULK-DELETE` | S0 | Native/private DELETE discrepancies retained | Bounded private one-hop cascade; S8 public mapping pin | Native sync/async outcomes and teardown | Both scoped cells PASS | Inventory/temporal and pin-guard omissions preserved | S8 protected upstream58PASS | No general bulk throughput qualification | S8 commit/recovery receipts | NARROWLY VERIFIED; broad bulk remains open |
| `S2-FASTAPI-E2E` | S1 | Prior teardown and unqualified-child refusals | External manifest/attach shim; no app source edits |58 native +58 protected +58+58 package-free PASS | Real app2.0.51; core both | No-optin/drift controls retained | Pinned upstream7257e606; no manual table schema edits | Raw app timings only | S8 same-host7-user/7-item recovery | ONE APP VERIFIED; second app open |
| `S3-REVERSIBLE-LIFECYCLE` | S0,S2 | Layout/oracle/fault discrepancies retained | Retained current-value lifecycle; typed planner corrections | S9 full suites; S8 decrypt/removal/real backup comparison | Both; same7 legacy assertion failures | Crash/connection/pin tests preserved | Package-free current-value operation verified | Pause/RTO budgets not qualified | S8/S9 source/artifacts/evidence | PARTIAL; legacy/fresh-cluster gaps open |
| `S4-ROTATIONS-KMS` | S3 | REWRAP-01 preparation evidence only | Partial experimental provider preparation | No complete real-provider three-operation proof | Existing scoped tests only | Not a full qualification | No production KMS cell | NOT QUALIFIED | Historical approved experiments retained | OPEN; credentials/resources/review needed |
| `S5-QUERY-PRIVACY` | S0 and reviewed change | Leakage/refusal research retained | Existing explicit equality profile; no lower-leakage profile | Frozen159-ID corpus; core current regression evidence | Both finite cells | Core semantic/crypto controls only | No new advanced profile promotion | Current warm baseline; alternatives remain research | S5 research archive and later receipts | OPEN; advanced objectives preserved |
| `S6-ONLINE-MIGRATION` | S3 and reviewed change | No admitted integrated online protocol | Safe maintenance fallback remains | Concurrent-write/catch-up/cutover proof NOT COMPLETE | NOT QUALIFIED | NOT COMPLETE | NOT COMPLETE | Pause SLO unresolved | Archived design research | OPEN; not completed by checkpoint S6 |
| `S7-PERF-DX-ADOPTION` | Integrated safe candidate | Actual retained performance gap measured | S8 integration simplification; S10 allocation prototype | Exact native/driver/protected results | Both baselines; S10 qualification ongoing | Wire and strict-input oracle; no skipped auth checks | Reproducible wheels; one pinned app | Warm finite evidence only; no broad point speedup | S9/S10 experiments and hashes | PARTIAL; doctor/scanner and broader qualification open |

## Compatibility corpus — finite, versioned facts

- Frozen S5 corpus `s5-current-compatibility-corpus.json`, SHA256 `9df455d63a89a0cb1cc4e6ee22bfdd0e3b50c2899187265bf3a8081bccebe971`; source identity retained in that receipt. Later source changes are not silently relabelled as a full corpus rerun.
- Unique operation IDs:159 (frozen S5).
- Executed native-vs-protected cells:554 (frozen S5).
- Frozen executed cells:398IDENTICAL /156REJECTED-LOUD /0DEFECT. Missing/unexecuted combinations remain listed in the corpus, not converted to passes.
- Later additions remain separate: S8 unqualified public-child35 cases per version; S9 numeric-boundary14 cases per version; S10 wire oracle in qualification.
- Unsupported dynamic queries and staging-scanner coverage: `NOT VERIFIED`
- Mandatory core families: entity/scalar/alias/outer joins, NULL truth tables, tenant switching, sync+async, SQLAlchemy 2.0+2.1, bulk, SAVEPOINT, concurrency, restore, public-type coexistence.

## Threat model, privacy/leakage and current security limitations

| Risk/adversary | Guarantee or observation | Reproducer / test evidence | Severity | Unresolved decision |
|---|---|---|---|---|
| Read-only database disclosure of ciphertext/index terms | NOT YET RECONCILED | NOT RUN | UNKNOWN | Exact leakage profile |
| Authenticated application and authorized decryption misuse | Outside pure encryption guarantee; requires authorization | NOT RUN | UNKNOWN | Host authorization integration |
| Application SQL injection/direct writer bypass | Parameterization/least-privilege/guards required | NOT RUN | UNKNOWN | Exact writer inventory |
| Frequency leakage in exact equality terms | Known structural risk; quantify conditional workload attack | NOT REPRODUCED IN THIS TEMPLATE | UNKNOWN | More private search profile |
| Same-context replay/deletion/hostile DB omission | Do not overstate authentication guarantee | NOT RUN | UNKNOWN | Explicit trust and freshness design |
| Untrusted old application workers during cutover | Explicit fencing and versioned external pin required | NOT RUN | UNKNOWN | Deployment protocol |

## Defect/FMEA and variant ledger

| Defect ID | Red reproducer | Native expected / protected observed | Severity | Root cause | Fix/revision | Mutation/variant results | Status / next action |
|---|---|---|---|---|---|---|---|
| `D-BULK-DELETE` | Native/protected private-profile reproductions retained | Same bounded public-child cascade effects | P1 until broader qualification | Private grammar/effect inventory | S8 integrated;58 protected upstream tests including teardown PASS | Native sync/async and drift/no-optin controls; guard-removal failures retained | Narrowly corrected; generic bulk capability remains unqualified |

## Performance and scale ledger

| Benchmark ID | Machine / corpus / source hashes | Native ORM | Driver-only | Protected | p50/p95/p99; units | Throughput; resource / WAL / index | Run order and spread | Regression / decision |
|---|---|---|---|---|---|---|---|---|
| `PERF-RETAINED-S9` | Same-host1000-row synthetic; installed S9 hashes retained | Point0.171/0.175ms | Point0.041/0.043ms | Point1.930/1.794ms | Median of5 block medians, SA2.1/2.0; not tail qualification | Exact results; other metrics still open | Alternating paths,40 samples/cell/block; raw samples preserved | Material overhead; profile-directed S10 remains experimental |

Existing documented targets (not pass claims): added p95 ≤3 ms point/equality; ≤8 ms IN-20; ≤2× protected column + equality-index space. Writer-throughput and acceptable cutover pause are **unresolved budgets**, not numbers to invent.

## Pending decisions and amendments

| Decision | Prior approval / actual contract evidence | Alternatives | Needed evidence | Action |
|---|---|---|---|---|
| ASYNC-01 / ACL-01 / UUID-01 / A6-COLLATION-01 | Verify original approvals and integrated source | Preserve safe fallback | Full native/cancellation/permission and real-app checks | RECONCILE |
| REWRAP-01 versioned successor | Experimental implementation approval only | Existing maintenance policy | Publication disagreement, pin recovery, real KMS | RECONCILE |
| More private search / online migration | Full product objective; approved architecture change required where contracts differ | Research opt-in profiles | Threat/semantics/recovery/benchmarks | OPEN |

## Seven independent qualification gates (NEVER self-certify)

| Gate | Current gate status | Evidence needed | External reviewer / resource | Next action |
|---|---|---|---|---|
| `G-ADAPTER` | UNKNOWN | Complete admitted matrix and unsupported-route coverage; independent adapter review; clean second app | Independent reviewer not assigned | Preserve finite test evidence and diagnose remaining adoption gaps |
| `G-CRYPTO` | UNKNOWN | Independent composition/nonce/context/key-lifetime review beyond local vectors and failure tests | Qualified independent cryptography reviewer | Keep existing primitives/format; submit auditable source/evidence only when arranged |
| `G-QUERY` | UNKNOWN | Complete semantic/leakage admission for each claimed profile, calibrated workloads and scanner coverage | Independent semantics/security reviewer | No advanced-profile or general SQL claim from current finite tests |
| `G-LIFECYCLE` | UNKNOWN | Legacy layouts, independent fresh-cluster disaster restore, online/rotation protocols and pause budgets | Existing fresh-cluster approval unanswered; independent reviewer | Continue unblocked maintenance correctness; wait only on dependent external setup |
| `G-PROVIDER` | UNKNOWN | Authorized real KMS credential/region/outage/revocation/custody/cost evidence | Real authorized provider account/access and reviewer | Do not create new credentials or claim local provider tests establish custody |
| `G-POLICY` | UNKNOWN | Deployment-owned writer inventory/auth, external pin authority, stale-worker fencing and recovery decisions | Deployment operator/independent policy review | Distinguish fixture attestations from independently verified operational facts |
| `G-RELEASE` | UNKNOWN | Full release criteria, known-failure resolution, SBOM/license/provenance, clean build/install/upgrade and reviews | Independent clean environment and reviewers | Retain reproducible local artifacts without release/promotion claims |

## Recovery/archive ledger

| UTC | Archive name + SHA-256 | Candidate source hash | Included file count | Fresh extraction DB/smoke | Durable location / verified sync | Result |
|---|---|---|---|---|---|---|
| 2026-10-13 | S5 archive SHA2562fd2baf252fd2be66d75b39d2ff279202fc40792f6072b3b9d6f5311b7e06fad; S9 source manifest above | Exact source manifests retained |3579 S5 files;174 S9 candidate files | S5 GitHub-only file restore and S9 composite hash restore PASS; fresh cluster NOT RUN | Private GitHub byte readback verified, checkpoint97b4ef6523ebbb1b7ce6f3a0718dc3c2a6074f27 | LIMITED VERIFIED; no clean-machine/credential claim |

## NEXT ACTION (top five; update after each slice)

1. Preserve verified S14 source, artifacts,183-file recovery and remaining evidence readback; prior checkpoints retained.
2. Investigate unresolved legacy-layout transition/restore compatibility; preserve all seven original assertions and approved safety contracts.
3. Extend remaining diagnostic evidence only where useful: bigint/single-tenant traversal, cross-table byte limits and key-lease outage behavior; provider custody remains unknown.
4. Establish a clean unrelated PostgreSQL application baseline. Fresh-cluster/new-credential qualification waits for the existing unanswered approval.
5. Continue separately reviewed full key rotation, lower-leakage search and online migration designs; preserve all original product objectives and independent review requirements.

## Atomic slice-checkpoint entry template — append once after every slice

```text
UTC:
Slice / OBJ IDs:
Source revision/hash BEFORE -> AFTER:
What changed and why:
Native expectation and independent RED reproducer:
Commands:
PASS / FAIL / SKIP / NOT RUN / warnings / duration:
Mutation and adversarial evidence:
Before/after performance or NOT MEASURED (reason):
Developer-visible changes and residual risk:
Decision/contract change:
Checklist row changes:
Archive name, SHA-256 and fresh-restore result:
Durable-sync result:
Next five actions:
```

## Exclusions that remain active objectives

No item is removed because it is difficult, unavailable, unsafe under one scheme, costly or pending external review. List profile-specific refusals here with objective ID, exact reason, alternative, and future research/qualification route.

| Objective ID | Current profile restriction | Concrete reason | Supported alternative | Open research/implementation path |
|---|---|---|---|---|
| OBJ-QUERY-03 / OBJ-SEC-06 | Advanced predicates/types not admitted by current text equality profile | Different semantics/leakage require explicit schemes and qualification | Loud rejection; declared equality/IN/storage profile | Research and compare independently; preserve all original advanced objectives |
| OBJ-QUERY-04 | Generic bulk DML/cascades not qualified | Current proof is a private one-hop profile with effect locks | Ordinary admitted ORM writes; default bulk rejection | Expand only with exact native/tenant/transaction/effect proof |
| OBJ-LIFE-03 / OBJ-LIFE-04 | No qualified online/parallel migration | Capture, fencing, ordering and recovery not proved | Secure maintenance fallback | Reviewed protocol plus native concurrency/cutover evidence |
| OBJ-LIFE-07 / OBJ-LIFE-08 | No production KMS or complete rotation triad | Local provider/rewrap preparation is insufficient | Approved local synthetic experiments | Obtain authorized resources and separate operation proofs |
| OBJ-LIFE-06 / OBJ-LIFE-09 | Fresh-cluster and legacy-layout restore incomplete | Explicit approval pending; format-specific assertions unresolved | Verified same-host retained recovery; preserve old artifacts | Independent restore and reviewed safe legacy route |
| OBJ-DX-02 / OBJ-DX-03 | Bounded unified doctor exists; complete provider/compatibility coverage and second unrelated app remain open | Current CLI and dynamic diagnostic coverage incomplete | Existing manifest inspection and pinned FastAPI path | Implement read-only diagnostic slice; establish clean second native baseline |

## Changelog

- **Template created:** No actual source implementation, test or release qualification is claimed by this document.

## Historical recovery event (resolved by later checkpoints)

The newest local candidate and 16:32 recovery directory are absent after an environment reset. Older workspace files remain. Recover Library archive libfile_613eb1e959b481d19e797a89e911a412, expected SHA-256 9c15c1696158fe328443cbcfb76b89ee5896fc025daafb33036b48903cc6d386. Prior recorded runtime results are historical until freshly reproduced. No implementation is promoted during recovery.

## Actual original requirement mapping source

Read `cryptalis-executable/repo/docs/research/CRYPTALIS_FINAL_REVAMP_BLUEPRINT.md`, lines160–166. The cross-references above are traceability mappings, not replacement definitions.

- R01: authenticated context, exact SQL, safe errors and authority boundaries.
- R02: current-data reverse, package-free exit, recovery, upgrades and three rotations.
- R03: provider-agnostic durable custody and optional AWS reference adapter.
- R04: move O(N) work outside downtime with exact catch-up/switch and measured pause.
- R05: stronger search privacy with exact or explicitly versioned semantics.
- R06: minimal integration changes, predictable ORM and diagnostics.
- R07: independent actual-artifact qualification and retained recovery.

## Current working software and recovery distinction

The old surviving candidate passed16 existing VARCHAR runtime tests in2.52s using actual PostgreSQL16.15, unchanged dual-role preflight and verified source import. Evidence: `cryptalis-executable/evidence/master-recovery-survivor-smoke-20261012-2014/{tests.log,junit.xml,source-stability.json}`. This proves the surviving lab can run that bounded selection; it does not reproduce the missing latest cascade candidate, installed wheel or FastAPI success.

Reproduce survivor smoke with the existing lab supervisor and a NEW evidence directory: `cryptalis-executable/repo/.venv/bin/python cryptalis-executable/toolchain/lab_session.py --candidate-root /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-public-types-strict --evidence /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/evidence/NEW_NAME -- -q tests/test_varchar_runtime.py --tb=short -ra`. Never run against another database or bypass the private dual-role preflight.

## S0 recovery work unit: finite acceptance before source changes

- Identity: freshly verify public main, original mailbox, survivor hashes and latest archive hash. Main and mailbox verified; latest archive blocked by Library scope.
- Restore: latest full archive into a fresh directory, verify all manifest entries, build a disposable dependency environment and rerun bounded native/protected smoke. NOT RUN for latest archive.
- Promote: only choose the integrated starting candidate after checking inheritance/dependencies. No blind prototype merge, and no fallback relabeled as latest.
- Performance: NOT REQUIRED FOR THIS RECOVERY SLICE; application-performance comparisons require restored identical source. Restore duration and smoke wall time are recorded separately.
- Highest product defect: historical FastAPI bulk teardown was resolved only in optionale52; fresh status UNKNOWN until latest archive is accessible. Do not reimplement an already-corrected defect from stale source.

## Precise blockers and next five actions

The archive-access blocker is RESOLVED by the user attachment. New full baseline is running; initial bounded run had508PASS/10FAIL. Four missing-asset failures are fixed; remaining lifecycle/representation failures are not dismissed or skipped.

1. Finish installed complete frozen2.1.3 suite within existing600second supervisor bound; classify every failure.
2. Reproduce full unchanged real FastAPI and package-free lifecycle from restored harness/environment after the lab lock is released.
3. Independently distinguish native semantic failures from old storage-layout assumptions; define the highest genuine correction before any runtime edit.
4. Execute one bounded correction with native RED/GREEN, required failure variants, dual-version installed tests and relevant measurements.
5. Update every affected objective/defect/corpus row, checkpoint complete source/evidence, test restore and continue the next eligible slice.

External release blockers remain: independent human review, real authorized production-provider qualification, deployment/retirement decisions, and any major contract amendment. Local work is not exhausted. Master mandate and template fully read; original R01–R07 blueprint mapping read; older instructions/source reconciliation continues. The two security/performance briefs mentioned within the mandate were not separately supplied, so their exact identities/content are not claimed read.

## Change log

2026-10-12T20:14:19Z: checklist initialized with all master OBJ requirements without abbreviation; actual R01–R07 mapped. Detected environment rollback, latest archive scope denial, verified preserved mailbox and public main, and16PASS surviving-lab smoke. No source edits, commits, pushes, production actions or contract changes. Latest integrated candidate restoration remains BLOCKED on archive access.

2026-10-12T20:15:42Z: Freshly extracted the recorded public base and successfully checked/applied all15 preserved mailbox messages sequentially without creating commits. Mailbox bytes unchanged. Receipt: master-recovery-2012/mailbox-apply-receipt.json. This verifies mailbox applicability, not restoration of later uncommitted experiments.

2026-10-12T20:17:22Z: surviving candidate SQLAlchemy2.0.51 smoke16PASS in2.42s. Saved older-baseline archive CRYPTALIS_SURVIVING_BASELINE_20261012T2017Z.tar.xz (902948 bytes), SHA-256 9b88aa9e0b0bb42cd32417aaff4dbc06d74c7f63146b879da18901425c77d91d. Fresh extraction checksums verified and source smoke rerun using the existing disposable PostgreSQL lab; see master-survivor-extraction-replay-20261012-2017. This is not a new-cluster restore or the latest e52 candidate.

## Recovery resolved — 2026-10-12T20:43:45Z

User supplied the requested archive as libfile_bc0c43151e2881d182145380b8811837. SHA-256 matches9c15c1696158fe328443cbcfb76b89ee5896fc025daafb33036b48903cc6d386; all2841 archived files verify. Earlier Library scope blocker is RESOLVED by this explicit new attachment, not bypassed.

Restored exact cascade source as candidate-master-integration-20261012; source-tree inventory hash bcbe45d390a3f43470fa9abe3574e8e0ee8d854a5def5501784d5e203404e441. Installed archived e52 wheel into a newly created14-package virtual environment offline. All34 runtime modules match. Reused unchanged disposable PostgreSQL16.15 lab and dual-role preflight; no new cluster claim.32 installed cascade/rollback/refusal/current-row reverse smoke tests PASS in11.12s. Evidence master-integrated-restored-smoke-20261012-2043. No code change or public-profile promotion yet.

### Next bounded run: integrated-suite compatibility triage

Before picking a correction, execute the complete frozen candidate test selection with stop-after10failures and the supervisor's600second bound. Purpose: identify integration regressions masked by earlier selected suites, distinguish obsolete representation assertions from real semantic defects, and preserve failure receipts. Do not skip or rewrite failing expectations to match implementation. No source edits during triage. Historical fast-app cascade defect is no longer assumed live. Next steps: (1) integrated test triage, (2) confirm highest real discrepancy with independent native oracle, (3) define correction acceptance and rollback, (4) narrow RED/GREEN and variant tests, (5) installed dual-version validation and checkpoint.

## Slice S0A: complete recovery assets (defined before correction)

D-RECOVERY-ASSET-01, HIGH for reproducibility:16:32 archive omitted examples/*.py and examples/envelopes/*.hex because its packager included only.json/.md in examples. Full frozen suite:508PASS,10FAIL, stop-after10 in18.13s, one known fork warning. Four failures are missing example/vector files; six are legacy deprotection representation assumptions needing separate triage. No product security success inferred.

Acceptance: recover all tracked example assets byte-for-byte from confirmed public base2ff72ea4fe7871f31a9fabbbf63f19a5cc714e43 into the separate integrated candidate only; preserve existing candidate examples and reject conflicts. Re-run the unchanged four affected test modules against the installed wheel; verify all12 base example paths exist and match. Update archive builder to include complete reviewed examples and a machine-checkable required-asset inventory; omit one asset in a disposable copy to show validation fails. No crypto, policy, schema or runtime change. Rollback is the immutable supplied16:32 archive. Performance benchmark NOT REQUIRED: restored documentation/demo/test assets do not affect runtime package code.

2026-10-12T20:46:18Z S0A verification: restored exactly4 omitted files from pinned public base; verified all12 tracked example assets. Unchanged affected modules269PASS in4.09s on SQLAlchemy2.1.3 and269PASS in3.84s on2.0.51, installed original e52 wheel with34 matching runtime modules. Deliberate asset omission makes the independent inventory validator exit1; restoration exits0. No runtime code or test-oracle edits. D-RECOVERY-ASSET-01 fixed in candidate and packaging workflow; fresh checkpoint replay pending. Six lifecycle-test failures remain open for independent interpretation/qualification.

## S0A checkpoint complete / S0B baseline begins

2026-10-12T20:47:31Z: complete recovery checkpoint CRYPTALIS_MASTER_S0A_RECOVERY_20261012T2046Z.tar.xz,2592180 bytes,SHA-25673efcb077c3c3c982eb1e85d1289b9997250a1949370c8a8c9659efcfa32068a. All3080 manifest files verified; independent fresh extraction reruns269 affected-module checks in4.09s, allPASS, extracted bytes unchanged. Current integrated source inventory hash0add607f237a6b86354116e9e5eac95d787bd81511633ef609add3a7dbe684f9. This hash includes restored example assets; all34 runtime modules remain byte-identical toe52.

S0B acceptance: complete candidate's frozen test selection on installed SQLAlchemy2.1.3 within600seconds, preserving every failure and no skips added. Classify failure root causes and independently confirm the highest correctness issue. Full suite success is not assumed from selected profile tests. Source remains frozen during this diagnostic run.

2026-10-12T20:52:35Z: restored pinned real-app environment by copying the surviving77-dependency environment and replacing only Cryptalis with archived e52wheel; all77 version entries identical, pipcheckPASS. Verified upstream FastAPI commit7257e606cb94eada1dca40173e2b7f99dd549bc6. No real-app re-execution yet; full baseline owns the lab lock.

## S0B result and S1T retained-layout verification slice

Full installed frozen baseline on SQLAlchemy2.1.3:1637PASS,50FAIL,0SKIP,2 known fork warnings,278.25s; evidence master-integrated-full-baseline-20261012-2048. Failures remain recorded in full-baseline-failures.json. Real-app replay subsequently passes58 native and58 protected tests including teardown, outer1PASS31.40s; package-free/backup receipt inspection pending.

S1T defined before test corrections: two demonstrated verification defects prevent integrated acceptance. D-ORACLE-LAYOUT-01: the common independent-frame reader selects retired logical column name after switch, observing intentionally NULL placeholders instead of retained CF1 bytes. Correct only its physical-column selection using the documented retained profile and fixed field identifier, retaining independent decryption/expected native values. D-FAULT-SCHEDULE-01: switch connection-loss test waits for removed DROP COLUMN SQL, so no fault occurs. Replace string matching with a phase-boundary callback that executes the real switch, then terminates that exact owned disposable backend before commit. Verify actual termination, durable original values/frames/journal, typed failure and exact retry. No product runtime change, no test skipped, no plaintext fallback. Remaining representation/metadata failures stay open.

Primary references checked2026-10-12: https://www.postgresql.org/docs/16/tutorial-transactions.html (atomic transaction visibility); https://www.postgresql.org/docs/16/functions-admin.html (same-role backend termination and timeout semantics). Test controls only the connection created for its positively identified disposable fixture; no arbitrary PID or third-party session. Alternative SQL-text matching rejected because this run demonstrated it misses the new cutover. Additional per-transaction admission or stale-worker redesign is not part of this slice.

Acceptance: unchanged semantic assertions must pass for targeted protection/resume/cutover cases on2.1.3/2.0.51; fault callback must prove it fired; disable termination in a throwaway test copy and require the test to fail, then restore exact source. Recheck installed34module equality. Performance NOT REQUIRED for test-only change. Preserve original50fail log and S0A archive as rollback.

2026-10-12T20:56:33Z S1T first pass14PASS/1FAIL in3.70s. The remaining failure was the same test asserting the legacy four-column/bytea layout after all native sync/async value checks passed. Replaced that physical-layout assertion with an explicit profile-specific full ordered type/column expectation and a zero-plaintext native-slot assertion; no value oracle weakened. New cutover termination test passed with actual verified backend termination and exact prior journal/data restoration.

2026-10-12T20:58:05Z S1T finite verification complete:15 targeted protection/native sync+async/resume/fault/warmed-mapper cases pass on2.1.3 (3.94s) and2.0.51 (3.76s). Fault-activity control without termination fails1 test in0.38s; exact restored callback passes1 in0.48s. This is proof the injection actually occurs, not removal of a production security guard. Only tests/test_migration.py changed; all34 runtime modules still match archivede52. Original full-suite50failures remain historical; no new full-suite success is claimed.

Fresh real-app results verified:58 nativePASS,58 protectedPASS including teardown,58 package-freePASS before removal and58 after removal, zero failures/errors/skips. Both independent package-free receipts confirm package absent, exact user/child values before fixture reset and no application-source edits. Exact nonempty encrypted backup recovery remains separately described in its receipt. Outer31.40s; copied77-package environment, not clean resolver. Evidence master-restored-real-fastapi-20261012-2054.

2026-10-12T21:00:10Z S1T checkpoint saved as libfile_138d191e3e3481d18724c71e28022b74: CRYPTALIS_MASTER_S1T_VERIFICATION_20261012T2058Z.tar.xz,SHA-256 aa49d5e4abc3be4d22323588eff2e7c1d0a82722ccf0291d08b5efa0de3f4be9,2615696bytes,3169files. Fresh extracted15-test replay PASS3.82s, all checksums unchanged. Integrated source-tree SHA-256 66c15c81d17a1556254a6c3e435456e2f5d33d13443412b727e3c53f94b0db15. No runtime module changes; full-suite remaining failures not yet rerun. Next independent verification slice addresses the same physical-frame assumption in the multitable oracle, keeping native values and independent field/tenant/record decoding intact.

## S1U defined: multitable independent-frame oracle

Root cause matches D-ORACLE-LAYOUT-01: tests/test_migration_multitable.py::other_frames selects logical name/note columns after retained cutover instead of fixed field-ID CF1 columns.13 failures were recorded in complete baseline. Change only that selector for the explicit retained profile; keep independent AES opening, expected native values, field/tenant/record context rejection, original journal/fence assertions and real process interruptions unchanged. Run the entire multitable module on both installed SQLAlchemy versions; record remaining failures without broad replacements. Rollback S1T archive. No runtime change or performance claim.

2026-10-12T21:02:13Z S1U: entire multitable module18PASS on SQLAlchemy2.1.3 (11.32s) and18PASS on2.0.51 (10.46s), including real process interruption/resume and field/tenant/record context cases. Only explicit retained-profile physical-column selector changed; independent expected values and decoder remain unchanged. This addresses13 historical failures from this module; no new complete-suite count claimed.

## S1V defined: reverse verification targets the real encrypted storage

Eight deprotection failures from the full baseline contain legacy column/format assumptions. Change only tests/test_deprotection.py to select the documented physical ciphertext column for the known retained profile, assert both native/payload types explicitly, and direct existing corruption/context/backup oracles at actual ciphertext. Keep all independently expected values, refusal assertions, journal invariants, real backup restore and package-free checks. Legacy profile branch remains explicit. Test the8 affected cases first on both versions; no runtime changes or promotion, no skips, and no new plaintext path. Preserve S1U checkpoint as rollback. Failure logs from the original frozen suite remain authoritative historical evidence.

2026-10-12T21:05:42Z S1V targeted reverse checks8PASS in3.42s on2.1.3; matching2.0.51 run completed separately (exact timing in receipt). Existing corrupt-frame, generation, membership, fence and wrong-row refusals now operate on actual CF1 storage, and independent encrypted-backup recovery decodes the correct field. Runtime unchanged. S1U archive durable at libfile_66d9d8516a0481d18087a47e330cef2e, SHA-256cff2aa6b3cbe357d5d3b075f52a5c12726386b2b6d34f0ee33f3bd66f5557c6a;18-test extracted replay11.28s.

## S1W defined: independently qualify public metadata preservation

Seven legacy reverse tests expect refusal/public-column copying, while retained layout intentionally keeps the original public columns. Do NOT change those refusal expectations simply to obtain a green full suite. Add a separate explicit retained-profile native oracle first: compare public column object identity, ordinal, type/collation, default, ACL, comment, statistics, storage/compression before and after reversal, plus exact current public values. Cover comment, column SELECT grant, statistics, storage and compression, and edits/wide public values during reverse. Any mismatch is a real lifecycle defect; a pass is profile-scoped evidence, not admission of a new public contract or erasure of the seven recorded failures. Run both version cells and checkpoint. Runtime code stays frozen.

2026-10-12T21:11:39Z: S1W7 native public-metadata/current-edit cases pass on2.1.3 in2.66s;2.0.51 receipt follows. These positive tests are separate from the seven legacy refusal/copy expectations; none of those was rewritten or skipped. Evidence stops atPLAINTEXT_PENDING, not generic final metadata removal. Native table/column identity, ordinal, type/collation/default/ACL/comment/statistics/storage/compression and exact public/protected values match in this finite fixture.

Pending action-time approval: user message Sentinel_0af68e22e6e081d1809780cc5d181f5d asks permission for a second disposable PostgreSQL16 cluster with fresh test-only logins and shutdown after recovery testing. Do not create it before approval. Existing-lab verification can continue.

## S1X defined: snapshot and phase-error storage observers

The remaining snapshot/audit failures assert bytea on the retained native placeholder. Correct their observed physical column only, preserving original snapshot-drain refusal, resume phase, actual database fault and expected bytea/text assertions. First modify and verify snapshot module; then separately audit phase test. Both version cells required; no runtime code changes. Seven legacy reverse-copy/refusal tests remain outside this correction and will stay visible.

2026-10-12T21:15:29Z S1X snapshot module9PASS in2.33s on2.1.3; now correcting only the phase-error audit physical-column observation, preservingSQLSTATE22012, original operation ID, exact prior phase, atomic rows and retry assertions. No product changes.

2026-10-12T21:18:15Z S1X verification complete: snapshot9PASS2.33s and audit40PASS3.75s on2.1.3; combined49PASS5.80s on2.0.51. Only the physical column observed after retained cutover changed; expected SQLSTATE, durable phases, snapshot refusal and retry semantics stayed unchanged. Seven legacy reverse-copy/refusal expectations are still not rewritten or skipped. Full suite rerun pending.

## S2 defined: actionable retained protected-SELECT schema failure

D-STALE-ATTACHMENT-DIAGNOSTIC-01: previously warmed encrypted factory reused after successful reverse returns raw PostgreSQL42703/SQLAlchemy ProgrammingError. Data remains intact, but it lacks Cryptalis's typed recovery guidance. Proposed bounded correction: translate only42703 for a currently owned retained-profile protected SELECT into a safe PolicyMismatch subtype, requiring rollback and current schema/deployment inspection. Preserve ordinary unprotected schema errors, uniqueness errors, disconnect handling and host exception chains. No extra SQL, new authority, automatic reattachment, query admission or crypto change. Do not claim pre-SQL stale-worker fencing or absence of races.

Separate candidate candidate-master-schema-errors-20261012 preserves integrated baseline as fallback. RED requires actual reverse then stale sync/async SELECT to produce the new typed safe failure; native public-column and unique-conflict controls must remain native. GREEN must preserve independent restored rows and usable rollback. Guard-removal mutation must restore the original failing behavior. Installed wheels on2.0.51/2.1.3, focused transaction regressions and affected real app required before promotion. Full seven-gate qualification remains UNKNOWN. Detailed throughput benchmarking NOT REQUIRED for this error-only dispatch slice; no latency improvement claimed.

Design sources: official SQLAlchemy2.0 DialectEvents.handle_error documentation and installed2.1.3 engine/base.py exception dispatch/cleanup; PostgreSQL16 transaction semantics. Alternative per-transaction catalog/lock revalidation would alter successful-path costs and broader fencing, so is deferred to a separately qualified design.

2026-10-12T21:22:34Z S2 RED:2 stale-factory cases fail with ProgrammingError on sync/async;2 native-error controls pass,1.59s. Narrow runtime correction implemented only in separate candidate sqlalchemy.py; source-mode GREEN pending before wheel build. No proactive fencing, auto-repair, query retry or broader authority introduced.

2026-10-12T21:32Z S2 focused verification: source GREEN8PASS2.93s; disabling only error-event registration yields4FAIL4PASS3.29s, exact restoration8PASS3.01s. This mutation demonstrates diagnostic activity, not a security-guard proof. Installed candidate edc94f93fca363025d3dd478ba1c2cd63e49a6b98dc8a16f2ed748c97146e699 passes81 focused cases on SQLAlchemy2.1.3 (12.60s) and2.0.51 (10.74s), including9 schema/native-error/host-handler cases plus transaction/thread/async cleanup regressions. All34 installed modules match source. Two offline wheel builds are identical;38 RECORD entries verified. Native42703/23505/22012 and host handler precedence remain checked. Copied FastAPI77-package environment has only Cryptalis replaced; pipcheckPASS. Full-app replay and full-suite reconciliation are pending. All production gates remain UNKNOWN.

2026-10-12T21:33Z S2 full-app replay:58 native,58 protected,58 package-free before removal and58 package-free after removal PASS,0 failures/errors/skips; outer1PASS28.08s. Installed34-module equality verified. Source unchanged; exact nonempty restoration and package absence are separately recorded by the existing harness. Full frozen installed suite now running; historical failures are not silently omitted.

2026-10-12T21:37Z S2 complete frozen installed suite:1696PASS,7FAIL,0SKIP,2 known fork warnings,270.73s. All seven remaining failures are the preserved legacy public-suffix copy/refusal expectations in test_deprotection_ordinals.py; none skipped or rewritten. Prior50 failures reduced by43 corrected physical-storage/fault observations;16 new profile tests pass. This is NOT full-suite acceptance. Separate retained native metadata/current-value oracles pass, but reconciliation of legacy semantics remains open. No newly observed runtime regression in this run. Exact failure inventory s2-full-failures.json.

2026-10-12T21:38Z S2 recovery checkpoint saved:2761276bytes,3399 checksummed files, library libfile_e2d824688afc81d1a5d3bb5509c031b9. Extracted candidate replay81PASS11.50s; all archive entries unchanged after verification. Original15-message mailbox SHA remains9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd. Fresh PostgreSQL cluster approval remains pending. Next: full second-version run and explicit legacy-profile compatibility reconciliation; no production promotion.

2026-10-12T21:44Z S2 full SQLAlchemy2.0.51 result:1678PASS,7FAIL,18SKIP,2 fork warnings,265.52s. Same seven legacy copy/refusal failures. The18 pre-existing skips are native2.1-only collection/session APIs; no skips added to hide failures. Two-version full-suite acceptance remains OPEN.

## S3 defined: public metadata through activation and final removal

S1W proof stopped atPLAINTEXT_PENDING. Extend separate synthetic native-oracle coverage through authorized existing-role cutover, PLAINTEXT_ACTIVE and REMOVED, including current public edits and wide values. Preserve original table/column identities, ordinal/type/default/comment/statistics/storage/compression and native values; verify owned metadata is absent. Existing role-retirement semantics remain explicit; do not assert the retired runtime keeps its old grants. Use existing fixture removal attestations as test inputs, not proof of an independently restored encrypted backup. Full application/backup evidence remains separately qualified. No runtime changes, no new credentials or cluster, no old tests removed. Candidate-master-removal-metadata-20261012 is separate; S2 source frozen.

2026-10-12T21:45Z S3:11 metadata tests PASS4.93s onSQLAlchemy2.1.3 and11PASS4.55s on2.0.51. Four new cases independently compare original table/column identity/type/ordinal/default/ACL/comment/statistics/storage/compression plus current public and restored protected values after REMOVED. Owned journal and payload/staging columns are absent. These four do not add a column grant to the retired role; intentionally retired access is not represented as preserved. No runtime edits; all34 modules match S2wheel. Original seven legacy failures remain unmodified. Source inventory8f0e87b875ed0c7fd040671f84f98fc536bf647a82b93f56b1fca8a9f6a74828.

2026-10-12T21:47Z S3 archive local/extracted verified:2769872bytes,3438files,SHAffd1e5268ac9e6cf4ea955961b1f5367f76869e4d1e509781c9eced410dcb0ca. Extracted11PASS4.89s. Library create returned internal error; exact-title reconciliation found the correct2769872-byte item libfile_c6657908555c81d18506ad5d6ea9eab9. No duplicate create retried; remote version unspecified.

## S4 defined: rerun exact historical compatibility operations on the integrated candidate

Historical159-operation/554-cell corpus has20 recorded DEFECT cells. Do not replace it with pytest counts. Copy six corpus harnesses to an isolated namespace, changing only candidate fixture import location and receipt filename prefix. Preserve operation IDs, expected admission/refusal and native-result/error/transaction oracles. Run complete selected corpus plus three original candidate preparation-boundary modules against installed S2runtime on both SQLAlchemyversions. Preserve old corpus and every failure; write separate current candidate results and exact harness provenance. No product runtime edits, public-profile promotion or expectation relaxation.

2026-10-12T21:49Z S4 core corpus:196pytest cases PASS27.63s on2.1.3 and196PASS28.21s on2.0.51. Independently merged92 original core operation IDs/368 exact cells:264IDENTICAL104REJECTED-LOUD0DEFECT. Exact key-set equality against historical core verified; exactly20 prior DEFECT cells now IDENTICAL, all other classifications unchanged. Remaining67 historical supplemental IDs/186cells are pending reconciliation, not counted as current. This finite core pass does not remove the seven legacy full-suite failures or promote public capabilities. Separate native oracles retain classification semantics; receipt/import-only harness diffs recorded.

2026-10-12T21:51Z S4 recovery checkpoint2796848bytes/3494files; extracted core196PASS28.57s and184classification cells verified on2.1.3. Three shared-prefix candidate receipt outputs were preserved under replay names, then originals restored byte-exact from archive; standalone original hash references stay valid. All archive bytes unchanged. Remaining67 supplemental IDs require reconciliation; next focus those exact inputs rather than inflation of coverage. No original mailbox/source commits or pushes.

## S5 defined: remaining historical supplemental compatibility cases

Re-run old UUID-text, native bulk-delete and warmed-mapper harnesses without changing expected classifications first. Only fixture import paths bind current candidate; old test assertions preserved. If an approved contract changed admission, record the old failure first, then require exact native result/state behavior under the current approved profile in a separate oracle. SQLModel uses only its supported2.0 environment; do not force2.1 dependencies. Reuse full frozen candidate native VARCHAR/public-type cases only after exact case/source correspondence is proven. Historical sparse cells remain sparse. No security-contract expansion, old-evidence rewriting or silent expected-failure suppression.

2026-10-12T21:53Z S5 historical refusal run on2.1.3:28PASS/15FAIL7.84s. All15 UUID cases fail solely because the old harness expects refusal, while current approved UUID-01 admits PostgreSQL-valid strings. Verified exact owner approval messageSentinel_e1abe646a87081d194a97aea302be80d (2026-10-11T06:48:53Z), including preserve-native-bind and independent canonical row authentication. Keep old failure evidence; add separate approved-profile oracle requiring exact native identity/value and unchanged driver-bound spelling on both paths. Bulk default refusal and8 warmed-mapper native comparisons pass. No runtime admission is changed by this slice.

2026-10-12T21:55Z S5 complete: exact historical159 IDs/554 key set matched;398IDENTICAL156REJECTED-LOUD0DEFECT. Changes are exactly20 former async DEFECT→IDENTICAL plus30 approved UUID refusal→IDENTICAL. Original UUID refusal harness15FAIL/28PASS on each version is preserved; current native-bind oracle15PASS2.19s on2.1.3, combined UUID/public49PASS5.84s on2.0.51. Public-only34PASS3.88s on2.1.3 (24corpus cells plus10oracle controls). SQLModel12PASS1.71s in supported2.0.51/Python3.14.8 app environment. Native VARCHAR40cells reused only after exact test-node PASS verification in frozen full suites. Default bulk20cases/version still refuse preSQL;8warm-mapper native+independent decoder cases/version pass. No new runtime changes. Blueprint and defect register updated to distinguish current from historical status; sparse historical cells remain missing.

2026-10-12T21:58Z S5 archive saved aslibfile_d022220ef99c81d18e14d8eb84616f6d:CRYPTALIS_MASTER_S5_COMPLETE_CORPUS_20261012T2156Z.tar.xz,2915204bytes,3579files,SHA2fd2baf252fd2be66d75b39d2ff279202fc40792f6072b3b9d6f5311b7e06fad. Extracted core+supplemental+VARCHAR replay293PASS44.18s; no archive checksum changed. Original core receipt bytes restored after preserving replay outputs under distinct names. SQLModel extraction replay running separately in supported2.0-only environment. No fresh-cluster claim.

2026-10-12T21:58:30Z S5 extracted SQLModel12PASS1.86s; all3579 archive checksums unchanged. Current complete historical corpus reconciliation is verified; production gates and seven legacy full-suite assertions remain open. Next recovery gate requires pending action-time permission for a fresh disposable PostgreSQL cluster/test-only logins. Do not create new credentials or silently substitute the existing cluster as clean-room proof.


## 2026-10-13 recovery and repository authority reconciliation

- Reattached S5 archive SHA256 verified: 2fd2baf252fd2be66d75b39d2ff279202fc40792f6072b3b9d6f5311b7e06fad. All 3579 manifest entries verified after safe extraction. This verifies recovered bytes; runtime replay has not yet run in this resumed environment.
- Latest master mandate is byte-identical to the archived master: a84484fb7423a26d979430034bde7e3ec678790f083852382a3cff36fcd11aee. Latest standalone checklist restored, preserving all earlier results and open gates.
- Owner clarification Sentinel_50860f088ea081d1a33f3da904406247 authorizes ongoing checkpoint commits/pushes ONLY to private debgh-workspace/cryptalis-research-lab. debrato2005/cryptalis remains read-only and the original mailbox remains immutable. This supersedes the temporary pause following the repeated master mandate.
- Two authorized non-sensitive connector probe revisions exist: 8995af2b67116777b605b882d5d2de851851790c and 47fcc38ccc1fdd3f648cfe896891bb44b9c9bf0e. Full candidate remote recovery remains pending; probe success does not establish reset-proof credentials or fresh-machine recovery.
- S5 recursive heuristic scan: 3814 file/archive members, zero findings for private-key blocks, GitHub token shapes, and credential-bearing PostgreSQL URIs. This is finite screening, not an independent secret audit. Private runtime homes and SSH key material remain excluded.
- Fresh second PostgreSQL cluster/new test-logins approval remains pending. Existing authorized lab work may continue after unchanged role preflights.

2026-10-13T07:22Z: Research repository checkpoint 6ac03d0af2190705f131bd1d55e3d88a253b2994 published by fast-forward with expected-head lease. All 12 archive parts independently fetched from the exact remote commit; GitHub-fetched restore script verified archive SHA256 and all 3579 entries in a new empty directory. Runtime replay PENDING, fresh-machine qualification NOT TESTED, credential survival across resets UNKNOWN. Older workspace inventory/history bundle remains pending separate preservation. Original repo HEAD and 15-message mailbox SHA reverified unchanged.

2026-10-13T07:25Z: GitHub-restored S5 wheel reinstalled offline into a separately copied dependency environment, Python3.12.14/SQLAlchemy2.1.3/psycopg3.3.6/cryptography50.0.2. First attempt failed due to default uv cache outside writable roots; package-origin guard correctly stopped before tests. Corrected only cache location and installation; unchanged two-role preflight PASS, 34 installed modules byte-match source, 20 schema/public-metadata tests PASS9.86s, server shutdown PASS. Full suite replay running separately. User authorized unattended recurring continuation; hourly schedule enabled, no uninterrupted-compute claim. New master/template/S5 attachments are byte-identical to recovered originals; additional toolkit is reference material, not permission to install agents or unrelated biomedical tooling.

2026-10-13T07:37Z: Complete GitHub-restored S5 installed suite on SQLAlchemy2.1.3: 1700PASS/7FAIL/0SKIP, 283.36s, 2 known fork warnings. Exact seven failure IDs equal frozen S2 inventory; 4 additional passes are S3 final-removal cases already in S5, not new fixes. Source bytes unchanged. Original history bundle verified and cloned locally without checkout; remote history upload incomplete after tool cancellation, awaiting explicit resume decision. Current S5 remote checkpoint remains valid. Highest open lifecycle issue: legacy copy/refusal assertions execute against retained-native fixture; existing independent retained-profile tests establish finite positive behavior, but old-layout compatibility remains unsupported and no full-suite PASS is claimed.

2026-10-13T07:42Z: Same immutable test_deprotection_ordinals.py SHA4855458d1b0847c353accab010b8521cc7374601f272340df8b2367ea8ea9cd5 passes10/10 in3.35s on historical legacy candidate, with unchanged two-role preflight and source stability. Current retained profile passes3/fails7 in full installed replay. Root cause verified as profile mismatch:5 legacy metadata refusals plus2 public-copy assumptions. Source-profile diagnosis preserved; no runtime changes or test-oracle edits. Legacy-layout upgrade support and full-suite acceptance remain OPEN. Second-version complete installed replay running.

2026-10-13T07:49Z: Original Git history bundle published in two batches of five files. Batch1 commit890db8251612012221c7486b19419048af8f0b1e and batch2 commitab588deb2864cfd6e3ef09d5332304b28f3a39b6: every added file independently fetched by exact commit and byte-compared. Cancelled blob checked first: GitHub404 confirmed absent before owner-authorized retry. Complete bundle parts match the locally verified, independently cloned original bundle. No original repository mutation. Complete second-version installed S5 replay:1682PASS/7FAIL/18SKIP,281.11s,2 known fork warnings; the18 skips are original native2.1-only APIs. Both version cells have the same seven legacy-profile assertion failures; no runtime source edits.

2026-10-13T08:30Z:166 of167 candidate files directly published unchanged and individually read back in small batches. Full 3579-file archive remains verified remotely. Last candidate file is the1746649-byte blueprint: initial shell transfer truncated; Git blob SHA mismatch caught before any commit/ref publication. Full content reassembled from bounded reads and blob SHA bce199ab572732de1be037bb35f4495aef622752 matches original. Final blueprint commit/readback pending. No completed database tests repeated. Source and publication inventories preserve every file/hash.


## S6: malformed protection-plan diagnostics (defined, not verified)

Source inspection found that MigrationPlan validates format/canonical bytes and UUID identities but lets parser, missing-field, wrong-type and UUID exceptions escape its documented TransitionFailure boundary. This is a bounded public diagnostic defect; it does not establish unauthorized database access or successful malformed-plan execution. Use a separate candidate-plan-diagnostics-20261013. Require RED for malformed inputs, unchanged admission for valid current plans, stable invalid_plan code, no input echo and no SQL during construction. Correction may only translate existing rejection paths; it must not admit legacy formats, alter crypto, loosen parser limits or automatically repair an artifact. Preserve S5 and all seven legacy-profile failures. Check affected real-PG plan/lifecycle controls after a source change; do not repeat completed tests merely for publication.

2026-10-13T08:38Z S6: RED8FAIL/2PASS0.46s confirms raw ManifestInvalid/ValueError/TypeError/AttributeError/KeyError. Separate candidate changes only MigrationPlan constructor rejection translation in migration.py; format, canonical-byte, nonzero UUID and parser bounds stay required. GREEN13PASS0.89s includes10 rejection cases and3 actual PostgreSQL planning/protection/reversal controls, unchanged dual-role preflight. Installed artifacts and affected lifecycle suites pending. No product release or legacy-format admission.

2026-10-13T08:41Z publication reconciliation: All167 unchanged S5 candidate files now exist directly in GitHub. Final five-file batch commit7b6502a14810905dedad6857be750a6e3db7e7f7 verified; oversized blueprint path resolves to blob bce199ab572732de1be037bb35f4495aef622752 and full1743865-character blob read matches original. GitHub content-by-path returns an empty body above1MiB; blob read is the verified complete route. Final receipt saved separately. Source S6 overlay and RED/GREEN evidence are checkpointed at23a928de8f523753e90ee318b3c1529eb1b8c2c3, five files each read back exactly. Candidate/ remains frozen S5 until installed S6 qualification.

Related S6 source-inspection question (OPEN, not yet reproduced): plan() accepts positive finite float rate inputs, while its shared artifact parser rejects JSON non-integer numbers. Fractional measured-rate compatibility needs a separate real planning experiment and a safe serialization decision; do not broaden parser numeric admission globally.

2026-10-13T08:44Z S6 installed2.1.3 full suite:1710PASS/7FAIL/0SKIP,287.14s,2 fork warnings. Exact seven failure IDs unchanged; all10 new diagnostic cases pass. Runtime34 modules match installed source and source hashes stayed fixed. Copied test bytecode retains earlier co_filename paths in traceback; generated caches preserved separately before next version run, with unchanged Python source. Same-host two offline builds yield wheel aa186579a457c1d6b749312071b1786871ee70b652cd3788f1db7cfd9f6da3f1 and sdist f790b3438146ef0e3c5df5a68aba7bfbf21ae5a59191fa94ad0589401926f291;38 RECORD entries verified. Experimental artifacts checkpoint5a25bd0c4c5f34526b40d0d06c91e55a73238f19 read back exactly. Second-version S6 qualification pending.


## S6 integrated diagnostic correction, 2026-10-13

Malformed protection artifacts previously escaped the MigrationPlan constructor as parser, UUID, missing-field or wrong-type exceptions. Ten public malformed-artifact cases establish8RED failures/2controls before correction. The bounded correction translates existing rejection paths to TransitionFailure(code=invalid_plan), suppresses underlying exception display and keeps format/canonical-byte/nonzero UUID/parser bounds unchanged. It does not authenticate an artifact, validate every semantic plan field, admit legacy formats or perform database work during construction.

Source GREEN13PASS includes3 real PostgreSQL plan/protect/reverse controls. Installed complete suites: SQLAlchemy2.1.3 1710PASS/7FAIL/0SKIP287.14s;2.0.51 1692PASS/7FAIL/18SKIP286.75s. All seven failures exactly match prior legacy-profile assertions; no new skip or expectation change. Original legacy test file independently passes10/10 on its original layout implementation. Full-suite acceptance and legacy-layout upgrades remain OPEN. Wheel aa186579a457c1d6b749312071b1786871ee70b652cd3788f1db7cfd9f6da3f1 reproduced twice offline; all34 installed runtime modules byte-match and38 RECORD entries verify. All seven production gates remain UNKNOWN.

Next: reproduce the separate fractional measured-rate planning concern without loosening manifest/lock numeric validation; preserve current correction and all historical failed evidence.

S6 integration means the bounded correction enters the experimental working candidate only. It is not full-suite acceptance or production promotion. Prior S5 source and artifacts remain in repository history and the independently restored S5 archive.

2026-10-13T08:54Z S6 integrated at62fe7f8c64e714cdb8782e4e149b8dc8fc86bb55; ten-file batch read back exactly. Composite recovery from GitHub-restored S5 plus4 exact-commit updates verifies all168 source/test/doc hashes. No repeated DB test or fresh-machine claim.

## S7: finite fractional measured-rate planning (reproduction first)

Public protection/reverse planners validate positive finite float rates but artifacts use the integer-only manifest parser. Reproduce rates20.5/10.25 using real native fixtures and verify read-only planning. Preserve S6; new candidate-rate-estimates-20261013 only. Do not globally relax manifest, compiler-lock, generation or identity numeric validation. Compare a field-scoped artifact parser with versioned decimal/rational representation; implement only a bounded correction to already implied rate input semantics after evidence. No novel crypto or numeric privacy claim.

2026-10-13T09:01Z S7 RED: real protection and reverse planners both fail on finite20.5/10.25 rates (2FAIL0.70s). Bounded candidate introduces a transition-artifact-only decoder using unchanged byte/depth/duplicate-key/integer/Unicode guards; positive finite floats allowed only at the two direct measured-rate fields and, for reverse artifacts, corresponding source-plan rate fields. Manifest/lock/descriptor decoders unchanged. Initial GREEN48PASS0.98s. Expanded run60PASS/1 fixture error2.66s: key_policies stores digest strings, not generation dictionaries. Corrected only that new test to mutate the actual policy-digest value to a float; original failure preserved. Expanded correction and scope-guard mutation pending. Integer artifact compatibility and older-reader refusal of new fractional artifacts must remain explicit.

2026-10-13T09:05Z S7 expanded source GREEN61PASS2.28s. Removing only the float field-scope guard yields3FAIL/12PASS1.94s at row-count, policy-digest and unexpected nested-rate paths; exact restoration15PASS2.30s. Existing integer-artifact roundtrip and manifest integer-only grammar preserved. Two offline builds produce identical wheel19efd5eafede07616c45c21be491fe85206f52cd0c1ada53fa76dee8ab2ea6e8 and sdist3e93ebc46749c9c42288815f18967043ac805944f5853fc2a87dc7a3a54043a1,39 RECORD entries. New artifact-only module raises installed runtime count to35. Installed full2.1.3 run in progress;2.0.51 follows. This does not prove old readers accept new fractional artifacts; they intentionally refuse them.


## S7 installed measured-rate correction, 2026-10-13

Both public protection and reversal planners previously rejected valid fractional measured rates after accepting their inputs (RED 2FAIL). A separate transition-artifact decoder now permits positive finite floats only in the two explicit estimate-rate fields and the corresponding reverse source-plan fields. Manifest, lock and descriptor numeric grammar remains unchanged. This is not artifact authentication or comprehensive semantic validation. Existing integer artifacts roundtrip unchanged; older readers refuse new fractional artifacts.

Source validation:61PASS; removal of only the field-scope guard produces3FAIL/12PASS, followed by exact restoration15PASS. Installed full PostgreSQL suites through unchanged dual-role preflights: SQLAlchemy2.1.3 1725PASS/7FAIL/0SKIP286.63s;2.0.51 1707PASS/7FAIL/18SKIP289.55s. Both have2 fork warnings. Exact seven legacy-profile failures remain unchanged; full-suite acceptance stays OPEN. Source stability verified; each server stopped cleanly. Reproducible wheel SHA25619efd5eafede07616c45c21be491fe85206f52cd0c1ada53fa76dee8ab2ea6e8. All seven production qualification gates remain UNKNOWN.

Next: independently reproduce the unqualified public-child table integration gap; protected-table physical binding already exists and must not be reimplemented or weakened. New-cluster/credential approval remains pending; existing authorized lab remains usable.


## S8 unqualified public-child binding prototype, 2026-10-13

Native differential reproduction:2FAIL2PASS1.47s. Both child DELETE and parent cascade fail only when the public-child mapper is unqualified. Prototype resolves native physical schema before lifecycle inspection restricts search_path, then freezes eligible same-compiled-schema ordinary public table names after successful validation. Protected mappings are excluded. Existing private opt-ins and locked inventories remain mandatory. No table-name guessing or schema translation.

First resolver placement still failed2/4 because the search path was already narrowed; moved resolution before inspection. Initial corrected4PASS. Expanded99PASS18.20s; async and missing-resolution controls8PASS3.10s. Earlier97PASS2FAIL was an over-specific new diagnostic expectation, preserved: DELETE admission can reject before mapping-fingerprint validation. Tests now independently verify typed DELETE refusal, PolicyMismatch on SELECT, zero emitted DELETEs and unchanged rows.

S8 remains a separate source prototype. Installed qualification and guard mutation checks pending. Integrated candidate remains S7. Original15-message mailbox SHA2569b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd reverified. All seven production gates UNKNOWN.

2026-10-13T09:47Z S8 installed complete:2.1.3 1760PASS7FAIL0SKIP314.69s;2.0.51 1742PASS7FAIL18SKIP302.26s. Exact legacy failure IDs unchanged;35 new cases pass in both. Runtime35 modules match wheel; all before/after source hashes fixed. Pin-guard mutant2FAIL0.73s, exact restoration tested in full suites. Wheel504224d80ff095071039f691e5a742da8f46536bf73947e8a9e67cefc7677cba reproduced twice. Pinned upstream FastAPI application test now running with per-table schema assignments removed; application changes are external shim only. No new application claim until it completes; integrated candidate remains S7.


## S8 integrated public-table binding correction, 2026-10-13

Unqualified public-child mappings reproduced a native/protected discrepancy for direct DELETE and parent cascade (2FAIL2PASS). Attachment now resolves ordinary direct public tables on the original runtime search path before lifecycle inspection, then freezes eligible mappings only inside already compiled schemas after validation. Protected models use their existing lock binding. Missing resolutions are not guessed. Schema/name drift rejects. This grants no public DELETE capability: existing private allowlists, grammar, OID checks and locked effect inventories remain required.

Installed SQLAlchemy2.1.3:1760PASS7FAIL0SKIP314.69s;2.0.51:1742PASS7FAIL18SKIP302.26s. Both retain2 known fork warnings and exactly the prior seven legacy-layout failure IDs. All35 new cases pass in both; installed35 modules and before/after source bytes match. Pin-guard removal fails2 tests, and exact restoration is covered by both full suites. Wheel504224d80ff095071039f691e5a742da8f46536bf73947e8a9e67cefc7677cba reproduced twice offline.

Pinned FastAPI7257e606cb94eada1dca40173e2b7f99dd549bc6 with original unqualified mappings:58 native,58 protected,58 package-free before removal and58 after removal PASS, each0 failures/errors/skips. Upstream source edits0; manual table-schema assignments0. Independent decoded7-user/7-item corpus, decrypt-back and real pg_dump/psql restoration match exactly; old encrypted restore fails REMOVED publication check. This is same-host synthetic evidence. Private one-hop cascade, explicit C collation,13 bootstrap/4 fixture lines and operator grants remain. The plaintext role was reused, not newly created. New cluster/credentials approval remains pending.

Full-suite acceptance, legacy-layout upgrade coverage and all seven production gates remain OPEN/UNKNOWN. No production deployment, generic cascade capability, online migration or external-key-custody qualification follows. Next: reconcile remaining integration friction and lifecycle qualification, preserving the seven unmodified legacy assertions and exact frozen compatibility corpus.


## S9 rate-estimate overflow correction (separate candidate)

Public protection/reversal planners expose OverflowError for huge integer rates and subnormal positive finite rates:4FAIL1.12s. Integer bounds now precede float conversion; only estimate arithmetic overflow/out-of-range counters translate to typed unrepresentable_cost_estimates. Existing formulas, artifact counter bounds, manifest grammar and key-provider exception handling unchanged. Source29PASS then36PASS; final14-case dedicated suite1.96s includes empty-table minimum float and representable maximum float/integer controls. Two offline builds match wheel27d62803d9c6f692d7fa91499983e9e7fcd9fb0c410065fb1223489ffb1da165,39 RECORD entries. Installed2.1.3 suite running;2.0.51 follows serially. S8 remains integrated. These estimates are not qualified performance bounds; all seven production gates UNKNOWN.

2026-10-13T10:03Z S9 installed2.1.3 complete:1774PASS7FAIL0SKIP301.57s,2 known fork warnings; exact prior failure IDs and source stability verified.2.0.51 running serially. S9 source/evidence9-file batch038ba6616d54c3c445ad9b8ec9733ac56fd70f39 and2-artifact batch3b476ed8d0b1f764ed155a7b8578793947dad960 both read back exactly. Integrated candidate remains S8. A new retained-layout warm search benchmark is prepared for execution only after current DB session ends; existing historical cache benchmark is not reused because it targets a different implementation/profile.


## S9 integrated planner numeric-rejection correction, 2026-10-13

Both public planners leaked OverflowError when converting oversized integer rates or forming duration estimates from positive subnormal rates (4FAIL before correction). Rate integer bounds now precede floating conversion. Duration-only arithmetic translates overflow or out-of-artifact-range counters into TransitionFailure(unrepresentable_cost_estimates), suppressing raw numeric exceptions. Representable max integer/float inputs and zero-row subnormal rates remain accepted. Host rate estimates, formulas, confidentiality and artifact parser grammar are unchanged; these estimates are not performance guarantees. Provider calls are not inside the numeric exception handler.

Source29PASS then36PASS; final dedicated14 cases PASS1.96s. Installed2.1.3:1774PASS7FAIL0SKIP301.57s;2.0.51:1756PASS7FAIL18SKIP312.37s, each2 known fork warnings. Same seven legacy-layout failure IDs; full-suite acceptance stays OPEN. All35 installed modules byte-match and source hashes remain fixed. Repeated offline wheel SHA25627d62803d9c6f692d7fa91499983e9e7fcd9fb0c410065fb1223489ffb1da165;39 RECORD entries. All seven production gates remain UNKNOWN.

Next: run the separately prepared retained-layout native/driver/attached benchmark, with exact results and bounded warm same-host measurements. It does not reuse obsolete cache-profile benchmark assumptions. No production latency or throughput claim follows from the result.

2026-10-13T10:13Z S9 integration commit ae24f8c125e52ca921061de5c5d6bc94981b4578 read back10/10 files; composite recovery174 source/test/doc hashes PASS. Retained-layout benchmark1000 rows,5 alternating blocks,40 measured samples per cell,1800 observations per dependency version; exact native/driver/protected results match. Warm median-of-block-median milliseconds:2.1.3 point0.171native/1.930protected, equality143rows0.372/8.257, IN286rows0.614/13.861;2.0.51 point0.175/1.794, equality0.396/8.159, IN0.657/13.759. Same-host synthetic, fixed statement objects; no production latency, throughput or tail qualification. Remaining overhead is material; a separate instrumented profile is running, with no cryptographic or validation bypass.


## S10 profile-directed tuple allocation experiment

S9 profiles identify repeated CF1 tuple serialization among result-path costs. Separate S10 candidate changes only tuple_bytes implementation to one-pass prefix/part references plus a single join. Exact uint32 wire format and strict bytes-only validation preserved; no caches, retained keys, crypto primitive or authentication changes. Independent writer132 cases including8MiB input and7 invalid types; targeted151PASS7.64s. Three-way pure function comparison: original1513ns,one-pass947ns,bytearray1289ns median;8MiB value peak traced allocations16,777,664 /8,388,864 /16,777,374 bytes. Same-host micro observations, not product speed proof. Repeated offline wheelf773483c07aa97d588585acb69c55d988263ed56713b214d62393d161458a9b6. First installed retained benchmark exact results PASS; native controls sped up too, so an S9 baseline return is required before causal attribution. Integrated candidate remains S9; full installed qualification pending.

2026-10-13T10:30Z S10 installed2.1.3:1776PASS7FAIL0SKIP301.99s, same known failures and stable source. Same-session7-block encoder comparison: point original1.732ms/new1.774ms (3/7 favorable; no benefit demonstrated), equality143rows7.641/7.186ms (6/7 favorable), IN286rows13.360/12.653ms (7/7 favorable). Exact results preserved. These small finite measurements support investigating multirow benefit, not a general speedup claim. Second installed dependency cell now running.

2026-10-13T10:44Z ledger correction: front requirement/corpus/recovery/defect/performance/next-action tables reconciled with accessible current evidence instead of leaving template UNKNOWN values contradicted by historical appendices. Every objective and unchecked full-acceptance box is preserved; no gate promoted.


## S10 allocation correction verified, 2026-10-13

The tuple encoder now joins count/length prefixes and original part references in one pass. Wire bytes and strict bytes-only checks are unchanged. No key cache, compiled cache, nonce, AEAD, HKDF, authentication, key lifetime or validation change. Independent writer oracle includes132 cases and7 invalid-type controls. Focused source151PASS.

Installed full PostgreSQL suites: SQLAlchemy2.1.3 1776PASS/7FAIL/0SKIP301.99s;2.0.51 1758PASS/7FAIL/18SKIP303.38s. Both retain exactly the seven known legacy-profile failures and two fork warnings. Source hashes match; both servers stopped. Full-suite acceptance remains OPEN. Wheel SHA256 f773483c07aa97d588585acb69c55d988263ed56713b214d62393d161458a9b6; repeated offline build identical.

For an8MiB input, incremental Python-traced peak allocation fell from16,777,664 to8,388,864 bytes. This is not request RSS. Same-session seven-block paired IN2 medians:13.360 to12.653ms on2.1.3,12.359 to11.818ms on2.0.51;7/7 and6/7 favorable blocks. Point/equality results vary; no blanket speedup or production performance claim. All seven production gates remain UNKNOWN.

Next: implement the missing read-only pre-adoption scanner/doctor under explicit checked/unknown boundaries. Existing database only; second cluster and credential approval remains pending. Original online-migration workstream S6 remains OPEN; corrective slice numbering does not imply its completion.


## S11 advisory diagnostic currency, 2026-10-13

Reconciliation found an existing bounded source scanner, so it is retained instead of rebuilt. Its UUID literal finding still asserted that UUID-01 was unapproved and all strings refused, although the runtime had already admitted PostgreSQL16 UUID text. Its Core DML warning omitted the private bounded DELETE profile. Five new source-report regressions failed against S10.

The separate S11 candidate reuses the runtime UUID grammar for literal classification, retains a refusal for malformed text, and reports admitted text as requiring staging rather than granting admission. Default Core DML refusal remains; its remedy now explains that private DELETE needs exact target/effect-inventory/staging verification. No runtime query admission, crypto, source execution, SQL execution or privilege change is added by this correction.

Eight real native/protected point-read controls independently verify canonical, compact, braced and four-digit-group spellings recover the same UUID and protected values. Existing invalid-literal and source-sanitization controls remain unchanged. Focused41PASS2.23s. PostgreSQL16 primary source corroborates the alternative spellings: https://www.postgresql.org/docs/16/datatype-uuid.html . No novel grammar claim.

Repeated offline wheel SHA256 cbc0ba6a34bf4d8d9c617da881005f94625555868886dce7d1aef82cbc63d99a;39RECORD entries,35installed runtime modules byte-match. Installed full qualification pending. Complete unified doctor remains unimplemented; all seven production gates UNKNOWN.

S11 first installed full cell:1789PASS/7knownFAIL/0SKIP310.59s. Second installed cell running; S11 remains separate, not integrated.


## S11 advisory diagnostic currency, 2026-10-13

Reconciliation found an existing bounded source scanner, so it is retained instead of rebuilt. Its UUID literal finding still asserted that UUID-01 was unapproved and all strings refused, although the runtime had already admitted PostgreSQL16 UUID text. Its Core DML warning omitted the private bounded DELETE profile. Five new source-report regressions failed against S10.

The separate S11 candidate reuses the runtime UUID grammar for literal classification, retains a refusal for malformed text, and reports admitted text as requiring staging rather than granting admission. Default Core DML refusal remains; its remedy now explains that private DELETE needs exact target/effect-inventory/staging verification. No runtime query admission, crypto, source execution, SQL execution or privilege change is added by this correction.

Eight real native/protected point-read controls independently verify canonical, compact, braced and four-digit-group spellings recover the same UUID and protected values. Existing invalid-literal and source-sanitization controls remain unchanged. Focused41PASS2.23s. PostgreSQL16 primary source corroborates the alternative spellings: https://www.postgresql.org/docs/16/datatype-uuid.html . No novel grammar claim.

Repeated offline wheel SHA256 cbc0ba6a34bf4d8d9c617da881005f94625555868886dce7d1aef82cbc63d99a;39RECORD entries,35installed runtime modules byte-match. Installed full suites:1789PASS/7FAIL/0SKIP310.59s on2.1.3;1771PASS/7FAIL/18SKIP297.10s on2.0.51. Both retain exactly the seven known legacy-profile failures and two fork warnings. Source hashes unchanged and servers stopped. No full-suite acceptance claim. Complete unified doctor remains unimplemented; all seven production gates UNKNOWN.


## S12 separate doctor candidate, 2026-10-13T11:12Z

Added bounded declaration CLI and explicit-host pre-adoption doctor API. Static CLI never opens a database and returns exit3 for incomplete checks; dynamic API composes the existing read-only compiler and advisory scanner. No automatic application import, attach, migration, repair, role change or key access. Roles/provider/ciphertext checks remain NOT_INSPECTED, ready/complete remain false. Full OBJ-DX-02 remains OPEN.

Source169PASS6.24s; read-only guard removal2FAIL, exact restoration14PASS0.43s. Reproducible wheel db6e83817fd4bad3e9be8f98b9aebbbc5641ac38f09e64e94ab11be84b77e332,40RECORD entries and36installed modules byte-verified. First installed full dependency cell running. S11 remains integrated.


## S12 bounded doctor verified, 2026-10-13

Partial OBJ-DX-02 implementation: cryptalis doctor declaration.json --json checks only product declaration grammar and returns exit3 for valid-but-incomplete inspection. Explicit-host cryptalis.doctor.doctor(...) adds native pre-adoption compiler admission and supplied-source compatibility inspection. It never imports application source by name, calls attach, migrates, repairs permissions, reads application values or accesses keys. Roles/provider/ciphertext checks are NOT_INSPECTED; complete/ready are always false. Active diagnostic mode rejects explicitly. Full doctor objective remains OPEN. See docs/doctor.md.

Source169PASS6.24s; removing existing read-only enforcement/assertion makes2 new controls fail; exact restoration14PASS0.43s. Installed console entry point returns expected incomplete report without modifying input. Installed full suites: SQLAlchemy2.1.3 1803PASS/7FAIL/0SKIP305.74s;2.0.51 1785PASS/7FAIL/18SKIP309.25s. Exact same seven legacy-profile failures, two fork warnings, unchanged source hashes; both servers stopped. Repeated wheel db6e83817fd4bad3e9be8f98b9aebbbc5641ac38f09e64e94ab11be84b77e332;40RECORD entries and36installed modules verified. All seven production gates remain UNKNOWN.

Read-only is a bounded database safeguard, not a sandbox for trusted host callbacks or a guarantee of zero disk writes. No production/fresh-cluster/provider qualification follows. Next: extend diagnostic coverage only with exact lifecycle/role/provider contracts and preserve the open independent-review and fresh-cluster requirements.


## S13 active deployment doctor, 2026-10-13

The explicit-host doctor API adds phase="active" with deployment=(plan,pin) and the planned runtime engine. It reuses existing check_attachment policy, requires an ACTIVE matching pin and matching declaration, and owns a PostgreSQL-enforced REPEATABLE READ/READ ONLY transaction. It checks active catalog/journal/pin consistency and the existing planned-runtime effective-permission/routine policy. It does not call attach, change mappings, grant privileges, inspect provider custody or authenticate row ciphertext. The host remains responsible for authenticating the external pin; later schema/permission changes are outside the snapshot. Full doctor and all seven production gates remain OPEN/UNKNOWN.

Three new controls failed before the API extension. Source17PASS then expanded62PASS. Omitting only the deployment inspector produces2FAIL (wrong owner and schema drift), followed by exact source restoration. Installed affected-path suites:157PASS10.89s onSQLAlchemy2.1.3;157PASS10.52s on2.0.51, zero failures/errors/skips. These cover both doctor modes, CLI, advisory source scanner, migration audit and9 new active controls. Both preserve exact source bytes; PostgreSQL stopped. The full suite was NOT rerun for this isolated diagnostic extension; last full baseline is S12 (1803/1785PASS and7 unresolved legacy-profile failures). Do not label S13 full-suite-qualified.

Wheel1600f108e2d6a44fecc5ecd7b2f38421492f58add9c9ddc764c9a498ad575cf9 reproduced twice;40RECORD entries and36installed modules match. No new cluster, credentials, crypto primitive, key cache or maintenance-approval exemption. Row integrity verification still follows the existing approved verification contract.


## S14 bounded ciphertext observation verified, 2026-10-13

The active doctor now accepts explicit ciphertext-audit opt-in, an existing trusted key resolver and strict global row/estimated-byte bounds. Active metadata and planned-role checks precede payload-only observation in one PostgreSQL REPEATABLE READ/READ ONLY transaction. Existing CF1 authentication and exact plan-bound key-policy/lease rules remain unchanged. No new credentials, key cache, provider, journal write or lifecycle certificate. Static CLI and default doctor calls do not access keys or row values.

CHECKED covers visible non-NULL cells only. NULL substitution, missing rows, same-context replay/freshness, external membership and provider custody are not proven. Any generation admitted by the policy can authenticate; active-write-generation readiness is not established. The estimated projection budget excludes metadata/lookahead and does not bound total network bytes, RSS, server work or elapsed time. Reports suppress data and arbitrary provider error text; comprehensive host logging hygiene was not tested. Full doctor and all seven independent gates remain OPEN/UNKNOWN.

Source controls: missing API3FAIL, then90PASS after one test-setup SQL correction (failed setup retained). Authentication removal1FAIL; byte-bound removal1FAIL; exact restoration19PASS. Full installed runtime suites: SQLAlchemy2.1.3 1831PASS/7FAIL/0SKIP315.40s;2.0.51 1813PASS/7FAIL/18SKIP315.98s. Both preserve exactly the seven legacy-layout failure IDs, two fork warnings and stable source hashes; both servers stopped. Full-suite acceptance remains OPEN.

Six additional tests were added after those full runs, with runtime bytes unchanged. All6PASS on each installed dependency cell (1.99s/1.81s): committed interleaved writer retains one snapshot, old-source SELECT independently denied with42501 while payload audit succeeds, audit-stage writes refused with25006 in normal/AUTOCOMMIT modes, global cross-table row bound and empty data. Replacing only REPEATABLE READ with READ COMMITTED makes the snapshot test fail (1 authenticated cell rather than6); exact runtime restoration and installed recheck PASS. Do not describe these six later tests as part of the earlier full-run counts.

Repeated wheel SHA25643c98cb0128c0a8cfda090febc8f485bd9b4883f3c9c047aefd155fe263ac080; sdist535e554d1df9e3fe59e59b4653e24d3c5ec6bbc1c86cf56ca598d8ae78209109.41RECORD entries and37installed modules verified. No audit latency benchmark, bigint/single-tenant audit-specific campaign or production-provider qualification yet. Native/CF1 independent fixture oracles are software checks, not external security review.


## S15 legacy maintenance bridge evidence, 2026-10-13

A bounded legacy→plaintext→retained-native journey is now exercised using complete version-pinned packages in separate interpreters. Text and VARCHAR(64) cases pass2/2 on each dependency cell (6.04s/5.61s). The source wrapper and nested current interpreter both use the unchanged role preflight; one coordinator serializes the cluster. Current installed S14 bytes match; original legacy source and mailbox remain unchanged. No runtime feature was promoted by this experiment.

Latest encrypted edits, wide public Unicode values, visible SELECT* order, native types/typmods/collations/index definitions and table OID survive legacy removal plus current re-protection/deprotection/removal. Independent CF1 decoders agree. Package-free legacy CRUD passes before/after removal; current package-free CRUD passes before removal. Actual encrypted legacy dump restore remains independently readable and is rejected by the newer current REMOVED pin. Physical suffix attnums are not preserved by legacy reconstruction.

An initial child setup omitted the required hide_parameters=True engine policy and correctly failed attachment; this was a harness correction, not a product security relaxation. The failed receipt is retained. Strict legacy suffix metadata refusal remains; no generic repair, transparent/online upgrade, secure erasure, fresh-cluster or production claim. Plaintext/WAL exposure requires explicit real-operation consent. Synthetic removal attestations precede the end-of-test restore and do not independently authenticate backups. Seven original ordinal assertions remain untouched and still fail on the retained profile. All seven gates UNKNOWN.

## Acceleration experimental checkpoint — 2026-10-13 13:12 UTC

S14 remains the integrated candidate; no worker branch promoted. Initial isolated branch snapshots were remotely byte-verified: ORM15d267ace19ced537f0b17e2878cc1b77c6884af(9 files), searchd97b58cd6b104d7a09feb1b23e64a546f8195cd6(10), lifecycle9de52eb6fff406e98e4a8c4476f1e4d1f31fd4d0(5). These snapshots precede later corrections.

- A expanded frozen public-only UPDATE suite:57PASS16.58s on SA2.1.3. A later pure custom-type default-path defect is confirmed and correction pending. Not integrated or protected-field bulk UPDATE support.
- B inactive rewrap successor plus existing preparation/lease suite:72PASS0.57s after provider-identity correction, under unchanged PostgreSQL role preflight. This does not implement active rewrap. Existing old workers are not retroactively fenced on reads by a new runtime check; persistent stale-write fencing and old-reader policy remain explicit publication blockers. No new role/credential created.
- C security/native focused suite:260PASS19.43s on SA2.1.3 and260PASS20.70s on SA2.0.51. Same declared seven-pair performance gate PASSED on2.1 but FAILED on2.0: equality median improves13.736%, only4/7 favorable pairs versus required6/7. IN2 improves26.217%,7/7; point regresses0.7595%, within10% bound. All exact native results passed. Promotion HELD; preserve failed gate, no lowered threshold or green-only reruns.
- All seven independent qualification gates remain UNKNOWN. Fresh-cluster/credential approval remains PENDING.

## S16 integration preparation — 2026-10-13 13:35 UTC

- A1 final mapping-type ordering correction:10 impacted controls PASS2.58s on2.1 andPASS3.08s on2.0, separate from preceding58-case runs. Guard-omission mutant yields2 failures1.65s. Frozen branch b3a3333d60e6db610d424e239023fcfd6e0d4a79,9files readback verified.
- B1 inactive successor corrected branch e0e66097d6f60726c6e536f487e89229795bba0b,5files verified;72PASS percell. Not included in integrated runtime.
- B2 REVERSE-PREDECESSOR-01:24FAIL5PASS15.54s before correction. Minimal exact-link/predecessor check:94PASS130.84s affected SA2.1 suite; expanded31PASS15.34s SA2.0;2 later abort/remove checksPASS1.36s SA2.1. Branch bf960b09b93ff2556cc1d252640ec7cc83fb7ba7,5files byteverified. Internal review found no false refusal in existing lost-commit/aborted-idempotence paths; this is not independent external review.
- C2 ORDER-TEXTUAL-LABEL-01:32FAIL58PASS10.21s on original wrapped ordering controls. First correction430PASS57.53s affected SA2.1. A related TypeCoerce wrapper gap then reproduced12FAIL18PASS3.35s; final correction pending. No protected ordering support is promised.
- C1 failed performance gate persisted at dd1ad0356bc9c167db6ca7219f47e414224f43e4,3files remotely verified. Excluded from integration.
- Coordinator owns candidate-accel-integrated-20261013 (verified S14 derivative plus A1/B2/C2 changes). Preliminary offline wheel/sdist repeated builds match; final C2 correction requires a new immutable build. No promotion or combined full-suite result yet. S14 remains highest integrated checkpoint.

## Expanded six-worker mandate — 2026-10-13 13:47–13:53 UTC

Owner attachment libfile_3ebf892c22c481d1be7f16a37a483245 authorizes expansion. Actual supported limit is7 concurrent agents total, permitting6 workers plus coordinator, not8 workers. Three new workers successfully launched: D online enumeration/capture, E defensive independent internal review, F developer experience/framework integration. A retains ORM; B lifecycle/legacy/rotation; C search/security/performance. Coordinator owns builds/release evidence/integration/Git; production custody research remains shared B/C/coordinator. No separately billed external service or new computing infrastructure started; native-agent billing/allowance not exposed.

Measured9CPU threads, one-minute load0.41, available memory8599264kB (~8.2GiB), free disk24.39GiB. Three additional private branches created from286afef6d183411a59f0af399ef21c224a0e9cbe: accel/online-20261013, accel/security-20261013, accel/developer-experience-20261013. New E/F source copies verify183/183 S14files; D takes exclusive ownership of B's separate online-enumeration copy after explicit handoff. SharedPG tests remain serialized through unchanged preflight/lock. Throughput benefit of expansion is not yet measured.

S16 combined installed validation completed:2047PASS7FAIL0SKIP381.08s onSA2.1.3;2029PASS7FAIL18SKIP362.47s onSA2.0.51,2forkwarnings each. Exact same7legacy profile assertions fail; do not label fullsuite green. Package-origin check matches all38modules; wheel d69904464fd70a49a559329536dee2ffa11876afb8dc993fe5ee2b285973fd85 andsdist ecaa571f4855e9cbefebf298a7db2c5b4c5ad0e6f16722e4213dd3a334c72266 repeatedbuildidentical,42RECORDentries checked. RealFastAPI replay is in progress againstS16 using existingPython3.14appcell clone;77dependencyversions identical andpipcheckPASS.

Promotion remains HELD pending independent internal E review's unprojected protected FROM-label ordering hypothesis; no confirmed result yet. All seven independent production gates remain UNKNOWN. Historical legacy test receipts do not certify B2predecessor safety; B is reviewing a separately versioned legacy safety derivative and explicitS16bridge. S14 remains latest promoted runtime.

## Expanded verification checkpoint — 2026-10-13 14:27 UTC

S16 remains HELD, not promoted: both installed full receipts2047/2029PASS withsame7legacyfailures, plus unchangedrealFastAPI58x4PASS. E's separate oracles confirmed30 further missing textual FROM/GROUP refusals. A2 found4 native driver-error transaction-state mismatches. These are corrected in experimental successors; no silent acceptance of S16.

- C3:204PASS23.30s SA2.1,349affectedPASS43.31s SA2.0. Finite variant inventory then found DISTINCT ON/window/ordered-aggregate omissions: initialremaining80cases32FAIL48PASS included12 invalid native WITHIN GROUP fixture cases. The corrected12-case subset yields4 genuine missingrefusals/8PASS. C4 reviewed local-scope correction passes284cases31.08s SA2.1;48warnings are upstream legacyDISTINCTON deprecation. SA2.0 andcombinedregression remain pending.
- A2: initial4FAIL2.15s, minimal4PASS2.01s. Expanded3FAIL52PASS17.97s contained cancellation-phase and unreachable driver-hook fixture errors. Native before-flush cancellation correction passes bothcases; finalization proof now explicitly injects a synthetic failure only after genuine native result completion, not a claimed natural psycopg fault. Final result pending.
- F1 engine logging preflight:76PASS plus18subtests8.34s underrealPG/unchangedpreflight; pure18cells and guard-omission sensitivity pass bothversions. Branchf45f10c988e0d0212d12a8fb99676309b36eac39,9files exactreadback. Notyetcombined.
- B4 complete separate legacy-safety derivative:26FAIL15PASS20.61s beforeminimalpredecessorcorrection;41PASS17.72s SA2.1 and117affectedPASS134.17s SA2.0,including10unchangedhistoricalordinalassertions. Explicit-target bridge prepared, notrun againstfinalcurrentcandidate. Legacyartifactformats/layout2 unchanged.
- D1 finite online enumeration research:31PASS2.65s;4independentobservercontrolsPASS0.36s;fourone-omissioncopieseachfail fullstage/native comparison(0.12/0.18/0.17/0.15s). Branch201ab4e9e3ddba749167ed472237390713b6a973 preservesexactsource/evidence;186-filecompositerestore verified. No productioncapture/CF1/cutover/scan-removal/onlinequalification.
- D2 independentCF1decode prerequisite:workerreports196purechecks,8frozenvectors+20int64vectors,onebindingomissiondetected; noD1hook/provider/productintegration.
- F2 KMS-boundary research:workerreports13puretests percell,sixguardomissionsdetected;synthetic/provisionalcontext, noSDK/transport/liveKMS/runtimeprovider. G-PROVIDER remainsUNKNOWN.

Freshcluster/credentials/liveprovider approvals andexternalreviews remainpending;allsevenindependentgatesUNKNOWN. The hourlytaskprompt nowreflectssixworkers;24/48/72auditdeadlineunchanged.

## S17 composition qualification — 2026-10-13 14:42 UTC

- C4 final bounded PostgreSQL receipts:284PASS31.08s SA2.1 and401PASS28SKIP45.51s SA2.0; skips are unavailable native2.1 APIs. Independent internal review found no actionable blocker; not independent external qualification.
- A2 final20cases PASS8.15s SA2.1 andPASS7.90s SA2.0. Synthetic post-result guard omission yields2FAIL1.23s at the exact root/SAVEPOINT quarantine assertion. This is synthetic fault injection after genuine result completion, not a natural driver-finalization failure. Original four driver-overflow mismatches and failed fixture stages remain preserved.
- Held S16 archived separately at6635f7b4e27db856079aa64aa890c622f18e9409; all10 remote file contents match. Main promoted runtime remainsS14.
- S17 composes A1/B2/C4/A2/F1, excludes C1 failed-performance optimization and inactive B1 successor. Runtime sqlalchemy SHA256 fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe. Clean three-way merges preserve exact independent oracle bytes.
- Repeated offline S17 wheel/sdist byte-identical;42 RECORD entries verified. Wheel b7b788edbab99a0110c35a6885c9b7387b34b0ed3a84507445b8cd423ff14aa0; sdist93f062d35d7a11274afa59d3891b497e8f6730046992f67526e418d82af4407b. Installed full SA2.1 running; SA2.0 queued. Full combined outcomes, real-app replay and explicit legacy-safety bridge pending. All seven qualification gates UNKNOWN.

## S17 bounded integration checkpoint — 2026-10-13 14:58 UTC

Final combined installed results: SA2.1 2235PASS7FAIL18subtests388.64s; SA2.0 2189PASS7FAIL46SKIP18subtests387.73s. The exact seven legacy suffix-copy profile failures remain untouched; this is not a green full suite. The46skips are unavailable native2.1 APIs. Same-host source and external-source stability pass.

Actual pinned FastAPI app passes58native+58protected+58packagefreebeforeREMOVED+58after,0fail/error/skip; no application edits,13bootstrap+4fixturelines. Explicit Ccollation/operator grants remain required. Existing plaintext role reused; historical receipt key new_plaintext_runtime_role is misleading and does not indicate role creation.

Complete B4 legacy-safety derivative to explicitly pinned installed S17 bridge:2PASS6.67s SA2.1,2PASS6.97s SA2.0. Text/VARCHAR latest values and schema checks, package-free removal and old-backup stale-pin refusal remain bounded maintenance evidence, not online/generic migration or fresh-cluster recovery. All five sessions source-stable and stopped.195-file composite source restore verified.

Source staged in two remotely byte-matched batches on accel/integration-s17-20261013:1360c75cd7893ab3fba0b217817417801e59dcd7 then2ae4048a5b9eb4384db56a547b8245b4848b2622. Artifact/evidence publication and final main promotion verification pending. C4 experimental commit34126c1b0b4dc681999c4e18390c5d0ebca580fb; A2 9a1d1e6dc28c82153750962162e5a40cc0731584; B4 47fe55039398e83f1a44bf4a1f5340c094dc3cb0. Each10files read back exactly. All seven full gates UNKNOWN; original mailbox unchanged.

## Publication decision — 2026-10-13 15:02 UTC

S17 research branch checkpoint ab40f030f377de564b7db58925ec76e919e4910c remotely verified: both artifacts, all17changed source files and195-file restored composite. Main promotion was denied by action review because research checkpoint authority did not explicitly cover moving an unqualified candidate onto main. Explicit user approval requested; no bypass/retry. Main remains123bceafa969c3d9e992768be612b7efb7cb0a07 with S14 runtime. Continue independent isolated work.

## Independent post-S17 slices — 2026-10-13 15:18 UTC

- A3 new native optimistic-versioning oracle:4PASS1.78s SA2.1 and4PASS1.47s SA2.0. Exact integer version_id_col, ordinary stale UPDATE/DELETE, sync/async, root transactions, rollback/retry and independent stored-value verification.195inherited S17files unchanged. Does not expand private bulk UPDATE or qualify all version generators.
- B5 initial four new reverse/ACL oracles plus affected controls:35PASS11.85s SA2.1 and35PASS11.21s SA2.0. Internal independent review confirms exact historical7failures remain, native catalog/value assertions genuine. Observer caveat: column-name checks and last-rowcount alone do not prove all fetched public bytes absent; stronger observer is being prepared, no runtime defect claimed.
- D3 isolated captured-text CF1 handoff:24PASS2.08s SA2.1 and24PASS2.65s SA2.0. D1capture/enumeration unchanged, D2 decoder independently verifies final current frames and rejects six corrupted/incomplete alternatives. Synthetic one-field/storage-only finite research; no online cutover/publication, process-death, live provider or performance qualification.
- C5 separate no-textual-reference admission fast-path hypothesis: deterministic100/100 redundant walks removed in in-memory experiment, existing admission counts preserved; pure predeclared gate FAILED SA2.0 IN2 consistency7/9 versus8/9 required. Runtime unchanged; no DB benchmark or promotion. C1 also remains held.
- D2 offline oracle published b132ba2b9e0fee260a736e82c9b729b02c435d84,4files remote-byte verified. F2 offline provider shape validator published a5b895d65d379d58fecdbe3ba85ff76bb0a80b32,9files verified. F2 internalreview found no actionable gap in narrowclaims, but authenticated provider binding/transport association/lease/cancellation/fork/rewrap/publication remain unproven; context metadata notapproved for real provider.

## S18 integration preparation — 2026-10-13 15:46 UTC

F3 explicit offline setup diagnosis resolves existing mapped selectors and checks local engine logging without connection/key access, model/schema duplication or transition authority.14puremethods percell and62affectedPGtests+21subtests percell PASS7.41/7.07s. Internalreview found no actionable bounded blocker. No measured integration-line reduction or new real-app replay is claimed. Exact8-file research snapshot4129f952d78a5f94612111811462d5fc5c263415 remote-byte verified.

S18 composes exactF3runtime with S17 and adds A3/B5finalindependentoracles;201files,only doctor.py/new_doctor_setup.py runtimechanges. Offline repeatedwheel c0f71703e6f98845f405027f5f431ec2f0b8274b7f7d79914bfde0371504353d andsdist ee530e15cf301c5f77775c054defa82522be05ec483b59b35596bf1d760edf5a match;43RECORDentries and39installedmodules verified. InstalledSA21 full2259PASS7samelegacyFAIL39subtests393.34s;SA20 running. S18notyetpublished/integratedqualified.

B5strongerobserver37PASS10.93/10.19s plusfinalfirst-backfill1PASS0.62/0.71s,bycomposition; old35case/37casebytes preserved. B5branch5f18111b014b1c6e589bb425e3ead4d7e7239726,10filesverified. D3atomicitycontrol1PASS0.39s andisolatedsplitretirement1FAIL0.40s precisely independent decoded==native. D3source/evidence10filecommit8a8fd8d5c9278d84aee7e06adcf2b329104852a8 and4fileproofcommitd3718eba3ca543995a9a937112b5f83f284c53b9 verified. Initial network-error ref update reconciled via missingbranchfile before exact expected-head retry; no duplicatecommit.

C6 onepredeclaredidenticalcodeA/A diagnostic found9/36pairedtiming differences>=10%;GC overlaps one largegap,remainingcausesunresolved. It cannot explainawayC5failure. No speedpromotion.15:27resource sample9CPU/load0.375/8.5GiBavailable islatercontext only,notcausal evidence. Mainapproval remains pending; originalrepo/mailbox unchanged; all7gatesUNKNOWN.

## S18 bounded results — 2026-10-13 15:55 UTC

InstalledSA2.1:2259PASS7unchangedlegacyFAIL39subtests393.34s. InstalledSA2.0:2213PASS7sameFAIL46nativeAPI skips39subtests393.95s. ActualpinnedFastAPI58x4PASS,0fail/error/skip,existingrole reused. All3sessionssource/externalstable andstopped.201-filecompositerestore verified. S17explicitlegacybridge retained asprior evidence; unchanged lifecycle/adapter/cryptobytes,notrelabeledasnewS18bridge.

Sourcepublishedonlyonaccel/integration-s18-20261013 in10-fileand3-filebatches b6324897a33f7f494707d8ba5c3a0dfbc362940f then5492cc04ee6c5d6696c9e9fc261f12fa61236043; exactreadbackpassed. Artifact/qualificationpublicationpending. No mainretry/attempt. Originalmailboxunchanged;all7qualificationgatesUNKNOWN.

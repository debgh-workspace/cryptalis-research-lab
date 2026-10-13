# CRYPTALIS — LIVING BUILD CHECKLIST

> **ACTIVE ENGINEERING LEDGER — integrated qualification in progress.** Dot must populate this file from the actual repository, newest recovered candidate, approved decisions and executable evidence before changing any statuses. Do not overwrite without first merging evidence.

## Identity and recovery

- Last updated UTC: `2026-10-12T21:58:30Z`
- Public GitHub SHA (read-only rechecked): `2ff72ea4fe7871f31a9fabbbf63f19a5cc714e43` via git ls-remote,2026-10-12T20:14Z
- Integrated candidate ID and source-tree SHA-256: `candidate-master-corpus-20261012`, `e33f65050a966056ca2c27c52289509be9615d1dcf8ff013043fd28494902486`. Runtime remains S2 wheel edc94f93fca363025d3dd478ba1c2cd63e49a6b98dc8a16f2ed748c97146e699; S3–S5 verification/evidence changes only.
- Preserved 15-commit mailbox SHA-256: `9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd` (freshly checked)
- Runtime versions / PG16 config / runtime role preflights: Python3.12.14, SQLAlchemy2.1.3, psycopg3.3.6, cryptography50.0.2, PostgreSQL16.15; unchanged dual-role preflight PASS; full durable-config inspection pending
- Last verifiably restorable recovery archive and SHA-256: `CRYPTALIS_MASTER_S5_COMPLETE_CORPUS_20261012T2156Z.tar.xz`, `2fd2baf252fd2be66d75b39d2ff279202fc40792f6072b3b9d6f5311b7e06fad`;3579file checksums verified; extracted293PASS44.18s plusSQLModel12PASS1.86s. Existing isolated database only; fresh-cluster proof pending permission.
- Last successful durable archive synchronization: S5 `libfile_d022220ef99c81d18e14d8eb84616f6d`; canonical checklist `libfile_8ec61502ba4481d18c8075b78eb2c33a`; next replacement guarded at version5.
- Execution wrapper: unchanged toolchain/lab_session.py with installed candidate and dual-role PostgreSQL preflight; exact run evidence under master-s2-*; no concurrent database sessions.

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
| [ ] | `OBJ-SEC-01` | Encrypt sensitive values in the trusted application **before PostgreSQL receives plaintext**, with proof at SQL/driver boundaries and independent connections. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-SEC-02` | Preserve confidentiality and authenticated integrity under declared tenant/field/row/key-generation context, detect swapped or malformed frames and unauthorized release. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-SEC-03` | Enforce application authorization, result lineage and tenant boundaries; handle SQL injection through parameterization, guarded operations and least privilege without falsely claiming that encryption prevents arbitrary application authorization flaws. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-SEC-04` | Detect plaintext bypasses via ORM, bulk DML, direct SQL, COPY, external writers, migrations, sessions, background jobs, triggers, caches, logs, exports, backups and privilege paths. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-SEC-05` | Keep payload/search keys isolated, never silently choose fallback keys, bound nonces/usage/leases, test memory/fork/cancellation/rotation and use robust existing cryptography. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R03 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-SEC-06` | Reduce equality, frequency and access-pattern leakage with a threat-modelled, independently benchmarked search-profile design; document residual leakage, low-entropy domains, adaptive leakage and query-pattern trade-offs. | RESEARCHING — candidate recovered; full-objective acceptance still open | R05 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-SEC-07` | Independent red-team/security, cryptography, SQL adapter, provider and supply-chain qualification; the seven gates pass only with real evidence. | RESEARCHING — candidate recovered; full-objective acceptance still open | R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Reconcile CF1, adapter and authorization guards against restored latest candidate |
| [ ] | `OBJ-QUERY-01` | Exact protected equality, `IN`, scoped uniqueness, SQL NULL/three-valued logic, empty lists, bound types, collision resistance/verification and concurrency races. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R05 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; reconcile complete S2 suite with compatibility corpus and remaining query gaps |
| [ ] | `OBJ-QUERY-02` | Ordinary SQL correctness: `IS NULL`, `IS NOT NULL`, `!=`, `NOT IN`, `IS DISTINCT FROM`, `IS NOT DISTINCT FROM`, nested Boolean expressions, aliases, outer joins, scalar/entity projections, relationships, subqueries. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; reconcile complete S2 suite with compatibility corpus and remaining query gaps |
| [ ] | `OBJ-QUERY-03` | Advanced SQL: ordering, keyset/offset pagination, ranges/comparisons, `LIKE`/`ILIKE`, prefix, suffix, substring, fuzzy, regex, full-text, `DISTINCT`, aggregates, `GROUP BY`, joins, JSON/array/numeric/datetime and other protected types. Each gets native semantics, a viable scheme/profile or an explicit, researched `REJECTED-LOUD` alternative—never silent omission. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R05/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; reconcile complete S2 suite with compatibility corpus and remaining query gaps |
| [ ] | `OBJ-QUERY-04` | ORM/Core and data-modification coverage: INSERT/UPSERT/UPDATE/DELETE, bulk DML, `RETURNING`, triggers, cascades, FKs, savepoints, retries, autocommit/isolation, idempotency and connection/transaction state. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; reconcile complete S2 suite with compatibility corpus and remaining query gaps |
| [ ] | `OBJ-QUERY-05` | Full, versioned compatibility corpus and pre-adoption read-only scanner, with exact native-versus-protected classification and reproducible cases. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06/R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; reconcile complete S2 suite with compatibility corpus and remaining query gaps |
| [ ] | `OBJ-LIFE-01` | Declarative, deterministic, safe plan → apply → verify; schema/writer/permission inventory; irreversible-step preview and actionable diagnostics. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-02` | Resumable, byte-bounded backfill, full final integrity/metadata verification, journaling, restart and crash-safe atomic chunks, failure fencing. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-03` | **Near-zero-writer-downtime migration**: concurrent writes, captured changes, ordered catch-up, deletion/PK-change handling, stale-worker fencing, verification, short publish/cutover, recoverability and measured pause SLO. Preserve native semantics and current secure maintenance fallback until this is proven. | RESEARCHING — candidate recovered; full-objective acceptance still open | R04 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-04` | Parallel/adaptive migration and verification without double processing, lost updates, unsafe memory, or unbounded locks/WAL. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02/R04 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-05` | Exact decrypt-back of **current edited data**, constraints, types, defaults, order, indexes, FKs, views, ACLs, owners and permissions; complete metadata removal; fresh application operation with Cryptalis uninstalled. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-06` | Safe rollback, restore, redeployment, stale snapshot/pin refusal, retained encrypted-backup readers, RPO/RTO and deployment-disaster drills; no false secure-erasure claim. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-07` | Three separate key operations: root/wrapping rewrap, payload-key rotation/re-encryption and search-root reindex/rotation, with separate correctness and recovery proofs. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02/R03 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-08` | Real production KMS, initially AWS KMS where authorized, robust credential/region/outage/throttling/revocation/cost testing, with a provider-independent contract and no hard dependency on AWS for local functionality. | RESEARCHING — candidate recovered; full-objective acceptance still open | R03 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-LIFE-09` | Safe install, upgrades, compatibility across versions, decommission and explicit clean uninstall, including unsupported legacy-layout repair or a tracked safe alternative. | RESEARCHING — candidate recovered; full-objective acceptance still open | R02/R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recovered; complete native reverse/removal/metadata and clean-room recovery qualification |
| [ ] | `OBJ-DX-01` | Almost zero business/model/query changes; one manifest, named profiles, one attach call, usable status/plan/apply/verify/deprotect/rotate operations and precise startup feedback. | RESEARCHING — candidate recovered; full-objective acceptance still open | R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover pinned FastAPI harness and validate complete suite, then second application |
| [ ] | `OBJ-DX-02` | `cryptalis doctor`: meaningful read-only static **and** dynamic diagnostics, policy/manifest/schema/ciphertext/role/provider/compatibility checks, with clear limits and no silent repair of privileges. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover pinned FastAPI harness and validate complete suite, then second application |
| [ ] | `OBJ-DX-03` | Fully working independent FastAPI/SQLModel integration; a second unrelated application; measure source edit lines, dependency and deployment requirements. Extend thoughtfully to Flask and Django via actually suitable adapters. | RESEARCHING — candidate recovered; full-objective acceptance still open | R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover pinned FastAPI harness and validate complete suite, then second application |
| [ ] | `OBJ-DX-04` | Normal SQLAlchemy semantics: ORM identity map, lazy/eager loading, `Session.exec`, sync/async, pooling, migrations, background jobs, serializers, errors and result metadata. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover pinned FastAPI harness and validate complete suite, then second application |
| [ ] | `OBJ-DX-05` | Accessible, complete docs: one small quickstart, profiles, threat model, leakage, boundaries, operations, recovery, practical examples, diagnostic errors and learning walkthroughs explaining what/why/how for each slice. | RESEARCHING — candidate recovered; full-objective acceptance still open | R06/R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover pinned FastAPI harness and validate complete suite, then second application |
| [ ] | `OBJ-PERF-01` | Continuous native ORM vs driver-only vs protected measurements of p50/p95/p99, write rate, steady-state throughput, CPU, RSS/allocations, WAL, storage/index sizes, query plans, provider RPC and recovery costs. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R04/R05/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Freeze recovered source and comparable datasets before matched timing |
| [ ] | `OBJ-PERF-02` | Profile-guided optimizations in Python, SQLAlchemy, PostgreSQL and crypto: batching, psycopg pipeline/executemany, pooling, safe cache use, allocations, projections, indexing, native accelerators and bounded key caching. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R04/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Freeze recovered source and comparable datasets before matched timing |
| [ ] | `OBJ-PERF-03` | Multithreading, multiprocessing, async and adaptive worker processing with 1/4/16/saturation tests, isolation, retries, process/fork safety, backpressure, cancellation and measured speedup **or regression**. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R04/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Freeze recovered source and comparable datasets before matched timing |
| [ ] | `OBJ-PERF-04` | Performance targets on agreed comparable conditions: repository's current added read p95 ≤3 ms for point/equality, ≤8 ms for `IN`-20 and ≤2× protected-column-plus-equality-index storage. Define write-throughput and pause SLOs through a documented stakeholder decision; do not invent an approved target or relax an existing target because a test fails. Evaluate million-row scale and a documented growth path to billion-row workloads without claiming the latter has already been tested. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R06 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Freeze recovered source and comparable datasets before matched timing |
| [ ] | `OBJ-OPS-01` | Reproducible installed wheels/source releases, verified license, SBOM, dependencies/provenance, locked builds, supported-version matrix, rollback documentation and independent reviewers. | RESEARCHING — candidate recovered; full-objective acceptance still open | R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover latest archive; remove fixed-path and dependency-cache assumptions in restore tooling |
| [ ] | `OBJ-OPS-02` | Recoverable research environment, immutable evidence hashes, source-to-test traceability, live Markdown checklist and durable local/authorized remote snapshots. | RESEARCHING — candidate recovered; full-objective acceptance still open | R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Recover latest archive; remove fixed-path and dependency-cache assumptions in restore tooling |
| [ ] | `OBJ-RESEARCH-01` | Comparative, source-backed reverse engineering and potential novel mechanism research; demonstrate independent novelty/prior art and repeatable advantages rather than claiming novelty from an interesting idea. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R02/R03/R04/R05/R06/R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Integrate only qualified compatible mechanisms; preserve all open objectives |
| [ ] | `OBJ-RESEARCH-02` | One finished, coherently integrated **working software candidate** that passes its admitted native-compatibility contract, end-to-end reversible lifecycle, real-app adoption proof and all relevant acceptance gates before a qualified release. | RESEARCHING — candidate recovered; full-objective acceptance still open | R01/R02/R03/R04/R05/R06/R07 | S0-RECOVER then objective-specific slice | Scoped recovered/current evidence in S0–S2 ledger below; full-objective acceptance OPEN | NOT MEASURED on restored latest candidate; gates UNKNOWN | Integrate only qualified compatible mechanisms; preserve all open objectives |

## Ordered integration run board

| Work unit | Dependencies | RED reproduction | Candidate change | Native/real-PostgreSQL comparison | SQLAlchemy 2.0 / 2.1 | Mutation proof | Installed-wheel / real app | Before/after performance | Checkpoint archive | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `S0-RECOVER` | Authorized archives | N/A | No source edits until identity verified | Disposable DB smoke | NOT RUN | N/A | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S1-BULK-DELETE` | S0 | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S2-FASTAPI-E2E` | S1 | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S3-REVERSIBLE-LIFECYCLE` | S0,S2 | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S4-ROTATIONS-KMS` | S3 | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S5-QUERY-PRIVACY` | S0 and reviewed change | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S6-ONLINE-MIGRATION` | S3 and reviewed change | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |
| `S7-PERF-DX-ADOPTION` | Integrated safe candidate | NOT RUN | Not implemented here | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT MEASURED | NONE | OPEN |

## Compatibility corpus — finite, versioned facts

- Corpus version and content SHA: `UNVERIFIED`
- Unique operation IDs: `UNKNOWN`
- Executed native-vs-protected cells: `UNKNOWN`
- IDENTICAL / REJECTED-LOUD / DEFECT / NOT RUN: `UNKNOWN / UNKNOWN / UNKNOWN / UNKNOWN`
- Exact cells added by latest defect: `NONE RECORDED HERE`
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
| `D-BULK-DELETE` | VERIFY AGAINST LATEST CANDIDATE | Same ORM bulk + cascade effects | POTENTIALLY HIGH | UNKNOWN IN CURRENT CANDIDATE | NOT VERIFIED | NOT RUN | Priority 1 |

## Performance and scale ledger

| Benchmark ID | Machine / corpus / source hashes | Native ORM | Driver-only | Protected | p50/p95/p99; units | Throughput; resource / WAL / index | Run order and spread | Regression / decision |
|---|---|---|---|---|---|---|---|---|
| `PERF-BASELINE` | UNVERIFIED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | NOT MEASURED | Reproduce matched before/after |

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
| `G-ADAPTER` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |
| `G-CRYPTO` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |
| `G-QUERY` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |
| `G-LIFECYCLE` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |
| `G-PROVIDER` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |
| `G-POLICY` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |
| `G-RELEASE` | UNKNOWN | Reconcile `docs/status.md` gate criteria; prove current candidate | UNKNOWN | Record exact missing evidence |

## Recovery/archive ledger

| UTC | Archive name + SHA-256 | Candidate source hash | Included file count | Fresh extraction DB/smoke | Durable location / verified sync | Result |
|---|---|---|---|---|---|---|
| NOT STARTED | NONE | UNKNOWN | UNKNOWN | NOT RUN | NOT VERIFIED | OPEN |

## NEXT ACTION (top five; update after each slice)

1. Reconcile the latest approved files, current public GitHub and recoverable candidate identities.
2. Prove full-source archive recovery in a fresh environment with disposable PG16 preflight.
3. Reproduce and safely fix the highest-priority remaining bulk-delete/teardown defect against native SQLAlchemy.
4. Verify unchanged FastAPI protected suite including teardown and complete reversible workflow.
5. Integrate proven safety fixes, then resume key lifecycle, advanced-search and online-migration workstreams.

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
| TO POPULATE | NONE ASSERTED HERE | UNKNOWN | UNKNOWN | Continue after baseline reconciliation |

## Changelog

- **Template created:** No actual source implementation, test or release qualification is claimed by this document.

## Current recovery event

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

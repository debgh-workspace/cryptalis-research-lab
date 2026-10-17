# Current 34-objective evidence/status audit

Snapshot: 2026-10-17 15:11 UTC. Source-only review; no tests, code edits or authoritative-ledger edits.

## Bottom line

All34 objectives remain active and all seven independent gates remain UNKNOWN. No percentage-complete score is justified by finite test counts. The new substantive progress is a missing scanner diagnostic corrected through the actual report path, exact combined-source recovery, and bounded same-host packaging. Recovery/rotation/online capabilities, independent security/provider/release qualification and operational adoption remain substantial product work. Message improvements do not implement recovery.

Authoritative inputs: CRYPTALIS_BUILD_CHECKLIST.md snapshot SHA256 d6ca7d36183d2de94166c95e8faffbf722a20cfbc71b51e580ff142e1a533ab6 and CRYPTALIS_DEFECT_REGISTER.md SHA256 2c8c04b0b838d4f89e3695f2d7aabd671833844941b62cf6ad99e28838358dfa. Checklist front is dated Oct16 and later entries supersede individual progress facts; defect front/latest14:22 entry are older than several accepted results. This report reconciles those dated facts without rewriting either file.

## Exact objectives retained

Names below are copied verbatim from the authoritative mapping. Every status is incomplete at full objective scope; finite verified slices are distinguished explicitly.

### `OBJ-SEC-01`
Encrypt sensitive values in the trusted application **before PostgreSQL receives plaintext**, with proof at SQL/driver boundaries and independent connections.

PARTIAL. Historical finite SQL/driver/frame evidence; no new writer-boundary proof. Complete missing plaintext-route inventory and independent observation.

### `OBJ-SEC-02`
Preserve confidentiality and authenticated integrity under declared tenant/field/row/key-generation context, detect swapped or malformed frames and unauthorized release.

PARTIAL. Historical CF1 context/authentication tests; this run's finite search tests do not requalify crypto. Independent composition/key-lifetime evidence remains.

### `OBJ-SEC-03`
Enforce application authorization, result lineage and tenant boundaries; handle SQL injection through parameterization, guarded operations and least privilege without falsely claiming that encryption prevents arbitrary application authorization flaws.

PARTIAL. Finite tenant/lineage controls retained; no application-wide authorization claim. Deployment-owned policy and independent adapter review remain.

### `OBJ-SEC-04`
Detect plaintext bypasses via ORM, bulk DML, direct SQL, COPY, external writers, migrations, sessions, background jobs, triggers, caches, logs, exports, backups and privilege paths.

PARTIAL. Guarded/refused routes and partial scanner exist. Unknown writers, exports/logs/caches and operational privilege paths still require real inventory.

### `OBJ-SEC-05`
Keep payload/search keys isolated, never silently choose fallback keys, bound nonces/usage/leases, test memory/fork/cancellation/rotation and use robust existing cryptography.

PARTIAL. Existing isolated key/context mechanisms; no completed full rotation/custody proof. Memory/fork/cancellation/usage and external custody remain.

### `OBJ-SEC-06`
Reduce equality, frequency and access-pattern leakage with a threat-modelled, independently benchmarked search-profile design; document residual leakage, low-entropy domains, adaptive leakage and query-pattern trade-offs.

RESEARCH OPEN. Earlier lower-leakage cost gates failed; no stronger privacy profile integrated. Define leakage and viable workload contract before implementation.

### `OBJ-SEC-07`
Independent red-team/security, cryptography, SQL adapter, provider and supply-chain qualification; the seven gates pass only with real evidence.

EXTERNAL OPEN. Internal agent reviews and same-host tests cannot close independent security/provider/supply-chain gates.

### `OBJ-QUERY-01`
Exact protected equality, `IN`, scoped uniqueness, SQL NULL/three-valued logic, empty lists, bound types, collision resistance/verification and concurrency races.

PARTIAL. Historical finite equality/IN corpus plus new25-method search checks; no new SQL grammar. Concurrency/native breadth and current corpus reconciliation remain.

### `OBJ-QUERY-02`
Ordinary SQL correctness: `IS NULL`, `IS NOT NULL`, `!=`, `NOT IN`, `IS DISTINCT FROM`, `IS NOT DISTINCT FROM`, nested Boolean expressions, aliases, outer joins, scalar/entity projections, relationships, subqueries.

PARTIAL. Both NULL-safe methods remain runtime-refused. This run fixes their missing advisory diagnostics; it does not implement these operators.

### `OBJ-QUERY-03`
Advanced SQL: ordering, keyset/offset pagination, ranges/comparisons, `LIKE`/`ILIKE`, prefix, suffix, substring, fuzzy, regex, full-text, `DISTINCT`, aggregates, `GROUP BY`, joins, JSON/array/numeric/datetime and other protected types. Each gets native semantics, a viable scheme/profile or an explicit, researched `REJECTED-LOUD` alternative—never silent omission.

PRODUCT OPEN. Advanced grammar/types need explicit researched semantics/leakage contracts and native oracles; current loud refusals retained.

### `OBJ-QUERY-04`
ORM/Core and data-modification coverage: INSERT/UPSERT/UPDATE/DELETE, bulk DML, `RETURNING`, triggers, cascades, FKs, savepoints, retries, autocommit/isolation, idempotency and connection/transaction state.

PARTIAL. Historical bounded ORM/DML evidence; general UPSERT/bulk/triggers remain open. Native cleanup verification depends on exact fixture authority.

### `OBJ-QUERY-05`
Full, versioned compatibility corpus and pre-adoption read-only scanner, with exact native-versus-protected classification and reproducible cases.

VERIFIED FINITE SLICE. Scanner6-method RED/GREEN and actual report4-method RED/GREEN; actual combined report4 PASS. Corpus/public wrapper/dynamic coverage remain incomplete.

### `OBJ-LIFE-01`
Declarative, deterministic, safe plan → apply → verify; schema/writer/permission inventory; irreversible-step preview and actionable diagnostics.

PARTIAL. Three remedies plus legacy guidance verified, including actual combined genuine-module5 PASS. No new apply/verify/recovery capability is implemented.

### `OBJ-LIFE-02`
Resumable, byte-bounded backfill, full final integrity/metadata verification, journaling, restart and crash-safe atomic chunks, failure fencing.

PARTIAL. Existing maintenance chunks/journaling remain bounded; pure38/ambiguous22 models are not native adapters. Closed journal grammar and crash/commit proof remain.

### `OBJ-LIFE-03`
**Near-zero-writer-downtime migration**: concurrent writes, captured changes, ordered catch-up, deletion/PK-change handling, stale-worker fencing, verification, short publish/cutover, recoverability and measured pause SLO. Preserve native semantics and current secure maintenance fallback until this is proven.

PRODUCT OPEN. No sustained-write native capture/catch-up/cutover proof or pause SLO. Resolve precise lifecycle/effect/authority contract before enabling anything.

### `OBJ-LIFE-04`
Parallel/adaptive migration and verification without double processing, lost updates, unsafe memory, or unbounded locks/WAL.

PRODUCT OPEN. No adaptive parallel migration/convergence qualification. Native scheduling, bounded locks/WAL and backpressure proof remain.

### `OBJ-LIFE-05`
Exact decrypt-back of **current edited data**, constraints, types, defaults, order, indexes, FKs, views, ACLs, owners and permissions; complete metadata removal; fresh application operation with Cryptalis uninstalled.

PARTIAL. Historical retained-layout current-value recovery; v0 missing comments/designation cannot be invented. Independent authenticated recovery and fresh restore remain.

### `OBJ-LIFE-06`
Safe rollback, restore, redeployment, stale snapshot/pin refusal, retained encrypted-backup readers, RPO/RTO and deployment-disaster drills; no false secure-erasure claim.

PARTIAL. Safe refusals and historical backup/recovery evidence; durable ABORTED replan and ambiguous COMMIT resolution are not implemented. Fresh disaster drill requires authority.

### `OBJ-LIFE-07`
Three separate key operations: root/wrapping rewrap, payload-key rotation/re-encryption and search-root reindex/rotation, with separate correctness and recovery proofs.

PRODUCT OPEN. Rewrap preparation is not three completed key operations. Specify one protocol's publication/pin/failure recovery before native implementation.

### `OBJ-LIFE-08`
Real production KMS, initially AWS KMS where authorized, robust credential/region/outage/throttling/revocation/cost testing, with a provider-independent contract and no hard dependency on AWS for local functionality.

APPROVAL/EXTERNAL OPEN. Local provider tests do not qualify real KMS. Authorized account/credentials and custody/outage/revocation/cost evidence required.

### `OBJ-LIFE-09`
Safe install, upgrades, compatibility across versions, decommission and explicit clean uninstall, including unsupported legacy-layout repair or a tracked safe alternative.

PARTIAL. Historical installed matrices and new diagnostic-only same-host packaging. Combined222 install/upgrade/uninstall and legacy repair remain separate.

### `OBJ-DX-01`
Almost zero business/model/query changes; one manifest, named profiles, one attach call, usable status/plan/apply/verify/deprotect/rotate operations and precise startup feedback.

PARTIAL. Manifest/attach route exists; complete operational CLI remains incomplete. Prioritize usable operation semantics rather than more wording-only changes.

### `OBJ-DX-02`
`cryptalis doctor`: meaningful read-only static **and** dynamic diagnostics, policy/manifest/schema/ciphertext/role/provider/compatibility checks, with clear limits and no silent repair of privileges.

VERIFIED FINITE SLICE. Missing NULL-safe diagnostic fixed through real report function; full static/dynamic/provider checks and public wrapper integration remain open.

### `OBJ-DX-03`
Fully working independent FastAPI/SQLModel integration; a second unrelated application; measure source edit lines, dependency and deployment requirements. Extend thoughtfully to Flask and Django via actually suitable adapters.

PRODUCT/ADOPTION OPEN. One pinned app and historical SQLModel evidence; second unrelated app and suitable Flask/Django integration remain unqualified.

### `OBJ-DX-04`
Normal SQLAlchemy semantics: ORM identity map, lazy/eager loading, `Session.exec`, sync/async, pooling, migrations, background jobs, serializers, errors and result metadata.

PARTIAL. Historical original artifact matrix remains historical. No universal ORM semantics claim or automatic transfer to combined222.

### `OBJ-DX-05`
Accessible, complete docs: one small quickstart, profiles, threat model, leakage, boundaries, operations, recovery, practical examples, diagnostic errors and learning walkthroughs explaining what/why/how for each slice.

PARTIAL. Exact NULL-safe refusal guidance and legacy evidence warning improved. Complete current quickstart/recovery walkthrough still needs real admitted end-to-end smoke.

### `OBJ-PERF-01`
Continuous native ORM vs driver-only vs protected measurements of p50/p95/p99, write rate, steady-state throughput, CPU, RSS/allocations, WAL, storage/index sizes, query plans, provider RPC and recovery costs.

MEASURED LIMITED. Two new experiments retain128 samples/524288 calls each; HOLD24 and HOLD28. Missing tails/concurrency/write/WAL/provider measurements remain.

### `OBJ-PERF-02`
Profile-guided optimizations in Python, SQLAlchemy, PostgreSQL and crypto: batching, psycopg pipeline/executemany, pooling, safe cache use, allocations, projections, indexing, native accelerators and bounded key caching.

HELD. Both cache predicates pass25 finite methods but fail unchanged timing criteria; baseline retained. No retuning/rerun/optimization promotion from these data.

### `OBJ-PERF-03`
Multithreading, multiprocessing, async and adaptive worker processing with 1/4/16/saturation tests, isolation, retries, process/fork safety, backpressure, cancellation and measured speedup **or regression**.

OPEN. No new1/4/16/saturation proof. Separate workload and resource/cancellation contracts before concurrency tests.

### `OBJ-PERF-04`
Performance targets on agreed comparable conditions: repository's current added read p95 ≤3 ms for point/equality, ≤8 ms for `IN`-20 and ≤2× protected-column-plus-equality-index storage. Define write-throughput and pause SLOs through a documented stakeholder decision; do not invent an approved target or relax an existing target because a test fails. Evaluate million-row scale and a documented growth path to billion-row workloads without claiming the latter has already been tested.

OPEN. Existing read/storage targets unchanged; no invented write/pause budget or billion-row claim. Stakeholder SLO decisions and matched scale evidence required.

### `OBJ-OPS-01`
Reproducible installed wheels/source releases, verified license, SBOM, dependencies/provenance, locked builds, supported-version matrix, rollback documentation and independent reviewers.

PARTIAL. Diagnostic-only221 same-host2-sdist/3-wheel reproducibility accepted; remote wheel restored. Combined222 packaging and clean-host provenance/SBOM/review remain.

### `OBJ-OPS-02`
Recoverable research environment, immutable evidence hashes, source-to-test traceability, live Markdown checklist and durable local/authorized remote snapshots.

VERIFIED LIMITED. Exact recovery/source maps, materialized222 and bounded remote persistence improved. Denied compressed archives remain approval-blocked; no complete portable-host claim.

### `OBJ-RESEARCH-01`
Comparative, source-backed reverse engineering and potential novel mechanism research; demonstrate independent novelty/prior art and repeatable advantages rather than claiming novelty from an interesting idea.

ONGOING. Failed search alternatives and accepted pure lifecycle models preserved. No novelty or native integration claim; use existing results rather than repeat models.

### `OBJ-RESEARCH-02`
One finished, coherently integrated **working software candidate** that passes its admitted native-compatibility contract, end-to-end reversible lifecycle, real-app adoption proof and all relevant acceptance gates before a qualified release.

OPEN. Actual combined222 report4 and genuine diagnostic5 pass, but no full-product/gate closure. Frozen preview is distinct and not automatically promoted.

## Seven independent gates

| Gate | Status | Missing deciding evidence |
|---|---|---|
| G-ADAPTER | UNKNOWN | Complete admitted/unsupported-route matrix, independent adapter review and clean second app |
| G-CRYPTO | UNKNOWN | Independent composition, nonce, context and key-lifetime review beyond local vectors |
| G-QUERY | UNKNOWN | Complete claimed-profile semantic/leakage admission and calibrated workloads/scanner coverage |
| G-LIFECYCLE | UNKNOWN | Legacy/fresh-cluster recovery, native online/rotation protocols and agreed pause budgets |
| G-PROVIDER | UNKNOWN | Authorized real KMS custody, transport, revocation/outage/throttling/cost evidence |
| G-POLICY | UNKNOWN | Deployment-owned writer inventory/authentication, pin authority, stale-worker and recovery decisions |
| G-RELEASE | UNKNOWN | Full release criteria, SBOM/license/provenance, independent clean build/install/upgrade and review |

## This run: exact evidence versus remaining requirements

- Combined222 V2 manifest486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d:218 unchanged+3 replaced+1new versus three-remedy221. Actual materialization222 files/4,469,599B accepted with exact namespace and donor separation. This is not a full-suite or installed artifact result.
- Actual combined report4 PASS/527 closure: INTEGRATED222_REPORT_TERMINAL_REVIEW.md SHA f306990d6c780774fc7cbd25df5b5c4c6ac651922f17ec5248f9094f475a596e. Both operators remain runtime-refused. Synthetic report-valid bytes exercise real Registry/Table/input validation; ProtectionPlan wrapper/compiler/schema admission remain outside scope.
- Actual combined genuine-module5 PASS/558 closure: ../transition-diagnostic-module-review-20261017/COMBINED222-LEGACY-MODULE-TERMINAL.md SHA92f248202f0ef4018ccd96a71912b02000c3cc18da2baf6808d1b4c56fdf59e3. Exactly17 product origins loaded,43 runtime files watched. Two legacy message cases plus three earlier-remedy controls; no native recovery/DB behavior is established.
- Diagnostic-only221 packaging accepted per latest authoritative ledger: two identical150917B sdists/f8520edb34bb20af9a348a2e68f4073346548057d8d7e52b1489d2d0608632d8; three identical141416B wheels/55fde72147caddf2be41fa397fc855682a347f2fcbb26c527262810117b90b03. This excludes combined222 changes. Published wheel restoration is not independent-host installation. StageB installed constructor qualification was unselected in the consulted ledger; do not pre-credit it.
- Both new performance screens remain HOLD. Second run's28 flags include23 scheduling,3 canonical consistency and2 fallback median regressions; uppercase storage16 wall1.03314242/CPU1.04079398 exceeds fixed1.03. Keep baseline. Neither correctness nor favorable canonical medians override failure.
- Historical original Integrated221 full suites (SA21 2684,SA20 2638 with46 native-version skips,optional38) remain tied to their original artifact. Frozen doctor preview has its own seven-case evidence. Neither result transfers to combined222 by source similarity.

## Highest-impact next steps, separated by authority

1. Finish already selected artifact verification and reconcile its terminal result before scheduling more work. Then root may separately select a reviewed combined222 packaging/installed-source binding if a deliverable requires it. Reuse accepted artifacts/evidence; do not rerun earlier baseline/scanner/model/timing cells merely to accumulate counts.
2. Prioritize a substantive lifecycle seam: source-only closed, phase-sensitive journal-state contract derived from actual _expand/_backfill_chunk/_verify/_switch producers, with exact cursor/scope/count bounds and format compatibility. First decide the historical journal integer contract rather than reusing artifact decoder limits. This can be prepared without DB authority; integration that changes accepted states needs explicit review/selection. Preserve _state's retained-journal refusal until predecessor authentication, row-preserving insertion and physical-journal/ACL proof exist. See ../online-integration-gap-20261017/REPORT.md; pure38 and ambiguous22 already answer their bounded model questions and need no repeat.
3. Specify one full rotation workflow end-to-end (start with existing rewrap preparation): externally current pin, publication disagreement, interrupted successor and rollback/readability invariants. Produce concrete source contract and literal failure oracle before expanding payload/search rotations. No real KMS access is inferred; native/provider execution requires its own admitted boundary.
4. Close a real adoption gap: define a clean second unrelated app baseline and an explicit supported-route inventory, or bind the public report wrapper with its actual compiler dependencies. Choose based on expected user value and current approved dependencies; do not stub a compiler or fabricate an authenticated plan. The already-passing direct report path need not be repeated for cosmetic changes.
5. Performance work should begin with a different measured cost center or a missing required workload contract, not another rearrangement of the held predicate. Preserve all noise and fixed gates. Before native timing, obtain the outstanding timing-policy/SLO decision and bounded workload authorization; do not claim local tiny-loop durations meet end-to-end targets.

## Approval-blocked and external work

- Native cleanup48-case/physical transaction-pool boundary and public quickstart/backup/restore/removal smoke need the exact fixture ACL authority; prior cutover helper authority is not a substitute.
- Independent fresh-cluster restore/disaster drills, real KMS/cloud access and required credentials/resources remain separately approved operations. No account/access/cluster configuration changes are implied by continuation.
- Opaque source archive publication and sdist publication have distinct pending exact approvals. Latest ledger names source requestSentinel_0c76d187bf0c81d1a95b1880f277281b and sdist requestSentinel_840ac69a2ce481d19913739a12be1504; older pending identifiers are historical, not permission. No alternate route/encoding or retry bypass. Existing focused archive+overlays and verified wheel remain the honest restore boundary.
- External reviewers, provider custody and clean-host supply-chain evidence cannot be supplied by more internal agent checks. Prepare exact source/evidence packets within current authority; contact, access or provisioning requires the relevant approval.

No broad roadmap or another remedy-only cycle is proposed as a substitute for these missing contracts. Independent engineering review may validate finite slices; it does not self-certify the seven gates.


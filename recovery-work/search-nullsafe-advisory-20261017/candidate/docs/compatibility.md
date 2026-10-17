# Query compatibility

**SPECIFIED:** selected scope and query contract. **No production cell is qualified.**
SUPPORTED selects design scope. IMPLEMENTED means code exists, with its boundary stated.
VERIFIED means named evidence exercises the stated property on its recorded revision and cell. It does not imply release qualification.
[Status](status.md) owns current evidence. [Security](security.md) owns collision, omission, replay, NULL-presence, and host-compromise limits.

## Support vocabulary

Every capability is exactly one of **SUPPORTED**, **UNSUPPORTED BY DESIGN**, or **INTERNAL ONLY**.
An unsupported capability remains rejected until admission changes its classification.
A research mechanism or receipt is INTERNAL ONLY and cannot establish public support.
All normative sections here are SPECIFIED. Recorded-cost sections are VERIFIED only at their stated historical measurement scope.

## Supported stack

Python 3.12+, SQLAlchemy 2.x, psycopg 3 sync and async, PostgreSQL 16.
The isolated cells are SQLAlchemy 2.0.51 and 2.1.3. Native `merge_all`/`delete_all` exist only in 2.1; no substitute API is added to 2.0.
Owning attached Sessions may use native SAVEPOINT, RELEASE and ROLLBACK TO through `begin_nested`.
Caller SQL/forged controls remain rejected. Failed control execution invalidates the connection: discard the whole unit, then explicitly rollback/close before reuse.
Normal nested results/state remain native. Continuing the outer unit after failed control is deliberately refused; no partial success is inferred.
Every protected value is text. Other protected types and PostgreSQL majors are UNSUPPORTED BY DESIGN until admission.
The compiler inspects exact text equivalence, nullability, stable application-generated IDs, tenant declarations, and constraint scopes.
Every protected table declares its tenant column or declares itself single-tenant.
Serial, identity, and database-default-generated primary keys fail at plan time with a plain explanation.
App-assigned UUID, Snowflake-style, and other ID mappings need frozen typed context encodings and differential evidence.
No sequence-USAGE or preallocation exception admits a server-generated key.

## Compatibility promise

Cryptalis never silently changes what the backend returns.
For every supported operation, results match the unprotected database, including native values, types, NULLs, and ORM behavior.
Every unsupported operation raises `UnsupportedEncryptedQuery` or an equivalent typed error before execution.
Different, partial, unauthenticated, or plaintext-fallback data is forbidden.
Full-term query exactness assumes HMAC collision resistance and intact search representations.
Payload authentication does not prove hostile-database completeness, freshness, or adversarial global uniqueness.

Unsupported operations on protected fields fail. Users must inspect this list before protecting a field:
ordered comparisons/ranges, ORDER BY, LIKE/prefix/contains, regex, SUM/AVG/MIN/MAX, general DISTINCT, protected-field joins, and non-text types.
The recommended adoption path is manifest → plan → staging apply plus the attached application suite → qualified production apply → decrypt-back exit.
Plan refuses server-generated keys, unsupported types, small-domain searchable fields, missing tenancy, and unsupported writers.
Attach rejects unsupported queries. Application tests on staging expose query-level incompatibilities before production.
This path does not guarantee zero changes and adds no command or mode.
Adoption costs a manifest, one attach call, typed replacements for opaque protected writers, and application-generated primary keys.
Rollback/removal transforms current data through decrypt-back until explicit finalization retires its recovery dependencies.

## Full capability matrix

| Protected-field operation | Classification | Contract or reason for rejection |
|---|---|---|
| Text storage/read/write, entity/scalar projection, SQL NULL | SUPPORTED | Randomized authenticated payload. Preserve exact str, empty text, NULL, native ORM state, and expected row/tenant context |
| Equality `==`, inequality `!=` / `<>`, `IN` and `NOT IN` | SUPPORTED | Declared full tenant/domain-bound HMAC term. Preserve typed binds and native NULL/empty-list truth tables |
| Tenant-scoped uniqueness | SUPPORTED | Full term plus tenant scope in a race-safe native unique index. Explicit single-tenant declaration supplies its one scope |
| Comparisons `<`, `<=`, `>`, `>=`, BETWEEN/ranges | UNSUPPORTED BY DESIGN | No admitted range representation |
| ORDER BY and sorted pagination on protected values | UNSUPPORTED BY DESIGN | No admitted order representation. Ciphertext ordering is forbidden |
| LIKE, ILIKE, prefix/startswith, contains, suffix | UNSUPPORTED BY DESIGN | No admitted pattern/text grammar or representation |
| Regex, fuzzy/similarity, full text | UNSUPPORTED BY DESIGN | No admitted exact query or text-search contract |
| SUM, AVG, MIN, MAX, arithmetic | UNSUPPORTED BY DESIGN | Selected payload/equality format does not implement these operations |
| General DISTINCT, DISTINCT ON, GROUP BY, COUNT DISTINCT | UNSUPPORTED BY DESIGN | Randomized-payload comparison changes logical semantics. A spike's scoped aggregate rewrite does not admit this family |
| Joins/FKs on protected fields | UNSUPPORTED BY DESIGN | No admitted shared search-domain or protected-FK contract |
| `IS NULL` / `IS NOT NULL` | SUPPORTED | Native presence semantics, including storage-only fields and null-extended rows; no equality term required |
| `IS DISTINCT FROM` / `IS NOT DISTINCT FROM` on protected fields | UNSUPPORTED BY DESIGN | Current attached grammar rejects these NULL-safe operators before SQL. Ordinary equality/inequality is not a general replacement; isolated research does not admit them |
| Field-to-field equality, general NOT of compound protected expressions, other unadmitted functions/operators | UNSUPPORTED BY DESIGN | No independent admission/proof for these shapes; tenant guards must not be inverted |
| Non-text protected values, JSON predicates, custom protected types | UNSUPPORTED BY DESIGN | Text is the only admitted protected type |
| Opaque raw SQL/COPY protected writes and unknown external writers | UNSUPPORTED BY DESIGN | Reject guarded routes. Plan blocks protection unless the deployment excludes separate routes |
| Research range/prefix arrays, order candidates, scoped aggregate helpers, internal binary projections | INTERNAL ONLY | Experiments and adapter machinery, not public query capabilities |

Plaintext fields retain native query semantics, including ranges, order, aggregates, and joins through unprotected keys.
Tenant-scoped uniqueness uses PostgreSQL's original qualified NULL behavior. Unqualified partial/compound or NULLS NOT DISTINCT variants must reject at plan time.

## Query semantics

Compare every admitted shape with the same native PostgreSQL application.
Test typed/reversed/late binds, AND/OR compositions of admitted predicates, aliases, projections, pagination, and outer joins through unprotected keys.
Preserve SQL UNKNOWN. Preserve NULL elements and empty `IN` lists. Reject an unadmitted nested operator before SQL.
NULL payloads remain SQL NULL. Empty strings encrypt normally. Reject PostgreSQL-forbidden NUL text before SQL.
Strict UTF-8 never changes composed/decomposed text or silently casefolds it.

Text equality requires inspected deterministic exact equivalence, such as a qualified `C` collation.
Nondeterministic collations, citext, bpchar padding, locale-sensitive operators, custom types, and changed normalizers are UNSUPPORTED BY DESIGN until admission.
The compiler rejects a constraint or mapping it cannot preserve exactly. Generic CHECK/FK/default/collation preservation is UNKNOWN.
[Lifecycle](lifecycle.md#integrated-lifecycle-checkpoint-2026-10-07) bounds the current verifier's source-index and scoped-uniqueness evidence.
A searchable small domain fails planning because enumeration can label equality classes. No arbitrary size threshold substitutes for leakage evidence.

## Portable DDL

Required extensions: none. The selected equality representation uses built-in `bytea`, B-tree `bytea_ops`, and immutable expression indexes.
The compiler emits the tenant scope, qualified NULL contract, and declared constraint structure.

```sql
-- SPECIFIED packed CF1 equality, with an explicit tenant scope.
CREATE UNIQUE INDEX protected_email_unique
  ON protected_customer USING btree
  (tenant_id, (substring(email_payload FROM 15 FOR 32)) bytea_ops);
```

The final index needs framing checks for suite, flags, admitted generations, minimum lengths, and term presence.
A declared single-tenant table needs no synthetic public tenant column.
Generated/separate equality terms are compiler choices for admitted constraints. They do not admit protected joins or FKs.
Shape checks reject malformed bytes, but cannot certify encryption without keys.
[Database prerequisites](../README.md#database-prerequisites) state migration/runtime role boundaries.
Exact generated CHECK/default/collation DDL preservation and deployment writer exclusion remain UNKNOWN.
The [slice 3 runtime checkpoint](status.md#restricted-runtime-role-completion-2026-10-08) verifies local non-owning CRUD and tested persistent DDL/ownership denials.

## Capability admission

Only after all seven build slices pass their real PostgreSQL tests can range, order, prefix, or text-search work start.
Every added type, operator, mapping, or platform must then pass all six technical gates:
G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, and G-POLICY.
[Status](status.md#missing-evidence-and-promotion-criteria) owns each gate's unchanged evidence requirements.
Admission also requires explicit per-capability leakage opt-in, exact grammar, bounded representations, published attack evidence, and approved measured costs.
G-RELEASE remains an additional release requirement. No local experiment or acknowledgment bypasses these gates.
The six-gate grouping and conservative unadmitted grammar assumptions are recorded in [reset notes](_reset/notes.md).

## Performance targets and recorded costs

**SPECIFIED targets; local observations do not qualify a deployment:**

| Workload | Approved target |
|---|---|
| Point and equality reads | Added p95 ≤ 3 ms against the matched unprotected backend |
| IN with 20 values | Added p95 ≤ 8 ms |
| Protected column with equality index | Storage ≤ 2× the matched plaintext column plus its equality index |
| Write throughput | Undecided (D). No approved number |
| Maintenance pause | Undecided (D). No approved number |

**VERIFIED, recorded earlier revision only:** [million-row CF1 receipt](../spikes/revamp/results/gate-performance.json), warm PostgreSQL 16.15 and memory-only local keys.
These observations predate the latest DISTINCT change and do not measure the current adapter.

| Workload | Native p95 ms | Protected p95 ms | Added p95 ms | Target result |
|---|---:|---:|---:|---|
| Point entity, 100 samples | 0.897 | 4.150 | 3.253 | Misses 3 ms |
| Equality entity, 100 samples | 0.928 | 6.517 | 5.589 | Misses 3 ms |
| IN-20 entities, 100 samples | 1.093 | 16.148 | 15.055 | Misses 8 ms |
| Plaintext-filter range/prefix/page, 20 samples | 23.852 | 127.098 | 103.246 | About 5.3× native. Full entity includes protected email |

The page-query anomaly has an unknown cause. Slice 4 source inspection corrects the former plaintext-only label:
[`browse_customers`](../spikes/revamp/plain_app.py) calls `active_customers`, which selects the complete Customer including email.
The historical receipt is retired as current-product cost evidence. The measurements and unexplained historical cause remain preserved.
Separate expression admission, statement compilation/cache behavior, driver/database time, row decoding, and materialization in the matched workload.
No encrypted range/prefix/order capability follows from these plaintext queries.

### Slice 3 local profile: 2026-10-08

**VERIFIED, bounded package adapter:** `.venv/bin/python tests/profile_sqlalchemy_adapter.py`.
The [hashed receipt](_reset/slice3-performance.json) records 5,000 synthetic rows, 100-row pages, and 40 paired samples.
The local cell uses Python 3.12.3, SQLAlchemy 2.1.3, psycopg 3.3.6, cryptography 50.0.2, PostgreSQL 16.15, and warm local keys.
Both paths use identical data and application-generated UUIDs. Queries consume and compare native values and types.
Protected fixtures are seeded through ordinary attached ORM writes. Empty fixture conversion to `bytea` is test setup, not product apply.
The final main-thread run followed the full suite and cache proof, with no concurrent Cryptalis checks.
Shared-host activity remains uncontrolled. The receipt retains earlier runs and their limits.

| Current bounded workload | Native p50/p95 ms | Attached p50/p95 ms | Added p95 ms |
|---|---:|---:|---:|
| Point entity | 0.435 / 0.618 | 1.715 / 2.903 | 2.285 |
| Unprotected range/prefix/page projection | 1.428 / 1.906 | 2.238 / 2.810 | 0.904 |

The point result is within the 3 ms added-p95 target in this local run. It does not qualify the deployment target.
Earlier runs vary with shared-host activity and code changes. The receipt retains those observations without deployment qualification.
Both plaintext page paths recorded 60 compilation-cache hits and one miss.
Protected entity statements disable compilation caching to prevent retention of another operation's tenant, point, or prepared keys.
Native unprotected compilation caching remains enabled.

Ten extra cProfile page queries separate exclusive Python time into categories.
Attached admission/guard cost 0.285 ms/query, compilation/cache 0.017 ms, driver/database 1.956 ms,
and decoding/materialization 0.065 ms. Native compilation/cache cost 0.015 ms, driver/database 1.590 ms,
and decoding/materialization 0.048 ms. Dispatch, key preparation, and other ORM/engine work remain separate in the receipt.
Profiling changes timings. Cumulative calls overlap; exclusive categories do not.
Driver time combines network wait and PostgreSQL work; those parts are not independently separated.
This small plaintext profile does not explain the historical million-row anomaly. Its cause remains **UNKNOWN**.
No equality/IN, isolated storage/index, sustained-write, remote-provider, or async performance qualification was performed.
Adoption in this fixture used one manifest, one attach call, authenticated tenant scope, and application-assigned IDs.
No business-query or model declarations changed between native and attached paths.
The later runtime checkpoint verifies separate credentials and fixture grants; deployment enforcement remains unverified.

### Slice 4 local million-row profile: 2026-10-08

**VERIFIED, local warm synchronous cell only:** the [receipt](_reset/slice4-performance.json) binds the final source hashes to 1,000,000 rows per path.
Both native and attached applications use the restricted runtime login, application UUIDs, identical 53-byte synthetic text and fully consumed results.
Owner credentials perform only fixture setup, ANALYZE, storage inspection and independent plan inspection. No extension is required.
Each workload has 10 warmups and 100 alternating paired samples. Entity samples expunge the identity map and materialize fresh objects.
Added p95 means attached p95 minus native p95; the receipt also records paired median differences and p99 estimates.

| Current workload | Native p50/p95 ms | Attached p50/p95 ms | Added p95 ms |
|---|---:|---:|---:|
| Point entity | 0.476 / 0.790 | 2.245 / 3.126 | 2.336 |
| Equality entity | 0.383 / 0.821 | 2.255 / 3.382 | 2.561 |
| IN-20 entities | 1.116 / 1.543 | 3.300 / 4.548 | 3.005 |
| Plain projection, range/prefix, broad OFFSET, 100 rows | 49.050 / 111.791 | 64.975 / 134.355 | 22.564 |
| Protected entities, plaintext range/prefix, five rows | 0.540 / 0.776 | 2.927 / 3.976 | 3.199 |

Point/equality and IN-20 meet their selected added-p95 targets in this run. No target was invented for either page workload.
The isolated protected column plus equality index is **1.4928×** the matched plaintext column plus equality index, below the 2× target.
The plaintext index is on name; the protected index is on tenant plus full term, as selected by the compiler. Whole-relation ratios are not the target denominator.
PostgreSQL plans used the generated expression index for equality and IN-20. There is no hidden filtering or result refill.
Both plain-projection paths recorded 109 cache hits and one miss; protected projections/predicates disable caching.
The receipt separates admission, compilation, key/term preparation, driver/database wait, decoding and other ORM work for all five workloads.
Server plans also record buffer reads and execution time; larger protected heaps affect ordinary plaintext page scans.
These observations do not establish the cause of the old 127/24 ms receipt. Its full-entity query and former plaintext-only label are retired as current-product evidence.
The current structural control differs in IDs, tenancy, distribution, selectivity and schema; historical causality remains UNKNOWN.

An earlier diagnostic equality run missed 3 ms at 3.565 ms added p95. Profiling removed repeated generated-node comparisons and unnecessary compilation.
The final source retained all admission checks and regression controls. Shared-host activity is uncontrolled; the earlier measurement remains in the receipt.
Seeding observed about 29,873 native and 10,648 attached rows/s. One 2,000-row chunk reached key expiry, rolled back and recovered with fresh keys.
An independent elapsed-expiry test checks no SQL/rows before recovery. Expiry limits were unchanged; a second profile retry failure would stop the run.
1,000 committed updates in ten batches observed about 7,493 native and 3,654 attached rows/s. This is an observation, not a write budget or load qualification.
Cold/remote providers, async costs, sustained-load/platform qualification and deployment admission remain unverified. All seven full gates remain UNKNOWN.

### Historical storage and transition costs

The customer relation/index total rose from 192,692,224 to 350,707,712 bytes, plus 11,100,160 bytes of operation/chunk tables.
That whole-relation total does not establish the per-column 2× target. Isolated protected-column/index evidence remains UNKNOWN.
Protection/verification took 128.821 s. Observed pause with VACUUM/ANALYZE was 130.380 s. Neither value is an approved pause budget.
Observed WAL/temp deltas and CPU/RSS are in the receipt. Unrelated activity can affect cluster/database deltas.

The [10,000-row cost receipt](../spikes/revamp/results/gate-write-cost.json) also measures an earlier adapter revision before the latest DISTINCT change.
It records paired results and 400 committed updates. It cannot establish current-revision performance or sustained write qualification.
The receipt's historical `current_adapter` labels remain unchanged provenance.
Database-only surrogate array measurements are INTERNAL ONLY, separate from actual CF1 and whole-backend costs.
Their bundle storage ratios do not establish the admitted equality column's target.

## Database evidence

**VERIFIED, bounded product cell:** PostgreSQL 16 storage/search/transition suites include protected DISTINCT refusal.
[Status](status.md) owns current revision-bound evidence. Earlier single-user/service research remains [archived provenance](research/revamp-evidence.md).
No production cell is qualified. No production provider, authenticated deployment procedure, or independent review is available.

| Cell | Classification and qualification |
|---|---|
| Selected Python/SQLAlchemy/psycopg/PostgreSQL 16 sync and async | SUPPORTED design scope. Exact runtime/driver/OS cell remains UNKNOWN |
| SQLite labs, single-user physical probes, old generated-ID adapter | INTERNAL ONLY evidence. Cannot qualify the selected contract |
| PostgreSQL majors other than 16 | UNSUPPORTED BY DESIGN until admission |
| PostgreSQL 16 managed services | SUPPORTED design scope. RDS/Aurora, Cloud SQL, Azure, Supabase, and Neon cells remain UNKNOWN |

The selected equality index requires no extension. No provider extension allowance supplies missing qualification.

## Ordinary negative predicates: bounded W4 amendment

The owner's W4 mandate admits IS NOT NULL, inequality and NOT IN using existing representations.
No new cryptographic primitive or search-privacy claim is introduced. NULL/three-valued semantics
and SQLAlchemy empty expanding-list semantics remain native. Empty NOT IN must keep proven-absent
outer-join rows while excluding present foreign-tenant rows. Ordinary negative comparisons require
the admitted equality representation; presence predicates also work for storage-only fields.
No plaintext fallback, client-side result filtering, or arbitrary Boolean NOT rewrite is admitted.
See tests/test_sqlalchemy_negative_predicates.py for fixed-seed native differential and tenant cases.
Full dependency-cell results are recorded separately; source inspection alone does not qualify support.

## Bounded A6 candidate profile

The uncommitted candidate admits exact standard Text/String/VARCHAR types matching native catalog type and character limit, plus the executed SQLModel 0.0.47 AutoString profile. It does not admit arbitrary custom TypeDecorator behavior. Qualified sync SQLModel factories retain native Session.exec and the tested lazy/selectin/joined relationships; async SQLModel refuses explicitly. See the A6 evidence boundary in [status](status.md).

VARCHAR writes follow native character-count assignment: excess ASCII spaces may be removed on storage; other overlength values refuse before data SQL. The assigned ORM value is not silently replaced; native refresh semantics expose the stored value. Query terms are never truncated or normalized. Overlength refusal is CharacterLimitExceeded, not a DBAPI DataError: applications catching only DBAPI errors need an explicit handler adjustment. Failed root/SAVEPOINT state and cleanup were compared independently. Do not claim identical exception classes.

Decrypt-back restores exact qualified text/VARCHAR type, typmod, collation and visible order for admitted ordinary suffix layouts. Default/generated values, non-text suffixes, dependent constraints/views and unsupported ACL metadata still refuse. Older Cryptalis implementations can refuse locks containing newly admitted source types; qualify upgrades and rollbacks rather than assuming old-reader admission. No original collation is silently changed to C, and no plaintext or native-session fallback is used.

## Read-only staged-adoption report (CP84 candidate)

Call `plan.compatibility_report(mapping, sources={"app/queries.py": source_bytes})` on a protection or migration plan. Supply the same SQLAlchemy registry used for planning and attachment. Each source label must be a relative Python module path. The caller chooses and reads the source files. The report does not discover files, import or execute source text, issue SQL, change grants, change plan bytes, or admit a runtime operation.

The returned JSON-compatible report contains declared model/field summaries, source byte hashes, line-numbered findings, reasons and practical alternatives. `authority` is `ADVISORY_NOT_AUTHENTICATED`. Coverage is `NOT_INSPECTED` without sources and `PARTIAL` with sources. `staging_required` is always true. An empty finding list does not prove compatibility. Findings remain SOURCE-INSPECTED even when the report implementation has passed executable tests.

The bounded scanner recognizes imported SQLAlchemy/SQLModel Core INSERT/UPDATE/DELETE and textual SQL constructors, declared storage-only comparisons, direct encrypted ranges/patterns/order methods, direct `is_distinct_from` / `is_not_distinct_from` calls on declared protected fields, and declared UUID point-read inputs. It reports unresolved shadowed/rebound imports, dynamic code, unavailable mapping identity, and parse failures. A conditional refusal applies only if the expression executes through the attached factory. For example, an Alembic `text()` call may use a separate maintenance connection; its presence alone is not a production defect. Variable types and runtime routing require staging evidence.

The scanner is not a complete Python type checker or control-flow analyzer. It does not resolve all aliases, query-builder wrappers, plugins, generated queries, relationships, nested statements, ordering/grouping arguments, or runtime parameter values. Source outside the supplied inventory is not inspected. Use the application's Python version to parse its syntax. Bytes honor Python encoding cookies; text inputs are hashed as UTF-8. No source literal values are included in diagnostic messages.

Limits are 256 source files, 1 MiB per file, 16 MiB total, 50,000 AST nodes per source, and 2,048 findings. Invalid input or exceeded analysis limits raise `cryptalis.manifest.compatibility.CompatibilityInspectionUnavailable` with a static code, `effects="NONE"`, and a staging remedy. This shape validation is not cryptographic validation of a lock. Split larger inventories into explicitly recorded batches and retain complete coverage accounting; do not discard an uninspected batch.

Adoption procedure:
1. Write the manifest and create the plan with the approved writer inventory.
2. Obtain the advisory report for declared mappings and supplied application sources. Review each conditional or unresolved finding.
3. Apply protection to a staging copy. Attach Cryptalis through the approved bootstrap. Run the unchanged application suite and fixed-seed native/protected differential corpus.
4. Resolve silent differences as release-blocking defects. For refused operations, use a documented supported operation or explicitly leave the field outside the protection policy. Never bypass an attached factory or use a plaintext fallback to suppress a refusal.
5. Deploy only after all required security, lifecycle and application gates pass. This report cannot substitute for those gates.

Current evidence and unresolved qualification are recorded in the research checkpoint. No automatic source discovery or new `plan`/`doctor` CLI command is claimed by this API addition.

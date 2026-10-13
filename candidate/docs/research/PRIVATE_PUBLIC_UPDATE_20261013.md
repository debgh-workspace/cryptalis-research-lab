# Private public-table UPDATE experiment, 2026-10-13

Status: IMPLEMENTED isolated candidate. The preceding 58-case source passed both pinned PostgreSQL dependency cells. The final custom-type refusal-order correction passed its ten impacted controls on both pinned PostgreSQL dependency cells. The full final 59-case file was not rerun as one cell. All seven production gates remain UNKNOWN.

## Contract

This opt-in experiment targets fully public, direct mapped tables in a schema already named by the protected deployment. It does not implement protected-field bulk UPDATE and does not close broad bulk-DML support. The public attachment API remains unchanged. Without the private table-object allowlist, bulk UPDATE refuses.

The caller supplies the exact mapped Table objects through `_experimental_public_update_tables` on the experimental attachment owner. This private research attribute is not a public configuration contract. One native UPDATE may assign explicit literal or typed-bind values to ordinary text, integer or Boolean columns. Public single-table comparisons, AND/OR, NULL predicates, IN/NOT IN, and direct public RETURNING stay native. No predicate, row scope, value, SQL NULL or result row is rewritten.

The first profile refuses protected tables, record primary-key assignments, mapped foreign-key assignments, inheritance/versioned mappings, executemany, extra parameter-derived assignments, custom codecs, callable binds, functions, subqueries, extra tables, custom prefixes/options, implicit onupdate behavior and generated columns. It also refuses database CHECK/FK/exclusion effects, user triggers, rules, RLS, inheritance/partitions, expression/partial indexes, and nonstandard types/index operator classes. This is intentionally narrower than general PostgreSQL UPDATE.

## Invocation and catalog boundary

Attachment freezes eligible public mapping schema/name/column identity without granting UPDATE authority. Pin capture skips schemas and exact types outside this profile, without reading custom-type optional accessors. Each invocation rejects a newly changed custom type before inspecting mapping identity. Preparation resolves the qualified relation OID, obtains SHARE ROW EXCLUSIVE NOWAIT on that table, then rechecks its OID and conservative inventory in READ COMMITTED. This strong table lock can reduce concurrency. It is retained by the ordinary transaction; callers must explicitly roll back a rejected or failed unit. The inventory reuses the existing private DELETE catalog bridge and adds UPDATE-specific effect exclusions. No grants, role changes, credentials, key cache or cryptographic changes are made.

A one-use permit binds attachment, Session, Connection and the exact original SQLAlchemy statement. Native annotation-only clones remain associated with the same underlying statement. The before-execute and driver hooks consume successive permit states. This path disables compiled-cache reuse because an older compiled object cannot convey the current invocation's authority. Explicit parameter names must already occur as binds in the statement. A parameter name matching a mapped column is accepted only if that column is already an explicit SET target. A parameters dictionary cannot silently add SET columns.

Native SQLAlchemy retains UPDATE execution, identity-map synchronization, RETURNING construction, autoflush and transaction behavior. The existing async mutation-result cleanup boundary is reused. The host still supplies authenticated tenant authority and ordinary business authorization. No tenant ownership is inferred for public tables, and no protected table is admitted through this profile.

## Acceptance and current evidence

- Coordinator-only PostgreSQL baseline `a1-public-update-red-20261013`: the native commit/auto case succeeds, then the attached path raises UnsupportedProtectedOperation before UPDATE. Result: 1 failed, 30 deselected, 0.62 s. Existing S14 runtime remained unchanged for this baseline.
- Python AST checks pass for the three executable files.
- First local pure smoke: five SQLAlchemy statement-admission controls pass with the existing SQLAlchemy 2.0.51 interpreter. They open no database and do not qualify execution.
- First coordinator GREEN (`a1-public-update-green-20261013`) records 28 FAIL / 3 PASS in 11.24 s. SQLAlchemy 2.1 removed the older ordered-values attribute; the parser now handles both installed shapes. One outgoing-FK fixture referenced the protected table after its plan and correctly failed source-schema admission; it now references a separate public table. No source-schema guard was weakened.
- Corrected pure smoke: seven fixed controls pass separately on SQLAlchemy 2.1.3 and 2.0.51, without a database.
- Corrected coordinator PostgreSQL cell (`a1-public-update-corrected-20261013`): 31 PASS in 10.21 s, unchanged runtime bytes, server stopped. This covers native rowcount/state, commit/rollback/SAVEPOINT, four synchronization modes, columns/entity RETURNING, repeated typed-bound statements, empty sets, default/shape refusal and catalog-effect refusal.
- Expanded SQLAlchemy 2.1.3 PostgreSQL cell (`a1-public-update-expanded-sa21-20261013`): 57 PASS in 16.58 s, server stopped. New cases cover AsyncSession.execute transactions/RETURNING, mapping identity/refusal, native unqualified resolution, catalog-effect drift after prior success, an independent lock-before-inventory observation, native Core/ORM autoflush, and pure one-use/stale-compiled invariants.
- Pure protocol omission controls pass their sensitivity check separately on both versions: removing initial-stage validation, consumption, or exact compiled-object identity makes the corresponding test fail. Each in-memory restoration passes all three controls. Disk source is unchanged. These are deterministic state-machine checks, not database or external security review.
- A later pure control confirmed that initial pin capture inspected optional attributes of an ineligible custom type. Final source filters those types before pin capture. The regression and all three protocol checks pass separately on both versions. Four final-source in-memory omission controls (the three protocol guards and eligible-type filter) each fail their corresponding check; restoring exact source definitions passes all four after each variant, with disk hashes unchanged.
- The preceding 58-case source passed PostgreSQL on SQLAlchemy 2.1.3 (58 PASS, 17.21 s) and 2.0.51 (58 PASS, 17.66 s), with source-stable runs and stopped servers.
- A final pure RED on both versions found an ordering issue when an already-pinned public mapping later changes to a custom type. The exact-type refusal now precedes identity inspection. The file has 59 cases after adding that second custom-type state. Five final-source in-memory omission controls each fail their corresponding regression; every restoration passes all five, and disk bytes remain unchanged.
- Final impacted PostgreSQL controls passed separately: 10 PASS / 49 deselected on SQLAlchemy 2.1.3 in 2.58 s and 2.0.51 in 3.08 s. Both coordinator receipts report unchanged source and successful server stop; their archived executable files byte-match the current candidate. Do not relabel the earlier 58-case runs as a full run of the final source. The cache-removal variant is derived exactly from the preceding 58-case snapshot, with only the new UPDATE cache-disable line omitted. Its coordinator run records 2 FAIL in 1.65 s: repeated typed-bound UPDATEs refuse at exact compiled identity/admission. This is expected sensitivity evidence, not a claim of a silently incorrect result. The complete final 59-case file, provider-failure UPDATE, installed candidate wheels and full integrated regression remain NOT RUN at this checkpoint.
- The seven unchanged legacy-layout failures remain unresolved. The completed S8 FastAPI acceptance is not rerun or relabelled by this experiment.

## Sources and qualification limits

The SQLAlchemy 2.0 ORM DML documentation describes custom-WHERE UPDATE, synchronization and RETURNING: https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html . Exact installed 2.0.51 source was inspected for annotation and dispatch mechanics. Current online documentation may describe a later patch version; only recorded installed-cell tests establish this candidate's behavior.

The PostgreSQL 16 locking documentation defines the table-lock modes and transaction lifetime: https://www.postgresql.org/docs/16/explicit-locking.html . These sources explain the mechanisms; they do not qualify this prototype's security or its actual execution.

## Residual boundaries

The bound is the explicit table/grammar/effect profile, not a maximum affected-row count, memory, elapsed-time or throughput guarantee. NOWAIT and the strong table lock can refuse work that an ordinary concurrent UPDATE would wait to perform. The inherited catalog bridge and operator/search-path assumptions are not an independent qualification of custom operator resolution when a custom schema explicitly precedes pg_catalog. Such broader application/database behavior remains unqualified. No new production or cryptographic claim follows from the private pilot.

## Default-path cost and integration classification

Source review finds no extra SQL, key preparation or SELECT-cache change when this profile is unused. Ordinary SELECT dispatch returns immediately from the UPDATE-type check; the admission hook checks an empty permit ContextVar. Attachment adds one structural pin pass proportional to eligible public mapped columns. It retains mapping references and public metadata, not row values, keys or tenant context. These are structural observations; no runtime latency or retained-memory bound was measured.

If these files enter the integrated candidate, retain INTERNAL ONLY, private opt-in and default bulk refusal. Integration is not promotion. The opt-in path incurs a strong NOWAIT lock, catalog work and uncached UPDATE compilation. Neither broad bulk UPDATE nor a performance/production claim is justified by the finite acceptance tests.

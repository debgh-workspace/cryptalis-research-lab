# Native48 fixture mutations: exact resource scope

2026-10-17 16:33 UTC. SOURCE ONLY. No DB command, credential read, test, permission change, policy determination or hold removal.

## Immediate scope discrepancy

Current tests/test_sqlalchemy_flush_preparation_failure.py declares24 cases/profile,48 across both profiles. Its internal native/protected loops instantiate42 fixtures/profile,84 across both:

| Selected function | Cases/profile | Fixtures/profile |
|---|---:|---:|
| rejected_text_flush (3 entrypoints ×2 modes ×2 nesting) |12|24 (native/protected)|
| rollback_quarantines_connection (2 modes ×2 nesting) |4|4|
| provider_failure (2 modes ×2 nesting) |4|8 (native/protected)|
| real_cancelled_provider (2 nesting) |2|4 (native/protected)|
| failed_invalidation (2 modes) |2|2|
| Total |24|42|

Thus the unanswered assistant request's “up to68” is not a faithful upper bound for the full current file on both profiles. This is static counting, not collection or an observed execution. The minimal two fault selectors remain6 cases/6 fixtures per profile,12 across both, and would answer a narrower question. No selector is chosen here.

## Statement-by-statement setup and cleanup

Source root: recovery-work/integrated222-v2-20261017/source. All selected calls use the default single-field, nonunique, tenant-column, ordinary SQLAlchemy mapping; relationship_model/sqlmodel_model/two_fields are false.

| Source operation | Resource/recipient | Persistence and qualification |
|---|---|---|
| search_application: schema = cryptalis_search_ + uuid4().hex | Proposed new schema name in existing connected database | Random naming is collision avoidance, not current ownership proof |
| CREATE SCHEMA quoted generated name, owner.begin | New schema | Commits before later steps; not one rollback-only fixture transaction |
| metadata.create_all(owner) | customer table in that schema: UUID id PK, tenant_id, name Text(C), label Text, rank integer; native name/rank/label indexes | Persistent fixture objects until cleanup; no sequences because UUID id autoincrement=False |
| compile_protection on empty native mapping | Actual catalog/role/environment reads | Fresh REPEATABLE READ READ ONLY transaction; SET LOCAL search_path=pg_catalog is transaction-local, not global configuration; does not install a migration journal |
| native_index.drop(owner), protected branch | name_native index within generated schema | Persistent fixture-only drop |
| ALTER TABLE generated.customer ALTER COLUMN name TYPE pg_catalog.bytea USING NULL::pg_catalog.bytea | Empty synthetic customer.name, protected branch | Destructive type conversion only on fixture's pre-write column; not real customer data |
| CREATE INDEX fixed field-derived name ON generated.customer (tenant_id, substring(name,15,32)) | Generated schema index, protected branch | Nonunique for these selected calls; fixed index name remains schema-scoped |
| ALTER TABLE generated.customer ADD CONSTRAINT fixed field-derived frame CHECK | Fixture table, protected branch | Persistent fixture check |
| SELECT1; SHOW server_version_num; SELECT current_user; pg_roles boolean query | Existing runtime connection identity | Reads only; exact assertions described below |
| REVOKE ALL ON SCHEMA generated FROM PUBLIC, runtime_current_user | ACL of generated schema; recipients PUBLIC and existing runtime role | Object ACL change, not role membership/attributes or database-wide PUBLIC removal; committed psycopg context |
| REVOKE ALL ON TABLE generated.customer FROM PUBLIC, runtime_current_user | ACL of generated table only | Removes table grants on that fixture, not global/default privileges |
| GRANT USAGE ON SCHEMA generated TO runtime_current_user | Same generated schema and existing role | Creates effective access to fixture until dropped/revoked; no grant option |
| GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE generated.customer TO runtime_current_user | Same generated table and existing role | Fixture CRUD privileges; no ownership transfer, membership or grant option |
| Optional child-table REVOKE/GRANT | Child table only if relationship_model | Unselected in this full flush file; exclude from actual proposed inventory |
| runtime Session/AsyncSession SQL | Fixture rows: synthetic valid/NUL/provider-failure values | INSERT, SELECT, transaction/SAVEPOINT/commit/rollback work; some nested outer-valid rows deliberately commit. Fault hooks may close/invalidate own captured connection |
| runtime.dispose; owner.begin DROP SCHEMA IF EXISTS generated CASCADE | Generated schema and PostgreSQL dependency closure | Commits removal; not merely rollback. Assumes no unrelated object/dependency has entered this schema/closure. CASCADE is not intrinsically restricted to the original fixture objects |
| owner.dispose, mapping.dispose | Owned local handles/mapping | In-process cleanup; may be skipped if an earlier finalizer raises |

All four explicit ACL statements execute for native AND protected fixtures. Full intended two-profile schedule therefore entails336 ACL statement executions across84 fixture lifecycles, assuming setup reaches that point without failure. No row-level grant is proposed. There is no journal grant in this selected fixture; that wording belongs to the separate public-smoke request.

## Existing resources, role authority and failure durability

The existing database and owner/runtime roles are used; no CREATE/ALTER/DROP ROLE, membership GRANT/REVOKE, ALTER DEFAULT PRIVILEGES, ALTER SYSTEM, database-wide grant, HBA/authentication change, extension creation or pg_terminate_backend is present in the selected fixture/test path. Own test connection close/invalidation and asyncio task cancellation are distinct from terminating arbitrary role sessions. Local compiler search_path/isolation/read-only transaction settings do not mutate global settings. This is scoped source inspection, not a claim that all transitive native initialization effects have been observed.

Fixture objects and ACLs are committed and can survive process termination, failed setup or failed finalization. Cleanup is not guaranteed by merely having a finally block: runtime.dispose or DROP can raise; no outer survivor audit exists in these source files. The try covers CREATE SCHEMA, but finalization does not track successful creation before DROP IF EXISTS. If creation fails because the randomly generated schema already exists, finally can attempt to drop that name. This is a source-visible failure-scope concern, not an observed collision. A current execution binding must establish exclusive ownership/names and exact cleanup authority rather than assuming UUID naming proves them. External dependencies and unexpected fixture survivors must be handled by a separately reviewed bounded cleanup disposition, never broad wildcard deletion.

The module also writes a version-specific compatibility corpus under an evidence directory during its autouse fixture teardown. It uses write_text and can overwrite that path; a fresh isolated output binding remains required. This is a filesystem effect, not a database privilege.

## Existing preflight assumptions, without inventing stronger checks

scripts/test_postgres.py clears inherited two test-URL variables, loads existing private owner/runtime files from Path.home, checks nonempty values and SELECT1 on both with connect_timeout5, then installs in-process _cryptalis_test_preflight and invokes pytest. tests/conftest.py requires that marker and redacts driver errors/credential-bearing failures. No credential body was opened in this audit. Neither the wrapper SELECT1 nor the marker alone proves port55432, database identity, owner/runtime separation, exclusive lab ownership, permissions or bounded cleanup. Those need the existing coordinator's genuine additional preflights/current admission; do not fabricate the marker or infer authority from an inherited environment.

search_application checks both URL variables exist. After creating/compiling/converting the fixture it reads the runtime identity and asserts PostgreSQL major16 and not rolsuper/rolcreatedb/rolcreaterole/rolbypassrls. This particular check is AFTER initial fixture writes, not an all-effects-before-preflight gate. It does not by itself inspect memberships, all effective rights, owner identity, or existing unrelated objects. Genuine product compile/attach admission adds its own contract checks; it is not a substitute for coordinator authorization and exclusive test resource ownership. _async_factory uses the same runtime URL and async psycopg connection, without changing roles.

## Approved contract distinctions to retain

Owner A7 Sentinel_4fec7289f29081d196b9295f436fb190 says Cryptalis prints deployment grants/revocations/session terminations but never executes them; owner ACL-01 Sentinel_e1abe646a87081d194a97aea302be80d allows exact transactional inventoried restoration without additional effective rights and keeps runtime-role changes operator-controlled. The fixture explicitly describes itself as owner setup, not product migration. The later ship-first attachment preserves approved PostgreSQL resources and previously approved permissions. None of these facts alone decides the current fixture permission classification.

Root's smallest concrete decision can distinguish (a) four object ACL statements on exclusively new disposable fixture objects to the existing runtime role, (b) committed schema/table/index/data lifecycle and exact CASCADE cleanup, (c) any distinct role/cluster/credential/session/global action, which is absent from this selected source but must remain excluded. Correct84 rather than68 if selecting the full current file, or state the narrower selector scope honestly. Current readiness and action approval remain separate; no execution or hold removal follows from this inventory.

## Source identities

- tests/test_sqlalchemy_search.py: 0d9de8f210d482db210b982e0aa2b027e989e0deb589114a753ee4dfbf869015
- tests/test_sqlalchemy_flush_preparation_failure.py: 8e86b882cc1a41d3a0971fa0b4f58e696ccf9e5c9647ed0844e21168c2055ee0
- tests/conftest.py: fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd
- scripts/test_postgres.py: 118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12

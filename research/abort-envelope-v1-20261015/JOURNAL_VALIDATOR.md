# Physical journal relation validator specification

Status: proposed source-level contract, NOT IMPLEMENTED / NOT RUN. It applies
only to new explicit successor admission and later selected v3 execution.
Do not retrofit it into historical safe abort or rewrite any existing journal.
Current migration._runtime_permissions validates owner/effective runtime rights;
it does not prove the complete physical table/PK structure below.

## Identity and observation order

1. Bind the authenticated target tuple, current intended database/maintenance
   owner, exact journal_schema, and fixed name _cryptalis_journal. Resolve with
   pg_catalog.pg_namespace + pg_class by exact names. Do not depend on search_path.
   Do not invent a historical table OID, PK/index name, or TOAST identity.
2. For a read-only proposal use one consistent snapshot, bounded observations,
   and no fixes. It is a proposal observation, not a concurrency guarantee.
3. For later mutation, use the existing same-scope advisory lock, documented
   sorted transition-table locks, then journal-table lock in one reviewed order.
   SHARE ROW EXCLUSIVE on the exact journal is the design candidate. Its purpose
   is to exclude ordinary DML/sibling insert as well as incompatible structural
   DDL. A row-level FOR UPDATE alone is insufficient.
4. Re-resolve and compare the relation OID under those locks; inspect all shape,
   owner/ACL, row counts, lineage and target facts within that transaction before
   effects. A relation changed between proposal and expansion is revalidated;
   no historical identity is fabricated. Preserve all observed identities during
   the new operation. Use properly quoted identifiers and bound values.
5. Table locking does not by itself prove concurrent role-membership, routine,
   schema privilege, or administrative changes are excluded. Preserve the host
   maintenance-authority exclusion and existing permission/routine checks.
   Native lock behavior is an open controlled-test question.

## Required relation and column shape

Reject if any expected observation is missing, duplicated, truncated, ambiguous,
or unknown. Catalog object identity uses schema plus built-in type/operator/
access-method identity, not a display string that a user can shadow.

- pg_class relkind='r', relpersistence='p', ordinary local heap table; not view,
  materialized view, foreign, temporary, unlogged, partitioned, or partition.
  No pg_inherits edge in either direction. No RLS/FORCE RLS or pg_policy rows.
  No user rewrite rules or user triggers. Under the exact fixture shape there
  are no extra internal triggers either; PK uniqueness is index-backed.
- Exactly three positive live attributes, ordered attnum 1,2,3, and no dropped
  user attribute hiding a prior incompatible shape:
  1. operation_id: pg_catalog.uuid, NOT NULL, typmod=-1, collation OID 0.
  2. plan_digest: pg_catalog.text, NOT NULL, typmod=-1, the built-in default
     collation selected by the original unqualified text declaration.
  3. state: pg_catalog.jsonb, NOT NULL, typmod=-1, collation OID 0.
- No domain substitute, array substitute, custom type, default expression,
  generated expression, identity, missing-value rewrite metadata, or unexpected
  column ACL. Resolve pg_type/namespace and pg_attribute facts directly.
  A server's built-in default collation is resolved, not a hardcoded numeric OID.
  Column storage/compression/statistics differences must be classified explicitly;
  the narrow initial fixture may require defaults. Do not silently assume an
  uninspected setting is safe, and do not rewrite it to obtain acceptance.
- Defaults must be absent in pg_attrdef as well as the attribute flags. Exclude
  unexpected row-level write behavior, rules, trigger functions and policies by
  their catalog entries, not only cached relation flags.

## Primary key and indexes

- Exactly one applicable user constraint: validated nondeferrable/nondeferred
  PRIMARY KEY on operation_id alone. conkey=[attnum 1], confrelid=0, no inherited
  parent/child constraint, and exact conindid linkage to the backing index.
- Exactly one ordinary user index, the PK backing index; do not guess its name.
  Same table and namespace/owner; native btree access method, built-in uuid_ops,
  no custom operator family, sort/collation, expression or predicate semantics.
- indnkeyatts=1, indnatts=1, indkey=[1]; no INCLUDE attributes. Require unique,
  primary, immediate, valid, ready and live. No exclusion semantics. Verify
  indcollation=0 and the ordinary ascending/null-order options. Handle
  indnullsnotdistinct explicitly for PostgreSQL 16; the original plain PK
  declaration uses the normal default. No invalid concurrent-build remnant.
- No extra CHECK, UNIQUE, exclusion, foreign-key, incoming foreign-key, or
  index object. Read constraints in both directions. A missing/deferrable/
  duplicate-permitting PK invalidates count-plus-chain membership reasoning.

These are proposed exact-fixture semantics, not claims about every permissible
PostgreSQL table. A source review cannot establish that each catalog column or
representation is observed correctly by a future validator.

## Owner and ACL contract: choose before implementation

Require journal and backing index owner to equal the authenticated planned
maintenance owner. Resolve identities through catalogs rather than trusting
names read from a JSON row. Inspect namespace ownership/ACL and relation/column
ACLs, effective privileges, and role reachability. Keep the existing
_runtime_permissions algorithm for PUBLIC, inheritance, SET/ADMIN reachability,
dangerous role attributes, owner reachability, schema CREATE, routines, and
journal writes. The new structural check supplements it; it never weakens it.

The proposed narrow fixture policy is:

- maintenance owner retains its inherent owner authority; its ordinary explicit
  owner ACL, if present, must not give authority to another role;
- the planned runtime role has effective SELECT; its direct grant, when present,
  has no grant option;
- PUBLIC has no journal privilege; no runtime-reachable role can INSERT,
  UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, or SELECT WITH GRANT OPTION;
- no nonowner column grant or other unreviewed relation grantee is accepted;
  no unreviewed schema principal can replace or introduce executable objects
  through CREATE. Namespace-owner/administrator powers remain in the explicitly
  trusted maintenance boundary;
- no GRANT, REVOKE, owner change, role change, or ACL repair is performed.

Root must select this ACL admission policy or a precise alternative before any
implementation. Existing unrelated read-only monitor grants cannot be silently
treated as historical proof or automatically removed. They cause a read-only
successor-admission decision under this narrow proposal, not a legacy-abort
refusal. Raw relacl=NULL is not 'no privileges': resolve owner/default semantics
and effective rights. Parse ACL entries structurally (grantee, privilege, grant
option and grantor), not as an unordered display substring. Superusers and
trusted administrative changes are outside an ACL-only exclusion proof.

## Dependencies and retirement safety

Inventory relevant pg_depend/pg_shdepend links in both directions, plus explicit
FK/rule/trigger/policy/inheritance links. Allow only classified ordinary internal
relation/row-type/PK/index/TOAST and built-in type/namespace/owner dependencies.
Identify these by native linkage and dependency kind, never by a name prefix or
an invented historical OID. Distinguish a journal's normal dependency on its
namespace from an external view/routine/object depending on journal contents.
Unknown dependencies, extension ownership, external dependent objects, or an
object requiring CASCADE are refusals before effects. No CASCADE or automatic
dependency removal is permitted.

Dependency graph classification is still unimplemented. The exact expected
catalog set must be established from an independently created original-shape
fixture and reviewed on PostgreSQL 16 before broad use. A database count or
JSON-only state validator cannot substitute for this check.

## Bounded row inspection after physical validation

Once a real native unique PK is proved, exact row count plus a complete verified
no-repeat chain can establish set membership. Row count alone cannot. Perform
all count/point-read/chain steps under the same snapshot and, for mutation, the
same insertion-excluding lock. Require exact authenticated expected categories:
forward-aborted ancestors, active source, validated aborted reverse attempts,
and the current row when present. No category overlaps or gets inferred from
an arbitrary ABORTED string.

Before transferring each state, use a parameterized point SELECT for
jsonb_typeof(state) and octet_length(convert_to(state::text,'UTF8')), plus exact
operation_id/plan_digest. If the selected transfer ceiling is exceeded, stop
that new successor proposal without fetching or mutating the entire state.
Only after length/type admission fetch the bounded state text, independently
canonicalize/validate it, and verify its authenticated commitment and links.
Prevent a race between size preflight and fetch by the approved snapshot/lock;
check identity/length again if that guarantee is absent. Do not fetchall history,
cache every ID/state, truncate, skip malformed rows, or trust server hashes as
host authorization. Active-source rows use their separately admitted contract.

## Required independent negative cases (none executed)

The controlled fixture must detect each changed shape before any new effect:
wrong relation kind/persistence/namespace; hidden dropped/extra column; reordered
columns; nullable column; domain/custom type/collation; default/identity/generated
column; missing/deferrable/wrong-key/invalid/not-ready PK; index INCLUDE/expression/
predicate/opclass alteration; added index/constraint/FK; RLS/policy; rule/trigger;
external dependency; extension membership; wrong owner; PUBLIC or column grant;
runtime SET/ADMIN/INHERIT path; schema CREATE; missing or extra history row;
competing sibling inserted during inspection; and administrative ACL drift.

Use separately authorized disposable fixture mutations with an independently
observed native oracle. Record exact pre/post facts and typed refusal, including
the invariant that already-admitted legacy abort remains available. A generic
parser failure or no-op mutation does not count as a physical-validator test.

# Required/default cache parity: source-only mechanism review

Date: 2026-10-14. Status: NO QUALIFYING PUBLIC-ONLY CORRECTION ESTABLISHED.
This is source/documentation review, not execution evidence. No candidate imports,
tests, DB work, dependency changes, private-hook prototype or Git actions occurred.
Only this new notes directory was written. Existing evidence remains unchanged.

## Result and priority

C9-NATIVE-CACHE-01 is an unresolved admitted SELECT compatibility discrepancy.
It is not the unsupported omitted-ORM-UUID-default route. Both installed dependency
versions have the discrepancy. Existing protected operation-fresh behavior agrees
with documented per-call bind semantics in the four recorded cases, while default
native warmed behavior does not. This supports an implementation-anomaly inference;
it does not establish an upstream acknowledged bug, novelty, a fix in another
release, or permission to waive the product's exact-native objective.

No inspected public API supplies the required operation: resolve the original
statement using exactly its native shared compilation-cache history, without
executing it, then transfer only effective parameter/error semantics into a new
operation-isolated protected compilation. No universal API-impossibility claim.

## Exact existing evidence (not rerun)

- ../candidate-accel-search-material-20261013/tests/test_c9_postgres_cache_order.py
  defines four sequences in ORDERS and test_c9_required_default_cache_order_observations.
- That candidate's tests/test_c9_postgres_guard_plans.py:38-68 constructs the
  same tenant-scoped SELECT of IDs with expanding Text bind named needles.
- ../evidence/c9-cache-order-sa21-20261014/junit.xml and corresponding sa20
  record all four mismatches, not parity passes. Both original and C9 agree.
- ../candidate-notes-native-bind-cache-20261014/{REVIEW.md,compiler_only_probe.py,
  compiler-only-sa20.json,compiler-only-sa21.json} supply earlier independent
  source/compiler characterization. This review does not run that private-API probe.
- ../../persistence-recovery-20261013/c9-cache-remote-verification.json records
  exact remote source/evidence at 81b3b4c49391b23357d291a0a28c8a22548f7805.

Second operation outcomes, identical on both pinned versions:
1. missing -> default-tuple: native StatementError/InvalidRequestError cd3x;
   protected returns IDs 1002,1003.
2. required-default -> default-tuple: same mismatch.
3. default-tuple -> missing: native empty rows; protected cd3x error.
4. default-tuple -> required-default: native IDs 1002,1003; protected cd3x error.

## Pinned primary source

Prefixes relative to cryptalis-executable:
- SA21: repo/.venv/lib/python3.12/site-packages/sqlalchemy (2.1.3).
- SA20: release-lab/s19-removal-boundary-sa20-20261013/lib/python3.12/site-packages/sqlalchemy (2.0.51).
SOURCE_PINS.json hashes the source files read, including both version declarations.

### Public semantics

SA21 sql/_elements_constructors.py:703-707 says the bind's default value is used
when no execution override is supplied. Lines 742-748 say required=True demands
an execution value, with default required state depending on value/callable input.
SA20 has the same contracts at 615-619 and 654-660. No inspected documentation
makes these promises contingent on which structurally equivalent statement was
previously executed. The reproducer uses ordinary documented bindparam/IN/SELECT,
not expanding executemany (which is explicitly unsupported).

Current online primary references corroborate these contracts; their 2.0 docs
identify release 2.0.54, not the installed 2.0.51, so they cannot prove changes:
- https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam
- https://docs.sqlalchemy.org/en/20/core/connections.html#sql-compilation-caching
The second describes caching as transparent and says it does not affect query
results. No release upgrade or issue-tracker resolution was investigated.

### Exact observed mechanism

SA21 sql/elements.py:2076-2079 infers required. Its _gen_cache_key at 2246-2272
includes type, key and literal_execute but excludes required and default values.
SA20 counterparts are 1990-1993 and 2160-2184. Value exclusion is necessary for
ordinary reusable bound queries; absence of required is the relevant distinction.

SA21 sql/elements.py:694-746 _compile_w_cache combines structural key, dialect,
execution parameter keys, schema-translation presence and executemany state. It
stores the compiler before parameter construction can fail. SA20:683-727.

SA21 sql/compiler.py:1990-2089 matches incoming extracted binds, but tests the
cached compiled bind's required flag before using the incoming bind's value.
SA20:1888-1978. Thus changing incoming values does not update required semantics.
The first failed required execution still populates the native compiler cache.

SA21 engine/base.py:1630-1684 performs before_execute, chooses the cache, calls
private _compile_w_cache and initializes the execution context with extracted
binds. This is the actual stage that a mirror would have to reproduce faithfully.

## Public mechanisms assessed

1. ClauseElement.compile(bind=engine or dialect=...): documented, but SA21
   sql/elements.py:257-319 directly calls _compiler. It does not consult or update
   the engine execution cache. Fresh compilation therefore loses warmed history.
2. Compiled.params: SA21 sql/compiler.py:2132-2142 calls construct_params with
   _check=False. This debugging accessor specifically bypasses required checks;
   it is not a substitute for native execution parameter validation.
3. SQLCompiler.construct_params: resolves a compiler's binds, but incoming
   extracted_parameters require an original cache key and private bind-match
   structures (1990-2006). A fresh compiler resolves current semantics only.
   A cached compiler still must be selected by exact native history, and manual
   invocation may evaluate callable binds outside native timing/error handling.
4. Public Connection/Engine execution_options(compiled_cache=dict): source
   engine/base.py:290-304 documents a storage override, including None to disable.
   It does not offer public compile-only execution. Caching rewritten protected
   statements is unsafe because processors bind operation-owned state, and their
   structural shape differs from the native statement. A second dictionary is
   not automatically a matching native cache: eviction, failures, interleaved
   unrelated calls, connection overrides and cache clearing all affect history.
5. CacheKey.to_offline_string: sql/cache_key.py:297-330 incorporates SQL and
   repr(bound values); it is not the engine lookup key. Native key generation
   uses private _generate_cache_key. SQL strings or value-derived substitutes
   cannot establish native structural equivalence or lifecycle; they can also
   retain sensitive search values unnecessarily.
6. Public before_execute/before_cursor_execute/DialectEvents: the early event
   precedes native compilation; late events occur after construction and cannot
   recover a required-bind failure that prevented them from firing. Executing an
   auxiliary native statement to obtain the cache decision would introduce
   extra queries/callbacks/events and potentially plaintext. Not proposed.
7. Clearing/disabling native cache or always supplying defaults explicitly can
   avoid this symptom, but changes the oracle/application execution contract.
   Neither is a protected runtime correction or warmed-native parity proof.

S20 sqlalchemy.py:1040-1044 must retain compiled_cache=None on protected paths;
_Payload.cache_ok=False and _sqlalchemy_search's operation-bound processors stay
unchanged. No tenant, point, prepared-key, lease, PID, strict-text or final-driver
boundary may be weakened to obtain a cache hit.

## Decision choices; none adopted here

A. Keep exact deployed-native behavior as the criterion. Leave C9 open and retain
   all four failures. Require a concrete safe public mechanism or a separately
   authorized architectural investigation; no broad mirror implementation yet.
B. Seek dependency-level resolution, then requalify an explicitly selected version.
   A corrected upstream dependency could remove the native discrepancy while
   preserving current protected isolation. Availability and suitability are
   UNKNOWN; source research or drafting a report is distinct from authorized
   external submission, installation or dependency changes.
C. Explicitly approve a narrowly documented exception: these cache-order anomalies
   follow documented per-call bind semantics, with warmed-native deviations still
   published. This changes the exact-native promise and cannot be silently treated
   as meeting the original objective. No such decision is implied or requested by
   this source review.
D. Restrict these already-admitted query sequences or require explicit parameters/
   cache normalization. This is a compatibility/adoption regression or oracle
   change, not a correction, and requires an explicit product decision. Not favored.

The conservative recommendation is A with source-only B research if requested.
Do not promote a documented-semantics pass to default-native compatibility.

## Independent oracle plan if a concrete mechanism emerges

Keep existing histories and evidence immutable. Use native, original S20 and the
new isolated correction with identical query histories on both dependency cells.
Compare full rows/types and error class/original cause/code, Session state,
transaction state and cursor counts. Include the four existing ordered cases,
explicit supplied-value controls, repeated equivalent statements and distinct
shapes. Native engine caching remains default and warm; no between-case clearing.

A history-sensitive design additionally needs real eviction, user-owned cache
options, clear_compiled_cache behavior, failed compilation/parameter construction,
unrelated queries and session/connection interleaving. These are proof obligations,
not presently authorized tests. Preserve errors at the native stage, without
extra callback evaluations or fabricated wrappers. Independently verify absence
of cached protected keys/processors and cross-tenant/lease/PID isolation, actual
wire plaintext exclusion and current NULL/empty-list/strict-input semantics.
Only after source review and appropriate execution authorization should any new
run occur. Cold/cache-disabled observations are diagnostic, never replacements.

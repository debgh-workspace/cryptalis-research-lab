# C8: indexed equality/IN cost attribution

Status: predeclared diagnostic, before database execution. No runtime correction.

## Exact question

On unchanged S18, how much admitted indexed equality/IN work comes from repeated
search-key derivation versus payload authentication, admission, compilation,
key preparation and transport? Does the number of search-key derivations equal
M + R for M non-NULL query terms and R returned non-NULL protected values, even
when the field, tenant and search generation are identical within that query?
The unique row-bound payload derivation is not interchangeable with this work.

This is distinct from held C1 public-metadata reuse and C5 admission skipping.
Their failed gates remain unchanged. No optimized path or before/after gate is
run here. A positive attribution result is only grounds to propose a separately
reviewed mechanism. It cannot establish speedup, safe caching or qualification.

## Source and authority

Copy exactly the 201 files in `INDEXED_PROFILE_SOURCE_MANIFEST.json` from S18
commit 5492cc04ee6c5d6696c9e9fc261f12fa61236043. Verify every file before and after.
Only this protocol, the manifest, workstream note and one test-only harness are
added. Product runtime, prepared-key/lease checks, query admission, CF1 framing,
AEAD/HKDF/HMAC and existing leakage opt-in stay byte-identical.

Coordinator only: unchanged lab_session.py and scripts/test_postgres.py with
fresh two-role preflights, serial PostgreSQL 16. First SQLAlchemy 2.1.3, then
2.0.51, once per cell. Worker does not run or start PostgreSQL. No new provider,
credentials, dependency, cluster, service or external AI. Scope is owned
synthetic schemas through the existing fixture. All seven gates remain UNKNOWN.

## Fixed workload

Use existing `single_tenant_public_cascade_application(rows=1000, unique=False,
public_table=False)` for independent native and protected applications. Existing
maintenance plan/apply/publish establishes the protected retained layout. The
fixture has 1,000 rows, seven repeated values (including NULL), C collation, one
explicit tenant, and native/CF1 equality indexes. Attach with one existing public
fixture Keyring instance, using its unchanged bounded cache and per-use leases.
No query processor or derived-key cache is added. This avoids charging creation
of the public fixture key factory to every query; it is not a speed comparison
with earlier factory-based runs.

Eight predicate families, each with IDs-only and ID+protected-text projections:
point (ID 600); equality miss; equality hot; IN-2 miss; IN-2 hot; IN-20 miss;
IN-20 with two hot and eighteen misses; IN-20 repeating those two hot values.
All results order by public ID. Expected counts are respectively 1, 0, 143, 0,
286, 0, 286, 286. M is respectively 0, 1, 1, 2, 2, 20, 20, 20.
The duplicate case tests repeated work without changing the result set.
No general query/type, range, prefix or confidentiality profile is added.

Independent native SQL uses a separate psycopg connection and bound values;
PostgreSQL `= ANY(text[])` supplies the IN oracle. Native SQLAlchemy and every
protected observation must match exact ordered native tuples. Extra untimed
controls: typed NULL equality, empty IN, IN [NULL], and IN [hot, NULL]. The typed
NULL equality remains SQL `=` rather than Python-None rewriting to `IS NULL`.

## Fixed observation schedule

For each of the 16 family/projection cells, fixed order as listed above:

1. Three warmup pairs, native/protected on even pair numbers and reverse on odd.
2. Ten recorded pairs in the same alternating order. Keep every observation.
3. Three separately profiled pairs in that order, outside latency summaries.

Each execution is measured in two API phases: `session.execute()` and `.all()`.
These are observed API boundaries, not assumed SQL or decryption boundaries;
the call graph establishes where actual work occurs. Record perf-counter,
MONOTONIC_RAW, process CPU and current-thread CPU for each phase. Retain GC
start/stop events and contemporaneous load/process usage. Never disable GC,
exclude observations, subtract noise or reinterpret C1/C5 failures.

Use cProfile with the current-thread CPU timer. Keep complete safe function and
caller statistics for each phase, without arguments, locals, SQL or binds.
Retain named counts for search derivation, payload derivation, term generation,
frame open, result processing, key resolution, admission and rewrite. Instrumented
CPU percentages are attribution hints; Python timer/profiler overhead makes them
unsuitable for a latency/speedup claim. Unprofiled means no cProfile, but clock
and GC measurement overhead still exists.

Capture each emitted application statement only in memory for one independent
read-only `EXPLAIN (FORMAT JSON)` through the runtime role. Retain only plan node
types, estimated rows/costs and whether an index node occurs. Never force index
selection; an admitted indexed representation does not guarantee the optimizer
uses that index at this selectivity. SQL, parameters and conditions are not
written to receipts. Owner `ANALYZE` is limited to both owned fixture tables.

## Finite decisions

- Validity requires exact native outputs for every sample/control, unchanged
  source, all 512 scheduled application executions (96 warmup, 320 timed,
  96 profiled), all 192 profile phases and 32 safe plans. Failure is retained.
- For the protected profiles, test the predeclared call-count prediction:
  `_term = M+R`, `_derive = M+2R`, `open_text = R` and `_resolve = 2M+4R`.
  IDs-only projections have R=0. These are diagnostic predictions, not an
  instruction to remove checks. Any mismatch is reported before interpretation.
- Report the `_derive` caller attributed to `_term` separately from its
  `open_text` caller. Rank this measured search-KDF CPU share against the other
  work. Do not sum inclusive times across nested functions.
- Propose a future correction only if the count prediction holds and the same
  avoidable work is observed in all three profiles of an applicable workload.
  Small attributed share is a useful negative result. No speed threshold is
  invented after measurement, and this diagnostic has no optimization gate.
- Any proposed sharing must remain invocation-local, preserve every before/after
  lease/context/generation check, and define exception, cancellation and thread
  cleanup. Persisting raw/derived keys on a reusable compiled processor is not
  authorized. Profiling itself adds no sharing or synchronization change.

This finite warm synthetic run does not qualify concurrent, cold-provider,
long-lived/expired, async, hostile-server, high-cardinality or production cost.
Existing equality/frequency/access/result-volume leakage remains explicit.

# C9 frozen serial handoff

Status: isolated research implementation. Pure compiler and crypto checks only.
No database test, benchmark, product promotion, or policy relaxation occurred in
this continuation. The coordinator owns all PostgreSQL execution through the
existing scripts/test_postgres.py wrapper and its unchanged two-role preflight.

## Pure evidence

Prior 74-case logs for each dependency cell remain unchanged. The new standalone
18-case suite covers shared named values across two fields, repeated predicates,
and a native plaintext predicate; mixed and all-NULL values; actual compiler-path
20-to-1 and 10-to-1 search derivations, 0-to-0 all-NULL, and unchanged list counts;
late generators, iterators, truth/iteration failure, no length-hint hooks, and
invalid text. Error comparison includes type and diagnostic contract fields;
operation IDs differ by design between independent operations.

The first combined run retained 85 PASS and 7 test-harness FAIL: six used an
incorrect compiler keyword; one compared intentionally unique operation IDs.
After harness correction, the 18 new controls pass independently on both cells.
Runtime source was not changed in this continuation. These checks do not prove
DBAPI wrapping, PostgreSQL truth values, driver adaptation, or planner behavior.

## Coordinator gates before timing (all remain unrun here)

1. Compare exact ordered rows and projected TRUE/FALSE/UNKNOWN for protected IN
   versus native IN and independent driver ANY(text[]). Cover NULL left side,
   empty and all-NULL right side, mixed NULL, duplicates, aliases, two fields and
   tenants, shared named values, repeated predicates, scalar/entity projections,
   and public-ID pagination.
2. Replace a generated eligible tuple bind before processing with another tuple,
   list, empty tuple/list, None, false scalar, invalid member and iterator. Compare
   exact outcome or original exception category/SQLSTATE and transaction state.
   Late replacement keeps ANY SQL; it cannot revert to expanding SQL. Empty and
   NULL truth-value equivalence is therefore a hard DB gate.
3. Mutate original list values at the existing event boundary: grow 20 to 21,
   clear, invalid member and shared-list cases. Prove all remain expanding IN.
4. Recheck required/missing values, unsupported expressions, original shared-name
   ambiguity refusal, positive IN versus NOT IN/equality controls, final cursor
   checks, lease expiry, PID/context and returned-row payload checks.
5. Compare custom/generic plans without forcing index use. Record index shape,
   adaptation, native failure and all correctness observations before timing.
6. Run existing affected selectors through the wrapper:
   tests/test_sqlalchemy_search.py, tests/test_cf1.py,
   tests/test_cf1_backend_failures.py, tests/test_key_lease_renewal.py,
   tests/test_sqlalchemy_thread_isolation.py. These selectors alone do not replace
   the additional C9 truth/replacement cases or the final full regression gate.

## Frozen performance protocol

R3 is the arithmetic authority, supplemented by the exact fixture/measurement
choices here. Both versions are pinned: SQLAlchemy 2.0.51 and 2.1.3, original
201-file S18/C8 baseline and this two-file candidate. Use the same C8 public
1,000-row single-tenant fixture (unique=False, public_table=False), warm Keyring,
ordinary GC, unchanged security checks and independently identical native rows.

Workloads in fixed order:
- IN-20 miss, IDs only: tuple('C8-missing-0' ... 'C8-missing-19'), 0 rows.
- IN-20 hot, IDs only: tuple('exact', '雪😀', 'C8-missing-0' ... 'C8-missing-17'), 286 rows.
- The same IN-20 hot tuple, ID plus returned text, 286 rows.
- Equality-hot 'exact', ID plus returned text, 143 rows.
- Point UUID(int=600), ID plus returned text, 1 row.

Construct explicit expanding bindparam needles with Text type and pass the tuple
as the execution value in BOTH original and candidate. Do not use literal
.in_(tuple), which SQLAlchemy may coerce to a fallback list. Before any timing,
observe actual cursor SQL and bind callback counts: candidate ANY(bytea[]) and
one query HKDF versus original expanding IN and twenty. A list control must show
expanding IN and twenty in both. Returned-text derivations stay unchanged. Remove
all instrumentation before measurement. A fallback-only run is invalid.

Each cell: seven blocks, all five workloads per block. Variant order is native,
original, candidate in even zero-based blocks; candidate, original, native in odd
blocks. Per variant/workload/block retain ten warmups then forty measured samples.
Exactly 5,250 executions per version (1,050 warmups, 4,200 measured), excluding
explicitly separate untimed correctness/path gates. No timing retries or filters.
Each sample times execute plus full fetch and close; row equivalence is checked
outside its timed interval. Retain start/end and elapsed wall/RAW/process/thread
clocks, row checks, run order, source/dependency hashes and failures. Flush raw
receipts on failure. Do not run cProfile or use instrumentation during timing.

Compute each variant/workload's seven measured wall block medians, then their
median. Each primary IDs-only workload must improve >=5% and have >=6/7 strictly
favorable blocks on EACH version. Each of the three controls must have aggregate
candidate/original <=1.10. No averaging versions or compensating workloads.
Separately report nearest-rank p95 (rank 266 of 280 measured observations) for
candidate minus equivalent native p95: <=3 ms equality, <=8 ms each IN-20
projection. Report native/original medians and p95 too. Keep all nominal outcomes
and clock anomalies. No claim of product performance from either gate alone.

Before execution, bind the coordinator's executable harness hash to this plan and
freeze any required implementation clarification. This handoff is NOT an
executable DB/profile harness and does not claim those missing gates are passed.
C1 and C5 remain held; returned-row reuse is excluded.

# C10 fixed-literal term-framing protocol

Status: STAGED, NOT EXECUTED. The coordinator must review the final source,
harness, arithmetic, selectors and this protocol before copying them into the
candidate or creating either approval file. No database, benchmark, source
promotion or wrapper modification is authorized by this document.

C10 is a narrow diagnostic mechanism experiment. The baseline is exact S20,
not C9. Failed C9 evidence and disposition remain untouched. Native compatibility,
C1/C5, all full qualification gates and production/independent-review gaps remain
OPEN regardless of a C10 mechanism result.

## Frozen inputs and source isolation

- Baseline: `candidate-s20-restored-20261014`, all 208 files in the manifest.
- Candidate: `candidate-accel-term-framing-20261014`, same 208 inherited files,
  with only `src/cryptalis/crypto/cf1.py` changed.
- Baseline manifest file SHA256:
  `eff60dbe9dc7b2c428f4623f8a945312e2dbdc54219a53594f19685ab6e57d6b`.
- Candidate cf1.py SHA256:
  `8c6a3ad82865734200424b6ab949ef46c38540561be20b743188073fbf593fb4`.
- New pure oracle `experiments/test_term_literal_framing.py` SHA256:
  `c0462824c21b7a3ed28007fd609d84d2d69d4961fe63e3109b216014a763065e`.
- Original cf1.py and `experiments/c10_baseline_cf1.py` SHA256:
  `d74abd2558023bf5ce1598fba0b61bb27198623dc56fb94ace24753531705278`.

Only two `_term` tuple assemblies change. Public fixed count/length/literal
fragments may persist; dynamic field bytes and encoded text are validated and
assembled afresh on each call. No field-specific info, root/salt, raw or derived
key, HMAC object, plaintext, encoded value or result cache is added. All other
functions, SQL rewriting, provider/lease checks, result ownership and wrappers
remain S20. The source gate rejects any other inherited-file change and any
extra runtime source file. Pure vector/failure-boundary receipts are separate
prerequisites and do not constitute native PostgreSQL evidence.

Native and original workers import the complete baseline source tree. Candidate
workers import the complete candidate source tree. Each worker verifies the
adapter import path and all 208 expected hashes before setup and after actual
fixture teardown. No monkeypatched original implementation or in-memory source
replacement is used in the correctness comparison or timed intervals.

The unchanged lab_session/test_postgres admission wrapper retains its serial
PostgreSQL lock and fresh two-role probes per dependency cell. Only the root
coordinator invokes it. A failed probe stops that attempt. Children inherit the
already-admitted environment for that same disposable lab database. They do not
read credential files, log environment values, restart PostgreSQL or rerun the
wrapper. The harness does not change wrapper configuration or admission rules.

## Correctness and regression admission before timing

Both pinned SQLAlchemy versions, 2.1.3 and 2.0.51, must pass. Dependency versions,
installed RECORD hashes and the exact interpreter are retained. No cross-cell
pooling or substitution is permitted.

1. Reuse the completed, unchanged-source 213-case affected-regression JUnit
   receipts per cell. Selectors are listed in `C10_SELECTORS.json`. Do not rerun
   a completed regression batch merely to combine receipts.
2. Require the 55-case pure candidate framing, independent CF1, dynamic operand,
   failure-boundary and primitive-count receipts already reviewed by the root.
   Timing admission validates their version, clean exit, exact 55-pass counts,
   empty failed-node list, unchanged-source flag, import origin and source/test
   hashes against the frozen candidate. These are not timed
   results and do not replace PostgreSQL evidence.
3. Execute the new source-isolated PostgreSQL gate and supplemental selectors in
   one separate JUnit receipt per cell. The new gate creates three source-pinned
   child processes serially. It tests 96 deterministic scenarios per variant:
   two tenants, direct/aliased fields, eight IN sets, eight equality operands,
   and eight fixed points with lazy iteration. IN covers empty, NULL, all-NULL,
   mixed NULL, duplicate, Unicode, miss20 and hot20 values. Shared bind names
   span two protected fields plus a plain field. It compares projected SQL truth,
   selected IDs, returned text, ORM entities and pagination. Native truth and
   text are independently selected using a separate psycopg connection; native
   SQLAlchemy results must match that driver before they are admitted as the
   original/candidate comparison. Invalid integer/bytes/NUL/surrogate text must
   preserve protected typed failure and pre-cursor refusal. Every Result and
   fixture is actually closed before source-after success.
4. Supplement with existing strict tuple, key-preparation cancellation, database
   cancellation and transaction-cleanup oracles. SQLAlchemy 2.1 additionally runs
   its native async collection-method tests. These APIs do not exist in 2.0, so
   those selectors are explicitly inapplicable and absent there. This is a
   documented scope difference, not an equal-coverage claim or accepted skip.

Before each new run, the coordinator reviews and freezes the exact collected
(classname, testcase-name) inventory as `experiments/C10_SAFETY_COLLECTION.json`.
It has version keys, each mapping `affected` and `supplemental` to arrays of
2-element classname/name arrays. The completed affected inventories are copied from their original JUnits.
Supplemental inventories are derived before execution from preserved S20 full
JUnits by the exact selected module/test-family prefixes, plus the new correctness
node. An explicit collect-only inventory can also be reviewed before execution.
Never derive a smaller passing inventory after a failure. Timing validates each receipt hash and exact inventory, rejects all
failure/error/skip nodes at any XML level and nonzero suite error/failure/skip
or disabled counters, requires all 213 affected cases and required module
families, and checks version-specific collection coverage. Missing evidence
blocks timing. Source or harness changes require review and a new frozen protocol.

## Timed fixture and independent native oracle

Each of the three persistent workers creates the exact C8 fixture once:
`single_tenant_public_cascade_application(rows=1000, unique=False,
public_table=False)`. Protected variants use unchanged maintenance run/publish,
one public-fixture Keyring and the existing deployment pin. Each fixture receives
ANALYZE outside timing. Each worker retains its fixture, engine and Session for
all seven blocks. GC remains enabled at unchanged ordinary thresholds. There is
no per-batch reset of those objects or SQLAlchemy compiled caches.

A separate psycopg connection materializes ordered expected native rows from
the native worker's committed fixture. Native bound `= ANY(text[])`, equality
and public-ID point SQL provide the oracle; this native-only oracle SQL does
not imply a protected ANY optimization. Each oracle transaction and connection
closes before untimed gates, samples or native-schema teardown. All three
workers require identical oracle hashes and prescribed row counts.

## Workloads and order

Seven blocks run in order 0 through 6. Every block uses this workload order:

1. IN20 miss IDs: `C8-missing-0` through `C8-missing-19`; 0 rows; CONTROL.
2. IN20 hot IDs: `exact`, `雪😀`, then `C8-missing-0` through `C8-missing-17`;
   286 rows; CONTROL.
3. Same IN20 hot values, public ID plus returned text; 286 rows; PRIMARY.
4. Equality `exact`, public ID plus returned text; 143 rows; PRIMARY.
5. Point UUID(int=600), public ID plus returned text; 1 row; CONTROL.

Every IN query uses an explicitly typed Text expanding bindparam with its tuple
supplied in the execution parameters. No default-bearing or `.in_(tuple)` query
shape is substituted. Even blocks execute native/original/candidate; odd blocks
execute candidate/original/native. Within each workload/variant/block retain
exactly 10 warmups then 40 measured observations. Each cell therefore retains
5,250 observations: 1,050 warmups and 4,200 measured. Workers run serially;
inactive workers wait on input. No sample is discarded, retried or selected.

## Untimed primitive and query-path checks

Before any timed sample, observe actual cursor SQL and fresh primitive calls
for all five workloads and a separate list20 miss control. All variants retain
expanding IN. Candidate must never take C9's ANY route. For M non-NULL query
operands and R non-NULL returned protected text values, both protected variants
must satisfy:

- `_term = M + R`
- `_derive(search) = M + R`; `_derive(payload) = R`
- `open_text = R`
- `PreparedKeys._resolve = 2M + 4R`
- Original generic `cf1.tuple_bytes = 3M + 6R`
- Candidate generic `cf1.tuple_bytes = M + 4R`

Only the two fixed `_term` generic tuple invocations disappear per term:
exactly `2(M + R)`. Native counts are zero. For the selected workloads, M is
20/20/20/1/0 and R is 0/0/286/143/1. No HKDF/HMAC/AEAD/check-count reduction is
accepted. All instrumentation is restored and event listeners are removed with
identity/absence assertions before timing. No cProfile or trace hook is active.

## Clock, resource and receipt boundaries

Each sample records start/end/elapsed values for perf_counter, MONOTONIC_RAW,
process and thread nanosecond clocks. The interval includes execute, complete
fetch and Result.close. Ordered-row comparison, hashes, IPC, JSON serialization
and receipt writes occur outside the interval. Retain all phases, block/workload/
variant/order/sequence/sample coordinates, counts, row comparisons and hashes.

Each batch records getrusage user/system CPU, voluntary/involuntary context
switches and process high-water maxRSS before/after/deltas outside sample clocks.
The coordinator records load averages before/after each batch when available.
These observations include receipt IO and can describe contention; they cannot
prove its cause and never filter samples or adjust thresholds. All raw samples
are flushed immediately. Partial receipts and safe failures remain on failure.

Negative elapsed clocks and absolute wall-minus-RAW disagreement above 1 ms are
flagged without removing observations. All raw clock values and disagreement
min/max remain in receipts. A clock anomaly must be disclosed and reviewed; it
never licenses a silent timing rerun.

Worker startup has a 300-second receipt deadline; each subsequent timing receipt
has a 180-second deadline. Raw pipe reads also bound partial-line stalls. Closure
receipts and initial exit waits each have 60-second deadlines, followed by a
10-second termination grace and 10-second kill/reap grace. A timeout stops the
run and retains partial evidence, never retries an observation. Cleanup attempts
continue for every worker and retain forced-termination/cleanup failures.
Workers start in their own process groups. The Linux parent-death safeguard
terminates a worker with SIGKILL if its coordinator exits; the startup parent-PID
check closes the race before the safeguard is installed. Explicit forced cleanup
terminates/kills the whole owned process group. Fixture workers do not create
further processes. Correctness workers each have a 300-second whole-process
deadline with the same process-group cleanup. These are
failure containment limits, not sample-quality filters.

Each worker acknowledges closure only after actual Session/fixture teardown and
source-after verification. Complete metadata requires every acknowledgment,
matching source and a clean exit. Summary arithmetic can exist before teardown;
a summary with incomplete metadata is not admitted evidence.

## Frozen arithmetic and decision

For each workload/variant, calculate seven measured wall-time block medians,
then their median. Both PRIMARY hot-text workloads individually require:

- At least 5% lower candidate median-of-block-medians than original.
- At least six of seven paired blocks strictly favorable to candidate.

Every CONTROL independently requires candidate/original aggregate median ratio
at most 1.05. All five conditions must pass on each dependency version. Do not
pool versions, use profiler reductions as a replacement, relax 6/7 to 5/7, or
substitute an IDs-only primary after seeing results.

Separately, nearest-rank p95 is sorted rank 266 of each variant/workload's 280
measured observations. Candidate minus native p95 must be <=8 ms for each IN20
projection and <=3 ms for equality-hot-text. Point added p95 is reported without
inventing a new threshold. Original/native medians and p95 remain visible.

`mechanism_admission_pass` equals the complete relative outcome.
`nominal_performance_pass` requires BOTH the relative outcome and every absolute
p95 budget. Both pinned cells must satisfy a claim; one cell cannot rescue the
other. Failure of an absolute budget prevents even a nominal full performance
pass. `product_qualified` is always false: full compatibility and security
qualification remain independent and OPEN. Performance FAIL is a retained result,
not a pytest execution error inviting an unchanged timing retry.

## Root-owned execution-control files

No approval/control file is prepared by this worker. The root creates them only
after final review, in the candidate's experiments directory. They contain no
credentials and cannot substitute for wrapper authorization/admission.

`C10_CORRECTNESS_APPROVAL.json` has exactly:
- coordinator_approved: true
- protocol_sha256, harness_sha256, timing_harness_sha256
- candidate_cf1_sha256, baseline_root
- cell_output_directories: both pinned versions, distinct new absent directories

For this file, harness_sha256 identifies `tests/test_c10_postgres_gates.py` and
timing_harness_sha256 identifies `tests/profile_c10_timing.py`.

`C10_COORDINATOR_APPROVAL.json` for timing has exactly:
- coordinator_approved: true; diagnostic_only: true
- whole_compatibility_gate: "OPEN"
- protocol_sha256, harness_sha256, arithmetic_sha256
- correctness_harness_sha256, safety_collection_sha256
- baseline_root, candidate_cf1_sha256
- cell_output_directories: both versions, new absent directories
- safety_junit: each version maps affected/supplemental to {path, sha256}
- pure_receipts: each version maps to the reviewed 55-case JSON {path, sha256}

For timing, harness_sha256 identifies `tests/profile_c10_timing.py`. The explicit
selector is `tests/profile_c10_timing.py::test_c10_frozen_timing_protocol`.
The profile filename remains excluded from ordinary test discovery. The timing
output has metadata.json, samples.jsonl, summary.json and variant stderr logs;
correctness has correctness.json and each worker's raw JSON/stderr receipts.
No existing output directory is reused or overwritten.

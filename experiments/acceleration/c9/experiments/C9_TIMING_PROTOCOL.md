# C9 executable timing protocol

Status: staged implementation, syntax checked, NOT EXECUTED. Timing remains
blocked until the twenty provided-input admission/lease/PID/cursor/payload/plan
safety cases pass on both cells and the coordinator approves this exact protocol.
The whole twenty-one-case compatibility gate stays OPEN: native cached
required/default omission behavior differs from both original and candidate.
The coordinator has bounded this as a DIAGNOSTIC-ONLY supplied-value experiment;
it does not clear that gap, qualify C9, or authorize a runtime change.

Authority: the unchanged C9_SERIAL_HANDOFF.md and C9_BIND_BATCH_PROPOSAL_R3.md.
The arithmetic and workloads below implement their frozen requirements. Any
material discrepancy stops execution; no compensating workload, retry, filtering,
threshold relaxation, or cross-version averaging is permitted.

## Persistent source-isolated cell

The coordinator enters one unchanged lab_session/test_postgres wrapper per
dependency cell, retaining its serial PostgreSQL lock and fresh two-role
preflight. Only then may the pytest selector
`tests/profile_c9_timing.py::test_c9_frozen_timing_protocol` start three persistent
child processes with that same pinned interpreter. No child starts PostgreSQL,
reads a credential file, changes credentials, or reruns the wrapper. Children
inherit the already-admitted two-role environment solely for the same owned
fixture database. Credentials and environment contents are never recorded.

Native and original children import the exact original 201-file S18 source
installation; candidate imports the frozen two-file C9 candidate. Every child
asserts its imported runtime path and all 201 hashes before and after. Baseline
manifest SHA256 is aba658622e884084762e09be61aed54c7a1023af37d332af9f5143aa5e358688.
SQLAlchemy must be 2.1.3 or 2.0.51 and identical across all three children in a
cell. Dependency versions/installed RECORD hashes, Python version/executable,
and source/harness/protocol hashes are retained. No in-memory original rewrite
substitution is used for timing.

Each child owns one persistent exact C8 fixture throughout the entire cell:
`single_tenant_public_cascade_application(rows=1000, unique=False,
public_table=False)`. Protected fixtures use unchanged maintenance run/publish,
then attach with one public-fixture Keyring instance and the existing deployment
pin. All three fixtures receive ANALYZE during untimed setup. Each child retains
its session and fixture across all seven blocks; there is no per-batch fixture,
engine, session, or compiled-cache reset. GC stays enabled with ordinary unchanged
thresholds. Key leases, renewals, admission, final checks and returned-row work
remain unchanged.

A separate psycopg connection reads identical ordered native rows from the
native child's committed schema. Bound `= ANY(text[])`, equality, and public-ID
point predicates supply independent expected rows. Each child verifies identical
oracle hashes and required counts before any measurement. Each oracle connection
ends its read-only transaction and closes immediately after materialization,
before untimed gates, samples, or another child's native-schema teardown.

## Workloads, counts, order and boundaries

Block order is fixed at 0 through 6. Within each block the workloads are:
1. IN-20 miss, IDs only: tuple C8-missing-0 through C8-missing-19; 0 rows.
2. IN-20 hot, IDs only: tuple exact, 雪😀, C8-missing-0 through C8-missing-17; 286 rows.
3. Same hot tuple, public ID plus returned text; 286 rows.
4. Equality exact, public ID plus returned text; 143 rows.
5. Point UUID(int=600), public ID plus returned text; 1 row.

For each workload, variant order is native/original/candidate in even blocks
and candidate/original/native in odd blocks. Each variant/workload/block emits
exactly ten retained warmups and forty retained measured samples. Total per cell
is 5,250 observations: 1,050 warmups and 4,200 measured. No test-only override can
alter these counts, values, order, or projections. All IN statements use an
explicit Text expanding bindparam with tuple supplied as the execution value,
never `.in_(tuple)` or a default-bearing cached user bind.

Untimed setup gates observe actual cursor SQL and actual search/payload HKDF
counts for every workload and an explicit list20 miss control. Candidate must
use ANY for tuple IN and reduce twenty query search derivations to one. Original
and list controls must use expanding IN and twenty. Returned-text derivations
are checked separately and unchanged. All monkeypatch/event instrumentation is
removed and checked absent before samples. No cProfile is used.

Each sample starts wall/perf_counter, MONOTONIC_RAW, process and thread clocks;
executes, fully fetches, and closes the Result; then stops all clocks. Exact
ordered-row comparison, hashes, command transport, JSON serialization and disk
writes occur outside that interval. All four raw start/end/elapsed nanosecond
clocks, phase, block, workload, variant, order, sequence, row count/check/hash are
retained. Outside sample clocks, each variant records per-batch getrusage
user/system CPU, voluntary/involuntary context switches and process high-water
maxRSS before/after/deltas; the parent records load averages before/after each
batch when available. These batch observations include receipt IO. They may
describe contention but are not causal proof and never filter samples or alter
thresholds. The coordinator writes and flushes each observation immediately;
metadata and partial raw receipts are retained on any failure. No sample is
retried or discarded. Workers operate serially; inactive workers wait on input.

## Frozen arithmetic and interpretation

For each variant/workload, compute each of seven measured wall-time block medians
and take their median. Each primary IDs-only workload must improve at least 5%
and have at least six of seven strictly favorable candidate/original blocks,
independently on each dependency version. Each of the three controls must have
aggregate candidate/original ratio at most 1.10.

Nearest-rank p95 uses rank 266 of each workload/variant's 280 measured wall
observations. Candidate minus native p95 must be at most 3 ms for equality and
8 ms for each IN-20 projection. Point p95 difference is reported without an
invented limit. Native/original medians and p95 are retained too. Relative and
absolute outcomes are independently reported as nominal diagnostic outcomes;
neither alone nor together qualifies C9 product performance while the broader
compatibility gate remains OPEN. A performance FAIL is retained in summary.json, not turned
into an execution failure that invites a timing retry.

Negative elapsed clocks and absolute wall-minus-RAW disagreement above 1 ms are
flagged without filtering. All clock values and min/max wall-minus-RAW differences
remain in the receipts regardless of nominal PASS/FAIL. No observations are
combined across dependency versions.

## Coordinator inputs and outputs

Only after reviewing the final frozen protocol/harness hashes, the root
coordinator creates the nonsecret local execution-control file
`experiments/C9_COORDINATOR_APPROVAL.json` in the candidate. The unchanged
wrapper's explicit environment map is not modified. No arbitrary shell
configuration variable is required or assumed to reach pytest.

The JSON object has exactly these fields:
- coordinator_approved: true
- diagnostic_only: true
- whole_compatibility_gate: "OPEN"
- protocol_sha256, harness_sha256, arithmetic_sha256: exact reviewed file hashes
- baseline_root: verified unchanged original source root
- cell_output_directories: a map from "2.0.51" and "2.1.3" to new, nonexisting
  receipt directories; the actual imported SQLAlchemy version selects the cell
- safety_junit: a map from "2.0.51" and "2.1.3" to objects containing path and
  sha256 for each existing 20-of-21 provided-input safety JUnit receipt

The harness validates every reviewed hash, exact twenty case names and absence
of failure/error/skip in both safety receipts. It records the control-file hash
and safety receipt hashes with the excluded default/cache gap explicitly OPEN.
The file controls root execution only. It is not credential authorization,
cannot substitute for the required unchanged fresh-two-role wrapper admission,
and never clears the broader compatibility gap. No approval file is created by
the worker preparing this harness. It must be created by the coordinator only
after review; setting a boolean alone cannot establish the underlying evidence.

The harness creates metadata.json, samples.jsonl, summary.json, and one stderr
log per persistent variant. Metadata identifies the source/dependency versions,
untimed gates, oracle hashes, batch resource observations, child exits and
source-after checks. A child emits its closed acknowledgment only after actual
session/fixture teardown, and the parent requires that acknowledgment plus a
clean exit before marking the run complete. The output
directory is never reused or overwritten. The arithmetic helper is
`tests/c9_timing_arithmetic.py`; neither helper nor profile test is part of the
original 201-file runtime baseline. The profile filename is excluded from normal
`test_*.py` discovery and requires the explicit selector and approval hash.

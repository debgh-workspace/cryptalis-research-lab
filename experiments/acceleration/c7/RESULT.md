# C7 fixed-scope scan checkpoint

## Decision

The research scanner matched native equality/IN semantics and its bounded
structural-transcript checks. **It failed the existing cost envelope in all four
size/dependency cells.** Keep it as a small-scope confidentiality control, not a
promoted query path or an automatic fallback. No product runtime was changed.

Coordinator PostgreSQL results:

- SQLAlchemy 2.1.3 correctness: **4 PASS**, 2 cost tests deselected, 22.11 s.
- SQLAlchemy 2.0.51 correctness: **4 PASS**, 2 cost tests deselected, 20.26 s.
- SQLAlchemy 2.1.3 cost: **2 FAIL**, 4 correctness tests deselected, 34.31 s.
- SQLAlchemy 2.0.51 cost: **2 FAIL**, 4 correctness tests deselected, 33.97 s.

Both correctness runs covered N=1,000 and 10,000, two tenants and fourteen
equality/IN cases: **112 native comparison groups** across both versions. The
32 additional recorded control outcomes include refusal, incomplete-operation
handling and fresh-session recovery. Corrupted tail frames rejected early-page
and empty-IN requests; short-lease expiry happened after one completed partition
in all four fixtures. Protected SQL equality on storage-only fields still refused
before any observed driver call.

The first SA21 directory's `n1000` label is narrower than its actual scope:
`-k n1000` also selected `n10000`. The four JUnit nodes in each correctness run
are `test_fixed_scope_native_semantics_and_structure` and
`test_fixed_scope_admission_and_incomplete_results`, each with `[n1000]` and
`[n10000]`. That larger scope was preserved, not rerun.

## Exact cost outcome

Thirty timed alternating native/scan pairs per workload followed ten warmups.
All 640 observations, including 160 warmup observations, are retained. No
exclusion, noise correction, threshold change or repeat-until-pass was applied.

| SQLAlchemy | N | Workload | Native p50 ms | Scan p50 ms | Median ratio | Native p95 ms | Scan p95 ms | Added p95 ms | Target result |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2.1.3 | 1,000 | Equality | 1.229799 | 28.767656 | 23.392× | 1.658920 | 33.613360 | 31.954440 | FAIL, 3 ms |
| 2.1.3 | 1,000 | IN-20 | 2.357067 | 29.333466 | 12.445× | 3.939154 | 31.886851 | 27.947697 | FAIL, 8 ms |
| 2.1.3 | 10,000 | Equality | 3.489358 | 301.952931 | 86.535× | 82.690659 | 397.020558 | 314.329899 | FAIL, 3 ms |
| 2.1.3 | 10,000 | IN-20 | 13.215390 | 296.716795 | 22.452× | 114.592238 | 396.710593 | 282.118355 | FAIL, 8 ms |
| 2.0.51 | 1,000 | Equality | 1.377789 | 29.092117 | 21.115× | 1.808237 | 32.413532 | 30.605295 | FAIL, 3 ms |
| 2.0.51 | 1,000 | IN-20 | 2.673363 | 33.235534 | 12.432× | 41.954158 | 44.379860 | 2.425702 | **PASS**, 8 ms |
| 2.0.51 | 10,000 | Equality | 3.316293 | 310.285279 | 93.564× | 4.827170 | 372.723772 | 367.896602 | FAIL, 3 ms |
| 2.0.51 | 10,000 | IN-20 | 14.311711 | 309.360333 | 21.616× | 122.839664 | 417.865191 | 295.025527 | FAIL, 8 ms |

The SA20 1k IN-20 submetric nominally passes and must remain a pass. Its native
tail includes 41.954158 and 62.345818 ms observations against a 2.673363 ms median.
The median paired scan increase is 29.483208 ms and the scan is faster in only
2/30 pairs. Those other descriptions do not replace the predeclared p95 gate.
No cause is established for the native spikes; C6 cannot explain them. Equality
still fails in this size/cell, so its overall cost gate is FAIL.

The measured equality is the hot-value case: 91/909 rows match at 1k/10k. IN-20
returns 455/4,545 rows. These selectivities are part of this synthetic workload,
not a population estimate. Every successful scan reads all 1k/10k rows and counts
95,593/956,383 logical frame-plus-identity bytes. Those are not actual network
bytes or peak RSS. Process maximum RSS includes fixtures, drivers and earlier
operations; no isolated per-scan memory bound was proved.

## Claim boundary

Storage-only CF1 contains no equality term. Query-enabled packed CF1 does contain
one; scanning it would retain snapshot equality-class leakage. The independent
source/vector inspection and fixture decoder support this distinction without
claiming a new cryptographic proof.

The positive evidence is event-level SQL/bind and logical-partition equality
across valid predicates, plus native values, three-valued truth and pagination.
It does not establish timing, backpressure, network-packet or whole-transcript
independence. Each scan uses its own REPEATABLE READ transaction over an unchanged
synthetic fixture, not a shared/exported snapshot. Row/byte caps are checked after
a partition arrives, not before transport. Failure/cancellation and later
application traffic remain visible. Returned-row authentication does not prove
hostile-server completeness, freshness, authenticated NULL or metadata hiding.

The frozen protocol's broad cache sentence is corrected by the separate
`PROTOCOL_CLARIFICATION.md`: no new cross-scan plaintext/result cache was added;
the existing bounded Keyring cache and all per-use lease checks remain. Original
protocol and harness bytes are retained. All 195 S17 baseline files are unchanged.
C1 and C5 remain held failures; C6 is only its independent A/A diagnostic.

## Next independently motivated hypothesis

For the already selected **LSDD-PG-v1 logical-snapshot target**, investigate whether
an indexed design can limit authenticated CF1 payload work to returned rows,
instead of decrypting N rows on every request, without reintroducing a full-value
deterministic row tag. First compare construction-level lookup/merge counts for
N=1k/10k, retained updates U/N=1/2/4 and hot/rare queries; include matching update
history and encrypted-index work, not only final matches. Stop if state/history
work is unbounded or the observer can recover the omitted deterministic partition.
This would be a separate predeclared, authorized specification/counting study,
not a new optimization of the failed scan or a claim of a qualified PG scheme.
The [L-SDd primary paper](https://www.usenix.org/system/files/usenixsecurity24-mondal.pdf)
does not supply a ready-made PG lifecycle/completeness/uniqueness implementation.

This direction **does not preserve the scan's stronger structural query hiding**:
search/access/volume leakage remains. The owner must accept that distinct observer
contract. If hiding those channels is required, a separately specified oblivious
index/ORAM or private-retrieval design is needed; the scan result does not show
that any such alternative meets the current cost envelope. No privacy or cost
contract is weakened automatically.

## Recovery and evidence

`evidence/raw-receipts.json` contains all twelve original result JSON documents
in compact form. Its reconstruction rule was checked byte-for-byte against each
original SHA-256. `evidence/result-analysis.json` records exact floats, ratios,
paired summaries, JUnit node IDs and source hashes. `evidence/tests.log` preserves
the four safe logs; only connection fingerprint strings were omitted, with the
original full-log hashes retained. No environment dump or credential is included.
`source-binding.json`, the frozen protocol and executable test recover the exact
research question. Publication does not promote any runtime change.

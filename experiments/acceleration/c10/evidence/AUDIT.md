# C10 frozen timing: independent evidence audit

## Verdict

**Evidence integrity: PASS. Frozen relative performance gate: FAIL on both cells. Frozen absolute performance gate: FAIL on both cells.**

C10 remains outside S20. Retain the failed result without changing thresholds, selecting samples, substituting a control for a primary, pooling versions, or rerunning unchanged timing. Product qualification and the whole compatibility gate remain OPEN.

This audit read existing receipts and source files only. It executed no product code, database operation, test suite, or benchmark. Its only writes are new files in this audit directory. The independent arithmetic implementation does not import the C10 arithmetic helper. All read inputs were hash-checked again after the audit and remained unchanged.

## Frozen primary outcomes

Each primary required at least 5% reduction in the median of seven block medians and at least six strictly favorable paired blocks. Added p95 limits were 8 ms for IN20 and 3 ms for equality.

| SQLAlchemy | Primary | Reduction | Favorable blocks | Added p95 | Relative | Absolute |
|---|---|---:|---:|---:|---|---|
| 2.1.3 | IN20 hot text | 2.055% | 5/7 | 14.035163 ms | FAIL | FAIL |
| 2.1.3 | Equality hot text | 2.231% | 6/7 | 8.824318 ms | FAIL | FAIL |
| 2.0.51 | IN20 hot text | 2.541% | 6/7 | 14.005799 ms | FAIL | FAIL |
| 2.0.51 | Equality hot text | 1.565% | 3/7 | 9.201093 ms | FAIL | FAIL |

All four primaries miss the 5% requirement. SA21 IN20 hot text and SA20 equality also miss the six-block requirement. Both primary p95 budgets fail in each cell.

All three controls satisfy the frozen candidate/original aggregate median ratio limit of 1.05:

| SQLAlchemy | IN20 miss IDs | IN20 hot IDs | Point text |
|---|---:|---:|---:|
| 2.1.3 | 0.923635 | 0.975049 | 0.980981 |
| 2.0.51 | 0.971337 | 0.967915 | 0.983032 |

The two IDs-only IN20 p95 budgets pass in each cell. Point added p95 is descriptive only, as frozen: 2.013211 ms on SA21 and 1.850602 ms on SA20. Passing controls cannot rescue failed primaries.

## Integrity checks

- All 10,500 raw JSONL observations were audited: 5,250 per cell, consisting of 1,050 warmups and 4,200 measured observations.
- Every coordinate matches the prescribed seven blocks, five workloads, alternating variant order, and 10 warmups followed by 40 measured samples. Sequences are contiguous and sample wall intervals do not overlap.
- Every row has successful status, true ordered-row comparison, exact expected count, and matching oracle hash. Native oracle hashes also match an independent reconstruction of the frozen 1,000-row public fixture.
- Every elapsed wall/RAW/process/thread value equals its recorded end minus start. No negative elapsed value or wall-versus-RAW disagreement above 1 ms was found.
- Independently recalculated block medians, median-of-block-medians, favorable-block counts, ratios, reductions, nearest-rank p95 at rank 266, absolute deltas, and all decision flags exactly equal both stored summaries.
- All 210 batch resource receipts are present in schedule order, and all recorded resource deltas recompute exactly.
- Both cells retain complete metadata, zero exits for all three workers, empty worker stderr, and all three post-teardown closure acknowledgments with exact source-after snapshots. No closure, transport, forced-termination, or receipt-flush failure is present.
- Native driver closure receipts precede gates. Instrumentation-removal receipts are present for every variant. GC remained enabled with thresholds 700/10/10.
- All 208 source hashes match before and after each worker. Native/original use exact S20; candidate changes only the frozen cf1.py. Current source trees also match, with no extra runtime files.
- Full dependency receipts agree across all variants within each cell and with the correctness gate. Installed RECORD hashes match the receipts. Versions are Python 3.12.14, psycopg 3.3.6, cryptography 50.0.2, greenlet 3.5.6, and SQLAlchemy 2.1.3 or 2.0.51 as labeled.
- Both 213-case affected JUnits, the 26-case SA21 and 16-case SA20 supplemental JUnits, and both 55-pass pure receipts match their frozen hashes and admission requirements. Correctness retains 96 equal scenarios per variant and matching protected safe-error outcomes, with clean teardown and source snapshots.
- Both wrapper receipts and JUnits show one clean timing-selector execution. Execution success does not mean performance success.

## Primitive and query-path evidence

All six untimed workload gates per variant match the independently calculated counts. Search/payload derivations, term calls, key resolutions, and text openings retain the frozen values. Only the intended generic tuple assemblies disappear:

| Workload | Original tuple calls | Candidate tuple calls |
|---|---:|---:|
| IN20 miss IDs | 60 | 20 |
| IN20 hot IDs | 60 | 20 |
| IN20 hot text | 1,776 | 1,164 |
| Equality hot text | 861 | 573 |
| Point text | 6 | 4 |
| List20 miss control | 60 | 20 |

Native primitive counts are zero. Every gate records `array_route: false`; the frozen harness asserts no ANY in executed workload SQL. The observed primitive reduction does not satisfy the failed performance admission by itself.

## Resource interpretation

Recorded one-minute load averages range from 0.108 to 0.362 on SA21 and 0.386 to 0.562 on SA20. Context switches are nonzero and vary: summed involuntary switches across all 35 original/candidate batches are 374/1,171 on SA21 and 306/238 on SA20. Candidate process high-water RSS increases by 256 KiB during each run; the metric is a process high-water mark, not live allocation accounting.

These batch counters include all phases and receipt IO. They can describe scheduling and resource activity but cannot establish the cause of a timing difference, certify an interference-free machine, or excuse a threshold miss. No resource observation was used to filter samples or alter decisions.

Wall-minus-RAW ranges are -269,565 to 70,131 ns on SA21 and -297,055 to 88,401 ns on SA20, within the frozen 1 ms anomaly threshold.

## Artifacts

- [audit.json](audit.json): full independently recomputed outcomes, resource summaries, dependency records, and SHA-256 inventory of every audited input.
- [audit_c10.py](audit_c10.py): independent standard-library-only audit implementation.
- Raw SA21 evidence: `../evidence/c10-frozen-timing-raw-sa21-20261014/`.
- Raw SA20 evidence: `../evidence/c10-frozen-timing-raw-sa20-20261014/`.

Reviewed timing harness SHA-256: `81c1fc50eaa8698e94bab5406f2cf10a9822a6b6fc4de2f559a2eed79f4fcf23`.

Reviewed protocol SHA-256: `37e8854cf795b612250f7c18a727a175ac888515b69e2515a86e95f02f665c01`.

Candidate cf1.py SHA-256: `8c6a3ad82865734200424b6ab949ef46c38540561be20b743188073fbf593fb4`.

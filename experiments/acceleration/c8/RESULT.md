# C8 indexed equality/IN attribution

## Result

**VERIFIED only for this unchanged S18 synthetic diagnostic:** SQLAlchemy 2.1.3
passed one test in 5.37 s; 2.0.51 passed one test in 5.34 s. All 1,024 scheduled
application executions and 32 extra typed-NULL/empty-IN controls matched the
independent native PostgreSQL oracle. Both exact schedules were retained.
All 96 protected call-count predictions matched. All 201 inherited files and
both frozen harness/protocol hashes remained unchanged. No product optimization,
performance acceptance gate or new confidentiality claim was tested.

The measured recurring work is real: within one field/tenant/search generation,
search-key derivation occurs once per non-NULL query term and once per returned
non-NULL protected value. Payload key derivation remains independently row-bound.
A separate invocation-scoped search-material proposal is justified for review.
This evidence does not approve a cache or predict its speedup.

## Exact work attribution

For M query terms and R non-NULL projected protected values, every protected
profile had these counts:

| Work | execute() | all() | Total |
|---|---:|---:|---:|
| Search term and its search KDF | M | R | M + R |
| Payload KDF | 0 | R | R |
| All KDF calls | M | 2R | M + 2R |
| PreparedKeys._resolve | 2M | 4R | 2M + 4R |
| open_text / protected result processor | 0 | R | R |
| Attachment admission | 3 | 0 | 3 |

IDs-only results have R=0. Equality-hot has M=1,R=143: 144 term calls, 287 KDF
calls and 574 resolve calls. IN-2-hot has M=2,R=286: 288 terms, 574 KDF calls and
1,148 resolves. IN-20-hot and repeated-IN-20 both have M=20,R=286: 306 terms,
592 KDF calls and 1,184 resolves. No input deduplication occurred. Point reads
have M=0,R=1; they retain two KDF calls and four resolve checks.

Search KDF caller-attributed share of total **instrumented thread CPU**:

| Full text projection | SA 2.1.3 | SA 2.0.51 |
|---|---:|---:|
| Point | 0.461% | 0.507% |
| Equality-hot | 11.631% | 11.481% |
| IN-2-hot | 12.680% | 12.336% |
| IN-20-miss | 6.852% | 7.963% |
| IN-20-hot | 12.929% | 12.445% |
| IN-20 repeated values | 12.896% | 13.105% |

Each percentage is the median of three per-query ratios. It uses only _derive
caller costs from _term divided by total profile CPU across both phases.
Payload KDF costs are separate. Nested inclusive costs are not added together.
The complete exclusive function/caller statistics and disjoint self-time groups
are retained. Search and payload KDF together account for about 23–26% of
instrumented CPU for these matching text projections. Neither is all result cost.

## Descriptive latency observations

The following are medians of ten **per-observation sums of two API-phase wall
measurements**, in milliseconds. They exclude harness work between execute()
and all(), and are not an end-to-end request latency or an optimization trial.
No measurements were dropped or corrected for noise.

| Full text projection | SA21 native | SA21 protected | SA20 native | SA20 protected |
|---|---:|---:|---:|---:|
| Point | 0.266452 | 1.9023985 | 0.2577695 | 1.558848 |
| Equality-hot | 0.5026745 | 6.6849345 | 0.5433595 | 7.5840065 |
| IN-2-hot | 0.7985395 | 11.8833515 | 0.921049 | 13.0620945 |
| IN-20-miss | 0.383669 | 2.3499525 | 0.4388655 | 2.3414245 |
| IN-20-hot | 0.804699 | 12.260602 | 0.999060 | 11.6837815 |
| IN-20 repeated values | 0.855018 | 11.686167 | 0.9389565 | 11.7815615 |

For protected equality-hot, execute()/all() phase wall medians are 2.498926 /
4.2338235 ms (SA21) and 2.845526 / 4.62618 ms (SA20). For IN-2-hot they are
3.2595855 / 8.630907 ms and 3.5465775 / 9.390469 ms. A sum of phase medians is
not necessarily the median of their per-observation sums.

Raw start/end clock fields are nanoseconds. Values inside `elapsed_ms` are
milliseconds despite their nested `_ns` key suffixes. `total_cpu_s` and profile
function/caller times are seconds of instrumented current-thread CPU. The
analysis uses explicit `_ms` names to avoid this historical label ambiguity.
Profiling and its Python timer substantially inflate CPU costs; the CPU numbers
must not be subtracted from wall measurements to predict an optimization gain.
Even the non-cProfile observations retain clock and GC instrumentation overhead.

## Plans, scope and limits

Both cells retain 22 of 32 plans with an index node. The optimizer chose plans
without an index node for both native/protected IN-2-hot and IN-20-hot, and for
protected repeated-IN-20. No index use was forced. This is the admitted indexed
representation, not proof that every query used its index. Plans are estimates,
not EXPLAIN ANALYZE execution measurements.

The fixture has 1,000 rows, one explicitly authorized synthetic tenant, C-collated
text, public IDs and fixed statement objects. One existing public-fixture Keyring
uses its unchanged bounded root cache and all original lease/context checks.
This differs from older factory-per-query fixtures; cross-run speed comparisons
with those experiments are not valid. No cold-provider, expiry, async,
cancellation, thread-safety or production-cost qualification is established here.
The process RSS high-water includes fixture and profiler storage. Full profiles
are intentionally large. No RSS bound or isolated per-query memory claim follows.

C1 and C5 failed gates remain held. C6's published A/A diagnostic does not reverse
them. C7's full-scan correctness and failed cost gates are separate evidence.
All seven full product gates remain UNKNOWN.

## Source and exact recovery

Baseline: 201-file S18 commit 5492cc04ee6c5d6696c9e9fc261f12fa61236043.
Source manifest: aba658622e884084762e09be61aed54c7a1023af37d332af9f5143aa5e358688.
Harness: 7d598b58cceddadb1dab8c472f712d00a2a24c9b8b3b00fb5c7a2caccced164f.
Protocol: 53f8faec2db1bb004af06592dd7973c1e4c3b14806f1a75a460009d137384b25.

Two complete JSON receipts total 80,929,174 bytes. Standard XZ compression plus
four bounded binary parts preserves every original byte, including all 384
profile phases, 640 timed observations, 192 warmups, 192 profiled observations,
GC events, resource snapshots, safe plans and native controls. No raw observation
was omitted from the publication bundle. SHA-256 verification and reconstruction
of both exact originals passed locally. The four parts total 2,346,796 bytes.

Restore with the standalone stdlib-only `analyze_and_restore.py --parts-dir
./evidence --restore-dir ./restored`. It verifies fixed part hashes, segment
lengths and each restored original SHA-256 before writing with exclusive create.
Then use `--input-dir ./restored --output ./analysis-recomputed.json` to reproduce
the machine-readable analysis. Neither action connects to a database or imports
Cryptalis. The analysis JSON contains source bindings, part hashes, all exact
phase summaries and count checks. Original raw hashes:

- SA21: 73727793b304a39e21c9b927f1d42d443a9f12ca43732850176043004e1c0c9b.
- SA20: a2affd3a0a7fa90df56a304ca10de03a30caa51b3c5adb963455ae37db407e29.

To reconstruct the runnable experiment, materialize the exact S18 source first,
place the harness at `tests/test_indexed_cost_profile.py`, and place protocol and
manifest at their original `experiments/INDEXED_PROFILE_*` paths. This archival
layout is not a product runtime replacement. Existing DB runs must not be repeated
merely to improve timings or change held gate outcomes.

## Safe original test receipts

Only the two connection fingerprints on each preflight line are omitted below.
No environment dump, credentials, SQL, bind values or provider material is copied.

### sa21

Original tests.log SHA-256: ce3a25dcb3e2f188338ba9f967b78c4ea70cf44600761d1fdeec3fe915908cd8.

```text
PostgreSQL preflight passed [connection fingerprints omitted]
.                                                                        [100%]
1 passed in 5.37s
```

JUnit original SHA-256: f823e9ae9daef2426f4cbb2a61d58ceceff39a2a0550d8aa6678090f579fd65e; one passing node `tests.test_indexed_cost_profile::test_indexed_equality_in_cost_attribution`.

### sa20

Original tests.log SHA-256: 08cdbd9096e4aa5d10d71f64ff6383e8cfb31c23943d1001f39a94c5eae83beb.

```text
PostgreSQL preflight passed [connection fingerprints omitted]
.                                                                        [100%]
1 passed in 5.34s
```

JUnit original SHA-256: 64472035253df8012d08757c340232843dd46865c4daf1f0f88ad509767792f8; one passing node `tests.test_indexed_cost_profile::test_indexed_equality_in_cost_attribution`.

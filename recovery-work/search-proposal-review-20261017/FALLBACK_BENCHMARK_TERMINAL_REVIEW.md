# Second benchmark independent terminal review

Disposition: ACCEPT EXPERIMENT INTEGRITY; PERFORMANCE SCREEN HOLD. Candidate remains unpromoted. No rerun, sample exclusion or gate change.

Packet fallback-order-benchmark-v1 SOURCE d176ed1773d01d731dca7c8406a04ed552e692ba6ae159ae36c962a57a7daeec. Capture root persistence-recovery-20261013/search-fallback-order-benchmark-20261017. Manifest SHA2566009d67980d89db5e264c4b812b7d922e38a577d1a0871c6915fc449e3b21d9f. Reducer stdout SHA256594b05d9d01060386745c9a1141242eaa3726a3249898dd2e19aa8ba92af2b85.

## Integrity

Independently parsed all16 captures: exact index/variant ABBA*4 schedule; eight complete samples in each fixed pair-specific cell order;4096 timed calls and verified outputs plus128 warmups per sample. Total128 samples,524288 timed calls,16384 warmups. Every child has statusPASS, no primary failure, exact448 selected43-source/399-dependency/six-control closure keys allPASS and absent bytecode prefix. All16 root/after exits0; stderr empty. All before/after control metadata are identical; every packet-after matches common successful packet-before hashes. All64 manifest-bound capture hashes verify. No samples were omitted or retried.

Each invocation records exact selected index, variant and new source seal, isolated Python/cold-prefix flags, absolute cwd, clean environment and stdin/dev/null. CPU30/VM1048576KiB/file512KiB/core0 readbacks exist for all16. Two output files each limited512KiB imply1MiB aggregate without an active aggregate monitor. Whole schedule35 seconds, exit0. Quiet-window attestation covers paused owned workers only, explicitly not a globally exclusive host.

Reducer exit1 carries complete HOLD JSON, empty stderr and after-exit0. Manifest/packet before-after records match. Reducer readback exists this time: CPU20/VM524288KiB/file512KiB/core0; invocation records wall60 and exact manifest pin. Sampling and reducer pycache prefixes are absent at review time. Successful integrity does not change the screen disposition.

## Independent calculation

Data-only recomputation from raw samples exactly matches reducer median ratios and its ordered28 flags. Full independent rows/counts/flags are retained in FALLBACK_BENCHMARK_RECOMPUTED.json.

Canonical wall/CPU median ratios and counts strictly below1:

- storage16:0.914004/0.913483;7/8 wall,8/8 CPU.
- storage1024:0.926631/0.924139;6/8 wall,7/8 CPU. Wall consistency fails.
- equality16:0.943036/0.934596;8/8 both.
- equality1024:0.973458/0.958881;5/8 wall,6/8 CPU. Both consistency checks fail.

Uppercase wall/CPU median ratios:

- storage16:1.033142/1.040794. Both exceed the fixed1.03 ceiling.
- storage1024:0.990380/1.008948.
- equality16:1.021035/1.027878.
- equality1024:1.026853/1.024916.

Each uppercase metric has7/8 pairs at most1.10, so fallback pair-count gates pass; the two fallback failures are specifically storage16 median ceilings. There are three canonical consistency flags and23 scheduling_or_major_fault flags, totaling28. All23 scheduling-category flags are involuntary-switch counts greater than2; major faults total0, maximum involuntary switches8. Do not describe these as23 major-fault samples. Minimum wall sample54,170,452ns exceeds50ms. No short-sample, wall/CPU-gap, dispersion or maxRSS flag occurs. Median paired process high-water RSS difference is−96KiB in all cells, not a current cell-local memory measurement.

All noisy samples remain included. Favorable canonical medians cannot override consistency, noise or fallback failures. The changed predicate has not established the required performance envelope.

## Interpretation and preservation

The comparison is successor versus original baseline, not a contemporaneous predecessor-candidate versus successor comparison. Cross-experiment median differences cannot isolate the reorder from time/host variation. Original benchmark V2's128 samples and24-flag HOLD remain preserved separately; this second experiment retains its own128 samples and28-flag HOLD. Correctness acceptance remains separate and does not authorize promotion.

Workload/gates/limits are the previously reviewed unchanged ones. Measurements concern warmed repeated real-CF1 result processing with synthetic pre-admitted keys and loop/append overhead. Construction/cache initialization, setup encryption, admission/imports and validation are outside timing. No tiny-resultset/end-to-end, DB/service, production, provider-custody, SA20 or significance claim follows. Existing-host stdlib/native-loader trust remains assumed; no vendor/native provenance, complete loaded-origin inventory or hostile-code sandbox is established.

Reviewer used reads, hashes, comparisons and JSON-data arithmetic only. No target execution, rerun or threshold/sample changes.

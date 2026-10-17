# Benchmark V2 terminal review

Disposition: ACCEPT CAPTURED EXPERIMENT INTEGRITY; PERFORMANCE SCREEN HOLD. Candidate remains unpromoted. No rerun, trimming or threshold change is justified by this review.

Source seal402f4c7aec63b1aec00840eea25255ec21ca56fdc95a153d814f50ff3e8289c8. Capture root persistence-recovery-20261013/search-new-sa21-benchmark-20261017. Capture manifest SHA25680745087d0d048a5d02b02269dab67fb8955d6b2f162228e9273b994acad75c5. Reducer stdout.json SHA256d2e04735e4594eeff87330766795181e61db5b95c1ed14ed54eb23078121eed9.

## Integrity and counts

Independently parsed all16 raw BENCHMARK_JSON records: exact ABBA*4 index/variant sequence; eight samples in each prescribed pair-specific order; each sample COMPLETE with4096 calls and4096 verified outputs plus128 warmups. Total128 samples,524288 timed calls and16384 warmups. No primary failures; every child statusPASS, bytecode absencePASS and exact448-member selected source/dependency/control closure entirelyPASS. All16 exit/after-exit receipts are0 and stderr empty. Control-before/after metadata compare identical; every packet-after equals the common packet-before successful hash ledger. All64 capture-manifest member hashes verify.

Each invocation records selected entry/index/variant, cwd, clean environment and stdin, timeout60s+2s grace and Python isolation/pycache flags. Every readback records CPU30s, VM1048576 KiB, per-file512 KiB and core0. Two capture files imply the chosen combined1 MiB bound, without an active aggregate monitor. Whole schedule completed34 seconds, schedule exit0. Quiet-window attestation limits itself to paused owned work and does not claim a globally dedicated host. Before/after resource snapshots do not eliminate scheduler interference.

Reducer exit1 is the expected screen-HOLD outcome, not a crash; after-exit0, empty stderr, complete11761-byte JSON. Reducer packet and manifest before/after records compare identical; its prefix is absent. INVOCATION records reducer wall60/CPU20/VM524288 KiB/file512 KiB/core0; no separate ulimit-readback file was supplied for the reducer, so this review distinguishes the recorded invocation from independently read-back enforcement. Sampling readbacks are present for all16 processes.

## Independent arithmetic and gates

Recomputed paired median wall/CPU ratios and every flag directly from raw samples using data-only arithmetic, without importing/running the reducer. Results exactly match reducer rows and ordered24-flag list. BENCHMARK_RECOMPUTED.json preserves that independent calculation.

Canonical cells, wall/CPU median ratios and favorable pair counts (<1):

- storage16:0.901023/0.883024;7/8 wall and6/8 CPU. CPU consistency fails.
- storage1024:0.920866/0.927626;8/8 wall and7/8 CPU.
- equality16:0.927663/0.935384;7/8 each.
- equality1024:0.975988/0.968764;6/8 each. Both consistency checks fail.

Uppercase fallback cells, wall/CPU median ratios and pair counts at most1.10:

- storage16:1.009551/1.035918;6/8 each. Both pair-count checks fail; CPU also exceeds1.03 median ceiling.
- storage1024:0.987869/0.999517;7/8 each.
- equality16:1.003512/1.010036;6/8 wall and7/8 CPU. Wall pair count fails.
- equality1024:0.990132/0.999319;6/8 each. Both pair counts fail.

There are16 scheduling_or_major_fault flags, all caused by more than2 involuntary context switches. Major faults total0; maximum involuntary switches6. The category label must not be summarized as16 major-fault samples. Minimum wall sample53,913,315ns exceeds50ms. No short-sample, wall/CPU-gap or dispersion flag fired. Median paired process-maxRSS difference is72 KiB in every cell, below8192 KiB; it remains a process high-water comparison, not current per-cell memory.

The other8 flags are3 canonical-benefit consistency failures and5 fallback-regression screen failures. All128 samples remain included, including the16 noisy samples. Favorable medians cannot override these prospectively fixed gates. This experiment does not establish an accepted speedup or safe fallback performance envelope.

## Interpretation

Correctness results remain accepted separately. This timing experiment measures warmed repeated real-CF1 result processing with synthetic pre-admitted keys, including Python loop/append costs. It excludes constructor/cache initialization, encryption/setup, admission/imports and output validation. It says nothing about tiny-resultset or end-to-end benefits, provider custody, DB/service latency, SA20 or production. Existing-host stdlib/native-loader trust remains assumed; no vendor/native provenance, complete loaded-origin inventory or hostile-native containment is established. Thresholds were exploratory screens, not significance tests.

Review performed capture reads, hashes, comparisons and JSON arithmetic only. No target execution or rerun occurred.

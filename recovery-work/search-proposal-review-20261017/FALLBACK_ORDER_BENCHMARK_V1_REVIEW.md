# Fallback-order benchmark binding independent review

Disposition: ACCEPT SOURCE ONLY for one separately admitted prospective comparison. Root retains execution selection; no new performance evidence exists.

Packet recovery-work/search-next-slice-20261017/fallback-order-benchmark-v1; SOURCE seal d176ed1773d01d731dca7c8406a04ed552e692ba6ae159ae36c962a57a7daeec, all93 members verified. Benchmark58410799880858721a463bc51954e62e33cd62fd408ae1e8408b653c8b76d68d; reducer9a707390488f7d398f9cb98543d39711c4db79688560d291e2c58e67108d491b.

Full packet comparison against benchmark-v2 confirms six changed members plus SOURCE seal: benchmark ROOT only; reducer ROOT and new capture root only; VIEWS root/candidate binding; candidate's reviewed one-line predicate order; PLAN; correctness evidence binding. Remaining source views, dependencies and WORKLOAD bytes are identical. WORKLOAD SHA256c518ceb007b13587dc429bcf892da848d19a03ebbb45557eaa8e227dcca75119. Candidate file is byte-identical to the candidate-only correctness-tested successor5ec115163c8c53ba01c34613a9140b4506cd3a38a8280224ea9c21f032743f6a. Its accepted terminal review2704c87b5d4d182b7a4f650360c893755c58058b513d7d2300142a7842eedde0 is correctly identified.

No workload, counts, noise filters, consistency thresholds, memory screen or resource/deadline retuning is introduced. Existing flags-first audit ordering is retained. Fixed16 processes/128 samples/524288 timed calls and all source-review prerequisites remain as in BENCHMARK_V2_REVIEW.md, including quiet-window attestation, fresh source/tool admission, exact invocation/resource readbacks, unconditional external afterchecks, preservation of partial/failing captures,240-second schedule ceiling and no automatic retries.

The comparison is successor versus unchanged original baseline. It cannot causally isolate the conjunct reorder against the predecessor candidate because those candidates are not compared contemporaneously. Cross-experiment median differences cannot remove time/host variation. The proposal says this explicitly, preserves original128 samples and24-flag HOLD and does not claim successor mutation qualification from historical controls.

Interpretation stays bounded to warmed repeated real-CF1 processing with synthetic pre-admitted keys, including loop/append overhead and excluding construction/cache initialization, setup encryption, imports/admission and output validation. No tiny-resultset/end-to-end benefit, significance, vendor/native provenance, complete loaded-origin ledger, DB/service qualification or promotion is implied. All noisy samples must remain; any preset failure is HOLD regardless of favorable medians.

No source correction required. Reviewer performed reads, hash checks and full diffs only; no imports, syntax checking, tests, benchmarks or packet edits.

# C5 SA2.0 distribution diagnosis

**Disposition remains HELD.** The declared IN2 median threshold passed, but
consistency was7/9 versus required8/9. This is insufficient consistency, not an
overall median slowdown. All pairs remain in the decision.

The two unfavorable pairs were:

- Block2, baseline first:109.005→110.209 microseconds/admission,1.10% slower.
- Block7, candidate first:105.731→137.151 microseconds/admission,29.72% slower.

The losses occur under both variant orders. Baseline-first pairs are4/5
favorable; candidate-first pairs3/4. Nine pairs cannot identify an order effect.
Across all pairs, median latency improves16.76%; mean latency109.729→92.861us
also improves. Those alternative summaries do not override the declared gate.

The block7 candidate IN2 cell takes about15.71ms more wall time over500 calls.
Immediately before it, the equality baseline cell was also unusually slow:
165.252us versus its116.270us overall median. This is compatible with transient
interference spanning adjacent cells of different variants, but does not prove
scheduling, garbage collection or any other cause. The unchanged-work public
label control also has materially variable paired wall times. Its aggregate
median regresses3.35%, while its mean improves; retain the predefined estimator.

The pure timing receipt contains one wall-clock average per500-call cell, not
per-call samples. It contains no simultaneous CPU/raw-clock/GC/scheduler or
native-database measurement. Separate cProfile counts establish eliminated work
but cannot explain the two timed losses. No timer fault is established, and no
noise subtraction, outlier removal or retrospective normalization is justified.

## Potential next independent experiment, not executed

An A/A measurement negative control would answer whether this harness produces
similar paired asymmetry when both slots execute exactly the same S17 admission
function. Predeclare one nine-block sweep with the same fixed families and
500-call cells; record wall, raw monotonic, process/thread CPU and GC event times.
Do not disable GC or change system settings. Report every pair, clock
disagreement and wall-only/GC overlap; do not select an optimized winner.

This question tests measurement validity, not C5 speed. It cannot convert C5 to
PASS, justify lowering its threshold or authorize repeating its failed gate.
Coordinator approval is pending. No further timing or DB run occurred.

Exact numeric analysis and all pair values are in
`evidence/sa20-distribution-analysis.json`; original raw receipts remain unchanged.

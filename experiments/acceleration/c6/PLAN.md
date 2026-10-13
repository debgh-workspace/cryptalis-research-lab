# C6 A/A diagnostic — predeclared before execution

Question: can identical unchanged S17 admission work show paired wall-time
variation material relative to the C5 ten-percent threshold on SQLAlchemy2.0.51?
This is not a C5 rerun, optimized-code comparison or speed certification.

Execute exactly one pure sweep on SA2.0.51, no DB. Same baseline method, owner and
fixed statement per family occupy both A and B slots. Families are point,
equality,IN2,public textual label, in that order. Nine blocks alternate A/B then
B/A. Thirty warmups per cell precede500 timed calls in ten50-call sub-batches.
Retain every cell/sub-batch, including all warmup GC events. No exclusions,
retries, forced collections, GC disablement or system-setting changes.

Record perf_counter_ns, CLOCK_MONOTONIC_RAW, process_time_ns,thread_time_ns at
cell/sub-batch boundaries; GC callback start/stop markers and generation/counts;
completed calls; and separate untimed cProfile call counts. Record clock
implementations/resolutions. GC callback telemetry introduces instrumentation
cost; it is symmetric diagnostic work and must not be sold as native latency.

Predeclared interpretation:
- Any A/B pair with >=10% absolute wall-average difference demonstrates material
  paired variance in this diagnostic. Otherwise it is NOT DEMONSTRATED here.
- Report median differences, sign counts and every outlier as observations only.
- Mark a gap wall-dominant only when its magnitude is >=1ms/cell and the matching
  absolute thread-CPU gap is <=25% of it. This is compatible with lost CPU time,
  not proof of scheduler causation.
- Report GC overlap durations without subtracting them or claiming causality.
- Flag cell perf/raw elapsed disagreement only when both >0.05ms and >1%; clock
  read ordering/telemetry overhead still require interpretation.
- Any completion/count/outcome mismatch or resource exception invalidates the
  diagnostic; stop and preserve it. Neither result changes C5's failed gate.

# C5 predeclared experiment: reference-free admission work

Baseline: exact 195-file S17 manifest 70a5293e76486f243305968c7a58b8fa8c6be97d5bec5508593529b9eacc49e7;
sqlalchemy.py fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe.
C1 stays held. This asks a different, point-read/admission question and changes
no CF1 derivation, key cache, equality leakage, result processor or SQL cache.

Hypothesis: the C4 local textual-reference walk repeats traversal on ordinary
point/equality/IN statements containing no textual reference. The existing first
admission traversal can record whether any such node exists. With none present,
retain the explicit direct ORDER/GROUP lineage checks but omit the otherwise
empty textual-namespace walk. With a textual node anywhere, keep the complete
C4 local-scope resolver. Each safety boundary still runs admission afresh.

No runtime edit yet. The pure probe builds an in-memory counterfactual from the
exact pinned admission method. It is diagnostic code, not a product correction.

## First finite gate, before timing

- Exact baseline/candidate acceptance or typed-refusal outcomes on the existing
  C2/E query families, nested scopes, native public shadows and direct protected
  ordering. No new expression admission.
- For point/equality/IN without textual names, local textual-helper calls fall
  from one to zero per admission; original admission calls remain one. With
  textual names, the helper remains enabled. No cross-call cache or key work.
- Nine alternating paired blocks, 500 timed admissions per cell, after 30 warmup
  calls per cell. Fixed statement objects; primary families point, equality,
  IN2. Require >=10% median admission reduction AND >=8/9 favorable pairs for
  each primary family on both pinned SQLAlchemy versions. Public-label control
  median may regress no more than5%. Failed gates remain failed; no reruns to
  seek a green result. Instrumented call counts are separate from timings.
- Eight-thread outcome controls use separate owners and shared fixed statements;
  cancellation controls check before/after the synchronous call. The proposed
  flag is an invocation-local bool; no object, session or ContextVar stores it.
  Concurrent in-place mutation of SQLAlchemy expression internals is outside
  this finite immutable/generative-AST proof and must not be claimed qualified.

## Coordinator-only PostgreSQL question, only if first gate passes

Use distinct synthetic 1000-row native and retained fixtures with the existing
role preflights. Verify every returned tuple against both native SQLAlchemy and
independent native driver queries; include NULL/Unicode/duplicate values and
public-label controls. Preserve all284 C4 native/refusal cases and existing
thread/cancellation/loader guards before considering promotion.

One fixed nine-block paired experiment per dependency cell, baseline/candidate
alternation,20 warmups and40 measured reads per variant/family. Measure native
point/equality/IN before and after each baseline/candidate pair to expose drift;
record wall/process CPU clocks and all raw observations. Primary end-to-end
point gate: >=5% median reduction and>=8/9 favorable pairs in both cells.
Equality/IN and public-label medians may regress no more than5%; every native
value check must pass. Any native bracket median drift above20% makes the
performance result INCONCLUSIVE, not PASS, with no automatic retry. Keep exact
native timings visible; no subtraction-based causal attribution.

Stop on a semantic/safety failure or a failed first gate. A new experiment needs
a new falsifiable question, not a lowered threshold. No production latency,
privacy or novelty claim follows from these same-host synthetic results.

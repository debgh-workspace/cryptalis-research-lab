# C5 reference-free admission investigation

## Result: first finite speed gate failed; no runtime change

The source/call-count hypothesis is supported: ordinary point/equality/IN
statements pay for a full local textual-reference walk even when no textual
reference exists. The experiment removes that redundant walk with a local
presence flag collected during the existing first admission traversal. It
retains fresh admission at every boundary, direct ORDER/GROUP lineage checks
and the full resolver whenever a textual reference exists anywhere.

This is an in-memory counterfactual only. All195 S17 baseline files remain
byte-identical to manifest70a5293e76486f243305968c7a58b8fa8c6be97d5bec5508593529b9eacc49e7.
Baseline sqlalchemy.py isfc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe.
No CF1, key lease, cache, nonce, wire format, leakage or runtime source changed.

## Predeclared experiment

`experiments/ADMISSION_EXPERIMENT.md` was written before timing. The first gate
required at least10% median admission reduction and8/9 favorable paired blocks
for point/equality/IN2 on both dependency cells. Public-label regression could
not exceed5%. Each block timed500 admissions per cell after30 warmups.
Instrumented call counts were measured separately.

`experiments/probe_admission.py` derives its counterfactual only from the exact
SHA-pinned baseline method. It neither creates an engine nor queries PostgreSQL.
The independent native execution baseline is specified for a later coordinator
experiment using distinct synthetic native/protected fixtures and both native
SQLAlchemy and direct psycopg results. That dependent experiment is NOT RUN or
queued because the first gate failed. Historical S9 native timings are not
claimed as S17 end-to-end evidence.

## Evidence

- Each100 reference-free admissions: textual helper100→0 calls; admission100→100;
  equality/IN search-shape checks200→200. Named public-label controls retain
  all100 textual-helper calls. One repeated identical ordering-lineage check
  per call also disappears; the actual clause still receives its check.
- SA2.1.3: point30.14%, equality24.69%, IN2 12.94% median admission reductions;
  each9/9 favorable. Public-label reduction6.27%. Declared pure speed gate PASS.
- SA2.0.51: point23.57% and equality28.15%, each9/9 favorable; IN2 16.76% but
  only7/9 favorable, below8/9. Public-label regression3.35%. Declared pure speed
  gate FAIL. Raw unfavorable blocks remain in the receipt. No rerun or threshold
  change is authorized by this result.
- Baseline/counterfactual outcomes agree on60 SA2.1 and50 SA2.0 bounded cases,
  including E's clause builders, public alias precedence and nested SELECTs.
- Per cell,1024 checks across8threads with separate owners/shared fixed statements
  preserve outcomes. Cancellation probes cover requests before admission and
  unchanged owner state after synchronous calls. They do not inject cancellation
  during a synchronous call or establish the planned after-call cancellation
  boundary. That remaining safety qualification is not labelled PASS.

Receipts: `evidence/admission-pure-sa21.json` and
`evidence/admission-pure-sa20.json`. They retain all9 raw block observations,
call counts and the independently calculated gate outcomes.

## Limits and disposition

The flag would be invocation-local, with no session/owner/ContextVar state,
cross-call memoization or asynchronous suspension. The finite controls assume
ordinary immutable/generative SQLAlchemy expression trees. Concurrent mutation
of expression internals or dynamic custom traversal is not qualified. Existing
three-stage admission and all lifecycle checks would remain required.

These pure timings do not establish database latency, native execution results,
production performance or a security improvement. C5 stops at the failed first
gate. C1 remains separately held for its original failed SA2.0 consistency gate.
No candidate is proposed for promotion; all seven production gates remain UNKNOWN.

# Correction slice results

2026-10-14. The 43 new finite observations PASS at Python optimization flags 0 and 1. Both actual-returned-text negative controls refuse exactly as intended. Full DESIGN correctness admission and all timing remain HOLD.

## What was executed

Only this correction's four new cells were run: positive and expected-failure negative at O0/O1. The old 1,182/1,246 suites were not rerun. No native binary was rebuilt, and no product code, dependency, original prototype file, database, Git state, or key-provider service was changed. The original normal native binary and separately named Python wrapper were reused after hash/origin/version checks.

Exact new positive/refusal coverage:
- 8 table-derived descriptor relocations with recomputed descriptor digests. Single-tenant cases change expected tenant together with table so they reach authentication refusal.
- 16 policy-domain mismatches, valid and malformed frame, across all eight representation/record/tenant modes; no native or material-resolution calls occur.
- 6 true A/B/A reads across different tenant AND record IDs, both representations; second A reuses its first PreparedKeys. 2 NULL cases verify one active payload resolution and zero native helper calls.
- 6 same-object lifecycle observations: valid read, controlled expiry with the same PreparedKeys/frame, then success with newly constructed public PreparedKeys, both representations.
- 3 selected-material expiries immediately after successful strict decode and before final resolution: storage payload, equality payload and equality search.
- 2 simulated PID changes after native return, one per representation, refusing at final payload resolution.

Every case compares exact returned text/type or all safe failure fields (class, code, stage, retryable, effects, remedy and operation-ID presence), exact ordered resolution arguments, and helper-call counts. The 43 IDs and exact expected records were frozen before candidate import. Positive O0/O1 observed records are byte-equivalent after JSON decoding, including traces and counts.

The actual-output negative starts by reading through the real candidate and checking its full unmodified observation exactly. It copies that actual returned observation and appends a fixed marker to its text value before the same downstream comparator. Each mode records exactly one native helper call, original_verified=true and perturbation_applied_to_actual_return=true; exits with code 1 and RuntimeError('Mismatch: actual-output-perturbation'); and records zero passed checks. `run_new.py` rejects any other failure cause. This is a downstream actual-return perturbation, not a native binary or product-return-channel mutation. The original weaker literal comparator controls remain unchanged and correctly limited.

## Provenance and review

`static-review/ORACLE-REVIEW.md` independently reviewed the correction oracle source before execution and found no certain blocker in this bounded scope. It did not execute the candidate or inspect later runtime results. The outer runner and data-only `audit_receipts.py` enforce the exact negative-failure gate and positive record correspondence; these are self-checks, not independent execution attestation. Root owns independent result review and publication.

Preparation verified the original 130-file inventory and original build/dependency pins, constructed only new baseline fixtures/expected records, then wrote a 628-entry PINS.json before importing native code. The manifest includes exact UTF-8/text values and fixture hashes. Final data-only integrity verifies all 628 pins and all 130 original artifacts remain unchanged. The existing pinned virtual-environment executable path was used without symlink resolution: Python 3.12.14 / cryptography 50.0.2 / oracle OpenSSL 4.0.3, versus native system OpenSSL 3.5.7. No timings were collected.

- cases.json SHA-256: 25e1252cbee9bd2e350aca536e8f0622049050610462c022e00edf5c9547afdb
- PINS.json SHA-256: 4211076650a56db951155113e7b4dfa94d6dcc84d602fa0ba126065d530daed8
- Original ARTIFACTS.json remains: bd6fba6d773ca746ae8ac0bc4ecc0f539f95fcf244b488b3bd6bc9e191ea81a8

Receipts are under evidence/: freeze-01.json, positive-o0/o1-01.json, negative-o0/o1-01.json, the four launch receipts, run-summary-01.json, and integrity-01.json. No failed positive build/check needed repair in this slice; the two negative process failures are expected retained evidence.

## Remaining holds

This closes only the named correction gaps. It does not retrofit the original suite's length/hash expectations into exact text checks, enumerate all original supplementary IDs before their past execution, repair class-only original fault adapters, add primitive or intermediate-value diagnostics, measure native allocator/leak balance, or prove all native failure paths. Cross-scope concurrency remains untested here; A/B/A is sequential. Native invocation counting surrounds the original research helper, not an independent C-internal counter. Expiry and PID controls are explicit synthetic state changes; post-decode expiry uses a research-only bytes subclass at the helper boundary. No provider custody, asynchronous cancellation, memory erasure or production platform qualification follows.

Setup/AAD versus data/final classification remains an observable stage policy with operational-cause ambiguity. Omitted pyca unused-encrypt/copy paths, allocation ordering and the different native backend still preclude full fault equivalence. Timing and product/backend admission remain held for root review and any additional required qualification.

# Static review: public mark observation supplement

Date: 2026-10-14. Disposition: bounded source-review clearance, contingent on the coordinator's separately authorized, isolated, timeout-bounded launch plan. No runtime pass/fail prediction and no general mark-preservation certification.

Reviewed candidate-native-mark-observation-20261014: native_cf1.c, run.py, build.py, prepare.py, cases.json, SCOPE.md and PINS.json. Read-only shell inspection, jq projection and SHA-256 verification only; no candidate preparation/build/import/execution/test, network, PG, Git or provider/settings changes. Only this review directory was written.

## Findings

- All recorded PINS.json hashes matched the current files. The candidate native source hash is f7de1d58667062c867a31d4ba0bd2fc2d0e8fccd91e1763b6acbb1ac95b19411; manifest b70cfd9895309386bc8c5968987a003af893a0d0fd750f83ec0f40c955e6ceac; runner 2129bee56241b8ca0972a3fb9cce69289554be3b6228c09fde4e0823b67b66ec.
- Manifest has 60 unique IDs: each of four configurations has three controls (baseline, consume-one, add-one) and twelve helper recipes. Totals are four positive baselines, eight negative controls and 48 helper observations. Baselines use kind=control and variant=baseline, so they intentionally do neither mutation nor helper invocation. An initial reviewer branch concern was withdrawn after checking this actual encoding.
- Public declarations for ERR_set_mark, ERR_pop_to_mark and ERR_count_to_mark are present in pinned /usr/include/openssl/err.h. No ERR_STATE fields, private symbols or direct hidden mark introspection are used. Counter semantics are the coordinator's previously inspected OpenSSL 3.5.7 primary-source premise, as recorded in SCOPE.md; this no-network review did not independently retrieve that implementation.
- Direct C-source diff against the preceding pinned unmarked observation supplement shows only four public fixture functions and their method registrations added. The underlying helper, diagnostic selectors, ordinary queue cleanup, output/error handling and inherited observation functions are unchanged.
- All cases use exact byte output or exact RuntimeError type/arguments for their inherited helper recipe, rather than interpreting errors as causal classifications.

## Independent operation walk

Let A and B be the two seed entries. Each probe appends C, counts entries above the nearest mark (or all queued entries if none), consumes one mark by popping, then inspects endpoints. A successful pop retains its marked entry and decrements its per-entry mark count. With no mark, pop returns zero and empties the queue.

Preserved traces, expressed as distance/pop/remaining sequence:
- B once: 1/1/AB; 3/0/empty.
- B twice: 1/1/AB; 1/1/AB; 3/0/empty.
- A once: 2/1/A; 2/0/empty.
- A and B: 1/1/AB; 2/1/A; 2/0/empty.

After consume-one, the exact traces are respectively:
- B once: 3/0/empty; 1/0/empty.
- B twice: 1/1/AB; 3/0/empty; 1/0/empty.
- A once: initial A; 2/0/empty; 1/0/empty.
- A and B: 2/1/A; 2/0/empty; 1/0/empty.
All consume-control final drains are empty.

After add-one, the exact traces are respectively:
- B once: 1/1/AB twice; final drain AB.
- B twice: 1/1/AB three times; final drain AB.
- A once: 1/1/AB; 2/1/A; final drain A.
- A and B: 1/1/AB twice; 2/1/A; final drain A.

These independent walks agree with every frozen control oracle inspected. Per-configuration preservation oracles are identical across all fifteen cases. Endpoint encoding deliberately repeats A for the single-entry queue; it is not a full queue snapshot. Negative controls must both differ from the preserved oracle and exactly equal their declared mutated oracle; an unrelated failure does not count as sensitivity evidence.

## Ownership, cleanup and bounds

Setup refuses a nonempty queue and seeds at most two entries. All setup, helper invocation and observations are synchronous native calls on the same Python thread with no GIL release introduced. Only public test data is installed. At most three test-created entries exist simultaneously (A, B, C); added marks do not add queue entries. No overflow, near-capacity or resource-exhaustion stimulus is introduced. Native/provider internal entries are explicitly outside this test-created-entry bound.

Probe count is frozen at two or three steps; it is not an exhaustion-seeking mark loop. The inherited final ERR_get_error_all drain runs until the finite thread queue is empty and records entries. Normal completed cases drain before the next seed; a failed assertion terminates the standalone runner, so it must not be embedded into an unrelated application's caller thread. No finally-based recovery is promised after a failing case. Existing helper cleanup remains intact.

Build uses a new directory, one -O2 CF1_DIAGNOSTIC artifact, pinned inputs, interpreter/version/optimization checks and an exclusive build receipt. Runner rechecks input/build pins, module origin, OpenSSL version and Python modes 0/1, and creates mode-specific exclusive receipts. Binary/dependency hashes are recorded at build. No normal-binary run is proposed.

Execution condition: the coordinator must supply the documented outer 60-second deadlines around the isolated build and each of the two mode launches. run.py does not implement its own wall-clock timeout, and build.py's compiler timeout does not bound its later ldd/version subprocesses. Do not rerun prepare.py or silently change the frozen candidate. Static clearance is not authorization to broaden the matrix, modify providers or draw arbitrary-depth/concurrency/allocation-failure conclusions.

The earlier categorical mark-loss claim remains unsupported. This design can supply bounded semantic evidence only after an independently authorized run and examination of its exact receipts.

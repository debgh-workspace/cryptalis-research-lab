# Preexisting mark semantic observations

2026-10-14. Bounded diagnostic result; independent postrun data audit pending at authoring. No timing/product/classifier approval.

## Outcomes

The frozen diagnostic-only build succeeded without compiler diagnostics. Python optimization modes 0 and 1 each passed all 60 ordered cases, exited 0 and produced empty stderr. Both modes use the same C -O2 binary. External 60-second deadlines and owned-process-group timeout cleanup were configured and recorded; no timeout, failure, retry or outcome-driven oracle change occurred. Preparation was not rerun.

Per mode:
- Four positive no-helper baselines matched the exact public-operation traces.
- Eight active negative controls matched their separately frozen altered traces and differed from the preservation oracle: one deliberately consumed mark and one extra mark for each configuration.
- Forty-eight helper observations matched exact preserved mark semantics: four mark configurations times twelve existing public-fixture action/representation combinations. Eight helper successes returned exact frozen encoded bytes; forty refusals matched exact private RuntimeError arguments.

The configurations were a mark on top sentinel B, two marks on B, a lower mark on A with unmarked B above it, and a mark on both A and B. These finite observations support preservation of those preexisting marks across the copied helper's selected successes and refusals on this pinned backend. They supply runtime evidence beyond the earlier source-only correction; they do not prove arbitrary queue preservation.

## What was actually observed

The test used only supported public ERR_set_mark, ERR_count_to_mark, ERR_pop_to_mark, ERR_new, ERR_set_debug, ERR_set_error, peek and drain interfaces. After helper return it appended public sentinel C, recorded distance to the nearest mark, consumed that mark, and recorded remaining queue endpoints. A fixed two/three-step sequence and final drain distinguished retained, lost and extra marks. A successful preservation case ended with a no-mark pop returning 0 and an empty drain.

The test is intentionally destructive on its own disposable queue after helper return. It does not read hidden per-entry mark counters. Oldest/newest records are explicitly endpoints, with duplicates for a one-entry queue; they are not misrepresented as a complete non-destructive queue snapshot. The exact full traces are in results-O0.json/results-O1.json and their independently prescribed expectations in cases.json.

At most two test sentinel entries preexisted and at most three test-created entries were present simultaneously during probing. Positive cases used at most two preexisting marks; the extra-mark control reached three. This bounds test-created entries, not arbitrary native/internal errors. No queue exhaustion, near-capacity test, resource exhaustion, provider change or unexpected internal fault was induced.

## Provenance and limits

Runtime backend: OpenSSL 3.5.7 9 Jun 2026.
Diagnostic binary SHA256: 289226d2c3cd4b8ae6316b5457f8dcdd2be04c92bf45bc3934af90e00d0c6528.
Frozen manifest SHA256: b70cfd9895309386bc8c5968987a003af893a0d0fd750f83ec0f40c955e6ceac.
C source SHA256: f7de1d58667062c867a31d4ba0bd2fc2d0e8fccd91e1763b6acbb1ac95b19411.
The completed candidate-native-backend-observation-20261014 package remains unchanged; all its 17 listed artifacts were rehashed before this preparation froze. New C methods only wrap public mark/probe fixture operations; helper crypto, refusal labels and cleanup remain inherited unchanged.

Results do not cover arbitrary nesting/capacity, failed ERR_set_mark, allocation failure, concurrency, other OpenSSL implementations, provider lifecycle, untested branches, normal-binary execution or independent security certification. These are finite semantic observations in a separate diagnostic copy. The earlier unqualified assertion of known top-mark loss is contradicted by the selected finite runtime observations and the pinned counter implementation, not generalized into a universal preservation guarantee.

No product sources/binaries, settings, provider loading/configuration, dependencies, installs, credentials or services changed. No network, PG, Git or benchmark was used for this supplement. Classifier wording, full DESIGN admission, timing and product adoption remain separate decisions.

# Frozen generation-1 admission characterization

Research only; no tests run by author. Five native tests, no product source delta.

| Test | Expected observation from current source | Meaning of PASS |
|---|---|---|
| inactive_preparation_keeps_source_admitted | Exact ordinary values before preparation, after one chunk, after terminal; inspect emits no DML/seals | Inactive compatibility retained |
| gap_successor_phase_alone_leaves_original_deployment_admitted | Original plan/pin remains admitted while only the preparation row has test-only unsupported phase | Confirms a gap; NOT pending-switch safety |
| unsupported_source_phase_denies_deployment_and_fresh_attachment | check_deployment typed refusal; fresh attach PolicyMismatch | Existing fail-closed unknown source-state handling |
| target_keys_cannot_reuse_source_deployment | Target generation-2 policy fails before SQL under unchanged original plan/pin | Existing independent key-policy binding |
| gap_warm_attachment_retains_reads_after_source_phase_probe | Fresh session on old attachment still reads generation-1 values after metadata-only phase change | Confirms host stop requirement; NOT stale-worker fencing |

All live payload frames remain generation 1 throughout. Existing B9B inactive staging may hold generation 2. The synthetic unsupported phase is explicitly TEST_ONLY_UNSUPPORTED_ROTATION_PENDING. It is not a product proposal or valid lifecycle state. Each phase probe conditionally restores the exact old journal value before fixture teardown. No production state, API, grant/credential adjustment or active payload replacement is added.

The fresh attachment uses a new native registry and engine; it does not reattach an existing modified mapper. check_deployment uses a fresh unguarded runtime engine for permitted metadata inspection. The warm test closes its first session before changing fixture metadata and then starts a new session on the existing attachment.

Root runs each dependency cell using its existing lab coordination and unchanged scripts/test_postgres.py, with pytest args:

    -q tests/test_payload_rotation_admission_boundary.py

Use root's existing interpreter, wrapper invocation, dual-role private-URL preflight and receipt conventions. A failed preflight stops. This author did not run imports, collection, tests, network/database calls, or Git commands. AST parsing and source-hash preservation only were checked.

Do not invert the two gap test assertions into safety PASSes. If desired safety behavior is later implemented, revise the frozen expected behavior explicitly with a source-bound before/after receipt. Passing this file alone cannot justify a switch, publication or retirement.

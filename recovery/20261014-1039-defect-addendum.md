# Research defect and limitation addendum — 2026-10-14 10:39 UTC

This supplements prior registers; it does not replace S20's seven retained legacy failures or any qualification gate.

| ID | Observation | Status and evidence | Next boundary |
|---|---|---|---|
| B9B-PROFILE | Inactive preparer refused UUID/storage and both BIGINT profiles. | Corrected only in isolated experiment: six RED failures become six passes plus sixteen retained cases on both existing cells. Module ac09b3c0; remote51341bb3. | No active rotation/public API support implied. |
| B9B-ORACLE | Two malformed storage-header controls expected experiment refusal although native CHECK rejects setup first. | Test-only correction; R1 preserved53PASS2FAIL, R2 exact SQLSTATE23514/constraint and unchanged state;55PASSboth. Remote8ccf91e3. | Do not weaken CHECK or claim a runtime security fix. |
| B9C-ADMISSION | Successor-only pending metadata is invisible to original operation admission; warm attachments retain generation1 reads after fixture-only source phase change. | Characterized in five tests both cells, remotef78ff9e4. Existing host contract requires old workers stopped. | Source/successor handoff and current-data reversal contract pending owner decision; no payload switch performed. |
| A10-EXPIRY | Suspected version-expiry reload mismatch. | Not reproduced: eight paired native/attached sync/async UPDATE/DELETE rollback/retry cases pass bothcells, remote91b4f063. | No general ORM or concurrent-writer guarantee. |
| NATIVE-ORACLE | Original fault test duplicated mapper and compared class only. | Separate149-entry exact safe-record/trace oracle exercises unchanged mapper; both modes pass; independent audit. Remote dd447223/b2e4f013. | Causal EVP classification/full allocation-copy equivalence remain unproved. |
| NATIVE-EXACT | Original successful read checks used length/hash, and supplementary manifest coverage was incomplete. | Newly frozen1098 exact observations pass both modes; original history unchanged. Independent postrun4109 data checks. Sourcea8808321. | Old ABI/fork supplement completeness, resources, backend/provider and full DESIGN remain HOLD. |
| RECOVERY-PUBLISH | Reviewer cannot independently verify two opaque recovery payloads. | Exact audited localarchives preserved; remainingB9B9parts and nativefollowup held. Explicit owner approvals requested10:20. | Do not retry/bypass while pending. |

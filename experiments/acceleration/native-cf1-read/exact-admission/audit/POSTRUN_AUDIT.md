# Independent postrun data audit

2026-10-14. PASS for the finite recorded admission experiment. No discrepancy found. This review read JSON, source text and file hashes only; it did not import or execute candidate/native code, run PostgreSQL, build, install dependencies, use Git or change product/evidence files.

## Verified results

- 4,109 independent checks passed, using the separate audit_postrun.py implementation.
- Both O0/O1 positive receipts contain exactly all 1,098 distinct IDs in frozen order. Every complete observation equals its frozen expected record, including exact text/type, failure metadata and safe-argument/cause flags, full resolution trace, native-entry count, decode-hook flag and synthetic nonce count. Full observation arrays also match across optimization modes.
- Per mode: 108 strings, 10 NULL, 12 unchanged-baseline byte outputs and 968 typed refusals. The refusal counts are 164 InvalidFrame, 17 RepresentationMismatch, 159 KeyUnavailable, 564 AuthenticationFailed, 56 InvalidContext and 8 InvalidText.
- All eight negatives contain the correct mode/case ID and verified original actual record. Exactly the intended text/type-label/stage/trace field changes, with exact mutation content. All have zero accepted observations, exit 1 and the intended RuntimeError mismatch signature.
- All ten launch commands, optimization modes, receipt hashes, pin/manifest identities and LAUNCHES ordering match. Positive launches have exit 0 and empty stdout/stderr. No timeout receipt exists.
- All 650 frozen pins match current bytes. The manifest and PINS hashes are unchanged from this reviewer's preexecution snapshot. Original invocation specifications, fixture inventory and original ID order remain intact.
- Final ARTIFACTS matches all 33 inventoried files, with exact directory membership excluding ARTIFACTS itself.

## Fingerprints

- cases.json: a4b192bdaaa98124960efa0bedfb7c1a6417b318143555157068b03f23bb946e
- PINS.json: 59a7e61da60f7df3eae1867bee5688040ebf9f9c8ee33df9a4802bd32a200e31
- ARTIFACTS.json: a9d1a85af121319a89e6a375206502405711b0dcb2d1c115db556e552454acbe
- O0 positive receipt: 4f3e402c7937b27a5c8ee6ccc665351cf1b55260efc408c438ea84a8a48b24b1
- O1 positive receipt: 665b022789dfad4873a25a5930af50ab81a7238a82b72f8cfb81d34268d209d0

Full check inventory and negative details are in POSTRUN_AUDIT.json.

## Unchanged limits

This is independent correspondence/integrity review of recorded evidence, not independent historical execution attestation. Safe exception flags are verified recorded observations; raw exception instances and literal operation IDs are not retained. Original failure expectations retain earlier baseline provenance, while newly exact original success text has the independent public-recipe provenance reviewed before execution.

Event-loop calls remain synchronous after yielding: separate coroutine callers, no overlapping async execution or cancellation qualification. Thread entry coordination does not establish arbitrary overlap/interleavings. Negatives remain downstream observation controls; 12 seal/query byte returns belong to unchanged baseline checks, not candidate sealing.

Full DESIGN, timing, production/backend adoption, comprehensive security/fault/memory review, resource/leak accounting, ABI/fork supplemental completion, provider custody/identity and operational-cause disambiguation remain HOLD. No broader gate is converted to PASS.

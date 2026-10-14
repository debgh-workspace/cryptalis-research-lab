# Independent data-only postrun audit

PASS for the named two-case supplement only.

The independent stdlib-only auditor in `audit_receipts.py` read all receipts and independently checked every frozen record with recursive type-sensitive equality. Its output is `POSTRUN-AUDIT.json`.

- All 684 preexecution pins remain unchanged. Cases and PINS digests match the preexecution review.
- All 23 inventoried files match ARTIFACTS, with no missing or additional candidate files other than the inventory itself. ARTIFACTS SHA-256: `e819a3b5b966014dd3dac767b2a5bea348585e95e595a5ef9557485181a30adf`.
- All six launch receipts match LAUNCHES in exact planned order. Their commands, optimization flags, result digests, modes, native origins and backend identities match expectations; every result records verification of all 684 pins before imports. This latter ordering is supported by the unchanged pre-reviewed runner, not by independent execution tracing.
- The O0 and O1 positives record exit 0, empty stdout/stderr, PASS, exactly the two ordered IDs and complete frozen records. They are exactly equivalent across optimization modes.
- Native return bytes are `61626364656667`. Each full record contains native-return, expire, decode-call and decode-return in order, with the expected full argument trace at every event. Selected expiry is true at decode call and return. Final traces and safe KeyUnavailable metadata match exactly, with no public return value and one native call per case.
- The identical-bytes-object claim is grounded in the unchanged pinned proxy and identity-filtered callback plus the matching observed events; no object pointer is serialized in the receipts. The callback does not replace decode. The observation establishes this specific CPython decode path, not arbitrary interpreter/hook coverage.
- Metadata and trace negatives at each optimization mode record exit 1, the exact intended RuntimeError message and stack location, full verified original observations and exactly the declared single-field mutation. No accepted observations or unrelated traceback is present.
- No unexpected failure or timeout receipt appears. Profile/native restoration remains established by the pinned finally block previously reviewed; a separate restoration-state field is not serialized.

No candidate/native code was imported or executed during this audit. No PostgreSQL, Git or candidate/shared-artifact modification occurred. Only the owned review directory was written. Full qualification, timing approval, provider custody/security and arbitrary leak/sanitization claims remain outside scope.

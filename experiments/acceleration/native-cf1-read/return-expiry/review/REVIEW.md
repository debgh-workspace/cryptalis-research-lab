# Preexecution static review: native-return expiry

Decision: no static blocker found for the frozen two-case supplement. This is permission-neutral review evidence, not an execution result or full qualification.

Reviewed candidate: `candidate-native-return-expiry-20261014`.
- Cases SHA-256: `61526cc88cd30e869a8f2bffbeba86a97dc9343d8ddcad30fecb2235690a553e`.
- PINS SHA-256: `9fdaf8c6e5cc8dd2c6a5f125447639fae60c6e2694b394438b17602fbcc72d38`.
- All 684 recorded file hashes independently matched by stdlib-only file reading/hashing. All five new Python sources, SCOPE, cases, and freeze evidence are pinned. PINS cannot self-pin; its digest above identifies the reviewed inventory.
- Prior source-manifest digest matches the frozen reference. Pinned interpreter, original normal build metadata, original wrapper, correction support and restored key implementation are included. Pre-import verification precedes candidate imports; runner checks module origins, interpreter version/ABI, native backend and oracle versions.

## Oracle and event order

The manifest contains exactly the ordered storage/payload and equality/search IDs. Runtime uses recursive type-sensitive comparison with exact dictionary keys and list lengths/order. No asserts occur in new Python files, so these checks survive O1.

The proxy calls the real normal native function once, requires exact bytes type, records those bytes, expires the selected prepared material, and returns the same object. It neither fabricates encoded bytes nor replaces decode. The retained object keeps identity meaningful. The profile callback filters built-in decode events by this exact object's identity and records call/return/error plus a deep-copied full resolution trace and expired flag. Missing, extra, or reordered events fail the exact expected record. A decode error cannot match the required return event.

Expected event sequence is native-return, expire, decode-call, decode-return, all before final re-resolution. Storage expects one payload resolution at each event and two at final refusal. Equality expects payload/search at each event and payload/search/payload/search at final refusal. The unchanged pinned wrapper confirms decode precedes final checks; the pinned prepared-key resolver records attempted resolution before the expired material raises.

All safe fields are compared: exception class name, code, stage, retryability, effects, remedy, nonempty string operation identifier, canonical exception args, absent explicit cause, suppression false, and no returned public value. A normal return, wrong error, incomplete record or unexpected exception cannot become PASS. Canonical args are built from independently compared safe metadata; this is not an arbitrary context, traceback, side-channel or leak-sanitization claim. Decoded text exists internally before refusal, as the scope explicitly tests.

## Cleanup, bounds, and negative controls

The callback is installed only around the wrapper invocation. A pre-existing profile is rejected before replacement. Finally restores the saved profile and native module and checks original mapper identity. Callback exceptions fail rather than bypass the oracle. This is single-threaded CPython profile observation, not general tracing coverage.

Six planned subprocesses cover metadata-negative, trace-negative, positive at O0 and O1. Each has a 180-second timeout with subprocess.run cleanup. Receipts are exclusive-create, including launch and timeout receipts. No unbounded retry loop exists.

Each negative first verifies the complete actual record, then mutates exactly one field: storage stage, or equality trace length. The launcher requires exit 1, FAIL receipt, RuntimeError, exact mismatch message, original_verified record, no positive observations and the exact final traceback signature. An earlier oracle failure has no verified negative record and cannot pass as the intended negative. Positive requires exit zero, empty stdout/stderr and PASS. Expected records are retained for postexecution independent inspection.

## Limits and performed actions

Only source/manifests and pinned files were read; stdlib hashing and AST inspection were used. No candidate or native module was imported or executed. No PostgreSQL, Git, provider operation, build, dependency change or shared-artifact edit was performed. Only this owned review directory was written. Runtime results remain unestablished until separately authorized execution and receipt review. Full DESIGN admission, broad error classification, provider custody/security, sanitizer proof and timing remain held.

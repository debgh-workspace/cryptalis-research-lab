# Independent postrun direct-only data audit

2026-10-14. Read-only source/JSON/hash audit after separately authorized worker execution. This reviewer did not build, import or rerun the candidate or tests. Only this audit note was written.

## Bounded result

Saved receipts are internally consistent with successful direct-only qualification:

- Normal build: 93 exact ordered unique IDs PASS in ordinary Python and 93 in -O.
- Diagnostic build: 96 exact ordered unique IDs PASS in ordinary Python and 96 in -O.
- Total: 378 positive case instances, each with PASS recovery marker.
- Four deliberate actual-output-corruption runs: expected failure in each build/mode, child exit 1, exact RuntimeError `tuple mismatch: oracle/uuid-storage-unicode/payload-info`.
- All four positive child exits are 0; all eight launcher records mark expected outcomes accepted. Each saved receipt SHA matches its launcher record; each positive receipt build hash matches the corresponding saved build record. Optimization/negative flags and command-line -O selection agree.
- Both builds report BUILT, compiler exit 0, cpython-312-x86_64-linux-gnu ABI. Commands match the reviewed flags and differ in diagnostic definition and output path. Both resulting extension hashes match. Each build's 231 recorded input hashes matches current bytes.
- Guard summary PASS has exactly four stage records: normal build/test, diagnostic build/test, all exit 0. Embedded records equal their individual saved files and point to the correct provenance hash. No failure receipt or retry appears in this run directory.

The positive records retain ID/PASS/recovery, not actual tuple output bytes. Therefore exact-byte correctness is supported by the reviewed driver's explicit literal comparisons and recorded successful outcomes, not independently recomputed from saved raw native output. The audit establishes record/source consistency, not signed execution attestation or proof of every reported machine action.

## Provenance and source stability

DIRECT_PROVENANCE.json SHA256:
`44f4300ed6c84a79f26d9ba41ec3d99e549e7048bac8973709471011b5eb5788`.

All 4,147 prebuild file pins match current bytes. Guard source matches its recorded SHA. All ten original DIRECT_FREEZE entries still match. Guard source checks these pins before and after each stage and rejects named inherited compiler/linker/loader/Python override variables. Its capture includes system/Python headers, GCC support tree, interpreter/compiler/assembler/linker/readelf/ldd, selected link objects and observed trusted-tool shared dependencies. The existing reviewed build/launch/direct sources were preserved.

Both saved readelf dynamic reports contain exactly one NEEDED library, `libc.so.6`; neither reports libcrypto. libc and observed tool dependencies are covered by the added provenance capture. This closes the earlier direct-run gap of only recording headers/tools at build time and leaving inherited named overrides unchecked. It remains a bounded provenance snapshot, not a claim to enumerate every compiler internal lookup, environment influence, filesystem race, kernel input or cryptographic attestation. No claim is made that this tuple-only test exercised P's cryptography/OpenSSL backend.

## What this supports, and what remains open

Supports direct tuple finite-oracle, wrong-type/count/keyword/size refusal, repeated borrowed-input refcount, diagnostic preallocation MemoryError refusal, and explicit-check harness sensitivity evidence on this build/ABI. Refcount observations are not allocator-free counts or leak proof. Diagnostic preallocation refusal is not actual memory exhaustion. No sanitizer, actual allocator-failure, module-import failure, platform-generalization or secure-erasure result follows.

The six wrapper allocation cases, full-wrapper 1098-case execution, precise expiry/PID/decode hooks, actual-fork/recovery and caller isolation evidence, source mutants, complete DESIGN mapping, and full-wrapper provenance remain unexecuted within this direct scope. No full-read correctness admission, performance result, five-arm protocol selection, product adoption or C9/C10 change follows. The full-wrapper and timing HOLD remains.

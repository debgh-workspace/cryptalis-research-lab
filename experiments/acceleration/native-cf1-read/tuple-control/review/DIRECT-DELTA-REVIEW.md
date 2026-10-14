# Subsequent direct-driver source review

2026-10-14. Supplemental review of DIRECT_FREEZE.json SHA256 `dd14a98195a42de193de2d7049fc6d942e96066ea6b435054dcedc1707936071`. No build/import/test execution. The initial REVIEW.md describes the earlier state and remains unchanged.

All ten delta hash entries match. The three new Python files parse as source. DIRECT_MANIFEST has exactly 93 unique normal IDs and 96 unique diagnostic IDs, consistent with selecting direct tests from the broad 106-item manifest. The difference is two allocation-diagnostic cases plus diagnostic allocation-refcount refusal. Six full-wrapper allocation tests and four future mutants are excluded, explicitly.

The direct driver compares exact bytes and exact type against frozen literals, exercises six wrong types at every position, 8-part/keyword refusals, exact cap/over-cap arithmetic, and applicable repeated refcount checks. The cap prefix literal decodes to one component of length 16,777,720. Refusal helpers return after exception handling, avoiding persistent exception traceback references at the refcount check. Recovery executes after each completed case. Explicit comparisons survive -O. Negative mode corrupts actual output after a real helper invocation and the launcher requires the specific first-oracle mismatch failure; this is harness sensitivity, not a C source mutant or wrapper negative.

Build uses exclusive new directories and records failure. Launch uses four sequential bounded child processes per build, with interpreter/ABI/source/binary checks before native import, exact extension import path, and required diagnostic export presence/absence. No tuple_read/S20/cryptography import appears in these direct drivers. Normal and diagnostic builds differ by the preprocessor definition. Ordinary and -O tests are separately invoked; failures stop rather than retry. No concrete source defect in these direct checks was identified.

Scope/provenance limits remain:

- Compiler/interpreter/header bytes are snapshotted during the future build rather than compared against predeclared toolchain-byte pins. Most compiler environment variables are inherited (only PYTHONPATH/PYTHONHOME are removed), so this is not a hermetic toolchain specification. Compiler subprocess selection/search paths and relevant environment should be recorded or constrained before claiming reproducibility.
- ELF dynamic dependencies are recorded by readelf but are not validated/hash-pinned by the launcher; interpreter shared dependencies and readelf itself are not in the explicit input list. This does not satisfy full original DESIGN binary/dependency provenance. No alternate crypto library is deliberately linked, but successful readelf output alone is not an enforcement check.
- No sanitizer/leak run or true exhausted-allocation injection is implemented. Direct refusal/refcount success cannot claim those properties.
- Direct child launch is bounded; a failed child without a receipt remains a failed launch, not a success. Build/direct completion cannot qualify full-wrapper behavior or authorize timing.

FULL_SOURCE_INDEX adds 23 references, all matching at review. FULL_EXPECTATIONS preserves ordered identity/index association for all 1098 canonical cases. An independent static classification from result type, exception, and ordered resolution trace agrees with every proposed tuple-entry count: 628 cases with 3, 394 with 0, 76 with 6. This is a consistency check against canonical frozen outcomes and wrapper order, not executed evidence or an independent re-derivation of the original outcomes. Canonical F native_calls must be excluded exactly as documented.

The new FULL_WRAPPER_PLAN correctly distinguishes T helper return from F plaintext return, preserves exact bytes, and proposes code-identity-specific decode tracing rather than bytes-subclass injection. Those hooks, their precise event/line/reachability checks and failure negatives remain unimplemented. Full-wrapper execution therefore remains HOLD. Applicable DESIGN A–F mapping, actual-fork evidence, six allocation-site hooks, source mutants and full runner still need frozen executable artifacts and review.

The author confirms no original checklist snapshot was captured, only its original hash. CONTEXT_LATER records a later ledger hash without replacing that history. Since the ledger is mutable, these hashes identify distinct preparation/review observations and are not candidate integrity failures. No historical bytes are claimed recovered.

Conclusion: source review supports coordinator consideration of a separately scoped, explicitly authorized direct-only smoke build/test, with the above provenance limits disclosed. It does not grant authority, assert results, or lift full-wrapper/timing/product holds.

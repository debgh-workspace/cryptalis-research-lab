# Bounded T direct-helper results

2026-10-14. Root separately authorized the independently source-reviewed direct
build/test boundary. Original source-preparation records are historical and remain
unchanged. This result does not supersede their original NOT RUN statements with
retroactive evidence.

- Normal build: 93 direct cases PASS in ordinary mode; 93 PASS in -O.
- Diagnostic build: 96 direct cases PASS in ordinary mode; 96 PASS in -O.
- All four downstream actual-byte-corruption controls failed at the frozen first
  tuple comparison, with exact expected error and process exit status.
- Every positive case includes an exact all-octet valid recovery invocation.
- Per mode, three normal and four diagnostic retained-input-reference loops run
  1,000 iterations each. This is retained-reference evidence, not heap leak proof.
- Diagnostic allocation refusal is injected before allocation. It does not prove
  actual allocator exhaustion or cleanup of allocations that were never acquired.

378 positive case observations total. No assertion-based checks, automatic retry,
replacement case, timeout, compile failure or unanticipated test failure occurred.
The two C compilations used the frozen source with the reviewed flag difference.
Both ELF dynamic reports declare libc.so.6 as their sole NEEDED library. No native
crypto provider, OpenSSL context or new cryptography backend is involved.

The additional pre-build provenance guard captured 4,147 pins, including trusted
compiler/tool dependency paths, Python/system headers, GCC support tree, libc and
link objects. It rejected inherited compile/link/Python override variables and
rechecked pins before and after every build/test stage. DIRECT_FREEZE.json was
not rewritten. This is bounded source/build integrity evidence, not hermetic or
signed execution attestation. The guard does not claim every compiler internal
lookup, kernel input or actual loaded-memory map has been independently observed.

Evidence:
- DIRECT_PROVENANCE.json, guard_direct.py
- build-direct-01-normal/build.json
- build-direct-01-diagnostic/build.json
- direct-evidence-01-normal/{positive,negative}-o{0,1}.json and launch.json
- direct-evidence-01-diagnostic/{positive,negative}-o{0,1}.json and launch.json
- direct-run-01/summary.json and four bounded outer process receipts

No full-wrapper test, crypto operation, timing, PostgreSQL, network, installation,
credential operation or Git operation occurred. Full-wrapper integration, exact
public failure/expiry/fork behavior, supported sanitizer/leak observations, timing
admission and product qualification remain HOLD/NOT RUN as applicable. Independent
postrun audit was requested; this file does not preempt its result.

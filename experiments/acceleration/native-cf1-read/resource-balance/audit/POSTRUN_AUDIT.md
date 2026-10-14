# Independent postrun evidence audit

PASS: 6,220 checks using only Python standard-library reads, JSON comparisons and hashing. No candidate code/native import, compilation, test rerun, database or Git operation was performed. Reviewer writes are confined to this review directory.

Verified:
- Both positive processes report all 170 declared observations in exact order. Public success values/types, safe failure metadata, resolution traces and native entry records match the frozen manifest. Direct admission observations match their declared bytes/exception outcomes.
- All ten resource categories match exact acquisition, release-call, transfer, outstanding and peak expectations for every observation. Scratch requested-byte counts match. All 170 observations per mode end at zero tracked outstanding references and scratch bytes.
- Full observation records match exactly between O0 and O1.
- All four negative processes fail with exit 1 and the exact RuntimeError comparator signature. Each contains the original verified real success record and precisely one intended change: MD release count reduced by one, or result ownership transfer removed. These are downstream evidence mutations, not induced leaks.
- All 692 runtime pins and 689 source pins match current bytes; the seven pre-reviewed source hashes remain unchanged. Build receipt records successful compilation and receipt origins match its native binary. Backend identity here is the harness's declared version/origin evidence, not independent provider custody attestation.
- All six launch receipt hashes verify. All 33 final artifacts are listed and hash-correct, excluding ARTIFACTS.json itself; its exact author freeze hash is checked separately. RESULTS.md matches the final author hash.

Per mode, eight EVP categories have acquisition/release-call totals of MD 246, MD_CTX 243, KDF 231, KDF_CTX 228, CIPHER 146, CIPHER_CTX 144, MAC 76 and MAC_CTX 75. Scratch has 136 acquisitions and 136 release calls. Reserved result references have 138 acquisitions, 28 decref-path releases and 110 successful return transfers. The 110 successful outcomes and 60 refusals cover only the declared finite manifest.

This is matched helper-owned reference accounting and observed cleanup/transfer path evidence. It is not evidence of actual internal OpenSSL/provider allocator deallocation, full leak freedom, zeroization, real allocation exhaustion, arbitrary partial failure, concurrent/free-threaded operation, full ABI/fork coverage, packaging, performance or production/security qualification. Existing holds remain.

Artifacts: audit_postrun.py and POSTRUN_AUDIT.json. The original pre-execution REPORT.md capture description was clarified to match the frozen guard: arguments are captured before success-designated calls, whose successful outcomes are then checked. No candidate file changed.

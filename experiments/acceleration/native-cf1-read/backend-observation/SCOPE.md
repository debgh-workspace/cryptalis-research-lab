# Bounded backend observation plan

Diagnostic public-fixture slice only; coordinator review required before compile/run.

Copy original native_cf1.c (SHA256 2926d61e43b3dc53a5fff56ab5367982c89b92b146ef9cbc47fbd2b71e5a9469) with call-local fixed-buffer observations at actual successful top-level fetches. Slots: payload SHA256/HKDF, AES-256-GCM-SIV, search SHA256/HKDF, HMAC. Public provider name and method name are copied while method is alive. Public cipher key/IV/block lengths, mode and flags are recorded. All request properties remain provider=default. Nested digest implementation identity is not observable here.

36 cases predeclared in cases.json: storage success/bad tag/fault1/fault10/fault17, equality same plus wrong search root/fault30; each with 0/1/2 benign unmarked public ERR_LIB_USER sentinels. Fresh public Unicode vector bytes, exact success bytes/private refusal string. Read pre-call oldest/newest sentinel using public peeks (0..2 known entries); after call drain with ERR_get_error_all and compare exact ordered code/file/line/function/data/data-flags, including no extra entries. No error-string causal classifier. Diagnostic result captures exception instance for exact private args comparison; no public wrapper policy inference.

Expected fetch-stage subsets are frozen in run.py from source branches. Identity values are observed rather than post-hoc oracle outcomes. Check provider=default selection and cipher key32/IV12, record other properties without turning observations into new prior expectations. Two downstream comparator controls (corrupt queue entry and provider name) must reject before positive receipt. Separate diagnostic binary, Python O0/O1, no normal-binary run. Build/run receipts and all source/header/library/interpreter/tool pins, exclusive output names. No product changes, installs, dependencies, provider load/config/security settings, credentials, service, PostgreSQL, Git or timing.

Queue claim excludes exhaustion, arbitrary internal errors, preexisting marks, other threads and untested failure paths. The old report's definite preexisting-top-mark-loss claim is not justified for tagged OpenSSL 3.5.7: crypto/err/err_mark.c increments/decrements per-entry mark counts. No runtime mark preservation result is claimed. ERR_set_mark failure/property guard injections are outside scope. Full classifier reconciliation, full DESIGN, timing and adoption remain undecided/held.

Primary references inspected:
- https://docs.openssl.org/3.5/man3/ERR_set_mark/
- https://docs.openssl.org/3.5/man3/ERR_get_error/
- https://docs.openssl.org/3.5/man3/EVP_EncryptInit/
- https://raw.githubusercontent.com/openssl/openssl/openssl-3.5.7/crypto/err/err_mark.c

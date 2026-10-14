# Independent public native oracle-extension evidence audit

2026-10-14. Verdict: bounded PASS. The extension closes the six standard primitive-vector and eight frozen intermediate-value comparison omissions identified by the original and correction audits, at the diagnostic scope below. No certain blocking defect was found for this bounded claim. Full DESIGN correctness admission, timing, product/backend admission and provider qualification remain HOLD.

## Method and result

Read the original DESIGN, prototype RESULTS and evidence audit, correction audit, extension source/diff, harness, freeze/build mechanism and final evidence. Ran only this directory's independently authored stdlib-only verify_data.py. No candidate/product imports, native execution, compilation, test rerun, benchmark, database, Git, installation or shared-source edits occurred. verification.json records the results. This is static/data verification, not independent historical execution attestation or complete security review.

- Exactly fourteen unique ordered entries preserve all original input records: four AES-256-GCM-SIV vectors, one RFC5869 HKDF-SHA256, one RFC4231 HMAC-SHA256, and eight CF1 vectors. Expected records exactly match their frozen fixture fields.
- Both positive receipts record the same ordered fourteen exact outcomes, exit 0 and empty stdout/stderr. All six launch commands and receipts agree on Python optimization mode, manifest/pin/binary digests and executable. O0/O1 mean Python flags; C is compiled once with -O2.
- All 639 current PINS entries, 636 PREBUILD pins and 161 original inventory files match. Both artifact inventories match; ARTIFACTS-02.json covers every other current extension file (31). The complete computed native-source diff equals NATIVE-SOURCE.diff.
- The recorded build exits 0 with empty output, uses CF1_DIAGNOSTIC, does not define CF1_SKIP_TERM, and links to the current prebuild digest. The manifest is a required input with a matching prebuild hash. Four Python scripts contain no AST Assert nodes.
- RESULTS.md's “five Python scripts” is corrected by preserved REPORT-ERRATUM.md to four; the final inventory includes the erratum and previous inventory. No substantive discrepancy follows.

## Oracle and provenance interpretation

The fixture digest remains 24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e. prepare_build.py copies the original frozen inputs and expectations directly, without native imports or regenerated expected cryptographic outputs. The eight CF1 fixture records retain the stated independent RFC8452 composition provenance: OpenSSL AES-ECB plus stdlib SHA256/HKDF/HMAC. This is independent composition, not an independently implemented machine/backend qualification. This audit verifies preservation and correspondence; it does not refetch RFCs or rerun the fixture reference.

The four AES entries compare both complete sealed bytes and complete authenticated plaintext. HKDF requests and compares all 42 bytes, with extract-and-expand through supported EVP_KDF. HMAC compares all 32 bytes through EVP_MAC. The CF1 derivation remains 32 bytes. Diagnostic primitive code uses supported EVP APIs rather than a new handwritten crypto implementation.

All eight intermediate entries compare exactly payload salt/key, search salt/key, header, AAD, term, encoded text and strictly decoded text. Storage search salt/key/term are explicitly empty. Source review confirms salt/key capture occurs from the actual values used by derive, AAD from the actual submitted buffer, term from the recomputed MAC, and encoded text from the authenticated output. Equality search derivation still follows successful AEAD finalization, and the dictionary is returned only after the term comparison succeeds. Header capture is the actual input header slice, not independent header construction. Strict Python decoding here is diagnostic-output decoding, not the original complete wrapper/final-resolution boundary.

## Negative-control strength and limits

Each mode first observes a successful native result and checks it exactly against the manifest. It copies the unmodified record into the receipt, changes the first byte of the actual output hex (HKDF output or intermediate payload key), and invokes the same explicit exact comparator used by positives. Independent receipt checks confirm the single changed byte and unchanged other fields.

All four controls record original_verified=true, FAIL, RuntimeError with exactly “Exact oracle mismatch”, zero positive observations and process exit 1 with empty stderr. The outer driver rejects missing receipts, unrelated failures and unexpected stderr. Source orders all negatives before positives. These are actual-result-derived downstream observation mutants; they are not mutations within the native implementation or product return channel. Hashes and consistent records cannot independently attest the historical execution order.

## Diagnostic isolation and remaining holds

The new source refuses compilation without CF1_DIAGNOSTIC and is built separately. Its capture dictionary is call-local. Product source and original native source/binaries remain covered by matching current pins/inventory. No runtime/product diagnostic hook was introduced. Public fixture byte copies deliberately survive as Python bytes; this is not secret-erasure or production-memory-safety evidence.

The source's explicit provider=default fetch properties and recorded successful primitive results support the narrow implementation claim. The actual provider identity is not separately queried/attested. Existing backend mismatch, operational-vs-authentication failure ambiguity, original incomplete supplementary manifests and class-only fault adapters, allocation/leak accounting, concurrent distinct-scope isolation, custody/platform/packaging and full provider qualification remain unresolved. This extension does not add unchanged sealing/query parity across all frozen vectors or retrofit every old read/grid outcome to exact text. The original full wrapper, NUL handling and final resolution gates are not comprehensively retested by this diagnostic entry.

No timing or shipping permission follows from this bounded PASS. No additional native execution is requested or implied.

## Artifacts

- verify_data.py: independently authored reproducible data/static checker
- verification.json: 639 pin, 636 prebuild-pin, 161-original, fourteen-entry and four-negative correspondence result
- cases.json SHA-256: a472b7a2531a41526fcbdb57a1971e370c96b47af5df9a2891059cf94ff93efe
- PINS.json SHA-256: 653fad85be61803399417a23b4c5de94c77347dcd39fa181e8c9291ffc6b7422

# Public native oracle extension results

2026-10-14. Bounded PASS: the six standard primitive entries and eight frozen public intermediate entries pass exact, assertion-independent comparison at Python optimization flags 0 and 1. Full DESIGN correctness admission, timing, and product/backend admission remain HOLD.

## Results

- Four preserved AES-256-GCM-SIV primitive entries compare exact encryption output and exact decrypted plaintext. One RFC5869 HKDF-SHA256 entry compares all 42 requested bytes. One RFC4231 HMAC-SHA256 entry compares all 32 bytes.
- All eight preserved CF1 vectors compare exact payload salt/key, search salt/key, header, AAD, recomputed equality term, authenticated encoded text, and strictly decoded text. Storage search/term values must be empty. Equality key derivation remains after successful AEAD authentication. CF1 derived keys remain 32 bytes.
- Four expected negative process failures are preserved: actual HKDF-output and actual intermediate-payload-key perturbations in both Python modes. Each first verifies the unmodified native result exactly, then mutates a byte in that actual result and uses the same comparator. Each exits 1 with exactly `RuntimeError: Exact oracle mismatch`, zero positive observations, and empty process stderr. The outer runner checks this precise failure, so unrelated import/setup failures cannot count as successful negative controls.
- Both positive processes exit 0 with empty stderr and exactly the same ordered fourteen observations. Comparisons use explicit conditionals, not assertions; AST inspection of all five Python scripts finds no Assert nodes.
- All 161 inventoried original files remain byte-identical. The original native source/binaries, correction, design, original audit and product sources were not changed. No old suite was rerun.

## Mechanism and provenance

The copied native source is compiled once into a separate diagnostic-only extension with GCC 14.2.0, C11, -O2, -Wall, -Wextra and -Werror. The build has zero warnings/errors. O0/O1 denote Python flags, not alternative C optimizations. The pinned venv executable is Python 3.12.14, ABI cpython-312-x86_64-linux-gnu. Native backend is explicitly checked as OpenSSL 3.5.7 9 Jun 2026. Supported EVP digest/KDF/MAC/cipher APIs use explicit `provider=default` properties. No provider service, private key, DB, installation, Git, product/runtime hook or timing work occurred.

The added capture is call-local, reads the actual salt/key values used by the copied CF1 path, and returns only after successful authentication and term verification. NATIVE-SOURCE.diff documents every change to the original C source. Separate primitive_diagnostic.inc supplies the primitive checks through supported EVP. It is not a new handwritten crypto implementation. The build is rejected unless CF1_DIAGNOSTIC is defined; no production API was modified. Diagnostic public-byte copies are not a secret-erasure claim.

prepare_build.py copies expectations directly from the unchanged fixture, freezes the fourteen-entry JSON before compilation/import, checks inherited pins, inventories originals, records pre-build hashes, compiler command/output, and post-build binary/dependency pins. check.py checks pins and exact import origin before native execution. run.py executes negatives before positives. audit_data.py performs a subsequent standard-library-only correspondence and integrity self-audit. Source hashes and process receipts support reproducibility; they are not independent execution attestation or authenticated historical chronology.

- cases.json SHA-256: a472b7a2531a41526fcbdb57a1971e370c96b47af5df9a2891059cf94ff93efe
- PINS.json SHA-256: 653fad85be61803399417a23b4c5de94c77347dcd39fa181e8c9291ffc6b7422
- Original fixture SHA-256: 24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e

Full receipts: build-01.json, PREBUILD.json, PINS.json, six process observation receipts and six launch receipts, SUMMARY.json, DATA-AUDIT.json. ARTIFACTS.json inventories final artifacts. No failed build/positive check required repair; four deliberate negative failures are retained.

## Strict limits and remaining holds

This closes only the named primitive/intermediate gaps. It does not qualify all DESIGN cases, rerun the wrapper's complete read boundary, verify final resolutions in this new diagnostic entry, retrofit old length/hash checks, add frozen sealing/query parity, repair original fault adapters, qualify generic EVP failure causes, or measure allocations/leaks. Exact text here is decoded from diagnostic authenticated bytes, not evidence of the complete Python wrapper boundary. Header capture compares the actual input slice with frozen expected bytes, not an independent native header construction. The eight frozen fixtures retain independent composition provenance (OpenSSL AES-ECB plus stdlib reference); this is not an independently implemented backend qualification.

Runtime provider identity is not separately queried or attested here; explicit fetch properties and successful primitive execution provide narrower evidence. No sanitizer/leak run or independent security review was added. Original backend mismatch, incomplete full fault equivalence, concurrent-scope tests, full manifest completeness, provider custody, platform/packaging and production approval constraints remain unchanged. Do not interpret this fourteen-entry PASS as permission to time or ship the candidate.

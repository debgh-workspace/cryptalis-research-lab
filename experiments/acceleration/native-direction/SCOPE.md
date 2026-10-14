# Direction-specific native primitive probe

Status: standalone component research only. Not CF1 integration, backend admission, performance qualification, or a product feature.

Hypothesis: a direction-specific per-value EVP decrypt can avoid constructing both encryption and decryption contexts. This first slice establishes only compilation and bounded primitive equivalence, before any timing or fused-CF1 work.

The module exposes only bounded AES-256-GCM-SIV decryption with exact bytes, 32-byte key, 12-byte nonce and 16-byte tag. It fetches the named cipher from the default provider, creates and frees native state for every call, checks every primitive result, and creates the Python plaintext result only after authenticated completion. There is no dynamic cache or product entry point. The isolated public fixture runner does not import Cryptalis or connect to PostgreSQL.

Build 01 failed because sysconfig retained /install/include/python3.12. Build 02 changed only the compiler include directory to the verified matching installed Python 3.12 headers. Source unchanged. Both receipts preserved; no packages installed.

76 checks pass: four frozen published primitive vectors, eight deterministic public-fixture comparisons against unchanged pyca, 32 authentication-refusal controls, eight successful fresh calls after refusal, 16 exact-type refusals and eight bounded-length refusals. These are component checks, not a complete native memory-safety audit or CF1 test suite.

System OpenSSL is 3.5.7; pyca's backend differs. No product backend change is authorized by these results. Full CF1 context/framing/HKDF/HMAC, lease/PID, NULL/codec behavior, async cancellation, packaging/distribution, independent review and real PostgreSQL/end-to-end performance remain unqualified. Python immutable inputs and returned bytes have no verified zeroization guarantee. Native buffers are cleared on release, without asserting whole-process secret erasure. The module holds the GIL, and its interaction with application threading and OpenSSL's error queue is not qualified.

Sources inspected: https://docs.openssl.org/3.5/man3/EVP_EncryptInit/ and the previously recorded pyca 50.0.2 implementation. No external implementation code was installed. Owned source authored in the authorized isolated workspace.

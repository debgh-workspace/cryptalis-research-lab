# Actual Stage A materialization: accepted

Decision: PASS_INDEPENDENT_DATA_MATERIALIZATION_AUDIT. This review accepts the actual deterministic wheel/dependency materialization for the separately source-reviewed, root-selected Stage B constructor check. It does not itself select or execute Stage B.

## Binding

Packet: diagnostic-installed-boundary-v1-20261017. Accepted executable source review SHA256 0bd9bf0e4e6452ab4d5e1b75f02a9c898bccb85dacfcfdbc2a99cdae733cebb8 (7275 bytes). Controller selection binds controller 8b2c9ab0079852ac0fc0e575b03a02cd1d514ae90eef65635ac83b044450ba66 and that exact review. FINITE_MATERIALIZE.json SHA256 75f93777b4c9bc6937f28e65b6447e45174dfd542f83adf085d7155c56f85cf3.

Actual wheel: 141416 bytes, SHA256 55fde72147caddf2be41fa397fc855682a347f2fcbb26c527262810117b90b03. Actual destination is the packet's run/installed/site-packages. This is data-only materialization, without package-manager installation or generated console launcher.

## Independent actual observations

- Exact 557 regular, single-link installed leaves and 55 required directories, with no extra leaves/directories or symlinks. All expected sizes and SHA256 values match. Metadata was admitted before the complete body-hash pass; each bounded no-follow read checked descriptor and path stability.
- All 509 dependency copies, totaling 56024595 bytes, match the declared CP84 donor bytes and hashes. Every donor/destination device-inode pair is distinct. Shared donor links remain allowed by the accepted finite source policy; every new leaf has one link.
- All 48 wheel files exactly equal the accepted wheel's uncompressed bodies. The archive has 54 unique entries: 48 files and six directory entries. The exact file namespace was checked before payload reads. CRC-checked payload reads and the independent installed comparison pass.
- All 48 RECORD rows cover the exact wheel file set. Each of the 47 non-self entries has the correct URL-safe SHA256 and byte count; RECORD's own fields are empty. All 43 Cryptalis runtime files have their exact expected hashes.
- The exact 532 original input paths match the guard's before/after path sets. Every after record reports metadata and bytes equal. Independently observed current seven-field metadata equals each recorded before tuple, and every current original body matches its pinned SHA256. This includes the 509 donors, wheel, controls, accepted reviews, interpreter and original patch.
- Original Outputs/CRYPTALIS_FINAL.patch remains 219914 bytes, SHA256 9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd.
- Materialization receipt reports complete_readback=true and 509 exact copy records, independently reconciled against the copy plan and actual outputs.

## Terminal and scope

Guard status PASS_GUARDED_MATERIALIZE_PENDING_TERMINAL_REVIEW is reconciled by this independent acceptance. Child exit 0, reason null, leader reaped, empty stdout/stderr, no group signals, no cleanup errors, no received signal, and cold bytecode prefix absent. The receipt's descendants_verified_absent=false is preserved; successful leader completion and stable admitted files do not prove global OS descendant absence.

Guard terminal: 277024 bytes, SHA256 a1f4008e43762b85f2cbaec1c7b3956e796d8477135c2f39b069c91382d81c65.
Materialization receipt: 261317 bytes, SHA256 a9bc4e36fdefdc96ef78a8e4b8035dd1f3e54ce99aad78485aabfbeec8516286.

Reviewer ran only its own standard-library read/hash/archive/JSON audit. No target import, product execution, installer rerun, build, test, database operation, Git action or opaque/private marker read occurred. Existing host/interpreter/native trust remains the explicitly accepted basis, without fresh native provenance claims. Installed runtime origins and the 20 candidate constructor outcomes remain Stage B evidence to establish after a fresh root selection and admission. No baseline/full-suite repeat, production or integration acceptance follows from this result.

CHECKS.json and audit.py in this directory retain the concrete data audit. All author outputs and earlier failures remain untouched.

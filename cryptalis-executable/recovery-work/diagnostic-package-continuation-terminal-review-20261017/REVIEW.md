# Independent diagnostic packaging continuation terminal acceptance

Status: ACCEPTED_SAME_HOST_DIAGNOSTIC_PACKAGING. The successful continuation completes the five-artifact evidence set by reusing the independently accepted first sdist and running only the four remaining builds. Original V3 remains FAIL; no historical failure is relabeled.

Root capture persistence-recovery-20261013/diagnostic-packaging-continuation-20261017-1452 records controller0 and after-check0. Guard status was PASS_GUARDED_DIAGNOSTIC_CONTINUATION_PENDING_TERMINAL_REVIEW, child0, no timeout/cancellation/group signals/cleanup errors, reaped leader and empty stdout/stderr. Driver status was PASS_SAME_HOST_PACKAGING_PENDING_INDEPENDENT_REVIEW. The two pending-review statuses are now accepted within this report's packaging scope. They do not establish installation/runtime/DB qualification.

## Actual artifact identities

Two byte-identical sdists,150917 bytes each:
SHA256 f8520edb34bb20af9a348a2e68f4073346548057d8d7e52b1489d2d0608632d8
- diagnostic-offline-package-controls-v3-20261017/run/sdist-1/cryptalis-0.1.0.tar.gz (retained original)
- diagnostic-offline-package-continuation-v1-20261017/run/sdist-2/cryptalis-0.1.0.tar.gz

Three byte-identical wheels,141416 bytes each:
SHA256 55fde72147caddf2be41fa397fc855682a347f2fcbb26c527262810117b90b03
- diagnostic-offline-package-continuation-v1-20261017/run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl
- diagnostic-offline-package-continuation-v1-20261017/run/repeat-wheel/cryptalis-0.1.0-py3-none-any.whl
- diagnostic-offline-package-continuation-v1-20261017/run/roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl

All relative paths above are under cryptalis-executable/recovery-work. Exact absolute paths are in CHECKS.json. These sizes/hashes are the artifact publication facts; no upload, public release or exception to the pending upload restriction is authorized by them. Version/filename remains0.1.0, so hashes and isolated locations distinguish this derivative from predecessor artifacts.

## Independent byte and preservation checks

All700 declared inputs were metadata-admitted as ordinary single-link files, independently rehashed against static/selection/pair/review pins, and checked against recorded before tuples (dev,ino,mode,nlink,size,mtime,ctime). All700 reported after checks and current observations pass. Original patch and old442 source-copy leaves remain included. Both original V3 driver and guard receipts still say FAIL; its first artifact is unchanged and build_repeated=false. Continuation records exactly four commands, all exit0, with no first-sdist command repeated.

The new two complete source copies have exact221-file namespaces and all442 hashes match proposed manifest1c453915b2cee3e5cd069bc6772d3ae70f8df9aa73c1f85b5cad4762e861d5f9. The49 extracted sdist files and exact parent-directory set independently match the admitted first sdist after roundtrip. Five output directories, including the retained one, contain only their distribution and one-byte '*' .gitignore; each sidecar matches the already admitted official-source behavior. No other hidden/cache body was read.

Independent bounded single-stream gzip decoding and tar/ZIP header/name/type/layout admission preceded member payload reads. Each sdist has49 regular payloads and6 directories; each wheel has48 payloads and6 directories. Header metadata matches the admitted predecessor archives. All43 runtime members match the proposed source. Only migration.py differs in sdist; only migration.py and RECORD differ in wheel. All other payloads match predecessor. Source LICENSE/README/lock and original TOML match source hashes, normalized TOML semantics agree, and PKG-INFO equals wheel METADATA. RECORD has48 unique exact rows,47 independently verified SHA256/size entries and empty self fields. ZIP member CRC reads completed successfully.

The successful sealed driver path necessarily executed the shared missing-lock and altered-lock rejection controls before reporting PASS. This reviewer independently inspected those control paths during source review and accepts their actual successful-path evidence here; the controls were not rerun during terminal review. Likewise no build/helper/product module was executed by the reviewer. Independent archive/data checks use reviewer-owned standard-library code only.

## Evidence and limits

- Guard terminal SHA256849ef11832dc921a6470438177c12efd25a7c2ea4201d26b0876d5d699c4dd7e
- Driver receipt SHA25676ba8f13ba1016b4c85daee1642b45a013e26a8e638983884efa98ac65205a23
- Independent CHECKS.json SHA256583a3fd13ac2214ab42d4135da2c18bad7bf0cf7c6c19818cd6ecb2be8275ddb

This establishes same-host offline package reproducibility and source/member/RECORD binding for the diagnostic-only derivative. Existing host interpreter/stdlib/loader/uv trust remains explicit, without fresh vendor/native source provenance. descendants_verified_absent stays false. No new installed-origin check, product runtime suite, DB operation, clean-host reproducibility, search integration or production promotion is established.

The next smallest evidence boundary is a separately reviewed fresh-prefix materialization of the exact141416-byte wheel, admitted existing dependency copies, complete installed hash/RECORD readback and genuine installed-origin candidate20-case constructor check. It needs separate source acceptance and root selection; do not repeat the accepted baseline constructor run. No download, existing-prefix mutation, database access or publication is implied.

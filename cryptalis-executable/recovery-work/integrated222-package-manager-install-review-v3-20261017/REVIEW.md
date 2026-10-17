# Actual V3 offline package-manager installation accepted

Decision: ACCEPTED_ACTUAL_OFFLINE_INSTALL. This reviews the completed root-selected operation, not a proposed or repeated installation. The separately selected generated-launcher smoke may use this concrete prerequisite; it has not yet run.

## Bound operation and results

Packet: recovery-work/integrated222-package-manager-smoke-v3-20261017, PACKET.sha256 f72906f313f765c2171576e29eaec114b7fbb2bf8250c5868b4f4d6746c424aa. Source review: integrated222-package-manager-smoke-review-v3-20261017/REVIEW.md, 4467 bytes, d88097a8b70ae8c1828a868a0efc16531294f7c1a410c7357b0154ecb862823e.

Root capture: persistence-recovery-20261013/integrated222-offline-install-v3-20261017-1547. Root controller and after-check exits are both 0. Guard reports PASS_GUARDED_OFFLINE_INSTALL_PENDING_TERMINAL_REVIEW; child exit 0, reason null, leader reaped, no signals or cleanup errors, empty child stdout/stderr, cold bytecode prefix absent. The pending-review status is resolved here only for the installation scope.

Actual recorded uv command exits 0. It uses the admitted Python, fresh target, --no-deps, --no-index, --no-build, --no-compile-bytecode, --link-mode copy, --offline, --no-config, --no-cache, --no-python-downloads, and --no-installer-metadata against the accepted 141600-byte wheel SHA256 898e2548a0943d3d718aec7e2c2346d434b3131ef68c1cfe243ae9b7d8a390c8. uv stderr reports one local Cryptalis 0.1.0 package installed. This is actual package-manager target installation evidence.

## Independent output audit

The reviewer enumerated metadata first and established the complete exact file and directory namespace before reading admitted bodies. There are exactly 50 regular single-link leaves with 50 distinct inode identities: 47 unchanged non-RECORD wheel payloads, rewritten RECORD, generated bin/cryptalis, and empty .lock. All 50 current sizes and SHA256 values equal the precomputed map and both installer receipt snapshots. No unexpected metadata, bytecode, dependency, or hidden leaf exists in the target. In particular INSTALLER, REQUESTED, direct_url.json, uv_cache.json and uv_build.json are absent; no forbidden metadata body was read or enrolled.

The 355-byte launcher equals the precomputed source byte-for-byte, SHA256 3b5b041d24add9b5942ca18bf162ca74a75e793a3844387580790c04f868ae2b, mode 0755. The 4217-byte RECORD equals the precomputed CSV, SHA256 24b6c936745536c81f3047dfe2698cd7c1a88eb613fd1e64f63d3e739acd3c8e. Independent CSV reconciliation confirms exactly 49 unique rows: 48 correct URL-safe SHA256/size entries and the empty RECORD self-entry. .lock is excluded from RECORD and has zero bytes. The 47 original payload hashes agree with the accepted wheel map.

## Input and failure preservation

All 295 static plus three dynamic inputs were independently metadata-admitted and rehashed. Their current seven-field metadata equals the recorded before metadata; every expected hash matches. All 298 guard after entries report both metadata and byte equality. This includes the original patch, complete 222-source candidate, accepted artifacts, tools, source review, V2 controls, failure receipts and safe logs. The V2 installation remains exit 2 with target absent, and its failure review remains pinned. V3 omits the redundant UV_COMPILE_BYTECODE environment key while retaining the explicit no-compile flag; this result does not establish the internal cause of the earlier option conflict.

## Receipt pins and limits

- guard/install/run/terminal.json: 137615 bytes, b3e9aed21567b040467cc3830904a37d067f42fd2603402f9cdcb89a38b937d7.
- run/INSTALL_RECEIPT.json: 37347 bytes, 79cc27e51eda9fb101d8aaacd0440376c0442625f735409fe350b2fe061ccbb8.
- run/install.stderr: 396 bytes, 88f26680023b7be3cabb177143030b496f78082a46feb46ed2c38f71c01e6bc3.
- run/install.stdout: zero bytes, standard SHA256 of empty content.

CHECKS.json and the reviewer-owned data-only audit.py retain the independent reconciliation. No installer, target module, launcher, test, build, database, or Git operation was executed by this review. Existing-host interpreter/native trust remains explicit; descendants_verified_absent remains false. No global descendant absence, shebang portability, dependency installation, runtime correctness, production readiness or publication approval is claimed. Launcher execution remains a separate root selection after binding this review.

Diagnostic note: an initial lookup guessed controller.exit/after.exit; these names were absent. The actual listed exit.txt and after-exit.txt were then used; this was a filename diagnostic, not an access denial.

# S25 full-source remote restore verifier: source review

Status: SOURCE_REVIEW_COMPLETE; NOT_EXECUTED.

Read the complete prepared script and reconciled its literal schema names, paths, hashes, counts and bounds against the pinned metadata. No blocking defect found. A draft allowlist-format label was corrected during source review before the final hash below. No version of this script was executed by this reviewer.

Script: `s25-full-source-remote-restore-v1.py`

SHA-256: `b3180b52bae93905506662b9c4ef33743559381fd64d25541cf6b50d14437beb`

Exact future command, only after coordinator authentication of actual remote readbacks and their commit/transport:

`python -I -S /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/reviewer-notes/s25-full-recovery-independent-20261014/s25-full-source-remote-restore-v1.py`

## Input identity

`P` is `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013`.

- Local split manifest: `P/s25-full-source-parts/MANIFEST.json`, 3,053 bytes, SHA-256 `2934b8cde031cbae2daf4eed1efd0ca00a6a7cc2bb265d34240d64b60d2ff61e`.
- Remote readback inputs: `P/s25-full-source-remote-parts/part-01.bin` through `part-18.bin`; 17 parts of 96,000 bytes and final part 94,604 bytes. Every part SHA-256 is bound by the manifest.
- Archive: 1,726,604 bytes, SHA-256 `8afcee82e8ac3c22a527c8dca7fd3e8a159c646e5b3cdb89a23d5e780d2e81fd`.
- Payload manifest: 173,695 bytes, SHA-256 `71b42d138f105ca6b8b106004d3a4d6da27de9f80746f8a91ecf9045d5fe817d`.
- Allowlist: `2bca812ecc65dbba8e24f4ec1a5a3ca2dbe71c915034084ca4dc76b686ea07c9`.
- Freeze: `61171aa74ff9c51ad08087813b96c84b92560ccc6d7332bbcffa12b09bed83f3`.
- Reconstruction plan: `486a364dbe3edcad217b99236b46b3b91c534dccdfb41e65f9b9eb8a4b6342d9`.
- Complete source manifest: `3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703`.

## Enforced guarantees

Uses standard-library imports and explicit exceptions; no assertions, subprocesses, dynamic imports/evaluators, network, database, test, build, install or Git operations. Isolated interpreter flags avoid project-path and site-startup imports.

All input reads are bounded regular files, rejecting symlink ancestors and final symlinks. The exact joined archive size/hash is checked before bounded decoding. Xz output is capped at 32,000,000 bytes and requires one complete stream. Tar parsing enforces canonical unique regular non-sparse names, reviewed metadata, count/byte bounds and zero tail padding without `extract` or `extractall`.

Exactly 498 members, 497 payload entries and 486 selected inputs must match. Member bytes total 18,413,730; manifested payload bytes total 18,240,035; selected-input bytes total 17,996,449. Maximum member size is 2,486,588. Exact allowlist/metadata closure, every payload size/hash and all complete source identities are checked before output creation. Source routing is explicitly `s25-source/` from the reviewed clean-source root.

Both extraction and source reconstruction are exclusive new roots. Every output uses exclusive no-follow file creation, mode 0600, with directory mode 0700. Every write is read back. Final verification checks exact files, exact directories, bytes, and nonexecutable regular-file types in both trees. The complete 216-file source must total 4,404,370 bytes. The archive is read back again; only afterward is the success receipt exclusively written and read back.

## Fresh output paths

- `P/s25-full-source-remote-reconstructed.tar.xz`
- `P/s25-full-source-remote-fresh-extraction/`
- `P/s25-full-source-remote-source-reconstruction/` containing the exact 216 relative source paths directly
- `P/s25-full-source-remote-restore.json`

Existing/interrupted output causes refusal, never silent reuse, removal or overwrite. The script assumes a controlled workspace without hostile concurrent directory replacement; it does not claim adversarial filesystem isolation or crash durability. It does not authenticate remote commits or grant publication authority.

The exact archive identity binds the independently reviewed distributions and synthetic fixtures. This restore verifier does not rerun tests, nested semantic audits or sensitive scans. Its receipt preserves seven unresolved failures, separate subtest accounting, UNKNOWN gates, no promotion, and the source/packaging snapshot's no-installed/no-observer limits. Complete source-byte reconstruction does not establish a dependency/runtime/database or standalone 1,201-pin qualification environment.

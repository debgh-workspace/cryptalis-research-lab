# Independent terminal audit: async cleanup packaging

Date: 2026-10-15 UTC.

## Verdict and exact artifact identities

**ACCEPT_BOUNDED_ASYNC_CLEANUP_PACKAGING.** The actual bounded packaging result satisfies the scoped packaging requirements. This accepts data-only artifact evidence, not installation, installed runtime, release or production readiness. Any subsequent installer packet still needs final safe source/input closure, exact source/command review and coordinator authorization.

Packet root: `experiments/async-cleanup-release-plan-20261015` under `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

- Both `run/sdist-1/cryptalis-0.1.0.tar.gz` and `run/sdist-2/cryptalis-0.1.0.tar.gz`: **f921da5830bcb3b0c7befb10e05f23346b2ab874c487175217be4a5e752706f7**, 149820 bytes each; independently byte-identical.
- Both `run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl` and `run/roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl`: **77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b**, 139308 bytes each; independently byte-identical.
- Actual S25 baseline sdist remains `4800ce1a8e21685d063daf84882e36885759b2b30bcd3c3ad43c6a688b2299ba`, 149364 bytes.
- Actual S25 baseline wheel remains `42150bab589fcb80083dafb8bd34186c5040776950fa1f5b04b11a43c1e3b36c`, 138881 bytes.

Complete archive inventories, sizes and member digests are recorded in `DATA_AUDIT.json`, SHA256 **ce06b28274305dd73dfe52d406c22cf2864ae2a410c604fee82c4685d9edbcb0**. The independent data-only audit implementation is retained as `audit_data_only.py`; it does not execute or import product or packet code.

## Immutable inputs and complete sources

Independently matched the supplied anchors:

- `PACKET.sha256`: `9b1a4b71f6f81f99ba8d8e67d020b45ed302eb410d023468660cd1168e3945e1`.
- `BUILD_CLEARANCE.sha256`: `7008da1de17172aa71fc9c42062117aab1fda557104b43a36d3085723082fbc4`.
- Source/command review: `7af2a312e23f6cd27d199eab64f873565d8c39c0540d13f26a95bb7f11338bc5`.
- Candidate source manifest: `4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649`.

All 279 sealed packet files currently match their hashes and exact PACKET_FILES membership. The non-output packet contains exactly these 279 files, PACKET.sha256 and the additive BUILD_CLEARANCE.sha256, with no other regular member or symlink. All four clearance review files currently match their listed hashes. Their source-runtime acceptance was supplied by the coordinator; this packaging audit does not re-audit those runtime executions.

The original candidate, clean packet source, source-1 and source-2 each have the exact complete 217-file source name/hash set. Original S25 has its exact complete 216-file set. The only source change is `src/cryptalis/sqlalchemy.py`; the only addition is `tests/test_sqlalchemy_async_exit_double_failure.py`. No source removal or other source/configuration/dependency/test change exists. Candidate and baseline cache directories were excluded at their metadata boundaries without traversal or payload reads. The three clean copies contain no excluded cache directories. Current source sets and anchors were checked again at the end of the independent audit.

## Archive, module and RECORD checks

Every archive pathname component, final regular-file type and bounded artifact size was admitted before its bytes were read. For each archive, complete member names, types, sizes and attributes were admitted before reading member payloads. This included both candidate sdists, both candidate wheels and the exact S25 comparison archives.

Each sdist has exactly **47 unique regular files and six directories**, 53 entries total. All names are safe relative names within `cryptalis-0.1.0`, with no duplicate, traversal, absolute name, symlink, hardlink, sparse or special member. File modes are 0644, directories 0755, timestamps zero, numeric owner/group zero, owner/group names empty, link names empty, and PAX headers empty. All extracted payload sizes are consistent with headers. Candidate uncompressed payload size is 580738 bytes.

Each wheel has exactly **46 unique payload files and six directories**, 52 entries total. All names are safe, with no duplicate or path escape. Every ZIP member uses Unix regular-file 0100644 or directory 040755 attributes, zero lower attributes, UTF-8-only flags 2048, no encryption, empty extra/comment fields, and timestamp 1980-01-01 00:00:00. Files use deflate and directories are empty/stored. Candidate uncompressed payload size is 466467 bytes. CRC and actual member-size checks succeed through the archive reader.

The exact 47-file extracted sdist tree and its complete directory set match the admitted sdist contents after roundtrip building, with no link, extra or altered payload.

All **41 runtime modules** match the complete candidate source, both sdist payloads and both wheel payloads. RECORD has exactly **46 unique rows**, exactly the wheel payload name set, **45 valid SHA256/size entries**, and an empty digest and size for its own row. The LICENSE matches source/sdist/wheel, README matches source/sdist, PKG-INFO matches wheel METADATA, and uv.lock matches the unchanged hash `faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e`. `pyproject.toml.orig` is byte-identical to source configuration; normalized pyproject configuration is semantically identical under TOML parsing.

Relative to the actual S25 archives, the inventories are unchanged. The only changed sdist member is `cryptalis-0.1.0/src/cryptalis/sqlalchemy.py`; the only changed wheel members are `cryptalis/sqlalchemy.py` and `cryptalis-0.1.0.dist-info/RECORD`. All other payload bytes match.

## Actual terminal, bounds and integrity evidence

The coordinator supplied terminal session 13628, chunk 54fd07, exit 0 at 2026-10-15T01:00:07Z. The independently read root exit file is exactly `0\n`. Root entry log and interpreter-admission receipt hashes are retained in DATA_AUDIT.json; the admission receipt records metadata-only resolution of the known python3 alias to the fixed regular python3.12 target before launch. The audit did not rerun that entry or independently re-read interpreter/uv executable payloads.

`parent-results/parent-receipt.json`, SHA256 **c6049d18eddde3a5b57ed4418b3cb5eefd6a57c34b21d45579035b928f7cdeed**, reports PASS_BOUNDED_PACKAGING. Its exact child is `/bin/bash` with the reviewed `run-after-review.sh`. Child exit is 0, reason null, leader reaped true, group signals empty and cleanup errors empty. Parent errors are empty and prior_artifacts_preserved is true.

The captured streams independently match their recorded UTF-8 byte lengths and SHA256 values:

- stdout: 100410 bytes; `1457aa17253c9f5ceb3637dadf200229dbc7f74ccc8573bc9fbb28a53c9f3d55`.
- stderr: zero bytes; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The configured child deadline is 120 seconds; each captured stream cap is 2097152 bytes; inherited regular-file cap is 8388608 bytes. No timeout, truncation, stream-cap or signal event is reported. All specifically admitted output artifacts/logs and source-copy files are below the per-file bound. The parent original file-size limits were [-1,-1] and restoration is explicitly true.

Every pre-run and final integrity group passes with no errors and the exact expected manifest/count: outer frozen 3, frozen inputs 534, original S25 216, clean derivative 217, candidate 217. The four separate post-check logs have exact corresponding name sets, line counts and only OK statuses. Current packet, source and archive hashes were independently rechecked; historical pre/post checks of the whole 534-file set remain bounded launcher evidence, not a second independent executable-payload audit.

The parent receipt's fixed-constant scrubbed environment exactly matches the reviewed declaration. It is not a live environment dump. Both source/roundtrip builds and all helper/version steps have empty stderr. Expected direct output-directory and named safe-log membership is exact. Cache/home/tmp subtrees were not opened or read.

## Negative controls and remaining limits

`run/verification.json`, SHA256 `1abe2c52a9fc32f8102339fea0735d773a0ba55f0cbd456a078bfa473e4240d9`, records PASS_SCOPED_PACKAGING and successful rejection of missing_lock and altered_lock. The exact executed verifier identity is `b893837e26741a51510e2c9087f0f521c3bcc7847d36ac708ec9ddb0be36393d`. This audit inspected its pinned implementation and earlier bounded execution evidence. It **did not independently rerun** either control or execute any packet helper.

`wall_seconds: 120` is a configured bound, **not measured elapsed execution time**. Measured elapsed time is not recorded. `descendants_verified_absent` remains false: leader reap does not prove every descendant is absent. These cooperative per-child/per-stream/per-file bounds are not aggregate disk/memory quotas, hostile-code containment, network isolation or complete process-tree attestation.

Reproducibility here is byte equality across two same-host builds and the direct/sdist-roundtrip route with a pinned bundled builder. It is not independent-builder or fresh-host reproducibility; bundled Rust source-to-binary provenance and full dependency provenance remain unestablished.

No product/helper import or execution, installation, runtime test, database, network or Git operation occurred during this audit. No raw phase JSON, credentials, live environment dumps or cache payloads were read, hashed or copied. Existing corrected-source runtime failures and limitations remain unchanged. All seven broader gates remain UNKNOWN: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE.

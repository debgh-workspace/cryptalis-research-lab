# Independent Integrated221 main installed-payload review

Decision: ACCEPT_SCOPED_INTEGRATED221_MAIN_INSTALLED_PAYLOAD. Both actual copied installations are accepted as installed payloads only. Runtime selection still requires separately reviewed source commands, complete dependency/startup/origin freezes and coordinator selection. No product imports, tests, database command, installation or Git execution was performed by this reviewer.

## Actual artifact and receipts

Plan: candidate-integrated221-main-installed-plan-v1-20261015. Original cells: release-lab/s23-installed-20261014/{sa21,sa20}. Installed cells: release-lab/integrated221-installed-20261015/{sa21,sa20}.

The actual selected direct wheel has SHA256 dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6. Its exact 48 payload files and six directory entries were independently admitted, with complete 48-row wheel RECORD coverage and 47 matching hash/size entries. All 43 installed runtime modules in both cells exactly match the accepted 221-file source snapshot and wheel. Source manifest identity remains 202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520, transitively bound by the accepted source and installer anchors.

Root entry exit 0 and empty stderr, bounded parent PASS_BOUNDED_INSTALLATION with no errors, and child exit 0/leader reaped are confirmed. Both parent integrity phases passed all five groups (3 outer anchors, 2765 frozen inputs, 1658 leaves per original, 221 source files). The root pre-status receipt correctly records exit 3, exact “pg_ctl: no server running” output and empty stderr. No database command was executed by this reviewer. Both per-cell installer logs identify the selected actual wheel and have empty stdout. Bound receipts do not assert hostile isolation or all descendants absent; descendants_verified_absent remains false.

## Independent actual payload checks

- SA21: 1255 ordinary regular files and four exact links. Product RECORD has 53 rows, SHA256 f78ea6f5119e58e32cdf8684f95a56881e146ebb9d36ec6ae92c77cd0814a60d. All 1202 nonproduct regular files plus four links equal the original; 13 dependency RECORDs have 1186 validated rows.
- SA20: 1253 ordinary regular files and four exact links. Product RECORD has 53 rows, SHA256 ce569f236e22d214294c5092dc80d5cefbf22a7cff41c6a52dada01bc6eeaf26. All 1200 nonproduct regular files plus four links equal the original; 13 dependency RECORDs have 1184 validated rows.
- Every installed product file is covered by its RECORD; every nonself row has an independently verified SHA256 and size. Five exact generated entries are the CLI, INSTALLER, REQUESTED, direct_url.json and uv_cache.json. No arbitrary RECORD path is followed; normalized targets must be inside the already admitted finite inventory.
- Both exact CLI bodies use their respective new bin/python. Both interpreter symlinks resolve through the explicitly admitted target /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12, SHA256 fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7. The other python aliases and lib64 are exact. Existing other console scripts are retained bytes, not exercised.
- Both direct_url.json files identify the exact selected local wheel. Their archive_info objects are empty; wheel identity is independently pinned by the actual wheel hash, not claimed from that metadata. uv_cache.json exactly matches the wheel mtime with null commit/tags and empty env/directories; INSTALLER is uv and REQUESTED is empty.
- Dependency RECORD bytes are unchanged. No absent targets, cache rows or product overlap exist. Complete ordinary dependency bytes, including startup files, are in the index for fresh runtime freeze preparation.

## Cache, metadata and inode boundary

Every source/original/installed name, directory, regular type and link was metadata-admitted against the pinned finite policy before expanded payload hashing. All cache bodies were excluded: no .pyc/__pycache__ body read, hash, copy, deserialization or execution. The 402 SA21 and 404 SA20 historical cache leaves were checked by lstat metadata only. Fresh cells contain no cache files or cache directories.

Complete source and original metadata remains exactly equal to the pinned pre-install CURRENT_METADATA_ADMISSION snapshot, excluding atime: dev, inode, mode, link count, uid/gid, size, mtime and ctime. All 221 source and 2502 original ordinary hashes equal their frozen snapshots. A second metadata scan confirms no audit-window mutation.

Complete new-cell inode sets, including directories and symlink inodes, are disjoint from source and both originals (including cache inodes from metadata), and from each other. Original historical hardlinks are preserved as historical facts rather than rejected. All copy and installed inode-receipt memberships/pairs are reconciled, and every nonproduct retained copy inode remains current.

## Preserved reviewer incidents

1. Discovery command chunk d1998b rejected the explicit 5,309,243-byte CURRENT_METADATA_ADMISSION.json at an overly strict 5,000,000-byte size guard before reading it. The same exact JSON was subsequently admitted under 6,000,000 bytes; its pinned SHA256 matched. No file was modified.
2. First audit attempt exited 1 at pre_status_failed because the reviewer incorrectly demanded pg_ctl status exit 0. Actual expected quiescent status 3 was inspected and confirmed by the coordinator. Failure outputs and the original script remain at the reviewer root.
3. Attempt2 exited 1 at exact_wheel_members because it compared all archive entries to the payload-only binding. ZIP metadata confirmed 48 payload files plus six directory entries. Attempt3 corrects only that schema distinction, independently admits all six directories, and passes with exit 0. Both failed attempts are preserved, not relabeled as successes.

These are reviewer comparison failures, not hidden product/install failures. No actual installation failure was observed. This is not runtime, clean-host or release acceptance. Clean-host dependency provenance remains blocked by unavailable original dependency artifacts. The seven broad product gates remain UNKNOWN. Future runtime expectations remain 2684 ordinary PASS on SA21; 2638 PASS plus 46 exact version skips on SA20; 56 passing subtests separately; no historical seven-failure waiver.

## Canonical audit data

- attempt3/AUDIT_RESULT.json: SHA256 b5e37c111e770662e701c7c09b82fd645243d845007190d0e094b02d71ef00d5, 4011 bytes.
- attempt3/INSTALLED_PAYLOAD_INDEX.json: SHA256 1bd9d272498d391a545656bdf22fde0f1e5d632636177cb712c628788e121dfb, 1763754 bytes.
- attempt3/SOURCE_AND_ORIGINAL_INDEX.json: SHA256 3bece870d1877c2e0de9c051e2a892d92730637bad65539e6b796ca80f3f65ee, 2130491 bytes.
- attempt3/METADATA_ADMISSION.json: SHA256 f5d5ed73308581219f9a4f231a070a25f7ccc95d3f36d8cc09580fc6d0a4f02d, 2279318 bytes.
- attempt3/READ_INPUT_INDEX.json: SHA256 7daa8fcab2018a862a1d734ef492b5f5bb307c16e711f1882b1ec292049641d0, 1417060 bytes.
- attempt3/audit.py: SHA256 e78eb2361ed771d6cd00a76c257ed43143757987b58b8efbfd46c9f9adfbee88, 18486 bytes.
- attempt3/audit.stdout: SHA256 f08cc158f2a1395e74e198afd142c7680b720b0a3c2f2fb085098369252528d1, 3391 bytes.
- attempt3/audit.stderr: SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, 0 bytes.
- attempt3/audit.exit: SHA256 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa, 2 bytes.

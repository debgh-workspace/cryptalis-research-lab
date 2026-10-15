# Independent Integrated221 optional installed-payload review

Decision: ACCEPT_SCOPED_INTEGRATED221_OPTIONAL_INSTALLED_PAYLOAD, including the exact preexisting 41 missing noncache dependency-record targets. This is an installed-payload acceptance only; separately reviewed runtime commands and a fresh complete dependency/startup/origin freeze remain required. No product imports, tests, database commands, installation or Git execution occurred in this audit.

## Exact binding and actual receipts

Plan: candidate-integrated221-optional-installed-plan-v1-20261015. Original: release-lab/cp84-adoption/sqlmodel-wheel-venv. Actual new cell: release-lab/integrated221-sqlmodel-installed-20261015/sqlmodel. Source-command acceptance is OPTIONAL_REVIEW.md SHA256 744c987958c527904863acaf2ba12be7cc7582498f85d4bac33e3d7a83f9b5ad. All 16 exact local plan/source anchors match the pinned final preparation checks.

The selected wheel is the actual Integrated221 direct wheel SHA256 dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6. Its exact 48 payload files, six directory entries, 48-row RECORD and 47 payload hash/size entries were independently verified. The 43 installed runtime modules exactly equal the wheel and accepted source221 snapshot. The source manifest identity remains 202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520 through the accepted source and installer bindings.

Root entry and installer child both exited 0, stderr was empty, the child leader was reaped, and parent status is PASS_BOUNDED_INSTALLATION with no errors. Both parent integrity phases passed the four groups: 3 outer anchors, 5148 frozen inputs, 5900 original leaves and 221 source files. The root pre-status check is the expected exit 3 with exact “pg_ctl: no server running” output and empty stderr. The per-cell installer log identifies the selected wheel; stdout is empty. Bounds remain cooperative: descendants_verified_absent is false and no hostile-isolation claim is made.

## Independent actual installed payload

The cell has 4896 ordinary regular files and four exact aliases. All 4843 nonproduct regular files plus four aliases equal the original. The complete installed product RECORD contains exactly 53 rows, SHA256 4ea705448ea6eb260fd35017a38e2530cfb6a4919c6bb2100ad9f39dff054cbf. Every product file is included; every nonself row has verified hash and size. The exact generated entries are CLI, INSTALLER, REQUESTED, direct_url.json and uv_cache.json.

The exact CLI body uses the new cell’s bin/python and has SHA256 fa3c14c1b38a13eb628c4cb01b15c295d633652810e16e23a38801b69f97eff7. Its exact interpreter target is /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/apps/runtime/python/cpython-3.14.8-linux-x86_64-gnu/bin/python3.14, SHA256 60b250069178fb421d296805bcff5514acfe9ea9597f92413863db87ed6b4a18. Other python aliases and lib64 match the finite policy. No copied console script was exercised.

The direct_url.json URL identifies the selected wheel and its archive_info is empty. The actual wheel hash is independently verified rather than inferred from that metadata. uv_cache.json matches the wheel timestamp exactly, with null commit/tags and empty env/directories. INSTALLER is uv and REQUESTED is empty.

## Exact inherited dependency limitation

All 76 dependency RECORD files remain byte-identical to the original, and their 4868 rows were individually examined. Every present nonself target has a matching SHA256 and size. Exactly 41 record/path pairs are absent in both original and new cell; the exact set equals the pinned plan, is recorded in INSTALLED_PAYLOAD_INDEX.json, and each target was confirmed lexists=false. These are noncache targets and include console scripts, two startup hooks, man pages and a header. No new missing target, path escape, product overlap or cache row is accepted.

This preserves the accepted bounded same-host namespace. It does not prove every dependency distribution is intact or provide clean-host provenance. The two absent hooks remain absent, and no hook/script was restored or run. Runtime preparation must retain and freeze this exact startup namespace and all ordinary dependency bytes.

## Metadata, cache and cross-cell inodes

All names/types/directories/links and cache classifications were metadata-admitted before expanded payload reads. The 1010 original cache leaves were inspected through lstat metadata only; no cache body was read, hashed, copied, deserialized or executed. No new-cell cache leaf or cache directory exists.

Every original and source metadata entry equals the pinned pre-install CURRENT_METADATA_ADMISSION snapshot, excluding atime: device, inode, mode, nlink, uid/gid, size, mtime and ctime. All 4886 original ordinary hashes and 221 source hashes match their frozen snapshots. A final metadata-only rescan confirms no audit-window mutation.

The new optional inode set includes all regular files, directories and symlink inodes. It is disjoint from source and optional original, including original cache inode metadata. Additionally, all main original/new-cell metadata was rechecked against the independently accepted main index, without reading any main payload bodies, and the optional new inode set is disjoint from all four main original/new sets. CROSS_CELL_METADATA_CHECKS.json records that result. All copy/install receipt memberships and original/current inode pairs reconcile; every nonproduct retained-copy inode is unchanged.

The optional audit passed on its first execution. Its comparator derives from the corrected main data-only audit; the three main reviewer incidents remain preserved in the separately sealed main report. No optional product/installation/audit failure was hidden or reclassified.

## Limits and next gate

This is not runtime or release acceptance. Optional runtime expectation remains 38 ordinary PASS and 114 passing phases with native/recovery oracles. No runtime result is claimed here. The seven broad product gates remain UNKNOWN, and clean-host provenance remains blocked by unavailable original dependency artifacts. Fresh runtime preparation and independent source-command admission are still required.

## Canonical audit data

- AUDIT_RESULT.json: SHA256 99a39c8d72970ec49042a658b7935cd4de261264962e6997bea54f7a82b00e63, 2547 bytes.
- INSTALLED_PAYLOAD_INDEX.json: SHA256 b87945857714104a27e61f2816366bd0e7d56ac7ece2f867e1c1053e15188ff9, 3522866 bytes.
- SOURCE_AND_ORIGINAL_INDEX.json: SHA256 793cb5eb24683f408ffe0b6e5d081ca6f0a3aaed6e606ef2fa40c4b408b2c585, 3616931 bytes.
- METADATA_ADMISSION.json: SHA256 028923c1fc96c8f9fc6f83e77580fb5d89f6ac805b43010e89335175e595ae10, 4233569 bytes.
- CROSS_CELL_METADATA_CHECKS.json: SHA256 4dea35ed3f732ddbb9d98d8dd8d224f770703ca41e0537a14955f603b01f85d4, 1033 bytes.
- READ_INPUT_INDEX.json: SHA256 fc4c1690540059d36e6a75196d1388fb03c7e8fe022514b5aeb66191a43d51af, 2812258 bytes.
- audit.py: SHA256 677b9714eded1cd42cee1a9678189083271d07a6c7c722f8bd8ec02c354c0469, 20697 bytes.
- audit.stdout: SHA256 4f7d4acd0698315c8de359714d49265ce34aeadbe2d99d0b5a4c677b4850a1c5, 2211 bytes.
- audit.stderr: SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, 0 bytes.
- audit.exit: SHA256 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa, 2 bytes.

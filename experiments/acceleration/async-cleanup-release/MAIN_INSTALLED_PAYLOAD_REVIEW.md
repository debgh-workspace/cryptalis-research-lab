# Independent main installed-payload audit, V2

Date: 2026-10-15 UTC.

## Verdict and closure

**PASS_SCOPED_MAIN_INSTALLED_PAYLOAD_AUDIT_V2. This independent main installed-payload audit is CLOSED.**

The completed successful attempt4 evidence was recovered after the connection interruption. A new complete, metadata-first, data-only continuity recheck passes. Its canonical result is byte-identical to DATA_AUDIT.json, SHA256 6df29ab079a089fc43c8ff1ea8c056667abf3ee4f78dbd1d32e5ae57bcf95523. Its complete admitted tree metadata is also byte-identical to METADATA_ADMISSION_ATTEMPT4.json, SHA256 9adfc35c367d53b101e2c138226c3c5604e5aaf7d257844134e64440861e5dc7. No installation or runtime was repeated to obtain this closure.

This closes only the independent actual main installation/payload audit. Runtime clearance remains **false**. No optional installation, installed test, DB operation, release approval or production-readiness claim follows from this report. All seven broader gates remain **UNKNOWN**: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE.

## Exact scope and evidence binding

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

- Selected plan: candidate-async-cleanup-main-installed-plan-v2-20261015.
- Accepted independent source/command review: reviewer-notes/async-cleanup-install-plan-independent-20261015/SOURCE_COMMAND_REVIEW_V2.md, SHA256 d0a02a438740fa321dd8c5b2e2a325e5c9cfddda9c35e7df8e11d50e30cda8ef. This identity was rechecked after interruption.
- Actual new cells: release-lab/async-cleanup-installed-20261015/sa21 and /sa20.
- Exact coordinator capture: ../persistence-recovery-20261013/cleanup-main-install-v2-coordinator, containing only selection.json, entry.log and exit.txt.
- Selected outer entry: /bin/bash followed by the exact main V2 PROPOSED_COMMANDS.txt path. The selection records runtime_authorized=false and metadata_admitted_before_hash=true.
- Accepted wheel: experiments/async-cleanup-release-plan-20261015/run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl, SHA256 77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b.
- Clean source: 217 files, manifest SHA256 4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649.
- All 19 accepted main packet file hashes, all 3 outer-frozen targets and all 3565 frozen-input targets match their retained accepted identities.

Whole-tree dependency payload reads occurred only after complete exact name/type/link metadata admission for all three original environments, clean source and both installed cells. The fresh continuity recheck first required complete equality to the successful attempt4 metadata, then performed its payload checks. Individual regular reads use no-follow opens and repeat stable metadata checks. Both the original successful audit and continuity recheck finish with complete metadata rescans and payload rechecks. Access times are excluded because reads can change them.

## Actual installed payload results

Both SA21 and SA20 have exactly 1633 leaves: 1629 regular files and the four approved aliases. Directory counts including each root are 159 and 162 respectively. The admitted aliases and approved directory membership are unchanged from the accepted policy.

For each installed cell:

- All 41 Python modules are byte-identical across clean source, accepted wheel and installed payload.
- All 45 non-RECORD wheel payloads are installed byte-identically. The archive itself contains exactly 46 regular payloads plus six directory entries; wheel RECORD has exactly 46 unique rows, 45 valid SHA256/size rows and empty self fields.
- Installed RECORD has exactly 51 rows and covers every installed Cryptalis-owned regular file, with no unowned product leaf. All 50 non-self digest/size rows are correct and the RECORD self fields are empty.
- The five installer-added rows are the exact CLI path, INSTALLER, REQUESTED, direct_url.json and uv_cache.json. Every generated addition is covered by the installed RECORD.
- direct_url.json names the exact accepted local wheel URI. INSTALLER is exactly the two bytes b'uv', SHA256 e6184ce10e266134fdcfa401e8f1a95005bcd4f18d16b62b757323e2833fe9a9. REQUESTED is empty.
- The CLI is executable and uses the exact direct shebang naming its own new cell interpreter. Its complete body matches SHA256 1460564e897e2e3fd6b7eca4bc61ed0de11435625fcfd9f952fca4b7140a4a79. No arbitrary wrapper is accepted.
- All 1582 nonproduct dependency leaves retain exact original bytes or approved link targets. All 13 dependency RECORDs are confined to the cell and do not overlap Cryptalis ownership.
- The sole startup hook remains inherited _virtualenv.pth, with both that file and _virtualenv.py byte-identical to the original. No additional .pth, sitecustomize.py or usercustomize.py is admitted.

Installed RECORD SHA256 values:

- SA21: 1987625404915575d4feaac357f4c9590030778c81e5070c7ec4f5b7f6e15f9d.
- SA20: 23f23859b97005bdff9f789d0b5a0afa1c6a9fda108abeaaba99c4b5084b5f22.

Complete CLI SHA256 values:

- SA21: 4d85d59cf220c7bd79420485909510d9eb1f3cc5f020ad861aa2740a5cc9f857.
- SA20: eae0496da262c413ca08f10684abca409569eb6dabdcd61589133ed039b1f12d.

## Preservation and inode evidence

The original SA21, SA20 and optional SQLModel environments remain exactly 1658, 1658 and 5900 leaves, with 1654, 1654 and 5896 regular files. Every original payload/link and complete preserved metadata record matches its accepted historical baseline. The 217-file clean source has unchanged bytes and preserved preparation metadata fields; its complete current metadata also remains equal through successful attempt4 and the post-interruption recheck.

Both complete current installed regular-file inode sets are disjoint from each other, every complete original environment set, and clean source. All measured pairwise overlaps in the recorded six-tree matrix are zero. This comparison covers all regular dependency files, not only product modules or sampled files.

Each copy receipt contains 1654 original/copy pairs, and each installed receipt contains 1628 surviving original/installed pairs. Recorded original identities match the admitted originals; live surviving identities match current installed files; unchanged dependency identities reconcile to the copies. Historical intermediate copy inode records remain receipt evidence only because replaced files are no longer independently observable.

The optional output release-lab/async-cleanup-sqlmodel-installed-20261015 is still absent. There is therefore no optional installed cell whose cross-plan inode relationships can yet be accepted. That must be checked if a separately authorized optional installation later creates it. Quiescence relies on the coordinator reservation; this audit does not independently attest OS process absence.

## Actual bounded-parent and installer evidence

The exact fixed parent receipt reports PASS_BOUNDED_INSTALLATION and matches SHA256 73606faa1ba2a3aaccd660a1d70073977c1bf2cde0e37e4d3cf8d32236e5ad86. Child exit is 0, reason is null, errors and cleanup_errors are empty, and the child leader was reaped. The coordinator exit file is exactly 0 plus newline. The entry transcript matches the exact reviewed metadata-first admission and frozen-check sequence.

Both before and after receipt groups pass with exact checked counts: outer-frozen 3, frozen-inputs 3565, original SA21 1658, original SA20 1658, source 217. Parent file-size limits were restored. The child command and fixed scrubbed environment match the reviewed plan. Captured parent child stdout/stderr are empty with exact byte counts and SHA256 values. No raw environment dump was inspected.

The inner verification matches PASS_INSTALLED_PAYLOAD_ONLY, SHA256 901cb6c718277baed22dfa64208ac23a823b567c1f12f292d70395dc51679957, and agrees with the independently checked payload, RECORD, dependency and inode results. Both recorded uv commands match the exact offline/no-index/no-deps/no-cache/copy/reinstall route and exact accepted wheel and fresh interpreter paths. Installer stdout is empty; each stderr is exactly 603 bytes, records one uninstall and one install of cryptalis 0.1.0, and contains no error marker or NUL. Exact stdout/stderr hashes are retained in DATA_AUDIT.json.

The configured child bound is 120 seconds, with 2 MiB per captured stream and 64 MiB per inherited regular file. These are cooperative bounds, not aggregate disk/memory quotas, network isolation or hostile-code containment. wall_seconds is configured, not measured elapsed time. The actual receipt explicitly records descendants_verified_absent=false. Successful leader reap and empty cleanup errors do not establish descendant absence.

## Retained attempts and interruption recovery

All original reviewer source versions, admission snapshots, logs and exits remain present and unchanged:

1. Attempt 1 failed on a reviewer comparison between full directory metadata and the preparation baseline's deliberately type-only directory entries. No regular-file difference was found.
2. Attempt 2 failed on a reviewer assumption equating ZIP members with payload files. The accepted archive has 46 regular payloads plus six directory members.
3. Attempt 3 failed on the reviewer's newline assumption for INSTALLER. The actual value is exactly b'uv', which satisfies the accepted verifier's stripped uv identity. The accepted narrow correction records its raw hash and size.
4. Attempt 4 completed successfully with exit 0 and the anchored DATA_AUDIT.json result.

The first recovery preparation used tuple(stat), inadvertently including access time. Its own evidence read changed that excluded field, so preparation stopped before creating a checker or reading target inventories. The shell then reported the absent checker with exit 2. That failed continuity-recheck.log and continuity-recheck.exit remain intact. The documented second preparation uses the accepted metadata fields excluding access time. No target assertion or successful-result requirement was relaxed.

The post-interruption continuity checker is a retained, narrowly adapted copy of the reviewed standard-library data-only checker. It preserves all original comparisons and adds exact prior-tree metadata equality, complete old-evidence hash checks and byte-identical result requirements. It exits 0. CONTINUITY_INPUTS.json pins all 18 preexisting reviewer files and the two preserved recovery failure records. All 20 remain hash-identical after the recheck.

## Remaining gates and restrictions

This scoped audit cannot establish imported versions, installed runtime behavior, complete dependency archive provenance, natural DBAPI-fault equivalence, physical quarantine, provider custody, bundled builder/source provenance, fresh-host/cluster restore, external human review or production readiness. The source review's main pycparser/iniconfig metadata-versus-lock discrepancies remain unresolved. Seven historical main failures remain unresolved.

Any later installed runtime needs fresh final control packets, the complete clean-source archive and current payload/RECORD/audit bindings, immutable-input and per-stage clearances, a fresh corpus baseline, source/command review and separate coordinator selection. No runtime authorization is granted here.

Only permitted source/data reading, complete metadata admission, hashes and writes inside this existing reviewer directory occurred during recovery. No candidate or target helper execution/import, installation, tests, DB, network or Git operation occurred. No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json, secrets, environment dumps or unapproved cache/home/tmp payload was read, hashed or copied. Incidental parent home/tmp/cache directories were only admitted as fixed top-level directory entries and were not traversed.

## Evidence identities

- DATA_AUDIT.json: 6df29ab079a089fc43c8ff1ea8c056667abf3ee4f78dbd1d32e5ae57bcf95523.
- audit_data_only.py: 9092e3f776131222cfac60a85d4396d6489e77b4c481b3a0d3d2bd16fec4fc31.
- METADATA_ADMISSION_ATTEMPT4.json: 9adfc35c367d53b101e2c138226c3c5604e5aaf7d257844134e64440861e5dc7.
- attempt4.log: 122277937497eba750d65bf54ae5e5aa753f64a4f39d626c10a2b491ec4e8d1a.
- attempt4.exit: 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa.
- CONTINUITY_INPUTS.json: f1e9d461e6e58bcbfab2c0de85ba2303bd639f210f6cd0963646b99429d3658f.
- CONTINUITY_ATTEMPTS.md: 7eb9c3a47f80e6c20885d85eb173ca081831dc49c1dabd993fa569afd4b8208c.
- audit_continuity_data_only.py: c826f468d8c39cc148f5731bcab69e5aaf9b8d462d912350d6b0b6f727e45d5a.
- METADATA_ADMISSION_CONTINUITY.json: 9adfc35c367d53b101e2c138226c3c5604e5aaf7d257844134e64440861e5dc7.
- DATA_AUDIT_CONTINUITY.json: 6df29ab079a089fc43c8ff1ea8c056667abf3ee4f78dbd1d32e5ae57bcf95523.
- CONTINUITY_VERIFICATION.json: 93b1e3396ef8de5df698f823be374508f430010899d0db00eb39d6f3632035d8.
- continuity-recheck-attempt2.log: 7a8ff47483e4648120e0b61b7623190fe11cf4a3a24aa0c60c9d47e716d0ec32.
- continuity-recheck-attempt2.exit: 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa.

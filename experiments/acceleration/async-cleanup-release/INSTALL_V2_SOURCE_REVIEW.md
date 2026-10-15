# Independent V2 installed-environment source/command review

Date: 2026-10-15 UTC.

## Verdict and scope

**PASS_SCOPED_INSTALLER_SOURCE_COMMAND_REVIEW_V2; EXECUTION_HOLD.** The fresh V2 plans close the identified sequential local-read defect and satisfy this source/command review. This is not installation authorization, an installed-payload result, installed runtime clearance, release approval or production readiness. The coordinator must explicitly select one exact V2 outer entry after the launch conditions below; each actual bounded installation must stop for independent artifact/payload audit before any later runtime.

V1 remains **HOLD_LOCAL_READ_ADMISSION_GAP**. Its report SOURCE_COMMAND_REVIEW_V1_HOLD.md, SHA2568e270a10f71d8ffbada35efdb45661556424233937897925691396c718b719e4, and both complete held packet copies remain unchanged. Both live V1 plan file sets and every file hash were independently rechecked against the retained V1 audit and match. No failed reviewer attempt was erased or retroactively accepted.

No prepared helper, candidate/product, installer, test or import was executed by this review. No malicious-path reproduction was performed. Findings derive from source/AST inspection, independently implemented standard-library data checks, complete metadata admission and hashes.

## Exact accepted V2 source/command identities

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

Main plan: candidate-async-cleanup-main-installed-plan-v2-20261015
- outer-frozen.sha256: 899bf2d59b2c28c5a2308a34185005b5caf8585946698b65c28b0c1e6b0fdd09
- frozen-inputs.sha256: 65f9668e941f0b64c6344b3726a0c932249fff4b961405a071320a316be03124
- PATH_ADMISSION.json: cbf24f59d1380be9937311d6b05d698574df7535199e736b6dacc905f19d5f2a
- FROZEN_TARGETS.json: dae5b3975bc4cdaba158f87123abec30dca162e60cda0ab1e31616e23fd06177
- preflight.py: 141852db07cab0350ca15d0708357f034bb26f63addf488710c84e29ea2d38e2
- PROPOSED_COMMANDS.txt: f92304b4cc46e231e5f4eab4abc4b06159aa531b902e5b82f4740358943970ad
- Exact frozen target count: 3565; exact local file count: 19.

Optional plan: candidate-async-cleanup-optional-installed-plan-v2-20261015
- outer-frozen.sha256: 5a3eb516a74f2a1206fe4fdc710e58c01faa4e422963d6abd4ca020185730468
- frozen-inputs.sha256: 994a94405a2822e77e4aea7b487a309313be267d541899bca14ffa361b4df656
- PATH_ADMISSION.json: 4852efca76c61776ae3b4e5d227fa1036c12738c338525261df7b9830964bd59
- FROZEN_TARGETS.json: f93ca064d73c5f715e802a65b41fb75afd6790c253c45da4b59d1a9d46d2f3af
- preflight.py: 50039248ca7589391cf67e6f0fd5caefd7dcbdc641101bf4278d4ee69c021c72
- PROPOSED_COMMANDS.txt: c20c5209c379b808e1e8b6b7a259dcc3e70337c43fb1c1ca32879f9c2eb3630b
- Exact frozen target count: 6152; exact local file count: 18.

The final V2 handoff matches supplied hash328bc6fdc3a63aa03435f747d236c380775f636ceec5a184499268dffb6c91ab. V2_ANCHORS.json matches616745750d90c876b03b48463135b3a2a08c794d6eb8db55bae451d49833b742. The exact complete target sets, all target hashes, all three outer-frozen entries, no-link local file membership and final packet hashes pass independently. Eight final Python helper ASTs parse without execution.

The independent allowable sets derive from the complete admitted original inventories, the exact217 clean-source names, fixed tools, specific safe accepted reviews/artifacts and named preparation source/data. They were compared for exact equality before expanded reads. Relative to V1, after moving the local root to V2, each frozen set adds only READ_ADMISSION_AUDIT.md and the two named V2 preparation data/source files V1_BEFORE.json and prepare_v2_source_only.py. No raw phase output, credential/environment dump or unapproved cache was admitted by a manifest.

## Independent read-site and sequential failure-path review

The former blocking path is closed in both V2 outer helpers. Each original_inventory invocation has its own try block and, before reading either payload, calls admission_local_path for plan.json and the selected snapshot basename. A fixed per-plan local-name allowlist rejects every other name. admission_regular checks all directory components and requires a regular no-link leaf. Thus a previous frozen-manifest failure cannot be followed by an unadmitted plan/snapshot read in the next group or in finally. If either local admission fails, that group's exception handler reports failure without reading either file. All independent integrity groups still execute and fail closed individually.

The inner top-level PLAN read directly invokes admission_local_path. Every selected original snapshot and source-original.json is admitted before the first pre-try snapshot payload read. The later finally block uses already parsed snapshots and metadata-first admitted_inventory; it does not reopen an unguarded local plan/snapshot.

All remaining direct read sites were enumerated from the actual final ASTs and inspected:
- PATH_ADMISSION/FROZEN_TARGETS are regular admitted local paths, checked against embedded digest before JSON parsing.
- Each manifest is regular admitted; complete target-set equality and all target path/type checks precede expanded hashes.
- Each recursive inventory first validates every directory/file/link name and type against its exact pinned policy; individual regular reads repeat path/type admission.
- Wheel archive opening, wheel/uv hashes and clean source-module reads require exact frozen-target membership and regular-path admission.
- Copied old RECORD reads follow exact copied inventory equality and have their own regular-path admission.
- Installed payload/RECORD/direct_url/INSTALLER/CLI reads have their own regular-path check and are dominated by complete installed-tree admission. Exact accepted wheel and RECORD schemas constrain their names; the only RECORD traversal entry is the exact permitted CLI path confined to that cell.
- Supervisor source receives explicit regular-path admission and the original fixed supervisor hash before the future authorized compile/exec. It is not executed during this review.
- Receipt/log open calls use exclusive write modes and are not hidden input reads.

READ_SITES_V2.json preserves every inspected read/open source expression and line number. AST checks independently verify the outer two-admissions-before-either-read ordering and inner all-snapshot-admissions-before-read ordering. This establishes the reviewed cooperative sequential contract. It does not claim concurrent hostile-filesystem race resistance.

## Current originals, source, artifact and dependency boundaries

The exact roots remain the S23 original main SA21/SA20 environments and the cp84 original optional environment, never runtime-touched S25 cells. Before expanding original payloads, complete name/type/link admission was renewed for all three roots. Historical snapshots remain exactly1658/1658/5900 leaves, including only the four approved aliases per cell. Current original bytes and links match the preserved historical inventories. Complete metadata equality also holds before and after this review: device/inode, mode, link count, uid/gid, size, mtime_ns and ctime_ns for regular files, links and directories. Atime is excluded because reads may change it. Fresh before/final V2 checks both pass.

Main regular counts are1654 each; optional5896. Subdirectory counts are161/164/663. Original interpreter aliases resolve to the fixed Python3.12 or existing cpython3.14.8 targets, bin/python3 and version aliases point to python, and lib64 points to lib. The bootstrap python3 alias currently reads python3.12 and resolves to the exact regular target. Each pyvenv.cfg has include-system-site-packages=false.

Old product RECORD ownership remains exact and confined:50/50/43 rows, every target a Cryptalis-owned regular file within its original cell. Other dependency RECORDs (13/13/76) contain no overlapping Cryptalis-owned target. The only startup .pth is the inherited import _virtualenv hook; its reviewed helper patches distutils/setuptools installation paths. There is no sitecustomize/usercustomize addition. Existing telemetry/CLI dependencies and historical bytecode are unchanged opaque payload, not broader trust or execution-provenance evidence. No original cache outside the exact completely admitted historical inventory was read.

Installed metadata gives main SQLAlchemy2.1.3/2.0.51 and optional SQLAlchemy2.0.51, SQLModel0.0.47, psycopg3.3.6. Main pycparser3.11/iniconfig2.3.1 versus lock3.0/2.3.0 remains unresolved; optional metadata has3.0/2.3.0. No imported-version check or complete dependency archive provenance is claimed.

The clean source remains exactly217 files, manifest4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649. Complete current source names, hashes and metadata match. The accepted packaging review275f4e0bbe4b9ce74e5b285393a499c5496f5af9edc9cb77c330fa630d137144 and source-review closure remain bound. Current wheel bytes match77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b. Independent data checks again confirm46 payloads,46 exact unique RECORD rows,45 valid SHA256/size rows, empty self fields and41 modules equal to clean source. The only entry point is the unchanged cryptalis.cli:main console script. No installed output yet exists.

Quiescence remains explicit coordinator evidence, not independent OS process attestation. The preparer retained the coordinator's original reservation of these environments and reports renewed confirmation for V2. This review observed no original metadata/byte drift. Reconfirm exclusive quiescence immediately before any launch; do not run an original to probe it.

## Copy, installation, CLI and bounded-parent semantics

Both V2 plans remain root siblings, so HERE.parent routing is correct. Main output stays release-lab/async-cleanup-installed-20261015; optional stays release-lab/async-cleanup-sqlmodel-installed-20261015. Those roots, V2 parent-results/run, final main/optional runtime packets and all three runtime evidence roots are absent in the final check. Output/copy/receipt creation remains exclusive; lexists catches dangling destinations.

V2 preserves copytree(copy2, symlinks=True), complete copied byte/link equality, original/copy inode inequality, product-only old uninstall ownership and the exact pinned uv argv:

UV --no-config pip install --offline --no-index --no-deps --no-cache --link-mode copy --reinstall-package cryptalis --python EXACT_NEW_CELL/bin/python ACCEPTED_WHEEL

There is no dependency resolution/download, alternate backend, original-cell installation, credential/DB creation or test in this route. Both cell SITE constants remain correct:lib/python3.12/site-packages main andlib/python3.14/site-packages optional. Activation and copied dependency console scripts remain prohibited routes because their historical shebangs persist.

Post-install admission permits exactly unchanged original nonproduct files, the46 wheel rows and INSTALLER, REQUESTED, direct_url.json, optional uv_cache.json and CLI additions, plus only approved aliases/directories. Exact nonproduct bytes/links,41 source/wheel modules,45 hashed payloads, installed RECORD coverage/hash/size, local wheel URI and uv installer identity remain checked. Installed RECORD has50 or51 rows according to the actual optional uv_cache addition; no universal51-row assumption is introduced.

The optional interpreter pathname is126 characters. Exact CLI body and all three permitted header assignments are AST-identical to reviewed V1. Body SHA256 is1460564e897e2e3fd6b7eca4bc61ed0de11435625fcfd9f952fca4b7140a4a79 and matches all actual original CLI bodies. Accepted headers are only the exact fresh interpreter direct shebang or the fixed /bin/sh exec trampoline with the exact interpreter, "$0" and "$@", with the interpreter unquoted or single-quoted. Arbitrary wrapper code fails. This does not predict which form uv will generate; the actual launcher must be inspected after installation without executing it.

The supervisor is byte-identical to V1/templates. Limits remain120 seconds per child,2MiB per captured stream and64MiB per inherited regular file, with WNOWAIT leader observation, exceptional group kill before leader reap, bounded reap, cleanup reporting, parent file-limit restoration and all outer finally integrity groups. These are cooperative per-child/per-stream/per-file bounds, not aggregate disk/memory quotas, network isolation, hostile-code containment or complete descendant proof. Successful leader reap does not establish descendant absence. Initial setup failures before try, catastrophic interpreter termination or receipt-write failure can prevent a terminal receipt; missing/incomplete evidence means HOLD. Configured wall_seconds is not measured elapsed time.

## Mandatory launch and later audit gates

1. Reconfirm quiescent originals and absent fresh destinations. Before the first checksum, independently admit the bootstrap executable pathname/components, exact python3 -> python3.12 alias/regular target and exact no-link V2 preflight/manifest files. Do not use a manifest to authorize its own expansion.
2. Externally match both selected-plan frozen-manifest digests and exact command/preflight identities listed above. The preflight embeds admission/target-table identities; it does not embed the outer-frozen or frozen-inputs digest. Merely running preflight is not a substitute for this external binding.
3. Coordinator must explicitly select the exact corresponding PROPOSED_COMMANDS.txt entry. It changes to that V2 root, checks fixed Python/preflight hashes, invokes the metadata-first preflight with -I -B, checks outer-frozen and launches one V2 outer. Never invoke V1, an inner helper or uv directly. This report alone grants no execution permission.
4. Stop after each separately selected installer for independent actual parent/result/payload audit. Require PASS_BOUNDED_INSTALLATION, child exit0/null reason, empty errors/cleanup errors, leader reaped, all before/final groups, parent file-limit restoration, exact logs and no truncation. Require actual original preservation against the retained metadata/payload baselines; inspect copies, all modules and complete RECORDs, CLI and generated additions.
5. Independently measure complete current regular inode sets across all three originals, all three fresh cells and clean source before runtime. Child checks are within its selected plan; they do not by themselves prove cross-plan optional/main disjointness or disjointness from clean source. Intermediate copy inode records remain receipt evidence only.
6. Installed runtime remains pending. New final control packets require complete217-file archives, actual payload/RECORD/audit bindings, immutable input and per-stage clearances, fresh26-file corpus baseline, source/command review and separate coordinator selection. Main SA21 then SA20 and optional38 retain the documented order and accepted-result gates. Mandatory installed-candidate routing and actual origin checks cannot be replaced by this data audit.

Seven historical main failures remain unresolved. All seven broader gates remain UNKNOWN:G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE. Natural DBAPI-fault equivalence, physical quarantine, provider custody, bundled builder/source provenance, complete dependency archive provenance, fresh-host/cluster restore, external human review and production readiness remain unestablished.

## Retained independent evidence and method

- PACKET_DATA_AUDIT_V2.json:22640e1c5960a193434ecc4a040a3f21029c390ae97d2edd954b45d628351cdd
- ORIGINALS_V2_BEFORE.json:da6e1365f2ea8553a84ce851f1f8dedd89a3dbdf1c006fdd6c5cd5d68caea67b
- FINAL_RECHECK_V2.json:3a62b850c6f816438011ded5abec918af4d8f6435b91c156a39cecf75351fbde
- FINAL_PACKET_RECHECK_V2.json:f178c0ebd7b4e4b2644b73d46ee1d9bd71c87f44e4972165565f6bb19eee3844
- READ_SITES_V2.json:e7c72231167e694610ee06f01635112af55fbcae439602037a1d2d1d1e1badfc
- ORIGINALS_DATA_AUDIT.json:d16776080fbe65848739b69f423a03c8009f377f5efa9b62234a8bc626a3ef30 retains the full independent before metadata and exact original inventory.

Only metadata inspection, permitted source/data reads, hashes, source AST parsing and reviewer-directory writes occurred. Reviewer tooling used standard libraries; no product or prepared helper was imported/executed. No install/test/DB/network/Git operation occurred. Raw tests.json/readiness.json/package-origin.json/postgres-start.json/postgres-stop.json, secrets/environment dumps and unapproved caches were not read, hashed or copied. Output is confined to reviewer-notes/async-cleanup-install-plan-independent-20261015.

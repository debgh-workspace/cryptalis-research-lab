# Independent V1 installed-environment source/command review

Date: 2026-10-15 UTC.

## Verdict

**HOLD_LOCAL_READ_ADMISSION_GAP; NO_INSTALLATION_OR_RUNTIME_CLEARANCE.** The final V1 data/identity checks otherwise pass, but an independent finally/integrity branch can read a local file after a preceding guard rejected its pathname/type. This is an actual sequential source-contract defect. It was identified without executing a candidate/helper, installer or test. The coordinator requested separately named V2 plans with a narrow fix; V1 remains held and unchanged.

V1 roots under /workspace/scratch/cb28ee9f5f4a/cryptalis-executable:
- candidate-async-cleanup-main-installed-plan-20261015
- candidate-async-cleanup-optional-installed-plan-20261015

The initial issue report is HOLD_ATTEMPT_1.md, SHA256 fa9bdc38e02d90474c590ecbc449408a80868cf40ace3f972f773de24bdc565d. Complete exact local V1 packets are preserved as held-main-seal1 (18 files) and held-optional-seal1 (17 files). No previous failed audit implementation or evidence was overwritten. ATTEMPTS.md records the two harmless reviewer formatting assumptions, their stopped checks and preserved implementations.

## Blocking sequential failure path

outer.integrity() deliberately evaluates every group, including after verify_manifest returns a failed result. Its frozen-manifest verification admits all target paths before expanded target reads. However, original_inventory next calls json.loads((HERE/'plan.json').read_text()) and reads the selected HERE/(name+'-original.json') before locally admitting either path. If frozen-manifest admission rejected either local path because it is a symlink or special file, a subsequent original_inventory in the same integrity call still reads it. The finally integrity call repeats the same possibility. An earlier failed group does not dominate or prevent these reads.

The fix must independently admit each exact local plan and snapshot before reading in every original_inventory invocation. The inner helper also reads top-level PLAN and pre-try snapshots without their own local path admission; although a successful outer normally gates launching it, those sites should meet the same local contract. Review the final source of every analogous read and each independent cleanup/postcheck. No hostile concurrent-race proof, imported execution or filesystem mutation test is required or was performed.

## Exact V1 seals and immutable input findings

The preparer's final handoff hash is ea3183ab25105ec0c070586c4de8f76f1e69d68535438638e3df71b88c87a08a; FINAL_HANDOFF_ANCHORS.json is fdeaa9bad35e18fcdf9a63a330897abea21c633bc09db8996639def3fad604d4. Both match the supplied final immutable identities. Earlier mutable preparation was not treated as final.

Main:
- outer-frozen.sha256: 7c835cb33a0c042e8cdcc9906610c63bcb6d3d87a545b17ceb674726a08c6abf
- frozen-inputs.sha256: 2675cc5d80069e164f88804d861c713a4ba8eaf8fc33e402ce9b448e476b2acc; exactly 3562 targets
- PATH_ADMISSION.json: 17fce4d1537e89c2f0421792970ed83b80d5c4362824fa8896ea7a7f0a1ded3e
- FROZEN_TARGETS.json: 575a835ddde846a4013db8e1dafe1ea5dad4347a670464a6b02882e4094cd107
- preflight.py: cb8b43d418084855b018e76d26c2ff869d1bd0f25ad1321269e8c28d35274efd
- PROPOSED_COMMANDS.txt: 38b323c0ce14a0c451075f97a3a3c7374cb380208f22cbb5566f3bcfb8818a7e

Optional:
- outer-frozen.sha256: 956594107488c8c539183bbdaf894c1f38ee34cdb421f422b2101372587f6eb9
- frozen-inputs.sha256: 2176c4ecaeb28a636d8e25311603c1eb4730f02ed0b204eda5b438625c582f8c; exactly 6149 targets
- PATH_ADMISSION.json: 83bc71d0be3dbbaefe9f1235d3155aa576faa45396ce08e46b5d83fbead187ec
- FROZEN_TARGETS.json: 1e3ed5c8dd0146dc27a092d57f634fa809e5bab3f17ca7450eee1b3f44b8fd5c
- preflight.py: 411270409a86c59ca7937d8d0d502fc2373ee7ffff6977ae8b6135756aea1cb1
- PROPOSED_COMMANDS.txt: 27d50e42a82fdfe050ca61ac15eb2fa23e5229e9f08fa29349b466b35ea25417

Every frozen target and hash matches, and all three outer-frozen targets match in each plan. Exact packet membership is 18/17 regular no-link files, with no extra member. The allowed target sets were independently constructed from specific reviewed source/documents/tools and metadata-admitted original inventories, then compared for exact equality before expansion. An arbitrary manifest was never treated as permission. All four Python helpers in each plan parse as source ASTs; neither plan helper was imported or executed.

The source is the exact 217-file clean release-packet tree, with complete name/hash equality to source manifest 4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649. It remained metadata/byte-identical through the static check. The accepted packaging review hash 275f4e0bbe4b9ce74e5b285393a499c5496f5af9edc9cb77c330fa630d137144 was independently matched. The accepted wheel is 77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b. The current wheel again matches that digest, has 46 payloads and 46 unique complete RECORD rows, 45 SHA256/size entries and empty self fields; all 41 runtime module bytes equal clean source. The only entry point is the existing cryptalis.cli:main console script. This is existing accepted artifact evidence, not a new installed result.

## Original environments, metadata, aliases, hooks and ownership

Complete original name/type/link admission of all three roots preceded any original payload expansion. Exact current byte/link inventories match the preserved S25 snapshot data:
- release-lab/s23-installed-20261014/sa21: 1658 leaves, 1654 regular files, four links; 161 subdirectories
- release-lab/s23-installed-20261014/sa20: 1658 leaves, 1654 regular files, four links; 164 subdirectories
- release-lab/cp84-adoption/sqlmodel-wheel-venv: 5900 leaves, 5896 regular files, four links; 663 subdirectories

No name, special-file, link or historical-byte drift was found. Full before/after regular/directory/link metadata also remains equal, including device, inode, mode, link count, uid/gid, size, mtime_ns and ctime_ns. Atime was not treated as preservation evidence because approved reads can affect it. The final independent recheck repeats complete set/type/link admission, payload equality and metadata equality for all three originals.

The exact four aliases per root are bin/python to its documented fixed external interpreter, bin/python3 and bin/python3.12 or bin/python3.14 to python, and lib64 to lib. The primary bootstrap alias is currently python3 -> python3.12, with the exact regular resolved target. No arbitrary interpreter substitution is admitted. Each pyvenv.cfg has include-system-site-packages=false. Metadata reports SQLAlchemy2.1.3/2.0.51 in main, and SQLAlchemy2.0.51, SQLModel0.0.47 and psycopg3.3.6 in optional. The optional interpreter target is the existing cpython-3.14.8 installation. These are metadata observations, not imported-version checks.

Only _virtualenv.pth is present as a startup hook in each environment, containing import _virtualenv (without a trailing newline). The admitted _virtualenv.py source patches distutils/setuptools installation paths and retains its existing finder. No sitecustomize/usercustomize hook appears. Existing optional telemetry/CLI libraries remain historical dependency payload; their presence/equality does not authorize executing them or establish a broad trust verdict. Historical bytecode was hashed only after complete historical admission and remains opaque payload, not executed-bytecode provenance.

Every old Cryptalis RECORD target is regular, inside its own cell and Cryptalis-owned: 50 rows in each main cell and 43 optional. Independent checks of all other dependency RECORD files (13/13/76) find no target overlapping Cryptalis-owned paths. No dependency-uninstall target was silently reclassified as product-owned.

Quiescence is coordinator-supplied evidence, not independently established OS process attestation. The exact quote retained in FINAL_HANDOFF says the S23 originals and cp84 optional environment are quiescent, no worker may execute them, DB tests remain coordinator-only, and conflicting execution will not start while admission/inventory work is active. Quiescence must be reconfirmed immediately before any later authorized launch.

## Reviewed installation route and still-pending evidence

Both plans are at root-sibling paths, so HERE.parent correctly denotes the project base. Only the original S23 main cells and cp84 optional original are copied; no runtime-touched S25 cell is selected. Output roots are the still-absent release-lab/async-cleanup-installed-20261015 and release-lab/async-cleanup-sqlmodel-installed-20261015. Both plans' parent-results/run and all final runtime packet/evidence destinations were absent. Existence checks use lexists; copy/output/receipt creation is exclusive.

The retained route uses copytree(copy2, symlinks=True), complete copied bytes/links, original/copy inode inequality and only the approved aliases. The uv argv is --no-config pip install --offline --no-index --no-deps --no-cache --link-mode copy --reinstall-package cryptalis --python EXACT_NEW_CELL/bin/python ACCEPTED_WHEEL. It resolves no dependencies, changes no original, and invokes no product CLI/test. Copied activation/dependency console scripts retain historical shebangs; only explicit new bin/python is permitted later.

Post-install metadata admission is independently derived from all unchanged original nonproduct entries, the exact 46 wheel payloads and permitted INSTALLER, REQUESTED, direct_url.json, optional uv_cache.json and CLI. Extra files/links/directories fail. All 41 modules, 45 hashed payloads, wheel/installed RECORD ownership/hash/size, local wheel URI and uv identity are checked. Installed RECORD permits exactly 50 or 51 rows depending on uv_cache presence. Complete final original/new/cross-new regular inode disjointness must be independently remeasured across all three future cells and clean source before runtime; the child proves only its own plan's current original/new and within-plan cross-new comparisons. Intermediate copy inode receipts are historical receipt evidence, not current identities.

The 126-character optional interpreter is handled by exact full CLI validation. The only accepted body has SHA2561460564e897e2e3fd6b7eca4bc61ed0de11435625fcfd9f952fca4b7140a4a79 and equals all three actual original launcher bodies. Prefix must be the exact fresh interpreter direct shebang, or a fixed /bin/sh exec trampoline using that exact interpreter, "$0" and "$@", either unquoted or single-quoted path. Other wrapper code is refused. No new CLI has yet been generated or executed; its actual post-install bytes remain an independent audit obligation.

The proposed command checks the fixed Python/preflight identities, runs only the metadata-first preflight, verifies outer-frozen and invokes the bounded outer. These V1 commands remain held. Independent external binding of both frozen manifest digests is required before any future entry: the preflight pins exact path/admission tables but does not itself embed the outer-frozen or frozen-inputs digest. Coordinator bootstrap metadata admission must precede the first executable/preflight checksum. Never run the inner or uv directly.

## Bounds, failure behavior and scope limits

The bounded supervisor is byte-identical to its reviewed template. It keeps a 120-second child deadline, 2MiB per captured stream, 64MiB inherited regular-file bound, WNOWAIT leader observation, group kill before reap on exceptional paths, bounded reap, cleanup reporting, parent file-limit restoration and all final integrity groups. These are cooperative per-child/per-stream/per-file bounds, not aggregate quotas, network isolation, hostile-code containment or proof of descendant absence. Setup before try/finally, catastrophic termination or receipt-write failure may prevent a receipt; missing/incomplete results are HOLD. No elapsed measurement or descendant proof is invented.

Actual bounded installer success, copied/installed payloads and independent installed audit do not exist. Neither metadata preparation nor a future installer result permits runtime. Final main/optional packets still need accepted installer audits, complete217-source archives, actual installed RECORD/module bindings, exact per-stage clearances, fresh corpus baseline, and independent final source/command review. Main must run SA21 then separately cleared SA20 with mandatory installed-candidate routing; optional38 remains separately gated after both main terminal results. Seven historical main failures and all seven UNKNOWN gates remain unchanged. Dependency lock drift, source-to-builder provenance, complete dependency archive provenance, natural fault equivalence, provider custody, physical quarantine, fresh-host restore and production readiness remain unresolved.

## Independent retained data

- ORIGINALS_DATA_AUDIT.json: d16776080fbe65848739b69f423a03c8009f377f5efa9b62234a8bc626a3ef30
- PACKET_DATA_AUDIT.json: 98965d29f2951567e531b9ea255ce6662c2b499b6ccabb4add3200dd49ee8a7d
- FINAL_RECHECK_V1.json: 8d84942f04f88f89a09cc72305c24812728ddac7ed26f311558943381956d0ad

Only safe source/data reads, metadata, SHA256 checks, source AST parsing and reviewer-directory writes occurred. No candidate/helper import or execution, installation, runtime test, database, network or Git action occurred. No forbidden raw phase JSON, credentials, secret/environment dump or unapproved cache payload was read, hashed or copied. The documented failure was found by source inspection; no malicious-path reproduction was performed.

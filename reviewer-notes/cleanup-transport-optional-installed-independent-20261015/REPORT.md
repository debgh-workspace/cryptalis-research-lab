# Independent Transport218 optional installed-payload audit

2026-10-15 UTC.

## Verdict

PASS_SCOPED_TRANSPORT218_OPTIONAL_INSTALLED_PAYLOAD_AUDIT_V2. Audit closed; runtime clearance remains false.

All live original/source/installed reads, final complete metadata rescans, payload rereads and frozen-input rehashes finished successfully before the coordinator was notified at approximately 06:16 UTC that the original reservation could release from this audit's perspective. Report preparation subsequently uses retained reviewer evidence only. Cooperative reservation and stable observations do not independently attest OS-wide quiescence or race resistance.

No target code, installer, tests, DB, imports, network, Git or live corpus were executed/read. Reviewer-written standard-library tooling only inspected data and wrote this reviewer directory. All seven gates remain UNKNOWN: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY, G-RELEASE.

## Exact bindings and method

Base B=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

- Plan: candidate-cleanup-transport-optional-installed-plan-v2-20261015.
- New optional cell: release-lab/cleanup-transport-sqlmodel-installed-20261015/sqlmodel.
- Source/command review: reviewer-notes/cleanup-transport-install-plan-independent-20261015/SOURCE_COMMAND_REVIEW_V2.md, SHA256 578aa50361e915d0d66ca15a1a599e5e2e06516833db99b6622b0f98b9031283.
- Main acceptance: reviewer-notes/cleanup-transport-main-installed-independent-20261015/REPORT.md, SHA256 ce7c60cab39482cb24e660a614c9b5d36bbc6c34b1a68467d269d7cc7463f8fc.
- Coordinator: sibling persistence-recovery-20261013/transport218-optional-install-v2-coordinator; exact seven-file capture, selected command vectors, preflight0/manifest0/outer0 and full fixed logs pass. Outer output is empty.
- Accepted wheel: SHA256 73c066adfce04d4efc3dd02c713e0d8ae0610497fb045ebb1484f54a8bb55e88.
- Clean source: 218 files, manifest SHA256 b8a8a6b00c597b63f4851defb74a2baa3dde8f3ff4c2e46d789699792600a204.
- All 18 local packet files, 3 outer targets and 6158 frozen-input targets pass.

The accepted cleanup217 optional checker was independently rebound to Transport218 plan/output/wheel/review identities and current coordinator captures. Its payload, ownership, RECORD, dependency and receipt assertions remain. Full source metadata is checked against the current accepted source review. Exact optional CLI matching is tightened to the actual quoted-shell form. The old path-length constant is replaced by measurement of the exact current path, rather than guessed rebinding. Full checker source and preparation are retained.

Complete name/type/link metadata admission for all three originals, clean source and all three installed cells precedes expanded payload hashing. All reads repeat regular-file/no-follow admission with stable descriptor metadata. Final complete rescans and payload rereads pass. Access times are excluded. Parent home/cache/tmp directory names were admitted but their contents were never traversed or read. Raw tests.json, readiness.json, package-origin.json, postgres-start.json, postgres-stop.json and postgres-start-stop.json were not read. Historical .pyc files and admitted inventory cache names are opaque copied bytes, never imported-execution evidence.

## Actual optional payload

The fresh optional cell contains 5896 leaves: 5892 regular files and four approved aliases; 661 directories including root.

- All 41 Python modules match exact source, accepted wheel and all three installed cells.
- Wheel membership is exactly 46 regular files plus six directories. All 46 unique RECORD rows cover it; 45 non-self hashes/sizes pass and self fields are empty.
- Optional installed RECORD contains 51 rows exactly covering every product-owned file; all 50 non-self SHA256/size fields pass. RECORD SHA256: 3c3d60b05366f9aa2c43ac80bf0970922a0a348553566a43866885d00d64b1b8.
- Installer additions are exact CLI, INSTALLER, REQUESTED, direct_url.json and uv_cache.json. INSTALLER is exactly b'uv'; REQUESTED is empty; direct_url points to the accepted local wheel URI.
- Full executable CLI matches the complete fixed body and quoted /bin/sh trampoline to its exact fresh bin/python, whose path has 130 characters. CLI SHA256: 20fd30217ea03ba37890ea06213c84397258cac416bf1f704839a2de31d7b048. Body SHA256: 1460564e897e2e3fd6b7eca4bc61ed0de11435625fcfd9f952fca4b7140a4a79.
- Exactly 5845 nonproduct dependency leaves retain original bytes or approved links. All 76 dependency RECORDs are cell-confined and do not overlap product ownership. The old product RECORD has its pinned 43-row ownership set.
- Sole startup hook is inherited _virtualenv.pth; it and _virtualenv.py remain unchanged. No additional startup hook or entry point is admitted.

Both main cells were fully rechecked, including modules, complete RECORD hashes/sizes, full direct CLI, dependencies and receipts. Their results exactly match accepted main audit evidence. Each still has 1633 leaves / 1629 regular files, 51 installed rows and 1582 unchanged nonproduct leaves.

## Preservation and inode disjointness

Original main cells each retain all 1658 leaves / 1654 regular files; original optional retains 5900 leaves / 5896 regular files. Complete metadata, bytes and aliases match accepted preserved baselines. All 218 source files and reviewed full metadata remain equal. Main installed metadata also remains identical to its accepted audit.

Complete current regular inode sets across three originals, three installed cells and clean source have zero overlap in all 21 measured pairs. Optional copy receipt covers all 5896 original/copy pairs; optional installed receipt covers 5884 surviving original/installed pairs and matches current identities. Main receipts also reconcile. Intermediate replaced-file copy identities are historical receipt evidence only. Current full-tree disjointness is independently measured, not inferred from those receipts.

## Parent and logs

Parent receipt SHA256 70b6448ec90a3086be934d9feadbc681ba5b2bf9bf62a8007eead9eea2ea1a50 reports PASS_BOUNDED_INSTALLATION. Child exit0, null reason, empty parent errors and cleanup errors, leader reaped, restored parent RLIMIT_FSIZE and exact empty captured stdout/stderr all pass. Exact before/after groups each contain outer3, frozen6158, optional-original5900 and source218. Scrubbed environment and inner command match the reviewed route.

Verification SHA256 653dfd30d46fc1b638101a0e4c301d0165f49854c21216bf9a13ef0182c8919d reports PASS_INSTALLED_PAYLOAD_ONLY and agrees with independently measured payload/dependency/receipt results. Exact uv argv has offline/no-index/no-deps/no-cache/copy/reinstall-package flags and names only the fresh interpreter and accepted wheel. Installer stdout is empty; stderr is 612 bytes, records one uninstall and install, and contains no error marker or NUL. Full log bytes/hashes are retained in DATA_AUDIT.json.

Configured bounds remain 120 seconds per child, 2 MiB per captured stream and 64 MiB per regular file. These do not establish aggregate resource quotas, network isolation or hostile-code containment. wall_seconds is configuration, not measured elapsed time. descendants_verified_absent is false. Completion was verified after a long tool gap; neither uninterrupted compute nor elapsed build time is inferred from that gap or filesystem timestamps.

## Attempts and residual scope

The first complete audit exited0. No audit assertion failed or was relaxed. The preparation completed without failure. The displayed checker comparison returned standard diff status1 for differences, not audit failure.

This audit does not authorize runtime, release or production use. Dependency provenance/lock drift, natural DBAPI-fault equivalence, physical quarantine, provider custody, independent fresh-host restore, external human security review and production readiness remain unestablished. Seven historical main failures remain unresolved. Fresh separately reviewed runtime packets, exact26-file corpus baseline, current installed bindings, immutable per-stage clearances and explicit main SA21 then SA20 then optional38 selections remain required.

## Evidence

- DATA_AUDIT.json: 2a6b77bf037bba44d344f245cb05a9b482d9eb6e2d8bab2f1faece611ae4ba9a
- audit_data_only.py: a80ab5641d16f2a3329d149f186f43b6acb1651b4a3c1f7add93dfa63ecce01d
- METADATA_ADMISSION.json: 72ed537808d2e40dba2b044ad0ac6fc54748e980025b1618de34fd277e226059
- attempt1.log: 17b71d61108a7adf23ddd6608718e1e2ee5b2acf3d97140c7df88f4bc22e0d8f
- attempt1.exit: 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa

# Independent optional installed payload audit, V2

Date: 2026-10-15 UTC.

## Verdict

**PASS_SCOPED_OPTIONAL_INSTALLED_PAYLOAD_AUDIT_V2.** The exact selected optional V2 offline installer completed, and this independent data-only audit accepts its on-disk copied/installed payload and bounded-parent evidence. All three original cells, both previously accepted installed main cells, and the clean source remain unchanged. This is not installed runtime acceptance, imported-module attestation, release approval, or production readiness. No runtime clearance is granted.

The coordinator explicitly reported terminal exit 0, immutable optional outputs and quiescence of every original/new cell before this reviewer read any optional output. Quiescence is coordinator evidence, not independent OS-process attestation. The reviewer executed only independent standard-library data checkers. No installer, prepared helper, product code, tests, database command, network request or Git operation was executed by this review.

Audit result: DATA_AUDIT.json, SHA256 d8ee23b4bbe45f1d7f472dbce5cbca24b3c6f7dd957c3e13fba7e38b1a166efb.

## Exact accepted inputs and selection

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

- Plan: candidate-async-cleanup-optional-installed-plan-v2-20261015.
- Actual installed cell: release-lab/async-cleanup-sqlmodel-installed-20261015/sqlmodel.
- Accepted source/command review: reviewer-notes/async-cleanup-install-plan-independent-20261015/SOURCE_COMMAND_REVIEW_V2.md, SHA256 d0a02a438740fa321dd8c5b2e2a325e5c9cfddda9c35e7df8e11d50e30cda8ef.
- Optional outer-frozen.sha256: 5a3eb516a74f2a1206fe4fdc710e58c01faa4e422963d6abd4ca020185730468.
- Optional frozen-inputs.sha256: 994a94405a2822e77e4aea7b487a309313be267d541899bca14ffa361b4df656.
- PATH_ADMISSION.json: 4852efca76c61776ae3b4e5d227fa1036c12738c338525261df7b9830964bd59.
- FROZEN_TARGETS.json: f93ca064d73c5f715e802a65b41fb75afd6790c253c45da4b59d1a9d46d2f3af.
- preflight.py: 50039248ca7589391cf67e6f0fd5caefd7dcbdc641101bf4278d4ee69c021c72.
- PROPOSED_COMMANDS.txt: c20c5209c379b808e1e8b6b7a259dcc3e70337c43fb1c1ca32879f9c2eb3630b.
- Main accepted report.md: 321ac1c7db1624e3fdf3e40276be274778c3f36f84e236e3fb2691cda57de7c6.

All 18 exact optional packet files match the accepted packet review. Both manifests have exact admitted target sets, respectively 3 and 6,152 targets; every target hash passes initially and finally. The exact coordinator selection is /bin/bash followed by the absolute optional V2 PROPOSED_COMMANDS.txt path. Its timestamp is 2026-10-15T02:30:55.980642+00:00. The selection's six external anchor entries match the exact expected mapping, including the accepted main report; no omitted or additional anchor is accepted. runtime_authorized is false. The exact entry transcript passes and exit.txt is exactly 0 followed by a newline.

Coordinator capture: /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/cleanup-optional-install-v2-coordinator.
- selection.json: bb2f262d9a90524255f198c11138a6c4e7364376f4064502e46c585e219d703c.
- entry.log: 5a33b7ba108dccbac6e6d97955555cdcdfa6c25383aeed163bff72a4294d6060.
- exit.txt: 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa.

## Admission, historical preservation and cross-plan continuity

The checker completely admitted names, types, directories, four exact aliases per environment, and regular metadata across all seven trees before any expanded payload hashing. No manifest authorized its own expansion. Fixed safe authority files were independently pinned; fixed output receipt/log names and top-level memberships were admitted separately. Individual payload reads repeat no-link regular-path admission and verify opened descriptor metadata before and after reading.

Original leaves remain exactly 1,658 / 1,658 / 5,900 for SA21 / SA20 / SQLModel. Their complete payload inventories and all retained metadata equal the historical baseline: device, inode, mode, link count, uid/gid, size, mtime_ns and ctime_ns for files, directories and aliases. Atime is intentionally excluded. The optional original has 5,896 regular files. Historical snapshots and hashes also match.

Clean source remains exactly 217 files with manifest SHA256 4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649. Its bytes and represented preparation metadata match. Preparation directories had deliberately type-only baseline fields; the audit compares those represented fields while separately retaining full fresh metadata. Full source metadata also equals the successful main-audit metadata snapshot.

Both installed main cells have the exact complete metadata retained by the accepted main audit. Their nonproduct bytes/aliases, all installed payloads, RECORDs, launchers, generated additions and inode receipts were independently rechecked. The full per-cell audit results equal the preserved main DATA_AUDIT.json, SHA256 6df29ab079a089fc43c8ff1ea8c056667abf3ee4f78dbd1d32e5ae57bcf95523; no main evidence was changed.

Complete current regular-inode counts are:
- original SA21: 1,654
- original SA20: 1,654
- original SQLModel: 5,896
- installed SA21: 1,629
- installed SA20: 1,629
- installed SQLModel: 5,892
- clean source: 217

All 21 pairwise intersections are empty. Thus each new cell is disjoint from all originals, both other new cells and the clean source. The optional installed tree contains 5,896 leaves and 661 directories including its root. Its 5,896-entry copy receipt and 5,884-entry surviving-installed receipt have complete exact coverage and match the independently observed original/current inode identities where applicable. Nonproduct copied inode identities persist. Intermediate copy identities remain receipt evidence, not a present-time independent observation of the intermediate tree.

All seven complete metadata inventories and payloads were rechecked at the end and remained equal to the start of the audit.

## Wheel, installed payload and dependency ownership

Wheel SHA256: 77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b.

Before ZIP payload reads, the checker required exactly 46 regular member names plus the six exact parent-directory entries, no duplicate names, path traversal or special member types. Wheel RECORD has exactly 46 unique rows covering every payload; 45 SHA256/size entries validate and the self row has empty digest/size. Every one of 41 runtime modules equals the clean candidate source. The only console entry point remains cryptalis = cryptalis.cli:main.

The optional installed RECORD has exactly 51 unique rows, with SHA256 6192317d138340a85e6eb5b732e0e34dbf2f11de90f12652b6b8b3abb1350338. Every row's coverage, target confinement, SHA256 and size validates, with empty self fields. All 45 hashed wheel payloads and all 41 modules equal the accepted wheel/source. RECORD owns every actual product file and no dependency file. The checker permits 50 or 51 rows according to actual uv_cache.json absence/presence; it does not assume a universal 51-row format.

The actual five additions are INSTALLER, REQUESTED, direct_url.json, uv_cache.json and ../../../bin/cryptalis. INSTALLER is exactly the two bytes b'uv', SHA256 e6184ce10e266134fdcfa401e8f1a95005bcd4f18d16b62b757323e2833fe9a9. REQUESTED is empty. direct_url.json identifies the exact accepted local wheel URI and has an empty archive_info object. No undeclared product path, alias, .pth file, entry point or startup hook appears.

All 5,845 optional nonproduct leaves are byte/link identical to the original. The only inherited startup hook remains _virtualenv.pth with its unchanged _virtualenv.py helper. All 76 dependency RECORDs have no overlapping product-owned target. The original optional product RECORD has the exact 43 historical owned targets. Existing dependency binaries/bytecode are unchanged opaque payload, not complete dependency archive provenance or historical execution attestation.

## Exact optional CLI

The fresh interpreter pathname is exactly 126 characters:
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/async-cleanup-sqlmodel-installed-20261015/sqlmodel/bin/python

The actual generated CLI uses the reviewed quoted /bin/sh exec trampoline, with that exact interpreter, "$0" and "$@", followed by the exact reviewed CLI body. The complete bytes match one and only one permitted launcher form. The file is executable. Its SHA256 is 0c04d9b44a91947cf07087fb7ba3260bb7eda0981e503b6905b5f167fb61f9e5. The body SHA256 is 1460564e897e2e3fd6b7eca4bc61ed0de11435625fcfd9f952fca4b7140a4a79. No CLI was executed. Copied activation scripts and other dependency console-script shebangs remain historical and are not approved launch routes.

## Bounded parent and safe logs

Parent receipt SHA256: 051198baa3551a2aeef5d0b9407a45203378d07ff7772e5c63b5210e8f8e65d2.
Inner verification SHA256: 31efb5f33b18d4f9744e036d3b9a1f466f974e1e55237a88426f31c9c30e4e23.

Actual parent status is PASS_BOUNDED_INSTALLATION. Child exit is 0, reason is null, errors and cleanup_errors are empty, leader_reaped is true and group_signals is empty. Both captured child streams are exactly empty with correct byte counts and SHA256. All four before/after integrity groups match exactly: outer targets 3, frozen targets 6,152, optional original leaves 5,900, source leaves 217. Parent file-size limits are restored; the original limit pair is [-1, -1]. The child command and scrubbed environment equal the reviewed fixed values.

Configured bounds are 120 seconds per child, 2 MiB per captured stream and 64 MiB per inherited regular file. These are cooperative limits, not aggregate disk/memory quotas, network isolation, hostile-code containment or complete descendant proof. wall_seconds is configuration rather than measured elapsed time. descendants_verified_absent is false and is not promoted to an absence claim.

The inner verification is PASS_INSTALLED_PAYLOAD_ONLY, reports unchanged original/source and matches every independently checked payload, RECORD, command and inode/dependency field. The exact uv command uses --no-config, offline/no-index/no-deps/no-cache, --link-mode copy and the new optional interpreter with only the accepted wheel. The installer stdout is empty. Stderr is 598 bytes, SHA256 737fa1685f536c15699ef12abd79dc37cbadcc8a3177bd7d97b0746c32cfe205, showing one Cryptalis uninstall and one install from the expected local wheel, with no error or truncation indicator.

## Preserved reviewer attempt and limits

Attempt 1 passed structural, payload and bounded-parent checks before stopping at the reviewer's inherited five-anchor selection allowlist. Optional selection legitimately adds the accepted main report as a sixth external anchor. The coordinator explicitly authorized a reviewer-only correction requiring exactly those six entries and the supplied main-report digest. Attempt 1 source/log/exit/metadata remain preserved. Attempt 2 changes only that allowlist check and the new snapshot filename, completes with exit 0 and produces this accepted audit. No source, installer, evidence, schema policy or oracle artifact was repaired. ATTEMPTS.md and attempt2-correction.patch retain the details.

No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json was read, hashed or copied. No secrets/environment dump or unapproved cache/HOME/tmp payload was read. The fixed scrubbed parent receipt was read only after terminal completion. The preapproved historical trees contain inherited bytecode/cache-like paths; those exact admitted files were treated as opaque historical payload. Reviewer output is confined to this directory.

## Required next gate

Installed runtime is still pending. Materialize new final runtime packets with the complete 217-file safe source archive, actual installed module/RECORD/audit bindings, immutable inputs, exact corpus baseline and separate independent source/command review. Preserve per-stage clearance and coordinator selection. Main installed SA21 must be terminally audited before main installed SA20; optional runtime remains gated on both accepted fresh main terminal results and its own final command clearance. Do not use this payload audit, a named clearance file or the unchanged templates as execution permission.

Seven historical main failures remain unresolved. All seven broader gates remain UNKNOWN: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY, G-RELEASE. Dependency lock/archive provenance, bundled builder/source provenance, natural fault equivalence, physical quarantine, real provider custody, independent-host reproducibility, fresh-host/cluster restore, external human review and production readiness remain unestablished.

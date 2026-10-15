# Independent installed cleanup217 evidence rebuild and inert restoration

Date: 2026-10-15 UTC.
Decision: **ACCEPT_INDEPENDENT_THREE_ARCHIVE_BYTE_REBUILD_AND_INERT_INSTALLED_EVIDENCE_RESTORE**.

This accepts the exact source/evidence recovery bytes below. It is not installed-environment recovery, runtime qualification, product-build reproducibility, release approval or production readiness. Only the root coordinator may promote this result.

## Exact input identities

Installed V2 archive: CRYPTALIS_ASYNC_CLEANUP_INSTALLED_RECOVERY_20261015_v2.tar.xz, 3,948,788 bytes, SHA256 4191955448fc3670cf907c27fb4f346e38b39c1089f3d47ab482d68d35436403. Its complete USTAR stream is 79,738,880 bytes, containing 550 regular members / 79,312,659 payload bytes. Manifest SHA256 2bd94c433bd17a87ce55b32be04e613c85c51f407fc1f03c6b2855b222ba0197; exact allowlist SHA256 adc77fb8037a9f95f66ce95c52d9d6da12576d72e22a857a266e27f53f56d1ec; candidate seal 1fb51eec785e63e5f4de0ee4b0bb6a5463c009aa56f76f91ed11b4e698dfc09c.

Focused/base V1 archive: CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.tar.xz, 1,029,680 bytes, SHA256 1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af. Manifest e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174 and accepted allowlist 8625a305e537c397a65ed75a8f113bf28c6396e6aa7c36a86f93b90907524176. Exactly 516 members; 9,543,680 USTAR bytes.

Full-source/build additive V2 archive: CRYPTALIS_ASYNC_CLEANUP_ADDITIVE_RECOVERY_20261015_v2.tar.xz, 2,176,040 bytes, SHA256 bab72dad661711acc3d8fdf2ab5e84f6abc7eaafd0d1f976023004b08e371262. Manifest b664ead41a5196f410589ef4d8626d3105107e56ac4ac34f8c83603cb71df26a and allowlist 5acba866d11b08a8652ac3268db1292e3d89957035b49ce9779e5456e3b71a01. Exactly 355 members; 38,635,520 USTAR bytes.

The freeze report b02afbb0bf74aca9611d97ea8995b7ed7c329cfee735a01444141711941e70fc and method seal 92f2f2f432f5233e0ef2b25d1463c2ee84ffe2db51ec35e1ec8ee47bf2594907 match. Both accepted preparation inventories, both independent review pins, all four preparation/review seals, and candidate/method seals were rechecked within exact admitted control scopes. The 3,818 installed logical records exactly match the union of the unchanged original and supplement inventories in path, size, digest, role and original locator. All 79 external control bodies match their archived objects.

## Independent method and admission

Newly authored verify_v2.py uses standard-library data operations only. No preserved producer, installer, reviewer, product or test program was executed or imported. External reads check real parents, regular single-link leaves, O_NOFOLLOW, bounded size and before/after metadata. The expanded external control metadata admission was persisted before those control-body reads. Existing input manifests establish the exact accepted data selections; recorded payload paths are never followed as live-origin targets.

Each of the three archives is bounded to 128 MiB compressed and complete decompressed bytes, with a 128 MiB XZ decoder memory limit. This is not a whole-process memory ceiling. The decoder requires exactly one XZ/CRC64 stream, EOF and no unused/trailing bytes. Every expected member is bounded to 16 MiB. Exact ASCII names, duplicates, casefold collisions, unsafe paths and file/directory collisions are checked. Every physical header must equal an independently generated canonical USTAR header with exact name and size, regular type, prescribed mode (0444 installed; 0644 dependencies), uid/gid/mtime zero and empty owners/link fields. The base physical names carry exactly its pinned archive_root; locators stay relative. Extended/special/link entries cannot match these headers. Full header admission for all 1,421 members was persisted before any member-body hash, indexing or restoration. Body alignment padding and canonical terminal record padding are zero.

Only after all three header sets passed did every body digest get verified. All three archived manifests equal their pinned external counterparts. Complete USTAR streams were independently rebuilt from expected headers and verified bodies, then compressed with explicit XZ preset6/CRC64. Both USTAR bytes and compressed byte strings match exactly. Independent rebuilt archives are retained at this review root.

## Fresh inert reconstruction and continuity

All content came from the three admitted archives, never live origins, dependencies, interpreters, caches or installed environments. Nested archive and wheel bodies remained opaque. Fresh tree creation was exclusive, with no overwrite or writeback. Every restored file is regular, single-link, nonexecutable mode0600; every restored directory is mode0700. Each tree had exact expected file/directory closure, complete readback and hash verification:

- fresh-logical-evidence-v1: 3,818 files / 176,927,273 bytes.
- fresh-controls-v1: 79 files / 7,493,718 bytes.
- fresh-installed-members-v1: 550 files / 79,312,659 bytes.
- fresh-focused_base_v1-members-v1: 516 files / 9,148,868 bytes.
- fresh-full_source_build_additive_v2-members-v1: 355 files / 38,348,976 bytes.
- fresh-green217-v1: 217 files / 4,423,405 bytes.

Total: 5,535 files / 315,654,899 bytes. The optional installed candidate-corpus directory is preserved empty. The installed logical manifest retains its complete source217 views and narrower wrapper captures through exact base-member resolutions; separate GREEN217 is copied from the verified base source members. No additional RED/baseline view was inferred outside this installed manifest scope. The final continuity pass rechecked every recorded external input and restored file with unchanged metadata and digest.

## Preserved failure and narrow correction

V1 failed at the first focused/base header comparison because the checker used its relative allowlist name as the physical header name, omitting the pinned base archive_root. It failed before archive-body hashing or extraction. A header-only inspection established the exact physical prefix. The source, literal command, traceback and exit1 remain unchanged, with METHOD_INCIDENT-v1.json binding their hashes.

The coordinator authorized only prepending BM.archive_root + '/' for focused_base_v1 physical header validation/rebuilding. V2 makes exactly those two header-call corrections plus a distinct external-admission output filename. Relative member locators, all pins and payload scope remain unchanged. V2 completed its first invocation with exit0. No failed evidence or input archive was repaired, replaced or erased.

## Limits retained

All seven historical failures remain unresolved and all seven production gates remain UNKNOWN. Recorded restoration is not continuous assurance. Origin/RECORD distinctions, cooperative containment, dependency metadata-versus-lock/provenance limits, natural-fault/provider/fresh-host limits and existing qualification boundaries remain.

The earlier static remote-source review remains static. The separately admitted completed remote-result review is preserved under its original authenticated-observation reliance; this local restoration does not make a new remote-authentication claim. The three historical transport boundaries remain prerequisite evidence, not full transport qualification or authorization for execution.

No raw excluded phase/cache/secret payload, live source/current corpus, installed dependency/interpreter target, product import, test, install, DB/server, network, Git, publication or promotion action occurred. The previously accepted bounded secret disposition is retained; no new universal secret-absence claim is made.

VERIFICATION_RESULT-v1.json, ALL_HEADERS_ADMITTED-v1.json, EXTERNAL_CONTROL_ADMISSION-v2.json and FINAL_CONTINUITY-v1.json contain the machine-readable result and continuity evidence. REVIEW_FILES.sha256 binds all root-level outputs except itself; restored trees are covered by exact admitted manifests and final readback records.

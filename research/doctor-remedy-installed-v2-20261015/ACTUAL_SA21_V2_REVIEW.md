# Independent actual SA21 V2 installed terminal and payload audit

Date: 2026-10-15 UTC

## Decision

ACCEPTED_ACTUAL_SA21_INSTALLED_PAYLOAD_AND_TERMINAL. No blocking issue was found in the completed installer or fresh installed payload. The accepted exact maps below may be used as inputs to separately reviewed runtime preparation. This report does not select runtime, database work, SA20 installation or publication.

Actual cell: `release-lab/doctor-remedy-installed-sa21-v2-20261015/sa21` beneath the fixed repository root `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

Root reported installer session 18994 terminal exit 0 before this audit started. All reads were within the expanded actual-audit scope. No installer, product, test, Python import, database/status command or runtime helper was executed by this reviewer.

## Exact accepted maps

Both maps are direct JSON objects, without an outer cell-name wrapper, in this report's directory:

- `SA21_INSTALLED_NAMESPACE.json`: SHA256 `933fa3d2611b6a82d41b0fb253f0274a5cfe341727626265612a62854309ad1d`. Keys are `directories`, `regular`, `links`, and `opaque_installer_metadata`. Exactly 111 directories, 1,255 regular files, four fixed aliases and one metadata-only opaque marker.
- `SA21_INSTALLED_ORDINARY.json`: SHA256 `20428bf087742a34249df5cd12527fcb1b2a77b17777fbbf175af6aa1e261201`. Exactly 1,254 relative-path-to-SHA256 entries. The sole regular-file exclusion is `lib/python3.12/site-packages/cryptalis-0.1.0.dist-info/uv_cache.json`.

The namespace marker metadata records a single-link regular file of 127 bytes with inode 1971600 on device 27. Its body was never opened, read, hashed or copied by this reviewer. Its declared RECORD digest remains intentionally unverified against its body.

## Actual terminal

The separately admitted entry's persisted selection identifies the exact accepted entry and concrete review. Preflight, outer-admission, outer and after-admission exit files are all 0. Both entry stderr files are empty. Preflight stdout records successful metadata-first launch admission; outer stdout is empty.

The actual parent receipt is `PASS_BOUNDED_INSTALLATION`, SHA256 `b5208963afb03c0adfe5236d12a072851b97220d1d072b600c269f04e33d2d22`. Both before and after contain precisely the successful 3 / 2,007 / 1,259 / 221 integrity groups with empty errors. Child exit is 0, reason null, cleanup errors empty, leader reaped true, captured child stdout/stderr empty. Parent file-size limits are restored, prior artifacts preserved and host prefixes absent. The reviewed limits remain 120 seconds, 2 MiB per captured stream and 64 MiB per child regular file. These are cooperative limits; descendant absence is explicitly not established.

The actual installed verification receipt is `PASS_INSTALLED_PAYLOAD_ONLY`, SHA256 `9d149efda7b158ff979cbfb10b0254a4ed47fe9179e5b169abb74f3422606cc9`. It reports the original donor and source preserved. The bounded child executed only the reviewed offline, no-index, no-deps, no-cache, copy-link uv reinstall command against the actual accepted V2 wheel. Its safe uv capture records the one-package replacement, with empty stdout and 615 bytes of informational stderr.

## Metadata-first independent admission

Before opening any installed/source/wheel payload, this audit admitted real-directory ancestry and complete non-following metadata namespaces for the fresh cell, current source and original donor. Full sets matched PATH_ADMISSION exactly: fresh and donor each 111 directories / 1,255 regular files / four aliases; source 21 directories / 221 regular files. All regular leaves were single-link and bounded, all types allowed, all aliases exact, and no bytecode or cache-directory names existed.

The four aliases remain: `bin/python` to the fixed direct host Python 3.12 executable; `bin/python3` and `bin/python3.12` to `python`; `lib64` to `lib`. No alias body was hashed or followed as an ordinary file. The live host executable/body and host stdlib were not reopened by this reviewer.

All donor and source metadata, including exact integer nanosecond timestamps, matched the prior materialization admission. At audit end, complete fresh/source/donor metadata and actual-wheel metadata matched their own initial snapshots exactly, excluding access times. All 1,254 fresh ordinary hashes, all 221 source hashes and the actual wheel hash also passed a second finite verification. All 17 bound controls, 42 safe source/review controls and terminal inputs remained unchanged.

## Payload, namespaces and complete RECORD audit

The actual direct wheel is 140,953 bytes, SHA256 `053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965`. Its complete archive namespace is exactly 48 regular payloads and six directories, with allowed modes, no duplicates, redirects, opaque marker or bytecode. All 47 non-self wheel RECORD hashes and sizes independently validate. Every one of these 47 payloads equals the corresponding installed ordinary hash.

All 221 current source hashes equal source-original. The complete installed cryptalis Python namespace is exactly the 43 source modules, with exact source/wheel/installed byte identity. No package imports were used.

Installed cryptalis RECORD SHA256 is `bf678cb8a7d3c1e0969f45d6dd55df590c582eb9a3d29d3b1b955a0aa36f1dcf`. All 53 rows are unique and exactly cover the installed product namespace: the wheel's 48 rows plus the five expected installer additions. Every ordinary non-self row independently matches its actual admitted file digest and size; self hash/size are empty. All paths normalize inside the fresh cell. The marker's physical presence exactly equals its RECORD membership. Its row passes the explicit SHA256 syntax and actual metadata/size checks only. There is no unclaimed product file or undeclared row.

All 13 dependency RECORDs, comprising 1,186 rows, independently validate their complete current ordinary target membership, normalized in-cell paths, uniqueness, digests and sizes. Empty digest/size pairs occur only for the corresponding RECORD itself. There are zero absent or cache rows and no product overlap. Every one of the 1,202 nonproduct ordinary hashes equals its original donor pin; adding the four preserved aliases gives the installer's reported 1,206 dependency inventory entries. Original donor bodies were not reread: current nonproduct payloads were compared to pinned original maps, while original preservation is also supported by the actual before/after parent checks and unchanged original metadata.

The 400-byte executable CLI is byte-exact to the fixed direct fresh-interpreter launcher and approved cryptalis.cli main tail. Entry-point metadata is exact, INSTALLER is the two bytes `uv`, REQUESTED is empty, and direct_url is exactly the accepted actual V2 wheel URI with empty archive_info. No old artifact identity was substituted.

## Inode evidence

All 1,254 copy-pair and 1,254 surviving installed-pair rows have the exact required names and agree with current original/fresh device and inode metadata. Copy inodes are unique and different from originals. Nonproduct installed inodes equal their recorded copy inodes. The complete 1,255-file fresh regular inode set, including the new marker, is unique and disjoint from both the entire current donor regular inode set and current source regular inode set. The marker inode differs from the original marker. No hard-link sharing is hidden by the ordinary-body exclusion.

## Narrow size information for runtime preparation

Already admitted metadata shows exactly one ordinary file exceeding 8 MiB in each fresh/donor cell: `lib/python3.12/site-packages/cryptography/hazmat/bindings/_rust.abi3.so`, exactly 14,434,376 bytes, also the largest ordinary file. This supports only that exact-path/exact-size runtime reader exception, not a general cap increase. `actual-sa21/ORDINARY_SIZE_EXCEPTIONS.json` SHA256 is `91b536d42f6f0bb28ce81364772fdcb51c022f153453eb0f816bd412627e75ff`.

## Evidence and next boundary

`actual-sa21/METADATA_ADMISSION.json`, `PAYLOAD_COMPARISONS.json`, `TERMINAL_COMPARISONS.json` and `END_CHECKS.json` record the independent full-set comparisons. `payload_compare.jq` and `sha256-base64.awk` are reviewer-owned data transformations, not product or installer execution. Before/after metadata, safe terminal hashes, wheel-member hash/size tables and the finite ordinary/source verification manifests are retained in the same directory. `ACTUAL_SA21_V2_REVIEW.sha256` seals this report, both maps and all finite evidence files without a self-reference.

A runtime binding still requires independent source-command review, root semantic acceptance, current quiescence and admission, and explicit root selection. Existing full-root guard, role/lock/stop/corpus controls remain mandatory. This audit ran no database or runtime operation and establishes no runtime seven-node result, SA20 result, publication readiness, hostile-process containment or broader host provenance. No opaque marker or bytecode body, raw phase/environment JSON, credential, private HOME/cache or corpus payload was read. All writes were confined to this assigned reviewer directory.

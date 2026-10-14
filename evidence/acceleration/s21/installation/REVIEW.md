# Independent S21 isolated installation review

Verdict: ACCEPT installed payload/local-preservation evidence only. No installation, reinstall, product import, runtime test, database or Git action was performed. Integration test JSON, environment files and credentials were not read. Active runtime work was not disturbed.

Independent current-file audit:
- Exact S21 wheel remains SHA256 ebd58ffca3bfdf9aaa624a394a2cddcc2dedd91ceb99a75e9416e88afdee3514.
- In each new SA21/SA20 cell, all 44 hashed wheel payload files match the wheel byte-for-byte; the Python module inventory is exactly 40.
- Each installed RECORD contains 50 unique rows: 44 original hashed payloads, blank self-entry, and five allowed installer additions (bin/cryptalis, INSTALLER, REQUESTED, direct_url.json, uv_cache.json). Independently checked every row's resolved in-cell path, SHA256 and size. Installed RECORD is correctly not claimed identical to wheel RECORD.
- Installed RECORD digests match saved receipts: SA21 3f08dce886db08f1e40096ba0abbb9615218e526fe638f4c3ea3742cb69fde80; SA20 7952f4770e429b8d3186b64be13821d5ac78cc37448e2eab38c9119a0424b535.
- direct_url.json points to the exact pinned local wheel; INSTALLER is uv; each regenerated Cryptalis CLI refers to its new interpreter.
- Both original environment inventories independently still equal their frozen 1672-entry name/hash/symlink-target inventories. All outer/helper/original regular-file pins reverify.

Historical installation evidence and bounds:
- Child receipt reports PASS_INSTALLED_PAYLOAD_ONLY, both original cells unchanged and 1582 non-Cryptalis inventory entries preserved per cell, including dependency bytecode. The count is inventory entries (including symlinks), not exclusively regular files.
- Source-reviewed copy2 and distinct-inode checks precede installation. Saved command records show pinned uv with no-config, offline, no-index, no-deps, no-cache, link-mode copy and reinstall-package cryptalis, targeting the new explicit interpreter and exact wheel.
- Parent receipt reports PASS_BOUNDED_INSTALLATION, all four integrity groups successful before/after, exit 0, leader reaped, no group signals/cleanup errors, no parent errors, and restored original parent file-size limits.
- Recorded limits match reviewed code: 120-second child allowance plus up to 10-second reap, 2 MiB per-stream capture, and 64 MiB inherited soft per-file limit. No aggregate-disk or adversarial-containment claim. Descendant absence remains unverified.

The new environments' dependency/bytecode inventories were deliberately not re-compared while authorized runtime tests were running. Dependency-byte preservation is scoped to the installation receipt's pre-runtime interval, not asserted for current post-runtime bytecode. This review independently verifies current installed Cryptalis payloads and unchanged original environments, and audits the historical preservation receipt without replaying installation.

Existing dependency drift, lack of original dependency-archive authentication, copied stale activation/dependency-script shebangs and runtime qualification limits remain. Use explicit new bin/python for separately authorized tests. No full-suite or focused runtime outcome is claimed here. All seven qualification gates remain UNKNOWN.

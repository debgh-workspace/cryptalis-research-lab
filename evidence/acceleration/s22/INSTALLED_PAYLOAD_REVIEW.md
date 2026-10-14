# Independent S22 installation post-run review

Verdict: ACCEPT scoped installed-payload/nonproduct-preservation result. Audit completed before root's separate focused runtime work. No reinstall, candidate verifier rerun, product import, test, database or Git action was performed.

Independent actual-file findings for each SA21/SA20 cell:
- All 44 hashed files of the pinned S22 wheel (346eac4f4cf54bac270e25dce6f7d97cdb591ac2969a00a3b9c073a0e4a20c57) match installed bytes. Exact 40-module inventory also matches frozen source.
- Installed RECORD has 50 unique rows: 44 wheel payloads, blank self-entry and five allowed generated entries (CLI, INSTALLER, REQUESTED, direct_url.json, uv_cache.json). Independently validated every resolved in-cell path/hash/size, exact additions, local-wheel origin, uv installer and new-interpreter CLI reference.
- RECORD hashes match receipts: SA21 bceac7019277e5c51ceec1fa91f4afa3b7b9a517da42311a065b49874ca18d5a; SA20 e6a2ea29fda3baca50e848cc46de9d64b285f418ab94e400b1e87f60a7551d39.
- All 1582 non-Cryptalis inventory entries match originals, including dependency bytecode. This consists of 1578 regular files plus four symlinks. Each of those 1578 regular copied dependency files has a distinct device/inode identity from its original.
- Both original 1660-entry name/hash/link inventories remain exact. Complete 212-file frozen source inventory matches. All outer and 3536 frozen-input pins reverify.

Receipt review: child PASS_INSTALLED_PAYLOAD_ONLY records original cells/source unchanged. Parent PASS_BOUNDED_INSTALLATION records all five integrity groups passing before/after, child exit zero, reaped leader, no signals or cleanup errors, no parent errors and restored parent file limits. Bounds agree with reviewed implementation: 120-second child allowance plus up to 10-second reap, 2 MiB capture per stream, 64 MiB inherited soft per-file cap. Descendant absence remains unverified; no aggregate disk quota or adversarial-containment claim is made.

Nonproduct byte preservation above is independently established at this pre-runtime audit point. Later runtime bytecode effects are separate and must not be misrepresented as installation changes. Existing dependency drift and original dependency-archive provenance gaps remain. Copied activation/dependency console-script shebangs retain old paths; future authorized tests must use explicit new bin/python. No runtime or full release qualification is asserted. All seven product gates remain UNKNOWN.

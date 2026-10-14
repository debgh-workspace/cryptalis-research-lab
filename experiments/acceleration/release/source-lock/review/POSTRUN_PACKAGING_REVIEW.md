# Independent S20 source-lock packaging artifact review

Verdict: ACCEPT scoped optional packaging hardening. This reviewer performed data/archive inspection only, with no rebuild, product import, install, runtime test, database or Git action. Candidate verification and negative controls were not rerun.

Independent artifact findings:
- Both new sdists are byte-identical: SHA256 46a7e99426282cdcb386ed24a0af2cae6ebf7ba8278598fa701857b5caaab0aa.
- Both direct and from-sdist wheels are byte-identical to original S20: SHA256 a46e527484daaf4621831f395af8d8193716220a24106c5d6d0d983a16a9cbb7. This also preserves every wheel metadata/license byte.
- Full tar member inventory increases from 51 to 52 members (45 to 46 regular files), adding only cryptalis-0.1.0/uv.lock. Common member types match. Only pyproject.toml and pyproject.toml.orig payload bytes change; all other common regular payloads remain byte-identical. No duplicate/special members were found.
- Included lock exactly equals derivative source lock, SHA256 faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e. The .orig config exactly equals derivative source; parsed normalized config is identical in meaning.
- All 40 module bytes independently match source, new sdist and original/new wheel. RECORD independently has exact unique payload coverage and 44 correct SHA256/size rows plus blank self-entry.
- Both current source inventories have 208 non-cache files. Full manifests reverify; directory comparison reports only pyproject.toml differs. Earlier source review verified its exact additive source-include delta.

Execution evidence review:
- Parent receipt reports PASS_BOUNDED_PACKAGING, exit 0, reaped leader, no group signals or cleanup errors, and restored parent file-size limits. Descendant absence remains explicitly unverified.
- Four before/after integrity groups report success (8 outer, 12 v1, 208 original, 208 derivative entries). This reviewer independently reverified all four groups now.
- Receipt matches reviewed 120-second deadline, additional up-to-10-second reap allowance, 2 MiB per-stream caps and 8 MiB inherited soft per-file limit. These are trusted-builder controls, not adversarial containment or aggregate disk quota. Parent restoration is recorded true, original soft/hard limits unlimited.
- Exact launch command is the frozen v1 bash launcher. Version logs identify uv 0.12.23 and Python 3.12.14; the four fixed build logs identify their expected archive names. All eight step stderr files are empty. Captured stdout/stderr hashes independently match the parent receipt. This review does not independently establish historical process tracing or elapsed duration beyond saved execution evidence.
- Verification receipt records the two reviewed missing_lock/altered_lock negatives rejected. No extra control or runtime test run was performed.

Scope: optional source-release lock preservation only. Original artifacts and S20 input bytes remain unchanged. No current installed-dependency drift is repaired, no dependency archive provenance is added, and no original builder identity is retroactively established. Same-host/pinned-executable packaging identity is not independent clean-machine reproducibility, signing, platform or complete release qualification. All seven product gates remain UNKNOWN.

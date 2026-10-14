# Independent S22 recovery capsule publication review

Verdict: ACCEPT this exact capsule for the root-authorized bounded researchlab publication. Review does not authorize a different destination, expanded payload or changed bytes. No Git/network publication, build, test, product import or database operation was performed by this reviewer. Restored code was never executed.

Exact artifact:
- CRYPTALIS_S22_SOURCE_EVIDENCE_20261014.tar.xz
- SHA256 99c9c8c5663ed4c09505022fe13653e82fb28eff65cd25cf9e7b3d0b1108f010
- 1,857,500 compressed bytes

Independent checks passed:
- Exactly 492 unique normalized relative regular archive members. No links, special files, absolute paths, traversal or backslash names.
- Exact composition: 272 explicitly allowlisted evidence files, 212 source files and eight capsule metadata files. No additional payload members. Embedded inventory and 491-entry payload manifest agree with every member hash/size; manifest self-file is additionally bound by the reviewed complete archive digest.
- All 212 restored source hashes match the included frozen source-preparation receipt. All 492 files match the builder's fresh extraction, and a separate new reviewer-owned restore independently reproduced and rehashed every byte.
- Explicit path inspection excludes raw tests.json/package-origin.json, environment-bearing readiness/start/stop JSON, environment dumps, credential files, virtual environments/site-packages, caches and database state. Included packaging/install parent receipts describe deliberately allowlisted clean environments rather than inherited environment dumps. Dependency inventory JSON contains recorded path/hash/link data, not dependency contents.
- Independently repeated four bounded high-confidence secret-pattern checks across all 492 archive members and 182 decompressed built-distribution members. Zero findings. This is not a universal proof that arbitrary secrets cannot exist.

Scope/provenance wording is appropriate: source and selected evidence restore, not a ready-to-run lab. The 3317 external recorded pins are explicitly neither fresh current-file validation nor packaged dependency bytes. Existing drift, official dependency-archive provenance gaps, seven known failures and all seven UNKNOWN gates remain. Same-host packaging/installation evidence is not independent clean-machine reproducibility, signing or production readiness.

The 26 preserved prior-corpus files and one changed corpus output are historical capture/restoration evidence only; the pending separate corpus refresh is excluded. This review does not silently promote historical capture into current corpus semantic qualification. Recorded test counts are preserved as prior observations, not new reviewer executions.

Publication condition: root may chunk only this exact hash-verified archive, within the specifically authorized researchlab destination and bounded batches. Verify reconstruction against the full archive digest before claiming remote persistence. This local review makes no claim that publication already occurred.

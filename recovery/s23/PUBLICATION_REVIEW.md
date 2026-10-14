# Independent S23 recovery publication review

Verdict: ACCEPT this exact capsule for root-authorized bounded researchlab publication. No network/Git publication, database action, runtime test, product import or restored-code execution was performed by this reviewer.

Exact artifact: CRYPTALIS_S23_SOURCE_EVIDENCE_20261014.tar.xz, SHA256 41c756d905f84f4754208ba4d27bda87621ab88d0bac58fcf421c7bbcbf50870, 1,750,488 bytes.

Independent checks passed:
- 408 unique normalized relative regular members, without links/special files/traversal/absolute/backslash paths.
- Exact composition: 213 source files, 186 explicit evidence allowlist files and nine metadata files. Embedded inventories and 407-entry payload manifest match every member hash/size; the manifest self-file is bound by the full reviewed archive digest.
- All 213 source hashes match the frozen S23 preparation receipt. All 408 members match the builder's restore and were independently written into a separate fresh reviewer directory and rehashed. No restored code was run.
- Both prior S22 capsule references independently match actual archive sizes/digests (main 99c9c8c5663ed4c09505022fe13653e82fb28eff65cd25cf9e7b3d0b1108f010 and corpus add-on 079a8bdf19faddc0ea41a02db04eb3828e444eebd4f8ae5d56e87cd36f733815). Earlier corpus campaigns are referenced, not silently relabelled as S23 qualification.
- Allowlist/path checks exclude raw environment-bearing tests/package-origin/readiness/start/stop JSON, environment dumps, credential files, venv/site-packages contents, caches and DB state. Included bounded parent receipts describe clean allowlisted execution environments; dependency snapshots retain recorded paths/hashes rather than dependency bytes.
- Independent four-pattern scan of all 408 members and 182 decompressed built-distribution files found zero high-confidence matches. This is a bounded inspection, not universal proof of secret absence.

Scope is appropriately limited: source plus selected evidence restoration, not an operational runtime/database lab. Full-suite reports retain seven failures in each cell; SA20 retains 46 skips. Installed-focused 52-pass results per cell and planning RED/GREEN remain recorded prior evidence, not new reviewer executions or full qualification. All seven gates remain UNKNOWN. The 3317 external recorded pins are not freshly checked dependency-byte authentication and external runtime contents are not packaged. Dependency drift, source-to-binary provenance, clean-machine reproducibility, signing and production readiness remain unqualified.

Publish only the exact reviewed bytes within the root-authorized destination/batch bounds. Verify remote reconstruction against the full archive SHA256 before claiming persistence. This local review does not claim publication already occurred.

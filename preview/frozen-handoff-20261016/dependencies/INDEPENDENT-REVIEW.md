# Independent frozen-doctor portability reconciliation review

2026-10-16 UTC. Decision: **ACCEPTED_STATIC_DEPENDENCY_PORTABILITY_RECONCILIATION**. No required correction.

Reviewed the three files under `reviewer-notes/frozen-doctor-portability-reconciliation-20261016`:
- REPORT.md: `ad4899b1daecf6b82c3370bb88a8068fccc62ef63546c7301472cc8e7e0a8f73`.
- MISSING_INPUTS.json: `8e4a07858358b24597f4d2fb4816a0b71088f5cb5fb1db7a2b3a5bccb1b3f7a4`.
- INPUTS.sha256: `17db9330c9cf10c6c53637c811eb20b12e7d42a7ac63652b466324ffe4fd3762`.

## Verified

1. All 24 finite input identities reverify. The actual selected source's uv.lock is included and has SHA256 `faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e`. Current pyproject explicitly includes that lock in the sdist. The accepted actual packaging review corroborates its retained bytes, exact 49-payload sdist and missing/altered-lock controls. The old missing-lock finding is not carried forward incorrectly.
2. Each Linux CPython 3.12 profile has eight runtime wheels and five test additions. The two-profile union is exactly 14 distinct dependency archives; adding uv gives 15. Every filename/URL/SHA256 matches the named prior official-metadata record; both complete requirement files and the 15-row acquisition declaration match exactly. All 13 locked URL/hash pairs also occur together in current uv.lock. SA20's separate SQLAlchemy override remains explicit.
3. Accepted fresh namespace maps independently match all 13 dependency names per cell, including pycparser 3.11 and iniconfig 2.3.1. The lock instead selects 3.0 and 2.3.0. The observed-version original filenames/digests remain null. Lock-faithful installation is correctly described as a changed qualification boundary, not reproduction of the tested cells.
4. Both actual payload reviews support donor nonproduct preservation and 13 complete dependency RECORDs, with 1,186/1,184 rows and zero absent rows. The separate historical optional-cell 41 omissions are not applied to these main cells. Seven-case current results and broader original-artifact suites retain their proper attribution.
5. Original archive authentication, archive-to-installed-payload equivalence, uv archive-to-executable equality, interpreter/image/native provenance, complete SBOM/native notices and clean-host qualification remain unestablished. The declared wheel-tag floor is not promoted to measured portability. The historical timeout observations and absence of permission denial are represented accurately as dated evidence. Later root acquisition observations are outside this packet's as-of scope.

The proposed resource request and install path remain conditional on resources, admission and separately reviewed execution. No installation command, acquisition, platform choice or qualification is authorized here. All seven production gates remain UNKNOWN.

Only metadata, safe declarations/maps, configuration and existing reviews were compared. No original archive, live installed/host/native payload, cache/marker/bytecode/private data was read; no network acquisition, product/helper execution, installation, runtime/database/status or Git action occurred. Only this isolated reviewer directory was written. `PORTABILITY_STATIC_V1_CHECKS.json` retains the exact data joins.

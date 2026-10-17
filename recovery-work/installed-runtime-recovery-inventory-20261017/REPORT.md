# Installed runtime recovery inventory — 2026-10-17

## Disposition

Historical installed acceptance is recoverable. Current runnable environment is NOT restored. No installation, environment creation, test/product import, executable packet invocation, database operation, credential access or Git command was performed. Root owns source221 and raw RESULT restoration; this inventory does not duplicate those jobs.

Private repository: debgh-workspace/cryptalis-research-lab. Complete nontruncated direct tree inspected at eed4482d824c87004c6df280a038f0b24ac17d8d. New installed review bodies read through GitHub connector at c0e23a899f75c45bc288607a8d61f50b142408ef. Root-restored raw unit results are from a1c4e520bc0e6a26d22ca766da435e702cb759a8. Published checklist and current restored checklist distinguish evidence-only recovery from runtime restoration.

## What is actually recoverable

1. Exact successor product wheel is directly published at preview/artifacts/cleanup-state-docs-v1-20261017/cryptalis-0.1.0-py3-none-any.whl,141155 bytes,SHA256 e1f9af85ce3c4e2bc6458d6bf3c1163e227cb2e09fea7365b4d6f7ef52bca28b. Matching sdist150623 bytes,SHA2568850a20e997e998862c7d44273bcaf8e1cf6022d108f59f04f123731ae7af334. No new binary restore duplicated here.
2. Both installed-payload acceptance reviews, both installed-unit reviews and pair summary are directly recoverable. Copies retained under evidence/. Pair SHA25655bacb818b8b35cb08b744b2581339b73b630ea5665a7e00b631ec31e7d4f1d4; SA20 unitf48c331ccf109680fdd5ef5ed612c1ac48ed34924ef005c5510e28df1669880b; SA21 unit4cdac89f71f051d499e25053e84252bcddc15bc4bf63dabffacfc4ae8ade725a.
3. All three exact regression sources are directly published under cryptalis-executable/experiments/orm-flush-diagnostic-state-source-v2-20261016/regression/. Inert fetched copies in recovered-test-sources/ independently match both actual RESULT test_sha256 maps:
   - test_flush_cleanup_state_contract.py c9121432cdc44d184241e42415b185acbd8ae09a6462ff201d64ce2d3669a9bd
   - test_flush_cleanup_state_faults.py 9f9b7656fc23ac56090a777230f56408538cd4c06384690f51b106b76bee8f3d
   - test_flush_diagnostic_continuation_successor.py d7d6c7bffa8c7537fcee3502a4705c4b9439f6b06f3d8460b66c1b15768f6940
4. Earlier installer source is directly available, but is NOT a replacement for the missing current sealed packet:
   - candidate-cleanup-transport-main-installed-plan-v2-20261015/{install_verify.py,outer.py,preflight.py,supervisor_v2.py,plan.json,outer-frozen.sha256}
   - experiments/acceleration/async-cleanup-release/installer-v2/{main,optional}/{PROPOSED_COMMANDS.txt,install_verify.py,outer.py,preflight.py}
   - experiments/acceleration/async-cleanup-installed-full/ retains run-full-sa20.sh,run-full-sa21.sh,verify_runtime_binding.py and historical input/selection/control/review files.
   RECOVERABLE_DIRECT_PATHS.json records36 exact related remote paths, blob identities and sizes. Earlier Transport218 plan explicitly binds source218/runtime41/wheel73c066… and old s23 donor cells; substituting cleanup wheel would require a new reviewed packet, not just reusing its acceptance.
5. Published historical recovery archive manifests/parts exist: async-cleanup-installed V2 archive41919554…/3948788B/42parts, with focused and full-source-additive prerequisites; integrated221-focused archive1f76f9bf…/1611936B/17parts. Their recorded scope is inert source/evidence recovery, not installed/runtime recovery. No archive payloads were downloaded or inspected here and no claim is made that they contain current missing packets. Later installed-recovery V3 opaque capsule publication was held in checklist; do not treat it as an available route.

## Precise missing current packet/runtime

Both exact installed_root paths from actual results are absent on this workspace (metadata-only existence checks):
cryptalis-executable/release-lab/cleanup-docs-package-installed-sa20-v1-20261017/sa20
cryptalis-executable/release-lab/cleanup-docs-package-installed-sa21-v1-20261017/sa21

Raw results hash verified: SA20 17013e601c006b7429f2d2646792b8530342717fa9c0bf7a606712e5e2479d13; SA21 66df597f0098b93a3c68f1cb92e0f0165b382995151bbd1ff1829060d29d7688. These contain ordered outcomes/read paths, not all pinned input bodies/digests. Historical success cannot reconstruct a missing interpreter/dependency or authorize a rerun.

The complete eed direct tree does not contain current cleanup-docs-installed-state-unit-v2-20261017/run-unit.py, INPUTS.json, ACCEPTANCE-sa20.json or ACCEPTANCE-sa21.json, nor its source REVIEW.md. The actual results reference them; ACTUAL_RESULT_REFERENCES.json and SOURCE_PACKET_GAPS.json retain exact names/argv. Current14-member unit source packet and42-member installer packet are not available as direct complete packets in that tree. Later c0e23a adds acceptance summaries; later a1c4e adds raw results, not those executables. Three matching regression files are recoverable at the alternate source path above. No inference that a hash alone restores missing bytes.

## Dependency/platform/native provenance blocker

Published preview/frozen-handoff-20261016/dependencies/MISSING_INPUTS.json is retained in evidence/. Its exact archive list is14 dependency wheels across SA20/SA21 plus uv: eight runtime packages/profile and five test additions/profile. It records original archive bytes as unauthenticated, not a verified installed recovery bundle.

Tested donor namespaces differ from lock in pycparser3.11 versus3.0 and iniconfig2.3.1 versus2.3.0. Authenticated original filenames/digests for the observed versions are absent from those records. The SQLAlchemy2.0.51 override versus2.1.3 is intentional. A lock-faithful installation would therefore be a changed qualification boundary, not exact reproduction of either installed passing cell.

Recorded host executable is Python3.12.14 at /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12, SHA256fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7; uv executable SHA256abdc39eab8b4ad341dca91f3823a23a343fae94bdb22ebdd9e91694415206f2f. These are historical pins, not current admission. Missing: approved reproducible interpreter distribution/base-image digest, OS/glibc identity and native/system linkage closure. Recorded uv0.12.23 archive565c6e… exists as an expected URL/hash, but archive-to-executable equivalence is UNKNOWN. Python source hash does not authenticate hosted binary. Wheel tags CPython3.12/Linuxx86_64 and aggregate glibc>=2.24 do not establish current compatibility.

Native original wheel authentication, bundled native library provenance/notices and selected-artifact/current-cell SBOM remain incomplete. No native library/opaque uv_cache.json/cache/credential bodies were inspected. Original unit evidence remains deterministic tests with doubles, not real DB/physical release/full-suite/promotion evidence. SA21 realpath pre-run hash caveat and original packaging timeout remain attached.

## Smallest next authorized step / resource request

Within present read-only recovery scope: preserve these exact test/source/review records and identify an authenticated surviving copy of the missing14-member unit and42-member installer source/control packets and their host/dependency maps. This is data recovery only; no executable launch is currently ready.

To restore a runnable environment, first obtain an approved digest-pinned CPython3.12/Linuxx86_64 runtime/base image with explicit OS/glibc/native linkage identity, the authenticated exact dependency archive originals (or surviving exact donor payload with full manifest), and pinned uv/independently admitted installer. For exact historical-cell reproduction, specifically supply authenticated pycparser3.11/iniconfig2.3.1 originals rather than substituting lock versions. Product wheel is already published. No DB credentials or optional-framework downloads are needed for this prerequisite.

Only after these resources and explicit installation authority: prepare a new isolated offline/no-index/no-deps/no-build/no-shared-cache restoration recipe, independently review its finite metadata/hash namespace and native/tool identities, select one bounded installation, and inspect actual payload/RECORD/origins before any separately selected unit run. Do not use generic pip install/uv sync, create an environment, reuse historical clearance, or rerun tests as a provenance probe. Current blocker is missing authenticated runtime/dependency resources and exact current admission/controller packet, not missing product source or historical pass summaries.

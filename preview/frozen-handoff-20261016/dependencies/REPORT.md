# Frozen doctor candidate: dependency portability

**As of 16 October 2026, 01:02 UTC.** Existing accepted source/review/maps only. No acquisition, installation, runtime operation or repeated experiment.

## Bottom line and smallest request

The selected wheel is available and installed in two accepted same-host copied-dependency cells. A self-contained clean-host installation is still unproved.

For the smallest **SA21 runtime** route, supply:
1. One approved digest-pinned CPython3.12/Linux x86-64 interpreter/base image, with identified OS/glibc (selected wheel tags require an aggregate floor of2.24).
2. The **eight original runtime wheels** listed in MISSING_INPUTS.json, plus the exact uv0.12.23 installer archive or a separately reviewed installer identity.
3. For qualification, add **five test wheels**. For SA20, add only the alternate SQLAlchemy2.0.51 wheel. The existing full acquisition list is **14 distinct dependency archives plus uv**,15 total.

Existing records identify exact filenames, official URLs and SHA256 values, but do not authenticate downloaded archive bytes. Earlier bounded direct/escalated attempts timed out with zero bytes; they were not permission denials. No retry is performed here. Supplying original hash-matching archives is enough to unblock artifact admission; no database credential, provider account or optional framework is needed for that step.

**Choose the dependency boundary explicitly:** the ready archive list follows uv.lock. It does not reproduce two versions in the tested cells. Installing that list creates a new qualification boundary.

## Product identities, already established

- Source221 manifest: `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7`.
- Wheel `cryptalis-0.1.0-py3-none-any.whl`,140953bytes: `053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965`.
- Sdist `cryptalis-0.1.0.tar.gz`,150427bytes: `2e2a3cfc266602b958e4f4b2206c4d7ccc9e8d1de154ef0412141f529446a330`.
- Immutable private artifact commit: `220d35ce796b913c0cced2bd19b416cf287011c9`, directory `preview/artifacts/doctor-remedy-v2-20261015`.
- Both sdists and all three direct/repeat/roundtrip wheels are accepted equal on the existing host. The49-payload sdist includes uv.lock; it is not the entire221-file research/test/docs source tree.

## Exact dependency distinction

| Component | Declared-lock target | Current accepted doctor namespace |
|---|---|---|
| cffi |2.1.1|2.1.1|
| cryptography |50.0.2|50.0.2|
| greenlet |3.5.6|3.5.6|
| psycopg / psycopg-binary |3.3.6|3.3.6|
| pycparser |3.0|**3.11**|
| SQLAlchemy |2.1.3; intentional SA20 override2.0.51|2.1.3 /2.0.51|
| typing-extensions |4.16.0|4.16.0|
| iniconfig (test) |2.3.0|**2.3.1**|
| packaging / pluggy (test) |26.3 /1.6.0|26.3 /1.6.0|
| pygments / pytest (test) |2.21.0 /9.1.1|2.21.0 /9.1.1|

The discrepancies are **not merely a stale S20 note**: accepted fresh SA21/SA20 namespace maps still name those versions, and both actual payload audits preserve every donor nonproduct hash. This reconciliation reads those safe maps/reviews, not live package metadata or bytecode.

Exact reproduction of the observed cells instead needs authenticated originals for pycparser3.11 and iniconfig2.3.1. Their original-wheel filenames/hashes are **not established in the selected records**. All dependencies still need archive-to-installed-payload equivalence; file/RECORD pins cannot stand in for original ZIP hashes.

Current main cells each have13 fully checked dependency RECORDs:1186rows onSA21 and1184onSA20, with **zero absent dependency rows**. The separate historical optional SQLModel cell retains41 noncache omissions; those do not apply to these main cells. No portable optional dependency closure or new doctor optional result is established. Default async refusal remains.

## Interpreter, installer and source-build gaps

Accepted local identities are Python3.12.14 executable `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7` and uv0.12.23 executable `abdc39eab8b4ad341dca91f3823a23a343fae94bdb22ebdd9e91694415206f2f`. Scoped host-file checks are not upstream interpreter provenance or native linkage closure.

Official uv archive target is `565c6e2874dbeae86c02f3dea97255e878fec672659a73d4930c6b93fcab2fff`. Its archive hash is distinct from the executable hash; contained-executable equivalence remains unverified. The recorded Python source-XZ hash cannot authenticate the hosted interpreter. Exact interpreter/image, OS/glibc and native/system dependency provenance remain missing.

Current pyproject retains `uv_build>=0.12.12,<0.13`; uv.lock does not lock the backend. The accepted reproducible build instead binds uv0.12.23's bundled backend externally. Do not change frozen source or switch to the separate uv_build shim merely to claim portability. The historical S20 missing-lock-in-sdist finding is closed for this selected archive; other provenance gaps remain.

## SBOM and native licenses

Project MIT license bytes are unchanged and accepted in current packaging. Earlier static evidence covers eight exact-lock components,12 notices, three vendor SBOMs and15 bundled library files. Rust has39 declared components/licenses; OpenSSL1component and auditwheel10components have no component-license fields in those inventories. Complete library-to-component/notice mapping, original archive authentication, platform variants and legal compatibility/compliance remain unestablished.

Historical nine-runtime/six-test-union SBOM evidence includes Windows conditionals. It is not a complete new SBOM bound to current doctor artifacts and their two observed dependency deviations. Windows-only tzdata2026.5/colorama are intentionally outside this Linux request, not missing Linux dependencies.

## Supported next install path

Keep both accepted cells untouched. After exact resources and separately reviewed execution are available: verify original hashes/interpreter/platform/installer; create a new isolated environment; use local-only, hash-required, no-index/no-build dependencies for the chosen profile; install the already accepted product wheel without dependency resolution/cache sharing; independently audit namespace/RECORD/payload/origin before selected runtime verification. No source build is required to install this wheel.

A source rebuild, if separately selected, must reuse the admitted bundled-uv route and controlled inputs. Generic source install, uv sync or unconstrained build is not equivalent evidence. Prior doctor7-case results remain on the actual copied-dependency cells; original2684/2638/optional38 counts remain on original Integrated221. All seven production gates remain UNKNOWN.

MISSING_INPUTS.json contains the full14 dependency filename/URL/hash inventory, uv input, explicit nulls for unestablished observed-version originals, platform/license gaps and accepted boundaries. INPUTS.sha256 pins24 finite safe inputs. No original file, selected candidate, root checklist or environment was modified.

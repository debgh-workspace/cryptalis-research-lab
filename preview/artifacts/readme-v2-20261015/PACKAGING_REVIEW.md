# README-only V2 independent terminal packaging review

Date: 15 October 2026 UTC.

## Decision

ACCEPT_SCOPED_README_ONLY_V2_PACKAGING_AND_SOURCE_EVIDENCE_TRANSFER.

The five actual successor distributions satisfy the exact accepted README-only packaging contract. Both sdists are byte-identical; direct, repeat and admitted-sdist-roundtrip wheels are byte-identical. No new or removed archive member exists. The only changed payloads against the original Integrated221 distributions are sdist README.md/PKG-INFO and wheel METADATA/RECORD. All source executable, test, configuration, dependency-lock, license and entry-point bodies remain unchanged. No blocking artifact or terminal-receipt defect was found.

This accepts documentation-only packaging and the explicitly bounded transfer of the accepted original source-suite evidence. It does not claim that this successor was installed, runtime-tested, publicly smoke-tested, clean-host reproduced, published or production-qualified. Any separately selected installed work is outside this review and was not inspected.

Procedural incidents are retained below and in PROCEDURE_FAILURE.md. This is not an incident-free-process claim.

## Exact input and action identities

Canonical packet: experiments/preview-readme-release-plan-v2-20261015 under /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

- Packet SHA256: 0aee3c684c9122bdcad903c8035f8d3864eb78d5c5016921bc921de2f12bdcdf.
- Accepted source-command review: fd8ccd1a2f0bf7274d5a6da42b1cd78b322934690c099f26fbd16df70449ddbb.
- Actual source221 manifest: 152ed80306b1cf9f5893242b499d54b7155efde33ef9ac43fc4edf8516cd53cc.
- README status binding: 19a6a26ece305b90ed55a10257fa557c5ed23c613682e092953150f4f3e9dbc0.
- README body: 0101bed8e6cc533e438d9a718281f7f15781fea170de91b788389938798cdcb5.
- Genuine BUILD_CLEARANCE.json: a78d508af782ca70787ff2ddd7f38edef2a75ba0e8aa30e6bfbf2917ef1bfb8a.
- Root-selected entry: run-build.sh, SHA256 0052acd3dd45194e439e1c9e1860fd9ef21b80fcf7e7e427a2838ea6f9f64b05.

The clearance has the exact seven top-level fields and nine required review roles. Every row's path/hash, ACCEPTED decision and exact role scope match the fixed policy and actual accepted report bytes, including the canonical source-command review. Quiescence is true and the packet/source/status anchors are exact. The retained root helper creates the clearance exclusively and invokes one entry; it was read as data, never executed by this reviewer.

## Five real artifacts

All five are under the canonical packet's run directory:

- sdist-1/cryptalis-0.1.0.tar.gz: 150,389 bytes, SHA256 7988fb28baa4dec5804d4779b8a1d626c7dae5e3d7d5e597a7a12a69e0d9a036.
- sdist-2/cryptalis-0.1.0.tar.gz: 150,389 bytes, the same SHA256 and directly equal bytes.
- direct-wheel/cryptalis-0.1.0-py3-none-any.whl: 140,936 bytes, SHA256 ce4817376f25411c8685c676802cce25c1799c85a87277b1dcc099556a40229c.
- repeat-wheel/cryptalis-0.1.0-py3-none-any.whl: 140,936 bytes, the same SHA256 and directly equal bytes.
- roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl: 140,936 bytes, the same SHA256 and directly equal bytes.

Each sdist contains exactly 49 regular payloads and six directories, totaling 581,773 uncompressed payload bytes. Each wheel contains exactly 48 regular payloads and six directories, totaling 475,450 uncompressed payload bytes. Expected member names were independently derived from the complete source map's 43 runtime modules plus fixed package metadata.

All archive paths and leaf metadata were admitted first. Complete TAR names/types/ownership/mode/time/link/PAX/sparse/size inventories and complete ZIP central fields, local headers, local/central equality, bounded nonoverlapping spans, modes, timestamps, flags, compression and exact sets were checked before member extraction. No member was extracted to disk by this reviewer. No added, removed, duplicate, unsafe or unexpected member was admitted.

## Exact payload deltas and roundtrip

Every unpermitted payload directly equals the canonical original archive. All 43 runtime modules in every new archive directly equal successor source. Tests remain complete in source and absent from distributions. Lock, license, entry points and original config bytes are retained; the sdist normalized pyproject is semantically equal to the unchanged source and byte-equal to the original sdist. The console entry remains cryptalis.cli:main.

Original PKG-INFO and METADATA are equal, with a description exactly equal to original README. Every successor PKG-INFO/METADATA retains the exact original header bytes, including version/dependencies/Markdown content type, and the description is exactly the bound successor README. Both successor sdist README payloads exactly equal that README. New sdist PKG-INFO equals every new wheel METADATA.

Each RECORD has the same ordered 48 unique rows, covers exactly its wheel, has 47 correct URL-safe SHA256/size entries and empty self fields. Comparing original and new RECORD rows, only the METADATA row changes. Both lock negative controls reject with their exact missing_lock and altered_lock reasons in the actual verifier and in the independent data-only predicate check.

The complete extracted tree has precisely the admitted 49-file sdist payload and seven directories including its extraction root. Every extracted file directly equals the first sdist after the actual roundtrip wheel build. The accepted extraction helper performs its immediate pre-roundtrip equality check; successful set-e sequencing establishes its completion, and the independent audit establishes final equality. The three-wheel direct byte comparison closes the roundtrip result.

## Finite standalone-distribution content scope

For any separately authorized decision concerning only the two standalone distribution files, the admitted content scope is exact:

- Sdist: 43 reviewed product runtime modules plus LICENSE, README.md, PKG-INFO, pyproject.toml, pyproject.toml.orig and uv.lock.
- Wheel: the same43 reviewed runtime modules plus METADATA, RECORD, WHEEL, entry_points.txt and licenses/LICENSE.

There is no extra dependency payload, cache, home, credential, test or recovery-supplement file in either archive. The intentional uv.lock is the unchanged reviewed dependency lock, not a bundled dependency payload. The README's nine links are exactly the intended immutable private source221-v4 guide links, checked against accepted source-command evidence and unchanged local guide bodies/seal. No new remote publication/access probe occurred.

These are finite member-set and content-identity findings. They do not certify comprehensive secret absence within all reviewed source content or authorize publication. The separately held original source/package recovery supplement was neither inspected nor modified by this review and is outside this standalone-distribution scope.

## Source and frozen-input preservation

Original candidate, original clean source, successor source and both actual complete source copies each have exactly 221 regular files and 22 source directories including each tree root. Candidate cache boundaries were checked as directory metadata only and never entered. All 221 original candidate bodies directly equal the original clean source. All 220 non-README successor bodies directly equal both originals, including all 43 runtime modules and all 116 test-tree files. The two build copies directly equal all 221 successor source bodies. Every corresponding leaf across all five trees has a distinct device/inode pair.

Independent finite membership/hash reconstruction passes exactly 256 packet declarations, three outer declarations, 726 frozen-input declarations, and 221 declarations in each baseline/derivative/candidate source group. Thirty-six local controls and their source maps are exact. Pinned helper/tool bytes and the Python alias target are retained. No product helper was imported or executed to perform these checks.

All five original distributions are frozen at their accepted identities: both original 154,158-byte sdists retain SHA256 1f447ac32bac75803826df6e2e66a1df5a8dd515448484c271175c279ef98b6c, and all three original 144,298-byte wheels retain dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6. They were not replaced by successor hashes. All 1,227 payloads read by the independent artifact audit were metadata-re-admitted and rehashed at its end; recorded leaf identity, mode, size, link count, mtime and ctime remained equal.

## Actual root, entry, parent and child closure

Root capture is persistence-recovery-20261013/preview-readme-v2-build-root; entry capture is its sibling preview-readme-v2-build-coordinator. Root argv is exactly /bin/bash, the pinned run-build.sh, packet digest and genuine clearance digest; root cwd is the workspace. The entry records the expected packet cwd and exact preflight/outer commands.

Root session16412 terminal exit0 was notified by root before output payload inspection. Persisted entry exit is0. Entry preflight, outer-tool admission and outer exits are all0. Parent status is PASS_BOUNDED_PACKAGING. Its actual child command selects the exact run-after-review.sh with matching packet/clearance digests; child exit0, reason null, leader_reaped true, no group signals and no cleanup errors. Entry and outer stdout/stderr are empty; all admitted packaging and post-group stderr leaves are empty.

Preflight and parent before/after receipts contain all six exact successful groups and counts, with no errors; derivative has 220 unchanged non-README bodies. Each of the six actual post-build group logs agrees. Actual verifier status is PASS_SCOPED_DOCUMENTATION_ONLY_PACKAGING and its hashes, controls and exact deltas reconcile with independent findings. Child aggregate stdout is735 bytes with the same hash as the independently read preflight JSON; stderr is0 bytes with the empty digest. Raw captured child stream values and environment values are excluded from the persisted safe receipt projection.

The actual parent binds 120 seconds, 2,097,152 bytes per captured stream and an 8,388,608-byte inherited regular-file limit. Original parent file limits were unlimited and restoration is true. No timeout/cap/cleanup failure is recorded. These remain cooperative bounds, not aggregate quotas, hostile-process isolation, OS network isolation or independent descendant-absence proof; descendants_verified_absent is explicitly false. There are no separate backend exit-status receipts. Successful set-e sequence completion and terminal child0 provide the available backend-completion evidence and are not relabeled as per-command exit records.

Root's persisted independent pre/post PostgreSQL status exits are both3, and the retained root helper checks these exact calls before clearance and after entry completion. Root separately confirmed its post-status3 assertion. This reviewer did not execute a database command, enumerate live processes or inspect any live installed cell/corpus.

## Source-evidence transfer and README scope

The exact unchanged 220-file executable/test/configuration/dependency/entry-point source delta and preserved package payloads support carrying forward the accepted original source-suite evidence without a redundant full runtime-suite execution for this documentation-only change. This is an evidence-transfer conclusion, not a new test result. A later executable, test, configuration, lock, entry-point or build-behavior change outside this reviewed packaging-control successor would require renewed assessment.

The source and installed terminal report identities remain exact. Their stated results reconcile with the bound 15:49 UTC README snapshot: SA21 2,684 ordinary passes and56 separate passing subtests; SA20 2,638 ordinary passes, the same46 accepted native-version skips and56 separate subtests; optional38 has38 ordinary passes and114 passing phases. Installed results qualify the original Integrated221 artifact. This review does not retroactively attribute those installed executions to the newly hashed successor.

All nine README guide links use exact immutable commit d952c505a4666266019e32f27c77f93edd5151ca and preview/docs/source221-v4/. Their nine local payloads and seal remain unchanged. Remote publication/access was not reprobed. The README clearly marks the guide as an earlier snapshot and its installation hashes as original-artifact identities. The status JSON's null successor-artifact field is an immutable prebuild snapshot, not a postbuild claim; the actual successor identities are recorded above and in ACTUAL_ARTIFACTS.json.

The exact public quickstart remains unexecuted and fresh-fixture ACL permission remains pending. All34 product objectives remain active; all seven broad production gates remain UNKNOWN. Original dependency artifact availability and clean-host provenance remain unresolved. No installation, public smoke, publication or downstream action is selected or authorized by this review.

## Evidence and procedural record

Both independent programs passed on first execution, exit0 and empty stderr:

- audit_artifacts.py; ARTIFACT_CHECKS.json SHA256 73a07de241d06c1090127c1010dd4d4567833a907011a843266d7b58237f674e.
- audit_receipts.py; RECEIPT_CHECKS.json SHA256 943977a840c9f78418b164959e1c7708ff89fbfbd7610d1e982624a4b521c220.
- ACTUAL_ARTIFACTS.json SHA256 97956cc709ba0e2ef3af908144e9534c12a1599e75396b6ba8b247899b20b1a1.
- INPUTS.json contains finite artifact-audit metadata/hash evidence; corresponding stdout/stderr/exit leaves retain exact audit outcomes.

Three procedural issues were disclosed to root: the two explicitly assigned initial review documents were read before metadata admission and subsequently admitted/rehashed; a preterminal shallow inventory lstat'ed run/parent-results directory entries without entering them or reading output leaves; an initial root argv display included its fixed nonsecret environment map. Subsequent receipt projections excluded environment values. PROCEDURE_FAILURE.md preserves the exact distinctions. Early truncated displays were not treated as complete validation.

No product execution/import, tests, installation, DB action, Git operation, network action, credential access, cache-body access or raw runtime-phase receipt inspection occurred in this review. Only finite source/package/control/safe receipt data was consumed after admission, subject to the disclosed initial-document incident. Writes were confined to this independent reviewer directory.

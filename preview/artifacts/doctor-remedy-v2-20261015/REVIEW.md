# Doctor-remedy V2: independent terminal packaging review

Date: 2026-10-15 UTC.

## Decision

**ACCEPTED_SCOPED_DOCTOR_REMEDY_V2_PACKAGING.** The five actual distributions satisfy the reviewed doctor-remedy packaging contract. Both sdists are byte-identical; the direct, repeat and admitted-sdist-roundtrip wheels are byte-identical. Only the approved CLI payload changes against accepted README-v2, plus the wheel RECORD entry required by that payload change. Complete source, payload, metadata, RECORD, extraction, preservation and terminal-receipt checks pass.

This accepts packaging of the exact source already qualified by the narrow accepted source RED/GREEN regression. It does not qualify an installed successor, transfer every earlier full runtime suite to the changed CLI, claim a new database check, authorize installation or publication, or advance a production gate.

Output payload inspection began only after root reported session 59175 terminal with exit 0 at 23:05 UTC. No build/helper rerun, product import, installation, test, database command, Git action or publication was performed by this reviewer.

## Exact selected identities

Canonical packet: `experiments/doctor-remedy-package-continuation-v2-20261015/build` under `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

- Packet seal: `23866b15d6c4751bce88a19dacf9c5e706469fc113ad47f8aea11045393a5e36`.
- Root-selected entry: `run-build.sh`, SHA256 `34d9df087851f95d4484bc0e574d04ea0abd82211137a5040591acfac7e49e8a`.
- Accepted source-command review: `66c3e35ac5e6e01ec5f2cfb769571b8343524925d5b1eb1c33028e7af039db97`.
- Actual clearance: `9d91dd42afeb7fb54d04082344da367f85bf150e6d8ee1393e2460b0ebbf8bc7`.
- Complete source221 manifest: `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7`.
- Accepted source RED: `a4817e237d082eee340232126e4b9cc27683a776ca5017aa3632ce7afca80483`.
- Accepted source GREEN: `1632e84f5b85fddfeafe165489598895ea9e699514fa17207e49b9ce7a250368`.
- Artifact index `ACTUAL_ARTIFACTS.json`: `0a8a7d1a996a9cd5f14e03a60edbc09e330bc4746648181ed511220aa9bbd089`.

The genuine clearance has the exact seven top-level fields and 12 required review roles. Every path/hash, ACCEPTED decision and role scope matches the policy and actual accepted review bytes. Its packet/source/status bindings are exact and quiescence is true. The V2 review is used; the V1 HOLD was not substituted.

## Five actual artifacts

All output paths below are relative to the canonical packet's `run/` directory.

- `sdist-1/cryptalis-0.1.0.tar.gz`: 150,427 bytes; SHA256 `2e2a3cfc266602b958e4f4b2206c4d7ccc9e8d1de154ef0412141f529446a330`.
- `sdist-2/cryptalis-0.1.0.tar.gz`: the same 150,427 bytes, digest and directly equal content.
- `direct-wheel/cryptalis-0.1.0-py3-none-any.whl`: 140,953 bytes; SHA256 `053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965`.
- `repeat-wheel/cryptalis-0.1.0-py3-none-any.whl`: the same 140,953 bytes, digest and directly equal content.
- `roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl`: the same 140,953 bytes, digest and directly equal content.

Each sdist has exactly 49 regular payloads and six directories, totaling 581,851 uncompressed payload bytes. Each wheel has exactly 48 regular payloads and six directories, totaling 475,528 uncompressed payload bytes. The member sets were independently derived from the 43 runtime source modules and fixed packaging files.

Finite archive paths and ordinary leaf metadata were admitted before archive reads. The independent audit checked complete TAR names/types/owner/time/mode/link/PAX/sparse/size metadata and bounded gzip expansion. It also checked ZIP central fields and local headers, matching local/central names, fields, sizes and CRCs, bounded nonoverlapping spans, modes, times, flags, compression and exact file/directory membership before reading members. No member was extracted to disk by this reviewer.

## Exact payload and roundtrip closure

The canonical comparison remains the accepted README-v2 sdist `7988fb28baa4dec5804d4779b8a1d626c7dae5e3d7d5e597a7a12a69e0d9a036` and wheel `ce4817376f25411c8685c676802cce25c1799c85a87277b1dcc099556a40229c`.

Every new sdist has exactly one changed payload, `cryptalis-0.1.0/src/cryptalis/cli.py`. Every new wheel has exactly two changed payloads, `cryptalis/cli.py` and `cryptalis-0.1.0.dist-info/RECORD`. There is no added or removed member. All unpermitted payloads directly equal the canonical comparison.

All 43 runtime modules in all five archives directly equal selected source. CLI has the exact accepted remedy-source digest `060cb66057f66c6d22c2b455bfba918545a3fabc251e72a30ab8fbfe61b0f409`; the other 42 runtime modules equal README-v2. Tests remain outside distributions. README, PKG-INFO, METADATA, license, dependency lock, original/normalized build configuration and console-entry payloads retain their exact comparison bytes. The normalized sdist TOML also equals source semantically, and the CLI entry remains `cryptalis.cli:main`.

README-v2's PKG-INFO and METADATA are identical and contain exactly its README description. Every new PKG-INFO/METADATA remains byte-identical to that accepted metadata, with unchanged headers, dependencies, version and Markdown description. The new source README has the bound digest `0101bed8e6cc533e438d9a718281f7f15781fea170de91b788389938798cdcb5`.

Each RECORD has the same ordered 48 unique rows, covers exactly its wheel, contains 47 correct URL-safe SHA256/size entries, and has empty self fields. Only the CLI row changes against README-v2. Both missing-lock and altered-lock controls produce their exact refusal reasons in the actual verifier and the independent data-only predicate check.

The actual extracted tree contains exactly the admitted 49-file sdist payload and seven directories including the extraction root. Every extracted file directly equals the first sdist after roundtrip. Successful set-e sequencing establishes completion of the accepted immediate extraction check; independent terminal readback and three-wheel byte equality close the final roundtrip result.

## Complete source and predecessor preservation

Baseline original source, selected candidate, packet source and both build copies each have exactly 221 ordinary single-link files and 22 source directories. The four remedy-source trees directly agree on all 221 files. Only README and CLI differ from original source, leaving 219 original bodies equal. Every corresponding leaf across all five trees has a distinct device/inode pair. No cache subtree or unexpected source file was admitted.

Independent manifest reconstruction reconciles exactly 247 packet rows, three outer rows, 1,198 frozen declarations and 221 rows in each baseline/derivative/candidate source group. All permitted local/source/prior-review/document/artifact payloads read under these declarations match their hashes. The 472 host-file and two tool rows were reconciled as inert declarations; current host/tool identity is supported separately by the successful exact pinned entry checks, not by reopening live host bodies in this review.

All ten predecessor distributions remain at their original identities: the five original Integrated221 artifacts and the five accepted README-v2 artifacts. Original sdists retain `1f447ac32bac75803826df6e2e66a1df5a8dd515448484c271175c279ef98b6c`; original wheels retain `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6`. README-v2 identities remain those above. No predecessor hash is replaced by a remedy-successor hash.

V1's seal `f2c617f48161a55b36539702a5b3195967edf80153e302dea4e173ab29c9f591`, all 247 sealed V1 members and its HOLD review `ce576e61697620a6254eb2b4e6ed4399ebc2832b22a9d4ca8affab08444e8d26` were independently rechecked after the V2 build and remain unchanged.

The artifact audit re-admitted/rehashed all 1,225 payloads it read at its end; recorded metadata and identities remained equal. The separate receipt audit rechecked its 52 inputs. Existing HOME/cache/tmp directories were treated as opaque directory boundaries and never descended for payload inspection.

## Actual terminal receipts and host admission

Entry capture is `persistence-recovery-20261013/doctor-remedy-build-v2-coordinator`. Its exact recorded route selects the pinned host Python 3.12 target, `-I -B -S`, the absent stage bytecode prefix and the correct preflight/outer paths and external digests. Persisted preflight, outer-admission, outer and host-after exits are all 0. Outer stdout/stderr and preflight stderr are empty.

The parent is PASS_BOUNDED_PACKAGING. Its child command is exactly the selected run-after-review.sh with the actual packet/clearance digests; child exit is 0, reason is null, leader_reaped is true, and cleanup errors/group signals are empty. The declared clean outer/child environment maps match the reviewed constants. Raw environment maps were excluded from the retained safe projection.

Preflight, parent before/after and all six individual post-build group logs agree exactly: packet247, outer3, inputs1198, baseline221, derivative221 with 219 unchanged original bodies, and candidate221. The actual verifier's output hashes, counts, payload deltas, lock controls and scope fields match independent findings. All admitted phase/postcheck stderr files are empty. The child's actual 742-byte stdout equals the preflight JSON and its recorded hash; stderr is empty with the correct digest.

Recorded versions are Python 3.12.14 and uv 0.12.23. The exact entry's successful before/repeated-before/after admission checks establish its scoped interpreter, 472 finite stdlib files and separately pinned uv file identity. The absent stage bytecode prefix was independently confirmed after terminal. No live host/tool payload was read by this reviewer, and no loaded-code or native linked-library provenance claim follows.

Actual cooperative limits are 120 seconds, 2,097,152 bytes per captured stream and 8,388,608 bytes per child regular file. Parent file limits were originally unlimited and their restoration is recorded true. No timeout, capture overflow or cleanup error is recorded. `descendants_verified_absent` remains false. Separate backend numeric exit receipts do not exist; successful set-e completion and child exit 0 are the available completion evidence.

## Database and qualification boundaries

This build route performs no database action. No fresh database-status command was launched before or after it. The most recent independently accepted stopped-state evidence remains the source GREEN terminal review. Root's initial absence of postgres/pytest/uv names is only a scoped observation, not proof of broad process-namespace visibility; it is not promoted to a new stopped-state receipt here.

The unchanged README/status binding is the earlier README-v2 snapshot, with original Integrated221 installed evidence. Its null successor hashes and earlier source manifest are not rewritten or misattributed to this executable successor. Actual remedy artifact identities live in the artifact index above. The narrow accepted source GREEN remains six cases; no new full source suite or installed suite ran in this packaging stage.

All 34 objectives remain active and all seven broad production gates remain UNKNOWN. Public quickstart remains unexecuted and fresh-fixture ACL permission remains pending. Same-host pinned-builder equality is the bounded reproduction result. Original dependency artifacts remain unavailable; clean-host and source-to-binary provenance remain unresolved. Any installation, installed runtime, publication or release decision requires separate authorization and qualification.

## Retained evidence

Both independent terminal programs completed on their first execution, exit 0 with empty stderr: `audit_artifacts.py` and `audit_receipts.py`. Their actual outcomes, source, read ledgers and safe projections are retained in `ARTIFACT_CHECKS.json`, `INPUTS.json`, `RECEIPT_CHECKS.json` and the audit stdout/stderr/exit files. `ACTUAL_ARTIFACTS.json` provides the exact machine-readable artifact identities; `V1_PRESERVATION.json` records the immutable predecessor check. `EVIDENCE.sha256` seals this finite evidence set.

All review writes are confined to this independent reviewer directory. No packet/product code was imported or run, no runtime-phase environment-bearing JSON was inspected, and no host/dependency/cache/credential/corpus/database payload was read or copied. No remote sharing or publication occurred.

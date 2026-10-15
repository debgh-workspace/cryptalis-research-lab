# Integrated221 packaging: independent terminal artifact review

Date: 2026-10-15 UTC.

## Decision

ACCEPT_SCOPED_INTEGRATED221_PACKAGING. The completed bounded build and all five actual artifacts satisfy the accepted source-command contract. The two sdists are byte-identical; direct, repeat and sdist-roundtrip wheels are byte-identical. Complete admitted payloads, exact baseline deltas, RECORD hashes, source copies, extraction, preserved entry/parent/child results and before/after integrity reconcile.

This review and ACTUAL_ARTIFACTS.json may be pinned as actual packaging evidence for separately reviewed next-stage preparation. They do not authorize installation, another build, product import, CLI/test execution, database work, promotion or release. All seven broad product gates remain UNKNOWN. Original dependency artifact downloads remain unavailable, so clean-host provenance remains BLOCKED.

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.
Packet: experiments/cluster-retained-release-plan-20261015.
Root capture: ../persistence-recovery-20261013/integrated221-build-root-admission.
Entry capture: ../persistence-recovery-20261013/integrated221-build-coordinator.

## Actual artifact identities

Paths below are relative to the packet.

- run/sdist-1/cryptalis-0.1.0.tar.gz:154158 bytes; SHA256 1f447ac32bac75803826df6e2e66a1df5a8dd515448484c271175c279ef98b6c.
- run/sdist-2/cryptalis-0.1.0.tar.gz:154158 bytes; the same SHA256 and independently checked actual byte equality.
- run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl:144298 bytes; SHA256 dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6.
- run/repeat-wheel/cryptalis-0.1.0-py3-none-any.whl:144298 bytes; the same SHA256 and independently checked actual byte equality.
- run/roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl:144298 bytes; the same SHA256 and independently checked actual byte equality.

Each sdist has49 regular files,6 directories and597313 uncompressed payload bytes. Each wheel has48 regular files,6 directories and483221 uncompressed payload bytes. ACTUAL_ARTIFACTS.json binds these observed outputs with installation_authorized=false and ALL_SEVEN_UNKNOWN; no output digest was invented in preparation.

## Packet, prerequisites and actual authorization

All identities below were read only after finite metadata admission and match current ordinary file bytes:

- PACKET.sha256: fa29107958d8d50764ed8126e216dcdce77edd2e0856aea798332455546ef117.
- frozen-inputs.sha256: 5c379cfce30af0f53e81daaad15ffdc70aaafe1cd61de4488b68d7b9a10824d2.
- INPUT_POLICY.json: 997e5dcca1c8dc0a26b319a2d1229b810bc96bc95b3e9d77c299374ab711bd32.
- Exact221 source manifest: 202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520.
- Actual BUILD_CLEARANCE.json: 9c9da019081bb699a11114b769e9c332ce7b4c4d4b33755188907a9202919384.
- Source-command review at the fixed policy path: c43e8794d80f061e3e51ed8b85a22169cf11f4f8f83de79bd29d5488077cb6e5.
- Accepted full-SA21 review: 0cfcaf87e7bffddb788da32df75d16e132e7d281160cefe64f15e81a62476de0.
- Accepted full-SA20 review: dcfd32012ee0f9fe13cc73e78013a5bee1be6dd8783552b8f0486a0a8848e625.
- Accepted optional38 source review: 459e467fff856dd8bfda53d8c53d1692e041c3a21a7a2a1e56668060c103346b.

The exact clearance schema, keys, one-bounded-build authorization, quiescence boolean, packet/source anchors, all four fixed review paths, actual digests, ACCEPTED decisions and scopes reconcile. The terminal review decisions were read. SA21 records2684 ordinary passes with zero failures/skips plus56 separate passing subtests; SA20 records2638 ordinary passes,46 specific native-version skips and zero failures/errors plus56 separate passing subtests. Optional38 records38 ordinary passes,114 passing phases and required native completion/recovery evidence. These are scoped accepted prerequisite reports, not reruns by this reviewer.

Root argv.json selects /bin/bash and the exact run-build.sh with external packet/clearance hashes. The entry-argv.txt exactly binds packet cwd and pinned Python -I -B preflight/outer commands. Current tool bytes, Python alias and all sealed source/helpers match the frozen-input map. Python3 resolves exactly to python3.12; target SHA256 fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7; uv SHA256 abdc39eab8b4ad341dca91f3823a23a343fae94bdb22ebdd9e91694415206f2f. Tools were hashed as data, never invoked by the reviewer.

Quiescence remains a coordinator attestation supported by the preserved preliminary status output; it is not continuous scheduler/process proof. Freshness was enforced by the accepted shell/outer source and successful exact route; historical directory absence was not independently observed by this artifact reviewer.

## Exact source, copies and input preservation

Independent finite-set reconstruction and metadata admission precede expanded payload hashing. Actual counts are packet250, outer3, frozen inputs697, baseline218, derivative221 and candidate221. Every current admitted hash matches. The original221 source manifest, packet source map, candidate source map and clean archive map agree exactly.

All three source inventories and both built source copies have exact declared names/types/directories. Candidate cache directories are opaque boundaries; no cache payload is inspected. Source-1 and source-2 each contain the complete221 allowed files and equal the clean source byte-for-byte. Baseline218 is independently checked against its pinned map. Relative to Transport218, the exact declared source delta is three added files and13 changed files with no removal. Packaging/runtime configuration, LICENSE, README and uv.lock remain unchanged.

The audit re-admits and rehashes1249 finite paths at final closure, including source trees/copies, sealed controls, prerequisite reviews, tools, baseline archives, all new archives, extracted files and safe receipts/logs. DATA_AUDIT.json retains per-path hashes and metadata. No broad unvalidated manifest-follow was used.

## Complete archive admission, closure and exact delta

Each archive path and output-directory inventory is admitted before compressed-file reads. Before any member payload is read, all member names, duplicates, full file/directory sets, safe relative paths, types, modes, times, sizes and applicable owner/ZIP attributes are validated. Symlinks, sparse entries, extra/PAX attributes and unexpected entries are refused.

Wheel local headers independently match central-directory names, UTF-8 flags, method, CRC, compressed/uncompressed sizes, DOS date/time and zero local extras. Local payload spans remain before the central directory and do not overlap. Payload reads additionally check actual lengths and ZIP CRCs. No packet extraction helper is executed by the reviewer.

Archive sets independently derive from43 source modules plus fixed metadata/configuration files. Baseline218 uses its distinct41-module/47-sdist/46-wheel inventory. Its accepted sdist (149965 bytes, fddf753a815e4babcb628f248c399d8cb9d31f6ab7621824c6327ba4b0debf34) and wheel (139445 bytes,73c066adfce04d4efc3dd02c713e0d8ae0610497fb045ebb1484f54a8bb55e88) are rehashed and fully inspected.

Every new artifact contains exact clean-source bytes for all43 runtime modules. The only archive additions are _cluster_designation.py and _legacy_designation.py. The only modified runtime files are _object_comments.py, deprotection.py, migration.py and sqlalchemy.py. Wheel RECORD also changes. No member is removed and no other member payload changes. Baseline runtime payloads independently equal baseline source.

All three new wheels have48 unique RECORD rows covering their exact payload set:47 correct SHA256/size rows and empty self fields. The baseline wheel has46 unique rows,45 hashes and empty self fields. Tests are excluded from every runtime archive. Lock SHA256 remains faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e. Original pyproject bytes, normalized TOML meaning, LICENSE, README and package metadata reconcile across source, sdists and wheels. The static and packaged console entry point is exactly cryptalis=cryptalis.cli:main. CLI and __main__ source bytes are covered; no CLI execution claim follows.

The final extracted tree has exactly49 regular payload files and7 directories including its root. Every file equals the first admitted sdist after the roundtrip build. No extra file or changed extracted payload remains.

## Actual statuses, logs and bounded execution

Root entry-exit.txt is0. Entry preflight-exit.txt, outer-admission-exit.txt and outer-exit.txt are each0. Root entry streams, entry preflight stderr and entry outer streams are empty. The preserved pre-status-exit.txt is exactly the byte3 without a newline; pre-status stdout is exactly "pg_ctl: no server running" plus newline, with empty stderr. This independent pre-build no-server status is retained as3, not normalized to0 or misrepresented as a build failure.

The parent receipt is PASS_BOUNDED_PACKAGING with empty errors. Before/after groups exactly equal packet250, outer3, inputs697, baseline218, derivative221 and candidate221, each passing without errors. The child selected the exact sealed inner shell with actual external digests, exited0, reason=null, leader_reaped=true, cleanup_errors=[] and group_signals=[]. descendants_verified_absent=false remains explicit.

Child stdout is694 bytes, SHA25601cf4dca4cda49d9e240cea54c7e3c198cc3a43e4f4bf64aa12486554874ca23, exactly equal to the independently captured preflight stdout. Child stderr is empty, and both declared stream byte counts/hashes are recalculated. All safe run logs and16 stderr files are admitted; all16 are empty. Six final single-group postchecks have exact expected counts and no errors. Source-copy, extraction and five artifact-filename logs match. Actual version logs report uv0.12.23 and Python3.12.14.

The verifier receipt is PASS_SCOPED_PACKAGING and exactly matches independently observed source/runtime/archive counts, hashes, deltas, CLI declaration and three-wheel/two-sdist equality. Successful set-e sequence plus actual terminal statuses supports completion of sequential commands; individual backend commands have no separate numerical exit receipt, and none is invented.

The unchanged pinned supervisor remains b5cc92887125d1b923cb49f9d673a922a75d55f31f19efb4934992c02a1f0065. Recorded bounds are120-second configured child deadline,2097152 bytes per captured stream and8388608 bytes per inherited regular file. Parent original limits[-1,-1] were restored. The allowed fixed outer/child environment maps match exactly, including SOURCE_DATE_EPOCH=0 and UV_OFFLINE=1; inner source replaces HOME/TMPDIR/UV_CACHE_DIR with its fresh run paths. No ambient environment dump or home/cache/tmp payload is read.

These are cooperative bounds, not aggregate resource quotas, OS network isolation or hostile-code containment.120 seconds is configured rather than measured duration. Leader reaping does not prove absence of all descendants.

## Negative controls, failed attempt and limits

The actual verifier records missing_lock and altered_lock rejected. Its exact sealed source is inspected as AST/text and constructs the two real in-memory mutations with specific refusal reasons. Independently, the reviewer applies the corresponding missing/changed-lock predicates to actual admitted sdist bytes; both reject. This does not execute or rerun the packet verifier.

Independent audit attempt1 stopped solely because its reviewer assertion required b'3\\n' for the preliminary status file. The failure was reported before correction, and audit_data_only-attempt-1.py, stdout/stderr/exit remain preserved. Explicit admitted byte inspection confirmed b'3', the no-server stdout and empty stderr. Only that reviewer formatting expectation changed; no product source, packet, baseline, runtime receipt or artifact changed. Attempt2 passed with exit0 and empty stderr. ATTEMPTS.md retains this correction. The earlier source-review metadata-admission incident remains preserved in its separately bound source report; it is not erased or retroactively recharacterized.

The artifact audit began only after the root terminal notice. All artifact-review payload reads used explicit finite metadata admission. No forbidden raw phase JSON/tests.json/readiness/package-origin/postgres-start/stop JSON, credential/key payload, ambient ENV or cache body was read, hashed or copied. No product import, preserved helper execution, build, installation, test, DB/process probe, Git or network action was performed by the reviewer. Writes are confined to this independent reviewer directory.

Same-host pinned-builder artifact equality is established. Independent-host reproducibility, source-to-binary builder provenance, installed221 runtime qualification and production readiness are not established. Future work must bind this actual review and ACTUAL_ARTIFACTS.json and receive separately accepted next-stage commands and explicit selection.

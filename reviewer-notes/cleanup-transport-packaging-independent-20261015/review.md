# Independent terminal review: transport218 packaging V2

Date: 2026-10-15 UTC. Method: data-only review of the completed packaging record and actual artifacts.

## Decision

**ACCEPT_SCOPED_TRANSPORT218_PACKAGING_V2.** The exact completed V2 package artifacts satisfy the accepted source/command contract. The two sdists are byte-identical, and the direct and sdist-roundtrip wheels are byte-identical. Their complete contents reconcile with source218 and accepted217. The preserved coordinator exits, bounded parent receipt, input guards, copies, extraction and final checks reconcile.

This immutable final review may be bound by its actual SHA256 for a separately reviewed installer preparation. It does not authorize installation, a runtime test, another build, product import, database work, promotion or release. Seven historical failures remain open. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE remain UNKNOWN.

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.
Packet: experiments/cleanup-transport-release-plan-v2-20261015.
Coordinator capture: ../persistence-recovery-20261013/transport218-build-v2-coordinator.

## Actual accepted artifacts

All paths in this section are relative to the V2 packet.

- run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl: 139445 bytes; SHA256 73c066adfce04d4efc3dd02c713e0d8ae0610497fb045ebb1484f54a8bb55e88.
- run/roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl: 139445 bytes; the same SHA256, with actual byte equality checked.
- run/sdist-1/cryptalis-0.1.0.tar.gz: 149965 bytes; SHA256 fddf753a815e4babcb628f248c399d8cb9d31f6ab7621824c6327ba4b0debf34.
- run/sdist-2/cryptalis-0.1.0.tar.gz: 149965 bytes; the same SHA256, with actual byte equality checked.

ACTUAL_ARTIFACTS.json is the machine-readable binding for these four actual outputs. It retains installation_authorized=false and ALL_SEVEN_UNKNOWN. These hashes are observed results, not values invented in preparation.

## Packet, command and genuine clearance binding

The following exact identities match current admitted bytes:

- PACKET.sha256: 5bd4c2fc946c97707b1f4e8c9bb7c0be7d9253bc5838da0b6efd4d2775d46af8.
- frozen-inputs.sha256: 630e77622e3abfb31d58fd985dbd2a65dd109c274cd1965ccfa97c76202abaf7.
- outer-frozen.sha256: 682f0bb37242c34accf5919dfa6cfd0069c552f22fc840ecc044ecc4ca3f4799.
- INPUT_POLICY.json: 2ec0dee1dd0d8cbc5277dd4c7bb32bcd5a67830ffc6829b5c84c609327d9de53.
- CANDIDATE_SOURCE_MANIFEST.json: b8a8a6b00c597b63f4851defb74a2baa3dde8f3ff4c2e46d789699792600a204.
- BUILD_CLEARANCE.json: ce3a0e46ec9da8873b49954cce6ca8fe2011d91ad6c394d3bb2dfd24da7f3eb4.
- Accepted source-command review: reviewer-notes/cleanup-transport-release-plan-v2-independent-20261015/SOURCE_COMMAND_REVIEW.md; SHA256 1f1ba6d41637a4eb8ae46b9dc9dc20be28b52f53b840d942f3c82e2a6b42e787.

The exact clearance keys, schema, authorization, quiescence boolean, packet/source identities and four review objects pass. Each review object names its genuine current pathname, actual digest, ACCEPTED decision and exact scope:

- source_sa21: reviewer-notes/cleanup-transport-full-v2-sa21-independent-20261015/review.md; 99d6b5530db189ccc74ba356d2d76424135ce9b7aa9dd9a13c543fedd736c422.
- source_sa20: reviewer-notes/cleanup-transport-full-v2-sa20-independent-20261015/review.md; 098f2b601b47fb695f10617add969771d411b57f5c40bfd9d98174192b24301d.
- source_optional38: reviewer-notes/cleanup-transport-optional38-terminal-independent-20261015/review.md; de70ac6c09f980e96e96ffb173b2afd88149340f67f1dfd04d417b0b9662dd00.
- source_command: the actual V2 report above, with its final digest.

Their actual decision sections were read. The SA21 and SA20 reviews retain seven historical failures; SA20 also retains 46 skips. Optional38 is scoped source evidence for 38 ordinary passes and 114 passing phases. This packaging audit binds those accepted reports for their stated scope; it does not rerun or re-audit their runtime evidence.

The coordinator selection records the exact primary Python -I -B preflight and outer argv, the exact V2 entry paths, and these actual packet/clearance values. The nine tool/entry/packet/review metadata records and all corresponding byte hashes reconcile with current ordinary paths. The Python alias is exactly python3 -> python3.12. The current target hash is fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7; current uv is abdc39eab8b4ad341dca91f3823a23a343fae94bdb22ebdd9e91694415206f2f. Tools were read as data, not invoked for packaging by this reviewer.

The recorded selected command is the reviewed route. No direct-inner/helper/uv fallback is shown by these receipts. Quiescence is an explicit coordinator attestation, not continuous scheduler or live-process proof. The accepted outer enforces absent run/ and parent-results/ before creating exclusive outputs; this reviewer did not observe their historical absence independently.

## Complete source and input preservation

The independent checker first constructs and compares exact allowed sets, admits complete path/type metadata, and only then hashes expanded inputs. All 243 packet members, all 688 frozen inputs and all three outer-frozen targets match. The packet consists of 25 controls and 218 clean source files, plus its separate seal. The only additive packet root entries are the genuine clearance and the two accepted runtime-output directories.

The full baseline217, candidate218 and clean218 source trees have exact inventories. Both built source-1 and source-2 copies contain all 218 permitted files and are byte-identical to clean218. Each source tree has 22 directories including its root. Candidate cache boundaries are ordinary directories and are excluded from payload access. Clean and copied trees contain no added entry or cache.

Relative to accepted217, exactly src/cryptalis/crypto/keys.py changes and exactly tests/test_crypto_failure_transport.py is added. No file is removed. All 41 runtime module names remain unchanged. The complete 218-file source copies include the new test; runtime archives exclude tests.

The checker independently retains and rehashes 1218 admitted file paths at closure. This covers the complete sealed packet, expanded frozen inputs, current tools, prerequisite reviews, coordinator captures, safe runtime receipts/logs, both copied source trees, all six new/baseline archives, and the extracted tree. Metadata and per-file SHA256 identities are retained in DATA_AUDIT.json.

## Metadata-first archives and exact accepted217 delta

All four output archive names and containing-directory inventories were admitted before archive bytes. Every archive member name, type, duplicate check, mode, size, directory set, timestamp and relevant attribute was admitted before any member payload was read. Wheel local headers additionally match their central directory names, flags, method, CRC, sizes, dates and offsets. No archive extraction helper was executed.

Each wheel contains exactly 46 regular payload files and six directory entries, with 466797 uncompressed payload bytes. Each sdist contains exactly 47 regular payload files and six directory entries, with 581068 uncompressed payload bytes. Their exact name sets are independently derived from the 41 admitted source modules and fixed metadata/configuration names, and agree with the sealed policy.

Both wheels have exactly 46 unique RECORD rows covering the complete payload set: 45 valid SHA256-and-size entries and empty self fields. Both archives' 41 Python module payloads equal clean218. The lock matches faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e; original configuration bytes, normalized configuration meaning, license, README and package metadata reconcile across source and artifacts.

The accepted217 baseline wheel is 139308 bytes, SHA256 77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b. The baseline sdist is 149820 bytes, SHA256 f921da5830bcb3b0c7befb10e05f23346b2ab874c487175217be4a5e752706f7. Their complete archive headers, baseline217 source-module payloads and wheel RECORD are independently rechecked.

No archive member is added or removed. For each new sdist, the sole payload delta from accepted217 is cryptalis-0.1.0/src/cryptalis/crypto/keys.py. For each new wheel, the only payload deltas are cryptalis/crypto/keys.py and cryptalis-0.1.0.dist-info/RECORD. All dependency and packaging metadata payloads remain exact baseline bytes.

The final extracted tree has exactly the 47 admitted sdist payload files and seven directories including the extraction root. Every final file equals the first sdist payload after the roundtrip build. No extra build output or modified extracted source is present.

## Actual terminal receipts, logs and bounds

The retained preflight-exit.txt and outer-exit.txt each contain exactly 0 plus newline. The outer log is empty. The bounded parent status is PASS_BOUNDED_PACKAGING. Its before and after arrays contain every expected group, exact count, pass=true and no errors: packet243, outer3, inputs688, baseline217, derivative218 and candidate218.

The exact child argv is /bin/bash, the sealed V2 run-after-review.sh, and the actual packet and clearance digests. The child exit is 0, reason is null, leader_reaped is true, cleanup_errors is empty and group_signals is empty. Parent errors are empty. These are the preserved completed-run receipts; this reviewer did not start or inspect a live build process.

The captured child stdout is exactly 694 bytes and matches the separately captured preflight log. Its SHA256 is 053f6341f131448f66ae63482a4bbb1d5dace66fa8e690eb685dc22df7592a8c. Child stderr is empty and has the empty-byte SHA256. Both byte counts and hashes are independently recalculated. All exact safe run logs are retained and hashed. All 15 safe stderr files are empty. Six shell postcheck logs each contain their exact single passing group, count, empty errors and scoped authorization. Copy, extraction and archive-filename log text reconcile. Observed version logs report Python 3.12.14 and uv 0.12.23.

The unchanged set-e shell sequence and successful outer/child terminal result support completion of all sequential build/verification steps. Individual backend commands have no separate numerical exit receipt, so this review does not invent one. The actual verification.json reports PASS_SCOPED_PACKAGING and exactly matches the independently observed archive/source/count/delta results.

The accepted supervisor remains b5cc92887125d1b923cb49f9d673a922a75d55f31f19efb4934992c02a1f0065. The receipt retains a 120-second configured child deadline, 2097152-byte cap for each captured stream, and 8388608-byte inherited regular-file limit. Original parent file limits are [-1,-1], and parent_fsize_limits_restored is true. All admitted safe outputs obey the recorded file-size ceiling. These are cooperative bounds; they are not aggregate quotas, network isolation or hostile-code containment. The value 120 is not measured elapsed time. descendants_verified_absent remains false.

Only the declared fixed scrubbed child/outer environment constants were compared inside the explicitly allowed parent receipt. No ambient environment was dumped. UV_OFFLINE=1 and the exact pinned bundled build-backend route remain recorded. This does not prove OS-level network isolation or source-to-binary provenance.

## Negative controls, attempts and limitations

The accepted verifier source is statically parsed and hash-bound. Its actual result records missing_lock and altered_lock as rejected, and its exact source constructs those two in-memory cases and checks their precise rejection reasons. This audit does not independently rerun the verifier or those controls. All seven Python helpers parse as data-only ASTs; none is imported or executed.

The independent full audit passed its first attempt, exit 0 with empty stderr. Its source, stdout, stderr and exit are preserved. A preliminary root AGENTS.md probe failed before payload reads because that exact file is absent; the permitted source snapshot's AGENTS.md was then read as source data. DISCOVERY_NOTES.md retains this probe and the initial bounded metadata-only survey. That preliminary maxdepth-2 survey did not explicitly prune home/cache/tmp; no payload from those directories was read, hashed or copied. The complete audit uses explicit skip boundaries without listing their children. This methodological caveat is retained rather than claiming the initial survey followed the stronger prune rule.

No product code, preserved helper, build, installer, test, database/server, network or Git operation was executed by this reviewer. No forbidden raw phase JSON, secret, ambient environment dump or cache payload was read, hashed or copied. Writes are confined to this independent reviewer directory. The original packet, clearance, run, captures, previous attempts and prior reviews were not changed.

The result establishes same-host pinned-builder artifact byte equality and exact scoped payload preservation. It does not establish independent-host reproducibility, builder/dependency provenance, full source218 runtime success, installed218 qualification or production readiness. Future work must bind this exact final review and ACTUAL_ARTIFACTS.json; a separately accepted command and explicit next-stage selection are still required.

## Retained independent evidence

- audit_data_only.py: 72a4ef2f2130ac1f646b4aabe3c03c36de290862c97f4bb2f92fa4750842ac3d.
- DATA_AUDIT.json: 91dbf16ffc6e9d02e613273cbbb62079a1705d9aa81241855f989f924c527ab7.
- ACTUAL_ARTIFACTS.json: 31037adc3a4836bccb892e74a355223c2da2c236bb0f4a8d00d271daf4505a2f.
- DISCOVERY_NOTES.md: 4ee88af84ea8c916357655436a89375db6c0490e14179847435571ec7fd88c13.
- audit-attempt-1.log: 03060830b4034a16a77e46930071ec4fa9e579c9819a25c1cbb607a431fe4ec8.
- audit-attempt-1.stderr: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
- audit-attempt-1.exit: 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa.
- Coordinator selection: 7b3d4ead6fa2c084f55b371c665d43fefe4e93e667d18302051f7295cf869b04.
- Parent receipt: 53f6c4d940cb78efd6bbd695ace62a66dc9f6966f8455ca6a5836f0d0ebd3fda.
- Verification receipt: 3a20a382cb6e732999ba6922a6ac27cfebfcce3ba8752e2026863ace38f1fbd0.

FINAL_CLOSURE.json and REVIEW_FILES.sha256 bind the final report and reviewer evidence. The report has no placeholder result hash and will not be revised in place.

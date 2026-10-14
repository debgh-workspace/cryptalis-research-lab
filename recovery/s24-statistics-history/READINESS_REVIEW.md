# S24 statistics history: independent publication and restore readiness

Review date: 2026-10-14 UTC.

## Disposition

CLEAR for publication review of the exact frozen archive and exact two-part/manifest set identified below. This is an independent technical clearance, not an instruction or authorization to publish.

CLEAR for the exact pinned restore source, conditionally limited to data-only restoration after the coordinator authenticates actual remote readbacks and their remote commit/provenance. Execution is NOT READY now: the remote-parts directory and all three remote-restore output paths are absent. No remote access or restore execution was attempted.

The final archive boundary review and static restore-source review are COMPLETE in this report. Prior saved artifacts prove the archive audit, sensitive-pattern scan, local fresh extraction/readback, and manifest-only reconstruction had completed. They do not prove the earlier final publication/source review was durably completed before interruption: AUDIT_v1.json still says "Pending final report-level boundary review", and that prior reviewer directory contains no final report/source-review receipt. A prior verbal CLEAR reported by the coordinator is not substituted for the current byte-bound findings.

## Verification performed now

- Confirmed exactly three regular entries in s24-statistics-history-parts: MANIFEST.json and exactly part-01.bin/part-02.bin. Both hashes/sizes agree with the manifest. Their ordered in-memory concatenation is byte-for-byte the frozen 128,896-byte archive. No combined archive was written.
- Re-read and hashed the frozen archive and metadata. A bounded, single XZ stream with no unused trailing stream contains 301 unique, case-distinct regular files totaling 3,316,383 bytes. Canonical relative names, no unsafe path components or file/directory collision, no links/sparse members, mode 0644, zero uid/gid/mtime, empty uname/gname, and only absent PAX headers or the exact path-only PAX mapping are required. The tar tail is at least 1,024 zero bytes. Individual payload file bound is 94,858 bytes.
- Archive member names/types were checked before reading member bodies. Raw phase JSON, environment files, secrets/cache/runtime/dependency paths, database/bytecode files, and nested archives are excluded. No excluded raw phase file was read or hashed.
- Verified all 300 payload entries and hashes, the separate 67,125-byte payload manifest, exact 293-entry allowlist/inventory closure, 3,249,258 payload bytes, and 3,156,719 preserved original bytes.
- Re-read only the exact 293 approved original paths and their preserved copies using regular-file/nonsymlink checks. Every current original and preserved byte string matches its inventory size/hash. No original was modified.
- Reverified both pre-existing extraction trees against all 301 archived files, including exact file sets and nonexecutable regular-file contents. No extraction was created in this review.
- Repeated the six previously reviewed credential/private-key/token/URI/bearer/JWT/assignment pattern families over all 301 allowed archive bodies. Zero findings. This is bounded pattern screening, not universal proof of absence of secrets. The known synthetic statistics marker remains a source-pinned test control.
- Recomputed all four manifest-only comparisons: the same 214 baseline reference hashes plus one preserved private observer hash exactly equal each version's 215-entry candidate manifest. No full baseline source was restored.
- Read the complete restore source and parsed it with the standard-library AST parser only. The restore module and archived code were not imported or executed. No tests, builds, installs, database operations, network calls, remote writes, or candidate imports occurred.

## Frozen publication identities

All paths below are relative to /workspace/scratch/cb28ee9f5f4a unless stated otherwise.

Candidate root: cryptalis-executable/candidate-s24-statistics-recovery-20261014

- CRYPTALIS_S24_STATISTICS_RECOVERY_20261014_v1.tar.xz: 128896 bytes; SHA-256 ececa28b6f0374274c5dc86935c5cf7098e011e4a96f41c9e5950aeeff76ac0f
- PAYLOAD_MANIFEST-v1.json: 67125 bytes; SHA-256 139653b4b900159e15ea8c9d39b7a7703b67a61b6db57ac92c75c31bea5d275b
- ALLOWLIST.txt: 23774 bytes; SHA-256 9ce9ddd2968c4f7fba68e618056688503a2b93c8e0abb98606b4b425b292cd53
- SOURCE_INVENTORY.json: 60087 bytes; SHA-256 b48ba3f6765c8de7165bc996c080ba2ab602a38f715bac4e9feeb5ec08e42eb2
- FREEZE_SCOPE.json: 593 bytes; SHA-256 5f2c72e8f28982cd05c9b1e63e2955dcdbbf0d1c18030bb8f010c102917f8d48
- TEMPORAL_SCOPE.md: 883 bytes; SHA-256 6c9348b05b3a72f2fc142fde5c850c6c919ba461f54759c32ccdb712d0526f1f
- RECOVERY.md: 5805 bytes; SHA-256 9b4d771bc802c0adef0006b6d4291e9ee9dbe33a4e35dfc5ef7f9b5a03180343
- SENSITIVE_SCAN.json: 881 bytes; SHA-256 1288268b54e8d80c7b55e2fa3478facc09fbbfd7ac721b0d85a30a8f440498ac
- RESTORE_VERIFICATION-v1.json: 2352 bytes; SHA-256 e950e096355935f4dea64c81d1cd15ffd57cfe7a99ef6ec9b00227637442b73c

Split publication root: persistence-recovery-20261013/s24-statistics-history-parts

- MANIFEST.json: 641 bytes; SHA-256 181af9ec2c00da21e158044740f4a365aa3fd04a4058728a35c70b82dca6099b
- part-01.bin: 96000 bytes; SHA-256 ac6ed624ae960725675ec8a34a7faeffc945c39922de1eb8ebd04d09d6017351
- part-02.bin: 32896 bytes; SHA-256 d181487cf36be05cd12f06c7c64929f728a82e76d16a396bd7e05735e9cf320a

The local part files are publication material, not remote-readback evidence. Copying them into the expected remote-input directory would not authenticate a remote restore.

## Restore-source pin and permitted path contract

Reviewed executable source path:
cryptalis-executable/reviewer-notes/s24-statistics-recovery-independent-20261014/s24-statistics-history-remote-restore-v1.py

19759 bytes; SHA-256 f75bac49fb9838c1673666be297315760932a72eb38e25084e043d89b3d3714d.

This clearance applies to that exact script and its frozen input identities only. The source calls only standard-library file/hash/JSON/XZ/tar functions. There is no network, subprocess, database, dynamic module loading, archive-code import, eval/exec, or general tar extraction call. Its main routine was not run. The documented isolated interpreter boundary is python -I -S; no execution is authorized by this report.

Permitted data inputs, under the absolute prefix /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/:

1. s24-statistics-history-parts/MANIFEST.json, pinned above.
2. s24-statistics-history-remote-parts/part-01.bin, authenticated actual remote readback, exactly 96000 bytes and the pinned part-01 hash.
3. s24-statistics-history-remote-parts/part-02.bin, authenticated actual remote readback, exactly 32896 bytes and the pinned part-02 hash.

Only these new output paths are permitted by the source under the same prefix:

1. s24-statistics-history-remote-reconstructed.tar.xz
2. s24-statistics-history-remote-fresh-extraction/ and exactly its 301 pinned archive member files plus necessary parent directories
3. s24-statistics-history-remote-restore.json

All three output roots must be absent. They were absent at review. No candidate/source tree outside that fresh extraction root is reconstructed or written. Input/output ancestors must be real directories; inputs must be bounded regular files and use O_NOFOLLOW. Output files use O_EXCL/O_NOFOLLOW with mode 0600; fresh directories use mode 0700. Existing output paths are refused. All archive identities, member metadata, full payload hashes, exact allowlist closure, temporal metadata, and all four 214+1 comparisons are validated in memory before any output is created. It then checks the complete fresh tree and file readbacks before writing its completion receipt.

The script does not itself authenticate a remote commit or authorize publication; its receipt explicitly says both are false. The coordinator must establish actual remote provenance separately and keep the exact input/output namespace free of concurrent writers. A failed execution after output creation may leave partial new outputs; the script intentionally refuses reuse, so any cleanup/retry decision needs separate review rather than overwriting them.

## Baseline and overlay identity limits

The preserved baseline reference manifest is 24243 bytes, SHA-256 6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d, at preserved/experiments/s24-statistics-diagnostic-20261014/BASELINE_SOURCE_MANIFEST.json inside the capsule. It contains 214 hashes, not their source bytes.

Version candidate-manifest SHA-256 values:

- V1: 063e1202a923f82cf07b0e2ae1eb942f90a728c40b6aade29382809e4635ad1e
- V2: edf8f3f57c0eb8db5526b358b20a1d4198a989cc701201c1b0718f30b96f729d
- V3: f43e8d22b6483c66cedd1b59bd3a8a52397e17478b696edc1f1de0a962254009
- V4: 2dcf80b1b200dd5d35db175cb95b7200db31e83a3a64d3ffa49a8dd6a87155e1

The only candidate-source members are the four private src/cryptalis/_statistics_diagnostic.py overlays: V1 is 10823 bytes, SHA-256 7db1c1600add557750a263078c63e10ef7664270b01a468dd1a4a970bd77421a; V2/V3/V4 are each 14714 bytes, SHA-256 6534250833d3a2362f838a1574a5b0bdd028b8016a8502167539b6a41140f962.

No complete baseline source, dependencies, runtime state, runnable checkout, installed package, or product execution is established by this capsule or review.

## Temporal and qualification boundary

The freeze selected G1/SA21 execution evidence only, for V3 and V4. Later G1/SA20 and G2 execution evidence are excluded. Historical NOT RUN wording is scoped to selection, not a statement about the current global queue. The earlier RECOVERY.md pending-review wording is preserved as history; FREEZE_SCOPE.json and TEMPORAL_SCOPE.md record the later local freeze authorization without expanding evidence or authorizing publication/code execution.

V1/V2 static HOLD history remains. V3 remains 20 failed/9 passed, wrapper exit 1; possible earlier-assertion masking remains unresolved. V4 retains 33 passed, all 29 original cases plus four helper controls, wrapper exit 0, and 33 xunit2/record_property warnings. V4 does not retroactively reclassify V3, prove strict xunit2 schema conformance, establish universal product cleanup success, qualify G2-G6, or qualify an integrated S25 feature. These existing safe-result findings were reviewed as historical evidence; no tests were rerun.

## Prior completion evidence retained unchanged

Prior reviewer root: cryptalis-executable/reviewer-notes/s24-statistics-recovery-independent-20261014

- AUDIT_v1.json: 4404 bytes; SHA-256 36d377e810e97b595706304279dbc638aca27d00a93afd6a74c22840ab8060af
- PATTERN_SCAN_v1.json: 239 bytes; SHA-256 a1fbd76cb92b361a82879627213362fed9b74d7b43e335270d33b34eecd50a0b
- MANIFEST_RECONSTRUCTION_v1.json: 1936 bytes; SHA-256 b40bedbfde0641b4141e75f4ed42c71d0a2ded875bd4a5624da1d6a037f71074
- audit_archive.py: 18385 bytes; SHA-256 8d041fcb3f0cdbb4229a0ba79652a66db71aba2df1e43bd9fb6f05c052f6f4eb

Both existing 301-file trees were fully compared without alteration: this prior reviewer's fresh-extraction-v1 and the candidate capsule's restore-verification-v1.

Only this new report was written by the readiness review. All existing archive, manifest, source, part, receipt, and evidence files remain unchanged.

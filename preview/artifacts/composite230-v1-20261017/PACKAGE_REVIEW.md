# Independent composite230 five-build terminal review

Decision: ACCEPTED SAME-HOST OFFLINE PACKAGING AND SDIST ROUNDTRIP. No rebuild, target import, controller execution or test rerun was performed by this reviewer. Source acceptance remains 87a3954c6712d1cc358b89cc33ccd48912f6a30b8fae87ab480242a7f41503ab (8470 bytes). All original captures and packets remain unchanged.

## Actual invocation and result

Root capture: persistence-recovery-20261013/composite230-packaging-v1-20261017-1831.
Controller and external aftercheck exit files both contain 0; outer stderr is empty. Guard child exit0, reason null, leader_reaped true, cleanup_errors empty, received_signal null, empty child stdout/stderr, cold bytecode prefix absent. No timeout or cancellation was reported. Descendant absence remains explicitly unproven.

The retained INVOCATION.json has the historical recipe marker RECIPE_ONLY_NOT_EXECUTED. It is not used as proof of execution: actual exit files, guard terminal, build commands, artifacts and preservation records establish this run. Its exact command binds the accepted controller/source review and all four actual prerequisite receipt/review hashes. Recording19 review accepts the actual230 run; public38 review explicitly transfers unchanged-source evidence from the prior229 execution without inventing a230 rerun.

The build receipt records exactly five commands, all exit0: sdist-1 and direct-wheel from run/source-1; sdist-2 and repeat-wheel from run/source-2; roundtrip-wheel from run/extracted/cryptalis-0.1.0. Every command retains the approved offline/no-sources/no-config/no-cache flags. No installed-package execution is inferred from those builds.

## Exact artifacts

All paths below are relative to cryptalis-executable/recovery-work/composite230-offline-package-controls-v1-20261017/run/.

- sdist-1/cryptalis-0.1.0.tar.gz: 156831 bytes, SHA256 7a39675dbaa646eecc39667184bb43db029e75d827804b0d5cb4c578b2777c05
- sdist-2/cryptalis-0.1.0.tar.gz: 156831 bytes, same SHA256; actual bytes equal sdist-1.
- direct-wheel/cryptalis-0.1.0-py3-none-any.whl: 150261 bytes, SHA256 534e61aa90279fc084b164a07fbc2959d641585778914460d3f0730544e91507
- repeat-wheel/cryptalis-0.1.0-py3-none-any.whl: 150261 bytes, same SHA256; actual bytes equal direct-wheel.
- roundtrip-wheel/cryptalis-0.1.0-py3-none-any.whl: 150261 bytes, same SHA256; actual bytes equal both direct wheels.

Independently read/hash-compared all five artifacts to their receipt identities. Each output directory contains only its named artifact and a one-byte '*' .gitignore, which was independently read and checked. The equality is actual byte equality, not just matching recorded hash labels. This review authorizes no upload or publication.

## Independent payload and restoration checks

Data-only archive inspection verified both sdists have exactly54 regular files plus6 directories (60 headers), and all three wheels exactly53 regular files plus6 directories (59 headers). Every header tuple matches the prebound accepted HEADER_TEMPLATES map and exact member set. No duplicate/extra names appear. Tar single-stream gzip bounds, padding, member offsets, types and end padding were independently checked; wheel members were read through CRC-checking zipfile. The accepted child parser's stricter local/central/EOCD checks, missing/altered lock controls and complete header-before-payload admission are supported by its pinned source and successful receipt; this review did not rerun that parser.

All48 runtime payloads in every artifact hash-match the actual source manifest. Each wheel RECORD has53 unique exact rows,52 valid payload digest/size entries and the empty self entry. Compared old accepted combined222 payloads independently: common sdist difference is exactly src/cryptalis/doctor.py; common wheel differences are exactly cryptalis/doctor.py and RECORD. The five added _journal modules are the only new runtime names. Fixed release metadata, license, README, uv.lock and build configuration remain equal to the old package payloads. Source-map and fixed-map checks preserve docs/tests exclusion.

All54 restored payload files equal the accepted sdist-1 bytes. The roundtrip source path is the restored sdist root above, not either full230 source copy. Restoring the distribution does not reconstruct the complete230 source/test/doc tree.

## Preservation closure

Independently reconciled all273 outer rows with273 successful after rows and all272 guard input after rows. Their sole set difference is the externally guarded PACKET.sha256. All inner metadata_equal and bytes_equal values are true. Root's after rows all report pass and final_metadata true.

Independently reconciled all514 owned records with the fixed EXPECTED_OWNED map:230 source-1 leaves,230 source-2 leaves and54 extracted leaves. All metadata_ok/hash_equal flags and all three namespace outcomes are true. Independently enumerated those trees and checked their exact file and directory sets.

Then independently admitted current metadata of the combined787 leaves (273 original/control plus514 owned) before reading any of their bodies: ordinary directory ancestors, regular single-link exact-size leaves. Read each with O_NOFOLLOW and descriptor identity/stability checks, verified every expected hash, and checked all final dev/inode/mode/link-count/size/mtime-ns/ctime-ns tuples unchanged. All787 passed. This is current read stability plus the retained before/after evidence, not an inference of historical native behavior.

All five outer artifact observations and sidecar checks succeed. All five child completed_output_after and three owned_after records succeed. Original patch, source, predecessor archives, prior failure receipts and accepted review inputs remain within the verified preservation closure. No cleanup, normalization, retry or replacement of failed predecessors occurred.

## Retained evidence identities

- guard/run/terminal.json: 289693 bytes, SHA256 d9c05aae11f020a6a61f5e5a29675c3c54d609c4214cdcebd99af53a2cb05297
- run/build-receipt.json: 5142 bytes, SHA256 757e26520f011f034b26e4ed3461c64945fe718e6a55def12e810a7ac15f32de
- capture before.json: 139823 bytes, SHA256 8efa70b0d35bd3bcee7ccd1ceea587b4ae8b8058d51accac9b8e6fca70e0ac97
- capture after.json: 52996 bytes, SHA256 070b2b3d8481261a2e9b6fe52ae0e6320baf0c67054fbf865351a09b6c981e82
- capture INVOCATION.json: 1529 bytes, SHA256 e8eb93850854791b34f7a4f4e93b0329793416e07974ef05f005461341b80b6f

## Scope

Accepted: the selected230 composition's reproducible five-build packaging and validated sdist-to-wheel roundtrip on the admitted existing host. This adds no installed-origin, package-manager, native database, full-suite, release publication or production qualification. No source preview/pointer is promoted by this review. Existing objectives and all seven production gate statuses remain unchanged.

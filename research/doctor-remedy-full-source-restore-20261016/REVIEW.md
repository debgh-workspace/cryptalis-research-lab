# Doctor full-source inert recovery: independent review

Date: 2026-10-16 UTC.

Decision: ACCEPTED_REVERIFIED_BASELINE_PLUS_REMOTE_OVERLAY_FULL_SOURCE221_RESTORE.

Recovered exactly 221 ordinary nonexecutable 0600 source files, 4,451,072 bytes, in restored-source221. Every path, size and SHA256 was reread and matches the complete accepted candidate manifest. All restored source inodes are distinct from the admitted baseline. Exactly 220 source files are unchanged from README-v2; the only change is src/cryptalis/cli.py. All 116 test-tree files remain unchanged. The separately published regression test is retained as publication evidence only, not inserted into source221.

- Exact candidate manifest SHA256: 40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7.
- CLI SHA256: 060cb66057f66c6d22c2b455bfba918545a3fabc251e72a30ab8fbfe61b0f409.
- Generated size/hash restoration receipt SHA256: f704908bfb482b78312865f79400b0455fc3fced41664b8d3598e4084f6fd985.

## Independently fetched remote overlay and manifest

Repository: debgh-workspace/cryptalis-research-lab.
Immutable commit: 4d6601e3d6e436f76c38c3315fd31bcb5728dbee.
Directory: research/doctor-remedy-source221-20261015.

The exact-ref directory and linked Git trees independently discovered eight ordinary 100644 blobs: BASELINE_SOURCE_MANIFEST.json, CANDIDATE_SOURCE_MANIFEST.json, GREEN_TERMINAL_REVIEW.md, SOURCE_MAPPING.json, STATUS.md, overlays/README.md, overlays/cli.py, and test_doctor_text_remedy_real.py. All eight were independently fetched with exact-ref base64 file reads. Canonical base64, lengths, Git blob SHA1, immutable URLs and SHA256 were checked; all freshly saved remote bodies were reread and directly compared with decoded fetch results.

All four untruncated linked trees were independently recomputed:
1. 43781159edc5efdaee2047f50c626e9b3620bf55 (commit root)
2. 5054ebbac5d2af1806a2ebc0bc1ced2564e7b1f9 (research)
3. 7b615bcf471ff93b8439aea6de43dc1361b02704 (doctor packet)
4. 01a90c65b3e2f171288addf5eac74243ae62fa06 (overlays)

The exact-commit API identity links those trees. Raw commit-object reconstruction and signer authentication are not claimed; API verification reports unsigned. REMOTE_METADATA.json retains commit/tree response data and FETCH_0.json through FETCH_7.json retain the structured file responses. Tokenized download URLs from the initial directory discovery were not persisted. This is not raw HTTP wire capture.

The remote original-baseline manifest differs from README-v2 only at README.md, and differs from doctor at README.md plus CLI. SOURCE_MAPPING.json hashes and overlay mapping reconcile. Its historical source-root strings were not dereferenced. Historical status fields remain preserved as publication evidence, not promoted into a new runtime claim.

## Reverified previously independently restored baseline

The precise input was reviewer-notes/preview-readme-remote-restore-independent-20261015/pass-v3/restored-source221, not live candidate source. Its pinned review hash is be4e370fd0dd8e325ba0666667cd0018754fb5443faca46eb4b8dc1a2f28e43f. Both its saved remote SOURCE221_MANIFEST.json (152ed80306b1cf9f5893242b499d54b7155efde33ef9ac43fc4edf8516cd53cc) and generated size/hash receipt (fa8ed86f4dc57098a0a0dd294556c382d2fe129a70ba7e68feb28fce68dda233) were rehashed. All 221 baseline bodies were individually admitted and rehashed; their exact namespace and 4,450,994-byte total match.

The accepted prior recovery lineage is the independently downloaded Integrated221 focused archive, followed by the README overlay published at b64ff0d76281678a168ae5ce67135abf4e96e079. This review relies on that pinned prior review for the original archive delivery/header-restoration provenance; it does not reread or re-extract that archive. It independently reverifies its already restored source bodies, then applies the newly fetched doctor CLI overlay.

## Package closure

Prior package delivery commit: 220d35ce796b913c0cced2bd19b416cf287011c9, preview/artifacts/doctor-remedy-v2-20261015. Pinned prior independent review SHA256: 7ce9bf7d67a55e1aa9b34462fd335abc97b6cd4fe5f9876d6d812204f9f5cc5a.

The finite prior RESTORE_CHECKS.json was matched to its EVIDENCE.sha256 entry. Only its explicitly admitted sdist-members and wheel-members payload paths were used. Every one of 49 sdist and 48 wheel payloads was metadata-admitted and rehashed against that prior receipt; both complete namespaces match. All 43 doctor runtime source module bodies directly equal the corresponding bodies in both packages. No live package/source or installed environment was read. The accepted package archive identities remain wheel 053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965 and sdist 2e2a3cfc266602b958e4f4b2206c4d7ccc9e8d1de154ef0412141f529446a330, as established by the pinned prior review. This pass reverified extracted payloads, not the archive containers or a new package download.

## Admission, continuity and limits

Full source/package name, type, link-count, size and ancestor admission completed before any payload copy. Safe relative paths, no-follow reads, exclusive no-follow writes and nonexecuting 0600 files were enforced. Exact directory/file sets were checked. The main verifier rechecked metadata and rehashed 554 finite input/output leaves; atime was excluded. Supplementary checks reread all eight saved remote bodies, confirmed distinct source inodes and reconciled published baseline/overlay lineage. All writes stayed within this new review directory.

The initial two assigned REVIEW.md files and generated baseline receipt preview were displayed before formal full leaf admission; they were subsequently admitted and rehashed against supplied expected hashes before reconstruction. No incident-free process claim is made. An initial oversized shell argument failed before process creation or any write; splitting the local evidence persistence into bounded individual writes succeeded. No denied action, network retry, held archive upload or alternate network route occurred.

No product import, compilation, execution, tests, database/status command, build, installation, credential/cache/home read, prohibited raw phase body read, Git write or upload occurred. Restored source remains inert data. This is full source221 recovery from a reverified previously restored baseline plus newly fetched immutable remote overlays. It is not a wholly new full remote/environment restore, clean-host or dependency reproduction, installed-successor qualification, production readiness or a new runtime result. Existing gates and selection remain unaffected.

Evidence: RESULT.json, ADMISSION.json, READ_LEDGER.json, SUPPLEMENTARY_CHECKS.json, RESTORED_SOURCE221_MANIFEST.json, remote-bytes/, exact fetch/tree records, verifier programs and their outputs. EVIDENCE.sha256 seals this review and its retained artifacts.

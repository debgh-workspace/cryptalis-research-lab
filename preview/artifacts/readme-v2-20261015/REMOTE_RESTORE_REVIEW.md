# Independent published README-only artifact delivery and inert restore

Date: 2026-10-15 UTC.

Decision: ACCEPTED_IMMUTABLE_REMOTE_BYTE_DELIVERY_AND_FRESH_INERT_RESTORE.

This is one new remote-delivery boundary check. It does not repeat runtime qualification or claim a public smoke test, installed successor qualification, clean-host reproduction, production readiness, or comprehensive secret absence.

## Remote delivery

Repository: debgh-workspace/cryptalis-research-lab.
Immutable commit: b64ff0d76281678a168ae5ce67135abf4e96e079.
Directory: preview/artifacts/readme-v2-20261015.
Verified artifact listing URL: https://github.com/debgh-workspace/cryptalis-research-lab/blob/b64ff0d76281678a168ae5ce67135abf4e96e079/preview/artifacts/readme-v2-20261015/ARTIFACTS.json

The reviewer independently fetched exactly ten known files through ten read-only GitHub fetch_file calls. Complete returned tool-response envelopes are retained in connector-responses. Their base64 contents were strictly decoded, required to re-encode identically, and checked against the returned immutable commit/path URLs and independently recomputed Git blob identifiers. This is complete tool-response preservation, not a claim to raw HTTP wire capture or a fresh directory-enumeration proof.

Every fetched file directly equals the corresponding specifically authorized, metadata-admitted local leaf, using full byte comparisons rather than prefixes or display snippets. No local staged bytes substituted for any fetch or restoration input. REMOTE_BYTE_IDENTITIES.json records all ten exact byte lengths, SHA256 values, Git blob identifiers, URLs, and serialized response hashes. REQUEST_PROVENANCE.json records exact request arguments. pass-v3/DIRECT_REMOTE_COMPARISONS.json records the finite local mapping.

- Wheel: cryptalis-0.1.0-py3-none-any.whl, 140,936 bytes, SHA256 ce4817376f25411c8685c676802cce25c1799c85a87277b1dcc099556a40229c.
- Sdist: cryptalis-0.1.0.tar.gz, 150,389 bytes, SHA256 7988fb28baa4dec5804d4779b8a1d626c7dae5e3d7d5e597a7a12a69e0d9a036.
- Fetched full source manifest: 24,860 bytes, SHA256 152ed80306b1cf9f5893242b499d54b7155efde33ef9ac43fc4edf8516cd53cc.
- Fetched source README: 5,607 bytes, SHA256 0101bed8e6cc533e438d9a718281f7f15781fea170de91b788389938798cdcb5.
- Fetched packaging review: 14,517 bytes, SHA256 e143bec9997d3b81177e37e4ffc811d759addcc147ca96b9a0a66230f5b4d4ab.
- Fetched README-only patch: 19,230 bytes, SHA256 9f3f554dfe39c7473375adbbc8b606cd4ef7d2804339f5fd63b824d7f4b0f81c.
- Fetched README status binding: 2,316 bytes, SHA256 19a6a26ece305b90ed55a10257fa557c5ed23c613682e092953150f4f3e9dbc0.

ARTIFACTS.json, SHA256SUMS, status binding, source manifest, README and packaging review reconcile. The status binding remains its explicitly dated prebuild snapshot, with null successor-artifact field; actual artifacts are identified separately. Installed predecessor evidence is not reassigned as newly executed successor evidence. Both packages retain version 0.1.0 and require immutable path/digest disambiguation.

## Fresh source reconstruction

The baseline was read only from the previously admitted saved independent connector archive:

reviewer-notes/integrated221-remote-independent-20261015/connector-readback/CRYPTALIS_INTEGRATED221_FOCUSED_RECOVERY_20261015_v1.tar.xz

Its exact length is 1,611,936 bytes; SHA256 1f76f9bf50e7e757430edfe45b5ecb81afee67283675f2465c0d0b102f05822b. The external exact-member manifest retains SHA256 0fcd5f1bb716ffaa0088e7409e86fb8fc186e7689f5797a45df63176cfe300e7. These two fixed leaves were metadata-admitted before reading. No held source/package recovery supplement was opened or used.

The decoder enforced one CRC64 XZ stream, a 128 MiB expanded-size ceiling and a 256 MiB decoder-memory bound, exact EOF, and no trailing stream. Raw TAR length is 35,235,840 bytes and SHA256 8e6c5233a98295872d30cd45bb5c79c27dda6e233ba20eb87497436c8caac50d. All 664 headers were admitted against exact canonical header bytes and external names, sizes, metadata, offsets and header hashes before selected member-body access. The zero end padding was verified. Only SOURCE221_MANIFEST-v1.json and its 221 source objects were selected and body-hashed; recovery maps, raw runtime receipts and arbitrary historical-path referents were not followed or parsed.

Replacing just the baseline README with the newly fetched source-README.md yields precisely the fetched complete 221-file SHA256 map. All 220 other bodies remain unchanged, including 43 runtime modules and 116 test-tree files. Independently regenerating the unified README diff from the two admitted README bodies exactly reproduces all fetched patch bytes.

The final fresh source tree is pass-v3/restored-source221: 221 files and 4,450,994 bytes. Restoration uses safe relative paths, real parent directories, exclusive file creation, no-follow flags, and non-executable 0600 files. All restored paths, hashes, sizes and the complete directory/file set were reread and checked. Its size/hash manifest is pass-v3/RESTORED_SOURCE221_MANIFEST.json, SHA256 fa8ed86f4dc57098a0a0dd294556c382d2fe129a70ba7e68feb28fce68dda233. This generated manifest is a restoration receipt; the separately identified fetched source manifest retains its own exact bytes and hash.

## Fresh distribution restoration

Both fetched distributions first matched their accepted exact whole-file hashes and original local bytes. Their finite expected names were derived from the full admitted 221-file map's 43 runtime modules and fixed packaging metadata.

Sdist admission required one bounded GZIP stream, exact regular/directory sets, no links/PAX/sparse entries, fixed modes/ownership/time, contiguous ordinary TAR headers, bounded member sizes and zero termination. Wheel admission required exact central/local header agreement, expected modes/types, fixed timestamp/flags, bounded sizes, no extras/comments/encryption, nonoverlapping contiguous local spans, exact central-directory end and no trailing data. Complete header admission receipts were saved before archive payload extraction.

- pass-v3/restored-sdist contains exactly 49 regular payloads and six archive directories, 581,773 payload bytes. Its restored manifest SHA256 is 554a004758944aff7705d7999b23efab74db320ac53fb8fa87703a978d63c88d.
- pass-v3/restored-wheel contains exactly 48 regular payloads and six archive directories, 475,450 payload bytes. Its restored manifest SHA256 is 8bc96d8a420a80fb059956c3d3865c48b5ab37dd49bcb604a78a04144d05a034.

Both packages' 43 runtime module bodies directly equal reconstructed source. Sdist README, lock, license and original configuration match source; normalized pyproject configuration is semantically equal. Sdist PKG-INFO equals wheel METADATA and its description equals the fetched README exactly. The console entry resolves semantically to cryptalis.cli:main. All 48 RECORD rows cover the exact wheel; 47 hash/size entries are correct and the self row is empty. No package code or entry point was imported or invoked.

Final successful output is 318 inert files across source, sdist and wheel. All are freshly created at mode 0600 and fully reread. Final input/restored-leaf continuity checks cover 351 leaves, including exactly 12 external leaves: the ten explicitly authorized local comparisons, saved focused archive and pinned exact-member manifest.

## Preserved attempts and limits

V1 performed finite source-map discovery and header admission, exit 0. V2 completed all ten direct comparisons, the 221-file source reconstruction, exact diff regeneration and distribution header/payload checks, then stopped at an overly strict entry_points.txt byte-format assumption. The actual entry file has one additional final blank line. This was a reviewer predicate error, not an artifact defect. Its partial source restore, stdout/stderr/exit and FAILED_ATTEMPT_V2.json remain untouched. V3 uses the accepted exact semantic console-entry predicate and a distinct fresh output root. V3 exited 0 with empty stderr. V2_PREDICATE_CORRECTION.md records the bounded change.

PROCEDURE_INCIDENTS.md also retains an initial filename-only AGENTS.md discovery and the assigned packaging review being displayed before formal leaf admission. That review was subsequently admitted and matched its supplied exact hash. Truncated display output was not used as complete validation. No incident-free-process claim is made.

No build, install, test, product execution/import, database command, Git command/write, credential/home/dependency-cache read, live source expansion, live cell/corpus access, arbitrary historical-path dereference, archive repacking, or publication occurred. The single exact source README local leaf was read only for the explicitly authorized byte comparison. The only network activity was the ten exact connector reads. All writes are confined to this new reviewer directory. Restored source remains inert data.

The successful boundary is independent immutable delivery and fresh inert source/package recovery. Public quickstart smoke, fixture ACL approval, clean-host/dependency provenance and broad qualification gates are unaffected.

Primary machine result: pass-v3/RESULT.json, SHA256 ea467631581e5b8c78ad36321ed79ab07bd27fc87e451f2dba1a03059db8c770.

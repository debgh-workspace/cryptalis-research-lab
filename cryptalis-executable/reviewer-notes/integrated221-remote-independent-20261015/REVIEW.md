# Independent immutable-remote Integrated221 recovery review

Decision: ACCEPTED_IMMUTABLE_REMOTE_READBACK_AND_FRESH_INERT_SOURCE_EVIDENCE_RESTORE.

## Remote artifact and provenance

Repository: debgh-workspace/cryptalis-research-lab
Directory: recovery/integrated221-focused-20261015/
Immutable commit: 2b5124c47e6b3188f22282af547bdc330eca8abb
Verified manifest URL: https://github.com/debgh-workspace/cryptalis-research-lab/blob/2b5124c47e6b3188f22282af547bdc330eca8abb/recovery/integrated221-focused-20261015/MANIFEST.json

- Transport MANIFEST.json: 4,204 bytes; SHA256 307fdbeaea8bb60c829d77cee11a97c23a3d960ac115c3abb5978c4f885d185f
- Manifest Git blob ID: c7a92b7176d1e2c69ffcff871bf759582dc82340
- Seventeen ordered binary parts: sixteen at 96,000 bytes and one at 75,936 bytes
- Whole archive: 1,611,936 bytes; SHA256 1f76f9bf50e7e757430edfe45b5ecb81afee67283675f2465c0d0b102f05822b
- Exact member-manifest SHA256: 0fcd5f1bb716ffaa0088e7409e86fb8fc186e7689f5797a45df63176cfe300e7

The initial verification used only the coordinator's saved actual remote-readback parts, not staged local publication inputs. Every part size/SHA256 and Git blob ID was recomputed; the manifest, part and whole-archive records agree.

The reviewer then independently fetched MANIFEST.json and all 17 part files through the GitHub connector at the exact repository/path/immutable commit above. All 18 complete tool-response envelopes are preserved in connector-readback/*.response.json. Each returned display URL is bound to that commit and exact path; every returned Git blob ID agrees with SHA1(blob-header + actual bytes). Manifest text and strictly decoded part bytes match the coordinator's saved remote readback byte-for-byte. Every part also matches the independently pinned manifest SHA256/size, and direct concatenation matches the whole-archive SHA256. DIRECT_CONNECTOR_CHECKS.json records the complete commit/path/blob/content chain. No prior frozen archive body or staged local part was used as remote proof.

## Reviewed adapters and fresh bounded restore

ADAPTER_REVIEW.json, DIRECT_ADAPTER_REVIEW.json and SEMANTIC_ADAPTER_REVIEW.json record script pins and the changed input/output roots before execution. The original local review and all its failed/successful attempts remain untouched.

Two separate fresh inert reconstructions passed: first from the coordinator's actual saved remote bytes, then from this reviewer's independently retrieved bytes. The second is the decisive direct-connector proof and resides under direct-connector-review/remote-restore/.

Each pass enforced the already accepted restore recipe: 128 MiB uncompressed and 256 MiB decoder-memory limits, one XZ CRC64 stream, exact EOF/no trailing data, and a complete header-only admission before member-body access. All 664 headers match the exact external inventory and independently constructed canonical USTAR headers. Names, regular types, sizes, offsets, ownership, time, no-link fields and padding are exact. No member exceeds 8 MiB. All body hashes and zero padding pass. The raw tar is 35,235,840 bytes with SHA256 8e6c5233a98295872d30cd45bb5c79c27dda6e233ba20eb87497436c8caac50d.

The archive contains 656 content-addressed objects and eight generated controls, with 34,721,556 payload bytes. Source and recovery maps are exact. Reconstruction used only explicit safe-relative paths and admitted object bodies, with exclusive creation into fresh reviewer-owned roots and non-executable 0600 file mode. No extractall or historical absolute-path writes were used. A manual USTAR rebuild and preset-9 CRC64 XZ recompression independently reproduced the exact remote archive bytes.

## Restored counts and complete hash closure

The direct-connector reconstruction contains:

- Source221: 221 files, 4,458,764 payload bytes. Restored manifest SHA256 8e594fc345c32468040c040282f796adf74d2b3027a224e88da6cc6df20507fc
- Logical source/evidence: 1,433 files, 29,195,255 payload bytes. Restored manifest SHA256 f03011272b968e7b804c1094fa060ac2222f5d2fa2f6cd1bfce69dd425af4b9c
- Preparation/review controls: 82 files, 25,309,294 payload bytes. Restored manifest SHA256 8bf3e2444c4cf751e9faf1cfa1a9fd30c8b318ca242e3f8554c6410af309b452

Every output path, size, hash and complete file set was reread and verified. The three reconstructed manifests are identical between both fresh remote-readback passes. All 21 exact local transport/provenance inputs and five external pinned review/recipe inputs retained metadata and byte continuity during each restoration. No-follow descriptor walks, real parent directories and single-link ordinary leaves were required; read-induced atime alone is excluded from continuity identity.

## Historical semantics and alias limitations

The direct-connector restored bodies were independently rechecked. Source221 agrees with the virtual map and both preserved-source maps; source213/source218 and both 17-file control sets close exactly. All 703 nonexcluded V2 historical safe-source entries and all 255 V3 entries resolve; 1,014 dependency-source entries remain explicit exclusions and were never followed.

Historical outcome lanes remain distinct: failed V2 is 77 passes and one failure from 78 executed, with 111 selected and 33 unexecuted; native diagnostic is two passes; V3 SA20 and SA21 each have 111 passes. Both V3 maps have 196 matching receipt pins. All 112 held cleanup/release receipts pass origin/hash/size and strict true-boolean schema checks.

All 24 content-identical aliases again match anchored V2 digests, actual preserved V3 bytes, exact historical launch case identities and terminal objects. Their original V2 temporary paths are recorded absent by the pinned prior review; original size, timestamps and inode remain null. These absolute paths were not accessed. Recovered sizes of 117/74 bytes describe content only, not original-file metadata. No original rediscovery, synthesized evidence or new V2 execution is implied. The two corrected recove1 case labels, failed predecessor and all 29 before-correction copies remain preserved.

## Boundaries and retained evidence

This remote verification had no failed validation/restoration attempt. Earlier local reviewer failures remain in the previously sealed review and are not replaced. All current work is additive in this new reviewer-owned directory. Source/scripts/tests/launchers were never imported or executed. No database, Git command, Git mutation, installation or build occurred. The only network actions were the 18 exact read-only connector requests. No credential/home content, cache/dependency/interpreter body, raw phase file, live corpus or runtime referent was opened.

Exact remote identity carries forward the prior bounded content-publication review; it is not an exhaustive secrets or security guarantee. The successful round trip accepts source and focused-evidence recovery only. It does not accept runtime/environment restoration, installed product, packaging, full-source/full-suite outcomes, production/security qualification, or resolve legacy lost-metadata/importer and durable ABORTED-replan obligations. This reviewer performed no publication or repository write.

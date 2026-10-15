# Independent additive review: preview documentation v4 link correction

Date: 2026-10-15 UTC.

## Decision

ACCEPT_SCOPED_DOCUMENTATION_V4_LINK_CORRECTION. DOC-LINK-01 from the v3 independent review is resolved. This accepts an additive, link-only successor to the same source221 documentation snapshot; it is not new source, installed-runtime, smoke, artifact-promotion or production qualification.

## Independently checked result

- Predecessor directory: preview-docs-v3-source221-20261015. Its seal remains exactly `5bb02a3a29fb198be50479c4ac3b7598faf5eca1a486b544d03f229619540cc0`, and every one of its 15 payload checksums still passes. The reviewed predecessor bytes are unchanged.
- Successor directory: preview-docs-v4-source221-20261015. It contains exactly the expected 16 regular files, with no additional directory, symlink or other entry at its root.
- Successor SHA256SUMS.txt SHA-256 is `70a21c43b880bfab82851c2088e8332f06bc919381e0e83c3317218a787a1b9e`, matching the supplied anchor. Every one of its 15 payload entries passes.
- Byte comparison of every named file proves only one content-file change: QUICKSTART.md line 7 replaces `[HOST-INPUTS.md]` with `[host inputs](HOST-INPUTS.md)`. No example or API code changes. Its SHA-256 changes from `2bf64e7e106b2dc8a63881692273a6e2da02cbb34d5c102c3ecc313a45384cb9` to `50c5369684bb1b3abd9fa8969a5131a82e47ba7909478ec6c52ac01c93d90e9d`.
- The only other byte change is the corresponding QUICKSTART.md hash line in SHA256SUMS.txt. All 14 other content files are byte-identical to the accepted v3 snapshot.
- All 29 complete Markdown links resolve to regular files inside the successor bundle, including the repaired host-inputs link. No external or parent-directory link was followed.
- The metadata-admitted root proof `preview-docs-v4-link-correction.json` agrees with these independently observed documentation counts, delta, seal and preservation checks. Root assertions about unchanged product source and nonexecution are not substituted for new execution evidence.

## Carried-forward acceptance and limits

The substantive v3 review remains applicable because all other content is unchanged. It is located at `reviewer-notes/preview-docs-v3-independent-20261015T1435/review.md`, SHA-256 `2b40f6cc372b3a498f5f362e566e4eda0d9fa720bcefb50b44c66e998e3d5689`.

All 34 objective IDs, complete descriptions and recorded stages remain intact. All seven production gates remain UNKNOWN. Source221/accepted bounded packaging remain distinct from PENDING installed221 and UNEXECUTED V5 smoke. Fresh-fixture ACL permission remains pending. Existing source/package README remains unchanged and the proposed replacement remains unpromoted. The copied prose and DELIVERY-BINDING.json retain their v3 logical snapshot labels; this v4 directory is the narrowly sealed link-only derivative described here.

This reviewer executed no API, example, product import, test, install, DB, Git or external action, and made no source/package or bundle edits. Static reads/hashes were confined to explicitly admitted documentation and the root proof; writes were confined to this fresh reviewer directory. No secret, raw phase/environment or cache payload was accessed. This acceptance authorizes no downstream effects.

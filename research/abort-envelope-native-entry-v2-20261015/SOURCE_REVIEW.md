# Independent source review: native abort-envelope outer entry V2

Verdict: ACCEPT_SCOPED_NATIVE_ABORT_ENVELOPE_ENTRY_V2_SOURCE.

No source blocker found. This is a minimal successor to the accepted V1 outer entry. It is acceptable for fresh root selection only after current authority and exact review semantics are confirmed. Nothing was executed, and this review supplies neither launch authorization nor native terminal acceptance.

## Exact verified anchors

- V2 companion: `experiments/abort-envelope-native-entry-v2-20261015`; seal SHA-256 `b872be2e11367c73c55b864fb580a2c3230b457518ba6c9e2342270719cd8bf8`.
- Entry SHA-256 `6aface4a47fc5d33f7592675481aea70a2f586134777acd4c6d39945ad50bfda`.
- Bootstrap SHA-256 `732df7d2e7a2ee3be43764214eef3707b431227fddfefbf55e422ef0a1eaa9d3`.
- Command SHA-256 `63ada3b8d11711a8ed5627a9ebc882cd6f36c635ee371c91271c53e4e484d807`.
- V2 native seal `f8ebb881794328c9b6054129e5966847cd37264dc80e7a21f4b71c4a10b99ff5`.
- V2 native source review: `reviewer-notes/abort-envelope-native-probe-v2-source-independent-20261015/REVIEW.md`; SHA-256 `3b048121ed37b172ccaed6538767b9e677c2b88c0db653d443ae7eefb8876018`.
- Actual V1 terminal review: `reviewer-notes/abort-envelope-native-terminal-independent-20261015/REVIEW.md`; SHA-256 `14492777a41a76912c1f5d92ae473d44ac6f9aa6c6d594ed3f9f084d0340ed0e`.
- Prior accepted outer-entry review: `reviewer-notes/abort-envelope-native-entry-independent-20261015/REVIEW.md`; SHA-256 `5458d39b16407874edc164a6b66de6f931750b4c8ef644fd2e06b23eb3af01c5`.

All five V2 companion members and all seven V2 native members match their seals. The current companion has only its five members and seal; no root selection or run directory exists. V1 companion members still match their original seal. The exact 31-ID expected file is byte-identical between native V1 and V2. All nine unchanged inert guard/binding/source/launcher/harness inputs still match their pins; the tenth input now correctly pins the actual V1 native seal.

## Complete delta review

Full text comparisons of all five companion members against accepted V1 show only:

1. Fresh V2 companion, native packet, evidence, selected test and confcutdir identities; the V2 native seal and exact accepted V2 native-source review pin.
2. The actual preceding native V1 packet and seal, replacing the older cost9 predecessor.
3. Mandatory `closed_outcome == 'CLOSED_FAILURE'`, replacing the prior generic pass-or-failure allowance.
4. The bootstrap's corresponding path and entry digest, the inert template's corresponding identities/formatting, and documentation of the failed predecessor and source correction.

No other executable entry/control logic changed. The accepted V1 source assessment of admission, archival, runtime binding, resource accounting, failure closure and terminal-audit limitations therefore carries forward with these new identities.

The native V2 source review independently accepts the two qualified `ORDER BY q.v` corrections and fresh evidence path; it confirms unchanged tests/assertions and full vectors. This outer review does not claim to have executed or database-parsed that correction.

## Honest failed-predecessor boundary

The verified V1 terminal review's verdict is `CLOSED_FAILURE_NATIVE_REPRESENTATION_UNPROVEN`: the first UUID-domain case failed at its unqualified ORDER BY; zero calls passed and no envelope state observation occurred. It accepts normal stopped-server/source/runtime/corpus closure while preserving failure. The int64 case was not executed. These are findings of that exact terminal review, not a fresh inspection of live runtime or corpus by this reviewer.

Root reports no later database stage. The new selection must bind that exact terminal review with `CLOSED_FAILURE`, this review's final exact digest, and the exact V2 native-source review above. It must freshly attest current bounded authority, semantic acceptance, exclusive selection and no intervening stage. The original failed attempt remains immutable. Neither an older cost9 success nor a future V2 success can rewrite it. Hashes do not supply authority.

## Unchanged controls and acceptance requirements

The archive remains exactly 249 files: source221 + native8 + companion/selection7 + inert inputs10 + reviews3. Full source-path admission, 4 MiB per-file and 64 MiB aggregate archival bounds, fresh exclusive output creation, exact archive namespace/hashes, and archive-before-runtime/status ordering are unchanged.

The same runtime guard/binding, cold launcher, exclusive lab lock, fresh dual-role preflights, installed origin checks, normal stop and 26-file corpus restoration remain selected. The wrapper is invoked once. Test/control subprocess deadlines remain 600/90 seconds; faulthandler remains 180 seconds. No new parent kill deadline or CPU/AS/RSS cap is claimed. wait4 accounting and its wrapper/reaped-descendant scope are unchanged. Post-status, source/archive and runtime-after are independently attempted after wrapper failure; missing or failed closure cannot be accepted.

The full 31 ordered IDs, 93 passing phases and 221 bounded observation records remain required, including all 184 state observations and all six actual 16 MiB boundary cases. The 404 SELECT total remains source-derived. Independent terminal audit must still validate all observation identities/values, domain ordering, rejection SQLSTATEs, omission detections, source/argv/archive identity, resources, stop evidence and source/runtime/corpus closure. A zero entry exit or count gate alone is insufficient.

Only finite inert source/map/review text, metadata and hashes were read or compared. No target execution/import/compilation/collection, database/status command, installed/live-cell/corpus/cache/environment/credential payload read, Git/network operation or existing-file mutation occurred. Only this new reviewer-owned review was written. All product/v3 gates remain unproved; source acceptance is the stopping point of this review.

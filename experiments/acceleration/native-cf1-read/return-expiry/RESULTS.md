# Native-return expiry: bounded result

2026-10-14. The two frozen cases passed with the unchanged normal native helper and wrapper in Python O0 and O1. The observed complete records were identical across optimization modes. Each positive launch exits 0 with empty stdout/stderr; each mode records exactly the two expected IDs, in order.

- `after-native-return/storage/payload`: normal native helper returns exact bytes `61626364656667`; payload generation 7 expires before built-in decode starts; decode completes; final payload resolution refuses with exact safe KeyUnavailable metadata and no published value. Native-entry count is one. Ordered resolution purposes are payload, payload.
- `after-native-return/equality/search`: helper returns the same exact bytes; search generation 9 expires before decode starts; decode completes; final payload resolution succeeds and final search resolution refuses with exact safe KeyUnavailable metadata and no published value. Native-entry count is one. Ordered resolution purposes are payload, search, payload, search.

The native proxy returns the identical bytes object. The profile callback observes that object's C decode call and return without substituting decoding behavior. All four ordered events include frozen full resolution arguments, with the selected material expired at both decode events. Metadata includes exact code, stage, retryable, effects, remedy, nonempty string operation ID, canonical safe args, absent explicit cause and the expected false suppression flag. This does not certify arbitrary exception context or attributes.

Metadata-negative (storage) and trace-negative (equality) each verify the original complete actual record before modifying exactly the declared stage/trace field. Both controls at O0 and O1 fail with the intended `RuntimeError: Exact return-expiry mismatch`, exit 1, and no accepted observations. No unexpected failures occurred.

Before candidate imports: 684 pinned files verified; manifest SHA-256 `61526cc88cd30e869a8f2bffbeba86a97dc9343d8ddcad30fecb2235690a553e`; PINS SHA-256 `9fdaf8c6e5cc8dd2c6a5f125447639fae60c6e2694b394438b17602fbcc72d38`. Static review found no blocker in `../candidate-notes-native-return-expiry-review-20261014/REVIEW.md`. Exclusive result and launch receipts are in `evidence/`; `LAUNCHES.json` indexes all six launches.

This closes only the named new full-oracle immediate-after-native-return expiry supplement. The old class-only tests and all original artifacts are preserved. It is not full qualification, a causal error classifier, timing approval, provider/queue/leak qualification or product adoption. No native builds, product/source/binary changes, PostgreSQL, Git, dependency changes or performance measurement occurred.

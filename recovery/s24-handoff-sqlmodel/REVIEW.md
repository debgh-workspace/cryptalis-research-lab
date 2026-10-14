# S24 handoff/SQLModel additive capsule: independent review

## Decision

**CLEAR for separately authorized publication of the exact reviewed archive. No blocking defect found.** This is technical clearance, not publication authorization or a claim that remote publication occurred.

- Archive: `candidate-s24-handoff-sqlmodel-recovery-20261014/CRYPTALIS_S24_HANDOFF_SQLMODEL_ADDITIVE_20261014_v1.tar.xz`
- SHA-256: `56a06d435f20883a6c88294c55062400765cbcc31f37fae7ef42c1e968ac98f9`
- Archive bytes: 291,412
- Selected inputs: 692, totaling 11,095,942 bytes
- Payload-manifest entries: 701; total regular members: 702
- Payload-manifest SHA-256: `952639202b8d5779c376ff61f826fd8da2dd5d8df45ba0a83ce36a2919e8eb3b`
- Exact allowlist SHA-256: `e0266d0403369b8d9f0903a690e7ccd1ff89eaf1fc0d2eedc744de8a01a14785`

Any byte change requires renewed review. Remote commit/transport identity and remote restoration remain separate verification steps.

## Complete byte and archive checks

The allowlist, inventory groups, 701-entry payload manifest, nine other recovery-metadata files and 702-member archive close exactly. Every original selected file matches before and after review. External metadata counterparts and archive bytes remain unchanged.

The archive is one clean bounded xz stream, with zero tar-tail padding. Every member is a canonical relative regular file with mode 0644, zero uid/gid/mtime and empty owner names. No links, special or sparse files, unexpected extended headers, traversal/control-character paths, duplicate/case-colliding file names or file/directory collisions were found. Member content totals 11,715,862 bytes; the largest member is 392,458 bytes.

The independent exclusive `fresh-extraction-v1/` contains exactly 702 complete readback-verified regular files, without executable bits. There are no nested archive files, full-source trees, source-repository capture trees, installed environments, dependency payload trees, caches, Git internals or database files. Pinned upstream test excerpts are retained as inert source/provenance bytes, not an installed dependency environment.

The scan covered all 702 members plus 30 decoded nested artifacts: 732 payloads, zero high-confidence sensitive-pattern matches. Checks include private-key headers, provider-token forms, credential-bearing URLs, bearer literals and JWT forms. This bounded result is not a universal secret-free guarantee. Forbidden raw wrapper phase/environment JSONs were absent and were not opened or hashed by this review. Child `ready.json` records are separately allowlisted synthetic handoff data.

## Two-file source overlay

Both complete manifests contain the same 214 paths. Baseline manifest SHA-256 is `6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d`; candidate manifest SHA-256 is `6fccbed2f4d10e78073036ab59a5da30b33f925e40090d5aef84d1b129881bff`.

Exactly two hashes differ: `src/cryptalis/_sqlmodel_support.py` and `src/cryptalis/sqlalchemy.py`. Their two original and two replacement payloads match both manifests and the overlay plan. Applying those two hash replacements reproduces the entire candidate manifest; the remaining 212 manifest identities are unchanged. No full checkout was reconstructed or executed here. The other 212 source bodies remain external dependencies rather than duplicated payloads.

V3's baseline/candidate manifests, source delta, fixture helper and conftest equal V2 bytes. This preserves the distinction between the V2 product delta and later test-only oracle/observability corrections. The installed legacy consumer is the original r3 wheel, not this source overlay. Genuine S23 producer source and the r3 source/qualification capsules remain separately pinned external dependencies.

## SQLModel outcomes and chronological boundaries

Independent parsing of the five preserved JUnits confirms:

- V2 baseline RED: eight cases, six failures and two passes.
- V2 derivative core: 36 cases, three failures and 33 passes.
- V3 targeted provider selection: three passes.
- V3 corrected core: 36 passes.
- V3 separate synthetic DML2: two passes.

No errors or skips appear in those five JUnits. Exact V3 selection sets show core36 and DML2 are disjoint and total 38 distinct nodes; targeted3 is a strict subset of core36. Targeted passes are not three extra capabilities or corpus keys.

The independent V2 runtime review retains the three invalid provider-exception identity assertions, their unreached downstream assertions, and the unreached post-yield zero-checkout measurement. The V3 targeted/core reviews separately establish their corrected sanitized-provider oracles and later reach, without rewriting V2 as green. Native exception identity remains strict. Default-off admission and product provider-error sanitization remain unchanged.

The DML2 review labels the fault as synthetic and test-only, after a genuine native UPDATE/result. Native committability and protected quarantine intentionally differ. No natural driver/network-fault equivalence, broad DML admission, installed-overlay qualification, complete synchronous regression, general async SQLModel admission or corpus-gap reduction follows. The finite supported experiment cell remains Python 3.14.8 / SQLAlchemy 2.0.51 / SQLModel 0.0.47 / psycopg 3.3.6.

Earlier V2 core and V3 targeted missing non-Python-capture observations remain time-specific. Their later completion addenda are preserved. This audit independently matches all 100 selected SQLModel non-Python captures and all 33 external Python captures to their selected originals, plus all 68 text-suffixed legacy packet captures. Historical NOT RUN/preparation labels are not silently converted to terminal results.

## Legacy preparation incident and subsequent handoffs

The V1 packet, both 154-byte failed entry-prefix logs and explicit V2 incident correction remain intact. Both logs match SHA-256 `77106ef442e2c3e9f725240639906395ab6c56b26ff44327a721edbaa168c79d`. The preserved incident note withdraws the earlier no-entry-execution statements: unquoted-heredoc command substitution invoked both entry scripts, which stopped at the missing ENTRY guard before the wrapper, imports, preflight or database work. Individual exit receipts were not reached. These are preparation failures, not product results, and later success does not erase them.

Each later legacy cell retains ten passing parent cases with `test_legacy_recovery` classnames and ten single-pass producer children with empty classnames. The same ten lifecycle scenarios run in two cells; child cases are producer/setup evidence, not extra recovery scenarios. The one known imported-plugin warning per cell remains explicitly described in the independent runtime report.

All 100 child files are present, with exactly request, ready, producer JUnit, release and cleanup per case. Requests and ready records agree on unique phase/direction, observed journal phase and old-source/fresh-preflight attestations. Producer records retain zero checkouts and unique nonempty closed-backend sets; release/cleanup objects exactly record completed consumer work, closed engines and successful fixture cleanup.

All 30 base64 artifacts decode strictly to canonical JSON and match their recorded hashes: 20 forward and ten reverse old-v0 artifacts. Reverse records' embedded forward plans, source-plan digests, operation IDs and target IDs match their actual retained forward artifact. There are 20 unique schema/forward-operation pairs and 15 distinct forward/reverse operations per cell. The 112 retained ciphertext frames remain deliberate synthetic evidence, not credentials or provider key material.

The independent runtime reports keep installed-origin/source counts, ownership/closure reasoning and endpoint claims scoped to planned transaction-free handoffs. This byte review does not independently reenact those runtime assertions. Crash recovery, lost COMMIT/ACK, timeout/signal injection, corruption, hostile-owner fencing, arbitrary upgrades, full installed-suite admission and four optional design-matrix extensions remain unproved/unrun.

## Recovery and qualification limits

One canonical 26-file prior corpus set matches all seven per-run manifests. This proves selected corpus preservation, not new classifications or a new 600-key reconciliation. Full source214, wrapper153, runner152, SQLModel external5, legacy external4, V3 packet24 and complete legacy packet34 remain distinct counts.

This second additive capsule neither supersedes prior capsules nor changes their historically accurate statements that these experiments were then unfinished. It is not a standalone runnable or installed environment. Baseline source, prior distributions, dependencies, credentials, provider state and databases are not restored by it. Seven historical full-suite failures remain unresolved, all seven qualification gates remain UNKNOWN, and dependency provenance/drift, independent-host/provider, security and other release/performance/storage limits remain open.

No raw phase files were read or hashed here, including those some historical SQLModel reviews had permission to hash opaquely. Those historical handling statements are preserved. An integrity ledger is not a publication allowlist; extraction does not authorize executing archived launchers or validators.

## Actions and artifacts

Only independently authored standard-library data tooling ran. No archived code, product, dependency, test, wrapper or helper was imported/executed; there were no test, build, install, database, Git or remote actions. Writes were confined to this reviewer directory.

- `AUDIT_v1.json`: complete byte/overlay/capture/selected-outcome reconciliation; its pending publication field records the earlier structural stage.
- `PATTERN_SCAN_v1.json`: 732 payloads and zero matches, with scan limits.
- `DECODED_ARTIFACTS_v1.json`: 30 nested artifact hash/length records, without artifact contents.
- `PUBLICATION_REVIEW_v1.json`: final CLEAR recommendation.
- `INPUTS.sha256`: exact reviewed input/helper/restore-script pins.
- `audit_archive.py`: independently authored data audit; archived helpers were not loaded.
- `s24-handoff-sqlmodel-remote-restore-v1.py` and `REMOTE_RESTORE_SOURCE_REVIEW_v1.md`: prepared, source-reviewed future remote byte verifier; not executed by this reviewer.

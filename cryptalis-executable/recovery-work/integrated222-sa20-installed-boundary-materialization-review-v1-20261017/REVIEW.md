# Actual combined222 SA20 materialization accepted

Decision: ACCEPTED_ACTUAL_552_FILE_MATERIALIZATION. The completed root-selected Stage A satisfies the materialization prerequisite for separately selected legacy5 and report4 runtime checks. No runtime result is inferred here, and no target program was rerun during this audit.

## Exact operation

Packet: recovery-work/integrated222-sa20-installed-boundary-v1-20261017; PACKET.sha256 f412020e7f5ee41151cf0308bfe3312b435a395c8010dd35c3d4ca582507012e. Accepted executable source review: integrated222-sa20-installed-boundary-executable-review-v1-20261017/REVIEW.md, 6769 bytes, SHA256 94d21ad04bbcace03e245d0d704b36d507caead620dc5dc4c3c9c08d39543348.

Root capture persistence-recovery-20261013/integrated222-sa20-materialization-20261017-1619 has exit.txt 0 and after-exit.txt 0. Guard status is PASS_GUARDED_MATERIALIZE_PENDING_TERMINAL_REVIEW; materializer status PASS_MATERIALIZED_552_PENDING_INDEPENDENT_REVIEW and complete_readback true. Those pending-review outcomes are accepted here only for data materialization. Child exit 0, reason null, leader reaped, no group signals, no cleanup errors, empty stdout/stderr, no received signal, cold prefix absent.

## Independent output and copy reconciliation

Metadata-first namespace enumeration establishes exactly 552 regular single-link leaves and 57 required directories under the fresh packet/run/installed/site-packages. No extra leaf, directory, symlink, bytecode or unadmitted metadata appears. All 552 current sizes and hashes match the precomputed INSTALLED_EXPECTED map.

The 504 dependency copies total 51,154,717 bytes. Each destination's bytes equal its exact admitted donor, and each source/destination device/inode pair differs. All 504 receipt copy entries reconcile source path, destination, byte count, digest and distinct-inode assertion against COPY_PLAN. The underlying dependency map is adfbc90a9232c76cca2e55449b3fe391d6947eb201bd3245dd4ff11759c25e29: the previously accepted finite same-host SA20 composition, not newly downloaded or vendor-authenticated packages.

The remaining 48 leaves equal all payloads in the admitted 141600-byte combined222 wheel, SHA256 898e2548a0943d3d718aec7e2c2346d434b3131ef68c1cfe243ae9b7d8a390c8. Independent ZIP namespace checks precede bounded payload comparison. The wheel has exactly 48 file entries plus six directory entries. Its 48-row RECORD reconciles 47 URL-safe SHA256/size pairs and the empty RECORD self-entry. All 43 product runtime bodies are the accepted current-wheel payloads.

## Original input continuity

All 764 static plus three dynamic inputs give exactly 767 unique paths. The before metadata set and after receipt path set equal this expanded map. Every after entry reports both bytes and metadata equal. Independent current metadata checks match all recorded seven-field before tuples, followed by stable nofollow reads matching all 767 pinned digests. This covers donors, wheel, original patch, 222 source files, source/control reviews and native-profile observations. No source or donor was modified by this audit.

The newly materialized prefix is independent of retained SA21 and older SA20 destinations. No previous runtime acceptance or historical test count transfers to this prefix. The two upcoming runtime operations must each bind this actual review and obtain separate root selection; their source-reviewed inner558/559 and outer1320 closures remain required.

## Evidence pins and boundaries

- guard/materialize/run/terminal.json: 384977 bytes, SHA256 2a179d1c6f2a46a09002f463cc8813df234ce0981faecd4ee4ac805b58596299.
- run/MATERIALIZATION_RECEIPT.json: 264510 bytes, SHA256 72ee533f398a6e20e5c87cd100d41030034d4a37ba386bc88c88aecce9dcf429.
- CHECKS.json and reviewer-owned audit.py retain the independent data-only reconciliation.

This acceptance establishes deterministic wheel payload materialization and exact dependency copying, not package-manager installation, native import compatibility or runtime correctness. Existing-host interpreter/stdlib/native provenance remains trusted; descendants_verified_absent remains false. No dependency/product import, target execution, test rerun, database, Git, publication or owned source edit occurred during review. Production qualification and separate native database authorization remain unchanged.

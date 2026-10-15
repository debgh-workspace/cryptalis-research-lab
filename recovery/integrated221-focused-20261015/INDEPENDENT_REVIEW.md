# Independent frozen Integrated221 focused capsule review

Decision: ACCEPTED_FROZEN_FOCUSED_CAPSULE_INDEPENDENT_REBUILD_AND_INERT_RESTORE, within the limits below.

## Exact accepted artifact

- Archive: CRYPTALIS_INTEGRATED221_FOCUSED_RECOVERY_20261015_v1.tar.xz
- Compressed bytes: 1,611,936
- SHA256: 1f76f9bf50e7e757430edfe45b5ecb81afee67283675f2465c0d0b102f05822b
- Uncompressed USTAR: 35,235,840 bytes; SHA256 8e6c5233a98295872d30cd45bb5c79c27dda6e233ba20eb87497436c8caac50d
- Exact member manifest SHA256: 0fcd5f1bb716ffaa0088e7409e86fb8fc186e7689f5797a45df63176cfe300e7
- Recovery manifest SHA256: 071b66d9a3126302ebfd3cbc156b7daf2780ab7ad28d5a4eece114686fafd462
- Exactly 664 regular members: 656 content-addressed objects and eight generated controls, totaling 34,721,556 member-payload bytes

The prior accepted input review, its seal, inventory v4 and corrected alias proposal v2 are hash-pinned and preserved. All original producer and input artifacts are unchanged. This additive review leaves their historical pending-status fields intact.

## Independent archive admission and deterministic rebuild

The restore recipe was reviewed before restoration and accepted only for bounded inert reconstruction into fresh separate destinations. The compressed archive matches the separately supplied size/hash. XZ decompression enforced a 128 MiB output bound and 256 MiB memory bound, required CRC64, one completed stream and no trailing data.

A complete header-only pass preceded member-body access. All 664 USTAR headers match independently constructed canonical headers and the exact external header pins. Names are sorted unique safe-relative ASCII; only regular members are present. Ownership, time, links, unused fields and padding are exactly as declared. Per-member limit is 8 MiB. Every member-body SHA256 and size, all body padding, and all 8,704 terminal/padding bytes pass.

An independent manual USTAR serializer rebuilt headers from names and sizes without importing or running the preserved producer. All object bodies were rebuilt from the actual admitted physical inputs and controls; the recovery/source manifests were regenerated and matched byte-for-byte. CRC64/preset-9 XZ recompression produced the exact original compressed bytes and hash. A separately saved rebuilt archive was reread and verified.

## Input continuity and inert reconstruction

Before and after reconstruction, all 1,447 selected physical inputs (30,115,285 bytes), all 82 retained preparation/review controls (25,309,294 bytes), and all 13 frozen outer files retained their exact bytes. All non-atime metadata matched: device, inode, size, mode, link count, mtime and ctime. Leaves were ordinary single-link files, parent directories were real, and no-follow descriptor walks bounded reads. Producer admission metadata matched the independent before/after observations.

Fresh reviewer-owned destinations contain:
- restored-source221: exactly 221 files
- restored-logical-evidence: exactly 1,433 files, including the historical source/evidence and recovered aliases
- restored-controls: exactly 82 files

Every destination set, relative path, size and hash matches its reconstruction map. Files are non-executable data (mode 0600). Nothing was restored to a historical absolute path, and no restored source, test, helper, launcher or installer was imported or executed.

## Historical closures and preserved failure evidence

Source221 agrees with the virtual 221-file manifest and both preserved-source maps. Historical source213 and source218 close exactly; both V2 and V3 17-file control sets close. All 703 nonexcluded historical V2 safe-source entries and all 255 V3 map entries are represented with exact hashes. The other 1,014 V2 entries are explicit dependency-source exclusions whose bodies were not opened.

Actual safe JUnit contents preserve separate historical outcomes: failed V2 has 78 executed, 77 passing and one failure, with 111 selected and 33 unexecuted; native diagnostic has two passes; V3 SA20 and SA21 each have 111 passes without failure/error/skip. These are retained observations, not new executions.

Each V3 receipt map contains 196 matching selected origin/hash pins. All 112 held V3 receipts match origin/copy/hash/size and exact true-boolean-only cleanup/release schemas. All 29 before-correction copies match their retained original bodies and recorded hashes. The failed proposal, failed independent check, original/corrected audit scripts, incidents and earlier seals remain represented. Unavailable earlier draft-report bodies remain unknown; retained hashes do not recreate them.

## Twenty-four content-identical aliases

All 24 aliases bind the preserved independent V2 terminal hash to actual retained V3 bytes, their selected canonical bodies and the restored logical output. Exact historical launch handoff-parent equality and terminal per-case objects verify each corrected case. Proposal v2 differs from v1 in exactly the two documented recove1 case labels; the defective predecessor remains preserved.

The 24 original V2 temporary files were recorded absent in the pinned accepted prior review. Their original size, timestamps and inode remain null. This review never accessed those absolute paths. The 117-byte cleanup and 74-byte release sizes describe recovered content only. No original-file rediscovery, original metadata reconstruction, synthesized evidence or new V2 execution is claimed.

## Reviewer incident and content-publication boundary

Attempt v1 stopped before member-body access because the independent manual serializer initially encoded unused regular-member device fields as octal text instead of the recipe's zero-filled bytes. The original script, failure, output and metadata snapshot are retained. A separate corrected attempt passes every strict check; no failing archive comparison was suppressed. See INCIDENTS.md.

The supplemental exact-archive content review scanned all 664 unique UTF-8 member bodies and inspected all ten broad-pattern findings. They are synthetic fixtures or inert source expressions, not detected live credentials/private keys. See PUBLICATION_CONTENT_REVIEW.md and its structured record. This is a bounded no-detected-blocker finding, not exhaustive absence-of-secrets proof or publication authorization.

## Scope and nonclaims

All work was additive inside this fresh reviewer-owned directory. No database, Git, network, installation, build, test or product execution occurred. No raw phase JSON, environment dump, credential/home content, dependency/interpreter/cache/bytecode body, live corpus or runtime referent was opened. Runtime maps and historical absolute paths were inert prior-proof data only.

This accepts exact source/focused-evidence recovery and independent deterministic archive reproduction. It does not accept environment/runtime restoration, installed product, packaging, full-source/full-suite results, production release or security qualification. Legacy lost-metadata/importer limitations and durable ABORTED-replan obligations remain held. A later full-source supplement requires its own additive admission/review; publication remains a separate authorized action.

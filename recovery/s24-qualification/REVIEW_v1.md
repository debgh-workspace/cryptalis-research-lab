# S24 additive qualification capsule: independent data review

## Publication recommendation

**CLEAR for separately authorized publication of these exact bytes. No blocking defect found in this review's scope.** This is technical clearance, not publication authorization or a claim that publication occurred.

- Capsule: `candidate-s24-qualification-recovery-20261014/CRYPTALIS_S24_QUALIFICATION_ADDITIVE_20261014_v1.tar.xz`
- SHA-256: `fd0c48e128167fd25e3200eda67bcf176dfb35d831224ef6c1c9ff919ae900f3`
- Archive bytes: 749,740
- Original selected inputs: 514, totaling 10,617,893 bytes
- Payload manifest: 522 entries; archive: 523 regular files including the manifest
- Exact allowlist SHA-256: `93d29bc49bd75ddb339155df5ce083738309c7011332944e22fa4ab6dbaf4750`

Any archive change invalidates this byte-specific recommendation. Remote transport, commit identity and future remote restoration require separate verification. No remote action was performed here.

## Independently verified

The exact archive, allowlist, inventory groups, payload manifest and eight additional recovery-metadata files close without missing, extra or duplicate paths. Every selected input matches its original bytes before and after the audit. Every external metadata counterpart and the archive remain unchanged.

All 523 archive entries are canonical relative regular files, mode 0644, zero uid/gid/mtime and empty owner names. There are no links, sparse files, special entries, path traversal, control-character names, duplicate/case-colliding file names, file/directory collisions or unexpected extended headers. A bounded decompression check verifies one clean xz stream and zero tar-tail padding. All 522 manifested sizes/hashes pass.

A new exclusive `fresh-extraction-v1/` under this review directory contains exactly 523 readback-verified files, without execute bits. The extraction used explicit new-file writes and did not apply archive ownership, permissions or code behavior.

The exact 138,495-byte wheel and 149,027-byte sdist are the only embedded archives. Their SHA-256 values are respectively `4a83731a84dec485fbe0cecf7563a530c64464ec82064b2d61416d5e1109d279` and `c579fdb38204f037f6799b327b5738235d727d93db6525cf76d494dc52c9e59f`. The wheel has 46 regular files and six directories; the sdist has 47 regular files and six directories. Nested path/type checks pass; no links or encrypted ZIP members are present. Both distributions' 41 runtime modules match the pinned 214-file source manifest, and all 46 wheel RECORD rows, including the empty self-entry, reconcile.

One canonical 26-file historical corpus set matches all 13 retained per-run manifests. Duplicate corpus copies and 153-file source-capture trees are omitted as declared. The original statistics report and protocol copies are byte-exact.

The bounded high-confidence sensitive-pattern scan covers 614 outer/nested payloads, finding zero matches. It checks private-key headers, common provider tokens, credential-bearing URLs, bearer literals and JWT forms without exposing matching values. This is not a universal secret-free guarantee. Forbidden raw phase JSON, environment files, database files, dependency/runtime payload trees, caches and Git internals are absent. No forbidden raw phase JSON was opened or hashed by this review.

## Claim boundaries checked

### Corpus

The selected terminal audit's 600 unique keys cover 159 operation IDs: 444 IDENTICAL and 156 REJECTED-LOUD. Its 554 baseline keys and 46 additive keys are disjoint; 82 historical missing combinations and 36 remaining gaps remain explicit. The seven archived JUnits independently reproduce 293, 293, 12, 15, 15, 8 and 8 passes, totaling 644 testcase passes across seven invocations. The 28 negative-control result records are preserved and all report detection; their validator was not executed again. No unsupported SQLModel 2.1 or general async SQLModel admission follows.

The wrong-path/audit-sequencing correction remains explicitly attributed to the coordinator, separate from terminal artifact verification. Earlier validator-development diagnostics remain historical, not substituted for the successful v2 terminal audit.

Of the corpus terminal audit's 1,721 historical input pins, 191 are embedded and all match. The remaining 1,530 inputs are not represented as restored. This concretely confirms the capsule's declared non-standalone boundary; it is not a self-contained replay of the historical full audit.

### Installed scopes

The two dependency cells retain separate 53 focused passes, eight native passes and eleven pure methods. Archived focused/native JUnit counts and pure logs agree with those totals. Each native cell retains one warning, empty JUnit classnames and `literal_expected_junit_ids_match: false`; the alternative names/source/command-provenance argument is not relabeled as exact classname equality. Focused scopes still lack the native/pure final in-process loaded-module origin report. The 214 complete source, 153 wrapper capture, 152 runner inventory, 41 runtime modules and 24-file installed packet remain distinct counts.

The historical installed reviewer candidly records preliminary top-level-key inspection of three raw phase receipts. Those raw files are absent here. This audit did not repeat that inspection or erase the historical limitation.

### Statistics

Each archived diagnostic has one JUnit pass, 992 observations, 64 unique sanitized plan positions, 16 unique semantic-control positions and 10,000 row/value checks. All 32 observation groups retain samples 0–30; native-equality flags and semantic controls agree. The pre-ANALYZE endpoint has absent expression statistics, and the post-ANALYZE endpoint has statistics. The preserved interpretation correctly separates 1,429 NULL rows from 8,571 non-NULL frames.

The preserved report expressly rejects an established end-to-end application speedup, a causal latency conclusion, default ANALYZE behavior, prepared-plan-defect claims or performance promotion. Separate-connection EXPLAIN observations are not application prepared-plan proof. This review checks selected recorded counts and boundaries; it does not rerun the diagnostic or independently reproduce every prior quantile calculation.

### Packaging, acceptance and recovery

The exact distributions preserve previously reviewed same-host packaging observations, not an independent rebuild or official dependency/source-to-binary provenance. Dependency drift/provenance, independent-host/provider and security gaps remain open. The seven historical full-suite failures are unresolved and not waived; proposed profile acceptance is not owner ratification. All seven qualification gates remain UNKNOWN, and no production/release/performance promotion follows.

The complete 214-file r3 source capsule is referenced, not embedded: SHA-256 `17691c7d230ba97cb3d7f6d0a4f1e999c48a3e3bfa8af296539f478f0f24764d`, source manifest `6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d`, coordinator-supplied remote commit `c4052dff7ad3a5c36e27e5775b52b650bdc012e8`. This reviewer did not authenticate that remote commit. The additive capsule alone restores neither a full checkout nor dependencies, installed distributions, credentials, providers, databases, runtime state or a functioning lab. Embedded wheel/sdist bytes are not an installation. Preserved launchers must remain inert unless separately authorized.

Preparation-time `not frozen` labels are retained historical context; the separate FREEZE receipt records the subsequent local freeze. Unfinished async SQLModel, private statistics-observer and installed legacy handoff packets are excluded. No content was rewritten to make historical evidence appear cleaner or stronger.

## Method and artifacts

Only newly authored standard-library archive/JSON/XML/CSV/hash tooling was executed. No archived helper, validator, product module or test was imported or executed. There were no test, build, install, database, server, Git or remote operations. Writes were confined to this review directory.

One first-pass reviewer helper expected the additive partition label `additive46`; direct data inspection showed the actual label `async46` with the same 46 records. The helper was corrected before its successful run. No source evidence changed and no substantive corpus defect was found.

- `AUDIT_v1.json`: complete structural audit and exact metadata/count checks; its publication field intentionally records the earlier pending report-review stage.
- `SCOPE_DATA_AUDIT_v1.json`: successful selected semantic/count reconciliation.
- `PATTERN_SCAN_v1.json`: 614 payloads, zero high-confidence matches and scan limitations.
- `NESTED_MEMBER_SHA256_v1.json`: 93 nested regular-file hashes.
- `INPUTS.sha256`: exact archive, manifest and audit-helper pins.
- `audit_archive.py`, `audit_scope_data.py`: independently authored data-only audit helpers.
- `PUBLICATION_REVIEW_v1.json`: final machine-readable CLEAR recommendation, superseding the structural audit's pending publication field.

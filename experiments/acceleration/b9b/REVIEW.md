# B9B profile extension: independent static review

## Result

No new correctness blocker found in the bounded profile extension. This is a static review of research-only inactive preparation, not runtime verification, a production security assessment, or approval to publish generation 2. Root owns PostgreSQL and acceptance.

Reviewed candidate: `candidate-durable-payload-profiles-20261014`.
Comparison baseline: `candidate-durable-payload-journal-20261014`.
Module SHA-256: `ac09b3c0f70c3089aada5bf584d64487072d7b8ea7083292e543773e03a4a8df`.
Baseline module SHA-256: `18de8f736a3fba717c1ed399a98d289a42e6d94e660234642563c363645b7edd`.
Full reviewed hashes are in HASHES.json.

## Profile and identity findings

- `_profile` derives native OID, logical identity bytes, frame overhead and header size from the compiled descriptor. It admits only UUID/BIGINT records, explicit UUID tenants and storage/equality representations. It does not infer profile or authority from persisted cursors or frame bytes.
- `_authority` still admits the externally supplied source plan/pin and maintenance input; it additionally checks model record codec against the field descriptor.
- `_source` checks actual native record OID 2950/20, NOT NULL, and no default/generated/identity assignment. The explicit tenant column must be UUID/NOT NULL. `_layout` selects the matching native stage OID and retains the exact metadata layout and constraint checks.
- Exact Python UUID/int identity checks cover source projections and payload retrieval, persisted prefix projections and bodies, and returned transform identities. BIGINT excludes bool, non-int coercions and values outside signed 64-bit bounds. The database and stage retain their native ordered identities; persisted strings are never used as a driver primary-key adapter.
- `_record_text` admits only canonical decimal BIGINT spellings within the signed range, or canonical UUID spelling. Cursor-before is tied to the previous validated source identity; cursor-after and every receipt identity are compared with the exact native-ordered source subset. Negative/positive integer lexicographic order cannot control resume order.

## Frames and bounds

- The unchanged batch primitive and extension agree on 32/24 logical identity bytes, 74/42 non-NULL frame overhead, and 46/14 header sizes for UUID/BIGINT and equality/storage respectively.
- Source generation checks require payload generation 1, equality search policy generation or storage generation zero. Target checks require generation 2 and preserve bytes 10 through the profile-specific header boundary. Storage nonce/ciphertext bytes are not treated as equality terms.
- Source lengths and logical row budgets are checked before source frame transport. The aggregate source cap remains 4 MiB and 64 rows; selection and persisted logical-byte receipt validation use the same descriptor-derived accounting. The global artifact bound remains a conservative upper cap, while actual row and batch admission use the correct profile-specific values.
- Full prefix verification still independently opens source and target frames and compares exact value types/values, NULL membership, source commitments and complete target commitments. Committed frames are not resealed.

## Authority, journal and lease regression inspection

AST-identical definitions include `_session`, `_lock`, `_catalog`, `_stage_permissions`, `_journal_rows`, `_revisions`, `_validate_entry`, `_prepared`, `_check_binding`, `_row` and `_target_commitment`.

The changed bind/entry code retains external ACTIVE pin and exact policy fingerprints, source journal digest, implementation hash check, OID/catalog/inventory verification, native runtime privilege inspection, the source-plan scope lock, source table lock, exact source revision, one additional row in the existing journal, explicit start, conditional prior-state journal UPDATE and affected-row checks. It retains the real prepared binding check after transformation, after DML, and after the before-commit observer immediately before COMMIT. Inspect/terminal paths revalidate the binding and perform no target/journal DML. Commit uncertainty remains UNKNOWN with fresh-worker inspection, without an in-session retry. No activation or policy publication path was added.

## Evidence and limits

- All 210 entries in PROFILE_BASE_HASHES.json match the original B9A directory. In the profile candidate, 209 of those inherited files remain byte-identical; only the intended experiment module differs. The inherited B9A tests, product src, runner, dependencies and canonical documents are unchanged.
- Static AST parsing succeeded for the changed experiment and new profile tests. No module imports, test collection, test execution, PostgreSQL commands, Git commands or source edits were performed by this reviewer.
- The new six parameter cells use native fixtures and an independently composed frame decoder. They cover current edited/inserted/deleted values, signed limits, NULL/empty/Unicode values, exact native ordering, receipts, generation-1 application reads, terminal idempotence and committed-prefix SIGKILL/fresh-process recovery across the three newly admitted profiles.
- The six cells do not repeat malformed decimal cursor/type rejection, exact-fit/oversize bounds, changed external authority, catalog drift, uncommitted rollback, lost reply or lease-expiry faults across every new profile. Existing B9A/B8 companions remain necessary; a pass in these six cells is not a four-profile fault-matrix pass.
- PROFILE_RED_MATRIX.md is a frozen RED-stage description: its statement that the module remains unchanged is historical and does not describe this post-implementation candidate. A final receipt must bind current hashes and actual root-run outcomes rather than treating that RED text as GREEN evidence.
- The host maintenance assertion and no-concurrent-owner-writer assumption remain necessary between chunk transactions. This extension does not qualify deployment-wide writer fencing or general concurrent-owner behavior.

Contracts read: app-assigned identity in docs/decisions.md, Changes and rotation / Restore and authority loss in docs/lifecycle.md, current docs/status.md, PROFILE_RED_MATRIX.md, and the original same-journal NEXT_SLICE.md contract. The unchanged CF1 implementation and batch primitive were checked against the extension.

Optional .agents/graphify absent-path probes returned exit 2. The reviewer stopped and obtained explicit root authorization to finish static verification; those probes were not retried and no access restriction was bypassed.

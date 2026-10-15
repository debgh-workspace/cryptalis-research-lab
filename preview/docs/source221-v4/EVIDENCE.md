# Evidence boundary

Snapshot: 15 October 2026, source status after the coordinator's 14:07 reconciliation and packaging acceptance at 14:15. Source APIs were read from Integrated221. Test/build outcomes below were supplied by the coordinator and the authoritative ledger. The accepted package review and actual-artifact record were statically read and their hashes checked. This task did not rerun tests/builds or independently inspect distribution payloads.

## Current versus installed

| Evidence | Exact accepted outcome | Boundary |
|---|---|---|
| Integrated221 full source, SQLAlchemy 2.1.3 | 2,684 PASS / 0 FAIL / 0 SKIP; 56 passing subtests; 471.98 s | Independent source acceptance |
| Integrated221 full source, SQLAlchemy 2.0.51 | 2,638 PASS / 0 FAIL / 46 expected native-version skips; 56 passing subtests; 465.98 s | Independent source acceptance |
| Integrated221 optional SQLModel source | 38 PASS / 114 passing phases; 8.28 s | Independent bounded source acceptance; corpus/dependency restoration reviewed |
| Integrated221 focused contract evidence | Corrected 111-case suites accepted in both cells, including native mutation and genuine historical-producer evidence | Thirteen replacement/new historical-contract cases also pass in full source suites |
| Integrated221 packaging | Actual entry 0; independent ACCEPT_SCOPED_INTEGRATED221_PACKAGING | Two identical sdists and three identical direct/repeat/roundtrip wheels; exact identities in INSTALL.md |
| Integrated221 installed main/optional suites | PENDING | No source-to-installed transfer assumed |
| Integrated221 exact public quickstart smoke | PENDING / UNEXECUTED; V5 harness source accepted | Installed binding and requested fresh-fixture ACL permission pending. Read-only identity V3 passed one case across both roles/routes; that is not a smoke result |
| Transport218 installed, SQLAlchemy 2.1.3 | 2,671 PASS / 7 FAIL / 0 SKIP; 56 passing subtests; 421.57 s | Highest audited installed baseline, not source221 |
| Transport218 installed, SQLAlchemy 2.0.51 | 2,625 PASS / 7 FAIL / 46 SKIP; 56 passing subtests; 398.45 s | Seven historical failures remain on that artifact |
| Transport218 installed optional SQLModel | 38 PASS; 5.82 s | Accepted recorded results/restoration records; no independent live corpus boundary after reuse |

Source221 is `candidate-cluster-retained-integrated-v2-20261015`, 221-file manifest SHA-256 `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`. Transport218 source-manifest SHA-256 is `b8a8a6b00c597b63f4851defb74a2baa3dde8f3ff4c2e46d789699792600a204`. Main remains S14; neither isolated source acceptance nor packaging implies main/release promotion. No current release commit is fabricated here.

## Historical seven failures: retained, then resolved in source221

The following Transport218 failures were in `tests/test_deprotection_ordinals.py`:

1. `test_reverse_refuses_unhandled_public_suffix_comment_before_staging`
2. `test_changed_public_staging_refuses_switch`
3. `test_public_copy_participates_in_chunk_byte_bound`
4. `test_reverse_refuses_unhandled_suffix_attributes[column_grant]`
5. `test_reverse_refuses_unhandled_suffix_attributes[statistics]`
6. `test_reverse_refuses_unhandled_suffix_attributes[storage]`
7. `test_reverse_refuses_unhandled_suffix_attributes[compression]`

They compared historical suffix-copy assumptions with retained-native behavior. The integrated correction replaces the invalid historical expectations with native metadata/value-preservation and refusal oracles plus mutation proofs; no safety assertion is waived by a skip/xfail. All 13 replacement/new cases pass in current source. The earlier 77 PASS / 1 FAIL fixture result, its native-two-case diagnosis and fixture-only V3 correction remain historical evidence, not deleted failures. Installed221 validation is still required.

The old changed-public-staging failure occurred at `NoResultFound` before its decisive tamper assertion. It did not prove acceptance of corrupt staging. Current source success does not qualify generic legacy conversion or every PostgreSQL metadata object.

## CLUSTER correction

The independently reproduced baseline had two affected failures and two controls passing: original remembered index designation was lost after protect, current edits and reverse. It did not measure physical heap order. Separate correction/default/legacy work was then integrated into source221 and accepted within its finite source suites and focused/native/mutation evidence.

New source221 plans record remembered designation explicitly. Old artifacts without that history remain conditionally recoverable or loudly blocked as described in [RECOVERY.md](RECOVERY.md). The correction is not present in Transport218. Installed221 and generic post-loss repair remain open.

## Application and recovery evidence

Historical FastAPI template source was pinned at `7257e606cb94eada1dca40173e2b7f99dd549bc6`. Recorded native, protected, package-free-before-removal and package-free-after-removal runs each passed 58 tests. The trial used zero upstream business-source edits, 13 external bootstrap lines and four fixture lines, explicit C collation, separate roles/operator grants, and a private bounded delete/cascade profile. The app's native greenlet 3.5.2 changed to 3.5.6 for package requirements. This is not a current public attach-only full-app result or zero deployment cost.

Same-host current-value/ciphertext and pg_dump/psql recovery evidence is retained. Exact inert archive restoration and remote byte persistence prove data-file recovery, not a fresh interpreter/dependency/runtime/database environment. Historical original dependency archives, clean-host reproduction, interpreter provenance and full release provenance remain incomplete; see [INSTALL.md](INSTALL.md).

## Documents are not executable evidence

Inherited source README/status/lifecycle paragraphs contain dated descriptions such as unimplemented decrypt-back and source-only unverified CLUSTER work. Those descriptions cannot override current source and independently accepted receipts. This separate guide corrects their interpretation without modifying the frozen source/package. A proposed replacement README is [separately staged and unpromoted](PROPOSED-PACKAGE-README.md). Documentation integration into a new package remains unfinished.

The package review SHA-256 is `4ba4234f4cda55a2cde9670d11e1fab07a169b8378a422f14f93f2c5be1d5665`; its ACTUAL_ARTIFACTS.json SHA-256 is `6e2fb242392635e931c904e8cdc25e29da7583622d8a1bd5a79056be43a18123`. The review explicitly authorizes no installation/test/database/promotion action. It establishes bounded same-host artifact equality, not clean-host provenance.

All seven production gates remain UNKNOWN. Every one of the 34 full-product objectives remains open at its recorded scope. No successful example execution, clean-host result or production approval is inferred from this documentation pass.

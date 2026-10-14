# S25 source integration: independent source/command review

## Decision

CLEAR for coordinator execution of the three frozen ROOT_COMMANDS blocks, one at a time, with independent terminal audit before advancing. This is source/command clearance only. It is not a runtime pass, release, installed qualification, or permission to alter the wrapper, preflight, lock, dependencies, tests, or source.

Exact pins:
- Candidate 216-file manifest: 3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703
- ROOT_COMMANDS.txt: d438c84f3943b79a8033c42b2d9fa8172b1faf281de52fa6bc2b9309d65246f3
- INPUTS.sha256: 24464a0dfd8a76b76864118aee7bbc5fa4019741d90f3e3ab9ca80477e89b205 (1201 entries, all match)
- PACKET.sha256: a6a0ae22f6bed59f878dcf0a1f00ec04c431bdbdb881ee88eb82a7ab493913ca (17 entries, all match)

## Source findings

Independently hashed actual tree and manifests: baseline214, candidate216, 212 baseline files identical, exactly two existing product overlays copied byte-for-byte from accepted V2 candidate. The two additions are relocated V3 tests and support. Every original test/configuration/lock/preflight remains identical. All 698 current preservation entries match.

The complete test body from assert_sanitized_provider_failure onward is byte-identical to V3; support from enable onward is byte-identical. Test relocation adds an explicit exact SQLModel0.0.47/SQLAlchemy2.0.51 admission error, not a skip. Support pins exact S25 root/cwd, complete216-file inventory, unchanged16 dependency source pins, existing SQLModel interpreter prefix, Python3.14.8 and psycopg3.3.6. Module setup and teardown retain checks. Existing tests/conftest.py is byte-identical to V3 conftest, preserving fresh preflight and diagnostic redaction. Default pytest prepend supplies the local helper path; no alternate import mode is introduced.

Product flag remains False, and async admission checks exact True and exact qualified versions before cached class lookup. Default-off therefore also applies after cache warmup. Plain SQLAlchemy mappings use the original base class. Guarded SQLModel uses the reviewed public sync_session_class composition and public native exec wrapped with the existing result boundary. Factory rejects bind/binds/class_/sync_session_class/_owner/_asynchronous overrides. Logging checks still precede optional admission; admission occurs before connection/validate/activate. Tenant/crypto/query guards and cleanup logic are unchanged except the already accepted result-boundary factoring. No new default-on or public DML authority is introduced.

## Matrix and counting

SQLModel selects38 distinct nodes; core36 and DML2 are disjoint and exhaustive. Targeted3 is contained in core36. Full SA21 and SA20 select every original2639 node and ignore only the new optional module. No original skip, test or failure is removed. Baseline tables match the independent R3 oracle exactly: SA21 2632 passed/7 failed, SA20 2586 passed/7 failed/46 skipped. Each has56 passing subtests separately; SA20's46 include18 setup and28 call skips.

The same SA21 wheel-venv and SA20 s20-payload-preparation-sa20-20261014 interpreter paths appear in the independently reviewed R3 PROPOSED_COMMANDS.md. Current interpreter bytes, pyvenv.cfg, SQLAlchemy METADATA and RECORD were checked against R3 INPUTS for both cells: all8 match (SQLAlchemy2.1.3 and2.0.51). No cell substitution is present. Optional cell uses the unchanged accepted SQLModel prefix/source pins.

Commands retain the unchanged wrapper, exclusive lab lock, fresh dual-role preflight, source origin checks, archived source, cleanup and shared-corpus restoration. Wrapper exit is captured explicitly; expected baseline exit1 is not converted to all-green. Stop for an independent audit after each block and before progressing, including after any unexpected failure or integrity/preflight issue.

No full2677-node SQLModel-environment run is proposed. Optional coverage remains38 nodes in its own exact cell. Do not normalize skip counts, count targeted overlap again, erase seven historical failures, or claim full optional/cross-module coverage.

## Preparation integrity correction

Independently observed the initial new INPUTS mismatch: exactly three historical .pytest_cache values, V2 lastfailed/nodeids and R3 nodeids. They were stale values expanded from V3's older preparation-preservation inventory. No source mismatch was found. INITIAL_STALE_CACHE_CHECK.log preserves the failed integrity check. The corrected new closure inherits approved V3 runtime INPUTS without recursively expanding that obsolete cache inventory; the original preservation snapshot is still pinned and was not rewritten. S25's current698-entry preservation snapshot verifies current original bytes, including cache files. This is a new-metadata provenance correction, not evidence repair or silent exclusion of a source mismatch.

## Scope

Read-only source/data hashing and static review only, with outputs written solely in this reviewer directory. No candidate imports, compilation, collection, tests, database, installation, Git, remote actions, or raw environment-bearing phase JSON reads. Earlier failures remain preserved. Production gates remain UNKNOWN.

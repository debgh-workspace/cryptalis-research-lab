# ORM workstream progress

Candidate: candidate-accel-orm-20261013. Integrated base: S14, 2065cb78f3c7126f207fc62c35887ddd204925af. Coordinator owns publication on accel/orm-20261013. No Git metadata is present in this isolated source copy.

## Current slice

Off-by-default explicit public-table bulk UPDATE. Protected-table/field bulk UPDATE is excluded. No production capability claim; all seven gates UNKNOWN. The original seven legacy-layout assertions remain unchanged.

## Files owned and changed

- src/cryptalis/_experimental_public_update.py: exact table/statement/connection permit, narrow grammar, locked OID/effect inventory
- src/cryptalis/sqlalchemy.py: private UPDATE dispatch/admission/driver hooks and native autoflush boundary
- tests/test_private_public_update.py: 59 native differential, refusal and pure regression cases
- docs/research/PRIVATE_PUBLIC_UPDATE_20261013.md: contract, evidence boundaries and sources
- WORKSTREAM_PROGRESS.md: this report

## Source hashes after final type-ordering correction

- sqlalchemy.py: 6e1484898bebfa6ddf30a7ec49f8ebd7acc693597b3e25a073160c895d43531c
- _experimental_public_update.py: bfd2e84e30acab549f7b221110b7bec3aa150bc16084669ea32a462a4e8c20c3
- test_private_public_update.py: 44b03cbee5469cab0ac3b5dc7d5e870f2adf12aba73e89b3947f6a445e3b25a6

## Tests

- Actual coordinator RED: a1-public-update-red-20261013; 1 FAIL, 30 deselected, 0.62 s. Native oracle proceeds; unchanged attached runtime refuses. Server stopped afterward.
- Actual local static: all three edited executable files parse as Python AST.
- Actual first local pure smoke: 5 statement-admission controls PASS on existing SQLAlchemy 2.0.51; no DB opened.
- Actual first coordinator GREEN: a1-public-update-green-20261013; 28 FAIL / 3 PASS, 11.24 s. SQLAlchemy 2.1 lacks the older _ordered_values attribute; one FK fixture also correctly triggered protected source_schema_changed. Both causes were corrected without changing the source-schema guard.
- Actual second local pure smoke: 7 controls PASS separately on SQLAlchemy 2.1.3 and 2.0.51, including ordered-assignment refusal and mapping-name drift. No DB opened.
- Public mapping identity is now frozen at attachment activation.
- Actual corrected coordinator GREEN: a1-public-update-corrected-20261013; 31 PASS, 10.21 s. Source stable; server stopped. Coordinator retains and publishes the exact archived prototype, without promotion.
- Actual pure omission controls on both versions: omitting initial permit-stage check, consumed-stage transition, or exact compiled-object check makes the corresponding test fail. After each in-memory omission, all three restored controls PASS. Disk bytes unchanged; no DB opened.
- Actual expanded coordinator SQLAlchemy 2.1.3: a1-public-update-expanded-sa21-20261013; 57 PASS, 16.58 s. Server stopped.
- Confirmed pure default-path RED on both versions: old pin capture reads an optional custom-type length accessor on an ineligible table. Final correction captures only already-qualified schemas and exact built-in types, and short-circuits absent pins.
- Final-source pure sensitivity on both versions: 4 omissions (initial stage, consumed stage, compiled identity, eligible-type filter) each fail the corresponding control. All 4 controls pass after each in-memory restoration; disk helper SHA256 remains a22c40f3115acf829d156ad5744abff1144cc73f864f4b4b5787ff1bf238782b. No DB opened.
- Actual preceding 58-case source: SQLAlchemy 2.1.3 58 PASS, 17.21 s; SQLAlchemy 2.0.51 58 PASS, 17.66 s. Both source-stable; servers stopped. These counts do not describe the later final ordering correction.
- Final ordering correction: both pure RED controls confirmed that an already-pinned mapping later changed to a custom type could access an optional attribute before refusal. Exact-type admission now precedes mapping identity inspection. Initial and post-attachment custom-type regressions pass separately on both versions.
- Final helper sensitivity: 5 in-memory guard omissions each fail their corresponding test on both versions; all 5 controls pass after each restoration. No DB or disk-source mutation.
- Queued impacted final-source selector: `tests/test_private_public_update.py -k "pin_skips or mapping_drift or unqualified_mapping or repeated_typed_binds" -q` (10 cases).
- Separate 58-case cache-omission copy: `../candidate-accel-orm-20261013-cache-omission`; all 187 copied files are exact except the new UPDATE cache-disable line. Mutant sqlalchemy.py SHA256 b01b9f0cd48ea729512db22f1f80e59148ca5e51baa36aa8e369818720514353. Coordinator-only selector: `tests/test_private_public_update.py -k repeated_typed_binds -q`. Its receipt records every source/copy hash. Main source unchanged by preparation.
- NOT RUN at this checkpoint: impacted final-source PostgreSQL controls, PostgreSQL cache-removal variant, provider-failure UPDATE, installed candidate wheel, full suite. Full 58-case PostgreSQL controls passed before the final type-ordering correction.

## Blockers and next task

Await the coordinator final impacted controls and separate cache-omission result. The full 59-case file and broader integrated regression have not been run on the final source. Runtime and test files are frozen until they return. Then resolve observed failures and report the exact finite acceptance boundary. No database server or test was started by this worker. New cluster/credentials are not needed for this slice; separate qualification approval remains pending.

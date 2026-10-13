# E1 textual-query oracles and S17 internal composition review

Date: 2026-10-13 UTC. This is an internal engineering review by a separate native worker, with independently authored behavioral controls. It is not independent external security, cryptography, provider, or production qualification. All seven production gates remain **UNKNOWN**.

## Frozen findings and native oracles

The three test files contain 164 finite cases on SQLAlchemy 2.1.3: 80 FROM/qualified-name cases, four GROUP-shadow cases, and 80 remaining-clause cases. They use synthetic fixtures. Native queries compare textual names against explicit column expressions. Attached public controls require native results; protected controls require `UnsupportedProtectedOperation` before the driver execution event. Sync/async paths and table aliases are included. They depend on existing repository fixtures and are not standalone tests.

The initial final-C2 guard checked selected-column keys but missed native FROM/qualified namespaces. The two initial RED receipts establish **30 missing-refusal failures**, not 30 distinct vulnerabilities:

| Receipt directory under `evidence/` | Observed result | Classification |
|---|---|---|
| `e1-textual-from-red-20261013` | 28 failed, 52 passed; 9.50 s | All failures: missing typed refusal |
| `e1-group-shadow-red-20261013` | 2 failed, 2 passed; 0.60 s | Both failures: protected input wins GROUP-name shadow |
| `e1-remaining-textual-clauses-red-20261013` | 32 failed, 48 passed; 17.78 s | 20 missing-refusal failures; **12 invalid native fixture failures** |
| `e1-within-group-native-corrected-red-20261013` | 4 failed, 8 passed, 68 deselected; 2.03 s | Four confirmed WITHIN GROUP missing refusals |
| `c4-textual-scope-green-sa21-20261013` | 284 passed; 31.08 s | Finite corrected query gate, including 120 C2 controls |
| `c4-textual-scope-affected-sa20-20261013` | 401 passed, 28 skipped; 45.51 s | Corrected query plus affected adapter/search/thread gate |

The original 12 `func.mode().within_group(textual_name)` failures included native/public cases and arose in SQLAlchemy's specialized type inference. They are **not product defects** and the original failed receipt is preserved. The fixture was changed to native `func.pg_catalog.mode().within_group(...)`; its native/public controls passed and four protected cases then established missing refusal. The final frozen test is the corrected fixture. The 28 SQLAlchemy 2.0.51 skips concern the absent native `distinct_on` extension and generic `FunctionElement.aggregate_order_by` API, not failed protected operations.

E read the coordinator's existing logs and JUnit records; E did not run PostgreSQL. All six named runs report unchanged source/external-source inventories, zero test errors, and successful server shutdown. The selected test logs contain failure traces, synthetic case names and summaries. A bounded scan found no credential-bearing URLs, secret assignments, private-key blocks, AWS access-key patterns or rendered parameter dumps. This scan is not a general secret-detection proof; credential, environment and raw database logs are excluded from this publication set.

## Correction and composition binding

The reviewed C4 runtime is `candidate-accel-search-clause-resolution-20261013/src/cryptalis/sqlalchemy.py`, SHA-256 `286869f5f2cf262991adea324344a5091e1e9d7994b4416464d2f799f087e2ad`.

C4 checks local textual references in their owning SELECT scope. Selected expressions use native FROM-only resolution; bare outer ORDER BY and DISTINCT ON use selected-label precedence; GROUP BY and references embedded in expressions account for input-name precedence. Nested SELECTs are skipped by the local walk and visited in their own scope. Namespace construction uses an empty pinned SQLAlchemy compiler without SQL rendering or key capture. Unresolved/protected ambiguity refuses; existing lineage guards remain.

The reviewed integrated S17 runtime is `candidate-accel-integrated-r2-20261013/src/cryptalis/sqlalchemy.py`, SHA-256 **`fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe`**. Read-only AST/byte comparisons were repeated while preparing this receipt:

- C4 `_admit_textual_references` and `protected` are AST-identical in S17.
- A2 `_execute` and `_async_delete_result_boundary` are AST-identical in S17. A2 source SHA-256: `ef764a712b60c6c33e694937ed23ce56f21b8374f081d276b0f076310a9d3b89`.
- The inner native-invocation branch leaves native `DBAPIError` transaction/flush state to SQLAlchemy. The outer post-result failure cleanup retains its attempted/not-already-cleaned condition, with **no DBAPIError exemption**, and always resets its context token in `finally`.
- F1 `attach` is AST-identical in S17. Its logging preflight runs after lock/type/profile parsing but before attachment construction or connection acquisition. F1 source SHA-256: `ae52d494024e09ebf330d152598b2f852b4fc8183f1260e067c520fc0013e2b1`.
- S16 `before_execute`, `check_cursor`, `_query_would_autoflush`, and the outer result boundary are AST-identical in S17. The public UPDATE restriction/pin module and reverse consistency implementation are byte-identical to S16; only `src/cryptalis/sqlalchemy.py` differs among their runtime Python files. S16 adapter SHA-256: `876db4735b0e69155eb7da8985c68275572199ab4e79cb184ab0ecc92285c60f`.
- All three frozen E oracle files are byte-identical in S17. No C1 performance optimization or B1 inactive rewrap successor was introduced by this composition.

No actionable composition blocker was found within this source-review boundary. That finding does not replace integrated executable qualification. The seven historical legacy ordinal-profile failures remain real failures and are not reclassified by these oracles.

## Finite coverage and limits

The textual-consuming inventory covers SELECT ORDER/GROUP, legacy/new DISTINCT ON, window ORDER/PARTITION, WITHIN GROUP, generic ordered aggregates, and relevant transparent ordering wrappers. The legacy PostgreSQL aggregate-order helper's ordinary string literals are not textual-label references. Compiler namespace behavior is pinned to SQLAlchemy 2.1.3 and 2.0.51; custom compilers, future extensions, arbitrary SQL grammar and all loader/context combinations are not proved by this finite set. Conservative ambiguity refusal does not admit new protected ordering, grouping, windows, aggregates or search leakage. No performance improvement, live KMS behavior, lease/fork/cancellation completeness, external review or production readiness is claimed.

This publication preparation changed only new notes outside candidates. Frozen source, tests, receipts and Git were not modified. The manifest is a proposed coordinator publication input; its creation is not publication or promotion.

## Exact publication-asset hashes

SHA-256 values below bind the unchanged files copied by the publication manifest. Paths are relative to `experiments/acceleration/e1/`.

| Asset | SHA-256 |
|---|---|
| `tests/test_textual_from_boundary.py` | `43bf89c1e5030101c8d590db4a4c56fb1eb4b2514ee184a2b868f3eb9ec009bf` |
| `tests/test_textual_group_shadow_boundary.py` | `9ffbbc24c425d76b060ba22d3cf2d744df97bb2278728ea5adadc342e9611aa6` |
| `tests/test_textual_clause_boundary.py` | `68cad71a86f5d7471c32a3bdafa0da72ec751530f6b451a50412aa20e109f4fc` |
| `evidence/e1-textual-from-red-20261013/tests.log` | `6ba2025fd827e9e508685db816280529869db39ac2da91b1906cfb170904a38e` |
| `evidence/e1-group-shadow-red-20261013/tests.log` | `20c5f5c2733b6d7fdea6626b38abfa93f8d10b0754fd75e64d4bdb1d16843bb4` |
| `evidence/e1-remaining-textual-clauses-red-20261013/tests.log` | `a29b61aa604591edef3cfe21b3a2f1de48c220129670286799d0c53ae2fa3fdd` |
| `evidence/e1-within-group-native-corrected-red-20261013/tests.log` | `15b698f14508739d9fa677822635a2d9a5a219ccd1e91e1e9ddfc958bb0db7e3` |
| `evidence/c4-textual-scope-green-sa21-20261013/tests.log` | `6bf1d8db902912cf8f5883483e77bd7aed3e65a08973163da56782fd91f315f3` |
| `evidence/c4-textual-scope-affected-sa20-20261013/tests.log` | `e81e43f6af9bcdbf31d1b668da9ced65cc06c428ac7111c22f8e36c6eeb3a828` |

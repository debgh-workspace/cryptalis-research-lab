# S24 test-only oracle corrections, r3

SOURCE PREPARED; NOT EXECUTED. Parent combined r2, its failed aggregate receipts and all earlier artifacts remain unchanged. Independent terminal traceback review confirmed 26 added failures: fourteen shared multitable routing failures, eleven exact-v0 assertions and one malformed new-plan constructor boundary. Seven previously reported ordinals failures remain separate and are not waived.

Only five test files change. Every product/source/configuration byte is identical to combined r2. The shared multitable frame reader admits exactly legacy retained v0 and retained comments v1, rejects unknown formats, and keeps its independent ciphertext-column/native-value/CF1 checks. Three automatic-plan assertions now require exact comments-v1 plus INVENTORIED scope; all byte-budget, state/refusal/recovery, native metadata and optimistic-versioning assertions remain.

The old doctor malformed-plan case is explicitly synthetic legacy-reader coverage: its format and absent inventory are changed before malformed models are constructed. It still requires REJECTED/invalid_deployment_state and NOT_INSPECTED roles. This is not genuine old-producer recovery. A separate new-format case requires safe invalid_plan rejection during construction and proves a designated diagnostic sentinel is absent from str/repr of the exception. Neither path relaxes product admission or changes the original active deployment.

PLANNED_CELLS identifies all 26 exact added failure nodes from retained terminal JUnit plus the new constructor case. Source preparation parsed edited test ASTs and hashed bytes only. No product imports, pytest collection, tests, database, builds, installs or Git operations were performed. The focused 27 and full aggregate remain unexecuted. All seven product gates remain UNKNOWN.

Require independent source review. Root owns each serial wrapper invocation and decides the next cell only after terminal status, exact node IDs, source stability, corpus restoration and clean stop. Preserve failures; no substitute DB, changed preflight, direct pytest or automatic retry. The runner/preflight bytes remain identical to r2.

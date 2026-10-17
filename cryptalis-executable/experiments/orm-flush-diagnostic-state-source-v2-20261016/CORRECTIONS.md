# V2: independently observable truth-hook oracle

V1 remains unchanged, seal
`3d475bc51acc99674733a0e7b5d101332f2b8253f37c945aa5d32e42db494af4`.

Only `regression/test_flush_cleanup_state_contract.py` changes among the eight
V1 payload members: it records every FalseLike.__bool__ call, then asserts the
record remains empty outside all product catches. The original raised assertion
alone could have been swallowed by a broad product catch. The external counter
makes attempted truth dispatch independently observable in every UNKNOWN arm.

Both product files, both product/test adaptation patches, the two other test
files and TEST_PLAN.md remain byte-identical to V1. This correction adds this
document and a separate TEST_ORACLE_V1_TO_V2.patch; SOURCE.sha256 seals V2.

Scope/counts are unchanged: shared ten-arm note-only-baseline/successor test;
successor six unittest methods, 29 subtest arms and one ordinary test. No test,
import, database, installation, Git, or promotion action occurred. Independent
V2 source review and root runtime selection remain required.

# V7 SA21 baseline: accepted bounded regression RED

Decision: ACCEPTED_EXACT_SYNTHETIC_UNIT_RED, 2026-10-16 10:40 UTC. The root-selected real-module direct-helper run completed three methods and exactly 15 subtest arms: 10 assertion failures, five passing controls, zero errors and no skips. This is separate from the V5/V6 pre-test setup HOLD records, which contribute no test outcomes.

Packet: `experiments/orm-flush-diagnostic-unit-packet-v7-20261016`; child records `run/sa21-baseline`; root capture `persistence-recovery-20261013/flush-unit-v7-sa21-baseline-root-20261016`. Selection/argv and child argv match accepted V7 command review `6c7f7a6c27bc6d8e20c6476ef2ab1809bb1e3b50787349023e446db33c76c1c7`. Test identity is `2bff9041c9e2e0f34eaecc02b56dcbe5bec28afd3bc16546afa3afcf3141baf7`.

## Exact outcomes

- `test_primary_survives_and_cleanup_is_attempted`: ordinary-note × success/rollback_failure/quarantine_incomplete all PASS (3 arms); override/unavailable-note × those same three cleanup variants all ASSERTION_FAILURE (6 arms).
- `test_note_failure_cannot_skip_close_or_later_connections`: override/unavailable-note × close_fails False/True all ASSERTION_FAILURE (4 arms).
- `test_absent_or_inactive_transaction_does_not_start_cleanup`: transaction None/inactive both PASS (2 arms).

Method outcomes are ASSERTION_FAILURE, ASSERTION_FAILURE, PASS. Every failing arm has AssertionError at the intended primary-exception identity assertion. The observed replacement is RuntimeError for overridden note delivery or TypeError for malformed `__notes__`; six outer-helper traces reach baseline `sqlalchemy.py:946`. The four lower-helper arms likewise fail identity, at regression line 118. Later per-arm cleanup/order assertions are consequently not reached in these failing baseline arms; they are requirements for an amended PASS, not independently passed baseline assertions. The ordinary-note arms verify context/cleanup/notes, while absent/inactive controls verify no cleanup initiation. The terminal text reports `Ran 3 tests in 0.003s`, `FAILED (failures=10)`; this timing is no performance claim.

## Origin and preservation

RESULT reports source/dependency after-equality true, 221 mapped source files per view and 15 loaded Cryptalis files. Independently reconstructed the complete expected pin map from reviewed INPUTS and compared it to AFTER: exact 1,332 keys/digests, matching metadata keys, all unchanged and errors `[]`. Every recorded read is pinned. All 367 loaded-file records have admitted origins and expected digests; AFTER and LOADED_MODULES agree exactly. The Cryptalis closure is exactly the reviewed 15 eager files under V7 baseline/source221, including baseline helper hashes `28cf5c4991aae1cb4f3baf6a5630b30d675cb2308e842ce09fd6a04ddaaf5a88` and `cb128481811576d8f16b233d4a30fca060eb9a1bfc4459d5e7e129434cc522ec`. No installed Cryptalis substitution is present.

Root/child exit 1 is explained by the intended unittest failures. Host-after-exit and preservation-after-exit are both 0. Both namespace before/after records match their exact controls; source/dependency preservation records are byte-identical. Fresh bytecode prefix is absent. All three JSON receipts parse completely (RESULT 203,470 bytes; LOADED_MODULES 96,832; AFTER 848,142); no timeout, truncation or post-admission error appears. Root stdout/stderr and child stdout are empty.

Evidence hashes:

- root selection.json: `21cefb3cdf66a56b69b680fd5634f6abfbf8b1ac0e50351756d91da91f702712`
- RESULT.json: `88cd600657e95c58555b2fd347552e7be7f3164a4e634704d4730b7d6e1fd4d2`
- LOADED_MODULES.json: `592c4e7af404fd5321b468d485613a85210201e554748d5a96db89ef21596912`
- AFTER.json: `ce068e14c3e52327c37dcb1b77828efa6a1d88ac50b56f0c44e01ee526f10392`
- stderr.txt: `ada1a8a55b88e504d67243d5ef93beabad44bcb884371ad9fc5417963b1de552`

Scope: synthetic direct-helper tests using real admitted modules and doubles; no database or physical release observation, public integration qualification, marker/name-hook correction, full suite or gate closure. Amended and SA20 outcomes remain pending separately selected processes. Reviewer inspected safe records/static test source only, with no test rerun/import, live dependency/host body read, DB/status, installation, product edit or Git action.

# V7 SA20 baseline: accepted bounded regression RED

Decision: ACCEPTED_EXACT_SYNTHETIC_UNIT_RED, 2026-10-16 10:44 UTC. Separate root-selected SA20 baseline process completes 3 methods and 15 arms: 10 intended assertion failures, five passing controls, zero errors/skips. Its method and subcase ledgers exactly equal accepted SA21 baseline review `7ca405468e90be6bd5b50a725360b035e84a19362c2db60435056d8f5f72b72e`.

Evidence: `experiments/orm-flush-diagnostic-unit-packet-v7-20261016/run/sa20-baseline`; root capture `persistence-recovery-20261013/flush-unit-v7-sa20-baseline-root-20261016`. Root selection and child argv match the accepted V7 command, driver and INPUTS; test identity remains `2bff9041c9e2e0f34eaecc02b56dcbe5bec28afd3bc16546afa3afcf3141baf7`.

The six override/unavailable-note × success/rollback_failure/quarantine_incomplete arms and four override/unavailable × close_fails False/True arms fail the intended primary-identity assertion. Replacement exceptions are the synthetic note RuntimeError or malformed-notes TypeError. Three ordinary-note arms and absent/inactive controls pass. Method outcomes are ASSERTION_FAILURE, ASSERTION_FAILURE, PASS. Later cleanup-order assertions are not reached in failing baseline arms; no baseline pass of those assertions is claimed. Stderr confirms `Ran 3 tests in 0.020s`, `FAILED (failures=10)`; timing is not performance evidence.

Independent reconstruction verifies the complete expected 1,327 pin keys/digests and metadata keys; AFTER reports all unchanged and errors `[]`. All 366 loaded-file records match admitted paths/digests, agree across AFTER/LOADED_MODULES, and every recorded read is pinned. Exact 15-file Cryptalis closure uses baseline/source221 and selected SA20 dependencies; baseline helper hashes remain `28cf5c4991aae1cb4f3baf6a5630b30d675cb2308e842ce09fd6a04ddaaf5a88` and `cb128481811576d8f16b233d4a30fca060eb9a1bfc4459d5e7e129434cc522ec`. Both source namespace checks match exact controls, before/after preservation receipts are identical, host-after and preservation-after exits are 0, and bytecode prefix is absent. Root/child exit 1 is the intended unittest RED; complete RESULT/LOADED_MODULES/AFTER receipts distinguish it from setup/guard failure.

Hashes:

- selection.json: `e5809dbe7b7aa929a9e75642cf9143b1885601bd33191946d662b0e772bad496`
- RESULT.json: `e05ab4e92fbcda0421d0ef15c5fbd100fce852d4ce4e350705c006c9c08b0265`
- LOADED_MODULES.json: `5a151e4a82d6d181bcb75ee52d0432958750fa1000adc6d1417c45ce8db11cfb`
- AFTER.json: `1c390d938dfb6f61d3905257375c253672580e69c6e7866f2a9f199e1352f1ad`
- stderr.txt: `65fd65788075472ade4096eb6ed9afc72eb4dd99821b12027972eb50aeccd24c`

Only the synthetic direct-helper regression is accepted. No public/database/physical-release/full-suite/installed-product qualification, performance comparison or gate closure. SA20 amended remains separately reviewed. Reviewer performed no rerun/import, live host/dependency body read, DB/status, installation, product edit or Git action.

# V7 SA21 amended: accepted bounded unit PASS

Decision: ACCEPTED_EXACT_SYNTHETIC_UNIT_PASS, 2026-10-16 10:44 UTC. Separate root-selected SA21 amended process: 3 methods, exactly the same 15 arm identities as accepted SA21 baseline, all PASS; zero failures/errors/skips. Root/child exit 0. Baseline RED remains preserved in review `7ca405468e90be6bd5b50a725360b035e84a19362c2db60435056d8f5f72b72e`.

Evidence: `experiments/orm-flush-diagnostic-unit-packet-v7-20261016/run/sa21-amended`; root capture `persistence-recovery-20261013/flush-unit-v7-sa21-amended-root-20261016`. Root selection pins V7 command review `6c7f7a6c27bc6d8e20c6476ef2ab1809bb1e3b50787349023e446db33c76c1c7` and accepted baseline. Test remains `2bff9041c9e2e0f34eaecc02b56dcbe5bec28afd3bc16546afa3afcf3141baf7`.

Independent exact-ledger comparison confirms nine ordinary/override/unavailable-note × success/rollback_failure/quarantine_incomplete arms; four override/unavailable × close_fails False/True arms; two absent/inactive controls. All methods and arms PASS with no exception type. Successful outer arms reach assertions for original primary identity, cleared preparation, exactly one cleanup call, original exception context, bypassed override and correct available/unavailable notes. Successful lower arms reach exact capture flag True and sequence `begin, rollback, invalidate_first, close_first, invalidate_second`, later connection invalidated, expected incomplete flag, primary identity and note handling. Assertions are outside the product catches where required. These are observations with doubles, not physical database/driver release evidence.

Reconstructed the expected full pin map from reviewed INPUTS: exact 1,332 pinned keys/digests and metadata keys; AFTER reports unchanged with errors `[]`. All 367 loaded-file records match allowed paths/digests; AFTER and LOADED_MODULES agree; all recorded reads are pinned. Cryptalis closure is exactly the reviewed 15 files under amended/source221. The two amended helper digests are `5ccac0060cb70dee9be4257289f8d9120e2f09ef88d9528ea139605d670a73fc` and `2d08b41c96ecabe99d8339fb7778c0b050b5338885d6292841943f3b409a5bc5`; no installed Cryptalis substitution. Both source namespaces exactly match expected controls before/after, preservation receipts are identical, host-after/preservation-after exits are 0 and bytecode prefix is absent. Complete RESULT/LOADED_MODULES/AFTER records parse. Stderr is the expected three-method `OK` report (0.001s, no performance inference).

Hashes:

- selection.json: `7dacd1d7a37065402d930d2ebf693b9fc31e734b7def9ea199bf4678702eaa22`
- RESULT.json: `b0ae948d74970a4a46075107f25c29eac2a0c943e5cd99a89dcda709e7b6c7bd`
- LOADED_MODULES.json: `8f02f98d8f3ec94bd1af08bc8bc3b5b4475b21f702efd867cbb15ad3d08fa227`
- AFTER.json: `1742886f87799566d7742bd5a56174c17c11d08e276992f6098492a7af2cd020`
- stderr.txt: `f522f5354d8f2e6be5980a2aac788822375495dc9debefa9e351d9d2211c5f0d`

Scope is the note-only two-helper correction in this real-module deterministic unit matrix. Marker/getter/setter/name-hook hardening, public integration, physical connection outcome, full suite, installed-product qualification and external gates are not established. V5/V6 setup holds are separate zero-test records. Reviewer inspected safe receipts/static source only; no rerun/import, live host/dependency body read, DB/status, install, product edit or Git action.

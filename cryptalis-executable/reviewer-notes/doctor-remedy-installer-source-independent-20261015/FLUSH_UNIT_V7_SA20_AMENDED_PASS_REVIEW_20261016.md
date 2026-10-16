# V7 SA20 amended: accepted bounded unit PASS

Decision: ACCEPTED_EXACT_SYNTHETIC_UNIT_PASS, 2026-10-16 10:47 UTC. Separate root-selected SA20 amended process: 3 methods, exactly 15 arms, all PASS; zero failures/errors/skips. Method and subcase ledgers exactly equal independently accepted SA21 amended review `639e3976d73ce5e282e3941001b4b44ac8a1384b3c46770ad1b2ac645901c204`.

Evidence: `experiments/orm-flush-diagnostic-unit-packet-v7-20261016/run/sa20-amended`; root capture `persistence-recovery-20261013/flush-unit-v7-sa20-amended-root-20261016`. Selection and actual argv match V7 command review `6c7f7a6c27bc6d8e20c6476ef2ab1809bb1e3b50787349023e446db33c76c1c7`. Root explicitly selected on its checked actual predecessor receipts while two peer reviews were finishing; the receipt accurately records that timing.

The same nine primary/cleanup variants, four lower cleanup-fallback variants and two absent/inactive controls all reach the assertions detailed in the SA21 amended report: original primary identity/context, preparation cleared, cleanup invoked once, exact True capture flag, exact begin/rollback/first-invalidate/first-close/second-invalidate order, later-connection continuation, expected incomplete flag and safe/unavailable notes. Test identity remains `2bff9041c9e2e0f34eaecc02b56dcbe5bec28afd3bc16546afa3afcf3141baf7`. These are synthetic doubles; they establish no actual database/physical release result.

Independently reconstructed and matched all 1,327 expected pin keys/digests and metadata keys; AFTER reports unchanged with errors `[]`. All 366 loaded-file records have expected admitted origins/digests and agree across receipts. All recorded reads are pinned. Exact 15-file Cryptalis closure uses amended/source221 with the reviewed two-helper patch and selected SA20 dependencies, with no installed Cryptalis substitution. Both source namespaces match controls before/after; preservation receipts are identical; bytecode prefix is absent. Root/child/host-after/preservation-after exits are all 0. Complete RESULT (202,173 bytes), LOADED_MODULES (96,442) and AFTER (844,411) parse. Stderr is the expected three-method OK report (0.001s, no performance inference); stdout/root stderr are empty.

Hashes:

- selection.json: `3a7db3b117d5d5eb92b220e2c230952848262d231c5ec293b80cae91e084fba6`
- RESULT.json: `60473dd540d1fc7c142e91415e64d9f714015cb1f13a8c48d341bc80366c6a17`
- LOADED_MODULES.json: `0a30d97b8b4cbfbc33b731bc6d7426943945f6fc1acfc9abbc65a1054a6e340f`
- AFTER.json: `f75d14532502cf9d97a85873c55eee455e317a494fab8d3bb343a4ea90abfc81`
- stderr.txt: `f522f5354d8f2e6be5980a2aac788822375495dc9debefa9e351d9d2211c5f0d`

Only the note-only direct-helper unit slice is accepted. Marker/name-hook hazards remain unresolved by it; native 48-case work remains approval-pending, with no authority inferred from this result. No public integration/full-suite/installed-product qualification, performance claim or external gate closure. Reviewer performed only safe receipt/static-source inspection, no rerun/import, live host/dependency body read, DB/status, installation, product edit or Git action.

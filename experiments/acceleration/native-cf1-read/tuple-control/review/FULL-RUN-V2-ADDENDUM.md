# V2 cache-provenance fix: bounded source clearance

2026-10-14. FULL_RUN_FREEZE_V2.json SHA256 `5baccd54e797c542faa240d24ec6d8e27aea8bbae01dcf3cd952770d7b4e9e01` reviewed without candidate build/import/execution.

All 4,459 pins match current bytes. All 4,387 V1 pins are preserved unchanged. Exactly 72 entries are added: 69 existing cryptography bytecode caches, the original V1 freeze itself, and two additive gate/launcher sources. Exact cache inventories match for all five scoped roots: cryptography has69 caches; S20 source, T, original fixture helper and correction helper trees have none. All inventoried caches are pinned.

`full_run_cached.py` checks V2 file pins and cache inventories before invoking unchanged V1 full_run.py via runpy, then repeats the checks in finally and emits an exclusive-create cache receipt. `full_launch_v2.py` requires before/after PASS and the expected V2 freeze hash in that receipt, records its hash, and applies unchanged ordinary/-O positive/negative acceptance rules. A failed initial check cannot be accepted merely because the final check passes: the launcher additionally requires the before PASS field and the original result receipt. Both additive sources parse, and V1 source/freeze bytes remain unchanged.

The identified cache-read provenance gap is resolved for these declared import roots. This remains bounded source/binary/cache provenance, not a complete hermetic interpreter/OS attestation or independent proof that cached code was generated from the pinned source. No cache is rewritten or deleted.

No remaining concrete source blocker was identified for coordinator authorization of the bounded 1098-case,14-child wrapper validation through full_launch_v2.py. This is conditional source-review clearance, not execution authority or a PASS result. Actual fork, allocation fault hooks, skipped-term/final code mutants, after-helper lease-expiry coverage, sanitizers/leak tooling, full DESIGN admission and any timing/product decision remain separate and unclaimed.

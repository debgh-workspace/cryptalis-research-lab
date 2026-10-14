# Independent r3 constructor-local reuse review

2026-10-14. Static source review only. No imports, tests, database, Git or product edits.

**CLEARANCE for the minimal r3 source change.** This is not a runtime performance result, integration decision, or promotion. R2's reported timeout remains historical evidence and is not converted to PASS.

Independently recalculated identities:

- R3 source manifest: `eef841a5ee605a8763784640b841a62931f15767e3616f33bb4bb40170b96323`
- R3 deprotection.py: `8277154feba671a663e4be13fba17090c4a85f5579f1c2bbfc30114e00c7a64a`
- Unchanged r2/r3 comment helper: `00c6bc68768fffc813bdfa4ee5302e93d4f76a9754b7b704955cf186c978192c`
- R2 source manifest: `f60c533cd016eee96c2045ddd3efe95633aaf07b2df5761bc2b6bcd695c32741`

A fresh recursive byte comparison found only deprotection.py changed from r2. Its exact delta adds `source_operation_id = source.operation_id` immediately after successful source-pin admission, then uses that local UUID in the existing reverse/source inequality and retired-history source-exclusion comparisons.

MigrationPlan is constructed from canonical immutable source artifact bytes. Its operation_id property obtains the UUID by parsing those same bytes. The constructor does not mutate that source artifact. Reusing the admitted UUID therefore preserves the comparison result. The earlier eager local read does not admit any document or bypass checks: source construction and `_admit` already require valid source identity, and all exceptions remain inside the same constructor refusal boundary.

No set membership, key/digest requirement, source/reverse pairing, type rule, source-pin rule, canonical-byte correspondence, policy subset, envelope budget, or lifecycle hook changes. There is no shared or persistent cache. This local optimization applies to both reverse formats without changing their accepted artifact semantics.

The history loop no longer reparses the entire embedded source once per item. It still parses each history UUID and checks duplicate/current/source exclusions and exact digest syntax. Other fixed-count document reads remain, so actual performance is a runtime question. No timeout extension or reduced test coverage was reviewed or approved here.

The r2 C1 clearance and recovery-hook review remain applicable because their source logic is unchanged. Root must independently check the r3-routed test/command packet and retain distinct r2/r3 receipts.

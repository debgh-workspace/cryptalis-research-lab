# S25 SA21 terminal audit

CLEAR to the frozen SA20 block. This aggregate is baseline-equivalent, not all green.

All2639 ordinary testcase identities and outcomes match R3 exactly:2632 passed,7 failed,0 skipped/errors. All seven historical failure messages match. The complete progress report multiset, including setup/call/teardown phases, matches R3. There are56 passing subtest events separately; runner2688 passes includes them. No new skip, missing test, selector, or hidden failure waiver is present. The sole explicit ignore is the new optional SQLModel test module. Summary:7 failed,2632 passed,50 warnings,56 subtests passed in412.23s. Wrapper/runner exit1 remains recorded.

All216 candidate manifest hashes match. All155 wrapper source/config entries are unchanged and match archived source and manifest; runner source pins match. Both1201-entry pre/post pin logs pass and all1201 inputs were independently rehashed. All19 archival packet copies match. External-source snapshots remain empty and unchanged.

Fresh dual-role preflight passes and package origin is S25 source. PostgreSQL shutdown confirms server stopped. All26 prior-corpus archives and restored primary files match. The generated candidate corpus archive matches its isolation hash; no deletion or isolation error exists. Setup/teardown progress matches the baseline without nonpassing phases.

The seven failures remain open. No new runtime capability or production gate is qualified. Optional38 coverage is separate from this full2639 baseline selection. Independent audit remains required after SA20.

Artifacts: SA21_TERMINAL_AUDIT.json, SA21_EXACT_OUTCOMES.tsv and audit_aggregate_terminal.py. Evidence-only filesystem review; no test/database/candidate import actions and no raw environment-bearing phase JSON reads.

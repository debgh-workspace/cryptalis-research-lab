# S24/S25 correctness register addendum

Updated 2026-10-14 21:16 UTC. Additive to the frozen historical defect register; no historical outcome is overwritten. Coordinator-owned current status also lives in CRYPTALIS_BUILD_CHECKLIST.md.

## SQLMODEL-PROVIDER-ORACLE-01 — test defect, bounded correction verified
V2 core had 33 PASS/3 FAIL because protected provider errors were incorrectly required to retain original object identity. Existing keyring contract raises a fresh sanitized KeyUnavailable from None. V3 changes only those assertions, preserves native identity and all downstream freshness/no-SQL/rollback/retry checks. Targeted3 passed, core36 passed, separate DML2 passed. Independent audit verifies38 distinct nodes; targeted3 overlaps. Do not claim the failed V2 downstream assertions ran. Product bytes unchanged between V2/V3. Source integration S25 optional38 passed6.60s; full SA21 retains exact R3 outcomes2632P/7F,56 subtests. Full SA20 matches R3:2586P/7F/46S and56 passing subtests; all2639 IDs/outcomes/failure messages independently verified. InstalledS25 remains pending.

## SQLMODEL-ASYNC-PUBLIC-HOOK-01 — bounded prototype, integration in progress
Public sync_session_class composition reaches genuine native SQLModel exec while retaining protected result/cleanup boundary. Default-off, exact existing SQLModel0.0.47/SA2.0.51 cell. Six baseline shape arms refused attachment after successful native controls; new route passes entity/scalar/tuple/count/parameter/SA-select controls. Result-fault tests use a synthetic post-native seam and do not establish arbitrary driver-fault behavior or protected-field bulk DML admission. S25 source-overlay integration and installed qualification are separate gates. No 600-key corpus reclassification yet.

## STATS-CLEANUP-01 — source proposal rejected before execution
Private unhooked observer V1 transaction context could replace primary query error/cancellation with rollback failure and under-report cleanup failure. V2 source independently reviewed as structurally corrected: explicit primary capture, rollback/quarantine reporting, fixed classification and trusted-host logging limits. No runtime claim. V2 packet remains HOLD for unbounded fixture ANALYZE, invalid unknown-typed schema mutant, snapshot race accounting and incorrect wrapper proposal. V3 fixes these in source; review pending. Baseline214 product files remain unchanged; no public call or automatic ANALYZE.

## EVIDENCE-PREP-HEREDOC-01 — preparation process defect, preserved
Installed legacy V1 unquoted Markdown heredoc invoked both entry scripts. Both failed at missing ENTRY checks before wrapper/database entry. V2 literal preparation preserves original failure logs and all producer/consumer assertions. Actual V2 installed legacy cells each pass10 parent phases and10 genuine S23 producer children;137 independent checks each plus10 cross-cell checks. No process-crash/lost-ACK evidence implied.

## Historical acceptance conflict — OPEN
Seven deprotection-ordinal assertions still fail identically to R3/S23. Version-specific profile acceptance decision is pending; no skips/xfails/waivers or silent weakening. Retained-profile safe in-place semantics and older public-copy expectations must remain separately evidenced. All seven qualification gates UNKNOWN.

## Recovery evidence
S24 r3 full source/evidence c4052dff7ad3a5c36e27e5775b52b650bdc012e8:1240 archive members/214 source files restored. Additive qualification e271ebc7da3e723f9827caf471ed9b4bd2dda40f:523 members restored. SQLModel/legacy additive2fc689f7c1bdceb37710270c2f8b785a6b609866:702 members restored. All exact remote bytes verified; data-only recovery is not operational database/dependency/independent-host recovery. Original mailbox remains9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd.

## STATS-TEST-CLEANUP-01 — actual V3 G1 failure, correction pending
V3 G1 SA21 produced20FAIL/9PASS/66deselected7.79s. All20 failures terminate at test-owned unconditional invalidate after observer closed the SQLAlchemy connection. These finally failures can mask earlier assertions; no failed node is relabeled. Samepattern in unrunG2 found. Nine actualpasses remain bounded; collector statistics-stage loop didnotexecute. Safe wrapper records tests exit1 and postgres-stop exit0, complete source/pins/corpusrestoration check. V4 test-only correction pending.

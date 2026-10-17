# Runner V2 independent source acceptance

Disposition: ACCEPTED SOURCE ONLY within the expressly selected existing-host interpreter/stdlib/native-loader boundary. Execution requires root's separate current admission and selection. No correctness or performance result is claimed.

Reviewed recovery-work/search-next-slice-20261017/runner-v2, SOURCE.sha256 seal 4747b053405eafe60a656f95adda95ea483bc3d3cfd676570517206d0e85059c; all 263 members verify. Runner SHA256 6b566ce3186cffc9db4e2e436628dd9cd1ce01f16304ec1fbf4946bad8047688. Six source views are byte-identical to preserved V1 views.

The V1 defect recorded in RUNNER_V1_REVIEW.md is resolved. expect_error invokes only the operation under test, catches Exception, and asserts exact exception class. Missing or wrong exceptions become explicit test failures. Setup and fixture construction remain outside this wrapper; BaseException is not swallowed. The seven replacements preserve AuthenticationFailed and KeyUnavailable literal requirements. Lambda calls occur synchronously, so loop-variable late binding does not alter tested cases. No arbitrary unittest error is accepted as a mutant kill.

The runner diff is only this helper, seven operation wrappers and the absolute V2 directory binding. PLAN documents the preserved V1 hold and correction. Previous source review of tenant identity/fallback, 23 literal observer cases plus subtype/codec and eight-combination real-CF1 checks, meaningful negative controls, 448-identity before/after closure and failure handling still applies.

External execution prerequisites remain: exact host/source/tool admission and invocation, absent pycache prefix, external time/CPU/memory/combined-output enforcement and termination evidence, complete terminal JSON with all closure checks PASS, and independent interpretation of required mutant failures with no setup/import primary or test errors. Source acceptance is neither SA20 nor DB qualification, native provenance assurance, provider-custody evidence, benchmark evidence, nor a hostile-code sandbox claim.

No target imports, syntax checking, tests, DB operations or candidate mutation performed by this reviewer.

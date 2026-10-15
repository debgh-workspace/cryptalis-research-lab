# Expected-RED SA21 terminal review

Verdict: EXPECTED_RED_VERIFIED for this nine-case source-overlay sensitivity campaign only. The observed six failures remain FAIL receipts; they are not relabeled as six ordinary passes or product late-corruption detection. GREEN and SA20 qualification are separate work.

## Evidence identity

- Coordinator: /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/retained-contract-red-sa21-coordinator.
- Capture: experiments/retained-contract-red-sa21-capture-20261015-v1.
- Evidence: evidence/retained-contract-red-sa21-20261015-v1.
- Plan: experiments/retained-contract-correction-20261015/runtime-plan-v1, externally bound PLAN_PINS SHA256 147c3077d7354c5fb599b058974c2364181a4596ab22d968616a8434287e8f70.
- Safe-evidence addendum SHA256 af762218a1d6a8d58c4a79bcfd522c786f741ce24a3442ffd09f7171e385811f is explicitly pinned in coordinator selection.
- RED_SA21_TERMINAL_CHECKS.json preserves the exact safe read set with hashes and all 27 successful reconciliation predicates. No unrestricted evidence-tree hash or copy was used.

## Exact observed result

Setup process exit 0. Test runner, wrapper, launcher and coordinator launch exit 1, as expected for RED. JUnit: 9 tests, 6 failures, 0 errors, 0 skipped. Progress has exactly the expected nine starts and 27 reports: all nine setup and teardown phases pass, three call phases pass, six call phases fail. No missing or additional ID appears. Exact runner argv matches the reviewed nine explicit selections plus unchanged progress/JUnit capture arguments.

Three unchanged positive IDs pass:

- tests/test_deprotection_ordinals.py::test_reverse_preserves_public_null_unicode_and_native_order
- tests/test_deprotection_ordinals.py::test_old_unversioned_staging_requires_inspection
- tests/test_deprotection_ordinals.py::test_abort_removes_every_ordered_stage_and_preserves_protected_values

Five metadata mutations fail at tests/test_deprotection_ordinals.py:31, reached through the real post-apply oracle at line 65, with AssertionError: native public metadata changed:

- comment: native catalog index 12 changed from the current Unicode comment to NULL.
- column_grant: native ACL index 11 changed from the exact column SELECT ACL to NULL.
- statistics: index 10 changed from 100 to -1.
- storage: index 8 changed from e to x.
- compression: index 9 changed from p to the default empty code.

The current-value mutation fails at tests/test_deprotection_ordinals.py:66, with AssertionError: native current values or visible order changed. Actual native rows contain the injected obsolete-copy marker instead of the independently expected current public value. The failure is not an injection assertion, preflight failure, product refusal, unrelated error or teardown failure.

This runtime evidence, bound to the reviewed mutation source, establishes acceptance-oracle sensitivity after successful real apply. It does not establish that product verification detects corruption introduced after apply returns.

## Source and boundary reconciliation

The coordinator selected the exact reviewed setup/launch argv and externally pinned the original plan, scripts, independent review, dependency admission and safe-evidence addendum. All those pinned public artifacts match their digests. Captured before/after pin records are identical with no mismatches. The full 219-file sealed source and exact RED derivative hashes in those records match their expected manifests. The setup receipt records only the admitted mutation override and an unchanged sealed source. The wrapper's 158-entry source snapshot and runner source/test hashes match the RED manifest; source and external-source stability receipts show no changes.

Safe wrapper output records start 0, readiness 0, package-origin 0, tests 1 and stop 0. The safe readiness log and runner receipt establish both required real preflight probes. The package-origin log points to the selected RED derivative/src/cryptalis/__init__.py.

All three required safe shutdown observations agree: wrapper postgres-stop exit 0; postgres-stop.log says server stopped; independent post-run pg_ctl status exits 3 and says no server running. Pre-run status also exits 3. This establishes the campaign's recorded terminal stopped boundary, not an indefinite claim that no later authorized campaign can start.

The 26-entry independent pre/post corpus maps and prior-corpus manifest are identical. The corpus-isolation receipt records primary_receipts_restored=true, errors=[], no archived changes and no deleted-during-run files. Boundary summary agrees with the underlying safe receipts and is not used as the sole acceptance oracle.

## Preserved incident and scope

The first literal metadata listing incorrectly placed the coordinator path beneath B=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable instead of W=/workspace/scratch/cb28ee9f5f4a. It failed with FileNotFoundError and command exit 1 at 11:33 UTC, before capture/evidence listing. The reviewer immediately reported and paused. Root supplied the exact W/persistence-recovery-20261013 path and explicitly authorized narrow metadata and continued admitted safe evidence review at 11:34 UTC. The wrong-prefix failure was not retried or hidden. No later check failed.

No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json content was read, hashed, copied, printed or archived. Metadata listings showed filenames only. No credentials, raw environment, target import, collection, database action, test execution, environment activation, installation, network action or Git command was performed by this reviewer. No candidate or previous receipt was changed.

The verdict is confined to source-overlay SA21 expected-RED. Installed-product bytecode equality, continuous subprocess source identity, the unchanged candidate's GREEN, SA20, broader suites, genuine old-artifact compatibility, CLUSTER integration and production/security/release gates are not established here.

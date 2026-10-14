# Maintenance budget boundary review

Date: 2026-10-14. Independent static and saved-evidence review. No tests rerun, database accessed, Git operations performed, or product/test files changed by this reviewer.

## Assessment

No blocking issue found in this bounded correction. The change applies `math.isfinite` only to exact floats after retaining the exact int/float type gate. Exact integers retain mathematical comparison semantics without an invented production pause ceiling. Invalid types, bools, numeric subclasses, nonfinite floats, and budgets below the plan estimate remain refused. Writer exclusion, external pins, plaintext consent, removal evidence, compiler admission, and connection ordering are unchanged.

All six affected public entrypoints are covered: migration apply/verify/abort and deprotection apply/abort/remove. The 132 new cases comprise 22 budgets per entrypoint. Rejections assert the exact typed code and operation ID, no explicit cause, and no consent/compiler/connect/provider calls. Accepted budgets traverse applicable real plaintext consent and stop at an identity-checked compiler-entry sentinel before database work. These structural-plan controls qualify only the input boundary, not full lifecycle behavior.

## Saved evidence verified

Read only the permitted runner receipts, test logs, progress records, source manifests/stability records, source-root records, and package-origin logs. Did not read tests.json, package-origin.json, environment values, or credentials.

- `evidence/maintenance-budget-red-20261014`: 12 failed, 120 passed, zero skipped; pytest log elapsed 0.92 seconds; exit 1. The 12 failures are exactly huge-positive-int and huge-negative-int across all six entrypoints. Progress records agree with the runner receipt and test-log summary.
- `evidence/maintenance-budget-green-sa21-20261014`: 224 passed, zero failed/skipped; pytest log elapsed 116.61 seconds; exit 0.
- `evidence/maintenance-budget-green-sa20-20261014`: 224 passed, zero failed/skipped; pytest log elapsed 113.36 seconds; exit 0.
- Each GREEN receipt and progress stream accounts for 132 maintenance boundary cases, 40 existing migration audit cases, and 52 existing deprotection cases. The existing database tests supplement, rather than replace, the pure boundary controls.
- Each source-stability record has identical before/after maps and `unchanged: true`. Its before map equals source-before.json, with 148 entries. Every overlapping runner-receipt hash matches that map.
- The runner receipt additionally records scripts/test_postgres.py, absent from the 148-entry source-before map. Its hash is identical in all three receipts; source-root records separately state `preflight_unchanged: true`. This is a recorded preflight attestation, not a claim that the 148-entry map includes the runner.
- RED and each GREEN source/test receipt manifest differ only at src/cryptalis/migration.py. Both GREEN manifests are identical. The new test bytes and all existing recorded test inputs are unchanged between RED and GREEN. No assertion weakening explains the result.
- Source-root records identify the RED derivative and GREEN maintenance candidate respectively. Package-origin logs verify imports from the corresponding candidate source. These are source-run observations, not installed-wheel qualification. Dependency-cell names identify the supplied SA21/SA20 evidence; this safe audit does not independently inspect installed distribution metadata.

## Exact hashes

SHA-256:

- RED migration.py: `64c9ff601a36352f5cee74d6d11b4ff8a469f10475816b2fac335327f7afe1b8`
- GREEN migration.py: `0c6df2baa2b3b8c25a9dedb5ee2d6e7a1b47804da3e04ebf4dda5c2a3a465b9a`
- test_maintenance_budget_boundary.py: `ea8e48b6304887d65df72d0b0d0ad3ee99a4fd97bfabfa13aedc32693129ab81`
- Recorded scripts/test_postgres.py: `118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12`
- RED runner-receipt.json: `d71a13218615ac8946c3cc9b745b55e034d703ab709862d5708cc6655eb323ae`
- GREEN SA21 runner-receipt.json: `25d7ac886702e634e60e600c6e9fe4b761b9d7fe88962777107e78d16131aff8`
- GREEN SA20 runner-receipt.json: `1df6b39b838c521fa3bbf0192e28c021815496dd3aef83403367729dd4ce9f25`

Direct hashing confirms that candidate-s21-correctness-20261014 contains the exact reviewed GREEN migration.py and new test file above. This checks only these two transferred files, not the entire combined candidate.

## Publication boundary

The evidence supports describing the maintenance-budget correction as bounded, tested research evidence and including its exact bytes in fresh combined integration. It does not qualify the source-lock/scanner composition, a full source suite, installed wheels, deployment writer exclusion, or a production release. Fresh combined-candidate qualification remains necessary; isolated passing suites cannot be substituted for it. No publication or promotion was performed. All seven production gates remain UNKNOWN.

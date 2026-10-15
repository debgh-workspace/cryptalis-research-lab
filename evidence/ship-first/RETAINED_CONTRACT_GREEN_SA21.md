# GREEN SA21 terminal review

Verdict: FOCUSED_GREEN_SA21_VERIFIED. The reviewed sealed candidate passes all 16 intended cases in both complete affected files. SA21 expected-RED remains six actual failure receipts plus three positive passes; nothing rewrites or reclassifies those failures. The SA21 focused RED/GREEN pair is complete. The evidence permits root to select the already reviewed SA20 RED action, subject to its unchanged fresh-destination, pin, authorization, no-overlap and pre-run stopped-state gates. It is not an automatic execution instruction.

## Evidence identity

- Coordinator: /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/retained-contract-green-sa21-coordinator.
- Capture: experiments/retained-contract-green-sa21-capture-20261015-v1.
- Evidence: evidence/retained-contract-green-sa21-20261015-v1.
- Exact selection: runtime-plan-v1 green-sa21, both entire tests/test_deprotection_ordinals.py and tests/test_retained_contract_mutations.py.
- PLAN_PINS SHA256 remains 147c3077d7354c5fb599b058974c2364181a4596ab22d968616a8434287e8f70. Root selection explicitly pins the preceding RED terminal review and safe-evidence addendum.
- GREEN_SA21_TERMINAL_CHECKS.json records all 25 successful reconciliation predicates and the exact safe file hashes used by this review.

## Runtime result and case identity

The coordinator, launcher, wrapper and runner exit 0. JUnit records exactly 16 tests, zero failures, errors or skips. All 16 exact case identities and their order match the reviewed selection. Progress records 16 starts and exactly 48 passing reports: setup, call and teardown for each case. No case was missing, substituted, duplicated, skipped or reported as an expected failure. Runner counts and exact ordered pytest arguments match the wrapper's reviewed selection plus unchanged progress and JUnit capture options.

The 16 cases are the seven current-contract replacements, three unchanged original controls and six captured sensitivity controls. Their source hashes match the reviewed tests and helpers. This binds the successful calls to these assertions:

- Comment, column grant, statistics, storage and compression are actually set to the intended nondefault native states. PostgreSQL catalog identity/metadata and current public values survive read-only planning, reverse apply and final removal. Native SELECT * names/order/all values are compared. The grant case also checks effective SELECT and absence of retired write privileges after removal.
- Protected-stage corruption triggers the specified value_verification_failed refusal twice, while native catalog/journal/current-value snapshots and independently decoded encrypted frames remain exact. Only the deliberate fixture stage corruption is repaired; the same operation resumes at a 512-byte budget and retains wide current public edits, native order and metadata through removal.
- The untouched-public transport case executes the native libpq-buffer observer: current wide public values are excluded from bounded transport, provenance and identity order are checked, and actual logical fetched bytes satisfy the budget. This does not establish RSS/server/WAL/disk bounds. The separately collected protected-byte backfill/verify refusal controls and other companion modules are not silently counted as executed by this two-file campaign.
- Original native NULL/Unicode/order, old unversioned-stage inspection and ordered-stage abort preservation controls remain passing.
- Each of the six captured sensitivity controls executes real apply, injects an actual post-apply native metadata/current-value change, and catches only the intended independent assertion. The mutation observation assertions pass. Their matching uncaptured expected-RED failures were independently verified in the prior SA21 campaign.

The sensitivity pair proves the acceptance oracles detect the injected native output regressions. It does NOT prove product detection of corruption introduced after apply has returned. Genuine pre-effect safety evidence here is the separate stage-corruption/refusal/recovery case.

## Closed boundary and source stability

All captured pins are identical before/after and have no mismatches. All 219 sealed candidate source pins match the accepted manifest; the source snapshot and runner source/test hash map agree. Source and external-source stability reports show no change, with no external selected source. The candidate was never temporarily patched for RED, so this GREEN is directly against the original sealed source.

Safe wrapper output records start/readiness/package-origin/tests/stop all at exit 0. The safe readiness log and runner receipt confirm both required probes. The safe package-origin log identifies candidate-retained-contract-correction-20261015/src/cryptalis/__init__.py.

Shutdown is independently established by the required safe triple: wrapper postgres-stop exit 0, postgres-stop.log reporting server stopped, and post-run pg_ctl status exit 3 with no server running. Pre-run status was also 3. This is the recorded end-of-campaign boundary, not a claim about future authorized activity.

All 26 pre/post corpus hashes and the prior-corpus manifest match exactly. Corpus isolation reports restored=true, no errors, no archived changes and no deleted-during-run files. The boundary summary agrees with the underlying records.

## Safety, incidents and limits

No failed literal lookup, audit assertion or capture read occurred during this GREEN review. The earlier RED wrong-prefix incident remains preserved in its original terminal review. No candidate, existing receipt, plan or earlier review was edited.

Only individually selected safe logs/receipts/JUnit/progress and known public review/plan inputs were read. Raw tests.json, readiness.json, package-origin.json, postgres-start.json and postgres-stop.json were never read, hashed, copied, printed or archived. Directory listings were names only. No credentials, raw environment, target import, test collection, database/test execution, environment activation, installation, network or Git action occurred.

Qualification remains source-overlay SA21 focused only. Installed-product cache equality and continuous every-subprocess source identity remain unqualified. SA20, broader retained/native modules, complete suites, genuine old-artifact compatibility, integrated CLUSTER, installed artifacts and production/security/release gates are not established by this review.

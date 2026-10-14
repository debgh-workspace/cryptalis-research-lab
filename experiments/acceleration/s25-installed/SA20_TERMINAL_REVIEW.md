# S25 installed full SA20 independent terminal review

Verdict: SA20 is exactly baseline-equivalent to the accepted S25 source and R3 main-cell runs. Together with the separately accepted SA21 terminal result, this completes the observed installed full main-cell regression comparison. It is not an all-green result.

## Exact observed result

- 2639 unique ordinary JUnit IDs: 2586 passed, 7 historical failures, 46 skipped, no errors.
- Exact ID/outcome maps, all seven failure messages, and every skipped-node message equal both source S25 and R3. Complete setup/call/teardown progress report multisets also match both references, with 2639 unique start IDs.
- 56 additional passing subtests remain separate. The runner's 2642 passing call reports include these subtests; its 28 skipped call reports exclude 18 setup skips. Total skips are 18 setup and 28 call.
- Terminal pytest summary: 7 failed, 2586 passed, 46 skipped, 2 warnings, 56 subtests passed in 397.95s (0:06:37).
- No new setup/teardown errors. This is recorded cleanup parity, not an independent live inspection of every pool, connection or descendant.

## Completion, pins and payload

Runner, wrapper and outer entry all retain actual exit 1. Post-run pin codes are 0 0 0. Every before/after ENTRY, INPUTS and installed-clearance log exactly matches its manifest's ordered paths and successful checks, covering 3, 457 and 91 entries respectively. All current file hashes and frozen manifest digests recheck. The outer entry log contains the exact 551 initial successful pin rows; its exit receipt is 1.

All 216 candidate manifest files match frozen hashes. All 155 archived source/config entries match before/after snapshots and the manifest. Runner source/test pins match. External-source snapshots are empty and unchanged. All 11 source-packet files exactly match the frozen control packet. Recorded runner arguments select the full candidate tests directory, with only the declared optional SQLModel test module ignored.

Safe package-origin.log identifies the installed SA20 site-packages package and reports 41 byte-matched modules. Independently, all 41 installed runtime modules match candidate source and the actual wheel bytes. The wheel digest remains 42150bab589fcb80083dafb8bd34186c5040776950fa1f5b04b11a43c1e3b36c. The installed-clearance manifest digest remains d7c5c67e140ae48847adea23bf0c655cdf96e7e9f19e03ae235e44679889316c.

Readiness and test logs each record fresh successful dual-role preflight; receipt preflight also passes. Wrapper PostgreSQL stop exit 0 and the explicit server-stopped shutdown log confirm stop completion. All 26 prior corpus archive files and restored primary files match hashes. The one generated corpus archive matches its isolation digest; no deletion/restoration error is recorded.

## Boundaries

Origin evidence comes from a separate process and byte checks; it is not continuous current-pytest or every-subprocess origin attestation. The seven historical failures remain unresolved, and all seven gates remain UNKNOWN: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE. This result does not establish full optional-environment cross-module qualification, independent-host/provider qualification, general package provenance or production readiness.

The reviewer performed only local data parsing and hashing with standard-library tools. No target/dependency import, collection, tests, database action, credential read, remote action or raw environment-bearing phase JSON read occurred. Existing source, runtime evidence and controls were read-only; only this new reviewer directory was written.

## Artifacts and reproducibility

- SA20_TERMINAL_AUDIT.json: machine results, complete failure/skip messages, safe evidence hashes and outer entry hashes.
- SA20_EXACT_OUTCOMES.tsv: all 2639 exact IDs and equal source S25/R3/installed outcomes.
- audit_terminal.py: data-only checker adapted from the reviewed prior terminal checker, extended to independently check exact pin-log paths, outer entry receipts and wheel-module equality. Output creation is exclusive and intentionally refuses an existing result.

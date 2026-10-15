# Independent source review: native abort-envelope representation probe

## Verdict

**The finite native comparison plan is acceptable as source, but the packet is not launchable or admitted.** No substantive defect requiring a change to its test body was found in this source-only review. Its absent outer entry, unresolved authority/selection and pending latest-predecessor binding are real execution blockers. This is neither a native PASS nor a product or v3 approval.

The reviewed packet is `experiments/abort-envelope-native-probe-v1-20261015`. Its seven listed members match `SHA256SUMS.txt` exactly; the directory contains precisely those seven regular files plus the seal. Seal SHA-256: `0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5`. All twelve source/review inputs recorded in `SOURCE_INPUTS.json` match their recorded sizes and SHA-256 values. The original copied conftest matches the transport conftest byte-for-byte. A matching seal establishes source identity, not launch permission.

`STATIC_VERIFICATION.json` records the finite input hashes, exact 31 expected test identities, exact 184 expected state-observation identities and independently checked accounting. No target Python module, launcher, guard, reference or test was imported, compiled, collected or executed. Source AST parsing and reviewer-owned small JSON arithmetic were used. No database/status command, live-cell, installed-payload, corpus, cache, environment, credential, raw-phase, network or Git inspection was performed. All existing files remained unchanged. Only this new reviewer directory was written.

## What question this actually answers

The new body independently constructs synthetic journal-shape values, encodes them with stdlib JSON, and asks PostgreSQL for native `jsonb::text` and native UTF-8 lengths. It imports neither the product nor the pure reference. Consequently the decisive comparison is not a reference function compared with itself:

- The server supplies actual `jsonb::text` and the two `octet_length(convert_to(...,'UTF8'))` results.
- The independent Python encoding supplies compact canonical bytes.
- Native text is parsed independently with duplicate/non-ASCII-key rejection, integer parsing, float/nonfinite rejection, exact recursive type/value comparison and canonical re-encoding. Boolean/integer equality cannot substitute for exact type equality.
- The structural separator count is a separate hypothesis. Equality to compact bytes plus separators is asserted, but actual observed native lengths of each shape are also compared with the separately observed native E.
- Domain observations verify text-format UUID/int8 values, native ordering, the nil/max UUID endpoints, signed-int64 endpoints and integers beyond 2**53.
- Omission controls independently spell out a complete ABORTED value. Omitting verification, cursor or counter reservation must produce an actual measured underestimate in both representations.

This supports a finite native representation observation on PostgreSQL 16 UTF8 / psycopg 3.3.6 in the selected SA21 route. It does not prove every possible JSON value, all widths in both directions/codecs, or a general PostgreSQL serializer theorem. The nineteen families cover both directions, UUID/int64 and mixed models, empty/nonempty counts, Unicode/control strings and selected counter-width edges; the large count grid is forward UUID only. The prior pure-reference argument and its accepted nineteen-method audit remain separate evidence.

The synthetic E is size-only and may combine reservations that are not a reachable persisted state. The positive shape families use reachable phase forms: forward verification absent before VERIFIED and complete at VERIFIED; reverse has none. Each actual pre-switch shape has a phase-only ABORTED copy. The shared shape-family initializer means this is not independent validation of the product's complete journal grammar; the packet expressly leaves schema/guard admissibility and physical journal validation open.

The earlier `NATIVE_PROTOCOL.md` also proposed invalid-depth/shape/refusal and later controlled-transaction questions. Those are not silently completed here. This narrower body does not implement the optional transaction stage or repeat the pure grammar suite. No SQL write ordering, rollback, actual expansion admission, journal PK/ACL shape, authenticated ancestry, legacy/historical abort, durable recovery or v3 release claim follows from a successful run.

## Source mechanics and bounds

Relevant source is `test_native_envelope.py`:

- Lines 75–112 provide the independent canonical encoder, structural counter and exact comparison.
- Lines 128–152 require the existing fresh-preflight marker, no bytecode, driver version and SA21 prefix; open one synchronous autocommit connection; and record native version/encoding/PID plus a database/role digest. The digest is diagnostic consistency evidence, not authority. Target authority must come from the selected preflight/runtime boundary.
- Lines 155–194 bound canonical input, obtain lengths before native text transfer, require text result OIDs/formats and actual received lengths, then perform semantic/canonical/prediction comparisons. Both queries use the same immutable synthetic parameter, so no mutable-row race is being claimed solved.
- Lines 197–243 independently construct E and the scoped state families. E reserves chunks=N; ordinary complete family states use ceil(N/5000). The omission control separately exercises chunks=N with a 17-digit count.
- Lines 246–355 define the exact domain, family, full-size, rejection and omission tests.

All five explicit execute call sites use fixed SELECT SQL with bound synthetic parameters where applicable and `prepare=False`. There is no new-body DDL/DML, application query, existing-journal read, loader registration, provider access or fixture privilege path. The existing runner still has its normal setup, origin import, shutdown and corpus restoration responsibilities; the new body's SELECT-only property should not be confused with bypassing those controls.

The resource arithmetic is internally consistent:

| Item | Count |
| --- | ---: |
| Domain / family / boundary / rejection / omission cases | 2 / 19 / 6 / 3 / 1 |
| Cases / ordinary setup-call-teardown phases | 31 / 93 |
| Connections / connection-identity SELECTs | 31 / 31 |
| Family observations | 2×7 + 17×9 = 167 |
| Boundary observations | 6×2 = 12 |
| Omission observations | 5 |
| Total state observations | 184 |
| Explicit SELECTs | 31 + 184×2 + 2 + 3 = 404 |
| JSONL records | 31 + 184 + 2 + 3 + 1 = 221 |

The exact 31 ordered external-file node IDs match `EXPECTED_CASES.txt`; they have the selected empty file prefix. A future audit must compare complete IDs plus the selected file identity, not strip arbitrary prefixes. The static enumeration is not pytest collection evidence.

Each JSONL record is limited to 8 KiB. Successful planned output has a theoretical per-record-bound ceiling of 1,810,432 bytes, before any unrelated runner logs. State records deliberately say `OBSERVED_BEFORE_ASSERTIONS`; recording a length/hash is not a successful comparator result. The corresponding passed call phase and complete exact ledger are required. A failed connection or earlier assertion can leave fewer records; that is an incomplete/failing attempt, not a new reduced success criterion.

Connections are serial and close through their context managers; the helper closes a connection if identity checks fail. The test does not print or persist the runtime URL. The copied redaction hook retains the established connection-error suppression. Rejection tests preserve actual SQLSTATEs and require class 22 instead of asserting an unobserved exact subclass.

## Independent boundary arithmetic

A reviewer-owned small literal state independently confirms the accepted 391-byte compact one-model UUID E. Replacing schema={} by schema={"fill":""} makes it 400 compact bytes. Direct container member counts give 22 colon/comma spaces and therefore a 422-byte candidate native base. No packet/reference sizing function was executed to obtain those values.

Let L=16,777,216. The selected six E observations are:

| Basis and margin | Expected compact E | Expected native E | Compact/native gates |
| --- | ---: | ---: | --- |
| canonical −1 | L−1 | L+21 | inside / outside |
| canonical 0 | L | L+22 | inside / outside |
| canonical +1 | L+1 | L+23 | outside / outside |
| native −1 | L−23 | L−1 | inside / inside |
| native 0 | L−22 | L | inside / inside |
| native +1 | L−21 | L+1 | inside / outside |

Each corresponding ABORTED observation must be exactly three bytes smaller in both representations. In the native +1 case the particular abort can fit even though E does not; this must not be reclassified as successful admission. These are expected arithmetic values, not native results.

The maximum parameter is L+1; the maximum fetch allowance is L+32; the largest expected fetch is L+23. Those diagnostic margins do not enlarge the proposed state ceiling. Twelve full-size text transfers are roughly 192 MiB aggregate, plus roughly 384 MiB aggregate parameter input across the two queries. These are logical payload estimates. The 1 GiB client RSS allowance is planning guidance, not an enforced or measured bound. Keep the existing 600-second test timeout and account for closure time outside it; do not reproduce the original unrelated 30-second unit CPU cap. Resource accounting should name the measured process/tree and include descendants or explicitly distinguish wrapper-only from test-process measurements.

## Exact blockers

1. `COMMAND_ARGV.json` has null `entry_argv`, `source_review`, `packet_seal_sha256` and `root_selection_sha256`. Its argv is an inert proposal, not a gate or selected command.
2. `PREDECESSOR_BINDING.json` has null terminal review path/digest and false authority, semantic-closure, exclusive-selection and no-intervening-stage fields. It historically names the intervening JSON transport packet. Root reports a newer cost9 stage is now active; the latest independently closed stage at selection time, including that stage if it intervenes, must replace the stale pending premise in a separate binding. This reviewer did not inspect or infer any current runtime outcome.
3. There is no native-packet outer admission/archive/closure entry, no selected current runtime-binding digest and no selected closure-aware outer watchdog/resource receipt. The cold launcher alone does not supply these packet-specific controls.
4. The transport `run-probe.sh` / `admit_packet.py` are not reusable native entries unchanged: they hardcode the transport namespace, selected test, 61-case/183-phase grid, exact packet members/archive count and an older predecessor. Their self-admission is not parameterized for this packet. Do not call them against this packet or copy their old successful predecessor.

The original eight packet files are complete and sealed for their stated source-only status. The absence of launcher/admission is intentional incompleteness of execution preparation, not a broken source seal.

## Smallest safe continuation

No implementation or v3 release work is necessary for this native question. The minimal continuation is an additive, independently source-reviewed outer selection/admission/closure companion around the already sealed body:

1. Finish the currently selected laboratory stage and obtain its actual independent terminal audit. Preserve unsuccessful outcomes and require verified normal stopped-server, source and corpus closure before selecting a successor. Do not use an older successful stage to hide an intervening failed stage.
2. Record root's current bounded authority, exclusive one-stage selection and no intervening laboratory work. Externally bind this review's exact digest, the native packet seal above, source221 manifest identity `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`, the actual latest terminal-review digest, the unchanged runtime guard/launcher and the selected SA21 runtime-binding identity. Hashes do not supply semantic approval.
3. Keep the current eight files unchanged. A small separate command/selection record can select the already recorded `wrapper_argv_after_separate_admission` and give the companion's concrete entry argv, fresh native audit/evidence paths and resource/watchdog selection. Seal and review the companion separately, so the source-only packet is not retroactively rewritten as admitted and review/seal hashes do not become self-referential.
4. Before any live referent/status action, the companion must verify its externally anchored selection, source review, exact packet files and relevant inert guard/source maps. Reject symlinked/extra/missing source inputs and pre-existing output destinations. Archive the selected native packet, companion/selection and exact source221 tree through the already accepted archival approach. Derive the native inventory; do not reuse the transport's 233-file constant or broaden reads during source preparation.
5. Under the selected fixed environment and existing exclusive runner controls, run the unchanged runtime guard's `before` gate with its exact selected SA21 binding; require the normal stopped-server boundary; invoke the unchanged cold launcher exactly once with the recorded native argv. Preserve fresh dual-role preflight, origin checks, cold/no-bytecode behavior and normal corpus protections. No direct pytest, alternative loader, role, credential, install, cache-warming or multi-cell path is needed.
6. On success, assertion failure, driver rejection or resource interruption, preserve the attempt. Ensure normal stop and source/runtime/corpus after-gates are attempted and independently inspected. Select a watchdog that permits normal stop/closure rather than killing the entire closure path. Do not retry, repair source or raise a budget inside an incomplete attempt.
7. Independently audit exact 31 IDs/93 ordinary phases, all 221 expected ledger identities and relevant native values, all three omission detections, both gate classifications at each boundary, argument/source/archive identity, resource outcome and terminal closure. Acceptance requires every planned case and all postconditions. A zero entry exit alone is not acceptance.

This path needs a small packet-specific adapter and actual latest-boundary selection, not a duplicate runtime guard or another broad infrastructure stack. No additional user question is needed to resolve facts root can establish from the existing authorized stage and its terminal review; any genuinely missing action authority remains root's responsibility.

## Preserved prior result

`reviewer-notes/abort-envelope-unit-terminal-independent-20261015/AUDIT.md` remains byte-identical at `2e31beb778ec9b3ebd0b2c78c57f8cce53bbbe9b848a107301edd61cfdd39e1e`: nineteen individually successful pure-reference methods across three preserved attempts, with the original invocation still incomplete/SIGKILL. Nothing in this review overwrites that qualified result, executes the reference again, or changes `experiments/aborted-successor-envelope-v1-20261015`.

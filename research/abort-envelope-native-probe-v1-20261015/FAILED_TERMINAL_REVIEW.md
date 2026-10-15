# Independent terminal review: native abort-envelope representation attempt

Verdict: **CLOSED_FAILURE_NATIVE_REPRESENTATION_UNPROVEN**.

The selected attempt failed in its first UUID-domain case, before any native envelope state observation. Normal shutdown, source/archive closure, installed runtime binding and corpus restoration are independently corroborated. This is an accepted closed failure, not a native representation PASS. There is no authorization to retry, alter the immutable attempt or select another database stage in this review.

## First decisive failure

The exact first selected identity is `::test_native_cursor_domains[uuid]`. Its setup passed, call failed and teardown passed. The failure appears consistently in the safe wrapper/tests output and JUnit:

`psycopg.errors.AmbiguousColumn: ORDER BY "v" is ambiguous`

The exception occurs at `test_native_envelope.py:264`, the domain query's `cur.execute`. The UUID query at lines 252–253 selects both `v` and `v::pg_catalog.text` and uses unqualified `ORDER BY v`. The int64 branch at lines 258–260 has the same ambiguous shape, but that branch was not executed. Source inspection identifies the query's output-name ambiguity; it is not an envelope-size, native-text-length, round-trip, numeric-width or admission failure. The numerical SQLSTATE is not emitted in the safe evidence, so none is reported as observed.

This actual rejection supersedes the earlier native source review's narrower finding that no substantive test-body defect had been found. It does not invalidate the accepted outer entry's failure closure. The original native source is preserved at SHA-256 `20d2727f58101a6f5378e3b23714d4cf87ff73f98b519386c7e7a5dc11c373b8`.

A later, separately authorized source correction would need an unambiguous native sort expression in both domain branches, such as qualification of the input column. This review makes no edit, does not validate such a correction by execution, and does not permit dropping the domain tests or reducing the 31-case grid. Any future selection must preserve this closed failure as its actual predecessor rather than reverting to the older cost9 success.

## Exact partial accounting

The independently reconstructed full selection still contains exactly 31 ordered identities: two domain, nineteen family, six full-size boundary, three rejection and one omission case. It agrees exactly with `EXPECTED_CASES.txt`; identities were not prefix-stripped. The selected external source's original, outer archive, runner archive and before/after hashes agree.

The actual records are:

| Item | Required for a complete attempt | Observed |
| --- | ---: | ---: |
| Started cases | 31 | 1 |
| Passed calls | 31 | 0 |
| Failed calls | 0 | 1 |
| Ordinary setup/call/teardown reports | 93 | 3: two passed, one failed |
| Connection records | 31 | 1 |
| State observations | 184 | 0 |
| Domain records | 2 | 0 |
| Class-22 rejection records | 3 | 0 |
| Omission records | 1 | 0 |
| Total JSONL records | 221 | 1 |

The single 223-byte, newline-terminated ledger record has exactly the expected connection schema and joins the failed `domain_uuid` call. It records PostgreSQL version 160015, client/server UTF8, positive integer backend PID and a valid 64-character target digest. The digest is consistency evidence, not authority. No database or role name was recovered from it.

JUnit independently reports exactly one test, one failure, zero errors and zero skipped cases, with the same exact empty-classname test identity. The other thirty cases were unexecuted, not successful or skipped. Progress has exactly one start followed by setup-pass/call-fail/teardown-pass in increasing monotonic order.

The reviewer independently enumerated all 184 expected state identities: 167 family, twelve full-size and five omission observations. Every one is absent. There are no native or canonical lengths/hashes to join, no successful semantic/canonical round trip, no actual domain ordering/value/width result, no class-22 rejection result and no reservation-omission detection. All six real 16 MiB minus/equal/plus-one boundary cases and both E/ABORTED observations per case are unexecuted. The size hypothesis is therefore unproved, not experimentally disproved by this attempt.

The planned 404 SELECT count remains source arithmetic. This attempt did not run that workload, and no runtime SQL trace was asserted. `accounting.json` is correctly absent: the entry rejected the failed wrapper after completing its closure gates and before its complete-success accounting path.

## Selection, source and exact archive

- Native packet seal: `0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5`.
- Entry companion seal: `9f7b4230ef29b37cbc98b69e76afa799906f42f66cac8d7472f67db04dc1dec1`.
- Root selection: `a2100b64d1da003488339705ee9074948ef45fc38961b1b934d3f5cc98b72c26`.
- Source221 manifest: `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`.
- SA21 binding: `669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54`.

All seven native members and five companion members match their externally anchored seals. Exact current native/companion namespaces match the expected sealed files plus the companion selection and run directory. The recorded `/bin/bash` bootstrap invocation uses the exact selected digests, cwd and fixed four-key non-secret environment. The selected cold wrapper argv, SA21 installed interpreter, candidate, complete external test file, confcutdir and stop-on-first-failure arguments match the actual runner pytest arguments, including only the documented progress/JUnit/faulthandler additions.

The three selected reviews match their exact paths and digests: native source `17d39a9c6bb9b3b4ca1c913d64ddfe6e3f9a5043a4461d88e139498309922159`, entry source `5458d39b16407874edc164a6b66de6f931750b4c8ef644fd2e06b23eb3af01c5`, and preceding cost9 terminal `cc1b8b36a1ba644722f9e40ca647353accac5375ed829293c0253063a5400f87`. Root's semantic acceptance, current bounded authority, exclusive selection and no-intervening-stage declarations are explicitly recorded. The selected predecessor is the actual cost9 packet with `CLOSED_PASS`, not the stale historical placeholder in the immutable native packet. This audit verifies those records; hashes themselves do not create authority.

The reviewer independently derives the archive inventory as 221 source files + eight native files + seven companion/selection files + ten pinned inert inputs + three reviews = **249 files, 6,584,093 bytes**. Both exact file and directory sets match. Every original and archived payload matches its expected digest; the archive receipt's complete map, counts, byte sum and three anchors agree. The reviewed sources and selected native packet are unchanged.

The wrapper's separate 160-file source snapshot is stable and joins source221. All 160 archived source payloads match their map. Its 159-entry runner source map correctly comprises the 158 Python files plus the unchanged preflight script; the separate snapshot also includes pyproject.toml and uv.lock. The single external-test archive matches the exact selected native source and its before/after record.

## Runtime identity and normal closure

Both unchanged runtime guard receipts have status `VERIFIED`, selected stage SA21 and the exact bound digest; exit codes are zero. Their maps are identical except for mode. Independently merging the four binding manifest maps produces the exact **3,025 targets** in both receipts, without conflicting overlaps. The exact 27-member guard packet map also matches.

Each guard reports source221, 26 corpus files, 2,402 nonproduct installed files and two opaque installer-metadata paths. Its 86 product-module count is **43 main modules in each of SA21 and SA20**, not 86 selected test modules. The reviewer independently derives those 43 source module identities and joins both installed-cell maps to their source bytes. The safe package-origin log confirms that the actual selected process used SA21's installed package and byte-matched 43 modules.

The sealed, unchanged guard source enforces exact cold installed namespaces before reading its admitted payloads, disallows bytecode/cache members, and treats installer cache metadata opaquely. The cold launcher and its `-B` invocation remain pinned. This audit joins those accepted controls and emitted before/after records; it does not import product/driver modules or independently reread installed/cache payloads.

Normal terminal evidence is consistent:

- Exactly one wrapper start reports `postgres-start exit 0`; readiness and package-origin exit 0 precede `tests exit 1`.
- The runner receipt confirms fresh dual-role preflight and the exact failed test outcome.
- `postgres-stop exit 0` appears once; the independent safe stop log matches its successful shutdown text in the wrapper log.
- Both entry and root pre-/post-status captures return 3 with `pg_ctl: no server running`.
- Closure records wrapper exit 1, post-status 3, source-after 0 and runtime-after 0.
- Root entry exit is 1 with `RUN_OR_CLOSURE_FAILED`, preserving the test failure rather than converting it to success.

The **same exact 26-file corpus hash map** joins root before, root after, runner prior manifest and both guard receipts, and agrees with the bound runtime target map. The isolation receipt reports restoration true, no errors, no generated candidate corpus and no deletion during this run; its candidate-corpus directory is empty. Corpus payloads were not opened by this reviewer. These independent evidence joins accept ordinary stopped-server/source/runtime/corpus closure despite the failed diagnostic.

## Measured resources and limitations

The wait4 receipt reports wrapper plus descendants reaped by that wrapper:

- Wall: 1.7737592229968868 seconds
- User CPU: 1.452378 seconds
- System CPU: 0.102396 seconds
- Total CPU: 1.554774 seconds
- Linux peak RSS: 62,932 KiB, approximately 61.457 MiB
- Child/wrapper exit: 1

These measurements describe this early failed wrapper. They are not evidence that the complete full-size workload fits any memory/time allowance. They exclude a whole-cluster resource guarantee and do not measure the entry's archive/guard work as part of wrapper wall time. The inherited tests/control timeouts remain 600/90 seconds. No new parent deadline or enforced CPU/address-space/RSS cap is claimed.

## Method, retained evidence and stopping point

The reviewer began run-evidence inspection only after root reported session 59647 terminal. All source/evidence payload reads were finite ordinary-file reads preceded by type, ancestor and size metadata admission. The complete archive paths were admitted before the hash loop. The reviewer-owned auditor performs JSON/XML parsing, source/evidence hashing and arithmetic only; it does not import or execute any reviewed target source. The final auditor records 3,673 successful consistency checks. Two initial reviewer comparison assumptions (argv slice offset and runner-versus-snapshot source-map membership) were corrected locally before the final audit; no laboratory process was rerun.

No database/status command, target test, target import, retry, Git operation, network action, environment/credential inspection, corpus payload inspection, private/cache payload read or raw tests/readiness/package-origin/PostgreSQL start-stop JSON-body read was performed. Safe redacted `.log` artifacts supplied phase outcomes. Existing laboratory sources and evidence were not modified. Only this fresh reviewer directory was written.

Supporting reviewer-owned artifacts are `AUDIT_RESULT.json`, `READ_MANIFEST.json`, `METADATA_MANIFEST.json`, `CHECKS.json` and `audit.py`. The result contains all exact expected state identities and the thirty unexecuted case identities.

The failed original attempt is preserved and closed. No retry or repair has occurred. All seven broad product gates remain **UNKNOWN**. Physical journal/PK/ACL safety, actual expansion admission, transactional ordering, authenticated ancestry, historical abort, durable recovery and product/v3 release remain unproved. Further work requires a new, separately reviewed and authorized selection rooted in this honest closed-failure boundary.

# AGENT6: frozen CLI / developer-experience integration review

Date: 2026-10-16 UTC.

Verdict: ONE_CONCRETE_EXTERNAL_DOCUMENTATION_GAP; no incorrect existing install-command syntax or frozen entrypoint/package mismatch found. No product correction is requested.

## Actionable finding: new evaluators are not told how to run or interpret static doctor

Priority: documentation usability, before directing a new evaluator through the current install handoff.

The current five-file handoff discusses accepted doctor regression evidence but supplies no doctor command or exit-status handling. INSTALL-CURRENT.md:31–37 provides the installer template only; INDEX.md:11–14 links installation/evidence/register/operator notes. The immutable v4 QUICKSTART.md:11–19 shows the Python setup API, not a CLI invocation or shell result contract. Neither the current handoff nor these public install/quickstart instructions exposes the static doctor's deliberately nonzero normal exit.

Actual frozen source is unambiguous:

- src/cryptalis/cli.py:160–166 accepts `doctor PATH [--json]`, with a required filesystem path and no setup/engine/phase options.
- src/cryptalis/cli.py:490–503 reads that file, writes the report to stdout, then returns 2 for a rejected declaration and otherwise 3. Valid declaration grammar does not yield exit 0.
- src/cryptalis/cli.py:75–83 and 382–390 send argument failures as errors on stderr. The file I/O mapping at 170–199 gives invalid/missing/inaccessible inputs exit 2 and unavailable I/O exit 4. Output failures at 294–313 use exit 4.
- src/cryptalis/doctor.py:24–28 sets complete/ready false; 41–49 distinguishes rejected declaration and grammar-only CHECKED.
- docs/doctor.md:7–11 contains the correct static command and exit semantics, but it is source documentation, absent from the 48-file accepted wheel payload set, and not linked by the current handoff.

Concrete evaluator failure: an unguarded static doctor command in a `set -e` shell or an `&&` chain stops on the normal valid-report exit 3. A stderr-only rejection collector also misses readable rejected-declaration reports, because those are stdout + exit 2. These follow directly from control flow; this review does not claim to have executed either scenario.

## Minimal root-owned correction

Add the supplied PROPOSED_EXTERNAL_DOC_INSERTION.md section to a separately reviewed current external installation/doctor supplement. It uses the exact supported `python -m cryptalis doctor PATH --json` spelling, checks explicit 2/3/4 outcomes, and preserves stdout and stderr separately. It points at the existing immutable manifest.example.json and says the operator must supply its local path; the wheel contains neither that example nor a default protection.json. The shell conditional avoids `set -e` swallowing expected exit 3 without masking all failures.

Do not change the frozen source, historical embedded README or immutable v4 guide in place. Only root should decide external promotion/publication. This is a proposed documentation insertion, not an executed smoke or permission request.

## Entry-point and packaging checks that passed

pyproject.toml:7–12 matches the public guide's Python/dependency declarations. pyproject.toml:15–16 and the accepted wheel's cryptalis-0.1.0.dist-info/entry_points.txt:1–2 both bind `cryptalis = cryptalis.cli:main`. src/cryptalis/__main__.py:1–4 forwards the module invocation to main and raises SystemExit with its result. The module invocation is `python -m cryptalis`; do not infer `python -m cryptalis.cli` from the console entrypoint string, since cli.py itself defines functions without a module main guard.

The three pertinent runtime module bodies (__main__, cli and doctor) match the accepted wheel bytes and full-source receipt. The CLI's current body remains SHA256 060cb66057f66c6d22c2b455bfba918545a3fabc251e72a30ab8fbfe61b0f409. The existing offline hash-required pip command has correct syntax, mandatory operator substitution paths and an explicit incomplete dependency-input boundary; no concrete command mismatch was found there. Historical artifact identity differences are explicitly superseded by the current handoff and are not reported as new defects.

## Evidence and limits

Finite admitted inputs: six frozen restored source files, three corresponding accepted wheel modules, entry_points.txt, finite package restore metadata, current INDEX.md and INSTALL-CURRENT.md, and nine independently fetched immutable v4 guide/example files. Remote UTF-8 bodies recompute their Git blob identities. Source hashes match the accepted source receipt. STATIC_CHECKS.json records exact input hashes; numbered guide copies preserve precise citation lines.

No accepted doctor7 rerun, product import/execution, build, restore, install, database, live installed environment, dependency cache, credential access or Git write occurred. The only executed program was the reviewer-owned static metadata/hash checker. All changes are confined to this isolated reviewer directory. This review neither requalifies APIs at runtime nor promotes its draft insertion.

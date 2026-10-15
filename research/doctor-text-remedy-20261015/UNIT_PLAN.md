# Unexecuted doctor text-remedy regression plan

Status: plan only. No tests, project imports, collection, compilation or execution
have run for this derivative. No RED or GREEN result is claimed.

## Test boundary and setup

Use one standalone new test module, proposed name
`tests/test_doctor_text_remedy.py`, in a separately materialized complete candidate.
Do not import the database fixture module `test_protection_compiler` merely to
obtain its declaration helper. Use small synthetic JSON byte strings, disposable
temporary regular files and the existing public `cryptalis.cli.main` entrypoint.
Run only the coordinator-selected exact node list through its reviewed route;
this document does not authorize a direct test run or a PostgreSQL session.

The minimal valid declaration should use the existing schema/profile, three
distinct nonzero canonical UUID strings, one synthetic model, single-tenant
context, one protected field, and empty query/leakage arrays. It is test data,
not an application admission claim. Keep its bytes identical in RED/GREEN runs.

## Decisive RED/GREEN property

1. `test_plain_doctor_rejection_shows_existing_safe_remedy`
   - Parameterize two independent rejection causes: malformed JSON containing a
     distinctive private marker; valid JSON with an unsupported schema string
     containing a different private marker.
   - Put a third marker in the disposable filename.
   - Invoke `main(["doctor", path])` through the public CLI function.
   - Require exit 2, empty stderr, the existing rejection code and unchanged
     incomplete/no-deployment banner.
   - Require exactly one indented line:
     `  remedy: Supply a valid bounded cryptalis.protection/v1 declaration.`
   - Require that all content/path markers are absent from stdout and stderr.
   - Require that input bytes are unchanged.
   - On the retained baseline this property is expected to fail only because
     the remedy line is absent. Preserve actual output before judging the RED.

## Compatibility and boundary controls

2. `test_json_doctor_rejection_remains_exact`
   - Use the same malformed declaration on baseline and derivative.
   - Require exit 2 and empty stderr; compare complete stdout bytes exactly.
   - Independently parse stdout and require the preexisting remedy, rejected
     manifest status, ready=false, complete=false and other checks NOT_INSPECTED.
   - Require no input/path markers. Do not add JSON fields to make text pass.

3. `test_valid_plain_doctor_output_remains_exact`
   - Feed the fixed valid declaration to baseline and derivative.
   - Require byte-identical stdout, exit 3 and empty stderr.
   - Require the existing incomplete/no-deployment banner, CHECKED manifest,
     all other checks NOT_INSPECTED and explicit-host dynamic-inspection notice.
   - Require no remedy line, unchanged input bytes and no success/ready claim.

4. `test_static_doctor_does_not_enter_dynamic_paths`
   - For valid and invalid fixtures, install local fail-fast sentinels on the
     compiler, active-report, setup and ciphertext-audit paths after loading the
     selected modules in the approved test environment.
   - Require each static CLI call to finish with its expected 3 or 2 exit and
     zero sentinel calls. Use supported monkeypatch points already available;
     do not acquire credentials or connect to any service to prove no access.
   - These are local route controls, not proof of provider custody or complete
     absence of host side effects.

5. `test_plain_doctor_remedy_output_failure_is_operational`
   - Supply the malformed fixture and replace stdout with a deterministic local
     writer that raises OSError(EIO) on delivery; leave stderr collectable.
   - Require exit 4 and the existing sanitized CLI.OutputUnavailable diagnostic,
     not exit 2, success, or a raw traceback; no private input/path marker.
   - Repeat with a short write and flush failure if the coordinator selects those
     existing output-boundary cases. No filesystem device or database is needed.

## Baseline preservation and independent mutation

- Preserve original bytes, command, node IDs and actual output for the baseline
  RED and proposed GREEN separately. Expectation is not evidence.
- Remove only the added remedy-rendering line from a separate derivative copy.
  The decisive text property must fail; restore the exact pinned line and rerun
  that selected property. Do not mutate original or selected candidate files.
- Run the existing CLI invalid-argument/privacy/output tests and existing static
  doctor tests under the coordinator's approved finite selection. Do not weaken
  assertions, alter expected statuses, add skips, or relabel historical failures.
- Independent review should verify the one-line runtime delta and confirm the
  unchanged doctor/parser/JSON/output-handler pins before interpreting results.

## Integration and stopping condition

If the finite static controls pass, report only that the proposed text remedy
is verified within those controls. The coordinator decides whether to include
it before freeze. An installed-artifact check and relevant affected suites are
still needed if a new package is selected. Existing selected wheel evidence does
not automatically qualify a derivative.

Stop and report any unexpected input, output, exit-code, redaction, import or
side-effect change. Provider/cluster testing and full doctor feature completion
are outside this plan. All production gates remain UNKNOWN.

# Preview doctor text-remedy slice

Status: isolated proposed derivative, static inspection only. No tests, imports,
project execution, build, integration, promotion or publication performed.

## Finding

The current plain-text `cryptalis doctor PATH` report drops the existing safe
remedy for an invalid protection declaration. The report shows
`manifest: REJECTED (invalid_protection_declaration)` but does not tell the caller
which declaration format to supply. The existing API and JSON CLI report already
contain `Supply a valid bounded cryptalis.protection/v1 declaration.`

This is an actionability gap, established from current source rather than an
executed reproduction. It is especially relevant because the structural
`manifest inspect` command and the `doctor` command accept different documents.
The public architecture explicitly separates field-intent declarations from
structural research-header schemas.

## Exact proposal

Add one conditional line to the plain-text check renderer in `cli.py`. If a check
already has a `remedy`, print it on an indented `remedy:` line immediately after
that check. The static doctor path supplies only the library's existing fixed
remedy; it does not receive arbitrary application callbacks or provider data.

The proposal changes human-readable text only. JSON report keys/values, error
envelopes, command names/options, declaration admission, bounded file reads,
exit codes, output-failure handling and all diagnostic implementations are
unchanged. Valid input still returns exit 3 and cannot qualify a deployment.
Invalid declaration content still returns exit 2. No public operation, provider
configuration, cluster access, key access or automatic repair is added.

The additive text is intentional. Consumers requiring a structured output
contract should continue to use the unchanged `--json` path. No guarantee of
byte-identical plain-text rejection output is made for this proposed change.

## Source and contract anchors

Selected source: `candidate-cluster-retained-integrated-v2-20261015` under the
parent `cryptalis-executable` directory. The root checklist records this as the
bounded Integrated221 candidate. The full 221-file manifest was not re-audited
by this inspection.

- Root `CRYPTALIS_BUILD_CHECKLIST.md`, OBJ-DX-01/02/05 rows: precise startup
  feedback, read-only doctor with explicit limits, and usable diagnostic errors.
- Selected `docs/security.md:307-325`: concrete safe remedies; no raw private
  values in errors; exits 2/3/4 preserve denied/incomplete/operational outcomes.
- Selected `ENGINEERING_PLAYBOOK.md:31-52`: safe causes and remedies, observable
  output failures and no silent security-critical failure.
- Selected `docs/architecture/README.md:164-177`: declaration/header distinction.
- Selected `docs/doctor.md:5-13`: bounded declaration-only static CLI and exits.
- Selected `src/cryptalis/doctor.py:39-47`: parser rejection produces the fixed
  remedy before any dynamic diagnostic path.
- Selected `src/cryptalis/cli.py:490-503`: text renderer omits remedies while JSON
  serializes the complete report; existing safe output writer is reused.
- Selected `tests/test_doctor.py:62-79`: static CLI tests exercise JSON only.

## Artifacts

- `baseline/src/cryptalis/cli.py`: exact retained original file for this proposal.
- `overlay/src/cryptalis/cli.py`: derivative with one additional rendering line.
- `doctor-text-remedy.patch`: unified patch for that exact file.
- `UNIT_PLAN.md`: unexecuted regression, compatibility and mutation plan.
- `SOURCE_PINS.sha256`: selected source/contract inputs inspected and pinned.
- `ARTIFACT_PINS.sha256`: this proposal's retained files, excluding this pin list.

This is a partial overlay, not a complete candidate tree and not an import target.
Original candidate files, current selection, packages, root checklist, Git,
databases, running cells, credentials, caches and corpus were not modified.

## Decision boundary

The existing contract is sufficient for this rendering-only correction. A full
operations CLI, stronger declaration-specific causes, provider diagnostics,
automatic discovery, or new dynamic CLI modes need separate design/admission
and evidence. They are deliberately outside this slice. All 34 objectives remain
active; preview remains the first delivery milestone. This proposal closes no
doctor objective or production qualification gate.

Before any execution or promotion, the coordinator must review the exact patch,
materialize a separate complete candidate from the selected inventory, and choose
the authorized finite test route. No execution command was issued here.

# Manifest-first offline setup, 2026-10-13

Status: IMPLEMENTED in an isolated S17-derived candidate; pure and native
model-object evidence only. Installation, PostgreSQL regression, application
replay and promotion remain coordinator work. All seven independent gates are
UNKNOWN. The separate offline KMS experiment is unchanged and supplies no live
provider permission.

## Adoption problem and bounded change

The default doctor API with a registry alone returns
`incomplete_dynamic_inputs`. Static declaration parsing cannot determine whether
a misspelled selector names an existing mapped attribute. Full native admission
requires an engine, database inspection and writer inventory. The existing
attachment also needs independently trusted lock/key/deployment/tenant inputs.

The new explicit `phase="setup"` resolves declarations against the existing
registry and inspects only local engine settings. Its template refers to those
host objects rather than serializing configuration or copying a schema. It uses
the current public `attach` signature and retains all runtime checks. This is
diagnostic scaffolding, not automatic migration or permission discovery.
The public API adds a phase and one report check, not another entry point.

The fixed template never includes user model names, URLs, defaults, credentials,
key bytes or deployment contents. Its seven placeholders must be bound by the
host. It does not synthesize the private profile flags needed by the recorded
FastAPI experiment. CHECKED is scoped to selector/local-setting inspection;
ready/complete remain false. The existing compiler still decides schema
admission, including types, defaults, constraints, exact identities and database
state.

## Comparison and design basis

CipherStash Stack revision `576b8986e00ebf8f4e2f39908ea0780f0359eaeb`
documents why its init scaffold stopped producing a parallel inferred schema:
the existing application's schema is authoritative and the scaffold points back
to it. This source observation supports reference-based scaffolding here; it
does not establish API parity or Cryptalis runtime compatibility. The archived
MIT license was inspected. No vendor code was copied or dependency introduced.
[Pinned init source](https://github.com/cipherstash/stack/blob/576b8986e00ebf8f4e2f39908ea0780f0359eaeb/languages/typescript/packages/cli/src/commands/init/utils.ts#L355-L375).

SQLAlchemy exposes `Mapper.iterate_properties` as a public inspection API.
Local source inspection and omission controls establish the relevant behavior
on the tested versions: unlike `attrs`, this iteration does not configure an
unresolved relationship. This is an executable version-specific observation,
not a claim that every future mapper implementation is inert.
[Official mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.iterate_properties).

## Evidence and measurable benefit

- Initial public-path RED: eight tests, 21 failures before setup implementation.
- Expanded final tests: 14 PASS in each cell, Python 3.12.14 with SQLAlchemy
  2.0.51 and 2.1.3, psycopg 3.3.6 and cryptography 50.0.2. Direct stdlib unittest
  invocation; no pytest wrapper bypass and no database run.
- Nine selector/context defect inputs are diagnosed without a connection:
  unknown model, typo, physical-name/attribute-name mismatch, synonym,
  computed expression, hybrid, relationship, missing tenant attribute, and
  protected primary key. Three unsafe logging inputs are separately refused.
- Default/type-repr/hybrid/unresolved-relationship and connection sentinels stay
  untouched. Custom dialect/name/truth hooks, invalid parser inputs and key
  opt-in refusal are controlled. Bound exhaustion gives no template.
- Sync and async generated text execute with replacement attachment/context
  objects to prove exact identity forwarding of all seven host inputs. This is
  template wiring evidence, not successful real attachment or database access.
- Four controls per dependency cell: remove logging guard (three failures),
  remove context protection (one failure), substitute configuring mapper access
  (20 errors), re-enable the model-name metaclass hook (one failure). Exact
  source restoration returns all 14 tests to PASS.
- Pinned FastAPI `app.models` oracle: upstream
  `7257e606cb94eada1dca40173e2b7f99dd549bc6`, file SHA256
  `4696396c84832a50ca9d60337c2b6ba24e961f2ee5b5e660d8081fb929ebf459`.
  SQLModel 0.0.47 / SQLAlchemy 2.0.51 on the existing Python 3.14.8 environment.
  The actual User/Item registry supplies two native mappers; a synthetic
  selector-only declaration protects User.full_name and User.email. One valid
  cell and seven defect cells pass. No settings or database module is imported.
  Source hashes, mapper configuration, tables, columns, type objects and default
  objects are unchanged; connection attempts and schema copies are zero.

Measured improvement: setup catches these mapping/configuration mistakes before
database or key access and produces one reference-based template with zero
duplicate model/schema definitions. No elapsed developer-time saving or runtime
integration-line reduction was measured. S17's complete FastAPI replay remains
58 tests in each of four native/protected/package-free cells, with 13 external
bootstrap lines plus four fixture lines and zero application-source changes.
The model-only oracle neither replaces nor extends that replay.

Initial expanded hook tests exposed two unsafe local inspections. The dialect
name access was replaced by exact ordinary dialect classification; model-name
access now calls the built-in type descriptor directly. Test-fixture hook
activation was then confined to inspection (native object construction and
disposal legitimately use those hooks). Failed fixture runs are retained.
A custom truth-value control exposed a setup-input guard evaluation and was
corrected with strict static type/length checks. No failure log was discarded.

## Reproduction and artifacts

Run `tests/test_doctor_setup.py` directly with each existing dependency-cell
Python and `PYTHONPATH=src`, with bytecode generation disabled. Run
`experiments/manifest_setup_fastapi_models.py <pinned-backend-directory>` only
with the existing SQLModel-qualified environment. The script checks the model
source hash before importing `app.models`; it does not invoke the app harness.

`evidence/manifest-setup/` retains RED/GREEN logs, the actual-model receipt,
four mutation receipts and their exact-restoration hashes. `frozen-files.json`
lists reviewable changed/new files and hashes; `manifest-setup.patch` contains
the isolated code/test/documentation change. The baseline is the coordinator's
195-file S17 manifest. Default and active doctor paths still require their
existing installed/PostgreSQL regression before promotion. No Git, database,
credential, SDK, grant or shared-tree action was performed for this slice.

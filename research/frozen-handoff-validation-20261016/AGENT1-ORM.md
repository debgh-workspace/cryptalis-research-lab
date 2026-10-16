# Freeze validation: ORM/attach/session integration

Date: 2026-10-16 UTC. Source-only inspection, no execution qualification.

## Result

The preferred published v4 QUICKSTART.md's concrete sync attach/add/commit/
scalar-equality sequence is source-aligned with the exact selected doctor
candidate in the inspected paths. One stale alternate walkthrough needs
explicit external handoff clarification. Async SQLModel wording is already
corrected by the current external handoff and is not a new defect. Leave the frozen sources/guides
unchanged; make no product patch or broad new runtime claim from this review.

Paths below are relative to cryptalis-executable. C denotes
candidate-doctor-remedy-integrated221-v1-20261015; G denotes
preview-docs-v4-source221-20261015; O denotes
experiments/integrated221-installed-sqlmodel-controls-20261015.

The candidate README:19 points to published commit d952c505a4666266019e32f27c77f93edd5151ca,
preview/docs/source221-v4/QUICKSTART.md. This review inspected the retained G
files as the approved local guide copy; it did not independently fetch or
revalidate the remote publication. It does not infer new publication identity.

## F1: stale alternate attach example omits required deployment authority

Evidence:

- C/docs/walkthrough-sqlalchemy.md:13 tells readers to perform the product
  protection transition before attachment.
- Its line23 calls attach(Base.registry, engine, lock=plan.lock_bytes,
  keys=tenant_keys.__getitem__) without deployment.
- C/src/cryptalis/sqlalchemy.py:1199 accepts deployment=None as a signature
  default, but passes it into the owner at1213; validate calls
  check_attachment with that deployment at432–436.
- C/src/cryptalis/migration.py:916–931 checks for a transition journal and
  raises external_pin_required at926 unless deployment is a two-item tuple;
  it then requires the exact plan/lock and planned runtime role. The ACTIVE
  plan/pin/current-state check is at908–913.
- The preferred G/QUICKSTART.md:72–75 correctly supplies deployment=(p,
  active_pin), following confirmed activation at62.

Impact: following the alternate embedded walkthrough after the required
product transition can refuse at attach. The signature's optional default is
not evidence that the tuple is optional for product-managed targets. This is
a concrete stale-document integration mismatch, not a missing API parameter in
the preferred public quickstart or a newly observed runtime failure.

Exact recommended external handoff wording:

“Use preview/docs/source221-v4/QUICKSTART.md as the preferred attach procedure.
The frozen package's docs/walkthrough-sqlalchemy.md contains an older alternate
example that omits deployment authority. After product protection, use
cryptalis.sqlalchemy.attach(mapping, runtime_engine, lock=p.lock_bytes,
keys=tenant_keyrings, deployment=(p, active_pin)), with the exact approved plan
and its current authoritative ACTIVE pin. Await attach for a supported plain
SQLAlchemy AsyncEngine. The tuple does not create or approve deployment
authority; missing or stale authority must remain a refusal.”

## Known corrected scope: optional async SQLModel is not default attach support

Evidence:

- G/CAPABILITIES.md:13 labels optional SQLModel “including public async hook”
  and references separate38-case evidence.
- C/src/cryptalis/_sqlmodel_support.py:11 sets
  _experimental_async_sqlmodel=False. Lines59–64 reject a SQLModel async
  mapping unless the private switch is true and its dependency restrictions
  match. Ordinary non-SQLModel async mappings return the standard base at60–61.
- C/src/cryptalis/sqlalchemy.py:1214–1219 turns that rejection into
  UnsupportedSQLModelRuntime. The remedy at83–85 states qualified sync
  SQLModel0.0.47 on SQLAlchemy2.0, with async qualification pending.
- O/installed_sqlmodel_oracle_support.py:95–96 explicitly monkeypatches the
  private switch true. O/test_async_sqlmodel_public_hook.py:54–55 calls this
  enable function; the native-shapes case calls it at100–102 as well.

Current override, checked after root identified it:

- experiments/frozen-preview-handoff-v1-20261016/INDEX.md:26 explicitly says the
  38 cases use an internal laboratory-enabled profile, default async refusal
  remains and no public opt-in is established.
- Its EVIDENCE-LIMITS.md:22 repeats that limit;25 separates historical broad
  suites from the current doctor successor.

This is already corrected external scope, not an open freeze defect or new
action. The wording below is only an optional consolidation restatement.
“Public async hook” describes the tested API surface under a private
experimental opt-in, not default public async-SQLModel admission. A reader
combining that matrix row with QUICKSTART:87's AsyncEngine sentence can infer
an attach route that selected default source refuses. No changes to private
flags, source or evidence are proposed. The38 historical cases remain on their
actual artifact/opt-in boundary; this review neither reruns nor discredits them.

Exact recommended external handoff wording:

“The quickstart's AsyncEngine note applies to supported ordinary SQLAlchemy
mappings. Default async SQLModel attachment is refused in the selected source.
The separate38-case SQLModel result includes a public async-session hook
exercised under an explicitly enabled private experimental flag in its exact
dependency cell. It is not a default public async-SQLModel attach guarantee.
Do not enable private flags as an adoption workaround.”

## Main quickstart: inspected source alignment, not qualification

- G/QUICKSTART:66 (attach before sessions, no checked-out connections) matches
  C/src/cryptalis/sqlalchemy.py:1232–1237 and1245–1250. Attachment validates and
  disposes old pooled connections before activating the mapping.
- G/HOST-INPUTS:46–52 supplies a synchronous tenant resolver; sqlalchemy.py:
  401–415 calls keys(tenant), requires a UUID and correct Keyring policy, and
  binds the policy to the selected deployment. No async-resolver assumption
  is introduced by the AsyncEngine note.
- QUICKSTART:77 uses the returned tenant factory; sqlalchemy.py:1191–1196
  validates its tenant ring and binds the exact engine/session class.
- QUICKSTART:78–80 explicitly assigns UUID identity and tenant before add/
  commit; sqlalchemy.py:782–819 requires stable assigned context and matching
  tenant and seals changed values inside the flush path903–923.
- QUICKSTART:81–84 uses a scalar protected equality predicate. The supplied
  manifest explicitly declares equality/unique. _sqlalchemy_search.py:28–51
  admits the direct declared-column/bound-value shape;54–116 rewrites it and
  adds predicate-local tenant scope at93–108. sqlalchemy.py:1029–1049 prepares
  keys at the query boundary and disables protected statement caching.
- Therefore the absence of an explicit tenant clause in this exact equality
  example is not identified as a bug. It must not be generalized into automatic
  tenancy/authorization for arbitrary queries: the guide expressly disclaims
  that at87, and _ReadText authenticates returned context at151–180.
- Public default operation limits agree in the inspected paths: ordinary ORM
  flush writes and bounded SELECTs are admitted (sqlalchemy.py:686–710), while
  general non-SELECT/non-flush writes refuse. Private update/delete branches
  require explicit internal allowlists (_experimental_public_update.py:79–99;
  _experimental_public_delete.py:87–99), so their existence does not expand
  the public quickstart or negate G/CAPABILITIES:32's default refusal boundary.

## Remaining behavior evidence, without repeating existing suites

The doctor7 cases do not exercise the public sequence's transition-authority
to attach handoff, new-session key resolver, ORM flush/commit, post-commit scalar
equality query or fresh-process policy reload. No new absence of broad-suite
coverage is claimed. The precise open acceptance item is the already-declared
exact public-example composition: G/SMOKE-TEST.md:16–17 requires actual matching
activation/attach, native-versus-attached CRUD/equality and process-restart
behavior; G/QUICKSTART.md:91 and C/README.md:13 explicitly leave it unexecuted.

Action: carry this exact smoke gap and its existing permission gate forward;
do not promote source alignment or doctor7 into successful public adoption.
No new tests, alternate harness, changed assertion or fixture permissions are
requested or supplied here. The F1 walkthrough clarification can be included
in an external freeze handoff without modifying frozen product bytes. Preserve
the existing async SQLModel correction; do not count it as a new defect.

## Inspection boundary

Inspected finite safe source/guide files: selected README and repository
instructions; selected docs/walkthrough-sqlalchemy.md, docs/compatibility.md
and the relevant status excerpt; sqlalchemy.py, migration.py,
_sqlmodel_support.py, _sqlalchemy_search.py, _experimental_public_update.py,
_experimental_public_delete.py and transaction/guard symbol locations; G
QUICKSTART/HOST-INPUTS/CAPABILITIES/SMOKE-TEST/manifest example and related
README/INSTALL references; O's named optional test/helper sources; and the
current external handoff INDEX.md/EVIDENCE-LIMITS.md overrides.

Only reviewer output is written. No source edits, imports, tests, DB/status
commands, Git, live environment/installed/cache/credential/private bodies,
raw phase receipt bodies or production system inspection occurred. Existing
source/evidence qualifications and all seven UNKNOWN production gates remain
unchanged. This is actionable integration inspection, not runtime acceptance.

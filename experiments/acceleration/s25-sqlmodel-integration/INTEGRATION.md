# S25 isolated source integration, pending independent review

Prepared 2026-10-14. No target import, compilation, collection, tests, database,
installation, Git operation or remote action performed. This is not promotion.

## Exact source ancestry

Parent: candidate-s24-test-oracles-r3-20261014; 214-file manifest
6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d.
Candidate: candidate-s25-async-sqlmodel-integration-20261014; 216-file manifest
3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703.

The only changed existing files are src/cryptalis/sqlalchemy.py and
src/cryptalis/_sqlmodel_support.py, copied byte-for-byte from independently
reviewed candidate-s24-async-sqlmodel-public-v2-20261014. The other 212 baseline
files are unchanged. Every original test, conftest, dependency lock,
configuration, documentation file and role preflight remains byte-identical.
No installed distribution or dependency is changed.

Two files are added: tests/test_async_sqlmodel_public_hook.py and
 tests/async_sqlmodel_oracle_support.py. SOURCE_DELTA.patch is complete.
PREPARATION_CHECKS.json records data-only comparisons. Original V2/V3 packets,
sources, failures and evidence remain untouched; no earlier outcome is rewritten.

The accepted prototype scope is 38 unique nodes: core36 plus disjoint DML2.
Targeted3 is a subset of core36, not three additional checks. The final DML2
runtime review accepts only synthetic post-native-result failure behavior,
including the intentionally different native-committable/protected-quarantined
outcomes. This integration has not itself executed any of those nodes.

## Test relocation and optional cell

The full test region starting at assert_sanitized_provider_failure is unchanged,
including all fixtures, decorators, parameter lists, synthetic fault injections,
cleanup assertions and completion receipts. The only test-module changes are its
docstring, explicit optional dependency admission before SQLModel imports, and
renaming the support import to avoid collision with external oracle_support.
No skip, xfail or weakened assertion is added. If selected with SQLModel absent
or versions other than SQLModel0.0.47/SQLAlchemy2.0.51, collection fails explicitly
with UsageError. Merely having SQLModel installed does not admit another cell.

Support derives ROOT from its own relocated path, requires the exact S25 root
and working directory, reads the S25 216-file manifest, and uses unchanged
16-file dependency pins. Its original Python3.14.8/psycopg3.3.6, exact dependency
prefix and module-origin assertions remain. The obsolete external-packet
sys.path insertion is removed: default pytest prepend imports tests from their
own directory, as existing repository test imports already do. No alternate
import mode is added. Module setup AND teardown verify source/dependency bytes.
The conftest is not copied into a second location: existing tests/conftest.py is
byte-identical to V3's conftest and supplies the same preflight/redaction hooks.

All fixture behavior from enable onward is byte-identical, including isolated
schemas, public table permissions, pool cleanup, public UPDATE experiment flag,
independent CF1 observer and native controls. No new fixture or runner policy is
introduced. The product flag stays False by default; tests alone monkeypatch it.
The public async sync_session_class route remains restricted to its exact
reviewed cell. No public API, default, security policy or DML admission expands.

## Exact proposed source-overlay matrix

Run each ROOT_COMMANDS.txt block separately, only after source/command clearance
and coordinator promotion. Require independent terminal audit before the next
block. All use the unchanged corpus wrapper, exclusive lab lock and fresh
unchanged dual-role preflight. No runner substitutions or installs are proposed.

1. SQLModel optional: existing cp84-adoption/sqlmodel-wheel-venv, Python3.14.8,
   SQLModel0.0.47, SQLAlchemy2.0.51, psycopg3.3.6. Select the integrated module,
   exactly38 IDs in SQLMODEL_NODE_IDS.txt. Require38PASS/no skips/errors/xfails,
   twelve shape receipts, nine provider/cancellation completion receipts, four
   genuine post-result reaches and four policy-correct recovery receipts.
2. SA21 full baseline selection: existing release-lab/wheel-venv, select all
   candidate/tests with only the new optional module explicitly ignored.
   Exactly2639 original ordinary IDs: baseline2632PASS/7FAIL/0SKIP and56 passing
   subtests separately. BASELINE_SA21_EXPECTED_OUTCOMES.tsv is the exact oracle.
3. SA20 full baseline selection: existing s20-payload-preparation-sa20-20261014,
   same explicit optional-module exclusion. Exactly2639 original ordinary IDs:
   baseline2586PASS/7FAIL/46SKIP and56 passing subtests separately, including
  18 setup skips and28 call skips. BASELINE_SA20_EXPECTED_OUTCOMES.tsv is exact.

The two full baseline selections retain all original tests, including all seven
historical failures. Their expected exit1 is not success and must not bypass
review. Compare exact IDs, outcomes, failure messages and skip reasons to original
R3 evidence. Unexpected failures, changed old outcomes, missing IDs, extra skips,
source drift or absent cleanup stop progression. Do not repair or waive failures
inside this candidate. The pending version-profile acceptance decision remains
pending and cannot be implemented as a hidden filter.

Optional38 are deliberately not collected in the unsupported main cells; this
is an explicit matrix applicability boundary, not38 passes or38 skips there.
Across the three proposed runs: 5316 ordinary case instances, 2677 distinct test
IDs, with2639 exercised in both main cells and38 only in the optional cell.
If exact baseline outcomes persist and optional38 pass, totals would be
5256PASS/14FAIL/46SKIP, plus112 passing subtest events separately. These are
predictions, NOT results. No full2677-node single SQLModel-environment run is
proposed or claimed; no cross-module SQLModel-cell aggregate claim follows.
No repeat of targeted3/core36/DML2 is added to the counts for integrated38.

## Evidence and stop conditions

Verify INPUTS.sha256 before/after each run. Preserve actual wrapper exit even
when1 is expected; do not use a boolean shell chain that mistakes it for an
all-green result. Review exact JUnit and progress identities, archived source,
setup/teardown origins, terminal runner receipt, normal connection cleanup,
shutdown success and shared corpus restoration before advancing. Retain the
packet's non-Python safe files alongside each result because the unchanged
wrapper archives source Python/config files, not this entire external packet.

INPUTS and PRESERVED_ORIGINALS are integrity manifests, NOT upload allowlists.
They reference historical opaque environment-bearing phase files; preparation
only hashes those bytes. Do not parse, display, copy or publish those files.
No publication is requested or approved here. All production gates, installed
qualification, natural DBAPI-fault equivalence, full adapter acceptance and
corpus reclassification remain UNKNOWN or unchanged.

## Preparation-only integrity correction

The first new INPUTS construction incorrectly expanded both V3 INPUTS and V3's
older preparation-preservation inventory. A data-only sha256sum check returned1
for three historical .pytest_cache entries (two V2 candidate caches and one R3
baseline cache), whose pre-runtime values no longer match after already accepted
runs. INITIAL_STALE_CACHE_CHECK.log retains the failed check. No source failure,
new test run or original-file mutation occurred. The corrected closure inherits
V3's approved runtime INPUTS without expanding its obsolete cache inventory;
that original preservation manifest itself remains pinned via V3 ancestry.
S25's own current PRESERVED_ORIGINALS snapshot is independently verified before
and after preparation, including currently present cache bytes. This correction
changes only new preparation metadata, not candidate source or historical pins.

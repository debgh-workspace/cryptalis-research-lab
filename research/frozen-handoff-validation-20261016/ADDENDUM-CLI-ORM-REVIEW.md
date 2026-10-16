# Accepted scoped operator-addendum review

2026-10-16 UTC. Verdict: ACCEPTED for the assigned CLI, ORM and index-delta scope.

Exact reviewed files under experiments/frozen-preview-operator-addendum-20261016:

- OPERATOR-CLARIFICATIONS.md: b3bdaf039aef832e4f41da13c8316f1291e5ed492ba595140af37558527c6cb3
- INDEX.md: 09ab05e24a9b1a8d7b0c5f48be5d83ef78f923d9f9fb3b26a3036f28c191c681

## Checks

The frozen candidate cli.py:490–503 reads declaration bytes from the path,
writes readable declaration reports to stdout and returns2 for REJECTED,
otherwise3. doctor.py:24–28 fixes complete/ready false. Argument failures use
exit2 and stderr (cli.py:75–83,382–390); invalid/missing/inaccessible path
errors map to2 and other unavailable I/O to4 (170–199). Output failures use4
(294–313), including inability to deliver diagnostics (515–522). The addendum
correctly distinguishes channels and does not equate empty stderr with
acceptance. Its “normally” wording preserves exceptional I/O/cleanup outcomes.

The shell if/else preserves the failing command status immediately in the
else branch, permits deliberate exit3 without an unguarded errexit abort,
and explicitly rejects2,4 and unexpected codes rather than masking all
nonzero outcomes. Exit3 is described as an incomplete report, not deployment
qualification. No shell template was executed for this review.

__main__.py:1–4 calls main through SystemExit; pyproject.toml:15–16 declares
cryptalis = cryptalis.cli:main. AGENT6's frozen-cli-dx-independent-20261016/
REVIEW.md confirms matching accepted wheel entry_points.txt and the exact
runtime module bodies. I independently checked the frozen source/packaging
declaration, not live installed payloads or a new wheel execution. The wording
now says “static doctor subcommand”, correctly avoiding the initial claim
that doctor is the only CLI command: manifest inspect/inspect-history remain
defined at cli.py:113–159. The required input path and approved output
directory are explicit; the template grants no install, smoke or custody
authority.

The ORM correction accurately reproduces the reviewed finding: the old
packaged walkthrough omits deployment after product protection; migration.py:
916–931 requires the external tuple and exact plan/lock/runtime-role checks.
The addendum now imports attach explicitly and supplies deployment=(p,
active_pin), retaining current approved ACTIVE authority and the default
async SQLModel refusal. It does not suggest fabricating a pin or enabling a
private flag. Main quickstart remains preferred and frozen files unchanged.

An exact text diff against experiments/frozen-preview-handoff-v1-20261016/
INDEX.md contains only the appended “16 October operator corrections” heading
and one relative-link paragraph. No prior index text was edited. Its summary
accurately names the three addendum topics and preserves unexecuted workflow,
unchanged artifacts and unchanged gates. Snapshot-holder technical acceptance
is delegated to the separately named snapshot review; I have not independently
requalified that section here.

No remaining correction in assigned scope. The initial “CLI accepts only”
scope wording was corrected before these final hashes were selected.

No product/source edits, imports, tests, DB/status, Git, installation or
publication occurred. Only this reviewer report was written. This accepts
documentation accuracy within scope, not operation authority or runtime
qualification.

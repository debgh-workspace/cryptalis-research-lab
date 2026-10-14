# C9 upstream follow-up: no matching correction established

Reviewed 2026-10-14, approximately 13:15-13:17 UTC. Additive source/web research
only. No dependencies installed/updated, external code executed, candidate imports,
tests, DB access, issues filed, maintainer contact or compatibility exception.
REVIEW.md and SOURCE_PINS.json are unchanged.

## Outcome

No exact supported version or commit correcting C9's four warmed required/default
expanding-IN sequences was established. Newer releases exist, but the inspected
tagged source still contains both relevant mechanism ingredients. Accordingly do
not recommend upgrading as a demonstrated fix, do not rerun merely on that hope,
and retain C9's recorded mismatch and all current security boundaries.

This is not proof that no issue, patch or fix exists anywhere upstream. Search and
history access were incomplete; no external release was executed.

## Verified release availability

Official release pages verify:
- [2.0.54](https://github.com/sqlalchemy/sqlalchemy/releases/tag/rel_2_0_54),
  September 15, 2026; displayed commit abbreviation bb8a901.
- [2.1.4](https://github.com/sqlalchemy/sqlalchemy/releases/tag/rel_2_1_4),
  October 7, 2026; displayed commit abbreviation 632c664; shown as Latest when read.

The [2.0 changelog](https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html)
lists 2.0.55 with no release date. Its existence as a changelog section does not
establish a released/installable correction. The [2.1 changelog](https://docs.sqlalchemy.org/en/21/changelog/changelog_21.html)
also has a 2.1.5 section; no release availability or relevant fix is claimed here.
Installed 2.0.51 and 2.1.3 remained untouched.

## Tagged source comparison

Read official tagged files, without downloading or importing executable code:
- [2.1.4 compiler.py](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/rel_2_1_4/lib/sqlalchemy/sql/compiler.py)
- [2.1.4 elements.py](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/rel_2_1_4/lib/sqlalchemy/sql/elements.py)
- [2.0.54 compiler.py](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/rel_2_0_54/lib/sqlalchemy/sql/compiler.py)
- [2.0.54 elements.py](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/rel_2_0_54/lib/sqlalchemy/sql/elements.py)

In both tags, BindParameter._gen_cache_key returns identity/class/type/key and
literal_execute metadata, without required. In both tags, SQLCompiler.construct_params
checks the compiled bind's required state before selecting the incoming
resolved_extracted bind value, in both nonempty-params and empty-params branches.
These are the same source conditions that the retained pinned-version compiler
and PostgreSQL evidence associates with C9's order dependence.

Inference: these inspected locations do not supply a correction. This is a bounded
source finding, not execution proof that every outcome on those releases matches
our installed matrix. No full source-tree diff or dependency qualification occurred.

For orientation only, the web renderer displayed the relevant 2.1.4 methods around
compiler lines 1882-1938 and elements 2079-2103; 2.0.54 around compiler 1785-1841
and elements 1998-2018. These are web-renderer line numbers, not a promised match
to downloaded-file line numbering. Method names and tag-specific URLs identify
the source precisely. The [main compiler](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/main/lib/sqlalchemy/sql/compiler.py)
also showed the required-before-extracted logic when inspected; main is mutable
and this observation is not an immutable release/commit claim.

## Similar changes are not C9 fixes

- 2.1.4 adds missing cache-key participation for return_defaults supplemental_cols
  on INSERT/UPDATE, correcting order-dependent RETURNING shape. This shares a
  general cache-metadata theme but does not repair SELECT BindParameter.required.
  Listed also for unreleased 2.0.55. See [2.1.4 SQL notes](https://docs.sqlalchemy.org/en/21/changelog/changelog_21.html#change-2.1.4).
- 2.0.38's #12314 corrects IN-list composition when an element is None; C9 instead
  uses an explicitly expanding bind whose required/default status differs between
  statements. It is not evidence for this fix. See [2.0.38 notes](https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html#change-2.0.38).
- [Discussion #13145](https://github.com/sqlalchemy/sqlalchemy/discussions/13145)
  concerns UPDATE/CTE bind names interacting with generated SET columns. It does
  not acknowledge C9's four SELECT histories.
- [Discussion #10819](https://github.com/sqlalchemy/sqlalchemy/discussions/10819)
  concerns lambda/plain-expression composition and stale closure values. It also
  does not acknowledge C9 or establish a matching correction.

## Semantics and acknowledgement

The official [bindparam contract](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
and [required-bind error documentation](https://docs.sqlalchemy.org/en/20/errors.html#a-value-is-required-for-bind-parameter-x-in-parameter-group-y)
support per-execution required-value checks. The retained pinned docstrings give
the same contract (see REVIEW.md). No reviewed official source says C9's successive
ordinary SELECT statements are unsupported or that cached required flags should
supersede the incoming declaration. No matching maintainer acknowledgement was
located. Therefore an implementation-anomaly inference remains appropriate;
upstream acknowledged bug, exact fix commit and qualified fixed version remain UNKNOWN.

## Search limits and stopping condition

Searched official docs and indexed sqlalchemy/sqlalchemy issues/discussions for
bindparam + required + cache, required flag/cache key, required=True/False,
construct_params and resolved_extracted. Inspected release/changelog near matches
and official tagged mechanism source. Some targeted search queries returned
irrelevant results; those were not relied upon. Direct GitHub compiler-history
and issue-filter pages returned tool Internal Error, so no exhaustive history or
issue search is claimed. No alternate authenticated access or external contact
was attempted. Scope ends at identifying a source-supported correction, or finding
none with precise limits; the latter was reached.

Next action remains a decision, not an automatic runtime task: retain exact-native
HOLD, or authorize a further bounded investigation. A proposed dependency change
would require an actual relevant source correction followed by new independent
qualification. Neither the release number nor unrelated cache fixes suffice.

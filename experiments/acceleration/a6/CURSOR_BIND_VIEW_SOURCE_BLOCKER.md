# Row-aware cursor bind view: source-only blocker

Status: BLOCKED for a public-event-only general row-aware mechanism.
No DB run requested. No new runnable test selector is frozen for root.

R2's 10 PASS in each pinned cell is preserved. Root reported 0.96 s (2.1.3)
and 0.76 s (2.0.51), stable source, unchanged preflight and stopped cluster.
Those results establish selected native state-to-logical-group lineage only.
They do not establish logical-group-to-final-driver-batch provenance.

## Public event can return an independent driver view

before_cursor_execute(retval=True) returns a statement and parameters used by
that cursor call. It can therefore return newly allocated driver parameters
without mutating context.compiled_parameters. This preserves the native logical
parameters consumed by postfetch, provided nothing else mutates them.

However, the event is AFTER all ordinary bind processors. It cannot implement a
post-default/pre-bind protected seam under the current sealed-only payload
processor. Synthetic ordinary TEXT transformation would demonstrate a later
boundary only. No placeholder, plaintext bypass, actual key or protected-route
relaxation is authorized.

## Missing exact native batch association

Installed source references are relative to each SQLAlchemy source root recorded
in the preceding design report.

| Evidence | 2.1.3 | 2.0.51 |
|---|---|---|
| Native batch record fields | sql/compiler.py:633-655 | sql/compiler.py:622 and following |
| Actual batch and compiled-group slicing | sql/compiler.py:6099-6103 | sql/compiler.py:5768-5772 |
| Positional batch flattening | sql/compiler.py:6186-6194 | sql/compiler.py:5852 and following |
| Named per-batch index expansion | sql/compiler.py:6198-6209 | sql/compiler.py:5864 and following |
| Local batch passed into engine execution | engine/base.py:2011-2047 | engine/base.py:2042-2080 |

The compiler keeps two lists, derived from this execution's native driver groups
and logical compiled groups. It takes corresponding slices for each batch.
The batch object retains batch driver-row references, sentinel values and batch
metadata. This is useful private provenance at the producer.

The public cursor event receives only the replacement statement, replacement
parameters, the full execution context and executemany=True. It does not receive
the batch object or the exact compiled_batch slice. For positional SQL the
native compiler flattens row tuples. For named SQL it creates a new dictionary
with generated keys such as key__i, where i restarts inside each batch. The
context still contains all logical rows for the entire execution.

Thus the R2 sidecar's exact compiled-dictionary identities do not identify which
row produced a given leaf in this event's flattened replacement dictionary or
tuple. Small batches may look straightforward but do not prove the general
mapping. Counting event calls, assuming page size, parsing SQL/suffixes or using
row index alone reconstructs a guess instead of carrying source identity.
Matching UUID/text values is still value matching and is not the requested
producer authority. Equal-valued rows remain a deciding case.

The engine chains before_cursor_execute listeners, passing each listener's
returned statement/parameters to the next. An earlier listener can replace,
copy or reorder them. A later listener can invalidate a transformation after
its validation. A local context association alone cannot authenticate this
replacement chain. Public events expose neither a privileged final listener
slot nor a native provenance transfer contract for arbitrary rewrites.

## Path-specific distinctions

- Single-row named execution can be narrowly checked against exact context and
  parameter-container identities. That is not general IMV proof.
- Ordinary positional/executemany needs a qualified native bind-slot mapping
  and exact input container lineage. A value-only check is insufficient.
- IMV introduces another native transformation and batch slicing. The public
  callback loses the batch object that records those source row containers.
- Reordered or replacement listener parameters require explicit provenance
  transfer. Without it, refusal is the honest outcome, even if values match.

## What would be needed for a later test-only experiment

A separately scoped private observer would need to carry exact receipts through
native logical-group-to-driver-group materialization AND through the actual
compiler/dialect IMV batch producer. It must retain the exact yielded batch,
its replaced parameter object, constituent driver-row references and the exact
native mapping of bind slots. The public event could then accept only that
unmodified current receipt; rewritten/reordered inputs would be negative cases.

Merely wrapping the public event and retaining the prior R2 map does not provide
these edges. Merely observing an IMV yield does not by itself identify all
positional slots: positional expressions, extra leading/trailing parameters,
compiler key escaping and batch downgrade branches remain obligations. A full
experiment would require both native producer surfaces, their pinned source
coverage and named/positional/downgrade/multipage/rewrite tests. These are new
private instrumentation costs, not an existing public solution or permission
to promote a cursor-level security boundary.

The stopping condition requested by root is reached: the public-only proposed
mechanism cannot presently prove all required positional/named/IMV/reordered
associations without guessing. Preserve refusal and report this exact gap.

## Files and unexecuted preliminary work

This candidate was copied from R2 without bytecode/test caches. All inherited
R2 source files remain unchanged. Before root narrowed the requested mechanism,
an ordinary scalar TypeDecorator demonstration was drafted and syntax-checked.
It does not prove a row-aware sealed bind view. It was moved out of pytest test
discovery to illustrative_scalar_projection_not_qualified.py and is explicitly
not a deliverable to run or qualify. It was never imported or executed. No
public cursor transformer, runtime hook, callback replacement, cryptography,
provider action, database access or Git operation was performed.

# Independent source review: canonical tenant parsing proposal

Disposition: ACCEPT SOURCE PROPOSAL ONLY. Runtime qualification and promotion HOLD.

Reviewed proposal SOURCE.sha256 seal ec7298aa79b41c53326e2aea616bd8e300a138a830da6eaefb98de3640d0d45e. All six members verified. Baseline sqlalchemy.py is byte-identical to restored source221 (bd36700fd6ee58afdad9b90943ce5b119967fe5ebde14d1f4cacd26c2a8160f1). Candidate is 5393819f2f312b9196bd2ffe185713d7d8ce6487eeb0b55b1b4e50cc7baa8395. The actual full diff contains only the two declared _ReadText changes. No target execution, import, syntax compilation, tests, DB or candidate edits occurred.

## Source findings

- Candidate lines 149–151 capture a strong reference plus canonical text only for exact UUID. Lines 170–175 reuse only for exact str, the original captured object still bound to self.tenant, and canonical text equality. Ordinary UUID value immutability is assumed, as elsewhere; hostile mutation of internals or module globals is outside this finite boundary.
- Rebinding self.tenant to B disables the shortcut. An A row is parsed normally then rejected by the unchanged comparison, before open_text. A B row uses fallback and forwards B with the current processor keys. That observer result is not a real-CF1 permission: _context still checks tenant against key policy.
- Equal-but-distinct A disables reuse without changing UUID value semantics. Restoring the original A permits reuse. Holding the object avoids ID-reuse reasoning entirely.
- UUID subclasses in the captured operation get no cache. String subclasses as incoming rows always reach the original UUID(tenant) call, even when their contents are canonical. Noncanonical ordinary strings, incoming UUID objects, bytes and other types likewise follow the original constructor and exception translation. This is source-level preservation of the constructor path, not a new promise about arbitrary subclass methods or every interpreter's constructor behavior.
- Record parsing, outer-join NULL scope, exact row shape, tenant/point comparisons, hex validation, exception normalization and final open_text call are unchanged. Current self.keys and self.points remain used. No context, authorization, key lease or crypto result is cached by this delta.
- _Payload.column_expression still admits the selected operation owner and captures that operation's fields. Existing captured-result semantics remain after ambient/original-operation rebinding. Both TypeDecorator cache_ok=False declarations and the protected SELECT compiled_cache=None remain unchanged. The independent search processor and rewrite logic are untouched.
- Real CF1 open_text calls _context first; a genuine SQL NULL then resolves payload policy before returning. Non-NULL frames still verify descriptor/tenant/record context, authentication tag and post-decrypt key resolution. The outer-join absent-row NULL return is a separate pre-existing branch, not evidence that real NULL can bypass key resolution.

## Literal oracles and mutation controls

The 23 literal rows are coherent parser/control-forwarding cases: canonical/noncanonical strings, wrong tenant/point, malformed input, outer NULL, processor tenant/key/point mutation, operation/ambient change and independent processor B. The observer must check call counts and forwarded values against literals, not just baseline equality. Setup instructions must be concretized with fresh objects, isolated state and complete per-call expectations for the P(A), Q(B), P(A) sequence; the one Q row does not itself encode all three outcomes.

The meaningful stale-cache mutant is old cached text matching A followed by substituting rebound self.tenant B. It passes the later tenant equality but must fail rebind-tenant-reject-old's literal AuthenticationFailed/call-count-zero requirement. In contrast, deleting only the identity gate while continuing to use cached[0] still reaches the unchanged comparison and rejects mismatched expected tenant; do not manufacture a failing oracle or claim that mutation proves a security property.

The literal catalog is not complete runtime qualification. Before a harness is source-accepted, add explicit cases for a benign str subclass and UUID subclass captured tenant; incoming UUID and bytes; UUID record codec including malformed/wrong record; single-tenant codec and both outer-join NULL branches; and bool versus integer record behavior. These exercise expressly retained fallback/codec behavior absent from the 23 rows. Additional exotic subclass side effects need not be admitted.

The required real-CF1 layer currently exists only as prose. Bind exact fixtures and literal outcomes for alpha/beta, wrong tenant, wrong record, altered tag, revoked/unavailable key on real NULL, both representations, record codecs and tenancy codecs. Observer-only keys-A/keys-B markers cannot establish these properties. Require the stated tenant/point/early-NULL mutants to be killed in their appropriate observer or real-CF1 layer. Do not reuse historical correctness counts as coverage for this new candidate.

## Missing runtime evidence

No runnable harness, complete source namespaces, dependency/native/interpreter bindings, current external admission, execution capture or performance result is supplied. Complete both admitted SQLAlchemy cells against independently literal expectations, preserve current authorization checks and separately review the exact harness/control packet before selecting execution. Any real-CF1 success with mismatched policy, surviving behavior-changing mutant, stale processor cross-use, or differing exception normalization is HOLD. No performance claim follows from removing one parse: constructor string/tuple allocation and per-row branches also cost work.

Smallest next step: author the isolated finite harness and expanded literal matrix, retaining this sealed proposal unchanged; review and admit that new packet before execution. No source correction to the two-hunk candidate is required by this review.

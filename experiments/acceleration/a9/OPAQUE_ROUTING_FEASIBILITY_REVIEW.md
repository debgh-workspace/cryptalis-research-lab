# Opaque exposure routing: bounded pure feasibility and stop decision

Status: NO-CRYPTO, NO-DATABASE feasibility only. Current runtime unchanged.
No architecture amendment, protected admission or implementation approval.

## Result

Both pinned SQLAlchemy versions completed 12 pure cases in a local fake DBAPI
harness: two ordinary native plaintext controls and ten routed cases covering
no-argument/context-aware UUID defaults with success, constructor failure,
default failure, bind-processor failure and fake-driver failure.

The routed cases exposed no synthetic plaintext in the checked before_execute,
before_cursor_execute, after_execute, handle_error.parameters, StatementError
or DBAPIError.params, ordinary formatted engine logs, or public context compiled
parameters. Pending inputs never reached fake cursor execution. Ordinary native
controls explicitly calibrated the same event collectors to see plaintext.

This is not a PostgreSQL or async pass. It is not a crypto or final guarded-driver
qualification. No network connection, real database, credential file or Cryptalis
runtime module was used. The Engine uses DefaultDialect and a directly supplied
in-memory FakeConnection; execute records arguments in Python and performs no
SQL. The source hashes/version of eight installed SQLAlchemy files were checked
before execution. Two small method patches live only inside this standalone
process and restore in finally. Installed package files were not changed.

## Pure routing model

1. At actual native UOW record production, preserve the protected logical value
   in an operation-local dictionary and replace its SQL input with an empty-slot
   Pending token before Connection execution events. The token's repr is fixed
   and contains neither plaintext nor a pointer field to the private store.
2. Observe construct_params' actual input and returned dictionary identities,
   following A7's source-association approach. Copies are not matched by value.
3. For no-argument defaults, let the native default method operate on opaque
   public compiled groups. The callback receives no new context argument and
   observes the ordinary native ORM attributes it already owns.
4. After default evaluation, replace safe public compiled token entries with
   SyntheticSafe inputs. The test's sealed-only processor accepts only this
   class and produces fixed public bytes containing the generated UUID, never
   the logical plaintext. These bytes are explicitly NOT ciphertext or CF1.
5. Native postfetch assigns the UUID normally; the original ORM secret attribute
   remains ordinary plaintext. Failure rollback follows the native Session path.
6. On context-aware defaults only, temporarily expose separately created private
   logical dictionaries while invoking the unchanged native default method.
   Capture each safe/private dictionary pair when created. Restore safe context
   groups in finally before constructor error handling. Remove instance-level
   current_parameters left on a failed default. Callback-retained logical
   dictionaries remain unchanged and plain in the trusted application.

The pure model intentionally changes protected SQL inputs before the first
execution-event dispatcher, rather than trying to redact plaintext after a
listener has already received it. Native mapper callbacks still receive normal
ORM state, as the existing trusted-application contract permits.

## Exposure surfaces checked, and remaining obligations

| Surface | Pure observation | Still required before a real route |
|---|---|---|
| First before_execute parameters | Pending tokens only on routed path | Actual protected mapping/fingerprint and UOW receipt admission; refuse transformations before/inside execution dispatcher |
| Constructor/default/processor failure .params | Opaque original SQL inputs; no synthetic plaintext | Full selected dialect/async/native exception and cancellation coverage |
| Public execution context after defaults/failure | Safe compiled entries; no instance current_parameters | Reentrant callbacks, other context fields, result/error hook auditing |
| before_cursor parameters | Synthetic safe bytes; no Pending token | Actual pre-materialization CF1 sealing, every lease/PID/context check and raw-driver collectors |
| after_execute inputs and result context | Pending/safe entries, no new plaintext parameters | Other result metadata and instrumentation surfaces; approved exposure contract |
| Ordinary engine parameter logging | hide_parameters=True and no synthetic plaintext in capture | Supported logger/debug/error paths, current engine admission unchanged |
| ORM attributes/postfetch UUID | Original plain attribute; native generated UUID | Full history/identity/default/error/retry parity against real dialects |
| Final actual driver arguments | Fake driver rejects Pending and plaintext | Actual final argument receipt check after ALL public listeners; not established here |

The generic harness does not transplant A7's complete named/positional IMV slot
probe machinery. A7 establishes those bounded producer edges separately. This
experiment tests the earlier exposure route and identity decision, not their
combined security. The final implementation would have to compose both rather
than treat either as a substitute for the other.

## Decisive context-aware compatibility counterexample

A native context callback can retain all three of:

- the actual ExecutionContext object;
- context.get_current_parameters()'s actual dictionary;
- context.compiled_parameters' actual list.

In ordinary native success, the retained context still points to that same
compiled-parameter list after flush. In this opaque model, the retained plain
dictionary remains valid, but the actual context must point back to its safe
public list before after_execute/error handlers can inspect it. The pure runs
observe native list identity True and routed identity False on BOTH versions.
This is an observable compatibility change, not a harmless internal detail.

There is no claim that all context-aware default behavior is preserved. Keeping
the native context/list plain after the callback would violate the independent
review HOLD on new public-context plaintext. Giving the callback a proxy or
copy would instead change its context identity/type/reflection. Silently limiting
callbacks to get_current_parameters alone would change the promised profile.

Decision needed: either explicitly approve a narrowly bounded initial no-arg
profile while keeping context-aware compatibility as a separate unresolved
objective, or review the permitted callback-context behavior/interface. Neither
choice is made by this experiment. The broader objective is not dropped.

Even the no-arg result is only a feasibility lead: stack inspection, arbitrary
application callback exceptions, custom codecs, reentrant/default SQL, native
async behavior, relationship tenants and real guarded driver receipt checks
are not qualified. Callback-owned application plaintext is allowed by the
existing trusted-process contract; that does not authorize new engine event
or exception parameter plaintext surfaces.

## Required full-pipeline design after a decision

- Capture protected plaintext privately at the actual producer BEFORE every
  execution-event boundary; no plaintext-bearing attributes on Pending tokens.
- Retain authoritative UOW/Session/state/mapper/table/connection/attempt receipts
  through safe parameter construction; preserve Core/raw/bulk refusal.
- All Pending values must be consumed or refused before driver materialization.
  Never allow a placeholder or placeholder bytes to reach SQL as a fallback.
- After native defaults, construct actual sealed bind inputs locally with exact
  UUID/tenant/context. The current _Payload plaintext refusal remains intact.
- Preserve safe public parameter dictionaries across constructor, bind, execute,
  result and error paths; private logical views cannot accidentally become event
  or exception .params. Native user exception payloads need their own reviewed
  boundary; this fixed-message harness does not establish arbitrary exception
  message sanitization while preserving arbitrary original exception objects.
- Compose A7's actual driver/IMV receipts and validate final effective SQL and
  parameters at the guard after all public retval listeners, immediately before
  the real driver permit. Validate both provenance and integrity. The existing
  check_cursor(context)-only signature does not establish that final check.
- Clear pending/private state on every unwind and prove no stale token permits
  a retry. No root/key material, key preparation or crypto was exercised here.

## Preserved initial failure and reproducibility

The initial pure run failed because the observer used hasattr on a class-level
current_parameters default and then tried to delete an absent instance entry.
The initial script and summary are preserved. The correction checks the instance
dictionary, matching the intended cleanup. This was a test observer failure,
not a SQLAlchemy or Cryptalis product defect.

Final executable: experiments/opaque_routing_feasibility.py.
Receipts: experiments/pure-sa21.json and experiments/pure-sa20.json.
These are standalone pure checks, not a pytest/PG selector. Root must separately
authorize any later real-database experiment through the unchanged wrapper.

STOP: no crypto/runtime integration and no claim of full context-callback parity.
The explicit callback-context decision and independent review remain required.

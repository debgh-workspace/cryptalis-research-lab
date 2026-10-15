# Independent source review: transient JSON constructor

Received 2026-10-15 from a separate source reviewer. No implementation, product imports, tests, database access or measurement was performed. This record is preserved by the coordinator from the returned findings.

## Disposition

Prefer the exact `jsonb_build_array` to `json_build_array` hypothesis at selected `sqlalchemy.py:221` over a new binary envelope. Leave `_ReadText` and all other product code unchanged. No source-level blocker was found for native admitted operand types, but runtime correctness, public compatibility and gain remain UNKNOWN. The OID/custom-loader issue requires mandatory characterization before product admission.

## Independent source evidence

- PostgreSQL REL_16_15's JSON builder retains array argument order and NULL slots and emits JSON text directly. JSONB construction creates an intermediate JSONB value that its output routine serializes. [json.c](https://raw.githubusercontent.com/postgres/postgres/REL_16_15/src/backend/utils/adt/json.c), [jsonb.c](https://raw.githubusercontent.com/postgres/postgres/REL_16_15/src/backend/utils/adt/jsonb.c).
- Admitted operands are hex text, native UUID or int8, and native UUID or single-tenant text. They become JSON strings, exact integer numbers or NULLs. No objects, duplicate keys, floats or custom scalar casts are newly admitted.
- Actual server result OID changes from 3802 to 114. `_ReadText` already declares JSON; `type_coerce` does not cast the server expression. [PG type catalog](https://raw.githubusercontent.com/postgres/postgres/REL_16_15/src/include/catalog/pg_type.dat).
- Psycopg 3.3.6 default text JSON and JSONB loaders share the same decoder. Binary JSONB decoding additionally removes the version byte. `set_json_loads` covers both types and formats. OID-specific custom registrations can differ. [Pinned psycopg JSON source](https://raw.githubusercontent.com/psycopg/psycopg/3.3.6/psycopg/psycopg/types/json.py).
- SQLAlchemy 2.0.51 delegates JSON result decoding to psycopg. SQLAlchemy 2.1.3 has native deserialization flags and installs engine JSON deserialization through psycopg's shared function. [2.0.51 dialect](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/rel_2_0_51/lib/sqlalchemy/dialects/postgresql/psycopg.py), [2.1.3 dialect](https://raw.githubusercontent.com/sqlalchemy/sqlalchemy/rel_2_1_3/lib/sqlalchemy/dialects/postgresql/psycopg.py).

## Preserved boundaries

`sqlalchemy.py:144–180` retains operation-local keys, expected tenant/point context, separate missing-join and present-NULL behavior, payload bounds, exception mapping and `open_text`. Crypto authentication and lease/fork checks remain at `crypto/cf1.py:181–222` and `crypto/keys.py:278–284`.

Labels, aliases and entities retain the projection hook and compiler adaptation at `sqlalchemy.py:562–584`. Protected DISTINCT is already refused at `:592–597`; protected ordering is separately refused. Verify these refusals occur before cursor execution, rather than relying on JSON's lack of comparison operators.

## Native comparator and controls

Return separately typed native bytea/UUID/bigint/NULL operands together with both constructors. Independently derive the expected Python list from those native values, without either constructor or `_ReadText` as oracle. Cover empty bytea versus NULL payload, all three NULL positions, single-tenant sentinel, nil/non-nil UUIDs and bigint -2^63, -2^53-1, -1, 0, 1, 2^53+1, 2^63-1. Require exact integer types and values.

Record actual OIDs/formats and decoded types for default, shared engine JSON deserializer, deliberately differential per-OID custom loaders, sync and async. Use separate connections for custom registrations. A binary-cursor comparison is a control, not permission to change application defaults.

The later application oracle needs independent native plaintext mapping/engine, original JSONB path and candidate JSON path, with exact values/types/labels/mappings/duplicates/order/pagination. Do not sort ordered results: earlier `profile_sqlalchemy_search.py:247–254` sorts its checks and cannot establish ordering preservation.

Existing selected test source anchors:

- `test_sqlalchemy_adapter.py:134–165`: entities/scalars/labels/aliases/outer joins/relationships/streaming.
- `:170–210,616–689`: interleaved tenant/context and async reuse.
- `:213–255,323–395`: authentication/requested-row enforcement.
- `:842–851`: single-tenant bigint outer join, currently only 2^40; add true int64 extremes to the new comparator.
- `test_sqlalchemy_outer_nulls.py:53–163`: NULL truth, duplicates and join topology.
- `test_sqlalchemy_ordering_labels.py:70,120`: pre-driver protected refusal and native public ordering.

## Rejected wider first slice

A binary envelope adds presence flags, signed-integer parsing, format/bounds validation and a new result processor. Default psycopg text results still transmit bytea as hex, so it does not inherently halve wire bytes. [Psycopg formats](https://www.psycopg.org/psycopg3/docs/basic/params.html#binary-parameters-and-results), [PostgreSQL bytea](https://www.postgresql.org/docs/16/datatype-binary.html).

## Procedure limitation

An initial source navigation command named nonexistent `src/cryptalis/crypto.py`. The reviewer paused under repository guidance, reported the exact missing-path issue and received explicit coordinator authorization to continue source-only reading of the actual `src/cryptalis/crypto/` package. No access restriction was bypassed or runtime action retried.

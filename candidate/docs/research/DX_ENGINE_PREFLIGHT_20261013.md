# Attachment logging preflight: DX-ENGINE-PREFLIGHT-01

Status: isolated S14-derived correction. No integrated promotion or PostgreSQL
regression is claimed here. All seven independent gates remain UNKNOWN.

## Observed adoption failure

The recorded FastAPI adoption and S15 maintenance-bridge setup each encountered
the existing requirement for `hide_parameters=True`. S14 checks logging settings
inside attachment activation, after database inspection, then raises a general
`PolicyMismatch`. The failure remedy lists several unrelated policy checks.

The public `cryptalis.sqlalchemy.attach` entry now checks the same logging
predicate before constructing its attachment or opening a connection. A failed
check raises `UnsafeEngineLogging`, a `PolicyMismatch` subtype with a fixed
`engine logging admission` stage and a concrete remedy: construct the runtime
engine with `echo=False` and `hide_parameters=True`.

This adds no accepted configuration. It does not set engine options, change
privileges, infer a key policy, or admit a new framework/profile. Existing
activation and per-operation checks remain unchanged. Malformed lock bytes
retain their existing `PolicyMismatch` failure precedence. Application logging
and trusted engine callbacks still need separate review.

## Deterministic public-boundary evidence

`tests/test_attachment_engine_preflight.py` uses real synchronous/asynchronous
SQLAlchemy engines with a `do_connect` sentinel that refuses before driver
connection. A separate key sentinel records unexpected key access. No database,
private credential file, provider or network service is accessed.

Four unittest methods contain 18 public-call cases:

- Twelve unsafe-setting cases: omitted redaction, disabled redaction, echo and
  debug echo, on both sync and async engines.
- Four allowed-setting cases reach the connection sentinel, preserving the
  existing admission path. These do not establish successful attachment.
- Two malformed-lock cases retain the existing safe failure and do not connect.

Each case checks that the engine configuration, mapper configuration and mapped
column type are unchanged. Error output and attributes exclude the synthetic
URL/error marker. Failures remain non-retryable with no effects.

Python 3.12.14, psycopg 3.3.6 and cryptography 50.0.2 were used in both cells:

| Boundary | SQLAlchemy 2.0.51 | SQLAlchemy 2.1.3 |
|---|---|---|
| Original S14 public preflight | 12 failures; 6 other cases pass | Not separately run |
| Corrected preflight | 4 methods / 18 cases pass | 4 methods / 18 cases pass |
| Remove only the new predicate | 12 failures | 12 failures |
| Restore exact runtime bytes | 4 methods / 18 cases pass | 4 methods / 18 cases pass |

The failures observe actual arrival at the connection sentinel, rather than
merely a missing exception class. The mutation leaves the new type defined but
removes its check. Raw logs and the source-bound mutation receipt are in
`evidence/dx-engine-preflight/` in this isolated work copy.

Direct execution is limited to these non-database unittest controls:

```sh
PYTHONPATH=src /path/to/existing/python tests/test_attachment_engine_preflight.py
```

Coordinator-owned PostgreSQL regression remains required through the unchanged
dual-role preflight. These controls do not qualify database schema validation,
successful attachment, runtime confidentiality, or release readiness.

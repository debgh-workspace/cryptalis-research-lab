"""Fault injection at external crypto boundaries; no alternate algorithm oracle."""

import traceback

import pytest
from sqlalchemy import event, select
from sqlalchemy.exc import StatementError

from cryptalis.crypto import cf1
from cryptalis.crypto.keys import CryptoBackendUnavailable
from test_cf1 import RECORD, TENANT, descriptor, setup_keys
from test_sqlalchemy_search import _row, search_application

CANARY = "synthetic-backend-diagnostic-must-not-escape-CP03"
STAGES = ("hkdf-constructor", "hkdf-derive", "hmac-constructor", "hmac-update", "hmac-finalize")


def _inject(monkeypatch, stage):
    """Replace only the selected external backend boundary, keeping others real."""
    if stage.startswith("hkdf"):
        original = cf1.HKDF
        class FaultHKDF:
            def __init__(self, *args, **kwargs):
                if stage == "hkdf-constructor":
                    raise RuntimeError(CANARY)
                self.native = original(*args, **kwargs)

            def derive(self, *args):
                raise RuntimeError(CANARY)
        monkeypatch.setattr(cf1, "HKDF", FaultHKDF)
    else:
        original = cf1.hmac.HMAC
        class FaultHMAC:
            def __init__(self, *args, **kwargs):
                if stage == "hmac-constructor":
                    raise RuntimeError(CANARY)
                self.native = original(*args, **kwargs)

            def update(self, *args):
                if stage == "hmac-update":
                    raise RuntimeError(CANARY)
                return self.native.update(*args)

            def finalize(self):
                raise RuntimeError(CANARY)
        monkeypatch.setattr(cf1.hmac, "HMAC", FaultHMAC)


def _safe_failure(error):
    original = error.orig if isinstance(error, StatementError) else error
    assert type(original) is CryptoBackendUnavailable
    assert original.code == "CryptoBackendUnavailable"
    assert original.stage == "cryptographic backend"
    assert original.retryable is True
    assert original.effects == "none"
    assert original.remedy and original.operation_id
    assert CANARY not in str(error)
    assert CANARY not in "".join(traceback.format_exception(error))


CASES = [(stage, operation, equality) for stage in STAGES
         for operation in ("seal", "open", "query") for equality in (False, True)
         if equality or (stage.startswith("hkdf") and operation != "query")]


@pytest.mark.parametrize("stage,operation,equality", CASES)
def test_cf1_external_backend_failures_have_safe_typed_diagnostics(monkeypatch, stage, operation, equality):
    field = descriptor(equality=equality)
    _, ring = setup_keys(equality=equality)
    keys = ring.prepare()
    frame = cf1.seal_text("exact value", field, TENANT, RECORD, keys)
    _inject(monkeypatch, stage)
    with pytest.raises(CryptoBackendUnavailable) as caught:
        if operation == "seal":
            cf1.seal_text("exact value", field, TENANT, RECORD, keys)
        elif operation == "open":
            cf1.open_text(frame, field, TENANT, RECORD, keys)
        else:
            cf1.equality_term("exact value", field, TENANT, keys)
    _safe_failure(caught.value)


@pytest.mark.parametrize("stage", STAGES)
@pytest.mark.parametrize("operation", ["insert", "query", "read"])
def test_backend_failure_preserves_database_and_safe_orm_errors(monkeypatch, stage, operation):
    with search_application() as app:
        row = _row(app, "before", 1)
        identity = row.id
        with app.sessions(tenant_id=app.tenant) as session:
            session.add(row)
            session.commit()
        calls = []
        listener = lambda *args: calls.append(True)
        event.listen(app.engine, "before_cursor_execute", listener)
        with monkeypatch.context() as faults:
            _inject(faults, stage)
            with app.sessions(tenant_id=app.tenant) as session:
                with pytest.raises((CryptoBackendUnavailable, StatementError)) as caught:
                    if operation == "insert":
                        session.add(_row(app, "must not persist", 2))
                        session.commit()
                    elif operation == "query":
                        session.scalars(select(app.Customer.id).where(app.Customer.name == "before")).all()
                    else:
                        session.scalars(select(app.Customer.name).where(app.Customer.id == identity)).all()
                _safe_failure(caught.value)
                session.rollback()
        event.remove(app.engine, "before_cursor_execute", listener)
        assert len(calls) == (1 if operation == "read" else 0)
        with app.owner_engine.connect() as connection:
            assert connection.exec_driver_sql(f'SELECT count(*), min(rank), max(rank) FROM "{app.schema}".customer').one() == (1, 1, 1)
        with app.sessions(tenant_id=app.tenant) as session:
            assert session.scalar(select(app.Customer.name).where(app.Customer.id == identity)) == "before"

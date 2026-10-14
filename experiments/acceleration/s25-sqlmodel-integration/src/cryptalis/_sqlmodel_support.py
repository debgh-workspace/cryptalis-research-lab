"""Narrow optional SQLModel integration; never accept an arbitrary Session class."""
from functools import lru_cache
from importlib.metadata import version
import sys
import sqlalchemy
from sqlalchemy import String


# Source-only laboratory prototype. Default admission stays unchanged.
# Never enable through a manifest, execution option, or Session argument.
_experimental_async_sqlmodel = False


def qualified_version():
    return version("sqlmodel") == "0.0.47" and sqlalchemy.__version__.split(".")[:2] == ["2", "0"]


def is_qualified_autostring(value):
    cls = type(value)
    if cls.__module__ != "sqlmodel.sql.sqltypes" or cls.__name__ != "AutoString":
        return False
    from sqlmodel.sql.sqltypes import AutoString
    return cls is AutoString and qualified_version() and type(value.impl) is String


def uses_sqlmodel(mapping):
    module = sys.modules.get("sqlmodel")
    return module is not None and any(issubclass(mapper.class_, module.SQLModel) for mapper in mapping.mappers)


@lru_cache(maxsize=2)
def guarded_session_class(base, native):
    # Class identity only: no attachment, tenant, row, keys or query context.
    class GuardedSQLModelSession(base, native):
        pass
    return GuardedSQLModelSession


def sync_session_class(base, mapping):
    if not uses_sqlmodel(mapping):
        return base
    if not qualified_version():
        raise ValueError("unqualified_sqlmodel_version")
    from sqlmodel import Session
    return guarded_session_class(base, Session)


@lru_cache(maxsize=2)
def guarded_async_session_class(base, native, guarded_sync, result_boundary):
    # Cache only class/function identities; no owner, engine, tenant or keys.
    class GuardedSQLModelAsyncSession(base, native):
        sync_session_class = guarded_sync
        # Native SQLModel.exec bypasses AsyncSession.execute. Keep the existing
        # Cryptalis result/cleanup boundary across its complete native call.
        exec = result_boundary(native.exec)
    return GuardedSQLModelAsyncSession


def async_session_class(base, sync_base, mapping, result_boundary):
    if not uses_sqlmodel(mapping):
        return base
    if (_experimental_async_sqlmodel is not True or not qualified_version()
            or sqlalchemy.__version__ != "2.0.51"):
        raise ValueError("unqualified_async_sqlmodel_version")
    from sqlmodel import Session
    from sqlmodel.ext.asyncio.session import AsyncSession
    return guarded_async_session_class(
        base, AsyncSession, guarded_session_class(sync_base, Session),
        result_boundary)

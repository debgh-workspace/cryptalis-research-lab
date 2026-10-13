"""Narrow optional SQLModel integration; never accept an arbitrary Session class."""
from functools import lru_cache
from importlib.metadata import version
import sys
import sqlalchemy
from sqlalchemy import String


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

"""Qualified native text metadata and assignment, outside the CF1 codec.

Limits come from the trusted source schema. Query values never use assignment
conversion. Arbitrary custom type decorators are not admitted by this module.
"""
from sqlalchemy import String, Text, VARCHAR
from sqlalchemy.dialects import postgresql
from .crypto.keys import InvalidText
from ._sqlmodel_support import is_qualified_autostring

_MAX_VARCHAR_CHARACTERS = 10_485_760


class CharacterLimitExceeded(InvalidText):
    stage = "native VARCHAR assignment"
    remedy = "Use a value within the declared character limit; no ciphertext or SQL was produced for this value."


def source_text_type(source):
    if type(source) is not dict or source.get("type_schema") != "pg_catalog":
        return None
    kind, raw = source.get("type"), source.get("typmod")
    if type(raw) is not str:
        return None
    if kind == "text":
        return ("text", None) if raw == "-1" else None
    if kind != "varchar":
        return None
    try:
        typmod = int(raw)
    except ValueError:
        return None
    if str(typmod) != raw:
        return None
    if typmod == -1:
        return ("varchar", None)
    if 5 <= typmod <= _MAX_VARCHAR_CHARACTERS + 4:
        return ("varchar", typmod - 4)
    return None


def mapped_text_type(mapped, source):
    native = source_text_type(source)
    if native is None:
        return None
    if type(mapped) in (Text, postgresql.TEXT):
        return native if native == ("text", None) else None
    if type(mapped) not in (String, VARCHAR, postgresql.VARCHAR) and not is_qualified_autostring(mapped):
        return None
    length = mapped.length
    if length is not None and (type(length) is not int or not 1 <= length <= _MAX_VARCHAR_CHARACTERS):
        return None
    return native if native == ("varchar", length) else None


def assign_text(value, character_limit):
    if value is None:
        return None
    if type(value) is not str:
        raise InvalidText()
    if character_limit is None or len(value) <= character_limit:
        return value
    if all(character == " " for character in value[character_limit:]):
        return value[:character_limit]
    raise CharacterLimitExceeded()

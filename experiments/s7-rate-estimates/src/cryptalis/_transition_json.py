"""Bounded transition artifacts; only measured-rate fields admit JSON floats.

Manifest, compiler-lock and descriptor decoders retain their integer-only
grammar. This decoder does not authenticate an artifact or replace its owning
plan's format, canonical-byte or semantic checks.
"""
import json
import math

from .manifest.parser import (
    MAX_DOCUMENT_BYTES, ManifestInvalid, _check_nesting, _check_unicode,
    _parse_counter, _reject_non_integer, _unique_object,
)


def _rate(token):
    value = float(token)
    if not math.isfinite(value) or value <= 0:
        raise ManifestInvalid('Measured rates must be finite and positive')
    return value


def decode_transition_json(raw, *, reverse=False):
    if not isinstance(raw, bytes):
        raise ManifestInvalid('Transition artifact input must be bytes')
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise ManifestInvalid('Transition artifact exceeds 16 MiB')
    _check_nesting(raw)
    try:
        document = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object,
                              parse_int=_parse_counter, parse_float=_rate,
                              parse_constant=_reject_non_integer)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ManifestInvalid('Invalid transition artifact JSON') from None
    if not isinstance(document, dict):
        raise ManifestInvalid('Transition artifact root must be an object')
    _check_unicode(document)
    prefixes = ((), ('source_plan',)) if reverse else ((),)
    allowed = {prefix + ('estimates', name) for prefix in prefixes
               for name in ('backfill_rows_per_second', 'verify_rows_per_second')}

    def check(value, path):
        if type(value) is float and path not in allowed:
            raise ManifestInvalid('Non-integer number outside measured-rate fields')
        if isinstance(value, dict):
            for name, member in value.items():
                check(member, path + (name,))
        elif isinstance(value, list):
            for index, member in enumerate(value):
                check(member, path + (index,))

    check(document, ())
    return document

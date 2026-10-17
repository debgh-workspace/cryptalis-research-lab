"""Decoded remaining projection shape only; no operational authority."""
from dataclasses import dataclass, field


class SchemaProjectionError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class SchemaInspection:
    classification: str = field(default='REMAINING_SCHEMA_PROJECTION_SHAPE_ONLY', init=False)
    metadata_validated: bool = field(default=False, init=False)
    current_native_verified: bool = field(default=False, init=False)
    successor_authorized: bool = field(default=False, init=False)
    text_order_verified: bool = field(default=False, init=False)


def _require(ok, code):
    if not ok: raise SchemaProjectionError(code)


def _members(value, names):
    _require(type(value) is dict and all(type(k) is str for k in value)
             and value.keys() == set(names.split()), 'invalid_members')


def _strings(value, keys):
    _require(all(type(value[k]) is str for k in keys.split()), 'invalid_string')


def _bools(value, keys):
    _require(all(type(value[k]) is bool for k in keys.split()), 'invalid_boolean')


def _vector(value, nullable=False):
    _require(type(value) is list and all(type(x) is str or (nullable and x is None) for x in value),
             'invalid_vector')


def _digest(value):
    _require(type(value) is str and len(value) == 64
             and all(c in '0123456789abcdef' for c in value), 'invalid_digest')


def inspect_remaining_schema_projection(value):
    _members(value, 'relation constraints indexes dependencies')
    relation = value['relation']
    _members(relation, 'relkind relpersistence relrowsecurity relforcerowsecurity relhasrules inherited user_triggers')
    _strings(relation, 'relkind relpersistence')
    _bools(relation, 'relrowsecurity relforcerowsecurity relhasrules inherited user_triggers')
    for key in ('constraints','indexes','dependencies'):
        _require(type(value[key]) is list, 'invalid_inventory')
    for item in value['constraints']:
        _members(item, 'name kind schema table deferrable deferred validated outgoing incoming columns referenced_columns definition_digest')
        _strings(item, 'name kind schema table')
        _bools(item, 'deferrable deferred validated outgoing incoming')
        _vector(item['columns']); _vector(item['referenced_columns'])
        _digest(item['definition_digest'])
    for item in value['indexes']:
        _members(item, 'name method constraint_name definition_digest primary unique exclusion nulls_not_distinct immediate valid ready live replica_identity partial expression total_columns key_columns columns dependency_columns opclasses collations')
        _strings(item, 'name method')
        _require(item['constraint_name'] is None or type(item['constraint_name']) is str, 'invalid_optional_string')
        _bools(item, 'primary unique exclusion nulls_not_distinct immediate valid ready live replica_identity partial expression')
        _require(all(type(item[k]) is int and item[k] >= 0 for k in ('total_columns','key_columns')), 'invalid_count')
        _vector(item['columns'], True); _vector(item['collations'], True)
        _vector(item['dependency_columns']); _vector(item['opclasses'])
        _require(item['key_columns'] <= item['total_columns'] == len(item['columns']), 'invalid_count_vector')
        _digest(item['definition_digest'])
    for item in value['dependencies']:
        _members(item, 'column kind')
        _strings(item, 'kind')
        _require(item['column'] is None or type(item['column']) is str, 'invalid_optional_string')
    return SchemaInspection()

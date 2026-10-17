"""Historical shape and supplied identity only; never operational admission."""
from dataclasses import dataclass, field
from uuid import UUID


class GuardProjectionError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class GuardInspection:
    classification: str
    metadata_validated: bool = field(default=False, init=False)
    current_native_verified: bool = field(default=False, init=False)
    successor_authorized: bool = field(default=False, init=False)
    text_order_verified: bool = field(default=False, init=False)


def _require(condition, code):
    if not condition:
        raise GuardProjectionError(code)


def _config(value):
    return value is None or (type(value) is list and all(type(item) is str for item in value))


def inspect_guard_projection(value, context):
    """Exact decoded shape then selected local identity policy; no normalization."""
    _require(type(context) is dict and all(type(k) is str for k in context)
             and context.keys() == {'operation_id', 'schema'}, 'invalid_context_members')
    _require(all(type(context[k]) is str for k in ('operation_id', 'schema')), 'invalid_context_string')
    try:
        operation = UUID(context['operation_id'])
    except ValueError:
        raise GuardProjectionError('invalid_operation_id') from None
    _require(str(operation) == context['operation_id'], 'invalid_operation_id')
    if value is None:
        return GuardInspection('MISSING_GUARD_OBSERVATION')
    _require(type(value) is list and len(value) == 11, 'invalid_guard_shape')
    _require(all(type(value[i]) is str for i in (0, 4, 5, 8, 9)), 'invalid_guard_string')
    _require(all(type(value[i]) is int and value[i] >= 0 for i in (1, 3)), 'invalid_guard_integer')
    _require(all(type(value[i]) is bool for i in (2, 6)), 'invalid_guard_boolean')
    _require(_config(value[7]), 'invalid_guard_config')
    _require(type(value[10]) is list, 'invalid_inventory')
    names = set()
    for item in value[10]:
        _require(type(item) is list and len(item) == 7, 'invalid_trigger_shape')
        _require(all(type(item[i]) is str for i in (0, 1, 2, 3, 6)), 'invalid_trigger_string')
        _require(type(item[4]) is bool, 'invalid_trigger_boolean')
        _require(_config(item[5]), 'invalid_trigger_config')
        _require(item[0] not in names, 'duplicate_trigger_identity')
        names.add(item[0])
    suffix = operation.hex
    _require(value[4] == context['schema'] and value[5] == '_cryptalis_' + suffix + '_guard',
             'guard_identity_mismatch')
    _require('_cryptalis_' + suffix + '_pause' in names, 'guard_identity_incomplete')
    return GuardInspection('GUARD_PROJECTION_SHAPE_AND_DECLARED_IDENTITY')

"""Column projection structure only; no catalog truth or operational admission."""
from dataclasses import dataclass, field

MEMBERS = frozenset(('attnum','name','type','type_schema','typmod','nullable',
    'identity','generated','collation_name','collation_schema','deterministic',
    'provider','default_digest','collation'))
STRINGS = ('name','type','type_schema','identity','generated')
OPTIONAL_STRINGS = ('collation_name','collation_schema','provider','collation')


class ColumnProjectionError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class ColumnInspection:
    classification: str = field(default='COLUMN_PROJECTION_SHAPE_ONLY', init=False)
    metadata_validated: bool = field(default=False, init=False)
    current_native_verified: bool = field(default=False, init=False)
    successor_authorized: bool = field(default=False, init=False)


def _require(condition, code):
    if not condition:
        raise ColumnProjectionError(code)


def _decimal(value):
    if type(value) is not str or not value:
        return False
    if value == '0':
        return True
    digits = value[1:] if value.startswith('-') else value
    return (bool(digits) and digits[0] in '123456789'
            and all(ch in '0123456789' for ch in digits))


def inspect_column_projection(columns):
    """No raw input conversion, catalog lookup, text sorting or input mutation."""
    _require(type(columns) is list, 'invalid_column_list')
    previous = 0
    names = set()
    for column in columns:
        _require(type(column) is dict and all(type(key) is str for key in column)
                 and column.keys() == MEMBERS, 'invalid_column_members')
        attnum = column['attnum']
        _require(type(attnum) is int and attnum > previous, 'invalid_column_order')
        previous = attnum
        _require(all(type(column[key]) is str for key in STRINGS), 'invalid_column_string')
        _require(column['name'] not in names, 'duplicate_column_name')
        names.add(column['name'])
        _require(_decimal(column['typmod']), 'invalid_column_typmod')
        _require(type(column['nullable']) is bool, 'invalid_column_nullable')
        _require(column['deterministic'] is None or type(column['deterministic']) is bool,
                 'invalid_column_deterministic')
        _require(all(column[key] is None or type(column[key]) is str for key in OPTIONAL_STRINGS),
                 'invalid_column_optional_string')
        digest = column['default_digest']
        _require(digest is None or (type(digest) is str and len(digest) == 64
                 and all(ch in '0123456789abcdef' for ch in digest)), 'invalid_column_default_digest')
        # Preserve the actual producer expression even for synthetic nullable
        # join combinations. This does not establish native join consistency.
        expected = (f"{column['collation_schema']}.{column['collation_name']}"
                    if column['collation_name'] else None)
        _require(column['collation'] == expected, 'invalid_column_collation')
    return ColumnInspection()

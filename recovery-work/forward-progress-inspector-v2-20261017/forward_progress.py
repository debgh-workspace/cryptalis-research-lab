"""Read-only local progress shape, never journal/native/authority admission."""
from dataclasses import dataclass, field
from uuid import UUID

FORMATS = frozenset((
    'cryptalis.transition/retained-native-research-v0',
    'cryptalis.transition/retained-native-comments-research-v1',
    'cryptalis.transition/retained-native-comments-cluster-research-v2',
))
CODECS = frozenset(('uuid16/v1', 'int64-be/v1'))
PHASES = frozenset(('EXPANDED', 'BACKFILLED', 'VERIFIED', 'PENDING',
                    'ACTIVE', 'DEPROTECTING', 'ABORTED'))
BASE = frozenset(('scope', 'cursor', 'rows', 'chunks', 'schema', 'guard'))


class ProgressShapeError(ValueError):
    """Fixed code only. No retained input, catalog body or operation authority."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class ProgressInspection:
    phase: str
    verification_present: bool
    classification: str = field(default='LOCAL_PROGRESS_SHAPE_ONLY', init=False)
    metadata_validated: bool = field(default=False, init=False)
    successor_authorized: bool = field(default=False, init=False)


def _require(value, code):
    if not value:
        raise ProgressShapeError(code)


def _members(value, names, code):
    _require(type(value) is dict and all(type(key) is str for key in value)
             and value.keys() == names, code)


def _uuid(value):
    if type(value) is not str or len(value) != 36:
        return False
    try:
        return str(UUID(value)) == value
    except ValueError:
        return False


def _digest(value):
    return (type(value) is str and len(value) == 64
            and all(ch in '0123456789abcdef' for ch in value))


def _cursor(value, codec):
    if codec == 'uuid16/v1':
        return _uuid(value)
    if type(value) is not str or not 1 <= len(value) <= 20:
        return False
    digits = value[1:] if value.startswith('-') else value
    if not digits or any(ch not in '0123456789' for ch in digits):
        return False
    number = int(value)
    return -(2**63) <= number <= 2**63-1 and str(number) == value


def inspect_forward_progress(context, state):
    """Validate only local progress structure; do not retain metadata references.

    context is a structural projection, not an authenticated plan. schema/guard
    and active_schema values are intentionally NOT inspected or authorized.
    No raw JSON, native membership or cross-table reachability claim is made.
    """
    _members(context, {'format', 'kind', 'models'}, 'invalid_progress_context')
    _require(type(context['format']) is str and context['format'] in FORMATS
             and type(context['kind']) is str and context['kind'] == 'protect',
             'unsupported_progress_profile')
    models = context['models']
    _require(type(models) is list and len(models) > 0, 'invalid_progress_context')
    codecs = {}
    for model in models:
        _members(model, {'table_id', 'record_codec'}, 'invalid_progress_context')
        table = model['table_id']; codec = model['record_codec']
        _require(_uuid(table), 'invalid_progress_context')
        _require(table not in codecs, 'duplicate_progress_table')
        _require(type(codec) is str and codec in CODECS, 'unsupported_record_codec')
        codecs[table] = codec
    _require(type(state) is dict and all(type(key) is str for key in state),
             'invalid_progress_state')
    phase = state.get('phase')
    _require(type(phase) is str and phase in PHASES, 'unsupported_producer_phase')
    verified = phase in ('VERIFIED', 'PENDING', 'ACTIVE', 'DEPROTECTING')
    has_verification = verified or (phase == 'ABORTED' and 'verification' in state)
    _members(state, {'phase', 'models', 'verification'} if has_verification
             else {'phase', 'models'}, 'invalid_phase_members')
    _members(state['models'], set(codecs), 'progress_table_set_mismatch')
    active = phase in ('PENDING', 'ACTIVE', 'DEPROTECTING')
    for table, codec in codecs.items():
        progress = state['models'][table]
        _members(progress, BASE | {'active_schema'} if active else BASE,
                 'invalid_model_members')
        scope = progress['scope']
        _members(scope, {'count', 'membership'}, 'invalid_scope')
        count, rows, chunks = scope['count'], progress['rows'], progress['chunks']
        _require(type(count) is int and type(rows) is int and type(chunks) is int
                 and 0 <= chunks <= rows <= count, 'invalid_progress_counters')
        _require(_digest(scope['membership']), 'invalid_membership_digest')
        if rows == 0:
            _require(chunks == 0 and progress['cursor'] is None, 'invalid_progress_cursor')
        else:
            _require(chunks > 0 and _cursor(progress['cursor'], codec), 'invalid_progress_cursor')
        if phase == 'BACKFILLED' or has_verification:
            _require(rows == count, 'incomplete_progress_phase')
    if has_verification:
        _members(state['verification'], set(codecs), 'verification_table_set_mismatch')
        _require(all(_digest(value) for value in state['verification'].values()),
                 'invalid_verification_digest')
    return ProgressInspection(phase, has_verification)

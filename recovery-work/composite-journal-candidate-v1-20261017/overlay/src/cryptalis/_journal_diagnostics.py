"""Offline decoded-state composition; never journal or recovery admission."""
from uuid import UUID
from . import _journal_progress as progress
from . import _journal_columns as columns
from . import _journal_guard as guard
from . import _journal_remaining as remaining

PROFILES = frozenset((
    'cryptalis.transition/retained-native-research-v0',
    'cryptalis.transition/retained-native-comments-research-v1',
    'cryptalis.transition/retained-native-comments-cluster-research-v2',
))
CODES = {
    'progress': frozenset('invalid_progress_context unsupported_progress_profile duplicate_progress_table unsupported_record_codec invalid_progress_state unsupported_producer_phase invalid_phase_members progress_table_set_mismatch invalid_model_members invalid_scope invalid_progress_counters invalid_membership_digest invalid_progress_cursor incomplete_progress_phase verification_table_set_mismatch invalid_verification_digest'.split()),
    'columns': frozenset('invalid_column_list invalid_column_members invalid_column_order invalid_column_string duplicate_column_name invalid_column_typmod invalid_column_nullable invalid_column_deterministic invalid_column_optional_string invalid_column_default_digest invalid_column_collation'.split()),
    'remaining': frozenset('invalid_members invalid_string invalid_boolean invalid_vector invalid_digest invalid_inventory invalid_optional_string invalid_count invalid_count_vector'.split()),
    'guard': frozenset('invalid_context_members invalid_context_string invalid_operation_id invalid_guard_shape invalid_guard_string invalid_guard_integer invalid_guard_boolean invalid_guard_config invalid_inventory invalid_trigger_shape invalid_trigger_string invalid_trigger_boolean invalid_trigger_config duplicate_trigger_identity guard_identity_mismatch guard_identity_incomplete'.split()),
}
ERRORS = {'progress': progress.ProgressShapeError, 'columns': columns.ColumnProjectionError,
          'remaining': remaining.SchemaProjectionError, 'guard': guard.GuardProjectionError}
LIMITS = (
    'State-projection shape coverage only; supplied context is not authenticated.',
    'Original comments, native designation and profile authenticity are not inspected.',
    'No current guard, catalog, ownership, transaction, cleanup or recovery authority is established.',
    'Text ordering, uniqueness, DISTINCT and native relational consistency remain unverified.',
    'Decoded ordinary input must remain stable during this synchronous call; no transport or concurrent snapshot guarantee.',
)


class JournalDiagnosticError(ValueError):
    """Only fixed code/component/status emitted by this module."""
    def __init__(self, code, component, status='REJECTED_INPUT'):
        self.code, self.component, self.status = code, component, status
        super().__init__(code)


def _require(condition, code, component='context'):
    if not condition:
        raise JournalDiagnosticError(code, component)


def _members(value, names, code, component='context'):
    _require(type(value) is dict and all(type(key) is str for key in value)
             and value.keys() == names, code, component)


def _uuid(value):
    try:
        return str(UUID(value)) == value
    except ValueError:
        return False


def _context(context):
    # Complete structural pass precedes profile-value classification.
    _members(context, {'format','kind','operation_id','models'}, 'invalid_context_members')
    _require(all(type(context[k]) is str for k in ('format','kind','operation_id')), 'invalid_context_string')
    _require(_uuid(context['operation_id']), 'invalid_operation_id')
    _require(type(context['models']) is list and len(context['models']) > 0, 'invalid_context_models')
    tables = set()
    for model in context['models']:
        _members(model, {'table_id','record_codec','schema'}, 'invalid_context_members')
        _require(all(type(model[k]) is str for k in ('table_id','record_codec','schema')), 'invalid_context_string')
        _require(_uuid(model['table_id']), 'invalid_table_id')
        _require(model['table_id'] not in tables, 'duplicate_context_table')
        tables.add(model['table_id'])
    if context['format'] not in PROFILES or context['kind'] != 'protect':
        raise JournalDiagnosticError('unsupported_diagnostic_profile','context','UNSUPPORTED_PROFILE')
    if any(model['record_codec'] not in ('uuid16/v1','int64-be/v1') for model in context['models']):
        raise JournalDiagnosticError('unsupported_record_codec','context','UNSUPPORTED_PROFILE')


def _call(component, function, *args):
    error_type = ERRORS[component]
    try:
        return function(*args)
    except error_type as error:
        if type(error) is not error_type:
            raise
        code = error.code
        safe = code if type(code) is str and code in CODES[component] else 'unsupported_diagnostic_reason'
        raise JournalDiagnosticError(safe, component) from None


def _schema(value):
    _members(value, {'relation','columns','constraints','indexes','dependencies'},
             'invalid_schema_members', 'schema')
    _call('columns', columns.inspect_column_projection, value['columns'])
    _call('remaining', remaining.inspect_remaining_schema_projection,
          {key:value[key] for key in ('relation','constraints','indexes','dependencies')})


def _inspect(context, state):
    _context(context)
    selected = {'format':context['format'], 'kind':context['kind'],
                'models':[{'table_id':model['table_id'],'record_codec':model['record_codec']}
                          for model in context['models']]}
    local = _call('progress', progress.inspect_forward_progress, selected, state)
    missing = False
    for model in context['models']:
        retained = state['models'][model['table_id']]
        _schema(retained['schema'])
        if local.phase in ('PENDING','ACTIVE','DEPROTECTING'):
            _schema(retained['active_schema'])
        observation = _call('guard', guard.inspect_guard_projection, retained['guard'],
                            {'operation_id':context['operation_id'], 'schema':model['schema']})
        missing = missing or observation.classification == 'MISSING_GUARD_OBSERVATION'
    return local.phase, local.verification_present, missing


def inspect_retained_journal(context, state):
    report = {
        'format':'cryptalis.retained-journal-diagnostic/v1',
        'status':'SHAPE_INSPECTED', 'effects':'NONE', 'authority':'ADVISORY_NOT_AUTHENTICATED',
        'complete':False, 'ready':False, 'metadata_validated':False,
        'current_native_verified':False, 'successor_authorized':False, 'text_order_verified':False,
        'phase':None, 'verification_present':None, 'guard_observation_missing':None,
        'code':None, 'component':None, 'limits':LIMITS,
    }
    try:
        phase, verified, missing = _inspect(context, state)
    except JournalDiagnosticError as error:
        report.update(status=error.status, code=error.code, component=error.component)
    else:
        report.update(phase=phase, verification_present=verified, guard_observation_missing=missing)
    return report

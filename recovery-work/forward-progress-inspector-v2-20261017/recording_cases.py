"""Non-DB integration cases for actual migration._save/_state and inspector.

Caller supplies pinned genuine modules. Facades do not authenticate plans/pins,
run SQL, emulate commit or establish native catalog/JSONB behavior.
"""
from copy import deepcopy
import json
from types import SimpleNamespace
from uuid import UUID

TABLE = '00000000-0000-0000-0000-000000000101'
OTHER = '00000000-0000-0000-0000-000000000102'
OP = UUID('00000000-0000-0000-0000-000000000201')
DIGEST = 'a' * 64
UPDATE = 'UPDATE "lab"."_cryptalis_journal" SET state=%s::jsonb WHERE operation_id=%s AND plan_digest=%s'
SELECT = 'SELECT plan_digest, state FROM "lab"."_cryptalis_journal" WHERE operation_id=%s'
EXISTS = 'SELECT pg_catalog.to_regclass(%s)'


class Quoter:
    def quote_identifier(self, value):
        if value not in ('lab', '_cryptalis_journal'):
            raise AssertionError('unexpected_identifier')
        return '"' + value + '"'


class RecordingConnection:
    def __init__(self, row=None, *, write=False, rowcount=1):
        self.dialect = SimpleNamespace(identifier_preparer=Quoter())
        self.row = row
        self.write = write
        self.rowcount = rowcount
        self.calls = []
        self.saved = None

    def exec_driver_sql(self, statement, params):
        self.calls.append((statement, params))
        if self.write and statement == UPDATE and len(self.calls) == 1:
            if params[1:] != (OP, DIGEST) or type(params[0]) is not str:
                raise AssertionError('save_identity_parameters')
            self.saved = params[0]
            return SimpleNamespace(rowcount=self.rowcount)
        if not self.write and statement == EXISTS and len(self.calls) == 1:
            if params != ('"lab"."_cryptalis_journal"',):
                raise AssertionError('journal_lookup_parameters')
            return SimpleNamespace(scalar_one=lambda: 'lab._cryptalis_journal')
        if not self.write and statement == SELECT and len(self.calls) == 2:
            if params != (OP,):
                raise AssertionError('state_identity_parameters')
            return SimpleNamespace(one_or_none=lambda: self.row)
        raise AssertionError('unexpected_recorded_sql')


def context(codec='int64-be/v1', profile='cryptalis.transition/retained-native-comments-cluster-research-v2'):
    return {'format': profile, 'kind': 'protect',
            'models': [{'table_id': TABLE, 'record_codec': codec}]}


def fixture(phase, *, rows=3, count=3, chunks=1, cursor='0', verification=None):
    # Intentionally opaque metadata surrogates. No catalog grammar claim.
    progress = {'scope': {'count': count, 'membership': 'b' * 64},
                'cursor': cursor, 'rows': rows, 'chunks': chunks,
                'schema': {'historical_expanded_metadata': True},
                'guard': ['historical_guard_metadata']}
    state = {'phase': phase, 'models': {TABLE: progress}}
    if phase in ('PENDING', 'ACTIVE', 'DEPROTECTING'):
        progress['active_schema'] = {'phase_specific_metadata': phase}
    if verification is True or (verification is None and phase in ('VERIFIED', 'PENDING', 'ACTIVE', 'DEPROTECTING')):
        state['verification'] = {TABLE: 'c' * 64}
    return state


def run_cases(migration, inspector):
    records = []
    p = SimpleNamespace(operation_id=OP, digest=DIGEST, document={'journal_schema': 'lab'})

    def check(label, callback):
        try:
            callback()
        except Exception:
            records.append({'id': label, 'status': 'FAIL', 'failure': 'case_assertion_or_exception'})
        else:
            records.append({'id': label, 'status': 'PASS'})

    def save(state):
        before = deepcopy(state)
        connection = RecordingConnection(write=True)
        migration._save(connection, p, state)
        assert state == before and len(connection.calls) == 1
        decoded = json.loads(connection.saved)
        assert decoded == before
        return decoded

    def inspect_positive(ctx, state, *, readback=True):
        saved = save(state)
        original = deepcopy((ctx, saved))
        if readback:
            phase = state['phase']
            pin = SimpleNamespace(phase='ACTIVE' if phase == 'ACTIVE' else 'PREPARED')
            connection = RecordingConnection((DIGEST, saved))
            observed = migration._state(connection, p, pin, allow_aborted=phase == 'ABORTED')
            assert observed is saved and len(connection.calls) == 2
        else:
            observed = saved
        result = inspector.inspect_forward_progress(ctx, observed)
        assert type(result) is inspector.ProgressInspection
        assert result.phase == state['phase'] and result.verification_present == ('verification' in state)
        assert result.classification == 'LOCAL_PROGRESS_SHAPE_ONLY'
        assert result.metadata_validated is False and result.successor_authorized is False
        assert not hasattr(result, '__dict__')
        try:
            result.phase = 'ACTIVE'
        except (AttributeError, TypeError):
            pass
        else:
            raise AssertionError('mutable_inspection')
        assert (ctx, saved) == original
        # No retained mutable input reference: mutation after return cannot alter
        # any declared scalar result. The validated state itself was not changed.
        ctx['models'].clear()
        saved['models'].clear()
        assert result.phase == state['phase'] and result.metadata_validated is False

    positive = [
        ('expanded_initial', fixture('EXPANDED', rows=0, chunks=0, cursor=None)),
        ('expanded_partial', fixture('EXPANDED', rows=2, cursor='-7')),
        ('expanded_complete_before_next_pass', fixture('EXPANDED')),
        ('backfilled', fixture('BACKFILLED')),
        ('verified', fixture('VERIFIED')),
        ('pending', fixture('PENDING')),
        ('active', fixture('ACTIVE')),
        ('aborted_partial', fixture('ABORTED', rows=2, cursor='-7')),
        ('aborted_complete_no_verification', fixture('ABORTED')),
        ('aborted_verified', fixture('ABORTED', verification=True)),
        ('empty_verified', fixture('VERIFIED', count=0, rows=0, chunks=0, cursor=None)),
        ('above_artifact_integer', fixture('BACKFILLED', count=2**53+17, rows=2**53+17, chunks=2**53+17)),
        ('int64_min_cursor', fixture('BACKFILLED', cursor=str(-(2**63)))),
        ('int64_max_cursor', fixture('BACKFILLED', cursor=str(2**63-1))),
    ]
    for label, state in positive:
        check('roundtrip:' + label, lambda state=state: inspect_positive(context(), state))
    check('serializer_only:deprotecting', lambda: inspect_positive(context(), fixture('DEPROTECTING'), readback=False))
    check('roundtrip:uuid_cursor', lambda: inspect_positive(context('uuid16/v1'), fixture('BACKFILLED', cursor=OTHER)))
    expected_profiles = (
        'cryptalis.transition/retained-native-research-v0',
        'cryptalis.transition/retained-native-comments-research-v1',
        'cryptalis.transition/retained-native-comments-cluster-research-v2',
    )
    def fixed_profiles():
        assert inspector.FORMATS == frozenset(expected_profiles)
    check('contract:exact_literal_profiles', fixed_profiles)
    for profile in expected_profiles:
        check('profile:' + profile, lambda profile=profile: inspect_positive(context(profile=profile), fixture('ABORTED')))

    def rejected(ctx, state, code):
        before = deepcopy((ctx, state))
        try:
            inspector.inspect_forward_progress(ctx, state)
        except inspector.ProgressShapeError as error:
            assert type(error) is inspector.ProgressShapeError
            assert error.code == code and error.args == (code,)
        else:
            raise AssertionError('mutation_not_rejected')
        assert (ctx, state) == before

    mutations = []
    def mutation(label, change, code, *, ctx=None, state=None):
        c = context() if ctx is None else ctx
        s = fixture('VERIFIED') if state is None else state
        change(c, s)
        mutations.append((label, c, s, code))
    for name, value in [('bool', True), ('float', 1.0), ('text', '1'), ('negative', -1)]:
        mutation('counter_' + name, lambda c,s,value=value: s['models'][TABLE].__setitem__('rows', value), 'invalid_progress_counters')
    mutation('chunks_over_rows', lambda c,s: s['models'][TABLE].__setitem__('chunks', 4), 'invalid_progress_counters')
    mutation('rows_over_scope', lambda c,s: s['models'][TABLE].__setitem__('rows', 4), 'invalid_progress_counters')
    mutation('incomplete_verified', lambda c,s: s['models'][TABLE].__setitem__('rows', 2), 'incomplete_progress_phase')
    for name, value in [('none',None),('plus','+1'),('leading_zero','01'),('negative_zero','-0'),('overflow',str(2**63)),('wrong_codec',OTHER)]:
        mutation('cursor_' + name, lambda c,s,value=value: s['models'][TABLE].__setitem__('cursor', value), 'invalid_progress_cursor')
    mutation('zero_with_cursor', lambda c,s: None, 'invalid_progress_cursor', state=fixture('EXPANDED', rows=0, chunks=0, cursor='0'))
    mutation('positive_without_chunk', lambda c,s: s['models'][TABLE].__setitem__('chunks', 0), 'invalid_progress_cursor')
    mutation('missing_table', lambda c,s: s['models'].clear(), 'progress_table_set_mismatch')
    mutation('extra_table', lambda c,s: s['models'].__setitem__(OTHER, deepcopy(s['models'][TABLE])), 'progress_table_set_mismatch')
    mutation('duplicate_context_table', lambda c,s: c['models'].append(dict(c['models'][0])), 'duplicate_progress_table')
    mutation('unknown_format', lambda c,s: c.__setitem__('format', 'cryptalis.transition/future-v3'), 'unsupported_progress_profile')
    mutation('reverse_kind', lambda c,s: c.__setitem__('kind', 'deprotect'), 'unsupported_progress_profile')
    mutation('wrong_codec_context', lambda c,s: c['models'][0].__setitem__('record_codec','text'), 'unsupported_record_codec')
    mutation('extra_context_member', lambda c,s: c.__setitem__('authenticated',True), 'invalid_progress_context')
    mutation('durable_prepared', lambda c,s: s.__setitem__('phase','PREPARED'), 'unsupported_producer_phase')
    mutation('reverse_state_member', lambda c,s: s.__setitem__('layout_version',101), 'invalid_phase_members')
    mutation('missing_verification', lambda c,s: s.pop('verification'), 'invalid_phase_members')
    mutation('extra_verification_table', lambda c,s: s['verification'].__setitem__(OTHER,'c'*64), 'verification_table_set_mismatch')
    mutation('bad_verification_digest', lambda c,s: s['verification'].__setitem__(TABLE,'G'*64), 'invalid_verification_digest')
    mutation('bad_membership_digest', lambda c,s: s['models'][TABLE]['scope'].__setitem__('membership','G'*64), 'invalid_membership_digest')
    mutation('extra_model_member', lambda c,s: s['models'][TABLE].__setitem__('abort_from','VERIFIED'), 'invalid_model_members')
    mutation('aborted_with_active_schema', lambda c,s: s['models'][TABLE].__setitem__('active_schema',{}), 'invalid_model_members', state=fixture('ABORTED'))
    mutation('incomplete_aborted_verified', lambda c,s: s['models'][TABLE].__setitem__('rows',2), 'incomplete_progress_phase', state=fixture('ABORTED',verification=True))
    class DictSubclass(dict): pass
    class ListSubclass(list): pass
    class IntSubclass(int): pass
    class StrSubclass(str): pass
    mutation('dict_subclass_state', lambda c,s: None, 'invalid_progress_state', state=DictSubclass(fixture('VERIFIED')))
    mutation('dict_subclass_context', lambda c,s: None, 'invalid_progress_context', ctx=DictSubclass(context()))
    mutation('list_subclass_models', lambda c,s: c.__setitem__('models',ListSubclass(c['models'])), 'invalid_progress_context')
    mutation('int_subclass_count', lambda c,s: s['models'][TABLE]['scope'].__setitem__('count',IntSubclass(3)), 'invalid_progress_counters')
    mutation('str_subclass_format', lambda c,s: c.__setitem__('format',StrSubclass(c['format'])), 'unsupported_progress_profile')
    mutation('tuple_models_context', lambda c,s: c.__setitem__('models',tuple(c['models'])), 'invalid_progress_context')
    mutation('bool_count', lambda c,s: s['models'][TABLE]['scope'].__setitem__('count',True), 'invalid_progress_counters')
    mutation('bool_chunks', lambda c,s: s['models'][TABLE].__setitem__('chunks',True), 'invalid_progress_counters')
    mutation('noncanonical_uuid_cursor', lambda c,s: None, 'invalid_progress_cursor', ctx=context('uuid16/v1'), state=fixture('VERIFIED',cursor='AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA'))
    for label, ctx, state, code in mutations:
        check('reject:' + label, lambda ctx=ctx,state=state,code=code: rejected(ctx,state,code))

    def state_refusal(state, pin_phase, code, *, allow=False, absent=False):
        row = None if absent else (DIGEST, save(state))
        connection = RecordingConnection(row)
        try:
            migration._state(connection,p,SimpleNamespace(phase=pin_phase),allow_aborted=allow)
        except migration.TransitionFailure as error:
            assert type(error) is migration.TransitionFailure and error.code == code
        else:
            raise AssertionError('existing_refusal_weakened')
        assert len(connection.calls) == 2
    for label,state,pin,code,allow,absent in [
        ('missing_successor_id',fixture('ABORTED'),'PREPARED','journal_identity_mismatch',False,True),
        ('aborted_default',fixture('ABORTED'),'PREPARED','operation_aborted',False,False),
        ('aborted_wrong_pin',fixture('ABORTED'),'VERIFIED','operation_aborted',True,False),
        ('active_stale_pin',fixture('ACTIVE'),'PREPARED','external_policy_behind_database',False,False),
        ('deprotecting_forward_read',fixture('DEPROTECTING'),'PREPARED','restored_state_behind_external_pin',False,False),
        ('behind_pin',fixture('EXPANDED'),'VERIFIED','restored_state_behind_external_pin',False,False),
    ]:
        check('state_refusal:' + label, lambda state=state,pin=pin,code=code,allow=allow,absent=absent: state_refusal(state,pin,code,allow=allow,absent=absent))
    def save_rowcount_refusal(rowcount):
        state = fixture('ABORTED', verification=True)
        before = deepcopy(state)
        connection = RecordingConnection(write=True, rowcount=rowcount)
        try:
            migration._save(connection, p, state)
        except migration.TransitionFailure as error:
            assert type(error) is migration.TransitionFailure
            assert error.code == 'journal_marker_write_failed' and error.operation_id == OP
        else:
            raise AssertionError('save_rowcount_not_rejected')
        assert state == before and len(connection.calls) == 1
        assert json.loads(connection.saved) == before
    check('save_refusal:zero_rows', lambda: save_rowcount_refusal(0))
    check('save_refusal:multiple_rows', lambda: save_rowcount_refusal(2))
    assert len(records) == 68 and len({r['id'] for r in records}) == 68
    return records

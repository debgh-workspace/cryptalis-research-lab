"""Pure maintenance-entry budget checks, not database/lifecycle qualification.

Structural artifacts below are not compiled deployment plans. A compiler-entry
sentinel stops accepted budgets before lock validation or any database work.
Rejected budgets must stop before that sentinel and the reverse consent check.
"""
import json
from uuid import UUID

import pytest

from cryptalis import deprotection as d
from cryptalis import migration as m


TARGET = UUID(int=1)
SOURCE = UUID(int=2)
REVERSE = UUID(int=3)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def plans():
    source_doc = {
        'format': 'cryptalis.transition/retained-native-research-v0',
        'kind': 'protect', 'operation_id': str(SOURCE), 'target_id': str(TARGET),
        'lock': {'models': []}, 'target': ['synthetic-target'],
        'runtime_role': 'synthetic-runtime', 'journal_schema': 'synthetic-schema',
        'estimates': {'writer_pause_seconds_estimate': 10},
    }
    source = m.MigrationPlan(canonical(source_doc))
    active_pin = {
        'target_id': str(TARGET), 'operation_id': str(SOURCE),
        'plan_digest': source.digest, 'phase': 'ACTIVE',
    }
    reverse_doc = {
        'format': 'cryptalis.reverse/retained-native-research-v0',
        'kind': 'deprotect', 'operation_id': str(REVERSE), 'target_id': str(TARGET),
        'source_plan': source_doc, 'source_pin': active_pin,
        'lock': source_doc['lock'], 'target': source_doc['target'],
        'runtime_role': source_doc['runtime_role'],
        'journal_schema': source_doc['journal_schema'],
        'key_policies': {}, 'active_schemas': {}, 'retirable_aborted': [],
        'estimates': {'writer_pause_seconds_estimate': 10,
                      'backfill_rows_per_second': 1, 'verify_rows_per_second': 1},
        'plaintext_runtime_role': 'synthetic-plaintext', 'cutover_readiness': {},
    }
    return source, d.DeprotectionPlan(canonical(reverse_doc))


class CompilerBoundaryReached(RuntimeError):
    pass


class NoConnection:
    def __init__(self, effects):
        self.effects = effects

    def connect(self):
        self.effects.append('connect')
        raise AssertionError('Database connection forbidden in pure budget checks')


def invoke(operation, source, reverse, engine, approval, keys, consent):
    if operation.startswith('protect_'):
        pin = m.DeploymentPin(TARGET, SOURCE, source.digest, 'PREPARED')
        options = {'pin': pin, 'approval': approval}
        if operation != 'protect_abort':
            options['keys'] = keys
        return getattr(m, operation.removeprefix('protect_'))(source, engine, **options)
    phase = 'REMOVING' if operation == 'reverse_remove' else 'PREPARED'
    pin = m.DeploymentPin(TARGET, REVERSE, reverse.digest, phase)
    options = {'pin': pin, 'approval': approval, 'plaintext_approval': consent}
    if operation == 'reverse_apply':
        options['keys'] = keys
    if operation == 'reverse_remove':
        options['removal_approval'] = d.RemovalApproval(
            reverse.digest, 'Synthetic workload attestation',
            'Synthetic backup attestation', True)
    return getattr(d, operation.removeprefix('reverse_'))(reverse, engine, **options)


class IntSubclass(int):
    pass


class FloatSubclass(float):
    pass


BUDGETS = [
    pytest.param(10**400, True, id='huge-positive-int'),
    pytest.param(-(10**400), False, id='huge-negative-int'),
    pytest.param(2**53 - 1, True, id='exact-large-int'),
    pytest.param(2**53 + 1, True, id='beyond-exact-float-int'),
    pytest.param(10, True, id='equal-int'),
    pytest.param(9, False, id='below-int'),
    pytest.param(11, True, id='above-int'),
    pytest.param(10.0, True, id='equal-float'),
    pytest.param(9.999999999999998, False, id='adjacent-below-float'),
    pytest.param(10.000000000000002, True, id='adjacent-above-float'),
    pytest.param(float.fromhex('0x1.fffffffffffffp+1023'), True, id='largest-finite-float'),
    pytest.param(5e-324, False, id='positive-subnormal-float'),
    pytest.param(0, False, id='zero'),
    pytest.param(-1.0, False, id='negative-float'),
    pytest.param(True, False, id='bool'),
    pytest.param(float('inf'), False, id='positive-infinity'),
    pytest.param(float('-inf'), False, id='negative-infinity'),
    pytest.param(float('nan'), False, id='nan'),
    pytest.param('10', False, id='string'),
    pytest.param(None, False, id='none'),
    pytest.param(IntSubclass(10), False, id='integer-subclass'),
    pytest.param(FloatSubclass(10), False, id='float-subclass'),
]


@pytest.mark.parametrize('operation', [
    'protect_apply', 'protect_verify', 'protect_abort',
    'reverse_apply', 'reverse_abort', 'reverse_remove',
])
@pytest.mark.parametrize('budget,accepted', BUDGETS)
def test_maintenance_budget_public_boundary(monkeypatch, operation, budget, accepted):
    source, reverse = plans()
    effects = []
    engine = NoConnection(effects)
    approval = m.MaintenanceApproval('Synthetic writer exclusion', budget)
    consent = d.PlaintextApproval(TARGET, REVERSE, reverse.digest, True,
                                 'Synthetic retained backup evidence')
    stop = CompilerBoundaryReached('Accepted budget reached compiler boundary')

    def compiler_boundary(*args, **kwargs):
        effects.append('compiler')
        raise stop

    def keys(*args, **kwargs):
        effects.append('provider')
        raise AssertionError('Provider use forbidden in pure budget checks')

    original_consent = d._consent

    def observed_consent(*args, **kwargs):
        effects.append('consent')
        return original_consent(*args, **kwargs)

    monkeypatch.setattr(m, '_previous_lock', compiler_boundary)
    monkeypatch.setattr(d, '_previous_lock', compiler_boundary)
    monkeypatch.setattr(d, '_consent', observed_consent)
    if accepted:
        with pytest.raises(CompilerBoundaryReached) as caught:
            invoke(operation, source, reverse, engine, approval, keys, consent)
        assert caught.value is stop
        assert effects == (['consent', 'compiler'] if operation.startswith('reverse_') else ['compiler'])
    else:
        with pytest.raises(m.TransitionFailure) as caught:
            invoke(operation, source, reverse, engine, approval, keys, consent)
        assert caught.value.code == 'writer_exclusion_or_pause_not_approved'
        assert caught.value.operation_id == (SOURCE if operation.startswith('protect_') else REVERSE)
        assert caught.value.__cause__ is None
        assert effects == []

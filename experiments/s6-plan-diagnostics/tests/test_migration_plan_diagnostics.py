"""Public artifact rejection remains typed and does not echo artifact data."""
import json
import traceback

import pytest

from cryptalis.migration import MigrationPlan, TransitionFailure


def artifact(**changes):
    value = {
        'format': 'cryptalis.transition/retained-native-research-v0',
        'kind': 'protect',
        'operation_id': '00000000-0000-0000-0000-000000000001',
        'target_id': '00000000-0000-0000-0000-000000000002',
    }
    value.update(changes)
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


@pytest.mark.parametrize('raw', [
    b'{',
    b'[]',
    b'{"format":"a","format":"b"}',
    artifact(operation_id='PRIVATE_ARTIFACT_SENTINEL'),
    artifact(operation_id=None),
    artifact(operation_id=7),
    artifact(target_id=[]),
    artifact().replace(b',"target_id":"00000000-0000-0000-0000-000000000002"', b''),
    artifact(format='cryptalis.transition/v1'),
    artifact(operation_id='00000000-0000-0000-0000-000000000000'),
])
def test_invalid_protection_artifact_has_safe_typed_failure(raw):
    with pytest.raises(TransitionFailure) as failure:
        MigrationPlan(raw)
    assert failure.value.code == 'invalid_plan'
    assert 'PRIVATE_ARTIFACT_SENTINEL' not in str(failure.value)
    rendered = ''.join(traceback.format_exception_only(type(failure.value), failure.value))
    assert 'PRIVATE_ARTIFACT_SENTINEL' not in rendered
    assert failure.value.operation_id is None

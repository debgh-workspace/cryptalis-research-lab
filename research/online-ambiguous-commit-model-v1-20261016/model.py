"""Synthetic claim-observation model only; no database or execution authority.

Evidence booleans are MODEL ASSUMPTIONS, not mechanisms that establish them.
A future adapter needs independent proof before assigning any of them True.
No result permits a retry, publication, cutover, worker admission or closure.
"""

FIELDS = frozenset({
    'expected_operation', 'observed_operation', 'expected_key', 'observed_key',
    'expected_attempt', 'observed_attempt', 'claim_token', 'dirty_token',
    'staged_token', 'stage_matches_claim', 'identity_verified',
    'original_transaction_terminal_verified', 'coherent_committed_observation',
    'pin_matches', 'phase',
})


def classify(evidence):
    def result(outcome):
        return {'outcome': outcome, 'retry_authorized': False,
                'closure_established': False, 'publication_authorized': False}

    if type(evidence) is not dict or set(evidence) != FIELDS:
        return result('UNKNOWN_INVALID_EVIDENCE')
    e = evidence
    for field in ('identity_verified', 'original_transaction_terminal_verified',
                  'coherent_committed_observation', 'pin_matches'):
        if type(e[field]) is not bool:
            return result('UNKNOWN_INVALID_EVIDENCE')
    for field in ('expected_operation', 'observed_operation',
                  'expected_attempt', 'observed_attempt', 'phase'):
        if type(e[field]) is not str or not e[field]:
            return result('UNKNOWN_INVALID_EVIDENCE')
    for field in ('expected_key', 'observed_key', 'claim_token'):
        if type(e[field]) is not int:
            return result('UNKNOWN_INVALID_EVIDENCE')
    if e['claim_token'] <= 0:
        return result('UNKNOWN_INVALID_EVIDENCE')
    for field in ('dirty_token', 'staged_token'):
        if e[field] is not None and (type(e[field]) is not int or e[field] <= 0):
            return result('UNKNOWN_INVALID_EVIDENCE')
    if e['stage_matches_claim'] is not None and type(e['stage_matches_claim']) is not bool:
        return result('UNKNOWN_INVALID_EVIDENCE')
    if ((e['staged_token'] is None) != (e['stage_matches_claim'] is None)):
        return result('UNKNOWN_INVALID_EVIDENCE')
    if not e['identity_verified'] or any(e['expected_' + name] != e['observed_' + name]
                                        for name in ('operation', 'key', 'attempt')):
        return result('UNKNOWN_IDENTITY')
    if not e['pin_matches'] or e['phase'] != 'PREPARING':
        return result('BLOCKED_PIN_OR_PHASE')
    # The same dirty token may still be visible while the original installer is
    # uncommitted. Absence may reflect other work. Neither observation resolves it.
    if not e['original_transaction_terminal_verified']:
        return result('UNKNOWN_ORIGINAL_TRANSACTION')
    if not e['coherent_committed_observation']:
        return result('UNKNOWN_OBSERVATION')

    claim = e['claim_token']
    dirty = e['dirty_token']
    stage = e['staged_token']
    if stage == claim:
        if e['stage_matches_claim'] is not True or dirty == claim:
            return result('HOLD_CONFLICTING_EVIDENCE')
        if dirty is None:
            return result('CLAIM_EFFECT_OBSERVED')
        return result('CLAIM_EFFECT_OBSERVED_OTHER_OBLIGATION')
    if dirty == claim:
        return result('ORIGINAL_OBLIGATION_OBSERVED')
    if dirty is not None:
        # No numerical ordering or global capture-token monotonicity assumption.
        return result('DIFFERENT_OBLIGATION_OBSERVED')
    return result('UNKNOWN_NO_MATCHING_EFFECT_OR_OBLIGATION')

"""Finite stdlib-only model driver. Not run during preparation."""
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / 'model.py'
CASES = ROOT / 'CASES.json'
# Reads only the separately reviewed new model and public synthetic case file.
model_bytes = MODEL.read_bytes()
case_bytes = CASES.read_bytes()
cases = json.loads(case_bytes)
classify = runpy.run_path(str(MODEL))['classify']
results = []
failures = []
for case in cases:
    actual = classify(case['evidence'])
    ok = (actual['outcome'] == case['expected'] and
          actual['retry_authorized'] is False and
          actual['closure_established'] is False and
          actual['publication_authorized'] is False)
    results.append({'id': case['id'], 'expected': case['expected'],
                    'actual': actual, 'pass': ok})
    if not ok:
        failures.append(case['id'])
# Two fixed counterfeit conclusions represent the precise unsafe alternatives.
# These are negative-oracle controls, not execution of altered product code.
by_id = {case['id']: case for case in cases}
negative_controls = [
    {'id': 'empty_queue_means_success', 'case': 'empty_without_stage',
     'counterfeit_outcome': 'CLAIM_EFFECT_OBSERVED'},
    {'id': 'dirty_token_means_transaction_finished', 'case': 'unresolved_original_dirty',
     'counterfeit_outcome': 'ORIGINAL_OBLIGATION_OBSERVED'},
]
for control in negative_controls:
    actual = classify(by_id[control['case']]['evidence'])['outcome']
    control['rejected'] = actual != control['counterfeit_outcome']
    if not control['rejected']:
        failures.append(control['id'])
unchanged = MODEL.read_bytes() == model_bytes and CASES.read_bytes() == case_bytes
if not unchanged:
    failures.append('input_changed')
print(json.dumps({'scope': 'synthetic deterministic observations; no native execution or authority',
                  'model_sha256': hashlib.sha256(model_bytes).hexdigest(),
                  'cases_sha256': hashlib.sha256(case_bytes).hexdigest(),
                  'case_count': len(cases), 'results': results,
                  'negative_controls': negative_controls,
                  'inputs_unchanged': unchanged, 'failures': failures}, indent=2))
sys.exit(1 if failures else 0)

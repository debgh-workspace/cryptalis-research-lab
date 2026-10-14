"""Run the four selected correction cells once; verify exact negative cause."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).parent.absolute()
if sys.executable!=str(ROOT.parent/'repo/.venv/bin/python'):raise RuntimeError('Pinned executable required')
manifest=json.loads((ROOT/'cases.json').read_text());ids=[c['id'] for c in manifest['cases']]
summary=[]
for optimize in (0,1):
    for mode in ('positive','negative'):
        name=f'{mode}-o{optimize}-01.json';flags=['-O'] if optimize else []
        cmd=[sys.executable,'-B',*flags,str(ROOT/'launch.py'),mode,name]
        try:
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=60,
                env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        except subprocess.TimeoutExpired as exc:
            with (ROOT/'evidence'/f'launch-{mode}-o{optimize}-01.json').open('x') as out:
                json.dump({'command':cmd,'status':'TIMEOUT','stdout':str(exc.stdout),'stderr':str(exc.stderr)},out,indent=2)
            raise
        entry={'command':cmd,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,
            'expected_exit':0 if mode=='positive' else 1}
        receipt_path=ROOT/'evidence'/name
        if receipt_path.exists():entry['receipt_sha256']=hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        with (ROOT/'evidence'/f'launch-{mode}-o{optimize}-01.json').open('x') as out:json.dump(entry,out,indent=2);out.write('\n')
        receipt=json.loads(receipt_path.read_text())
        if receipt['optimize']!=optimize:raise RuntimeError('Wrong optimization mode')
        if mode=='positive':
            if proc.returncode!=0 or receipt['status']!='PASS' or receipt['passed']!=ids:
                raise RuntimeError('Correction positive check failed')
            if len(receipt['observations'])!=43:raise RuntimeError('Missing exact observations')
            for observation,case in zip(receipt['observations'],manifest['cases']):
                if observation['id']!=case['id'] or observation['actual']!=case['expected'] or observation['native_calls']!=case['native_calls']:
                    raise RuntimeError('Correction observation disagreement')
        else:
            if (proc.returncode!=1 or receipt['status']!='FAIL' or receipt['passed'] or
                receipt.get('error_type')!='RuntimeError' or receipt.get('error')!=manifest['negative']['expected_error'] or
                receipt['observations']!=[{'id':'actual-output-perturbation','native_calls':1,
                    'original_verified':True,'perturbation_applied_to_actual_return':True,'comparison_expected':'reject'}]):
                raise RuntimeError('Actual-output negative failed for the wrong reason')
        summary.append({'mode':mode,'optimize':optimize,'expected_outcome_verified':True,'receipt':name,
                        'passed_count':len(receipt['passed']),'receipt_sha256':entry['receipt_sha256']})
with (ROOT/'evidence/run-summary-01.json').open('x') as out:
    json.dump({'status':'PASS','scope':'43 new cases and one actual-output negative, each O0/O1; full DESIGN HOLD','runs':summary},out,indent=2);out.write('\n')
print(json.dumps({'status':'PASS','positive_cases_per_mode':43,'actual_negative_modes':[0,1],'no_old_tests_rerun':True}))

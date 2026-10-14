"""Frozen finite full-wrapper launch plan. Await separate execution clearance."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
R=Path(__file__).parent.absolute()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
    with p.open('x') as out:json.dump(v,out,indent=2);out.write('\n')
name=sys.argv[1]
if Path(name).name!=name:raise RuntimeError('Invalid output name')
freeze=json.loads((R/'FULL_RUN_FREEZE_V2.json').read_text())
if sys.executable!=str(R.parent/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14):raise RuntimeError('Wrong launcher Python')
if any(k in os.environ for k in freeze['reject_environment']):raise RuntimeError('Environment override')
for n,h in freeze['pins'].items():
    if sha(n)!=h:raise RuntimeError('Pinned input changed')
out=R/name;out.mkdir();records=[]
for optimize in (0,1):
    for mode in freeze['modes']:
        target=out/f'{mode}-o{optimize}.json'
        cmd=[sys.executable,'-I','-B']+(['-O'] if optimize else [])+[str(R/'full_run_cached.py'),mode,str(target.relative_to(R))]
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        except subprocess.TimeoutExpired as exc:
            save(out/f'{mode}-o{optimize}-timeout.json',{'command':cmd,'timeout':180,'stdout':str(exc.stdout),'stderr':str(exc.stderr)})
            raise
        cache=Path(str(target)+'-cache-check.json')
        record={'cache_sha256':sha(cache) if cache.exists() else None,'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result_sha256':sha(target) if target.exists() else None}
        save(out/f'{mode}-o{optimize}-launch.json',record);records.append(record)
        if not target.exists() or not cache.exists():raise RuntimeError('Missing result/cache receipt')
        cache_result=json.loads(cache.read_text())
        if cache_result.get('status')!='PASS' or cache_result.get('before')!='PASS' or cache_result.get('after')!='PASS' or cache_result.get('freeze_sha256')!=sha(R/'FULL_RUN_FREEZE_V2.json'):raise RuntimeError('Cache provenance failure')
        r=json.loads(target.read_text())
        if mode=='positive':
            if p.returncode!=0 or p.stdout or p.stderr or r['status']!='PASS' or len(r['observations'])!=1098:raise RuntimeError('Positive failure')
        else:
            n=r.get('negative');control=next(c for c in json.loads((R/'FULL_HOOKS.json').read_text())['negatives'] if c['mode']==mode)
            if p.returncode!=1 or p.stdout or r['status']!='FAIL' or r.get('error_type')!='RuntimeError' or r.get('error')!='Exact admission mismatch' or not n or not n.get('original_verified') or n['case_id']!=control['case_id'] or r['observations'] or not p.stderr.rstrip().endswith('RuntimeError: Exact admission mismatch'):
                raise RuntimeError('Unexpected negative signature')
        for n,h in freeze['pins'].items():
            if sha(n)!=h:raise RuntimeError('Post-child pin mismatch')
save(out/'launches.json',records)

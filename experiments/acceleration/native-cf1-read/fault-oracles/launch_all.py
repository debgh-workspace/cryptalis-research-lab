"""Bounded launch driver; exact expected negative failures, no timing."""
import hashlib,json,os,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent
launches=[]
for optimize in (0,1):
    for mode in ('stage','trace','positive'):
        name=f'{mode}-o{optimize}.json';args=[str(B/'repo/.venv/bin/python')]+(['-O'] if optimize else [])+[str(R/'run.py'),mode,name]
        p=subprocess.run(args,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
        receipt=json.loads((R/name).read_text())
        record={'command':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'receipt':name,'receipt_sha256':hashlib.sha256((R/name).read_bytes()).hexdigest()}
        launches.append(record)
        if mode=='positive':
            if p.returncode!=0 or receipt['status']!='PASS' or p.stderr:raise RuntimeError('Positive failed '+name)
        elif p.returncode!=1 or receipt.get('error')!='Exact fault oracle mismatch' or receipt.get('error_type')!='RuntimeError' or not receipt['observations'][-1].get('original_verified'):raise RuntimeError('Wrong negative failure '+name)
with (R/'LAUNCHES.json').open('x') as f:json.dump(launches,f,indent=2);f.write('\n')
print('PASS: two positive launches; four intended metadata/trace refusals')

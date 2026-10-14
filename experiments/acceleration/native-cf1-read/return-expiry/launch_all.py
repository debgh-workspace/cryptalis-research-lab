"""Finite launches, negatives before positive receipts; bounded cleanup."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).absolute().parent
records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for optimize in (0,1):
    for mode in ('metadata','trace','positive'):
        name=f'{mode}-o{optimize}-01';result_path=R/'evidence'/(name+'.json')
        cmd=[sys.executable,'-B']+(['-O'] if optimize else [])+[str(R/'run.py'),mode,str(result_path.relative_to(R))]
        try:p=subprocess.run(cmd,capture_output=True,text=True,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        except subprocess.TimeoutExpired as exc:
            failure={'command':cmd,'timeout':180,'stdout':str(exc.stdout),'stderr':str(exc.stderr)}
            with (R/'evidence'/(name+'-timeout.json')).open('x') as out:json.dump(failure,out,indent=2)
            raise
        record={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result_sha256':sha(result_path) if result_path.exists() else None}
        with (R/'evidence'/(name+'-launch.json')).open('x') as out:json.dump(record,out,indent=2);out.write('\n')
        records.append(record)
        if not result_path.exists():raise RuntimeError('Missing result receipt')
        result=json.loads(result_path.read_text())
        if p.stdout:raise RuntimeError('Unexpected stdout')
        if mode=='positive':
            if p.returncode or p.stderr or result['status']!='PASS':raise RuntimeError('Positive admission failure')
        else:
            n=result.get('negative')
            if p.returncode!=1 or result['status']!='FAIL' or result.get('error_type')!='RuntimeError' or result.get('error')!='Exact return-expiry mismatch' or not n or not n.get('original_verified') or result['observations'] or not p.stderr.rstrip().endswith('RuntimeError: Exact return-expiry mismatch'):
                raise RuntimeError('Wrong negative failure signature')
        print(json.dumps({'mode':mode,'optimize':optimize,'expected_result_verified':True,'observations':len(result['observations'])}),flush=True)
with (R/'LAUNCHES.json').open('x') as out:json.dump(records,out,indent=2);out.write('\n')

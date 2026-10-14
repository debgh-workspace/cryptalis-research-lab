"""Bounded negative-before-positive O0/O1 driver; preserve each process result."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).absolute().parent;PY=str(R.parent/'repo/.venv/bin/python')
def write(p,v):
    with p.open('x') as f: json.dump(v,f,indent=2);f.write('\n')
results=[]
for mode in ['wrong-hkdf','wrong-intermediate','positive']:
    for opt in [0,1]:
        name=f'{mode}-o{opt}-01.json';cmd=[PY,'-B',*(['-O'] if opt else []),str(R/'check.py'),mode,name]
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
        p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
        record={'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        write(R/('launch-'+name),record)
        if not (R/name).is_file(): raise RuntimeError('Missing process receipt; preserved launcher')
        r=json.loads((R/name).read_text())
        if mode=='positive':
            if p.returncode!=0 or r['status']!='PASS' or len(r['observations'])!=14: raise RuntimeError('Positive failed')
        elif not (p.returncode==1 and r['status']=='FAIL' and r['exception']=='RuntimeError' and r['message']=='Exact oracle mismatch' and r.get('original_verified') is True and r['observations']==[]): raise RuntimeError('Wrong negative failure')
        if p.stderr: raise RuntimeError('Unexpected process stderr')
        results.append({'mode':mode,'optimize':opt,'returncode':p.returncode,'receipt':name})
a=json.loads((R/'positive-o0-01.json').read_text());b=json.loads((R/'positive-o1-01.json').read_text())
if a['observations']!=b['observations']: raise RuntimeError('Optimization divergence')
for path,d in json.loads((R/'ORIGINALS.json').read_text()).items():
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=d: raise RuntimeError('Original changed')
write(R/'SUMMARY.json',{'status':'BOUNDED_PASS','results':results,'original_inventory_unchanged':True,'identical_positive_records':True,'full_design_admission':'HOLD','timing':'NOT RUN'})
print('14 exact oracle entries PASS at O0/O1; four negative process failures retained; originals unchanged')

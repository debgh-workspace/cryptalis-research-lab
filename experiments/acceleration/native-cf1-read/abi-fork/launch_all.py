import json,os,signal,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent;results=[]
for opt in (0,1):
 for mode in ('abi','fork','positive'):
  name=f'r2-o{opt}-{mode}.json';cmd=[str(B/'repo/.venv/bin/python'),'-B']+(['-O'] if opt else [])+[str(R/'run.py'),name]+([] if mode=='positive' else [mode])
  p=subprocess.Popen(cmd,start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  try:out,err=p.communicate(timeout=60)
  except subprocess.TimeoutExpired:
   os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate();raise RuntimeError('Owned process group timed out')
  # Also kill any surviving owned descendants after abnormal direct-child exit.
  if p.returncode not in (0,1):
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
  receipt=json.loads((R/'evidence'/name).read_text())
  expected=0 if mode=='positive' else 1
  results.append({'name':name,'returncode':p.returncode,'stdout':out.decode(),'stderr':err.decode()})
  with (R/'evidence'/(name+'.launch')).open('x') as f:json.dump(results[-1],f,indent=2)
  if p.returncode!=expected or receipt['status']!=('PASS' if mode=='positive' else 'FAIL'):raise RuntimeError('Unexpected launch outcome')
  if mode!='positive' and (receipt.get('error_type'),receipt.get('error'))!=('RuntimeError','Negative oracle mismatch'):raise RuntimeError('Wrong negative failure')
with (R/'LAUNCHES.json').open('x') as f:json.dump(results,f,indent=2)

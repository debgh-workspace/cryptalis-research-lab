import json,os,subprocess,sys,hashlib
from pathlib import Path
R=Path(__file__).absolute().parent;python=str(R.parent/'repo/.venv/bin/python')
launches=[];(R/'evidence').mkdir()
for opt in [0,1]:
    for mode in ['release','transfer','positive']:
        name=f'{mode}-O{opt}';dest='evidence/'+name+'.json'
        command=[python]+(['-O'] if opt else [])+[str(R/'run.py'),mode,dest]
        p=subprocess.run(command,capture_output=True,text=True,timeout=180,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
        for suffix,text in [('stdout',p.stdout),('stderr',p.stderr)]:
            with (R/'evidence'/f'{name}.{suffix}').open('x') as f:f.write(text)
        receipt=json.loads((R/dest).read_text())
        launch={'name':name,'command':command,'exit':p.returncode,'receipt_sha256':hashlib.sha256((R/dest).read_bytes()).hexdigest()};launches.append(launch)
        if mode=='positive':
            if p.returncode!=0 or receipt['status']!='PASS':raise RuntimeError('Positive failed '+name)
        elif p.returncode!=1 or receipt.get('error')!='Exact resource mismatch' or receipt.get('error_type')!='RuntimeError' or not receipt['observations'][0].get('original_verified'):raise RuntimeError('Wrong negative '+name)
with (R/'LAUNCHES.json').open('x') as f:json.dump(launches,f,indent=2);f.write('\n')
print(json.dumps({'launches':len(launches),'status':'PASS'}))

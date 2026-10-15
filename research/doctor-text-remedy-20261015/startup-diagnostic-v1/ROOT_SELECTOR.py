import os,json,hashlib,subprocess,stat,resource
from pathlib import Path
W=Path('/workspace/scratch/cb28ee9f5f4a');B=W/'cryptalis-executable';D=B/'experiments/preview-doctor-dx-slice-20261015/startup-diagnostic-v1';O=W/'persistence-recovery-20261013/doctor-startup-diagnostic-v1';O.mkdir(mode=0o700)
def h(p):
 p=Path(p)
 for q in reversed(p.parents):assert stat.S_ISDIR(q.lstat().st_mode)
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 return hashlib.sha256(p.read_bytes()).hexdigest()
py='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'
assert h(py)=='fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7'
pins={str(D/'startup_probe.py'):'c5d5b86cbc1da6641ea3acced87d3cc436d72e5daab5b76e8a8066852dcd1ec1',str(D/'RUN_PLAN.md'):'31e7ee4cda70b339f269889adfe162ca36f6bf20ad54c82c336f43d2a6b4533d',str(B/'reviewer-notes/doctor-remedy-slice-independent-20261015/STARTUP_DIAGNOSTIC_REVIEW.md'):'ba5d29a4f50d5c5fd897be202fdb104d8fff69afcd274d1b1f0bb157d6ec5c7e'}
for p,d in pins.items():assert h(p)==d
for mode,env in [('empty',{}),('fixed-locale',{'LC_ALL':'C.UTF-8'})]:
 assert not os.path.lexists(D/'no-bytecode-use')
 argv=[py,'-I','-B','-S','-X','pycache_prefix='+str(D/'no-bytecode-use'),str(D/'startup_probe.py'),mode]
 (O/(mode+'-selection.json')).write_text(json.dumps({'argv':argv,'environment':env,'cwd':str(D),'pins':pins,'timeout_seconds':5,'output_limit':16384},indent=2)+'\n')
 def limits():resource.setrlimit(resource.RLIMIT_FSIZE,(16384,16384))
 with (O/(mode+'.stdout')).open('xb') as out,(O/(mode+'.stderr')).open('xb') as err:
  p=subprocess.Popen(argv,cwd=D,env=env,stdout=out,stderr=err,preexec_fn=limits)
  timeout=False
  try:code=p.wait(timeout=5)
  except subprocess.TimeoutExpired:timeout=True;p.kill();code=p.wait()
 result={'exit_code':code,'timeout':timeout,'pins_unchanged':all(h(p)==d for p,d in pins.items()),'prefix_absent':not os.path.lexists(D/'no-bytecode-use')}
 (O/(mode+'-RESULT.json')).write_text(json.dumps(result,indent=2)+'\n')
 assert code==0 and not timeout and result['pins_unchanged'] and result['prefix_absent']
 assert (O/(mode+'.stderr')).stat().st_size==0 and (O/(mode+'.stdout')).stat().st_size<=16384
 print(mode,(O/(mode+'.stdout')).read_text().strip())

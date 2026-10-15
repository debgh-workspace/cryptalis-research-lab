import hashlib,json,stat,subprocess,resource,time,os,sys
from pathlib import Path
mode=sys.argv[1];assert mode in ('light17','boundary1')
W=Path('/workspace/scratch/cb28ee9f5f4a');B=W/'cryptalis-executable';D=B/'experiments/aborted-successor-envelope-v1-20261015';R=B/'reviewer-notes/aborted-successor-envelope-independent-20261015';O=W/'persistence-recovery-20261013'/('abort-envelope-unit-v3-'+mode+'-root');O.mkdir(mode=0o700)
def digest(p,cap=1048576):
 for q in reversed(p.parents):assert stat.S_ISDIR(q.lstat().st_mode)
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size<=cap
 return hashlib.sha256(p.read_bytes()).hexdigest()
pins={R/'REVIEW.md':'a15a3cc81b5ad65734a22d9691538ad94cd26b28e7c52961586a9ac2eb77c021',R/'SPLIT_V3_PREPARATION.md':'081720008501e6d728a5a0eae16cbd080830a0f04203836c60c0aee57afe7dc2',R/'UNIT_RUNNER_SPLIT_V3.py':'f9b36facdb5d208fd217f243152ac79642aa5bd5fb4b80fb33d63b1d1bd1e546',D/'envelope_reference.py':'27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c',D/'test_envelope_reference.py':'152f8c605be07d5a63877f09942f66c3f89045457dad051cd8b85a780aa60d6c',D/'correction-v2/test_deciding_vectors.py':'e631a11f36b346984cee7304d22abefa2099e61c760d08a414af93d32fccf8cc'}
for p,h in pins.items():assert digest(p)==h
py=Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12');assert digest(py,134217728)=='fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7'
cpu,wall=(30,60) if mode=='light17' else (240,300)
argv=[str(py),'-I','-B','-S',str(R/'UNIT_RUNNER_SPLIT_V3.py'),mode]
(O/'selection.json').write_text(json.dumps({'mode':mode,'argv':argv,'cwd':str(W),'expected_methods':17 if mode=='light17' else 1,'excluded_completed_cursor_method':True,'pins':{str(p):h for p,h in pins.items()},'wall_timeout_seconds':wall,'cpu_soft_hard_seconds':[cpu,cpu],'per_file_limit_bytes':2097152,'scope':'Pure reference unit partition; no product/PG/v3'},indent=2)+'\n')
def limits():
 resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152));resource.setrlimit(resource.RLIMIT_CPU,(cpu,cpu))
start=time.monotonic();timedout=False
with (O/'stdout.log').open('xb') as out,(O/'stderr.log').open('xb') as err:
 p=subprocess.Popen(argv,cwd=W,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','TZ':'UTC'},stdout=out,stderr=err,preexec_fn=limits)
 while True:
  pid,status,usage=os.wait4(p.pid,os.WNOHANG)
  if pid:break
  if time.monotonic()-start>wall:
   timedout=True;p.kill();pid,status,usage=os.wait4(p.pid,0);break
  time.sleep(0.05)
 code=os.waitstatus_to_exitcode(status);p.returncode=code
post={str(q):digest(q) for q in pins};assert all(post[str(q)]==h for q,h in pins.items())
result={'mode':mode,'exit_code':code,'signaled':os.WIFSIGNALED(status),'signal':os.WTERMSIG(status) if os.WIFSIGNALED(status) else None,'timeout':timedout,'wall_seconds':time.monotonic()-start,'child_user_cpu_seconds':usage.ru_utime,'child_system_cpu_seconds':usage.ru_stime,'child_peak_rss_kib':usage.ru_maxrss,'resource_scope':'wait4 for this exact child; Linux KiB RSS','source_pins_unchanged':True,'stdout_bytes':(O/'stdout.log').stat().st_size,'stderr_bytes':(O/'stderr.log').stat().st_size}
(O/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));print((O/'stderr.log').read_text());sys.exit(0 if code==0 and not timedout else 1)

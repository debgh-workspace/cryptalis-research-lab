import hashlib,json,stat,subprocess,resource,time
from pathlib import Path
W=Path('/workspace/scratch/cb28ee9f5f4a');B=W/'cryptalis-executable';D=B/'experiments/aborted-successor-envelope-v1-20261015';R=B/'reviewer-notes/aborted-successor-envelope-independent-20261015';O=W/'persistence-recovery-20261013/abort-envelope-unit-v2-root';O.mkdir(mode=0o700)
def digest(p,cap=1048576):
 for q in reversed(p.parents): assert stat.S_ISDIR(q.lstat().st_mode)
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and s.st_size<=cap
 b=p.read_bytes();return hashlib.sha256(b).hexdigest()
pins={R/'REVIEW.md':'a15a3cc81b5ad65734a22d9691538ad94cd26b28e7c52961586a9ac2eb77c021',R/'UNIT_RUNNER.py':'665cfa4894726559623e7d56511c76890f18e8a40f617460f9f68712503d63e9',D/'envelope_reference.py':'27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c',D/'test_envelope_reference.py':'152f8c605be07d5a63877f09942f66c3f89045457dad051cd8b85a780aa60d6c',D/'correction-v2/test_deciding_vectors.py':'e631a11f36b346984cee7304d22abefa2099e61c760d08a414af93d32fccf8cc'}
for p,h in pins.items():assert digest(p)==h
py=Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12');assert digest(py,134217728)=='fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7'
argv=[str(py),'-I','-B','-S',str(R/'UNIT_RUNNER.py')]
(O/'selection.json').write_text(json.dumps({'scope':'Isolated stdlib reference unit proof only; no product/PG/v3 admission','argv':argv,'cwd':str(W),'expected_test_methods':19,'subtests_counted_separately':False,'pins':{str(p):h for p,h in pins.items()},'wall_timeout_seconds':60,'cpu_seconds_limit':30,'per_file_limit_bytes':2097152},indent=2)+'\n')
def limits():
 resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152));resource.setrlimit(resource.RLIMIT_CPU,(30,30))
start=time.monotonic();timeout=False
with (O/'stdout.log').open('xb') as out,(O/'stderr.log').open('xb') as err:
 try:r=subprocess.run(argv,cwd=W,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','TZ':'UTC'},stdout=out,stderr=err,timeout=60,preexec_fn=limits);code=r.returncode
 except subprocess.TimeoutExpired:timeout=True;code=None
post={str(p):digest(p) for p in pins};assert all(post[str(p)]==h for p,h in pins.items())
result={'exit_code':code,'timeout':timeout,'wall_seconds':time.monotonic()-start,'source_pins_unchanged':True,'stdout_bytes':(O/'stdout.log').stat().st_size,'stderr_bytes':(O/'stderr.log').stat().st_size,'scope':'Unit observation only; independent terminal audit pending'}
(O/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));print((O/'stdout.log').read_text());print((O/'stderr.log').read_text())

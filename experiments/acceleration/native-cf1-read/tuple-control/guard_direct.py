"""Additional provenance gate; preserves the original reviewed source freeze."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).parent.absolute()
PYTHON=str(ROOT.parent/'repo/.venv/bin/python')
OVERRIDES=('CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','OBJC_INCLUDE_PATH','LIBRARY_PATH',
 'COMPILER_PATH','GCC_EXEC_PREFIX','LDFLAGS','CFLAGS','CPPFLAGS','CC','CXX','LD',
 'LD_PRELOAD','LD_LIBRARY_PATH','LD_AUDIT','PYTHONPATH','PYTHONHOME','GCC_SPECS')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
 with p.open('x') as s:json.dump(v,s,indent=2);s.write('\n')
def environment():
 if any(k in os.environ for k in OVERRIDES):raise RuntimeError('inherited compile/link/Python override present')
 if sys.executable!=PYTHON or sys.version_info[:3]!=(3,12,14):raise RuntimeError('wrong guard Python')
def validate(p):
 environment()
 for name,h in p['pins'].items():
  if sha(name)!=h:raise RuntimeError('provenance changed: '+name)
 if sha(ROOT/'guard_direct.py')!=p['guard_sha256']:raise RuntimeError('guard changed')
mode=sys.argv[1];environment()
record=ROOT/'DIRECT_PROVENANCE.json'
if mode=='capture':
 tools=[Path(PYTHON),Path('/usr/bin/gcc'),Path('/usr/libexec/gcc/x86_64-linux-gnu/14/cc1'),
        Path('/usr/libexec/gcc/x86_64-linux-gnu/14/collect2'),Path('/usr/bin/as'),Path('/usr/bin/ld'),Path('/usr/bin/readelf'),Path('/usr/bin/ldd')]
 files=set(tools)
 for directory in ['/usr/include','/usr/lib/gcc/x86_64-linux-gnu/14','/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12']:
  files.update(f for f in Path(directory).rglob('*') if f.is_file())
 for name in ['libc.so','libc.so.6','libc_nonshared.a','libgcc_s.so.1','crti.o','crtn.o','ld-linux-x86-64.so.2']:
  files.add(Path('/usr/lib/x86_64-linux-gnu')/name)
 files.add(Path('/lib64/ld-linux-x86-64.so.2'))
 dependencies={}
 for tool in tools:
  if tool.name=='ldd':continue
  r=subprocess.run(['/usr/bin/ldd',str(tool)],capture_output=True,text=True,timeout=10)
  if r.returncode:raise RuntimeError('trusted tool dependency query failed')
  dependencies[str(tool)]=r.stdout
  for word in r.stdout.split():
   if word.startswith('/') and Path(word).is_file():files.add(Path(word))
 freeze=json.loads((ROOT/'DIRECT_FREEZE.json').read_text())
 files.add(ROOT/'DIRECT_FREEZE.json')
 files.update(ROOT/f for f in freeze['sha256'])
 for name,h in freeze['sha256'].items():
  if sha(ROOT/name)!=h:raise RuntimeError('reviewed source freeze mismatch')
 data={'scope':'Pre-build direct-only toolchain/header/runtime dependency snapshot; not hermetic attestation',
  'guard_sha256':sha(ROOT/'guard_direct.py'),'overrides_rejected':list(OVERRIDES),
  'pins':{str(f):sha(f) for f in sorted(files)},'trusted_tool_dependency_reports':dependencies,
  'limitation':'Pinning includes compiler support tree, system/Python headers, libc/link objects and observed tool dependencies; does not claim every tool internal lookup or kernel input.'}
 save(record,data);print(json.dumps({'status':'CAPTURED','pins':len(data['pins']),'sha256':sha(record)}))
elif mode=='run':
 p=json.loads(record.read_text());validate(p)
 runroot=ROOT/'direct-run-01';runroot.mkdir();runs=[]
 try:
  for buildmode in ('normal','diagnostic'):
   for stage in ('build','test'):
    validate(p)
    buildname='build-direct-01-'+buildmode
    args=['build_direct.py',buildmode,buildname] if stage=='build' else ['launch_direct.py',buildname,'direct-evidence-01-'+buildmode]
    command=[PYTHON,'-I','-B',str(ROOT/args[0]),*args[1:]]
    proc=subprocess.run(command,capture_output=True,text=True,timeout=100 if stage=='build' else 400)
    r={'mode':buildmode,'stage':stage,'command':command,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
    save(runroot/(buildmode+'-'+stage+'.json'),r);runs.append(r)
    validate(p)
    if proc.returncode:raise RuntimeError('bounded direct stage failed; preserve without retry')
  save(runroot/'summary.json',{'status':'PASS','provenance_sha256':sha(record),'runs':runs})
 except BaseException as exc:
  save(runroot/'failure.json',{'status':'FAIL','error_type':type(exc).__name__,'error':str(exc),'runs':runs})
  raise
else:raise RuntimeError('unknown guard mode')

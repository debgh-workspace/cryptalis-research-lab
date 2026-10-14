from pathlib import Path
import sys,sysconfig,hashlib,json,subprocess
R=Path(__file__).parent.absolute();B=R/'build'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if sys.executable!=str(R.parent/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sys.flags.optimize:raise RuntimeError('Interpreter mismatch')
pins=json.loads((R/'PINS.json').read_text())
for p,h in pins.items():
 if sha(p)!=h:raise RuntimeError('Pin changed: '+p)
B.mkdir();binary=B/('native_cf1'+sysconfig.get_config_var('EXT_SUFFIX'))
command=['/usr/bin/gcc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-std=c11','-DCF1_DIAGNOSTIC','-I/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12',str(R/'native_cf1.c'),'-lcrypto','-o',str(binary)]
p=subprocess.run(command,capture_output=True,text=True,timeout=60)
receipt=dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,python=sys.version,executable=sys.executable,soabi=sysconfig.get_config_var('SOABI'),pins=pins)
if p.returncode==0:
 linked=subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True);receipt['ldd']=linked
 for word in linked.split():
  if word.startswith('/') and Path(word).is_file():pins[word]=sha(word)
 pins[str(binary)]=sha(binary)
receipt['compiler']=subprocess.check_output(['/usr/bin/gcc','--version'],text=True)
with (B/'build.json').open('x') as out:json.dump(receipt,out,indent=2)
print(p.stdout,p.stderr);sys.exit(p.returncode)

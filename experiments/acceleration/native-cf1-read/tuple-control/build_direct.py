"""Explicitly authorized future compile only. Does not run/import the extension."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig
ROOT = Path(__file__).parent.absolute()
PYTHON = str(ROOT.parent/'repo/.venv/bin/python')
INCLUDE = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12')
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path, value):
    with path.open('x') as out: json.dump(value, out, indent=2); out.write('\n')
if sys.executable != PYTHON or sys.version_info[:3] != (3,12,14) or sys.flags.optimize != 0:
    raise RuntimeError('wrong build Python')
mode, name = sys.argv[1:]
if mode not in ('normal','diagnostic') or Path(name).name != name:
    raise RuntimeError('invalid build selection')
build = ROOT/name; build.mkdir()
receipt = {'status':'FAIL', 'mode':mode, 'python':sys.executable, 'version':sys.version,
           'soabi':sysconfig.get_config_var('SOABI'), 'scope':'direct tuple only; no wrapper/crypto qualification'}
try:
    freeze = json.loads((ROOT/'DIRECT_FREEZE.json').read_text())
    for path, pin in freeze['sha256'].items():
        if digest(ROOT/path) != pin: raise RuntimeError('source freeze mismatch: '+path)
    inputs = [ROOT/path for path in freeze['sha256']] + [ROOT/'DIRECT_FREEZE.json', Path(PYTHON),
        Path('/usr/bin/gcc'), Path('/usr/libexec/gcc/x86_64-linux-gnu/14/cc1'), Path('/usr/bin/as'), Path('/usr/bin/ld')]
    inputs += list(INCLUDE.rglob('*.h'))
    if not (INCLUDE/'Python.h').is_file(): raise RuntimeError('missing pinned headers')
    pins = {str(p):digest(p) for p in inputs}
    binary = build/('native_tuple'+sysconfig.get_config_var('EXT_SUFFIX'))
    command = ['/usr/bin/gcc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-std=c11', '-I'+str(INCLUDE)]
    if mode == 'diagnostic': command.append('-DTUPLE_DIAGNOSTIC')
    command += [str(ROOT/'native_tuple.c'),'-o',str(binary)]
    receipt.update(command=command, pins=pins, binary=str(binary))
    env = dict(os.environ); env.pop('PYTHONPATH', None); env.pop('PYTHONHOME', None)
    result = subprocess.run(command,capture_output=True,text=True,timeout=60,env=env)
    receipt.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
    receipt['compiler'] = subprocess.run(['/usr/bin/gcc','--version'],capture_output=True,text=True,timeout=10,check=True).stdout
    if result.returncode: raise RuntimeError('compile failed')
    # Read-only ELF dependency inspection; does not load/run the new extension.
    receipt['elf_dynamic'] = subprocess.run(['/usr/bin/readelf','-d',str(binary)],capture_output=True,text=True,timeout=10,check=True).stdout
    for path, pin in pins.items():
        if digest(path) != pin: raise RuntimeError('build input changed')
    receipt['binary_sha256'] = digest(binary); receipt['status'] = 'BUILT'
except BaseException as exc:
    receipt['error_type'] = type(exc).__name__; receipt['error'] = str(exc)
    raise
finally:
    save(build/'build.json',receipt)

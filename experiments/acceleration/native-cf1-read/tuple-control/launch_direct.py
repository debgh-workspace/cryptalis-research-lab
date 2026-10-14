"""Bounded parent or checked child. No timing, crypto, fixture construction or PG."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig
ROOT = Path(__file__).parent.absolute()
PYTHON = str(ROOT.parent/'repo/.venv/bin/python')
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path, value):
    with path.open('x') as out: json.dump(value,out,indent=2); out.write('\n')
def check(build):
    if sys.executable != PYTHON or sys.version_info[:3] != (3,12,14): raise RuntimeError('wrong Python')
    m = json.loads((build/'build.json').read_text())
    if m['status'] != 'BUILT' or m['soabi'] != sysconfig.get_config_var('SOABI'): raise RuntimeError('bad build/ABI')
    for path,pin in m['pins'].items():
        if digest(path) != pin: raise RuntimeError('pinned input changed: '+path)
    if digest(m['binary']) != m['binary_sha256']: raise RuntimeError('binary changed')
    if Path(m['binary']).parent != build: raise RuntimeError('binary outside selected build')
    return m
if sys.argv[1] == '--child':
    build = ROOT/sys.argv[2]; output = ROOT/sys.argv[3]; negative = sys.argv[4] == 'negative'
    receipt = {'status':'FAIL', 'optimize':sys.flags.optimize, 'negative':negative}
    try:
        m = check(build)
        if sys.flags.optimize not in (0,1): raise RuntimeError('unexpected optimization')
        spec = importlib.util.spec_from_file_location('native_tuple',m['binary'])
        native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
        if native.__file__ != m['binary']: raise RuntimeError('origin mismatch')
        diagnostic = m['mode'] == 'diagnostic'
        if hasattr(native,'tuple_alloc_failure') != diagnostic: raise RuntimeError('wrong diagnostic surface')
        driver_spec = importlib.util.spec_from_file_location('direct_test', ROOT/'direct_test.py')
        direct_test = importlib.util.module_from_spec(driver_spec); driver_spec.loader.exec_module(direct_test)
        receipt['passed'] = direct_test.run(native,diagnostic,negative)
        receipt['status'] = 'PASS'; receipt['build_hash'] = digest(build/'build.json')
    except BaseException as exc:
        receipt['error_type'] = type(exc).__name__; receipt['error'] = str(exc)
    save(output,receipt)
    sys.exit(0 if receipt['status']=='PASS' else 1)
else:
    name, outname = sys.argv[1:]
    if any(Path(n).name != n for n in (name,outname)): raise RuntimeError('invalid name')
    build = ROOT/name; m = check(build)
    out = ROOT/outname; out.mkdir(); results=[]
    for optimize in (0,1):
        for variant in ('positive','negative'):
            target = out/f'{variant}-o{optimize}.json'
            cmd = [PYTHON,'-I','-B'] + (['-O'] if optimize else []) + [str(ROOT/'launch_direct.py'),'--child',name,str(target.relative_to(ROOT)),variant]
            env = dict(os.environ); env.pop('PYTHONPATH',None); env.pop('PYTHONHOME',None)
            try:
                proc = subprocess.run(cmd,capture_output=True,text=True,timeout=90,env=env)
                r = json.loads(target.read_text())
                valid = proc.returncode == 0 and r['status']=='PASS' if variant=='positive' else (
                    proc.returncode==1 and r['status']=='FAIL' and r.get('error_type')=='RuntimeError' and
                    r.get('error')=='tuple mismatch: oracle/uuid-storage-unicode/payload-info')
                results.append({'command':cmd,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'accepted':valid,'receipt_sha256':digest(target)})
                if not valid: raise RuntimeError('unexpected child outcome')
            except BaseException as exc:
                results.append({'error_type':type(exc).__name__,'error':str(exc)})
                save(out/'launch.json',results)
                raise
    save(out/'launch.json',results)

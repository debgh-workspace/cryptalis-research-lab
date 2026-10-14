"""Additive cache-provenance gate; original frozen full runner stays unchanged."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
R=Path(__file__).parent.absolute()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=json.loads((R/'FULL_RUN_FREEZE_V2.json').read_text())
target=R/(sys.argv[2]+'-cache-check.json')
receipt={'status':'FAIL','freeze_sha256':sha(R/'FULL_RUN_FREEZE_V2.json')}
def check():
    if any(n in os.environ for n in p['reject_environment']):raise RuntimeError('Cache gate environment override')
    for n,h in p['pins'].items():
        if sha(n)!=h:raise RuntimeError('Cache gate pin mismatch: '+n)
    for root,expected in p['bytecode_inventory'].items():
        actual=sorted(str(f) for f in Path(root).rglob('*.pyc') if f.is_file())
        if actual!=expected:raise RuntimeError('Cache inventory changed')
try:
    check();receipt['before']='PASS'
    sys.argv[0]=str(R/'full_run.py')
    runpy.run_path(str(R/'full_run.py'),run_name='__main__')
finally:
    try:
        check();receipt['after']='PASS';receipt['status']='PASS'
    except BaseException as exc:
        receipt.update(error_type=type(exc).__name__,error=str(exc));raise
    finally:
        with target.open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')

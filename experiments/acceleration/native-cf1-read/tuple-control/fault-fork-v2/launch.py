"""Finite launch with bounded stdout/stderr, process-group kill and bounded reap."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
R=Path(__file__).parent.absolute();B=R.parent.parent
name=sys.argv[1]
if Path(name).name!=name:raise RuntimeError('Invalid output name')
if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14):raise RuntimeError('Wrong Python')
freeze=json.loads((R/'FREEZE.json').read_text())
if any(k in os.environ for k in freeze['reject_environment']):raise RuntimeError('Environment override')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
    with p.open('x') as out:json.dump(v,out,indent=2);out.write('\n')
def kill_group(proc):
    try:os.killpg(proc.pid,signal.SIGKILL);return True
    except ProcessLookupError:return False

def bounded(command):
    buffers={'stdout':bytearray(),'stderr':bytearray()}
    state={'command':command,'stream_cap_bytes':65536,'deadline_seconds':180,'cleanup_reap_seconds':10,'group_kill_requested':False,'launcher_reaped':False}
    problem=None;proc=None;selector=None
    try:
        proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        selector=selectors.DefaultSelector()
        for stream,label in [(proc.stdout,'stdout'),(proc.stderr,'stderr')]:
            os.set_blocking(stream.fileno(),False)
            selector.register(stream,selectors.EVENT_READ,label)
        deadline=time.monotonic()+180
        while selector.get_map():
            remaining=deadline-time.monotonic()
            if remaining<=0:raise RuntimeError('Top-level child timeout')
            events=selector.select(remaining)
            if not events:raise RuntimeError('Top-level stream timeout')
            for key,_ in events:
                try:data=os.read(key.fileobj.fileno(),4096)
                except BlockingIOError:continue
                if not data:selector.unregister(key.fileobj);continue
                buf=buffers[key.data];space=65536-len(buf);buf.extend(data[:space])
                if len(data)>space:raise RuntimeError('Top-level stream limit')
        while proc.poll() is None:
            if time.monotonic()>=deadline:raise RuntimeError('Top-level exit timeout')
            time.sleep(0.01)
    except BaseException as exc:
        problem=exc;state.update(error_type=type(exc).__name__,error=str(exc))
    finally:
        cleanup_errors=[]
        if proc is not None:
            try:
                state['group_kill_requested']=kill_group(proc)
                reap_deadline=time.monotonic()+10
                while proc.poll() is None and time.monotonic()<reap_deadline:time.sleep(0.01)
                state['launcher_reaped']=proc.poll() is not None
            except BaseException as exc:cleanup_errors.append(type(exc).__name__+': '+str(exc))
            for stream in (proc.stdout,proc.stderr):
                try:stream.close()
                except BaseException as exc:cleanup_errors.append(type(exc).__name__+': '+str(exc))
        if selector is not None:
            try:selector.close()
            except BaseException as exc:cleanup_errors.append(type(exc).__name__+': '+str(exc))
        state.update(exit=proc.returncode if proc is not None else None,stdout=buffers['stdout'].decode('utf8',errors='replace'),stderr=buffers['stderr'].decode('utf8',errors='replace'),cleanup_errors=cleanup_errors)
        state['terminal_state']='reaped' if state['launcher_reaped'] and not cleanup_errors else 'UNKNOWN'
        if state['terminal_state']=='UNKNOWN' and problem is None:
            problem=RuntimeError('Top-level terminal state unknown')
            state.update(error_type='RuntimeError',error=str(problem))
    return state,problem

for p,h in freeze['pins'].items():
    if sha(p)!=h:raise RuntimeError('Pin mismatch')
out=R/name;out.mkdir();records=[]
for optimization in (0,1):
    for mode in freeze['modes']:
        target=out/f'{mode}-o{optimization}.json'
        command=[sys.executable,'-I','-B']+(['-O'] if optimization else [])+[str(R/'run.py'),mode,str(target.relative_to(R))]
        record,problem=bounded(command)
        record['receipt_sha256']=sha(target) if target.exists() else None
        save(out/f'{mode}-o{optimization}-launch.json',record);records.append(record)
        if problem is not None:raise problem
        if not target.exists():raise RuntimeError('Missing receipt')
        result=json.loads(target.read_text())
        if result.get('precheck')!='PASS' or result.get('postcheck')!='PASS' or result.get('freeze_sha256')!=sha(R/'FREEZE.json'):raise RuntimeError('Integrity check failure')
        if mode=='positive':
            if record['exit'] or record['stdout'] or record['stderr'] or result['status']!='PASS' or len(result['observations'])!=88 or len(result['fork_receipts'])!=4:raise RuntimeError('Positive supplement failure')
        else:
            n=result.get('negative')
            if record['exit']!=1 or record['stdout'] or result['status']!='FAIL' or result.get('error_type')!='RuntimeError' or result.get('error')!='Supplement mismatch' or not n or not n.get('original_verified') or n.get('mode')!=mode or result['observations'] or result['fork_receipts'] or not record['stderr'].rstrip().endswith('RuntimeError: Supplement mismatch'):raise RuntimeError('Negative signature mismatch')
save(out/'launches.json',records)

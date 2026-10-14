"""Executable bounded process-group containment; no automatic retries."""
import json,os,selectors,signal,subprocess,time
from pathlib import Path

def bounded(command,timeout,stream_cap,receipt_path):
    receipt_path=Path(receipt_path)
    if receipt_path.exists():raise RuntimeError('Refuse receipt overwrite')
    start=time.monotonic();p=None;sel=selectors.DefaultSelector();chunks={'stdout':bytearray(),'stderr':bytearray()}
    reason=None;result={};interrupted=None;cleanup_errors=[]
    def kill_group(sig):
        if p is not None:
            try:os.killpg(p.pid,sig)
            except ProcessLookupError:pass
            except BaseException as exc:cleanup_errors.append(type(exc).__name__+': group signal')
    try:
        env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
        env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONNOUSERSITE']='1'
        p=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env=env)
        for name,pipe in [('stdout',p.stdout),('stderr',p.stderr)]:
            os.set_blocking(pipe.fileno(),False);sel.register(pipe,selectors.EVENT_READ,name)
        while sel.get_map():
            if time.monotonic()-start>=timeout:reason='timeout';break
            for key,_ in sel.select(min(0.1,max(0,timeout-(time.monotonic()-start)))):
                data=os.read(key.fileobj.fileno(),65536)
                if not data:sel.unregister(key.fileobj);key.fileobj.close();continue
                stream=chunks[key.data]
                room=max(0,stream_cap-len(stream));stream.extend(data[:room])
                if len(data)>room:reason='stream-cap';break
            if reason:break
        if reason is None:
            try:p.wait(timeout=max(0.1,timeout-(time.monotonic()-start)))
            except subprocess.TimeoutExpired:reason='timeout'
    except BaseException as exc:
        reason='interruption-or-supervisor-error';interrupted=exc
    finally:
        # Signaling the group and reaping the direct child is not proof that every
        # descendant is absent. Cleanup failures must not suppress the receipt.
        kill_group(signal.SIGTERM)
        if p is not None:
            try:p.wait(timeout=2)
            except subprocess.TimeoutExpired:
                kill_group(signal.SIGKILL)
                try:p.wait(timeout=5)
                except BaseException as exc:cleanup_errors.append(type(exc).__name__+': final reap')
            except BaseException as exc:cleanup_errors.append(type(exc).__name__+': initial reap')
            kill_group(signal.SIGKILL)
        try:
            for key in list(sel.get_map().values()):
                try:sel.unregister(key.fileobj);key.fileobj.close()
                except BaseException as exc:cleanup_errors.append(type(exc).__name__+': registered pipe close')
        except BaseException as exc:cleanup_errors.append(type(exc).__name__+': selector inventory')
        try:sel.close()
        except BaseException as exc:cleanup_errors.append(type(exc).__name__+': selector close')
        if p is not None:
            for pipe in (p.stdout,p.stderr):
                try:
                    if pipe is not None and not pipe.closed:pipe.close()
                except BaseException as exc:cleanup_errors.append(type(exc).__name__+': pipe close')
        if cleanup_errors and reason is None:reason='cleanup-error'
        result={'command':command,'reason':reason,'exit_code':None if p is None else p.returncode,
                'elapsed_seconds':time.monotonic()-start,'process_reaped':p is not None and p.returncode is not None,
                'group_termination_attempted':p is not None,'descendants_verified_absent':False,
                'cleanup_errors':cleanup_errors,'stdout':chunks['stdout'].decode('utf8','replace'),
                'stderr':chunks['stderr'].decode('utf8','replace'),'stream_cap_bytes_each':stream_cap,'timeout_seconds':timeout}
        with receipt_path.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    if interrupted is not None:raise interrupted
    return result

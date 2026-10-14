"""Bounded child capture. Never reap leader before the last group signal."""
import hashlib,os,selectors,signal,subprocess,time

def bounded(command,environment,seconds,cap=2097152):
    result={'command':command,'environment':environment,'exit_code':None,'reason':None,'leader_reaped':False,'group_signals':[],'cleanup_errors':[],'descendants_verified_absent':False}
    proc=None;selector=selectors.DefaultSelector();buffers={'stdout':bytearray(),'stderr':bytearray()};primary=None
    def kill_unreaped():
        # No poll()/wait() occurs before here. An exited-but-unreaped leader still
        # reserves its numeric identity. returncode is set only by final wait().
        if proc is None or proc.returncode is not None:return
        try:os.killpg(proc.pid,signal.SIGKILL);result['group_signals'].append({'pid':proc.pid,'signal':'SIGKILL','leader_reaped':False})
        except ProcessLookupError:result['group_signals'].append({'pid':proc.pid,'signal':'SIGKILL','result':'group absent','leader_reaped':False})
        except BaseException as exc:result['cleanup_errors'].append('signal: '+repr(exc))
    try:
        proc=subprocess.Popen(command,env=environment,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        for key,stream in [('stdout',proc.stdout),('stderr',proc.stderr)]:
            os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,key)
        deadline=time.monotonic()+seconds
        while True:
            # WNOWAIT observes termination without releasing PID/PGID identity.
            exited=os.waitid(os.P_PID,proc.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT) is not None
            if exited and not selector.get_map():break
            remaining=deadline-time.monotonic()
            if remaining<=0:result['reason']='timeout';break
            for key,_ in selector.select(min(0.05,remaining)):
                chunk=os.read(key.fileobj.fileno(),65536)
                if not chunk:selector.unregister(key.fileobj);continue
                name=key.data;space=cap-len(buffers[name]);buffers[name].extend(chunk[:space])
                if len(chunk)>space:result['reason']='stream-cap';break
            if result['reason']:break
    except BaseException as exc:
        primary=exc;result['reason']='supervisor-exception';result['primary_error']=repr(exc)
    finally:
        # Kill before any reaping, including an exited leader with open inherited
        # pipes. No further group signaling is attempted after wait returns.
        if proc is not None:
            if result['reason'] is not None:kill_unreaped()
            try:
                proc.wait(timeout=10);result['leader_reaped']=True;result['exit_code']=proc.returncode
            except BaseException as exc:result['cleanup_errors'].append('bounded reap: '+repr(exc))
        for key in list(selector.get_map().values()):
            try:selector.unregister(key.fileobj)
            except BaseException as exc:result['cleanup_errors'].append('unregister: '+repr(exc))
        try:selector.close()
        except BaseException as exc:result['cleanup_errors'].append('selector close: '+repr(exc))
        if proc is not None:
            for stream in [proc.stdout,proc.stderr]:
                try:stream.close()
                except BaseException as exc:result['cleanup_errors'].append('pipe close: '+repr(exc))
        result['stdout']=bytes(buffers['stdout']).decode('utf8',errors='replace');result['stderr']=bytes(buffers['stderr']).decode('utf8',errors='replace')
        result['stdout_bytes']=len(buffers['stdout']);result['stderr_bytes']=len(buffers['stderr'])
        result['stdout_sha256']=hashlib.sha256(buffers['stdout']).hexdigest();result['stderr_sha256']=hashlib.sha256(buffers['stderr']).hexdigest()
    # Caller persists this record before raising/re-reporting interruptions.
    return result

"""Held additive executor: four correctness children and two reducers; no retries."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time

D=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/reviewer-notes/tenant-fastpath-v11-runtime-supervisor-v1-20261017')
P=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/tenant-fastpath-no-db-packet-v11-20261017')
R=D/'attempt-001'
PREPARED_SHA='0ee0e251481d6bd01e5eda6dbf67e3e568c25ed643570c565c635ae3fdc2f7a2'
ALLOW_SHA='17413de2a8f341f221355e288b1fef3d0e8f759912d5dfbd0366be93d18cbb17'
PACKET_SHA='7af82fd53dda6564f6d2a670cee43d0dc255ac4798dda1e32d817cfff2938426'
sys.path.insert(0,str(P))
from io_guard import read,metadata,check,namespace,absences,newfile,write_new,PREFIX,module_origins,STDLIB
O=P/'output'
HOST='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'
ENV={'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1',
     'PYTEST_ADDOPTS':'--assert=plain -s --tb=short'}
LIMIT=2*1024*1024
SECONDS=60
received_signal=None
child_history=[]
def interrupted(signum,frame):
    global received_signal
    # Record only: never interrupt assignment of a newly acquired Popen handle
    # or throw during cleanup. Repeated signals do not grow an unbounded log.
    if received_signal is None: received_signal=signum
for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP): signal.signal(sig,interrupted)

def cancellation_point():
    if received_signal is not None: raise InterruptedError('runtime cancellation requested')

def external_dump(name,value):
    data=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
    assert len(data)<=8*1024*1024
    fd=os.open(R/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb') as stream: stream.write(data)

def startup(initial_controls):
    absences()
    assert Path(__file__).absolute()==D/'supervisor.py' and Path.cwd()==D
    assert sys.executable==HOST and sys.flags.isolated and sys.flags.no_site
    assert sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize
    assert dict(os.environ)=={'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}
    assert not any(n in sys.modules for n in ('site','sitecustomize','usercustomize','pytest','conftest'))
    for path in (P/'HOST_STDLIB_SHA256.txt',P/'HOST_STDLIB_PATHS.txt',P/'io_guard.py',D/'supervisor.py'):
        initial_controls[str(path)]=metadata(path)
    raw=read(P/'HOST_STDLIB_SHA256.txt','8eb693338797591e5c35d9d42f5978e1a90d5a669d9afade9d25bece107d6793')
    paths=read(P/'HOST_STDLIB_PATHS.txt','1643bd6ce850cfbaf738a21a835b5f4df0c2c46d3fae6c7dd12361665d836d72')
    host={}
    for line in raw.decode().splitlines():
        digest,name=line.split('  ',1)
        assert len(digest)==64 and all(c in '0123456789abcdef' for c in digest)
        assert name not in host and name and str(Path(name))==name and not Path(name).is_absolute() and '..' not in Path(name).parts
        host[name]=digest
    names=paths.decode().splitlines()
    assert len(host)==488 and len(names)==488 and set(host)==set(names)
    allowed={str(STDLIB/n) for n in host}|{str(D/'supervisor.py'),str(P/'io_guard.py')}
    return module_origins(allowed,D/'supervisor.py')

def sha(p): return hashlib.sha256(read(p)).hexdigest()
def dump(p,value):
    write_new(p,(json.dumps(value,sort_keys=True,indent=2)+"\n").encode())

def child(name,mode,selection,allow):
    cancellation_point()
    stdout=O/'results'/f'{name}.stdout'
    stderr=O/'results'/f'{name}.stderr'
    command=[HOST,'-I','-S','-B','-X','pycache_prefix='+str(PREFIX),str(O/'child.py'),mode,str(selection),str(allow),sha(allow)]
    start=time.monotonic();total=0;reason=None;primary=None
    process=None;streams=None;status=None;cleanup_errors=[];leader_observed=False;group_cleanup_attempted=False;ownership_lost=False
    receipt={'argv':command,'exit':None,'stop_reason':None,'bytes':0,'failure_type':None,'cleanup_failure_types':cleanup_errors,'stage':'OUTPUT_ACQUISITION'}
    child_history.append(receipt)
    class CapturedOutput:
        def __init__(self,path): self.path=path;self.stream=None
        def __enter__(self):
            fd=None
            try:
                fd=newfile(self.path);self.stream=os.fdopen(fd,'wb');return self.stream
            except BaseException as error:
                receipt['output_open_failure']=type(error).__name__
                if fd is not None:
                    try: os.close(fd)
                    except BaseException as closing: cleanup_errors.append('output_open_cleanup:'+type(closing).__name__)
                raise
        def __exit__(self,exc_type,exc,tb):
            nonlocal primary,reason
            try: self.stream.close()
            except BaseException as error:
                cleanup_errors.append('output_close:'+type(error).__name__)
                if primary is None: primary=error
                reason=reason or 'output_close_error'
                receipt['failure_type']=type(primary).__name__
                receipt['stop_reason']=reason
            return False
    def stop_owned():
        nonlocal group_cleanup_attempted
        # No poll/wait/reap has occurred: the owned PID remains reserved even
        # if the leader exited. Cleanup targets its original process group.
        if process is not None and not group_cleanup_attempted and not ownership_lost:
            group_cleanup_attempted=True
            try: os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError: pass  # Already-exited owned group only.
            except BaseException as error: cleanup_errors.append(type(error).__name__)
    with CapturedOutput(stdout) as out,CapturedOutput(stderr) as err:
        try:
            assert signal.getsignal(signal.SIGCHLD)==signal.SIG_DFL
            process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,cwd=O,env=ENV,start_new_session=True)
            cancellation_point()
            # Ownership starts immediately after Popen, including selector setup.
            streams=selectors.DefaultSelector()
            streams.register(process.stdout,selectors.EVENT_READ,out)
            streams.register(process.stderr,selectors.EVENT_READ,err)
            while streams.get_map():
                cancellation_point()
                if time.monotonic()-start>SECONDS: reason='timeout';break
                for key,_ in streams.select(0.1):
                    data=os.read(key.fileobj.fileno(),65536)
                    if not data: streams.unregister(key.fileobj);continue
                    total+=len(data)
                    if total>LIMIT: reason='output_limit';break
                    key.data.write(data)
                if reason: break
            if reason is None:
                while True:
                    cancellation_point()
                    if time.monotonic()-start>SECONDS: reason='timeout';break
                    # Observe termination without releasing ownership/PID.
                    try: observed=os.waitid(os.P_PID,process.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
                    except ChildProcessError:
                        ownership_lost=True
                        cleanup_errors.append('OwnedLeaderNoLongerWaitable')
                        raise
                    if observed is not None:
                        assert observed.si_pid==process.pid
                        leader_observed=True;break
                    time.sleep(0.05)
                cancellation_point()
        except BaseException as error:
            primary=error;reason='signal' if received_signal is not None else 'supervisor_error'
        finally:
            if process is not None:
                # Always clean the owned group before the one reaping operation.
                # An already exited successful leader keeps its original status.
                stop_owned()
                if not ownership_lost:
                    try:
                        status=process.wait(timeout=10)
                    except BaseException as error:
                        cleanup_errors.append(type(error).__name__)
                        if primary is None: primary=error
                for pipe in (process.stdout,process.stderr):
                    if pipe is not None:
                        try: pipe.close()
                        except BaseException as error: cleanup_errors.append(type(error).__name__)
            if streams is not None:
                try: streams.close()
                except BaseException as error: cleanup_errors.append(type(error).__name__)
            # Update history before output flush/close can fail at context exit.
            receipt.update({'exit':status,'stop_reason':reason,'bytes':total,'failure_type':type(primary).__name__ if primary else None,'received_signal':received_signal,'leader_observed_before_cleanup':leader_observed,'group_cleanup_before_reap':group_cleanup_attempted,'ownership_lost':ownership_lost,'stage':'OWNED_CLEANUP_COMPLETE'})
    receipt.update({'argv':command,'exit':status,'stop_reason':reason,'bytes':total,
             'failure_type':type(primary).__name__ if primary else None,
             'cleanup_failure_types':cleanup_errors,
             'received_signal':received_signal,'leader_observed_before_cleanup':leader_observed,
             'group_cleanup_before_reap':group_cleanup_attempted,
             'ownership_lost':ownership_lost,
             'limits':{'seconds':SECONDS,'combined_output_bytes':LIMIT}})
    receipt['stdout_sha256']=sha(stdout);receipt['stderr_sha256']=sha(stderr)
    dump(O/'results'/f'{name}.json',receipt)
    if primary is not None: raise primary
    cancellation_point()
    assert not cleanup_errors, 'child cleanup failed; preserve receipt'
    assert reason is None and status==0, 'child failed; preserve and stop'
    return stdout

def execute():
    cancellation_point()
    absences()
    assert len(sys.argv)==3 and sys.argv[1]==PREPARED_SHA and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
    prepared=O/'PREPARED.json'
    assert sha(prepared)==sys.argv[1]
    receipt=json.loads(read(prepared)); allowed=receipt['closure']
    assert receipt['status']=='MATERIALIZED_ONLY' and receipt['declared_cases']==468 and receipt['execution_selected'] is False
    assert receipt['packet_sha256']==PACKET_SHA and receipt['allow_sha256']==ALLOW_SHA
    assert sha(O/'ALLOW.json')==receipt['allow_sha256']
    assert json.loads(read(O/'ALLOW.json'))==allowed
    check(allowed)
    assert not (O/'PREPARE_FAILED.json').exists()
    namespace(O,set(n for n in allowed if Path(n).is_relative_to(O)) | {str(O/'ALLOW.json'),str(O/'PREPARED.json')})
    (O/'results').mkdir(mode=0o700)
    success=[]
    for cell in ('sa20','sa21'):
        pair={}
        for variant in ('baseline','candidate'):
            cancellation_point()
            check(allowed)
            name=f'{cell}-{variant}'
            path=child(name,'correctness',O/f'{name}.json',O/'ALLOW.json')
            check(allowed)
            matches=[line[len('DIFFERENTIAL_JSON='):] for line in read(path).decode().splitlines() if line.startswith('DIFFERENTIAL_JSON=')]
            assert len(matches)==1
            data=json.loads(matches[0])
            assert len(data['collected'])==468 and len(set(data['collected']))==468
            pair[variant]=str(path)
        selection=O/'results'/f'{cell}-reduce-selection.json'
        cancellation_point()
        dump(selection,pair)
        reduction=dict(allowed)
        for path in [selection,*map(Path,pair.values())]: reduction[str(path)]=sha(path)
        allow=O/'results'/f'{cell}-reduce-allow.json';dump(allow,reduction)
        child(f'{cell}-reduce','reduce',selection,allow)
        check(allowed)
        success.append(cell)
    return {'status':'COMPLETED_CORRECTNESS_ONLY','cells':success,
                                 'cases_per_variant':468,'timing_selected':False,
                                 'product_speedup_claim':False}

def main():
    assert len(sys.argv)==3 and sys.argv[1]==PREPARED_SHA
    assert len(sys.argv[2])==64 and all(c in '0123456789abcdef' for c in sys.argv[2])
    assert Path(__file__).absolute()==D/'supervisor.py' and Path.cwd()==D
    for p in [D,*D.parents]:
        assert p.is_dir() and not p.is_symlink()
    assert not os.path.lexists(R)
    R.mkdir(mode=0o700)
    primary=None;result=None;startup_inventory=None;receipt=None
    monitored={};before={};initial_controls={};after={};namespace_results={};final_errors=[]
    def observe(final=False):
        observations={};safe={}
        # All finite metadata admission precedes any expanded body hashing.
        for path,digest in monitored.items():
            try:
                m=metadata(path)
                if final: assert path in before and m==before[path]
                elif path in initial_controls: assert m==initial_controls[path]
                safe[path]=m;observations[path]={'metadata':'PASS','stat':m}
            except BaseException as error:
                observations[path]={'metadata':'HOLD','error_type':type(error).__name__}
        if not final:
            before.update(safe)
            if len(safe)!=len(monitored): return observations
        for path,m in safe.items():
            try:
                read(path,monitored[path]);assert metadata(path)==m
                observations[path]['hash']='PASS'
            except BaseException as error:
                observations[path]['hash']='HOLD';observations[path]['error_type']=type(error).__name__
        return observations
    try:
        startup_inventory=startup(initial_controls)
        cancellation_point()
        source=D/'SOURCE.sha256'
        initial_controls[str(source)]=metadata(source)
        raw=read(source,sys.argv[2]);controls={}
        for line in raw.decode().splitlines():
            digest,name=line.split('  ',1)
            assert len(digest)==64 and all(c in '0123456789abcdef' for c in digest)
            assert name in {'supervisor.py','launch.sh','PLAN.md'} and name not in controls
            controls[name]=digest
        assert set(controls)=={'supervisor.py','launch.sh','PLAN.md'}
        monitored[str(source)]=sys.argv[2]
        for name,digest in controls.items(): monitored[str(D/name)]=digest
        prepared=O/'PREPARED.json';allow=O/'ALLOW.json'
        initial_controls[str(prepared)]=metadata(prepared)
        initial_controls[str(allow)]=metadata(allow)
        receipt=json.loads(read(prepared,PREPARED_SHA))
        assert receipt['status']=='MATERIALIZED_ONLY' and receipt['execution_selected'] is False
        assert receipt['packet_sha256']==PACKET_SHA and receipt['allow_sha256']==ALLOW_SHA
        assert receipt['declared_cases']==468 and len(receipt['original_inputs'])==2841 and len(receipt['closure'])==3053
        assert json.loads(read(allow,ALLOW_SHA))==receipt['closure']
        monitored.update(receipt['original_inputs']);monitored.update(receipt['closure'])
        monitored[str(prepared)]=PREPARED_SHA;monitored[str(allow)]=ALLOW_SHA
        initial=observe();external_dump('BEFORE.json',initial)
        assert len(initial)==len(monitored) and all(v.get('hash')=='PASS' for v in initial.values())
        external_dump('INVOCATION.json',{'argv':sys.argv,'cwd':str(Path.cwd()),'env':{'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'},'packet_sha256':PACKET_SHA,'prepared_sha256':PREPARED_SHA,'allow_sha256':ALLOW_SHA,'source_sha256':sys.argv[2],'startup_inventory':startup_inventory})
        cancellation_point()
        result=execute()
    except BaseException as error: primary=type(error).__name__
    finally:
        try:
            after=observe(True)
            external_dump('AFTER.json',after)
            assert monitored and len(after)==len(monitored) and all(v.get('hash')=='PASS' for v in after.values())
        except BaseException as error: final_errors.append('closure:'+type(error).__name__)
        if receipt is not None:
            for branch in ("baseline","candidate","harness","sa20","sa21"):
                try:
                    namespace(O/branch,{n for n in receipt['closure'] if Path(n).is_relative_to(O/branch)})
                    namespace_results[branch]='PASS'
                except BaseException as error:
                    namespace_results[branch]=type(error).__name__;final_errors.append('namespace:'+branch)
        else: final_errors.append('namespace:NOT_ADMITTED')
        try:
            absences()
        except BaseException as error: final_errors.append('absence:'+type(error).__name__)
        summary={'primary_failure':primary,'closure_failures':final_errors,'namespaces':namespace_results,'received_signal':received_signal,'unchanged':not final_errors,'trusted_bootstrap_inventory':startup_inventory,'child_history':child_history}
        try: external_dump('CLOSURE_FINAL.json',summary)
        except BaseException as error: final_errors.append('receipt:'+type(error).__name__)
        if (O/'results').is_dir():
            try: dump(O/'results'/'CLOSURE_FINAL.json',summary)
            except BaseException as error: final_errors.append('output_receipt:'+type(error).__name__)
    # A signal during any evidence write is checked again before and after the
    # nominal result. Receipts alone never qualify a nonzero/signalled attempt.
    try:
        cancellation_point()
        assert primary is None and not final_errors and result is not None
        dump(O/'results'/'RESULT.json',result)
        cancellation_point()
        external_dump('TERMINAL.json',{'status':'COMPLETED_CORRECTNESS_ONLY','received_signal':received_signal,'source_sha256':sys.argv[2],'prepared_sha256':PREPARED_SHA})
        cancellation_point()
    except BaseException:
        # If success receipt already exists, retained exit/nonzero signal state
        # overrides it. No overwrite/delete or adaptive rerun is attempted.
        if not os.path.lexists(R/'TERMINAL.json'):
            external_dump('TERMINAL.json',{'status':'HOLD','primary_failure':primary,'closure_failures':final_errors,'received_signal':received_signal})
        return 1
    return 0

if __name__=='__main__':
    code=main()
    raise SystemExit(1 if received_signal is not None else code)

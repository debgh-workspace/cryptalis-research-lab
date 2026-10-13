"""Disposable independent process for durable reverse transitions and death."""
from pathlib import Path
from uuid import UUID
import os,signal,sys
from cryptalis import deprotection as d
from cryptalis import migration as m
from test_migration import engine,keys
artifact,phase,pin_phase,mode=sys.argv[1:]
p=d.DeprotectionPlan(Path(artifact).read_bytes())
pin=m.DeploymentPin(p.target_id,p.operation_id,p.digest,pin_phase)
consent=d.PlaintextApproval(p.target_id,p.operation_id,p.digest,True,'Public fixture backup reader retained')
e=engine('CRYPTALIS_TEST_DATABASE_URL')
if mode=='kill_second_chunk':
    from sqlalchemy import event
    updates=[0]
    def kill_after_second_update(conn,cursor,statement,params,context,many):
        if statement.startswith('UPDATE ') and '_plain"' in statement:
            updates[0]+=1
            if updates[0]==2:os.kill(os.getpid(),signal.SIGKILL)
    event.listen(e,'after_cursor_execute',kill_after_second_update)

try:
    result=d.apply(p,e,keys=keys,pin=pin,approval=m.MaintenanceApproval('Synthetic operator excluded privileged writers',3600),plaintext_approval=consent,chunk_size=2,until=phase)
    print(result.phase,flush=True)
    if mode=='pause':signal.pause()
finally:e.dispose()

"""Real PG chunks, durable-prefix and independent-frame oracles for renewal."""
from types import SimpleNamespace
import pytest
from sqlalchemy import event
import cryptalis.crypto.keys as key_module
from cryptalis.crypto import Keyring
from test_migration import application, keys, TENANT, PROVIDER, PublicFixtureProvider, run, frames, independent_open

@pytest.fixture
def clock(monkeypatch):
    now=[100.0]
    monkeypatch.setattr(key_module,'time',SimpleNamespace(monotonic=lambda:now[0],monotonic_ns=lambda:int(now[0]*1e9)))
    return now

class Provider(PublicFixtureProvider):
    def __init__(self):self.calls=[];self.offline=False;self.failed=False
    def unwrap(self,wrapper,context):
        self.calls.append(context.purpose)
        if self.offline:
            self.failed=True
            raise RuntimeError('PRIVATE_PROVIDER_DIAGNOSTIC')
        return super().unwrap(wrapper,context)

def ring_for(provider):
    return Keyring(keys(TENANT).policy,{PROVIDER:provider},max_age=10)

def test_near_expiry_chunk_prepares_before_sealing(clock,monkeypatch):
    p=Provider();ring=ring_for(p);ring.prepare();assert len(p.calls)==2
    with application(rows=2) as app:
        clock[0]=109.5;native=app.m.seal_text
        def slow_seal(*args,**kwargs):
            clock[0]+=.3
            return native(*args,**kwargs)
        monkeypatch.setattr(app.m,'seal_text',slow_seal)
        result=run(app,until='BACKFILLED',key_resolver=ring)
        assert result.committed_rows==2 and len(p.calls)==4
        desc=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        assert {r:independent_open(f,desc,TENANT,r) for r,f in frames(app).items()}=={r:v for r,(t,v) in app.source.items()}

def test_outage_next_chunk_preserves_prefix_and_emits_nothing_after_failed_prepare(clock,monkeypatch):
    p=Provider();ring=ring_for(p);ring.prepare()
    with application(rows=4) as app:
        original=app.m._backfill_chunk;calls=[];prefix={};after_failure=[]
        def chunk(*args,**kwargs):
            result=original(*args,**kwargs);calls.append(result)
            if len(calls)==1:
                # Called before this chunk commits; next iteration sees outage.
                clock[0]=109.5;p.offline=True
            return result
        monkeypatch.setattr(app.m,'_backfill_chunk',chunk)
        def emitted(*args):
            if p.failed:after_failure.append(args[2])
        event.listen(app.owner,'before_cursor_execute',emitted)
        try:
            with pytest.raises(app.m.TransitionFailure) as err:run(app,until='BACKFILLED',key_resolver=ring)
            assert err.value.code=='KeyUnavailable' and 'PRIVATE_PROVIDER' not in str(err.value)
            assert after_failure==[]
        finally:event.remove(app.owner,'before_cursor_execute',emitted)
        bodies=frames(app);ordered=sorted(bodies)
        assert bodies[ordered[1]] is not None
        assert all(bodies[r] is None for r in ordered[2:])
        with app.owner.connect() as c:
            state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal').scalar_one()
        progress=next(iter(state['models'].values()))
        assert progress['rows']==2 and progress['chunks']==1
        prefix={r:bodies[r] for r in ordered[:2]}
        p.offline=False;p.failed=False
        result=run(app,until='BACKFILLED',key_resolver=ring)
        assert result.committed_rows==4
        assert {r:frames(app)[r] for r in prefix}==prefix
        desc=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        assert {r:independent_open(f,desc,TENANT,r) for r,f in frames(app).items()}=={r:v for r,(t,v) in app.source.items()}

def test_expiry_and_outage_mid_batch_roll_back_only_current_chunk(clock,monkeypatch):
    p=Provider();ring=ring_for(p);ring.prepare()
    with application(rows=4) as app:
        native=app.m.seal_text;sealed=[];writes=[]
        def seal(*args,**kwargs):
            sealed.append(1)
            if len(sealed)==3:
                p.offline=True;clock[0]=109.9
            elif len(sealed)==4:clock[0]=110.1
            return native(*args,**kwargs)
        monkeypatch.setattr(app.m,'seal_text',seal)
        def emitted(conn,cursor,statement,parameters,context,many):
            if statement.startswith('UPDATE ') and '."customer" SET ' in statement:writes.append(statement)
        event.listen(app.owner,'before_cursor_execute',emitted)
        try:
            with pytest.raises(app.m.TransitionFailure) as error:run(app,until='BACKFILLED',key_resolver=ring)
            assert error.value.code=='KeyUnavailable'
            assert len(writes)==1  # first chunk only; second never emits UPDATE
        finally:event.remove(app.owner,'before_cursor_execute',emitted)
        prefix=frames(app);ordered=sorted(prefix)
        assert prefix[ordered[1]] is not None and all(prefix[r] is None for r in ordered[2:])
        monkeypatch.setattr(app.m,'seal_text',native)
        emitted_after=[]
        def after(*args):
            if p.failed:emitted_after.append(1)
        event.listen(app.owner,'before_cursor_execute',after)
        try:
            with pytest.raises(app.m.TransitionFailure):run(app,until='BACKFILLED',key_resolver=ring)
            assert p.failed and emitted_after==[]
        finally:event.remove(app.owner,'before_cursor_execute',after)
        assert frames(app)==prefix
        p.offline=False;p.failed=False
        assert run(app,until='BACKFILLED',key_resolver=ring).committed_rows==4
        final=frames(app)
        assert all(final[r]==prefix[r] for r in ordered[:2])
        desc=app.plan.document['lock']['models'][0]['fields'][0]['descriptor']
        assert {r:independent_open(f,desc,TENANT,r) for r,f in final.items()}=={r:v for r,(t,v) in app.source.items()}

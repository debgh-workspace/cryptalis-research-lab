"""Provider-count and actual crypto-use oracles for bounded chunk leases."""
import asyncio
from types import SimpleNamespace
import pytest
import cryptalis.crypto.keys as module
from cryptalis.crypto import DevelopmentKeyProvider, KeyUnavailable, InvalidContext
from test_cf1 import setup_keys, descriptor, TENANT, RECORD
from cryptalis.crypto import seal_text, open_text

@pytest.fixture
def clock(monkeypatch):
    now=[100.0]
    monkeypatch.setattr(module,'time',SimpleNamespace(monotonic=lambda:now[0],monotonic_ns=lambda:int(now[0]*1e9)))
    return now

class CountingProvider(DevelopmentKeyProvider):
    def __init__(self):
        super().__init__();self.calls=[];self.offline=False;self.after=None
    def unwrap(self, wrapper, context):
        self.calls.append(context.purpose)
        if self.offline:raise RuntimeError('PROVIDER_SECRET_MUST_NOT_ESCAPE')
        root=super().unwrap(wrapper,context)
        if self.after:self.after(context)
        return root


def prepare(ring, asynchronous, **kw):
    return asyncio.run(ring.prepare_async(**kw)) if asynchronous else ring.prepare(**kw)

def read(keys):
    f=descriptor(equality=True)
    return open_text(seal_text('exact-value',f,TENANT,RECORD,keys),f,TENANT,RECORD,keys)

@pytest.mark.parametrize('asynchronous',[False,True])
def test_near_expiry_renews_through_provider_without_extending_old_snapshot(clock,asynchronous):
    p,ring=setup_keys(equality=True,max_age=10,provider=CountingProvider())
    old=prepare(ring,asynchronous);assert len(p.calls)==2
    clock[0]=105
    assert read(prepare(ring,asynchronous,minimum_validity=1))=='exact-value'
    assert len(p.calls)==2
    clock[0]=109.5
    fresh=prepare(ring,asynchronous,minimum_validity=1)
    assert len(p.calls)==4 and read(fresh)=='exact-value'
    clock[0]=110
    with pytest.raises(KeyUnavailable):read(old)
    assert read(fresh)=='exact-value'
    clock[0]=119.5
    with pytest.raises(KeyUnavailable):read(fresh)

@pytest.mark.parametrize('asynchronous',[False,True])
def test_provider_outage_during_renewal_has_no_stale_fallback(clock,asynchronous):
    p,ring=setup_keys(equality=True,max_age=10,provider=CountingProvider())
    old=prepare(ring,asynchronous);clock[0]=109.5;p.offline=True
    with pytest.raises(KeyUnavailable) as error:prepare(ring,asynchronous,minimum_validity=1)
    assert 'PROVIDER_SECRET' not in str(error.value)
    # An already-issued lease remains valid until its original deadline;
    # this does not assert instantaneous revocation or offline detection.
    assert read(old)=='exact-value'
    clock[0]=110
    with pytest.raises(KeyUnavailable):read(old)

@pytest.mark.parametrize('asynchronous',[False,True])
def test_provider_latency_counts_against_total_lease_age(clock,asynchronous):
    p,ring=setup_keys(equality=True,max_age=10,provider=CountingProvider())
    p.after=lambda context:clock.__setitem__(0,clock[0]+4.6)
    with pytest.raises(KeyUnavailable):prepare(ring,asynchronous,minimum_validity=1)
    assert len(p.calls)==2
    p.after=None;p.offline=True
    # The failed preparation must not publish partially usable roots.
    with pytest.raises(KeyUnavailable):prepare(ring,asynchronous)

@pytest.mark.parametrize('budget',[-1,True,None,'1',float('nan'),float('inf'),10,11])
@pytest.mark.parametrize('asynchronous',[False,True])
def test_invalid_chunk_budget_refuses_before_provider(clock,budget,asynchronous):
    p,ring=setup_keys(equality=True,max_age=10,provider=CountingProvider())
    with pytest.raises(InvalidContext):prepare(ring,asynchronous,minimum_validity=budget)
    assert p.calls==[]


def test_cancelled_renewal_does_not_publish_partial_roots(clock):
    async def scenario():
        entered=asyncio.Event()
        class Waiting(CountingProvider):
            async def unwrap_async(self,wrapper,context):
                root=self.unwrap(wrapper,context)
                if context.purpose=='search':
                    entered.set()
                    try:await asyncio.Future()
                    except asyncio.CancelledError:pass
                return root
        p,ring=setup_keys(equality=True,max_age=10,provider=Waiting())
        task=asyncio.create_task(ring.prepare_async(minimum_validity=1))
        await entered.wait();task.cancel()
        with pytest.raises(asyncio.CancelledError):await task
        p.offline=True
        with pytest.raises(KeyUnavailable):ring.prepare()
    asyncio.run(scenario())

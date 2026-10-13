"""Synthetic roots only. File custody is development functionality, not KMS."""
import asyncio,hashlib,importlib,json,os,subprocess,sys
from dataclasses import replace
from uuid import UUID
import pytest
from cryptalis.crypto import KeyContext,KeyUnavailable

CONTEXT=KeyContext(UUID(int=1),UUID(int=2),'payload',UUID(int=3),1)
ROOT=b'public development test root!!!!'
ROOT=hashlib.sha256(ROOT).digest()

def provider_type():return getattr(importlib.import_module('cryptalis.crypto'),'FileDevelopmentKeyProvider')


def test_fresh_process_reopens_exact_provider_and_unwraps(tmp_path):
    cls=provider_type();path=tmp_path/'custody.key';provider=cls.create(path)
    wrapped=provider.wrap(ROOT,CONTEXT)
    payload={'path':str(path),'provider':str(provider.provider_id),'sealed':wrapped.sealed.hex()}
    code='''import json,sys,hashlib
from uuid import UUID
from cryptalis.crypto import FileDevelopmentKeyProvider,KeyContext,WrappedRoot
p=json.load(sys.stdin);provider=FileDevelopmentKeyProvider.open(p['path'])
c=KeyContext(UUID(int=1),UUID(int=2),'payload',UUID(int=3),1)
w=WrappedRoot(UUID(p['provider']),c,bytes.fromhex(p['sealed']))
assert provider.provider_id==w.provider_id
print(hashlib.sha256(provider.unwrap(w,c)).hexdigest())
'''
    result=subprocess.run([sys.executable,'-c',code],input=json.dumps(payload),text=True,capture_output=True,check=True)
    assert result.stdout.strip()==hashlib.sha256(ROOT).hexdigest()
    assert asyncio.run(cls.open(path).unwrap_async(wrapped,CONTEXT))==ROOT
    assert path.stat().st_mode & 0o777 == 0o600


def test_existing_file_is_never_overwritten(tmp_path):
    cls=provider_type();path=tmp_path/'custody.key';cls.create(path);before=path.read_bytes()
    with pytest.raises(KeyUnavailable):cls.create(path)
    assert path.read_bytes()==before


@pytest.mark.parametrize('variant',['missing','truncated','extra','corrupt','mode','symlink','hardlink','directory'])
def test_unsafe_or_lost_custody_fails_closed(tmp_path,variant):
    cls=provider_type();path=tmp_path/'custody.key';cls.create(path)
    if variant=='missing':path.unlink()
    elif variant=='truncated':path.write_bytes(path.read_bytes()[:-1])
    elif variant=='extra':path.write_bytes(path.read_bytes()+b'x')
    elif variant=='corrupt':
        blob=bytearray(path.read_bytes());blob[25]^=1;path.write_bytes(blob)
    elif variant=='mode':path.chmod(0o644)
    elif variant=='symlink':
        target=tmp_path/'real.key';path.rename(target);path.symlink_to(target)
    elif variant=='hardlink':os.link(path,tmp_path/'other.key')
    elif variant=='directory':path.unlink();path.mkdir()
    with pytest.raises(KeyUnavailable) as error:cls.open(path)
    assert str(path) not in str(error.value)
    if variant=='missing':assert not path.exists()


def test_reopened_provider_preserves_wrapper_context_authentication(tmp_path):
    cls=provider_type();path=tmp_path/'custody.key';provider=cls.create(path);wrapped=provider.wrap(ROOT,CONTEXT)
    reopened=cls.open(path)
    with pytest.raises(KeyUnavailable):reopened.unwrap(wrapped,replace(CONTEXT,tenant_id=UUID(int=4)))
    with pytest.raises(KeyUnavailable):reopened.unwrap(replace(wrapped,sealed=wrapped.sealed[:-1]+bytes([wrapped.sealed[-1]^1])),CONTEXT)


def test_inherited_provider_cannot_unwrap_after_fork(tmp_path):
    cls=provider_type();provider=cls.create(tmp_path/'custody.key');wrapped=provider.wrap(ROOT,CONTEXT)
    pid=os.fork()
    if pid==0:
        try:provider.unwrap(wrapped,CONTEXT)
        except KeyUnavailable:os._exit(0)
        except BaseException:os._exit(2)
        os._exit(1)
    _,status=os.waitpid(pid,0)
    assert os.waitstatus_to_exitcode(status)==0
    assert provider.unwrap(wrapped,CONTEXT)==ROOT


def test_nonregular_fifo_is_rejected_without_waiting_for_a_writer(tmp_path):
    cls=provider_type();path=tmp_path/'pipe';os.mkfifo(path,0o600)
    code='''import sys
from cryptalis.crypto import FileDevelopmentKeyProvider,KeyUnavailable
try: FileDevelopmentKeyProvider.open(sys.argv[1])
except KeyUnavailable: sys.exit(0)
sys.exit(1)
'''
    result=subprocess.run([sys.executable,'-c',code,str(path)],capture_output=True,timeout=2)
    assert result.returncode==0


def test_partial_file_creation_is_loud_and_never_regenerated(tmp_path,monkeypatch):
    cls=provider_type();path=tmp_path/'partial.key';original=os.write;calls=[]
    def fail_after_prefix(fd,body):
        if calls:raise OSError('private failure marker')
        calls.append(1);return original(fd,body[:3])
    with monkeypatch.context() as patch:
        patch.setattr(os,'write',fail_after_prefix)
        with pytest.raises(KeyUnavailable) as error:cls.create(path)
    assert path.stat().st_size==3
    assert 'may exist' in error.value.effects
    assert 'private failure marker' not in str(error.value)
    with pytest.raises(KeyUnavailable):cls.open(path)
    with pytest.raises(KeyUnavailable):cls.create(path)
    assert path.stat().st_size==3


def test_short_reads_and_close_failure_keep_safe_outcomes(tmp_path,monkeypatch):
    cls=provider_type();path=tmp_path/'custody.key';provider=cls.create(path);wrapped=provider.wrap(ROOT,CONTEXT)
    original_read=os.read
    with monkeypatch.context() as patch:
        patch.setattr(os,'read',lambda fd,n:original_read(fd,min(n,3)))
        assert cls.open(path).unwrap(wrapped,CONTEXT)==ROOT
    original_close=os.close;calls=[]
    def close_then_fail(fd):
        original_close(fd)
        if not calls: calls.append(1);raise OSError('private close marker')
    with monkeypatch.context() as patch:
        patch.setattr(os,'close',close_then_fail)
        with pytest.raises(KeyUnavailable) as error:cls.open(path)
    assert 'private close marker' not in str(error.value)
    assert cls.open(path).unwrap(wrapped,CONTEXT)==ROOT


def test_unsafe_parent_permissions_refuse_creation(tmp_path):
    cls=provider_type();directory=tmp_path/'unsafe';directory.mkdir();directory.chmod(0o770)
    with pytest.raises(KeyUnavailable):cls.create(directory/'custody.key')
    assert not (directory/'custody.key').exists()


def test_wrong_file_owner_check_is_enforced(tmp_path,monkeypatch):
    cls=provider_type();path=tmp_path/'custody.key';cls.create(path);uid=os.getuid();calls=[]
    def observed_uid():
        calls.append(1);return uid if len(calls)==1 else uid+1
    with monkeypatch.context() as patch:
        patch.setattr(os,'getuid',observed_uid)
        with pytest.raises(KeyUnavailable):cls.open(path)

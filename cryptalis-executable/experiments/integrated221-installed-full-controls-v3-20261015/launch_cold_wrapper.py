"""One-purpose cold-cache environment adapter for the unchanged guarded wrapper."""
import sys
import runpy
from pathlib import Path
import hashlib
import stat

BASE=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
WRAPPER=BASE/'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py'
if not sys.dont_write_bytecode:
    raise RuntimeError('Launcher requires explicit -B before any wrapper import')
for path in [WRAPPER,*WRAPPER.parents]:
    mode=path.lstat().st_mode
    if not (stat.S_ISREG(mode) if path==WRAPPER else stat.S_ISDIR(mode)):
        raise RuntimeError('Unadmitted wrapper path')
if hashlib.sha256(WRAPPER.read_bytes()).hexdigest()!='e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453':
    raise RuntimeError('Wrapper identity changed')
sys.path[0]=str(WRAPPER.parent)
sys.argv[0]=str(WRAPPER)
namespace=runpy.run_path(str(WRAPPER),run_name='__cold_cache_wrapper__')
main=namespace['main']
ENV=namespace['ENV']
baseline_environment=sys.modules['run_baseline'].ENV
if ENV is not baseline_environment or main.__globals__['ENV'] is not ENV:
    raise RuntimeError('Wrapper environment identity changed')
if set(ENV)!={'HOME','PATH','LANG','TZ'}:
    raise RuntimeError('Wrapper fixed environment schema changed')
ENV['PYTHONDONTWRITEBYTECODE']='1'
raise SystemExit(main())

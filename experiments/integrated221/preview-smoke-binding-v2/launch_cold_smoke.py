"""One-purpose cold-cache environment adapter for the unchanged guarded wrapper."""
# HELD additive V5 binding; only the separately reviewed root entry may select it.
import sys
import runpy
from pathlib import Path
import hashlib
import stat
import os

BASE=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
WRAPPER=BASE/'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py'
IDENTITY = BASE/'evidence/preview-identity-capture-v3-sa21-20261015/safe-identity.json'
IDENTITY_SHA = '089bac088003d7921f755409509afed5544741ebfee8af66faea0776fbfbb92c'
if not sys.dont_write_bytecode:
    raise RuntimeError('Launcher requires explicit -B before any wrapper import')
if sys.flags.optimize:
    raise RuntimeError('Enabled assertions required')
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
# Same three V5 finite-operation acknowledgement guards; no authority implied.
ENV['CRYPTALIS_PREVIEW_REVIEWED_EXECUTION'] = '20261015-single-synthetic-smoke'
ENV['CRYPTALIS_PREVIEW_PLAINTEXT_APPROVED'] = 'two-reverse-operations'
ENV['CRYPTALIS_PREVIEW_CUTOVER_APPROVED'] = 'existing-positive-activation-helper'
for key, expected in (
    ('CRYPTALIS_PREVIEW_IDENTITY_FILE', str(IDENTITY)),
    ('CRYPTALIS_PREVIEW_IDENTITY_SHA256', IDENTITY_SHA),
):
    if os.environ.get(key) != expected:
        raise RuntimeError('Exact accepted identity binding required')
    ENV[key] = expected
raise SystemExit(main())

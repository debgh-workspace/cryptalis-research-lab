"""Inert source-only recovery. Never imports or executes restored product/test files."""
import argparse, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
ROOT=Path('/workspace/scratch/cb28ee9f5f4a')
BASE=ROOT/'cryptalis-executable/reviewer-notes/doctor-full-source-restore-independent-20261016/restored-source221'
MAPS=[(ROOT/'cryptalis-executable/experiments/orm-flush-diagnostic-unit-packet-v7-20261016/BASELINE_SOURCE_MAP.json','f704908bfb482b78312865f79400b0455fc3fced41664b8d3598e4084f6fd985'),(ROOT/'cryptalis-executable/experiments/orm-flush-state-unit-packet-v1-20261016/AMENDED_SOURCE_MAP.json','d2ace8320a60b6cf9b7d8472ca4819efe5129f6130e800a5958951266ef2f6ff')]
KEYS=['src/cryptalis/_sqlalchemy_transactions.py','src/cryptalis/sqlalchemy.py']
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def ancestors(p):
 for q in list(p.parents)[::-1]:
  if not stat.S_ISDIR(q.lstat().st_mode):raise ValueError('Nonordinary ancestor: '+str(q))
def admit(p,size=None):
 ancestors(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_size>8*1024*1024 or (size is not None and s.st_size!=size):raise ValueError('Metadata mismatch: '+str(p))
 return identity(s)
def read(p,meta,digest=None):
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  if identity(os.fstat(fd))!=meta:raise ValueError('Changed input')
  with os.fdopen(fd,'rb',closefd=False) as f:b=f.read()
  if identity(os.fstat(fd))!=meta:raise ValueError('Changed during read')
 finally:os.close(fd)
 if identity(p.lstat())!=meta:raise ValueError('Changed path')
 b.decode('utf-8')
 if b'\0' in b or (digest and hashlib.sha256(b).hexdigest()!=digest):raise ValueError('Text/hash mismatch: '+str(p))
 return b
def namespace(base,keys):
 ancestors(base/'placeholder')
 expected_dirs={'.'}
 for k in keys:
  pp=PurePosixPath(k)
  if pp.is_absolute() or '..' in pp.parts or str(pp)!=k:raise ValueError('Unsafe key')
  expected_dirs.update(str(x) for x in pp.parents)
 files=set();dirs={'.'}
 for parent,ds,fs in os.walk(base,followlinks=False):
  for n in ds:
   p=Path(parent)/n
   if not stat.S_ISDIR(p.lstat().st_mode):raise ValueError('Nonordinary dir')
   dirs.add(str(p.relative_to(base)))
  for n in fs:
   p=Path(parent)/n;files.add(str(p.relative_to(base)))
 if files!=set(keys) or dirs!=expected_dirs:raise ValueError('Namespace mismatch: '+str(base))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--overlay-root',required=True);ap.add_argument('--output',required=True);ap.add_argument('--provenance',choices=['local-only','root-supplied-remote-bytes'],required=True);a=ap.parse_args()
 overlay=Path(a.overlay_root);out=Path(a.output)
 for p in [overlay,out]:
  if not p.is_absolute() or '..' in p.parts:raise ValueError('Absolute normalized path required')
 if not out.is_relative_to(ROOT/'persistence-recovery-20261013') or out.exists():raise ValueError('Fresh recovery output required')
 if not overlay.is_relative_to(ROOT):raise ValueError('Overlay must be root-supplied workspace data')
 maps=[json.loads(read(p,admit(p),sha)) for p,sha in MAPS];bm,am=maps
 if len(bm)!=221 or set(bm)!=set(am) or sorted(k for k in bm if bm[k]!=am[k])!=KEYS:raise ValueError('Map shape/delta mismatch')
 namespace(BASE,bm)
 # Admit the entire finite leaf set before any source-body read.
 pins={BASE/k:admit(BASE/k,v['bytes']) for k,v in bm.items()}
 pins.update({overlay/Path(k).name:admit(overlay/Path(k).name,am[k]['bytes']) for k in KEYS})
 bodies={k:read(BASE/k,pins[BASE/k],v['sha256']) for k,v in bm.items()}
 for k in KEYS:bodies[k]=read(overlay/Path(k).name,pins[overlay/Path(k).name],am[k]['sha256'])
 out.mkdir(mode=0o700)
 for k,b in bodies.items():
  p=out/k;p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
  fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'wb') as f:f.write(b)
 namespace(out,am)
 for k,v in am.items():
  p=out/k;read(p,admit(p,v['bytes']),v['sha256'])
  if p.stat().st_ino==(BASE/k).stat().st_ino:raise ValueError('Shared inode')
 for p,m in pins.items():
  if admit(p)!=m:raise ValueError('Input metadata changed')
 # Rehash the inputs after output verification; preserve any failure and never retry in place.
 for k,v in bm.items():read(BASE/k,pins[BASE/k],v['sha256'])
 for k in KEYS:read(overlay/Path(k).name,pins[overlay/Path(k).name],am[k]['sha256'])
 print(json.dumps({'status':'PASS_INERT_SOURCE221_RECONSTRUCTION','files':221,'bytes':sum(v['bytes'] for v in am.values()),'amended_source_map_sha256':MAPS[1][1],'overlay_paths':KEYS,'output':str(out),'provenance':a.provenance,'remote_fetch_verified_by_this_script':False,'product_execution':False,'environment_recovery':False},indent=2))
if __name__=='__main__':main()

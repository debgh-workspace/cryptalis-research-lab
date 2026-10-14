"""Data-only frozen-input validation/archive. No product/dependency imports."""
from pathlib import Path
import argparse, hashlib, json, re, shutil
B=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
PACKETS={B/'experiments/async-cleanup-full-integration-plan-20261014',B/'experiments/async-cleanup-sqlmodel-overlay-plan-20261014'}
DENIED={'tests.json','readiness.json','package-origin.json','postgres-start.json','postgres-stop.json'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--packet',type=Path,required=True)
parser.add_argument('--clearance',required=True)
parser.add_argument('--archive',type=Path)
a=parser.parse_args();P=a.packet
assert P in PACKETS and P.resolve()==P
assert a.clearance in {'CLEARANCE_MAIN_SA21.sha256','CLEARANCE_MAIN_SA20.sha256','CLEARANCE_OPTIONAL38.sha256'}
# Read only this fixed interpreter-target map before validating symlinks.
interpreter_file=P/'INTERPRETER_TARGETS.json'
assert interpreter_file.resolve()==interpreter_file and not interpreter_file.is_symlink()
INTERPS={Path(k):Path(v) for k,v in json.loads(interpreter_file.read_bytes()).items()}
expected_interps={B/'repo/.venv/bin/python',*(B/f'release-lab/s25-installed-20261014/{c}/bin/python' for c in ('sa20','sa21')),B/'release-lab/cp84-adoption/sqlmodel-wheel-venv/bin/python'}
assert set(INTERPS)==expected_interps
for p,v in INTERPS.items():
 assert v==(B/'apps/runtime/python/cpython-3.14.8-linux-x86_64-gnu/bin/python3.14' if 'sqlmodel-wheel-venv' in str(p) else Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'))
def safe(p):
 assert p.is_absolute() and p.is_relative_to(B) and '..' not in p.parts,p
 assert p.name not in DENIED and not any(x in str(p).lower() for x in ('password','credential','secret','.cryptalis-test')),p
 assert not any(x.lower() in {'environment','environment.json','.env'} or x.lower().startswith('.env.') for x in p.parts),p
 assert p.is_file() and p.resolve(strict=True)==INTERPS.get(p,p),p
 if p not in INTERPS:assert not p.is_symlink(),p
 return p
def read(p):return safe(p).read_bytes()
def digest(p):return hashlib.sha256(read(p)).hexdigest()
def parse_manifest(p):
 rows=[]
 for line in read(p).decode().splitlines():
  m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);assert m,p
  h,raw=m.groups();q=Path(raw);safe(q);rows.append((q,h))
 assert len(rows)==len({q for q,h in rows}) and rows,p
 return rows
names=read(P/'PACKET_FILES.txt').decode().splitlines()
assert len(names)==len(set(names)) and names==sorted(names)
for n in names:
 r=Path(n);assert not r.is_absolute() and '..' not in r.parts and not any(x.startswith('.') for x in r.parts),n
 assert r.suffix in {'.py','.sh','.txt','.md','.json','.sha256','.patch','.tsv'}
 safe(P/r)
packet_rows=parse_manifest(P/'PACKET.sha256')
assert {q for q,h in packet_rows}=={P/n for n in names}
inputs=json.loads(read(P/'SAFE_INPUTS.json'))
input_rows=parse_manifest(P/'INPUTS.sha256')
assert {str(q):h for q,h in input_rows}==inputs
source_roots={B/'candidate-next-unblocked-correctness-20261014',B/'candidate-s25-async-sqlmodel-integration-20261014'}
source_tops={'AGENTS.md','ENGINEERING_PLAYBOOK.md','LICENSE','README.md','docs','examples','experiments','pyproject.toml','scripts','src','tests','uv.lock'}
evidence_basenames={'junit.xml','progress.jsonl','runner-receipt.json','readiness.log','package-origin.log','postgres-stop.log','source-stability.json','source-root.json','prior-corpus-manifest.json','candidate-corpus-isolation.json','async-sqlmodel-origin.jsonl'}
explicit_sources={B/'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py',B/'candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py',B/'repo/scripts/test_postgres.py',B/'toolchain/lab_progress.py',B/'toolchain/run_baseline.py'}
old_packet_names={'BASELINE_SOURCE_MANIFEST.json','GREEN_SOURCE_MANIFEST.json','NEW_NODE_IDS.txt','SOURCE_DELTA.patch','PLAN.md','PREPARATION_CHECKS.json','NATIVE_SOURCE_PINS.sha256'}
corpus_re=re.compile(r'(?:master-s4-)?compatibility[^/]*corpus-v1-sa[^/]*\.json')
def allow_input(q):
 if q in INTERPS or q in explicit_sources:return
 for root in source_roots:
  if q.is_relative_to(root):
   r=q.relative_to(root);assert r.parts[0] in source_tops and (r.suffix in {'.py','.md','.json','.toml','.lock','.hex'} or str(r)=='LICENSE')
   if r.parts[0]=='experiments':assert str(r)=='experiments/manifest_setup_fastapi_models.py'
   return
 if q.parent==B/'experiments/next-unblocked-correctness-20261014':assert q.name in old_packet_names;return
 if q.parent==B/'evidence':assert corpus_re.fullmatch(q.name);return
 if q.is_relative_to(B/'evidence'):
  assert q.parent.parent==B/'evidence' and q.parent.name in {'s25-async-sqlmodel-integration-sa21-20261014','s25-async-sqlmodel-integration-sa20-20261014','s25-installed-full-sa21-20261014','s25-installed-full-sa20-20261014','s25-async-sqlmodel-integration-sqlmodel-20261014'}
  assert q.name in evidence_basenames;return
 if q.is_relative_to(B/'reviewer-notes'):
  if q.parent.name in {'async-cleanup-green-sa21-independent-20261014','async-cleanup-green-sa20-independent-20261014'}:
   assert q.parent.parent==B/'reviewer-notes' and q.name in {'review.md','audit-summary.json','node-audit.json'};return
  assert q.parent.parent==B/'reviewer-notes' and q.parent.name in {'s25-integration-independent-20261014','s25-installed-full-independent-20261014','s25-installed-sa20-terminal-independent-20261014'}
  assert q.name in {'SA21_TERMINAL_REVIEW.md','SA20_TERMINAL_REVIEW.md','SQLMODEL_TERMINAL_REVIEW.md','SQLMODEL_TERMINAL_AUDIT.json'};return
 for prefix in [*(B/f'release-lab/s25-installed-20261014/{c}/lib/python3.12/site-packages' for c in ('sa20','sa21')),B/'release-lab/cp84-adoption/sqlmodel-wheel-venv/lib/python3.14/site-packages']:
  if q.is_relative_to(prefix):
   r=q.relative_to(prefix)
   assert (r.parts[0] in {'sqlalchemy','sqlmodel'} and r.suffix=='.py') or (len(r.parts)==2 and re.fullmatch(r'[A-Za-z0-9_.+-]+\.dist-info',r.parts[0]) and r.name=='METADATA')
   return
 raise AssertionError(('Unapproved input path',str(q)))
# Validate the complete path set before reading any listed payload bytes.
for q,h in input_rows:allow_input(q);assert re.fullmatch('[0-9a-f]{64}',h)
clearance=P/a.clearance
clearance_rows=parse_manifest(clearance)
for q,h in clearance_rows:
 assert q.parent.parent==B/'reviewer-notes' and re.fullmatch(r'async-cleanup-[a-z0-9-]+-20261014',q.parent.name),q
 assert q.suffix in {'.md','.json','.txt','.tsv'} and q.name not in DENIED,q
 assert not q.name.startswith('.'),q
for label,rows in [('PACKET',packet_rows),('INPUTS',input_rows),('CLEARANCE',clearance_rows)]:
 for q,h in rows:
  assert digest(q)==h,('Hash mismatch',str(q));print(str(q)+': OK')
 print(label+': '+str(len(rows))+' verified')
# Exact source inventories and unchanged dual-role preflight.
for name,root,n in [('CANDIDATE_SOURCE_MANIFEST.json',B/'candidate-next-unblocked-correctness-20261014',217),('BASELINE_SOURCE_MANIFEST.json',B/'candidate-s25-async-sqlmodel-integration-20261014',216)]:
 manifest=json.loads(read(P/name))['source_sha256'];assert len(manifest)==n
 assert all(inputs.get(str(root/rel))==h for rel,h in manifest.items())
 actual={str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}
 assert not set(manifest)-actual
 assert all('__pycache__' in Path(r).parts or '.pytest_cache' in Path(r).parts for r in actual-set(manifest))
assert read(B/'candidate-next-unblocked-correctness-20261014/scripts/test_postgres.py')==read(B/'repo/scripts/test_postgres.py')
source_names=read(P/'SOURCE_FILES.txt').decode().splitlines()
assert source_names==sorted(json.loads(read(P/'CANDIDATE_SOURCE_MANIFEST.json'))['source_sha256'])
corpus=json.loads(read(P/'CORPUS_BASELINE.json'));assert len(corpus)==26
for n,h in corpus.items():assert corpus_re.fullmatch(n) and inputs[str(B/'evidence'/n)]==h
actual_corpus={q.name for pat in ('compatibility*corpus-v1-sa*.json','master-s4-compatibility*corpus-v1-sa*.json') for q in (B/'evidence').glob(pat)}
assert actual_corpus==set(corpus)
if a.archive:
 dest=a.archive
 assert dest.is_absolute() and dest.is_relative_to(P/'run') and '..' not in dest.parts
 assert not dest.exists();dest.mkdir()
 for n in names+['PACKET.sha256',a.clearance]:
  target=dest/'packet'/n;target.parent.mkdir(parents=True,exist_ok=True)
  with target.open('xb') as f:f.write(read(P/n))
  assert target.read_bytes()==read(P/n)
 for rel in source_names:
  target=dest/'candidate-source'/rel;target.parent.mkdir(parents=True,exist_ok=True)
  with target.open('xb') as f:f.write(read(B/'candidate-next-unblocked-correctness-20261014'/rel))
  assert target.read_bytes()==read(B/'candidate-next-unblocked-correctness-20261014'/rel)
 print('Archived exact frozen packet, additive clearance, and 217 candidate source files')
print('Data-only verification complete; runtime result remains a separate claim')

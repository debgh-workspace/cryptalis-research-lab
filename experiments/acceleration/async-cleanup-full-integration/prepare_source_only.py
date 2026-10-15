"""Prepare two review packets using only validated source/data reads and writes."""
from pathlib import Path
import ast, collections, difflib, hashlib, json, re, shutil, xml.etree.ElementTree as ET
B=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
OLD=B/'experiments/next-unblocked-correctness-20261014'
P=B/'experiments/async-cleanup-full-integration-plan-20261014'
O=B/'experiments/async-cleanup-sqlmodel-overlay-plan-20261014'
C=B/'candidate-next-unblocked-correctness-20261014'
S=B/'candidate-s25-async-sqlmodel-integration-20261014'
DENIED={'tests.json','readiness.json','package-origin.json','postgres-start.json','postgres-stop.json'}
INTERPS={B/'repo/.venv/bin/python':Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'),**{B/f'release-lab/s25-installed-20261014/{c}/bin/python':Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12') for c in ('sa21','sa20')},B/'release-lab/cp84-adoption/sqlmodel-wheel-venv/bin/python':B/'apps/runtime/python/cpython-3.14.8-linux-x86_64-gnu/bin/python3.14'}
reads=set()
def safe(p):
 p=Path(p)
 assert p.is_absolute() and p.is_relative_to(B) and '..' not in p.parts,p
 assert p.name not in DENIED and not any(x in str(p).lower() for x in ('password','credential','secret','.cryptalis-test')),p
 assert not any(x.lower() in {'environment','environment.json','.env'} or x.lower().startswith('.env.') for x in p.parts),p
 assert p.is_file(),p
 assert p.resolve(strict=True)==INTERPS.get(p,p),p
 if p not in INTERPS: assert not p.is_symlink(),p
 return p
def rd(p):
 p=safe(p);reads.add(p);return p.read_bytes()
def sha(p):return hashlib.sha256(rd(p)).hexdigest()
def js(p):return json.loads(rd(p))
def w(root,name,data):
 p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
 encoded=data.encode() if isinstance(data,str) else data
 if p.exists():
  assert p.read_bytes()==encoded,p
  return
 with p.open('xb') as f:f.write(encoded)
def j(root,name,data):w(root,name,json.dumps(data,indent=2,sort_keys=True)+'\n')
def cp(root,name,source):w(root,name,rd(source))
def source_manifest(p,root,count):
 d=js(p);h=d['source_sha256'];assert len(h)==count
 for rel,hash_ in h.items():
  q=Path(rel);assert not q.is_absolute() and '..' not in q.parts and re.fullmatch('[0-9a-f]{64}',hash_)
  assert q.parts[0] in {'AGENTS.md','ENGINEERING_PLAYBOOK.md','LICENSE','README.md','docs','examples','experiments','pyproject.toml','scripts','src','tests','uv.lock'},rel
  assert q.suffix in {'.py','.md','.json','.toml','.lock','.hex'} or str(q)=='LICENSE',rel
  if q.parts[0]=='experiments':assert rel=='experiments/manifest_setup_fastapi_models.py'
  safe(root/q)
 for rel,hash_ in h.items():assert sha(root/rel)==hash_,rel
 actual={str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}
 assert all('__pycache__' in Path(q).parts or '.pytest_cache' in Path(q).parts for q in actual-set(h))
 return d
baseline=source_manifest(OLD/'BASELINE_SOURCE_MANIFEST.json',S,216)
green=source_manifest(OLD/'GREEN_SOURCE_MANIFEST.json',C,217)
bh=baseline['source_sha256'];gh=green['source_sha256']
assert set(gh)-set(bh)=={'tests/test_sqlalchemy_async_exit_double_failure.py'} and not set(bh)-set(gh)
assert [q for q in bh if gh[q]!=bh[q]]==['src/cryptalis/sqlalchemy.py']
new=rd(OLD/'NEW_NODE_IDS.txt').decode().splitlines();assert len(new)==len(set(new))==22
assert all(n.startswith('tests/test_sqlalchemy_async_exit_double_failure.py::test_') for n in new)
P.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
for root in (P,O):
 cp(root,'CANDIDATE_SOURCE_MANIFEST.json',OLD/'GREEN_SOURCE_MANIFEST.json')
 w(root,'SOURCE_FILES.txt','\n'.join(sorted(gh))+'\n')
 cp(root,'BASELINE_SOURCE_MANIFEST.json',OLD/'BASELINE_SOURCE_MANIFEST.json')
 cp(root,'NEW_NODE_IDS.txt',OLD/'NEW_NODE_IDS.txt')
 cp(root,'SOURCE_DELTA.patch',OLD/'SOURCE_DELTA.patch')
cp(P,'prepare_source_only.py',Path(__file__)) if False else None
# Current corpus names are validated as a set before reading any payload.
patterns=('compatibility*corpus-v1-sa*.json','master-s4-compatibility*corpus-v1-sa*.json')
corpus=sorted({q for pat in patterns for q in (B/'evidence').glob(pat)})
cre=re.compile(r'(?:master-s4-)?compatibility[^/]*corpus-v1-sa[^/]*\.json')
assert len(corpus)==26
for q in corpus:assert cre.fullmatch(q.name);safe(q)
corpus_map={q.name:sha(q) for q in corpus}
for root in (P,O):j(root,'CORPUS_BASELINE.json',corpus_map)
# Read only explicitly allowlisted current source/control inputs, never expand old manifests.
common={S/q:h for q,h in bh.items()}|{C/q:h for q,h in gh.items()}
fixed=[B/'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py',B/'candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py',B/'repo/scripts/test_postgres.py',B/'toolchain/lab_progress.py',B/'toolchain/run_baseline.py',B/'repo/.venv/bin/python']
for p in fixed:safe(p)
for p in fixed:common[p]=sha(p)
assert sha(C/'scripts/test_postgres.py')==sha(B/'repo/scripts/test_postgres.py')
for p in corpus:common[p]=corpus_map[p.name]
for name in ['BASELINE_SOURCE_MANIFEST.json','GREEN_SOURCE_MANIFEST.json','NEW_NODE_IDS.txt','SOURCE_DELTA.patch','PLAN.md','PREPARATION_CHECKS.json','NATIVE_SOURCE_PINS.sha256']:
 p=OLD/name;common[p]=sha(p)
# Explicit source-only native dependency pin classes. Validate all names before reads.
native=[]
for line in rd(OLD/'NATIVE_SOURCE_PINS.sha256').decode().splitlines():
 m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);assert m
 h,raw=m.groups();p=Path(raw)
 assert any(p.is_relative_to(B/f'release-lab/s25-installed-20261014/{c}/lib/python3.12/site-packages/sqlalchemy') for c in ('sa20','sa21'))
 assert p.suffix=='.py';safe(p);native.append((p,h))
assert len(native)==14
for p,h in native:assert sha(p)==h;common[p]=h
for c in ('sa20','sa21'):
 p=B/f'release-lab/s25-installed-20261014/{c}/bin/python';common[p]=sha(p)
# Preserve installed dependency metadata as data; no import/version command.
metadata=[]
for c in ('sa20','sa21'):
 root=B/f'release-lab/s25-installed-20261014/{c}/lib/python3.12/site-packages'
 for p in sorted(root.glob('*.dist-info/METADATA')):
  assert re.fullmatch(r'[A-Za-z0-9_.+-]+\.dist-info',p.parent.name);safe(p);metadata.append(p)
for p in metadata:common[p]=sha(p)
# Extract exact original outcomes and failure/skip messages from safe source/installed JUnit.
def outcomes(path):
 t=ET.fromstring(rd(path));out={};diagnostics={}
 for e in t.iter('testcase'):
  n=e.get('classname')+'::'+e.get('name');assert n not in out
  kinds=[k for k in ('failure','error','skipped') if e.find(k) is not None];assert len(kinds)<=1
  kind=kinds[0] if kinds else 'passed';out[n]=kind
  if kinds:diagnostics[n]={'outcome':kind,'message':e.find(kind).get('message'),'text':e.find(kind).text}
 assert len(out)==2639;return out,diagnostics
baseline_notes=[]
for c in ('sa21','sa20'):
 source=B/f'evidence/s25-async-sqlmodel-integration-{c}-20261014'
 installed=B/f'evidence/s25-installed-full-{c}-20261014'
 a,ad=outcomes(source/'junit.xml');b,bd=outcomes(installed/'junit.xml');assert a==b
 assert {n:(v['outcome'],v['message']) for n,v in ad.items()}=={n:(v['outcome'],v['message']) for n,v in bd.items()}
 original=B/f'experiments/s25-async-sqlmodel-integration-20261014/BASELINE_{c.upper()}_EXPECTED_OUTCOMES.tsv'
 lines=rd(original).decode().splitlines();expect=dict(line.split('\t') for line in lines[1:]);assert a==expect
 cp(P,f'S25_{c.upper()}_EXPECTED_OUTCOMES.tsv',original)
 expected=dict(a)
 for n in new:
  rel,suffix=n.split('::',1);n=rel.removesuffix('.py').replace('/','.')+'::'+suffix;assert n not in expected;expected[n]='passed'
 assert len(expected)==2661
 w(P,f'EXPECTED_{c.upper()}_OUTCOMES.tsv','exact_junit_id\texpected_outcome\n'+''.join(n+'\t'+v+'\n' for n,v in sorted(expected.items())))
 j(P,f'S25_{c.upper()}_DIAGNOSTICS.json',ad)
 # Each static safe filename is selected directly, not from raw JSON evidence maps.
 for root in (source,installed):
  for n in ('junit.xml','progress.jsonl','runner-receipt.json','readiness.log','package-origin.log','postgres-stop.log','source-stability.json','source-root.json','prior-corpus-manifest.json','candidate-corpus-isolation.json'):
   p=root/n;common[p]=sha(p)
 source_review=B/f'reviewer-notes/s25-integration-independent-20261014/{c.upper()}_TERMINAL_REVIEW.md'
 installed_review=B/(f'reviewer-notes/s25-installed-full-independent-20261014/{c.upper()}_TERMINAL_REVIEW.md' if c=='sa21' else 'reviewer-notes/s25-installed-sa20-terminal-independent-20261014/SA20_TERMINAL_REVIEW.md')
 for p in (source_review,installed_review):common[p]=sha(p)
 baseline_notes.append({'cell':c,'source_review':str(source_review),'installed_review':str(installed_review),'original_outcomes':dict(collections.Counter(a.values())),'planned_outcomes':dict(collections.Counter(expected.values())),'ordinary_ids':2661,'subtests_separate':56,'expected_wrapper_exit':1,'basis':'Exact original JUnit identities, outcome maps and failure/skip messages agree between accepted S25 source and installed controls. New22 pass is a required prediction, not observed integration evidence.'})
j(P,'MATRIX.json',{'status':'PROPOSED_NOT_EXECUTED','source_files':217,'cells':baseline_notes,'main_case_instances':5322,'main_distinct_ids':2661,'optional_case_instances':38,'all_three_case_instances_if_qualified':5360,'all_three_distinct_semantic_ids_if_qualified':2699,'all_three_predicted_outcomes':{'passed':5300,'failure':14,'skipped':46},'subtests_separate_if_main_cells_complete':112})
# External SQLModel oracle: preserve the candidate and all test/fixture bodies.
orig_test=rd(C/'tests/test_async_sqlmodel_public_hook.py').decode()
orig_help=rd(C/'tests/async_sqlmodel_oracle_support.py').decode()
new_test=orig_test.replace('"""Pinned optional SQLModel regression; use the reviewed source-overlay matrix."""','"""Pinned optional SQLModel regression; proposed cleanup-candidate source overlay."""',1).replace('from async_sqlmodel_oracle_support import (','from cleanup_sqlmodel_oracle_support import (',1)
old_header="ROOT = Path(__file__).resolve().parents[1]\nLAB = ROOT.parent\nPACKET = LAB / 'experiments/s25-async-sqlmodel-integration-20261014'\nif ROOT != LAB / 'candidate-s25-async-sqlmodel-integration-20261014' or Path.cwd().resolve() != ROOT:\n    raise RuntimeError('Exact reviewed S25 source root is required')"
new_header="PACKET = Path(__file__).resolve().parents[1]\nLAB = PACKET.parents[1]\nROOT = LAB / 'candidate-next-unblocked-correctness-20261014'\nif PACKET != LAB / 'experiments/async-cleanup-sqlmodel-overlay-plan-20261014':\n    raise RuntimeError('Exact reviewed cleanup overlay packet is required')\nif ROOT != LAB / 'candidate-next-unblocked-correctness-20261014' or Path.cwd().resolve() != ROOT:\n    raise RuntimeError('Exact reviewed cleanup source root is required')\n# Admit only the frozen source test helper directory; product routing stays in the wrapper.\nsys.path.insert(0, str(ROOT / 'tests'))"
assert orig_help.count(old_header)==1
new_help=orig_help.replace(old_header,new_header,1).replace("!= 216:","!= 217:",1).replace("Expected complete 216-file input inventory","Expected complete 217-file input inventory",1).replace("'source_files': 216,","'source_files': 217,",1)
anchor="    dependency_pins = json.loads((PACKET / 'DEPENDENCY_SOURCE_PINS.json').read_text())"
extra="""    overlay = json.loads((PACKET / 'OVERLAY_SOURCE_MANIFEST.json').read_text())
    if set(overlay) != {'oracle/conftest.py', 'oracle/cleanup_sqlmodel_oracle_support.py', 'oracle/test_async_sqlmodel_public_hook.py'}:
        raise RuntimeError('Expected exact three-file evidence-only overlay')
    for relative, digest in overlay.items():
        if hashlib.sha256((PACKET / relative).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Selected overlay differs from frozen manifest: ' + relative)
"""
assert new_help.count(anchor)==1;new_help=new_help.replace(anchor,extra+anchor,1)
assert new_test[new_test.index('def assert_sanitized_provider_failure'):]==orig_test[orig_test.index('def assert_sanitized_provider_failure'):]
assert new_help[new_help.index('def enable('):]==orig_help[orig_help.index('def enable('):]
for name,text in [('oracle/test_async_sqlmodel_public_hook.py',new_test),('oracle/cleanup_sqlmodel_oracle_support.py',new_help)]:
 ast.parse(text,filename=name);w(O,name,text)
cp(O,'oracle/conftest.py',C/'tests/conftest.py')
for n,old,new_ in [('test_async_sqlmodel_public_hook.py',orig_test,new_test),('cleanup_sqlmodel_oracle_support.py',orig_help,new_help)]:
 w(O,n+'.patch',''.join(difflib.unified_diff(old.splitlines(keepends=True),new_.splitlines(keepends=True),fromfile='candidate/tests/'+('async_sqlmodel_oracle_support.py' if n.startswith('cleanup_') else n),tofile='overlay/oracle/'+n)))
ov={str(p.relative_to(O)):sha(p) for p in sorted((O/'oracle').iterdir())}
j(O,'OVERLAY_SOURCE_MANIFEST.json',ov)
cp(O,'DEPENDENCY_SOURCE_PINS.json',B/'experiments/s25-async-sqlmodel-integration-20261014/DEPENDENCY_SOURCE_PINS.json')
nodes=rd(B/'experiments/s25-async-sqlmodel-integration-20261014/SQLMODEL_NODE_IDS.txt').decode().splitlines();assert len(nodes)==len(set(nodes))==38
w(O,'S25_SEMANTIC_NODE_IDS.txt','\n'.join(nodes)+'\n')
w(O,'PLANNED_NODE_SUFFIXES.txt','\n'.join(n.split('::',1)[1] for n in nodes)+'\n')
w(O,'EXACT_SELECTION_PATHS.txt',str(O/'oracle')+'\n')
# Optional interpreter/dependency source pins remain the existing source-qualified cell.
opt_common=dict(common)
optional_prefix=B/'release-lab/cp84-adoption/sqlmodel-wheel-venv'
opt_common[optional_prefix/'bin/python']=sha(optional_prefix/'bin/python')
deps=js(O/'DEPENDENCY_SOURCE_PINS.json');assert len(deps)==16
for rel,h in deps.items():
 assert rel.startswith('lib/python3.14/site-packages/') and '..' not in Path(rel).parts
 assert Path(rel).suffix=='.py' or Path(rel).name=='METADATA';safe(optional_prefix/rel)
for rel,h in deps.items():assert sha(optional_prefix/rel)==h;opt_common[optional_prefix/rel]=h
for n in ('SQLMODEL_TERMINAL_REVIEW.md','SQLMODEL_TERMINAL_AUDIT.json'):
 q=B/'reviewer-notes/s25-integration-independent-20261014'/n;opt_common[q]=sha(q)
for n in ('junit.xml','progress.jsonl','runner-receipt.json','async-sqlmodel-origin.jsonl'):
 q=B/'evidence/s25-async-sqlmodel-integration-sqlmodel-20261014'/n;opt_common[q]=sha(q)
j(O,'SOURCE_COMPARISON.json',{'status':'STATIC_ONLY_NOT_INDEPENDENT_REVIEW','candidate_modified':False,'candidate_files':217,'overlay_files':3,'test_changes':['docstring','unique support import name'],'test_region_from_assert_sanitized_provider_failure_byte_identical':True,'helper_region_from_enable_byte_identical':True,'conftest_byte_identical':True,'helper_binding_changes':['exact external packet/root/cwd binding','frozen candidate/tests fixture import path','216 to 217 source inventory','three-file external overlay hash check at original setup and teardown origin checks'],'dependencies':'Same existing Python3.14.8 SQLModel0.0.47 SQLAlchemy2.0.51 psycopg3.3.6 source-qualified interpreter; unchanged16 dependency pins','static_semantic_nodes':38,'actual_external_node_paths':'NOT_COLLECTED; reconcile returned node suffixes and actual external path with S25 semantic38; no guessed rootdir-based identity'} )
# Record safe names, not environment-bearing phase inventories.
for root,inputs in ((P,common),(O,opt_common)):
 j(root,'SAFE_INPUTS.json',{str(p):h for p,h in sorted(inputs.items())})
 w(root,'INPUTS.sha256',''.join(h+'  '+str(p)+'\n' for p,h in sorted(inputs.items())))
 w(root,'INTERPRETER_TARGETS.json',json.dumps({str(p):str(v) for p,v in INTERPS.items()},indent=2,sort_keys=True)+'\n')
# Text below is supplied separately; final sealing occurs only after all packet files exist.
j(P,'PREPARATION_CHECKS.json',{'status':'SOURCE_DATA_ONLY','baseline_files':216,'candidate_files':217,'changed_existing':['src/cryptalis/sqlalchemy.py'],'added':['tests/test_sqlalchemy_async_exit_double_failure.py'],'main_original_ids_per_cell':2639,'new_planned_nodes':22,'main_planned_ids_per_cell':2661,'corpus_count':26,'safe_main_inputs':len(common),'safe_optional_inputs':len(opt_common),'forbidden_phase_files_opened_or_hashed':False,'runtime_executed':False,'product_imports':False,'candidate_or_checklist_writes':False,'optional_helper_original_still_S25_bound':True,'optional_overlay_is_separate':str(O),'independent_source_and_terminal_reviews':'PENDING'})
print(json.dumps({'main_packet':str(P),'optional_packet':str(O),'main_inputs':len(common),'optional_inputs':len(opt_common),'safe_read_files':len(reads)},indent=2))

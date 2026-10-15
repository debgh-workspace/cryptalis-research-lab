"""Reviewer-owned finite source/evidence auditor. No target imports or execution."""
import ast
import collections
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import xml.etree.ElementTree as ET

W=Path('/workspace/scratch/cb28ee9f5f4a')
B=W/'cryptalis-executable'
D=B/'reviewer-notes/abort-envelope-native-v2-terminal-independent-20261015'
P=B/'experiments/abort-envelope-native-entry-v2-20261015'
N=B/'experiments/abort-envelope-native-probe-v2-20261015'
M=B/'experiments/integrated221-installed-full-controls-v3-20261015'
S=B/'candidate-cluster-retained-integrated-v2-20261015'
A=P/'run/sa21'
E=B/'evidence/abort-envelope-native-probe-v2-sa21-20261015'
C=W/'persistence-recovery-20261013/abort-envelope-native-v2-sa21-root'
NS='f8ebb881794328c9b6054129e5966847cd37264dc80e7a21f4b71c4a10b99ff5'
ES='b872be2e11367c73c55b864fb580a2c3230b457518ba6c9e2342270719cd8bf8'
SS='202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520'
BS='669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54'
SEL='a53e2dbd1e1fba7f919924a4361676fc06a93a694152b358bab295956973821f'
DENIED={'tests.json','readiness.json','package-origin.json','postgres-start.json','postgres-stop.json','.env','environment','environment.json','__pycache__','.pytest_cache','uv_cache.json','home'}
reads={}
metadata={}
checks=[]

def check(ok,name):
 if not ok: raise AssertionError(name)
 checks.append(name)

def admit(p,limit=4*1024*1024):
 p=Path(p)
 assert p.is_absolute() and p.is_relative_to(W) and '..' not in p.parts
 assert not any(s in DENIED for s in p.parts),str(p)
 assert not any(s in str(p).lower() for s in ('credential','password','.cryptalis-test')),str(p)
 for q in reversed(p.parents):assert stat.S_ISDIR(q.lstat().st_mode),str(q)
 st=p.lstat();assert stat.S_ISREG(st.st_mode) and st.st_size<=limit,str(p)
 metadata[str(p)]={'bytes':st.st_size,'mode':stat.S_IMODE(st.st_mode)}
 return p

def raw(p,limit=4*1024*1024):
 p=admit(p,limit)
 with p.open('rb') as f:v=f.read(limit+1)
 assert len(v)<=limit
 reads[str(p)]={'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
 return v

def digest(p):return hashlib.sha256(raw(p)).hexdigest()
def unique(rows):
 d={}
 for k,v in rows:
  assert k not in d,'duplicate JSON key'
  d[k]=v
 return d

def doc(p):return json.loads(raw(p),object_pairs_hook=unique)
def text(p):return raw(p).decode('utf-8')

def tree(p):
 p=Path(p)
 assert stat.S_ISDIR(p.lstat().st_mode)
 files=set();dirs=set()
 for root,ds,fs in os.walk(p,followlinks=False):
  for n in ds:
   q=Path(root)/n;assert stat.S_ISDIR(q.lstat().st_mode)
   assert n not in DENIED,str(q)
   dirs.add(str(q.relative_to(p)))
  for n in fs:
   q=Path(root)/n;admit(q);files.add(str(q.relative_to(p)))
 return files,dirs

def seal(p,expected):
 check(digest(p/'SHA256SUMS.txt')==expected,'seal:'+str(p.relative_to(B)))
 rows={}
 for line in text(p/'SHA256SUMS.txt').splitlines():
  m=re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)',line)
  assert m is not None and m[2] not in rows
  rows[m[2]]=m[1]
 for n,h in rows.items():check(digest(p/n)==h,'sealed_member:'+str((p/n).relative_to(B)))
 return rows

native=seal(N,NS);entry=seal(P,ES)
check(set(native)=={'COMMAND_ARGV.json','EXPECTED_CASES.txt','PREDECESSOR_BINDING.json','PROTOCOL.md','SOURCE_INPUTS.json','conftest.py','test_native_envelope.py'},'native_exact_sealed_members')
check(set(entry)=={'entry.py','run-entry.sh','README.md','COMMAND_ARGV.json','SELECTION-TEMPLATE.json'},'entry_exact_sealed_members')
check({p.name for p in N.iterdir()}==set(native)|{'SHA256SUMS.txt'},'native_exact_current_namespace')
check({p.name for p in P.iterdir()}==set(entry)|{'SHA256SUMS.txt','SELECTION_SA21.json','run'},'entry_exact_current_namespace')
check(digest(P/'SELECTION_SA21.json')==SEL,'selection_external_anchor')
selection=doc(P/'SELECTION_SA21.json')
check(selection['cell']=='sa21' and selection['status']=='SELECTED_BY_ROOT_AFTER_INDEPENDENT_ACCEPTANCE','selection_status_cell')
check(selection['entry_seal_sha256']==ES and selection['native_seal_sha256']==NS and selection['command_sha256']==entry['COMMAND_ARGV.json'],'selection_source_bindings')
check(all(selection[k] is True for k in ('root_current_read_only_authority_confirmed','root_exclusive_selection','no_intervening_lab_stage')),'root_selection_declarations')
reviews={
 'native_source_review':('abort-envelope-native-probe-v2-source-independent-20261015/REVIEW.md','3b048121ed37b172ccaed6538767b9e677c2b88c0db653d443ae7eefb8876018'),
 'entry_source_review':('native-entry-v2-independent-20261015/REVIEW.md','6a370f2f0a24fa65d26ca4c24c37c491bf7fbfa9765b09e54c62506f21fc2d64'),
 'preceding_terminal_review':('abort-envelope-native-terminal-independent-20261015/REVIEW.md','14492777a41a76912c1f5d92ae473d44ac6f9aa6c6d594ed3f9f084d0340ed0e')}
for k,(name,h) in reviews.items():
 p=B/'reviewer-notes'/name;row=selection[k]
 check(row['path']==str(p) and row['sha256']==h and row['root_semantic_verdict_confirmed'] is True and digest(p)==h,'accepted_review:'+k)
check(selection['preceding_terminal_review']['closed_outcome']=='CLOSED_FAILURE' and selection['preceding_terminal_review']['source_packet']=='experiments/abort-envelope-native-probe-v1-20261015' and selection['preceding_terminal_review']['source_packet_seal_sha256']=='0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5','actual_selected_predecessor')
source=doc(M/'CANDIDATE_SOURCE_MANIFEST.json')['source_sha256']
check(len(source)==221 and digest(M/'CANDIDATE_SOURCE_MANIFEST.json')==SS,'source221_anchor')
pin_rows=[
 ('experiments/integrated221-installed-full-controls-v3-20261015/verify_runtime_binding.py','c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861'),
 ('experiments/integrated221-installed-full-controls-v3-20261015/launch_cold_wrapper.py','fe7eb1d38cf826c79ecf201a330522f96501d4edc4d40b2f56f779df24f2acbc'),
 ('experiments/integrated221-installed-full-controls-v3-20261015/BINDING_SA21.json',BS),
 ('experiments/integrated221-installed-full-controls-v3-20261015/CANDIDATE_SOURCE_MANIFEST.json',SS),
 ('candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py','e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453'),
 ('candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py','4c0429a182b5b7a2f7e561892936dba89ed279583bff181b18238f50485de86f'),
 ('toolchain/lab_progress.py','673e3d41398f6be36876008f80110b313ad86553363052c8f14a25e1c47b93c1'),
 ('toolchain/run_baseline.py','a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f'),
 ('repo/scripts/test_postgres.py','118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12'),
 ('experiments/abort-envelope-native-probe-v1-20261015/SHA256SUMS.txt','0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5')]
expected={}
for n,h in source.items():expected['source221/'+n]=(S/n,h)
for prefix,p,m,h in [('entry',P,entry,ES),('native',N,native,NS)]:
 for n,d in m.items():expected[prefix+'/'+n]=(p/n,d)
 expected[prefix+'/SHA256SUMS.txt']=(p/'SHA256SUMS.txt',h)
expected['entry/SELECTION_SA21.json']=(P/'SELECTION_SA21.json',SEL)
for n,h in pin_rows:expected['inputs/'+n]=(B/n,h)
for k,(n,h) in reviews.items():expected['reviews/'+k+'.md']=(B/'reviewer-notes'/n,h)
check(len(expected)==249,'independently_derived_archive249')
archive=A/'frozen-inputs'
files,dirs=tree(archive)
check(files==set(expected),'archive_exact_files')
check(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'archive_exact_directories')
for n,(p,h) in expected.items():admit(p);admit(archive/n)
total=0
for n,(p,h) in expected.items():
 check(digest(p)==h and digest(archive/n)==h,'archive_original_join:'+n)
 total+=metadata[str(p)]['bytes']
archive_receipt=doc(A/'archive-receipt.json')
check(archive_receipt['files_sha256']=={n:h for n,(p,h) in expected.items()},'archive_receipt_exact_map')
check(archive_receipt['files']==249 and archive_receipt['source221']==221 and archive_receipt['bytes']==total,'archive_receipt_counts_bytes')
check(archive_receipt['selection_sha256']==SEL and archive_receipt['entry_seal_sha256']==ES and archive_receipt['native_seal_sha256']==NS,'archive_receipt_anchors')

commands=doc(P/'COMMAND_ARGV.json');invocation=doc(C/'entry-argv.json')
check(invocation['argv']==['/bin/bash',str(P/'run-entry.sh'),SEL,ES] and invocation['shell'] is False and invocation['cwd']==str(B),'exact_root_entry_invocation')
env={'HOME':str(B/'runtime/home'),'LANG':'C.UTF-8','PATH':str(B/'toolchain/pg16/bin')+':/usr/bin:/bin','TZ':'UTC'}
check(invocation['fixed_environment']==env and commands['environment']==env and commands['cwd']==str(B) and commands['shell'] is False,'fixed_nonsecret_environment')
wrapper_expected=[str(B/'repo/.venv/bin/python'),'-B',str(M/'launch_cold_wrapper.py'),'--candidate-root',str(S),'--installed-candidate','--python',str(B/'release-lab/integrated221-installed-20261015/sa21/bin/python'),'--evidence',str(E),'--','-q','-c',str(S/'pyproject.toml'),str(N/'test_native_envelope.py'),'--confcutdir='+str(N),'-p','no:cacheprovider','--tb=short','-x']
check(commands['wrapper_argv']==wrapper_expected,'exact_selected_wrapper_argv')
runner=doc(E/'runner-receipt.json')
check(runner['pytest_args']==wrapper_expected[11:]+['-p','lab_progress','-o','faulthandler_timeout=180','--junitxml='+str(E/'junit.xml')],'actual_runner_pytest_argv')
check(runner['exit_code']==0 and runner['counts']=={'passed':31},'runner_terminal_passed31')
check(runner['preflight']=={'select_1_each':'passed','sha256_prefixes':['76053d5b','a38ab71b']},'fresh_dual_role_preflight_receipt')
check(len(runner['gates'])==7 and set(runner['gates'].values())=={'UNKNOWN'},'seven_product_gates_unknown')

families=['f_uuid_empty','r_uuid_empty','f_uuid_one','r_uuid_one','f_int64_one','r_int64_one','f_two_mixed','r_two_mixed','f_unicode','r_unicode','f_controls','r_controls','f_count9','f_count10','f_count9999','f_count10000','f_count2p53m1','f_count2p53','f_count17digits']
boundaries=['canonical_below','canonical_equal','canonical_above','native_below','native_equal','native_above']
rejections=['nul','high_surrogate','low_surrogate']
ids=['::test_native_cursor_domains['+n+']' for n in ['uuid','int64']]+['::test_jsonb_state_families['+n+']' for n in families]+['::test_jsonb_full_size_edges['+n+']' for n in boundaries]+['::test_jsonb_unrepresentable_unicode['+n+']' for n in rejections]+['::test_native_reservation_omission_controls']
check(text(N/'EXPECTED_CASES.txt').splitlines()==ids and len(ids)==31,'exact_full31_id_order')
state_ids=[]
for case in families:
 labels=['expanded']+([] if case.endswith('_empty') else ['partial'])+['backfilled','verified']
 state_ids.extend((case,label) for label in ['envelope']+labels+['abort_'+label for label in labels])
state_ids.extend((case,label) for case in boundaries for label in ['envelope','aborted'])
state_ids.extend(('omission_controls',label) for label in ['correct_envelope','independent_abort','omit_verification','omit_cursor','omit_counters'])
check(len(state_ids)==len(set(state_ids))==184,'independent_expected184_state_identities')

# Independent specification reconstruction; never load or call target functions.
old_native=B/'experiments/abort-envelope-native-probe-v1-20261015'
check(digest(old_native/'test_native_envelope.py')=='20d2727f58101a6f5378e3b23714d4cf87ff73f98b519386c7e7a5dc11c373b8','failed_v1_body_preserved')
old_body=text(old_native/'test_native_envelope.py')
check(old_body.replace('abort-envelope-native-probe-v1-sa21-20261015','abort-envelope-native-probe-v2-sa21-20261015').replace('q(v) ORDER BY v','q(v) ORDER BY q.v')==text(N/'test_native_envelope.py'),'exact_three_v2_body_substitutions')
check(digest(N/'EXPECTED_CASES.txt')==digest(old_native/'EXPECTED_CASES.txt') and digest(N/'conftest.py')==digest(old_native/'conftest.py'),'selection_conftest_unchanged_from_v1')
events=[json.loads(line,object_pairs_hook=unique) for line in raw(E/'progress.jsonl').splitlines()]
expected_events=[]
for nodeid in ids:
 expected_events.append(('start',nodeid,None,None))
 expected_events.extend(('report',nodeid,phase,'passed') for phase in ['setup','call','teardown'])
observed_events=[(x.get('event'),x.get('nodeid'),x.get('when'),x.get('outcome')) for x in events]
check(observed_events==expected_events and len(events)==124,'exact31_starts93_passed_phases_order')
check(all(type(e['monotonic']) in (int,float) for e in events) and [e['monotonic'] for e in events]==sorted(e['monotonic'] for e in events),'progress_time_order')
lines=raw(E/'envelope-observations.jsonl').splitlines(keepends=True)
check(len(lines)==221 and all(l.endswith(b'\n') and len(l)<=8192 for l in lines),'exact221_bounded_newline_records')
records=[json.loads(l,object_pairs_hook=unique) for l in lines]
check(collections.Counter(r['kind'] for r in records)=={'connection':31,'state':184,'domain':2,'rejection':3,'omission':1},'exact_complete_kind_counts')
junit=ET.fromstring(raw(E/'junit.xml'));suites=list(junit.iter('testsuite'));cases=list(junit.iter('testcase'))
check(len(suites)==1 and suites[0].attrib['tests']=='31' and all(suites[0].attrib[k]=='0' for k in ['failures','errors','skipped']),'junit31_no_fail_error_skip')
check(len(cases)==31 and ['::'+c.attrib['name'] for c in cases]==ids and all(c.attrib['classname']=='' and len(list(c))==0 for c in cases),'junit_exact31_ordered_identities')
accounting=doc(A/'accounting.json')
check(accounting=={'status':'MECHANICAL_ACCOUNTING_COMPLETE_PENDING_INDEPENDENT_AUDIT','cases':31,'passed_phases':93,'observation_records':221,'state_observations':184,'source_derived_explicit_SELECT_count':404,'SELECT_count_is_runtime_trace':False,'native_packet_sha256':NS,'expected_ids':ids},'entry_accounting_exact_independent_join')

LIMIT=16777216
TABLE='00000000-0000-0000-0000-000000000001'
TABLE_TWO='00000000-0000-0000-0000-000000000003'
SOURCE='00000000-0000-0000-0000-000000000002'
MAX_UUID='ffffffff-ffff-ffff-ffff-ffffffffffff'
MIN_INT=-9223372036854775808
family_specs=[
 ('f_uuid_empty',False,'uuid',0,'plain'),('r_uuid_empty',True,'uuid',0,'plain'),
 ('f_uuid_one',False,'uuid',1,'plain'),('r_uuid_one',True,'uuid',1,'plain'),
 ('f_int64_one',False,'int64',1,'plain'),('r_int64_one',True,'int64',1,'plain'),
 ('f_two_mixed',False,'mixed',10,'plain'),('r_two_mixed',True,'mixed',10,'plain'),
 ('f_unicode',False,'uuid',10,'unicode'),('r_unicode',True,'uuid',10,'unicode'),
 ('f_controls',False,'uuid',10,'controls'),('r_controls',True,'uuid',10,'controls'),
 ('f_count9',False,'uuid',9,'plain'),('f_count10',False,'uuid',10,'plain'),
 ('f_count9999',False,'uuid',9999,'plain'),('f_count10000',False,'uuid',10000,'plain'),
 ('f_count2p53m1',False,'uuid',9007199254740991,'plain'),('f_count2p53',False,'uuid',9007199254740992,'plain'),
 ('f_count17digits',False,'uuid',10000000000000000,'plain')]
check([r[0] for r in family_specs]==families,'literal_family_spec_order')

def uuid_text(n):
 h=format(n,'032x')
 return h[:8]+'-'+h[8:12]+'-'+h[12:16]+'-'+h[16:20]+'-'+h[20:]

def specification(reverse,codec,n,profile,form,abort=False):
 # Each state is assembled anew from its phase specification.
 phase={'bound':'BACKFILLED','expanded':'EXPANDED','partial':'EXPANDED','backfilled':'BACKFILLED','verified':'VERIFIED'}[form]
 rows=0 if form=='expanded' else 1 if form=='partial' else n
 models={}
 types=[(TABLE,'uuid' if codec=='mixed' else codec)]+([(TABLE_TWO,'int64')] if codec=='mixed' else [])
 for table,kind in types:
  if rows==0:cursor=None
  elif form=='bound':cursor=MAX_UUID if kind=='uuid' else str(MIN_INT)
  else:cursor=uuid_text(rows-1) if kind=='uuid' else str(MIN_INT+rows-1)
  chunks=rows if form=='bound' else (rows+4999)//5000
  schema={};guard=['A']
  if profile!='plain':
   special='é 雪 😀 e\u0301 \u2028 \u2029 " \\ / , : [] {}' if profile=='unicode' else ''.join(map(chr,range(1,32)))+'\\"/:,'
   schema={'columns':[{'name':special,'nullable':True}],'text':special}
   guard=['A',30,True,0,'public','guard_fn',False,['search_path=pg_catalog',special],special,'owner',[['pause','A',special,special,False,['search_path=pg_catalog'],'owner']]]
  models[table]={'scope':{'count':n,'membership':'0'*64},'cursor':cursor,'rows':rows,'chunks':chunks,'schema':schema,'guard':guard}
 state={'phase':'ABORTED' if abort else phase,'models':models}
 if reverse:state.update(layout_version=101,source_operation_id=SOURCE,source_plan_digest='1'*64)
 if not reverse and form in ['bound','verified']:state['verification']={table:'f'*64 for table,_ in types}
 return state

def canonical_json(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def native_hypothesis(v):
 # A separately implemented finite rendering hypothesis, compared against actual
 # server output hashes. It is not imported from the native test/reference.
 if type(v) is dict:
  names=sorted(v,key=lambda k:(len(k.encode('utf-8')),k.encode('utf-8')))
  return '{'+', '.join(json.dumps(k,ensure_ascii=False)+': '+native_hypothesis(v[k]) for k in names)+'}'
 if type(v) is list:return '['+', '.join(map(native_hypothesis,v))+']'
 return json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False)

def punctuation_spaces(v):
 if type(v) is dict:return len(v)+max(0,len(v)-1)+sum(map(punctuation_spaces,v.values()))
 if type(v) is list:return max(0,len(v)-1)+sum(map(punctuation_spaces,v))
 return 0

def strict_equal(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(strict_equal(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
 return a==b

position=0
state_join=[]
connections=[]
roundtrip_calls={nodeid for event,nodeid,when,outcome in observed_events if event=='report' and when=='call' and outcome=='passed'}

def take(kind,case,label=None):
 global position
 check(position<len(records),'ledger_position_present:'+str(position))
 row=records[position];position+=1
 check(row.get('kind')==kind and row.get('case')==case and (label is None or row.get('label')==label),'ordered_ledger_identity:'+str(position))
 return row

def connected(case):
 row=take('connection',case)
 check(set(row)=={'kind','case','version','client_encoding','server_encoding','backend_pid','target_digest'},'connection_schema:'+case)
 check(type(row['version']) is int and row['version']==160015 and row['server_encoding']==row['client_encoding']=='UTF8','connection_pg16_utf8:'+case)
 check(type(row['backend_pid']) is int and row['backend_pid']>0 and type(row['target_digest']) is str and re.fullmatch('[0-9a-f]{64}',row['target_digest']) is not None,'connection_type_fields:'+case)
 connections.append(row)

def verify_state(case,label,value,nodeid):
 row=take('state',case,label)
 compact=canonical_json(value);native_bytes=native_hypothesis(value).encode('utf-8')
 compact_size=len(compact);native_size=len(native_bytes);spaces=punctuation_spaces(value)
 expected={'kind':'state','case':case,'label':label,'status':'OBSERVED_BEFORE_ASSERTIONS','canonical_bytes':compact_size,'supplied_bytes':compact_size,'native_bytes':native_size,'received_native_bytes':native_size,'candidate_native_bytes':compact_size+spaces,'canonical_sha256':hashlib.sha256(compact).hexdigest(),'native_sha256':hashlib.sha256(native_bytes).hexdigest(),'root_type':'object','length_oids':[23,23,25],'length_formats':[0,0,0],'text_oid':25,'text_format':0,'canonical_within_limit':compact_size<=LIMIT,'native_within_limit':native_size<=LIMIT}
 check(strict_equal(row,expected),'state_full_schema_lengths_formats_hashes:'+case+':'+label)
 check(native_size==compact_size+spaces and compact_size<=LIMIT+1 and native_size<=LIMIT+32,'state_independent_spacing_and_diagnostic_bounds:'+case+':'+label)
 check(nodeid in roundtrip_calls,'state_passed_call_roundtrip_join:'+case+':'+label)
 check(strict_equal(json.loads(native_bytes),value) and canonical_json(json.loads(native_bytes))==compact,'reviewer_native_reconstruction_roundtrip:'+case+':'+label)
 state_join.append(row)
 return row

for codec,values,oid,width in [
 ('uuid',[uuid_text(0),uuid_text(1),MAX_UUID],2950,36),
 ('int64',['-9223372036854775808','-9007199254740993','-1','0','9007199254740993','9223372036854775807'],20,20)]:
 case='domain_'+codec;connected(case);row=take('domain',case)
 check(strict_equal(row,{'kind':'domain','case':case,'formats':[0,0],'oids':[oid,25],'texts':values,'maximum_ascii_characters':width}),'domain_exact_values_order_width_types:'+codec)
 check('::test_native_cursor_domains['+codec+']' in roundtrip_calls,'domain_passed_call_join:'+codec)

for case,reverse,codec,n,profile in family_specs:
 connected(case);nodeid='::test_jsonb_state_families['+case+']'
 bound=verify_state(case,'envelope',specification(reverse,codec,n,profile,'bound'),nodeid)
 forms=['expanded']+([] if n==0 else ['partial'])+['backfilled','verified']
 for abort in [False,True]:
  for form in forms:
   row=verify_state(case,('abort_' if abort else '')+form,specification(reverse,codec,n,profile,form,abort),nodeid)
   check(row['canonical_bytes']<=bound['canonical_bytes'] and row['native_bytes']<=bound['native_bytes'],'actual_family_bound_both_representations:'+case+':'+str(abort)+form)

boundary_results=[]
for case,basis,margin in [('canonical_below','canonical',-1),('canonical_equal','canonical',0),('canonical_above','canonical',1),('native_below','native',-1),('native_equal','native',0),('native_above','native',1)]:
 connected(case);nodeid='::test_jsonb_full_size_edges['+case+']'
 value=specification(False,'uuid',1,'plain','bound')
 check(len(canonical_json(value))==391,'independent_boundary_literal391:'+case)
 value['models'][TABLE]['schema']={'fill':'x'*(LIMIT+margin-(400 if basis=='canonical' else 422))}
 bound=verify_state(case,'envelope',value,nodeid)
 value['phase']='ABORTED'
 aborted=verify_state(case,'aborted',value,nodeid)
 compact_expected=LIMIT+margin-(0 if basis=='canonical' else 22);native_expected=compact_expected+22
 check(bound['canonical_bytes']==compact_expected and bound['native_bytes']==native_expected and aborted['canonical_bytes']==compact_expected-3 and aborted['native_bytes']==native_expected-3,'all_actual_full_size_edge_values:'+case)
 boundary_results.append({'case':case,'envelope_compact':compact_expected,'envelope_native':native_expected,'aborted_compact':aborted['canonical_bytes'],'aborted_native':aborted['native_bytes'],'envelope_compact_gate':bound['canonical_within_limit'],'envelope_native_gate':bound['native_within_limit'],'aborted_compact_gate':aborted['canonical_within_limit'],'aborted_native_gate':aborted['native_within_limit']})
 del value

rejection_results=[]
for case,wire,observed_sqlstate in [('nul','{"x":"\\u0000"}','22P05'),('high_surrogate','{"x":"\\ud800"}','22P02'),('low_surrogate','{"x":"\\udfff"}','22P02')]:
 connected('reject_'+case);row=take('rejection',case)
 check(strict_equal(row,{'kind':'rejection','case':case,'raw_ascii_sha256':hashlib.sha256(wire.encode('ascii')).hexdigest(),'sqlstate':observed_sqlstate}),'rejection_payload_hash_observed_sqlstate:'+case)
 check(len(row['sqlstate'])==5 and row['sqlstate'].startswith('22') and '::test_jsonb_unrepresentable_unicode['+case+']' in roundtrip_calls,'rejection_class22_passed_call_join:'+case)
 rejection_results.append(row)

case='omission_controls';nodeid='::test_native_reservation_omission_controls';connected(case)
correct=specification(False,'uuid',10000000000000000,'plain','bound')
good=verify_state(case,'correct_envelope',correct,nodeid)
actual={'phase':'ABORTED','models':{TABLE:{'scope':{'count':10000000000000000,'membership':'0'*64},'cursor':MAX_UUID,'rows':10000000000000000,'chunks':10000000000000000,'schema':{},'guard':['A']}},'verification':{TABLE:'f'*64}}
terminal=verify_state(case,'independent_abort',actual,nodeid)
check(terminal['canonical_bytes']<=good['canonical_bytes'] and terminal['native_bytes']<=good['native_bytes'],'omission_control_positive_bound_both')
omission_results=[]
for omitted in ['verification','cursor','counters']:
 faulty=specification(False,'uuid',10000000000000000,'plain','bound')
 if omitted=='verification':del faulty['verification']
 elif omitted=='cursor':faulty['models'][TABLE]['cursor']=None
 else:faulty['models'][TABLE].update(rows=0,chunks=0)
 row=verify_state(case,'omit_'+omitted,faulty,nodeid)
 check(terminal['canonical_bytes']>row['canonical_bytes'] and terminal['native_bytes']>row['native_bytes'],'actual_omission_underestimate_both:'+omitted)
 omission_results.append({'omitted':omitted,'faulty_compact':row['canonical_bytes'],'faulty_native':row['native_bytes'],'actual_abort_compact':terminal['canonical_bytes'],'actual_abort_native':terminal['native_bytes'],'underestimate_compact':terminal['canonical_bytes']-row['canonical_bytes'],'underestimate_native':terminal['native_bytes']-row['native_bytes']})
row=take('omission',case)
check(strict_equal(row,{'kind':'omission','case':case,'killed':['verification','cursor','counters'],'status':'THREE_INDEPENDENT_SIZE_UNDERESTIMATES_DETECTED'}),'exact_three_omission_detection_receipt')
check(position==len(records)==221,'exact_complete_ordered_ledger_consumed')
check([(r['case'],r['label']) for r in state_join]==state_ids and len(state_join)==184,'all184_state_identity_join')
check(len(connections)==31 and len({r['target_digest'] for r in connections})==1,'all31_connections_same_target_digest')
check(len({r['backend_pid'] for r in connections})==31,'all31_observed_connection_pids_distinct')


snapshot=doc(E/'source-before.json');stability=doc(E/'source-stability.json')
check(len(snapshot)==160 and stability=={'before':snapshot,'after':snapshot,'unchanged':True},'runner_source160_stability')
check(all(source[n]==h for n,h in snapshot.items()),'runner_source160_source221_join')
check(runner['source_test_sha256']==({n:h for n,h in snapshot.items() if n not in {'uv.lock','pyproject.toml'}} | {'scripts/test_postgres.py':source['scripts/test_postgres.py']}),'runner_source159_receipt_join')
snapfiles,_=tree(E/'source-repository')
check(snapfiles==set(snapshot),'runner_source_archive_exact160')
for n,h in snapshot.items():check(digest(E/'source-repository'/n)==h,'runner_source_archive:'+n)
extkey=str((N/'test_native_envelope.py').relative_to(B));ext={extkey:native['test_native_envelope.py']}
check(doc(E/'external-source-before.json')==ext and doc(E/'external-source-stability.json')=={'before':ext,'after':ext,'unchanged':True},'selected_native_external_source_stability')
extfiles,_=tree(E/'source-external')
check(extfiles==set(ext),'runner_external_source_exact1')
check(digest(E/'source-external'/extkey)==ext[extkey],'runner_external_native_hash')

binding=doc(M/'BINDING_SA21.json');check(digest(M/'BINDING_SA21.json')==BS,'runtime_binding_anchor')
joined={}
for manifest in binding['manifests'].values():
 for p,h in manifest['targets'].items():
  check(p not in joined or joined[p]==h,'runtime_manifest_overlap:'+p)
  joined[p]=h
check(len(joined)==3025,'runtime_independent_union3025')
before=doc(A/'runtime-before.log');after=doc(A/'runtime-after.log')
for label,report in [('before',before),('after',after)]:
 check(report['status']=='VERIFIED' and report['stage']=='sa21' and report['mode']==label and report['binding_sha256']==BS,'runtime_mode_status_binding:'+label)
 check(report['verified_target_sha256']==joined and report['exact_input_count']==3025,'runtime_full_target_join:'+label)
 check(report['verified_packet_sha256']==binding['packet_members'] and len(report['verified_packet_sha256'])==27,'runtime_packet27_join:'+label)
 check(report['source_files']==221 and report['corpus_files']==26 and report['installed_modules']==86 and report['complete_nonproduct_files']==2402 and report['opaque_installer_metadata_paths']==2,'runtime_expected_counts:'+label)
check({k:v for k,v in before.items() if k!='mode'}=={k:v for k,v in after.items() if k!='mode'},'runtime_before_after_identical_except_mode')
modules={n.removeprefix('src/'):h for n,h in source.items() if n.startswith('src/cryptalis/') and n.endswith('.py')}
check(len(modules)==43,'main43_source_modules')
for cell in ['sa21','sa20']:
 root=Path(binding['installed_roots'][cell])/'lib/python3.12/site-packages'
 check(all(joined[str(root/n)]==h for n,h in modules.items()),'installed_main43_source_join:'+cell)
origin=doc(E/'package-origin.log')
check(origin=={'package_origin':str(B/'release-lab/integrated221-installed-20261015/sa21/lib/python3.12/site-packages/cryptalis/__init__.py'),'expected_source':str(S/'src'),'installed':True,'byte_matched_modules':43,'verified':True},'actual_selected_origin43')
corpus_before=doc(C/'corpus-before.json');corpus_after=doc(C/'corpus-after.json');prior=doc(E/'prior-corpus-manifest.json')
check(len(corpus_before)==26 and corpus_before==corpus_after==prior==before['verified_corpus_sha256']==after['verified_corpus_sha256'],'five_way_corpus26_join')
check(all(joined[str(B/'evidence'/n)]==h for n,h in corpus_before.items()),'corpus26_binding_join')
isolation=doc(E/'candidate-corpus-isolation.json')
check(isolation=={'patterns':['compatibility*corpus-v1-sa*.json','master-s4-compatibility*corpus-v1-sa*.json'],'archived':[],'deleted_during_run':[],'primary_receipts_restored':True,'errors':[]},'corpus_restoration_receipt')
check(not any((E/'candidate-corpus').iterdir()),'candidate_corpus_empty')

log=text(A/'wrapper.log');stop=text(E/'postgres-stop.log')
check(log.count('postgres-start exit 0\n')==1 and log.count('postgres-stop exit 0\n')==1 and log.count('tests exit 0\n')==1,'single_wrapper_start_tests_stop_receipts')
check('waiting for server to shut down.... done\nserver stopped\n' in stop and stop in log,'successful_stop0_log_join')
check(text(C/'entry-exit.txt')=='0\n' and text(A/'wrapper-exit.txt')=='0\n','entry_wrapper_terminal0')
for d,n in [(C,'pre-status'),(C,'post-status'),(A,'pre-status'),(A,'post-status')]:
 check(text(d/(n+'-exit.txt'))=='3\n','status3:'+str(d.relative_to(W))+':'+n)
 logname=n+('.stdout' if d==C else '.log')
 check(text(d/logname)=='pg_ctl: no server running\n','stopped_status_output:'+str(d.relative_to(W))+':'+n)
for mode in ['before','after']:check(text(A/('runtime-'+mode+'-exit.txt'))=='0\n','runtime_exit0:'+mode)
closure=doc(A/'closure.json')
check(closure=={'post_status':3,'runtime_after':0,'source_after':0,'terminal_acceptance':'PENDING_INDEPENDENT_REVIEW','wrapper_exit':0},'honest_closed_pass_receipt')
check(text(C/'entry.stderr')=='' and 'Mechanical accounting complete' in text(C/'entry.stdout'),'entry_success_message')
resources=doc(A/'wrapper-resources.json')
check(resources['child_exit']==resources['entry_wrapper_exit']==0,'resource_success_exit_join')
check(resources['inherited_tests_timeout_seconds']==600 and resources['inherited_control_phase_timeout_seconds']==90 and resources['new_parent_deadline'] is None,'resource_inherited_deadlines')
check(resources['linux_wait4_peak_rss_kib']==258784 and resources['wall_seconds']==7.536790651007323 and resources['user_cpu_seconds']==2.937396 and resources['system_cpu_seconds']==1.02865,'measured_resource_values')

result={'verdict':'CLOSED_PASS_SCOPED_NATIVE_REPRESENTATION_OBSERVATIONS','checks_passed':len(checks),'archive_files':249,'archive_bytes':total,'source221':221,'runtime_exact_targets':3025,'selected_main_modules':43,'guard_modules_across_sa21_sa20':86,'corpus_files':26,'root_entry_exit':0,'wrapper_exit':0,'stop_exit':0,'post_status':3,'expected_cases':31,'started_cases':31,'passed_calls':31,'failed_calls':0,'reported_phases':93,'passed_phases':93,'failed_phases':0,'expected_observations':221,'actual_observations':221,'actual_observation_kinds':dict(collections.Counter(x['kind'] for x in records)),'expected_state_identities':state_ids,'actual_state_identities':[(r['case'],r['label']) for r in state_join],'independently_reconstructed_state_hash_pairs':184,'full_size_cases_executed':6,'full_size_observations':12,'boundary_results':boundary_results,'domain_records':2,'class22_rejection_records':3,'rejection_results':rejection_results,'omission_records':1,'omission_results':omission_results,'native_test_sha256':native['test_native_envelope.py'],'entry_seal_sha256':ES,'native_seal_sha256':NS,'selection_sha256':SEL,'runtime_binding_sha256':BS,'resources':resources,'resource_peak_mib':resources['linux_wait4_peak_rss_kib']/1024,'cpu_seconds':resources['user_cpu_seconds']+resources['system_cpu_seconds'],'product_gates':runner['gates'],'raw_phase_json_bodies_read':False,'database_status_target_tests_target_imports_lab_reruns_git_executed':False}
for name,value in [('AUDIT_RESULT.json',result),('READ_MANIFEST.json',reads),('METADATA_MANIFEST.json',metadata),('CHECKS.json',checks),('STATE_JOINS.json',state_join)]:
 with (D/name).open('x') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'expected_state_identities','actual_state_identities','product_gates'}},indent=2,sort_keys=True))


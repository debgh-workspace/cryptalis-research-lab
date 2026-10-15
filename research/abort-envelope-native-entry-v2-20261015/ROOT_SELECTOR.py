import json,hashlib,stat,subprocess
from pathlib import Path
W=Path('/workspace/scratch/cb28ee9f5f4a');B=W/'cryptalis-executable';P=W/'persistence-recovery-20261013';D=B/'experiments/abort-envelope-native-entry-v2-20261015';O=P/'abort-envelope-native-v2-sa21-root';O.mkdir(mode=0o700)
def h(p):
 p=Path(p)
 for q in reversed(p.parents): assert stat.S_ISDIR(q.lstat().st_mode)
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,v):(O/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
reviews={
'native_source_review':('abort-envelope-native-probe-v2-source-independent-20261015/REVIEW.md','3b048121ed37b172ccaed6538767b9e677c2b88c0db653d443ae7eefb8876018'),
'entry_source_review':('native-entry-v2-independent-20261015/REVIEW.md','6a370f2f0a24fa65d26ca4c24c37c491bf7fbfa9765b09e54c62506f21fc2d64'),
'preceding_terminal_review':('abort-envelope-native-terminal-independent-20261015/REVIEW.md','14492777a41a76912c1f5d92ae473d44ac6f9aa6c6d594ed3f9f084d0340ed0e')}
seal='b872be2e11367c73c55b864fb580a2c3230b457518ba6c9e2342270719cd8bf8';command='63ada3b8d11711a8ed5627a9ebc882cd6f36c635ee371c91271c53e4e484d807'
assert h(D/'SHA256SUMS.txt')==seal and h(D/'COMMAND_ARGV.json')==command
assert h(D/'run-entry.sh')=='732df7d2e7a2ee3be43764214eef3707b431227fddfefbf55e422ef0a1eaa9d3'
for _,(p,d) in reviews.items():assert h(B/'reviewer-notes'/p)==d
env={'HOME':str(B/'runtime/home'),'PATH':str(B/'toolchain/pg16/bin')+':/usr/bin:/bin','LANG':'C.UTF-8','TZ':'UTC'}
def run(argv,label):
 dump(label+'-argv.json',{'argv':argv,'cwd':str(B),'fixed_environment':env,'shell':False})
 with (O/(label+'.stdout')).open('xb') as out,(O/(label+'.stderr')).open('xb') as err:r=subprocess.run(argv,cwd=B,env=env,stdout=out,stderr=err)
 (O/(label+'-exit.txt')).write_text(str(r.returncode)+'\n');return r.returncode
status=[str(B/'toolchain/pg16/bin/pg_ctl'),'-D',str(B/'runtime/data'),'status'];assert run(status,'pre-status')==3
expected=json.loads((P/'abort-envelope-native-v1-sa21-root/corpus-after.json').read_text())
def corpus():return {n:h(B/'evidence'/n) for n in expected}
assert len(expected)==26 and corpus()==expected;dump('corpus-before.json',expected)
s=json.loads((D/'SELECTION-TEMPLATE.json').read_text());s.update(status='SELECTED_BY_ROOT_AFTER_INDEPENDENT_ACCEPTANCE',entry_seal_sha256=seal,command_sha256=command,root_current_read_only_authority_confirmed=True,root_exclusive_selection=True,no_intervening_lab_stage=True)
for k,(p,d) in reviews.items():s[k].update(path=str(B/'reviewer-notes'/p),sha256=d,root_semantic_verdict_confirmed=True)
s['preceding_terminal_review']['closed_outcome']='CLOSED_FAILURE'
with (D/'SELECTION_SA21.json').open('x') as f:json.dump(s,f,indent=2);f.write('\n')
try:
 code=run(['/bin/bash',str(D/'run-entry.sh'),h(D/'SELECTION_SA21.json'),seal],'entry');print('native_entry_exit',code,flush=True)
finally:
 post=run(status,'post-status');actual=corpus();dump('corpus-after.json',actual);print('post_status',post,'corpus_equal',actual==expected,flush=True)

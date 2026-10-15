from pathlib import Path
import hashlib,json,shutil,subprocess,sys
w=Path('/workspace/scratch/cb28ee9f5f4a');b=w/'cryptalis-executable';p=b/'experiments/cleanup-transport-metadata-20261014'
phase,cell=sys.argv[1:];assert phase in ('red','green') and cell in ('sa21','sa20')
anchor='6a7257031d8e38e7712aa037c14fa704579d6cb994c9be205ba6e8f39c8247d3'
assert hashlib.sha256((p/'PACKET.sha256').read_bytes()).hexdigest()==anchor
s=(p/'PROPOSED_COMMANDS.txt').read_text();start=s.index('# BEGIN '+phase+' '+cell+':');end=s.index('# END '+phase+' '+cell,start)+len('# END '+phase+' '+cell);block=s[start:end]+'\n'
e=b/('evidence/cleanup-transport-metadata-'+phase.lower()+'-'+cell.lower()+'-20261014');c=e.with_name(e.name+'-packet')
assert not e.exists() and not c.exists();c.mkdir();shutil.copytree(p,c/'packet');(c/'exact-command.sh').write_text(block);shutil.copy2(__file__,c/'coordinator-driver.py')
checks={'selected_phase':phase,'dependency_cell':cell,'outer_argv':['bash',str(c/'exact-command.sh')],'exact_command_sha256':hashlib.sha256(block.encode()).hexdigest(),'packet_anchor':anchor}
for when in ('before','after'):
 if when=='after':
  with (c/'outer.log').open('wb') as f:r=subprocess.run(checks['outer_argv'],cwd=w,stdout=f,stderr=subprocess.STDOUT)
  checks['outer_exit']=r.returncode
 assert hashlib.sha256((p/'PACKET.sha256').read_bytes()).hexdigest()==anchor
 with (c/(when+'-packet-copy.log')).open('wb') as f:r=subprocess.run(['diff','-qr',str(p),str(c/'packet')],stdout=f,stderr=subprocess.STDOUT)
 checks[when+'_packet_copy_exit']=r.returncode
 assert r.returncode==0
 for name in ('PACKET.sha256','INPUTS.sha256'):
  with (c/(when+'-'+name+'.log')).open('wb') as f:r=subprocess.run(['sha256sum','-c',str(p/name)],cwd=w,stdout=f,stderr=subprocess.STDOUT)
  checks[when+'_'+name]=r.returncode
  assert r.returncode==0
q=e/'coordinator-wrapper-exit.txt';checks['wrapper_exit']=int(q.read_text()) if q.exists() else None
(c/'coordinator-status.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))

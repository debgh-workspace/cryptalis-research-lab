"""Parse and hash validation sources/receipts only; do not execute them."""
import ast, hashlib,json
from pathlib import Path
R=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-native-direction-probe-20261014'); O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((O/'recomputed-evidence.json').read_text())
checks={'original_audited_bytes_unchanged':all(sha(R/k)==v for k,v in old['observed_sha256'].items())}
original=(R/'test_direction.py').read_text(); orig_ast=ast.parse(original)
wrapper=(R/'validate_direction_explicit.py').read_text(); wa=ast.parse(wrapper)
checks['wrapper_has_no_assert']=not any(isinstance(n,ast.Assert) for n in ast.walk(wa))
origmain=next(n for n in orig_ast.body if isinstance(n,ast.FunctionDef) and n.name=='main')
receipts={}; hashes={'validate_direction_explicit.py':sha(R/'validate_direction_explicit.py')}
labels=json.loads((R/'evidence/public-vector-checks-01.json').read_text())['passed_checks']
for opt in (0,1):
 for mode in ('positive','negative'):
  suffix=f'explicit-o{opt}-{mode}';path=R/f'generated_{suffix}.py';src=path.read_text(); tree=ast.parse(src)
  checks[suffix+'_no_assert']=not any(isinstance(n,ast.Assert) for n in ast.walk(tree))
  main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
  checks[suffix+'_main_cases_identical']=ast.dump(main)==ast.dump(origmain)
  expected=original.replace('    assert actual == expected', "    if actual != expected:\n        raise AssertionError('Output mismatch')").replace("        assert str(exc) in ('Native operation failed', 'Exact bytes required', 'Invalid bounded input')", "        if str(exc) not in ('Native operation failed', 'Exact bytes required', 'Invalid bounded input'):\n            raise AssertionError('Unexpected refusal text')").replace("    main();receipt['status']='PASS'", "    if '--negative-control' in sys.argv:\n        equal(b'wrong', b'expected')\n    main();receipt['status']='PASS'").replace("'python':sys.version.split()[0]", "'python':sys.version.split()[0], 'optimize':sys.flags.optimize, 'validation_style':'explicit exceptions'").replace('evidence/public-vector-checks-01.json',f'evidence/{suffix}.json')
  checks[suffix+'_only_expected_edits']=src==expected
  rpath=R/f'evidence/{suffix}.json';r=json.loads(rpath.read_text());receipts[suffix]={k:r[k] for k in ('status','count','optimize','cryptography','pyca_backend','native_backend')}
  checks[suffix+'_flags']=r['optimize']==opt and r['validation_style']=='explicit exceptions'
  checks[suffix+'_pins']=r['source_sha256']==sha(R/'native_direction.c') and r['binary_sha256']==sha(R/'native_direction.cpython-312-x86_64-linux-gnu.so')
  checks[suffix+'_fixture']=r['fixture_sha256']==sha(R.parent/'candidate-accel-payload-integrated-20261014/tests/fixtures/cf1_vectors.json')
  checks[suffix+'_expected_result']=(r['status']=='PASS' and r['count']==76 and r['passed_checks']==labels) if mode=='positive' else (r['status']=='FAIL' and r['count']==0 and r['passed_checks']==[] and r['failure']=={'type':'AssertionError','message':'Output mismatch'})
  hashes[str(path.relative_to(R))]=sha(path);hashes[str(rpath.relative_to(R))]=sha(rpath)
launch=json.loads((R/'evidence/explicit-validation-launches.json').read_text())
checks['four_launches']=len(launch)==4
checks['launch_exits']=all(x['exit_code']==x['expected_exit']==(1 if '--negative-control' in x['command'] else 0) for x in launch)
checks['launch_modes']=sorted(('-O' in x['command'],'--negative-control' in x['command']) for x in launch)==[(False,False),(False,True),(True,False),(True,True)]
hashes['evidence/explicit-validation-launches.json']=sha(R/'evidence/explicit-validation-launches.json')
result={'method':'Read-only AST/source/hash/JSON inspection; no candidate imports or runs','checks':checks,'all_checks_pass':all(checks.values()),'receipts':receipts,'sha256':hashes}
(O/'explicit-addendum-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_checks_pass':result['all_checks_pass'],'checks':len(checks),'receipts':receipts},indent=2))

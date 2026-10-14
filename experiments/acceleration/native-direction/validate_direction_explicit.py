"""Non-optimizable validation harness; preserves the original frozen experiment."""
from pathlib import Path
import ast
import hashlib
import json
import runpy
import sys
import sysconfig

ROOT = Path(__file__).resolve().parent
original = ROOT / 'test_direction.py'
for name, expected in {
    'native_direction.c': '5933299b46e349cd0e80032fd89beffd797e5ad04230cbfda1d985ef1eca0239',
    'native_direction' + sysconfig.get_config_var('EXT_SUFFIX'): '393cf26a573870a9e7e1d3b12a3196528f9301f840214dbc05d84e1cb37575ed',
}.items():
    if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
        raise RuntimeError('Frozen component mismatch')
if hashlib.sha256(original.read_bytes()).hexdigest() != '7ce19da934fc54bccdb53fc73265d81693cb51a9f90065385380aa1c4bb19924':
    raise RuntimeError('Original validation source mismatch')

# Retain the exact original cases while replacing the two optimization-sensitive
# checks. The generated file is independently inspectable, never imported by product.
source = original.read_text()
source = source.replace('    assert actual == expected',
    "    if actual != expected:\n        raise AssertionError('Output mismatch')")
source = source.replace("        assert str(exc) in ('Native operation failed', 'Exact bytes required', 'Invalid bounded input')",
    "        if str(exc) not in ('Native operation failed', 'Exact bytes required', 'Invalid bounded input'):\n            raise AssertionError('Unexpected refusal text')")
source = source.replace("    main();receipt['status']='PASS'",
    "    if '--negative-control' in sys.argv:\n        equal(b'wrong', b'expected')\n    main();receipt['status']='PASS'")
source = source.replace("'python':sys.version.split()[0]", "'python':sys.version.split()[0], 'optimize':sys.flags.optimize, 'validation_style':'explicit exceptions'")
suffix = f"explicit-o{sys.flags.optimize}-{'negative' if '--negative-control' in sys.argv else 'positive'}"
receipt = ROOT / f'evidence/{suffix}.json'
if receipt.exists():
    raise RuntimeError('Refusing to overwrite previous evidence')
source = source.replace('evidence/public-vector-checks-01.json', f'evidence/{suffix}.json')
if any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))):
    raise RuntimeError('Optimization-sensitive validation remains')
generated = ROOT / f'generated_{suffix}.py'
if generated.exists():
    raise RuntimeError('Refusing to overwrite previous harness')
generated.write_text(source)
runpy.run_path(str(generated), run_name='__main__')

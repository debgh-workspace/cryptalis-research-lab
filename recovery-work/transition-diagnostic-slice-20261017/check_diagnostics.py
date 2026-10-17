"""UNEXECUTED source packet: isolated class compatibility, never product import.

Root must select any future run. No DB, provider, fixture or product module runs.
The selected AST is exactly a pinned inert class contract, executed alone.
"""
import ast
import builtins
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PINS = {
    'migration.baseline.py': '94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014',
    'migration.derivative.py': '1d806f3f70ce9ae191871a75d372f7acdef4e35aaf7d63b0a8cbdadd03ade01b',
    'TransitionFailure.contract.py': '26b57fdd6f64182dd76630dbb0c0eb6efa248c0b976b01a167164571b84c5b89',
}
# Independent literal message oracles; do not read expected values from the patch
# or the observed class's dictionary.
NEW = {
    'operation_aborted': ' This forward identity cannot be resumed. Preserve the retained journal and original artifact. A different operation identity does not authorize reuse or replacement of that journal; forward-successor integration is not implemented.',
    'journal_identity_mismatch': ' Preserve the journal and authenticated current artifact. Do not delete, relabel or replace a journal row to make this plan fit; the mismatch does not authorize another operation or a successor.',
    'database_effect_requires_inspection': ' A connection or COMMIT acknowledgement failure does not establish rollback or completion. Preserve the original attempt evidence and current external policy. Do not blindly repeat the operation or infer completion from an empty queue; no native ambiguous-COMMIT reconciler is implemented.',
}
OLD = (
    'legacy_profile_creation_disabled',
    'legacy_designation_evidence_required',
    'legacy_transient_designation_requires_review',
    'other_database_snapshots_active',
    'unsupported_reverse_suffix_metadata',
    'reverse_staging_layout_requires_inspection',
)
ALLOWED_NODES = {
    ast.ClassDef, ast.Name, ast.Load, ast.Store, ast.Assign, ast.Constant,
    ast.FunctionDef, ast.arguments, ast.arg, ast.Tuple, ast.Call, ast.Attribute,
    ast.JoinedStr, ast.FormattedValue, ast.GeneratorExp, ast.comprehension,
    ast.BoolOp, ast.Or, ast.Dict, ast.BinOp, ast.Add, ast.Expr,
}


def require(value, label):
    if not value:
        raise AssertionError(label)


def read_pinned(name):
    path = ROOT / name
    require(not path.is_symlink() and path.is_file(), 'ordinary_input:' + name)
    require(path.stat().st_size <= 128 * 1024, 'input_bound:' + name)
    body = path.read_bytes()
    require(hashlib.sha256(body).hexdigest() == PINS[name], 'input_hash:' + name)
    return body.decode('utf-8')


def select_class(text, name):
    module = ast.parse(text, filename=name, mode='exec')
    classes = [node for node in module.body
               if isinstance(node, ast.ClassDef) and node.name == 'TransitionFailure']
    require(len(classes) == 1, 'unique_class:' + name)
    node = classes[0]
    require(not node.decorator_list and not node.keywords, 'class_decorators_keywords')
    require(len(node.bases) == 1 and isinstance(node.bases[0], ast.Name)
            and node.bases[0].id == 'RuntimeError', 'class_base')
    require(not getattr(node, 'type_params', []), 'class_type_parameters')
    for item in ast.walk(node):
        require(type(item) in ALLOWED_NODES, 'unexpected_node:' + type(item).__name__)
        if isinstance(item, ast.FunctionDef):
            require(item.name == '__init__' and not item.decorator_list
                    and item.returns is None and not getattr(item, 'type_params', []),
                    'method_shape')
    return node


def dump(node):
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def execute_class(node):
    # No full-module exec/import. Only a separately exact-compared class reaches
    # this function, or its single dictionary-entry deletion mutant below.
    namespace = {
        '__name__': 'isolated_transition_diagnostic_class',
        '__builtins__': {
            '__build_class__': builtins.__build_class__,
            'RuntimeError': RuntimeError,
            'tuple': tuple,
            'super': super,
        },
    }
    module = ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(node)], type_ignores=[]))
    exec(compile(module, '<isolated TransitionFailure only>', 'exec'), namespace, namespace)
    result = namespace['TransitionFailure']
    require(result.__bases__ == (RuntimeError,), 'executed_base')
    return result


def attributes(error, code, operation, state, cleanup):
    require(type(error).__bases__ == (RuntimeError,), 'exception_type')
    require(error.code == code and error.operation_id == operation and error.sqlstate == state,
            'identity_attributes')
    require(error.cleanup_errors == tuple(cleanup), 'cleanup_attribute')
    require(error.effects == 'INSPECT_JOURNAL' and error.retry == 'after_inspection',
            'effect_retry_attributes')
    require(error.args == (str(error),), 'runtimeerror_args')


def expected_message(code, operation, state, cleanup, remedy):
    suffix = ''.join(f' cleanup={stage}:{cause}:{sqlstate or "UNKNOWN"};'
                     for stage, cause, sqlstate in cleanup)
    return (f'{code}; operation={operation or "unstarted"}; SQLSTATE={state or "UNKNOWN"}. '
            'Keep writers stopped. Inspect this operation and the external current policy before resume.'
            + remedy + suffix)


def new_oracle(cls, code, operation=None, state=None, cleanup=()):
    error = cls(code, operation, state, cleanup_errors=cleanup)
    attributes(error, code, operation, state, cleanup)
    require(str(error) == expected_message(code, operation, state, cleanup, NEW[code]),
            'new_message:' + code)


def main():
    before = {name: read_pinned(name) for name in PINS}
    baseline_text = before['migration.baseline.py']
    derivative_text = before['migration.derivative.py']
    contract_text = before['TransitionFailure.contract.py']
    anchor = '        remedy = {\n'
    addition = ''.join(f'            {code!r}: {message!r},\n' for code, message in NEW.items())
    require(baseline_text.count(anchor) == 1 and contract_text.count(anchor) == 1, 'unique_anchor')
    require(derivative_text == baseline_text.replace(anchor, anchor + addition, 1), 'exact_three_entry_delta')
    baseline = select_class(baseline_text, 'baseline')
    derivative = select_class(derivative_text, 'derivative')
    contract = select_class(contract_text, 'contract')
    expected_derivative = select_class(contract_text.replace(anchor, anchor + addition, 1), 'expected')
    require(dump(baseline) == dump(contract), 'exact_baseline_class_contract')
    require(dump(derivative) == dump(expected_derivative), 'exact_derivative_class_contract')
    old_cls, new_cls = execute_class(baseline), execute_class(derivative)
    cases = []
    variants = (
        ('default', None, None, ()),
        ('context_cleanup', '00000000-0000-0000-0000-000000000123', '08006',
         (('rollback', 'RuntimeError', None), ('close', 'OSError', '08003'))),
    )
    for code in NEW:
        for variant, operation, state, cleanup in variants:
            old = old_cls(code, operation, state, cleanup_errors=cleanup)
            attributes(old, code, operation, state, cleanup)
            require(str(old) == expected_message(code, operation, state, cleanup, ''), 'baseline_new_code')
            new_oracle(new_cls, code, operation, state, cleanup)
            cases.append('new:' + code + ':' + variant)
    for code in OLD + ('unknown_diagnostic_code',):
        for variant, operation, state, cleanup in variants:
            old = old_cls(code, operation, state, cleanup_errors=cleanup)
            new = new_cls(code, operation, state, cleanup_errors=cleanup)
            attributes(old, code, operation, state, cleanup)
            attributes(new, code, operation, state, cleanup)
            require(str(new) == str(old), 'existing_message:' + code)
            if code == 'unknown_diagnostic_code':
                require(str(new) == expected_message(code, operation, state, cleanup, ''), 'unknown_fallback')
            else:
                require(str(new) != expected_message(code, operation, state, cleanup, ''), 'existing_remedy_present')
            cases.append('compatible:' + code + ':' + variant)
    # Three meaningful sensitivity controls. Each missing-entry mutant must fail
    # its specific new-message oracle, not merely raise some unrelated error.
    mutants = []
    for code in NEW:
        mutant = copy.deepcopy(derivative)
        dictionaries = [item for item in ast.walk(mutant) if isinstance(item, ast.Dict)
                        and any(isinstance(key, ast.Constant) and key.value == code for key in item.keys)]
        require(len(dictionaries) == 1, 'unique_mutant_dictionary')
        target = dictionaries[0]
        positions = [i for i, key in enumerate(target.keys)
                     if isinstance(key, ast.Constant) and key.value == code]
        require(len(positions) == 1, 'unique_mutant_entry')
        index = positions[0]
        del target.keys[index]
        del target.values[index]
        mutant_cls = execute_class(mutant)
        try:
            new_oracle(mutant_cls, code)
        except AssertionError as error:
            require(str(error) == 'new_message:' + code, 'mutant_wrong_failure')
        else:
            raise AssertionError('mutant_not_detected:' + code)
        mutants.append('removed_entry:' + code)
    require(len(cases) == 20 and len(set(cases)) == 20 and len(mutants) == 3, 'case_inventory')
    for name, body in before.items():
        require(read_pinned(name) == body, 'input_preservation:' + name)
    print(json.dumps({
        'status': 'PASS_ISOLATED_CLASS_DIAGNOSTICS',
        'cases': cases, 'case_count': len(cases),
        'detected_message_mutants': mutants,
        'scope': 'Exact extracted class only; not a real-module, native, security or lifecycle qualification',
        'product_module_imported': False, 'database_used': False,
        'candidate_mutated': False, 'input_preservation': True,
    }, sort_keys=True))


if __name__ == '__main__':
    main()

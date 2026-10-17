"""Invoke unchanged literal recording tests directly; no pytest session/plugins."""
import test_fixture_ownership_recording as cases
import test_sqlalchemy_search as fixture

SPEC = (
 ('test_preflight_refusal_precedes_engine_or_mutation', ('bad_at',), (0,1,3)),
 ('test_successful_preflight_before_owner_engine', (), (None,)),
 ('test_unacquired_schema_never_dropped', ('failure',), ('create_collision','commit_ambiguous')),
 ('test_owned_schema_cleaned_after_body', ('body_error',), (None,'RuntimeError','KeyboardInterrupt')),
 ('test_full_fixture_acquisition_cleanup_boundaries', ('fault','expected'),
  ('owner_acquire','runtime_acquire','registry_acquire','mapping_setup','create','commit','create_all',
   'runtime_dispose','mapping_dispose','owner_dispose')),
)


def run_cases(migration, unused):
    records=[]
    assert cases.fixture is fixture
    assert set(name for name in vars(cases) if name.startswith('test_')) == {s[0] for s in SPEC}
    for name,argument_names,expected_ids in SPEC:
        fn=getattr(cases,name)
        if argument_names:
            marks=fn.pytestmark
            assert len(marks)==1 and marks[0].name=='parametrize'
            assert tuple(marks[0].args[0].split(','))==argument_names
            values=marks[0].args[1]
        else:
            assert not hasattr(fn,'pytestmark')
            values=[None]
        assert len(values)==len(expected_ids)
        for index,(value,expected_id) in enumerate(zip(values,expected_ids)):
            if name=='test_owned_schema_cleaned_after_body':
                observed=None if value is None else type(value).__name__
            elif len(argument_names)==2:
                observed=value[0]
            else: observed=value
            assert observed==expected_id
            args=() if not argument_names else (tuple(value) if len(argument_names)==2 else (value,))
            try:
                fn(*args)
            except BaseException as error:
                records.append({'id':name+':'+str(index),'status':'FAIL','type':type(error).__name__})
                return records
            records.append({'id':name+':'+str(index),'status':'PASS'})
    assert len(records)==19
    return records

"""Source-only controls for explicit package selection; no interpreter is run."""
from pathlib import Path
import shutil
import pytest
from _bridge_binding import binding,verify_source,verify_package


@pytest.fixture
def selected(tmp_path):
    legacy=tmp_path/'candidate-legacy'
    current=tmp_path/'candidate-current'
    python=tmp_path/'release-lab/env/bin/python'
    for root in (legacy,current):
        (root/'scripts').mkdir(parents=True)
        (root/'scripts/test_postgres.py').write_text('# same synthetic runner\n')
    (current/'src/cryptalis').mkdir(parents=True)
    (current/'src/cryptalis/__init__.py').write_text('# synthetic package\n')
    (current/'src/cryptalis/lifecycle.py').write_text('# synthetic lifecycle\n')
    (current/'tests').mkdir()
    (current/'tests/test_helper.py').write_text('# synthetic helper\n')
    python.parent.mkdir(parents=True)
    python.write_text('not an executable; this test never starts it\n')
    return legacy,current,python,binding(str(current),str(python),legacy)


@pytest.mark.parametrize('missing',['both','source','python'])
def test_bridge_requires_each_explicit_target_input(selected,missing):
    legacy,current,python,_=selected
    with pytest.raises(ValueError,match='both .* are required'):
        binding(None if missing in ('both','source') else str(current),
                None if missing in ('both','python') else str(python),legacy)


def test_bridge_cannot_select_the_legacy_package_as_current(selected):
    legacy,_,python,_=selected
    with pytest.raises(ValueError,match='separate explicit candidate'):
        binding(str(legacy),str(python),legacy)


def test_bridge_refuses_a_changed_role_preflight(selected):
    legacy,current,python,_=selected
    (current/'scripts/test_postgres.py').write_text('# different runner\n')
    with pytest.raises(ValueError,match='unchanged dual-role preflight'):
        binding(str(current),str(python),legacy)


@pytest.mark.parametrize('drift',['runtime','helper','runner'])
def test_selected_source_change_is_detected_before_child_launch(selected,drift):
    _,current,_,chosen=selected
    path={'runtime':'src/cryptalis/lifecycle.py','helper':'tests/test_helper.py',
          'runner':'scripts/test_postgres.py'}[drift]
    (current/path).write_text('# changed after selection\n')
    with pytest.raises(ValueError,match='changed after explicit selection'):
        verify_source(chosen)


@pytest.mark.parametrize('drift',['changed','missing','extra'])
def test_complete_installed_module_binding_refuses_mixed_or_partial_package(selected,tmp_path,drift):
    _,current,_,chosen=selected
    installed=tmp_path/'installed/cryptalis'
    shutil.copytree(current/'src/cryptalis',installed)
    verify_source(chosen)
    verify_package(installed,chosen)
    if drift=='changed':(installed/'lifecycle.py').write_text('# wrong revision\n')
    elif drift=='missing':(installed/'lifecycle.py').unlink()
    else:(installed/'unselected_module.py').write_text('# unexpected old module\n')
    with pytest.raises(ValueError,match='not the complete selected runtime'):
        verify_package(installed,chosen)

"""Opt-in bridge options; no default target and no product admission."""
from pathlib import Path
import pytest
from _bridge_binding import binding


def pytest_addoption(parser):
    parser.addoption('--bridge-target-source', default=None,
                     help='Required explicit frozen current candidate for bridge tests')
    parser.addoption('--bridge-target-python', default=None,
                     help='Required installed interpreter whose complete package matches that candidate')


@pytest.fixture
def bridge_target(request):
    try:
        return binding(request.config.getoption('--bridge-target-source'),
                       request.config.getoption('--bridge-target-python'),
                       Path(__file__).resolve().parents[2])
    except (ValueError, OSError) as error:
        raise pytest.UsageError(str(error)) from None

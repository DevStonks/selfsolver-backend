"""Smoke-test the app version."""
from selfsolver import __version__


def test_version():
    """Check for version match."""
    assert __version__ == "0.1.0"

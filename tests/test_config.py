"""Set up configuration from environment variables."""

import pytest

from selfsolver.app_factory import create_app
from selfsolver.config import TestingConfiguration


@pytest.fixture()
def fake_url(faker):
    """Provide a fake url as a fixture."""
    return faker.url()


@pytest.fixture()
def fake_hex(faker):
    """Provide a fake hexstring as a fixture."""
    return faker.binary(16).hex()


@pytest.fixture()
def fake_db_uri():
    """Provide a fake database uri as a fixture."""
    return "postgresql://postgres@localhost/cosmic-horror"


@pytest.fixture()
def _patch_environment(monkeypatch, fake_url, fake_hex, fake_db_uri):
    """Monkeypatch environment variables."""
    monkeypatch.setenv("TEST_DATABASE_URL", fake_db_uri)
    monkeypatch.setenv("JWT_SECRET_KEY", fake_hex)
    monkeypatch.setenv("PASSWORD_PEPPER", fake_hex)
    monkeypatch.setenv("SELFSOLVER_ENDUSER_APP", fake_url)


@pytest.mark.usefixtures("_patch_environment")
def test_config(fake_hex, fake_url, fake_db_uri):
    """Test configuration values are loaded from environment."""
    app = create_app(TestingConfiguration())

    assert app.config["SQLALCHEMY_DATABASE_URI"] == fake_db_uri
    assert app.config["JWT_SECRET_KEY"] == bytes.fromhex(fake_hex)
    assert app.config["PASSWORD_PEPPER"] == bytes.fromhex(fake_hex)
    assert app.config["SELFSOLVER_ENDUSER_APP"] == fake_url

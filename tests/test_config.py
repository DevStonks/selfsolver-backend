"""Set up configuration from environment variables."""
import importlib

import pytest

SECRET = "b78dcfe9c98e8342c29ead18e79aff6e42bc0e975261d0966ae74647624498cc"


@pytest.fixture(autouse=True)
def _config(monkeypatch):
    """Monkeypatch environment variables."""
    monkeypatch.setenv(
        "TEST_DATABASE_URL", "postgresql://postgres@localhost/cosmic-horror"
    )
    monkeypatch.setenv("JWT_SECRET_KEY", SECRET)
    monkeypatch.setenv("PASSWORD_PEPPER", SECRET)


def test_config():
    """Test configuration values are loaded from environment."""
    import selfsolver.config

    config = importlib.reload(selfsolver.config)

    assert (
        config.Configuration.SQLALCHEMY_DATABASE_URI
        == "postgresql://postgres@localhost/cosmic-horror"
    )
    assert config.Configuration.JWT_SECRET_KEY == bytes.fromhex(SECRET)
    assert config.Configuration.PASSWORD_PEPPER == bytes.fromhex(SECRET)

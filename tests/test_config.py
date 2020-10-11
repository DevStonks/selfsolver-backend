"""Set up configuration from environment variables."""
import pytest

SECRET = "b78dcfe9c98e8342c29ead18e79aff6e42bc0e975261d0966ae74647624498cc"


@pytest.fixture(autouse=True)
def _config(monkeypatch):
    """Monkeypatch environment variables."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres@localhost/selfsolver")
    monkeypatch.setenv("JWT_SECRET_KEY", SECRET)
    monkeypatch.setenv("PASSWORD_PEPPER", SECRET)


def test_config():
    """Test configuration values are loaded from environment."""
    from selfsolver.config import Configuration

    assert (
        Configuration.SQLALCHEMY_DATABASE_URI
        == "postgresql://postgres@localhost/selfsolver-test"
    )
    assert Configuration.JWT_SECRET_KEY == bytes.fromhex(SECRET)
    assert Configuration.PASSWORD_PEPPER == bytes.fromhex(SECRET)

"""Test password hashing and verifying."""
import pytest


@pytest.fixture()
def password(monkeypatch):
    """Monkeypatch password module to hardcode password pepper."""
    monkeypatch.setattr(
        "selfsolver.config.PASSWORD_PEPPER",
        "b78dcfe9c98e8342c29ead18e79aff6e42bc0e975261d0966ae74647624498cc",
    )
    from selfsolver import password

    return password


@pytest.fixture()
def precomputed_hash():
    """Provide a precomputed hash as a fixture."""
    return (
        "$argon2id$v=19$m=102400,t=2,p=8$ViqFkDImZIxRinGutbZWKg$McQuTE/ycaPWBiVVuLmtxQ"
    )


def test_verify(password, precomputed_hash):
    """Ensure hashed password can be verified."""
    assert password.verify("correct-horse-battery-staple", precomputed_hash)


def test_hash(password):
    """Ensure password is properly hashed."""
    hash = password.hash("528491")
    assert password.verify("528491", hash)

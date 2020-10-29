"""Test password hashing and verifying."""
import pytest

from selfsolver import password


@pytest.fixture()
def _patch_app_pepper(monkeypatch, app):
    """Monkeypatch app pepper."""
    monkeypatch.setitem(
        app.config,
        "PASSWORD_PEPPER",
        bytes.fromhex(
            "b78dcfe9c98e8342c29ead18e79aff6e42bc0e975261d0966ae74647624498cc"
        ),
    )


@pytest.fixture()
def precomputed_hash():
    """Provide a precomputed hash as a fixture."""
    return (
        "$argon2id$v=19$m=102400,t=2,p=8$ViqFkDImZIxRinGutbZWKg$McQuTE/ycaPWBiVVuLmtxQ"
    )


@pytest.mark.usefixtures("_patch_app_pepper")
def test_verify(app, precomputed_hash):
    """Ensure hashed password can be verified."""
    with app.app_context():
        assert password.verify("correct-horse-battery-staple", precomputed_hash)


def test_hash(app):
    """Ensure password is properly hashed."""
    with app.app_context():
        hash = password.hash("528491")
        assert password.verify("528491", hash)

"""Test custom flask commands."""
import pytest
from selfsolver.commands.database import create_all, recreate_all
from selfsolver.commands.secret import generate_secret


@pytest.fixture()
def runner():
    """Provide flask test cli runner as a fixture."""
    from selfsolver.app import app

    return app.test_cli_runner()


@pytest.fixture()
def db_create_all(monkeypatch, mocker):
    """Monkeypatch db.create_all and provide stub to check calls."""
    stub = mocker.stub(name="db.create_all")
    monkeypatch.setattr("selfsolver.models.db.create_all", stub)
    return stub


@pytest.fixture()
def db_drop_all(monkeypatch, mocker):
    """Monkeypatch db.drop_all and provide stub to check calls."""
    stub = mocker.stub(name="db.drop_all")
    monkeypatch.setattr("selfsolver.models.db.drop_all", stub)
    return stub


def test_generate_secret(runner):
    """Test generate-secret command."""
    result = runner.invoke(generate_secret)
    assert result.exit_code == 0
    assert result.output
    assert bytes.fromhex(result.output)


def test_database_setup(runner, db_create_all):
    """Test database setup command."""
    result = runner.invoke(create_all)
    db_create_all.assert_called_once()
    assert result.exit_code == 0


def test_database_reset(runner, db_create_all, db_drop_all):
    """Test database reset command."""
    result = runner.invoke(recreate_all)
    db_create_all.assert_called_once()
    db_drop_all.assert_called_once()
    assert result.exit_code == 0

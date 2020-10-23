"""Test custom flask commands."""
import pytest
from selfsolver.commands.create_user import create_user
from selfsolver.commands.database import create_all, recreate_all
from selfsolver.commands.secret import generate_secret
from selfsolver.models import User


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


@pytest.mark.usefixtures("db_session")
def test_create_user(runner, company):
    """Test create-user command."""
    result = runner.invoke(
        create_user, [str(company.id), "email@nanana.com", "tijolo22"]
    )
    user = User.query.filter_by(company_id=company.id).first()
    assert result.exit_code == 0
    assert user.id


@pytest.mark.usefixtures("db_session")
def test_create_user_without_password(runner, company):
    """Test create-user command."""
    result = runner.invoke(create_user, [str(company.id), "email@nanana.com"])
    user = User.query.filter_by(company_id=company.id).first()
    assert result.exit_code == 0
    assert user.id

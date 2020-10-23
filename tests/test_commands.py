"""Test custom flask commands."""
import pytest
from selfsolver.commands.create_user import create_user
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


@pytest.fixture()
def db_session_add(monkeypatch, mocker):
    """Monkeypatch db.session.add and provide stub to check calls."""
    stub = mocker.stub(name="db.session.add")
    monkeypatch.setattr("selfsolver.models.db.session.add", stub)
    return stub


@pytest.fixture()
def db_session_commit(monkeypatch, mocker):
    """Monkeypatch db.session.commit and provide stub to check calls."""
    stub = mocker.stub(name="db.session.commit")
    monkeypatch.setattr("selfsolver.models.db.session.commit", stub)
    return stub


@pytest.fixture()
def mock_user(monkeypatch, mocker):
    """Provide MockUser class and stub."""
    mock_user = mocker.stub(name="MockUser")
    monkeypatch.setattr("selfsolver.commands.create_user.User", mock_user)

    return mock_user


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


def test_create_user(runner, db_session_add, db_session_commit, mock_user):
    """Test create-user command."""
    result = runner.invoke(create_user, ["1", "email@nanana.com", "tijolo22"])
    mock_user.assert_called_once_with(  # noqa: S106
        email="email@nanana.com", password="tijolo22", company_id=1
    )
    db_session_add.assert_called_once_with(mock_user.return_value)
    db_session_commit.assert_called_once()
    assert result.exit_code == 0


def test_create_user_without_password(
    runner, db_session_add, db_session_commit, mock_user
):
    """Test create-user command."""
    result = runner.invoke(create_user, ["1", "email@nanana.com"])
    mock_user.assert_called_once_with(
        email="email@nanana.com", company_id=1, password=None
    )
    db_session_add.assert_called_once_with(mock_user.return_value)
    db_session_commit.assert_called_once()
    assert result.exit_code == 0

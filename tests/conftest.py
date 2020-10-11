"""Configure pytest globally."""
import pytest
from pytest_factoryboy import register

from tests.factories import UserFactory


@pytest.fixture(scope="session")
def _db():  # noqa: PT005
    """Provide _db fixture for pytest-flask-sqlalchemy own fixtures.

    Also, make sure all tables are created at the beginning of the session
    and destroyed at the end.
    """
    from selfsolver.models import db
    from selfsolver.app import app

    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


register(UserFactory)

"""Configure pytest globally."""
import pytest
from pytest_factoryboy import register

from selfsolver.config import TestingConfiguration
from selfsolver.models import db
from tests.factories import (
    BrandFactory,
    CompanyFactory,
    DeviceFactory,
    FamilyFactory,
    LocationFactory,
    TicketFactory,
    UserFactory,
)


@pytest.fixture(scope="session")
def app():
    """Provide app fixture for pytest-flask own fixtures."""
    from selfsolver.app_factory import create_app

    return create_app(TestingConfiguration())


@pytest.fixture(scope="session")
def _db(app):  # noqa: PT005
    """Provide _db fixture for pytest-flask-sqlalchemy own fixtures.

    Also, make sure all tables are created at the beginning of the session
    and destroyed at the end.
    """
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


register(BrandFactory)
register(CompanyFactory)
register(DeviceFactory)
register(FamilyFactory)
register(LocationFactory)
register(TicketFactory)
register(UserFactory)

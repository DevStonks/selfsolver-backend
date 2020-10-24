"""Set up model factories for testing."""
import factory
from selfsolver.models import Company, db, Location, User
from sqlalchemy.orm.scoping import scoped_session

TEST_EMAIL = "nanana@nonono.com"
TEST_PASSWORD = "correct-horse-battery-staple"
TEST_LABEL = "UNICHAMPZ"


class FlaskSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Connects factory meta session to a pytest-flask-sqlalchemy scoped session."""

    class Meta:  # noqa: D106
        abstract = True
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )
        sqlalchemy_session_persistence = "commit"


class CompanyFactory(FlaskSQLAlchemyModelFactory):
    """Create companies and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = Company


class LocationFactory(FlaskSQLAlchemyModelFactory):
    """Create location and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = Location

    label = TEST_LABEL
    company = factory.SubFactory(CompanyFactory)


class UserFactory(FlaskSQLAlchemyModelFactory):
    """Create users and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = User

    email = TEST_EMAIL
    password = TEST_PASSWORD
    company = factory.SubFactory(CompanyFactory)

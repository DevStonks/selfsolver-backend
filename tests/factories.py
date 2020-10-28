"""Set up model factories for testing."""
import factory
from sqlalchemy.orm.scoping import scoped_session

from selfsolver.models import Brand, Company, Family, Location, User, db


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

    label = factory.Faker("city")
    company = factory.SubFactory(CompanyFactory)


class UserFactory(FlaskSQLAlchemyModelFactory):
    """Create users and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = User

    email = factory.Faker("email")
    password = factory.Faker("password")
    company = factory.SubFactory(CompanyFactory)


class BrandFactory(FlaskSQLAlchemyModelFactory):
    """Create brand and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = Brand

    name = factory.Faker("company")


class FamilyFactory(FlaskSQLAlchemyModelFactory):
    """Create family and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = Family

    name = factory.Faker("color_name")
    brand = factory.SubFactory(BrandFactory)

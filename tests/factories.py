"""Set up model factories for testing."""
import factory
from selfsolver.models import db, User

TEST_EMAIL = "nanana@nonono.com"
TEST_PASSWORD = "correct-horse-battery-staple"


class FlaskSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Connects factory meta session to a pytest-flask-sqlalchemy scoped session."""

    @classmethod
    def _setup_next_sequence(cls):
        """Set sequence to start at 1 to keep postgres happy."""
        return 1

    class Meta:  # noqa: D106
        abstract = True
        sqlalchemy_session = db.create_scoped_session()
        sqlalchemy_session_persistence = "commit"


class UserFactory(FlaskSQLAlchemyModelFactory):
    """Create users and optionally save them to the database."""

    class Meta:  # noqa: D106
        model = User

    id = factory.Sequence(int)
    email = TEST_EMAIL
    password = TEST_PASSWORD

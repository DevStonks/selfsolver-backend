"""Read and expose configuration from environment variables."""
import os


# flake8: noqa: N802
class BaseConfiguration:
    """Base configuration from environment variables."""

    JWT_AUTH_USERNAME_KEY = "email"
    # https://github.com/pallets/flask-sqlalchemy/pull/727
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def JWT_SECRET_KEY(self):
        """Flask-JWT-extended configuration."""
        return bytes.fromhex(os.getenv("JWT_SECRET_KEY"))

    @property
    def PASSWORD_PEPPER(self):
        """Bytes to use as pepper on selfsolver.passwoed."""
        return bytes.fromhex(os.getenv("PASSWORD_PEPPER"))

    @property
    def SELFSOLVER_ENDUSER_APP(self):
        """Enduser app URL for CORS purposes."""
        return os.getenv("SELFSOLVER_ENDUSER_APP")

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """Flask-SQLAlchemy configuration."""
        return os.getenv("DATABASE_URL")


class TestingConfiguration(BaseConfiguration):
    """Testing configuration overrides."""

    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """Flask-SQLAlchemy configuration override for testing."""
        return os.getenv("TEST_DATABASE_URL")

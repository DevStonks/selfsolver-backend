"""Read and expose configuration from environment variables."""
import os


class BaseConfiguration:
    """Base configuration from environment variables."""

    JWT_AUTH_USERNAME_KEY = "email"
    JWT_SECRET_KEY = bytes.fromhex(os.getenv("JWT_SECRET_KEY"))
    PASSWORD_PEPPER = bytes.fromhex(os.getenv("PASSWORD_PEPPER"))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # https://github.com/pallets/flask-sqlalchemy/pull/727
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfiguration(BaseConfiguration):
    """Testing configuration overrides."""

    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    TESTING = True


Configuration = (
    TestingConfiguration if os.getenv("ENV") == "testing" else BaseConfiguration
)

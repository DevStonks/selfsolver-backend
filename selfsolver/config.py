"""Read and expose configuration from environment variables."""
import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
PASSWORD_PEPPER = os.getenv("PASSWORD_PEPPER")

"""Provide utils for hashing and verifying passwords."""
from passlib.context import CryptContext
from selfsolver import config

context = CryptContext(schemes=["argon2"])
PEPPER = bytes.fromhex(config.PASSWORD_PEPPER)


def hash(password):
    """Hash the password with PEPPER bytes."""
    return context.hash(PEPPER + password.encode("utf-8"))


def verify(password, hash):
    """Pepper the password and verify it matches stored hash."""
    return context.verify(PEPPER + password.encode("utf-8"), hash)

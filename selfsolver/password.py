"""Provide utils for hashing and verifying passwords."""
from flask import current_app
from passlib.context import CryptContext

context = CryptContext(schemes=["argon2"])


def hash(password):
    """Hash the password with PEPPER bytes."""
    pepper = current_app.config["PASSWORD_PEPPER"]
    return context.hash(pepper + password.encode("utf-8"))


def verify(password, hash):
    """Pepper the password and verify it matches stored hash."""
    pepper = current_app.config["PASSWORD_PEPPER"]
    return hash and context.verify(pepper + password.encode("utf-8"), hash)

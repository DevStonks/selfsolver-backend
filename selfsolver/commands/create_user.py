"""Provide a command for easy user creation.

Usage:
$ flask create-user test@example.com tijolo22
"""
import click
from flask.cli import with_appcontext
from selfsolver import password
from selfsolver.models import db, User


@click.command("create-user")
@click.argument("email")
@click.argument("passwd", metavar="PASSWORD")
@with_appcontext
def create_user(email, passwd):
    """Create a user with email and password (hashed)."""
    user = User(email=email, password=password.hash(passwd))
    db.session.add(user)
    db.session.commit()

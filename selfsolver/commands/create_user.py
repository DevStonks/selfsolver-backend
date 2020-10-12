"""Provide a command for easy user creation.

Usage:
$ flask create-user test@example.com tijolo22
"""
import click
from flask.cli import with_appcontext
from selfsolver.models import db, User


@click.command("create-user")
@click.argument("email")
@click.argument("password")
@with_appcontext
def create_user(email, password):
    """Create a user with email and password."""
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

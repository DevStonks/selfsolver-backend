"""Provide a command for easy user creation.

Usage:
$ flask create-user test@example.com tijolo22
"""
import click
from flask.cli import AppGroup
from flask.cli import with_appcontext
from selfsolver.models import db, User

user_cli = AppGroup("user")


@user_cli.command("create")
@click.argument("company_id", type=int)
@click.argument("email")
@click.argument("password", required=False)
@with_appcontext
def create_user(company_id, email, password=None):
    """Create a user with email and password."""
    user = User(email=email, password=password, company_id=company_id)
    db.session.add(user)
    db.session.commit()

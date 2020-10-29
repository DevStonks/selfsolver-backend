"""Provide a command for easy user creation.

Usage:
$ flask create-user test@example.com tijolo22
"""
import click
from flask.cli import AppGroup, with_appcontext
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

from selfsolver.models import User, db

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
    try:
        db.session.commit()
    except IntegrityError as exception:
        if isinstance(exception.orig, ForeignKeyViolation):
            raise click.UsageError(f"No company found with id {company_id}.")
        else:
            raise  # pragma: no cover

    click.echo(f"Created user {user.id}.")

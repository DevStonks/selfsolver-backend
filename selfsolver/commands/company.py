"""Provide a command for easy company creation.

Usage:
$ flask create-company test@example.com tijolo22
"""
import click
from flask.cli import AppGroup, with_appcontext
from selfsolver.models import Company, db

company_cli = AppGroup("company")


@company_cli.command("create")
@with_appcontext
def create_company():
    """Create a company."""
    company = Company()
    db.session.add(company)
    db.session.commit()
    click.echo(f"Created company {company}.")

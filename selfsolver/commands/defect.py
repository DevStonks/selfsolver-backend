"""Provide a command for easy defect creation.

Usage:
$ flask defect create 'This spoon is too big.'
"""
import click
from flask.cli import AppGroup, with_appcontext

from selfsolver.models import Defect, db

defect_cli = AppGroup("defect")


@defect_cli.command("create")
@click.argument("description")
@with_appcontext
def create_defect(description):
    """Create a defect."""
    defect = Defect(description=description)
    db.session.add(defect)
    db.session.commit()
    click.echo(f"Created defect {defect}.")

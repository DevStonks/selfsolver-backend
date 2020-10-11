"""Provide commands for database setup and reset (after model updates).

Usage:
$ flask database setup
$ flask database reset
"""
from flask import current_app
from flask.cli import AppGroup
from selfsolver.models import db

database_cli = AppGroup("database")


@database_cli.command("setup")
def create_all():
    """Create tables in database for all defined models."""
    db.create_all(app=current_app)


@database_cli.command("reset")
def recreate_all():
    """Drop all tables, then (re-)create them for all defined models."""
    db.drop_all(app=current_app)
    db.create_all(app=current_app)

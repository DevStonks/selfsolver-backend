from flask import current_app
from flask.cli import AppGroup
from selfsolver.models import db

database_cli = AppGroup('database')

@database_cli.command('setup')
def create_all():
    db.create_all(app=current_app)

@database_cli.command('reset')
def recreate_all():
    db.drop_all(app=current_app)
    db.create_all(app=current_app)
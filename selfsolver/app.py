"""Create and configure selfsolver flask application.

Configure the app, initialize all extensions (sqlalchemy and jwt) and register
selfsolver blueprints and commands.
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from selfsolver.blueprints.auth import auth
from selfsolver.commands.create_user import create_user
from selfsolver.commands.database import database_cli
from selfsolver.commands.secret import generate_secret
from selfsolver.models import db

app = Flask(__name__)
app.config.from_object("selfsolver.config.Configuration")

db.init_app(app)
JWTManager(app)

app.register_blueprint(auth)

app.cli.add_command(database_cli)
app.cli.add_command(create_user)
app.cli.add_command(generate_secret)

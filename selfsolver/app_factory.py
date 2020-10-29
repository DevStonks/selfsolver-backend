"""Provide a function to create and configure selfsolver flask application.

It should configure the app, initialize all extensions (sqlalchemy and jwt) and register
selfsolver blueprints and commands.
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from selfsolver.blueprints.auth import auth
from selfsolver.blueprints.enduser import enduser
from selfsolver.commands.company import company_cli
from selfsolver.commands.database import database_cli
from selfsolver.commands.secret import generate_secret
from selfsolver.commands.seed import seed
from selfsolver.commands.user import user_cli
from selfsolver.models import db
from selfsolver.schemas import ma


def create_app(configuration):
    """Create an app instance."""
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)
    ma.init_app(app)
    JWTManager(app)
    CORS(app, origins=[app.config["SELFSOLVER_ENDUSER_APP"]])

    app.register_blueprint(auth)
    app.register_blueprint(enduser)

    app.cli.add_command(generate_secret)
    app.cli.add_command(database_cli)
    app.cli.add_command(company_cli)
    app.cli.add_command(user_cli)
    app.cli.add_command(seed)

    return app

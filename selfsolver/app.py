from flask import Flask
from flask_jwt_extended import JWTManager
from selfsolver import config
from selfsolver.blueprints.auth import auth
from selfsolver.commands.create_user import create_user
from selfsolver.commands.database import database_cli
from selfsolver.commands.secret import generate_secret
from selfsolver.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["JWT_SECRET_KEY"] = bytes.fromhex(config.JWT_SECRET_KEY)
app.config["JWT_AUTH_USERNAME_KEY"] = "email"

db.init_app(app)
JWTManager(app)

app.register_blueprint(auth)

app.cli.add_command(database_cli)
app.cli.add_command(create_user)
app.cli.add_command(generate_secret)

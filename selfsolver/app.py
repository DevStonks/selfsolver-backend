from flask import Flask
from flask_jwt_extended import JWTManager
from selfsolver import config
from selfsolver.models import db
from selfsolver.blueprints.auth import auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = bytes.fromhex(config.JWT_SECRET_KEY)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

db.init_app(app)
JWTManager(app)

app.register_blueprint(auth)
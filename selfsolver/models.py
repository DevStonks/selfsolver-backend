from flask_sqlalchemy import SQLAlchemy
from .app import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'
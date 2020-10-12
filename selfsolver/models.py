"""Set up database models for selfsolver app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Hold user data from the database."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        """Represent a user instance in python shell."""
        return f"<User id={self.id} email={self.email}>"

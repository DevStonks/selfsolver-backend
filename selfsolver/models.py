"""Set up database models for selfsolver app."""
from flask_sqlalchemy import SQLAlchemy
from selfsolver.password import hash

db = SQLAlchemy()


class User(db.Model):
    """Hold end-user info and credentials."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    @property
    def password(self):
        """Get or set the user password. Automatically hashed on set."""
        return self._password

    @password.setter
    def password(self, passwd):
        """Hash password and set to user.password."""
        self._password = hash(passwd) if passwd else None

    def __repr__(self):
        """Represent a user instance in python shell."""
        return f"<User id={self.id} email={self.email}>"


class Company(db.Model):
    """Hold client company info."""

    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("User", cascade="all,delete-orphan", backref="company")

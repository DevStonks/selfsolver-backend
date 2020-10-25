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
    locations = db.relationship(
        "Location", cascade="all,delete-orphan", backref="company"
    )


class Location(db.Model):
    """Hold location info."""

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    label = db.Column(db.String(64), nullable=False)
    printers = db.relationship(
        "Printer", cascade="all,delete-orphan", backref="location"
    )


class Brand(db.Model):
    """Hold brand info."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    models = db.relationship("Model", cascade="all,delete-orphan", backref="brand")


class Model(db.Model):
    """Hold model info."""

    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    printers = db.relationship("Printer", cascade="all,delete-orphan", backref="model")


class Printer(db.Model):
    """Hold printer info."""

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)
    serial_number = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    tickets = db.relationship("Ticket", cascade="all,delete-orphan", backref="printer")


class Solution(db.Model):
    """Hold solution info."""

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)


class Ticket(db.Model):
    """Hold ticket info."""

    id = db.Column(db.Integer, primary_key=True)
    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey("solution.id"), nullable=False)
    send_time = db.Column(db.DateTime, nullable=False)
    forward_time = db.Column(db.DateTime, nullable=True)
    closed_time = db.Column(db.DateTime, nullable=False)


class Defect(db.Model):
    """Hold defect info."""

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)


class Occurrence(db.Model):
    """Hold occurrence info."""

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)
    defect_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)

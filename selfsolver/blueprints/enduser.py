"""Provide routes for enduser app."""
from flask import Blueprint, abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, ValidationError, fields

from selfsolver.models import (
    Company,
    Defect,
    Device,
    Location,
    Occurrence,
    Solution,
    Ticket,
    User,
    db,
)
from selfsolver.schemas import DefectSchema, DeviceSchema, SolutionSchema, TicketSchema

enduser = Blueprint("enduser", __name__)


@enduser.route("/tickets", methods=["GET"])
@jwt_required
def tickets():
    """Return the list of tickets for current user's company."""
    current_user = get_jwt_identity()
    tickets = Ticket.query.join(Device, Location, Company, User).filter(
        User.id == current_user, Ticket.closed.is_(None)
    )

    return TicketSchema(many=True).jsonify(tickets)


@enduser.route("/devices", methods=["GET"])
@jwt_required
def devices():
    """Return the list of devices for current user's company."""
    current_user = get_jwt_identity()
    devices = Device.query.join(Location, Company, User).filter(User.id == current_user)

    return DeviceSchema(many=True).jsonify(devices)


@enduser.route("/defects", methods=["GET"])
@jwt_required
def defects():
    """Return the list of known defects."""
    defects = Defect.query.all()

    return DefectSchema(many=True).jsonify(defects)


class NewTicketSchema(Schema):
    """Schema for ticket POST request data."""

    defect = fields.Integer(required=True)
    device = fields.Integer(required=True)


@enduser.route("/tickets", methods=["POST"])
@jwt_required
def create_ticket():
    """Create a ticket for a specific device."""
    current_user = get_jwt_identity()

    try:
        data = NewTicketSchema().load(request.json)
    except ValidationError:
        print("valerr")
        abort(400)

    defect = Defect.query.filter(Defect.id == data["defect"]).first()
    device = (
        Device.query.join(Location, Company, User)
        .filter(User.id == current_user, Device.id == data["device"])
        .first()
    )

    if not (defect and device):
        abort(400)

    ticket = Ticket(device=device)
    occurrence = Occurrence(ticket=ticket, defect=defect)

    db.session.add(occurrence)
    db.session.commit()

    return TicketSchema().jsonify(ticket)


@enduser.route("/tickets/<int:ticket_id>/solutions", methods=["GET"])
@jwt_required
def solutions_for_ticket(ticket_id):
    """Create a ticket for a specific device."""
    solutions = Solution.query.all()
    return SolutionSchema(many=True).jsonify(solutions)

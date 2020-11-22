"""Provide routes for enduser app."""
from datetime import datetime

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
        abort(400)

    defect = Defect.query.get(data["defect"])
    device = Defect.query.get(data["device"])

    if not (defect and device):
        abort(404)

    device = (
        Device.query.join(Location, Company, User)
        .filter(User.id == current_user, Device.id == data["device"])
        .first()
    )

    if not device:
        abort(403)

    ticket = Ticket(device=device)
    occurrence = Occurrence(ticket=ticket, defect=defect)

    db.session.add(occurrence)
    db.session.commit()

    return TicketSchema().jsonify(ticket)


@enduser.route("/tickets/<int:ticket_id>/solutions", methods=["GET"])
@jwt_required
def solutions_for_ticket(ticket_id):
    """Get available solutions for current ticket."""
    solutions = Solution.query.all()
    # @TODO: rank tickets.
    return SolutionSchema(many=True).jsonify(solutions)


class TicketSolvedSchema(Schema):
    """Schema for ticket POST request data."""

    solution = fields.Integer(required=False)
    forwarded = fields.Boolean(required=False)


@enduser.route("/tickets/<int:ticket_id>", methods=["PUT"])
@jwt_required
def close_ticket(ticket_id):
    """Create a ticket for a specific device."""
    current_user = get_jwt_identity()

    try:
        data = TicketSolvedSchema().load(request.json)
    except ValidationError:
        abort(400)

    solution = data.get("solution", None)
    forwarded = data.get("forwarded", None)

    # one is required
    if not (solution or forwarded):
        abort(400)

    if not Ticket.query.get(ticket_id):
        abort(404)

    if solution and not Solution.query.get(solution):
        abort(404)

    ticket = (
        Ticket.query.join(Device, Location, Company, User)
        .filter(User.id == current_user, Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        abort(403)

    if solution:
        ticket.solution_id = solution
        ticket.closed = datetime.now()

    elif forwarded:
        ticket.forwarded = datetime.now()

    db.session.add(ticket)
    db.session.commit()

    return TicketSchema().jsonify(ticket)

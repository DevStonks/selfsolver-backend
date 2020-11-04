"""Provide routes for enduser app."""
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from selfsolver.models import Company, Device, Location, Ticket, User
from selfsolver.schemas import DeviceSchema, TicketSchema

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
    """Return the list of tickets for current user's company."""
    current_user = get_jwt_identity()
    devices = Device.query.join(Location, Company, User).filter(User.id == current_user)

    return DeviceSchema(many=True).jsonify(devices)

"""Provide routes for enduser app."""
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from selfsolver.models import Company, Device, Location, Ticket, User
from selfsolver.schemas import TicketSchema

enduser = Blueprint("enduser", __name__)


@enduser.route("/tickets", methods=["GET"])
@jwt_required
def tickets():
    """Return the list of tickets for current user's company."""
    current_user = get_jwt_identity()
    tickets = Ticket.query.join(Device, Location, Company, User).filter(
        User.id == current_user, Ticket.closed.is_(None)
    )

    schema = TicketSchema(many=True)

    return jsonify(tickets=schema.dump(tickets))

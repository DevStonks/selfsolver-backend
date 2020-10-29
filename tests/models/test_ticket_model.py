"""Test selfsolver ticket model."""

from selfsolver.models import Ticket


def test_ticket_creation(db_session, device):
    """Test ticket creation."""
    ticket = Ticket(device=device)
    db_session.add(ticket)
    db_session.commit()

    assert ticket.id

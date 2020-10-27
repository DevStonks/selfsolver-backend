"""Test selfsolver location model."""
from selfsolver.models import Location


def test_location_creation(db_session, company, location_factory):
    """Test user creation."""
    location = Location(label=location_factory.label, company=company)
    db_session.add(location)
    db_session.commit()

    assert location.id
    assert location.label == location_factory.label

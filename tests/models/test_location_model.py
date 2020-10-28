"""Test selfsolver location model."""
import pytest

from selfsolver.models import Location


@pytest.fixture()
def location_stub(location_factory):
    """Provide a location stub as a fixture."""
    return location_factory.stub()


def test_location_creation(db_session, company, location_stub):
    """Test location creation."""
    location = Location(label=location_stub.label, company=company)
    db_session.add(location)
    db_session.commit()

    assert location.id
    assert location.label == location_stub.label

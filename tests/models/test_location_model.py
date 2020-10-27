"""Test selfsolver location model."""
import pytest

from selfsolver.models import Location


@pytest.fixture()
def label(location_factory):
    """Provide a random label fixture."""
    return location_factory.label.generate({"locale": None})


def test_location_creation(db_session, company, label):
    """Test location creation."""
    location = Location(label=label, company=company)
    db_session.add(location)
    db_session.commit()

    assert location.id
    assert location.label == label

"""Test selfsolver location model."""
import pytest
from sqlalchemy.exc import IntegrityError

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


@pytest.mark.parametrize("option", ["label"])
def test_location_creation_without_required(db_session, location_factory, option):
    """Test location creation fails without required parameters."""
    location = location_factory.build(**{option: None})
    db_session.add(location)
    with pytest.raises(IntegrityError, match="psycopg2.errors.NotNullViolation"):
        db_session.commit()

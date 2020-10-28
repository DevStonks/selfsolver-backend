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


def test_label_creation_with_non_existing_company(db_session, label):
    """Test user creation fails with non-existing company."""
    location = Location(label=label, company_id=1)
    db_session.add(location)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()


def test_location_update_with_non_existing_company(db_session, location):
    """Test updating location company to non-existing company."""
    location.company_id = 1
    db_session.add(location)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()

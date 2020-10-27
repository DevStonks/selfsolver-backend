"""Test selfsolver company model."""
import pytest

from selfsolver.models import Company, Location, User


@pytest.fixture()
def user_and_location(db_session, user, location_factory):
    """Provide both user and location fixtures with the same company."""
    location = location_factory(company=user.company)
    db_session.add(location)
    db_session.commit()
    return user, location


def test_company_creation(db_session):
    """Test company creation."""
    company = Company()
    db_session.add(company)
    db_session.commit()

    assert company.id


def test_company_cascades(db_session, user_and_location):
    """Test users and locations are deleted when company is deleted."""
    user, location = user_and_location
    db_session.delete(user.company)
    db_session.commit()

    assert not db_session.query(User).all()
    assert not db_session.query(Location).all()

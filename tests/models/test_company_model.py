"""Test selfsolver company model."""
import pytest

from selfsolver.models import Company, Location, User


def test_company_creation(db_session):
    """Test company creation."""
    company = Company()
    db_session.add(company)
    db_session.commit()

    assert company.id


@pytest.mark.usefixtures("db_session", "location")
def test_company_cascades(db_session, user):
    """Test users and locations are deleted when company is deleted."""
    db_session.delete(user.company)
    db_session.commit()

    assert not db_session.query(User).all()
    assert not db_session.query(Location).all()

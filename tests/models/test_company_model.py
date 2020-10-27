"""Test selfsolver company model."""
from selfsolver.models import Company, User


def test_company_creation(db_session):
    """Test company creation."""
    company = Company()
    db_session.add(company)
    db_session.commit()

    assert company.id


def test_company_cascades(db_session, user):
    """Test users are deleted when company is deleted."""
    db_session.delete(user.company)
    db_session.commit()

    assert not db_session.query(User).all()
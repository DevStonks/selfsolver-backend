"""Test selfsolver database models."""
import pytest
from selfsolver.models import Company, User
from selfsolver.password import verify
from sqlalchemy.exc import IntegrityError


def test_company_creation(db_session):
    """Test company creation."""
    company = Company()
    db_session.add(company)
    db_session.commit()

    assert company.id


def test_user_creation(db_session, company, user_factory):
    """Test user creation."""
    user = User(
        email=user_factory.email, password=user_factory.password, company=company
    )
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email == user_factory.email
    assert verify(user_factory.password, user.password)


def test_user_creation_without_email(db_session, user_factory):
    """Test user creation fails without email."""
    user = user_factory.build(email=None)
    db_session.add(user)
    with pytest.raises(IntegrityError, match="psycopg2.errors.NotNullViolation"):
        db_session.commit()


def test_user_creation_without_company(db_session, user_factory):
    """Test user creation fails without company."""
    user = user_factory.build(company=None)
    db_session.add(user)
    with pytest.raises(IntegrityError, match="psycopg2.errors.NotNullViolation"):
        db_session.commit()


def test_user_retrieval(db_session, user):
    """Test user retrieval."""
    retrieved = db_session.query(User).first()

    assert retrieved.id == user.id
    assert retrieved.email == user.email
    assert retrieved.password == user.password
    assert retrieved.company.id == user.company.id


def test_user_retrieval_non_existing_id(db_session, user):
    """Test user retrieval fails with non-existing id."""
    retrieved = db_session.query(User).get(1337)
    assert retrieved is None


def test_user_update(db_session, user):
    """Test user update."""
    user.email = "carmen@vile.org"
    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).first()

    assert retrieved.id == user.id
    assert retrieved.email == "carmen@vile.org"
    assert retrieved.password == user.password


def test_user_update_remove_email(db_session, user):
    """Test user update."""
    user.email = None
    db_session.add(user)

    with pytest.raises(IntegrityError, match="psycopg2.errors.NotNullViolation"):
        db_session.commit()


def test_user_delete(db_session, user):
    """Test user deletion."""
    db_session.delete(user)
    db_session.commit()

    retrieved = db_session.query(User).first()
    assert retrieved is None


def test_user_repr(db_session, user):
    """Test user model representation."""
    user.__repr__() == f"<User id={user.id} email=nanana@nonono.com>"


def test_company_cascades(db_session, user):
    """Test users are deleted when company is deleted."""
    db_session.delete(user.company)
    db_session.commit()

    assert not db_session.query(User).all()

"""Test selfsolver user model."""
import pytest
from sqlalchemy.exc import IntegrityError

from selfsolver.models import User
from selfsolver.password import verify


@pytest.fixture()
def email(user_factory):
    """Provide a random email fixture."""
    return user_factory.email.generate({"locale": None})


@pytest.fixture()
def password(user_factory):
    """Provide a random password fixture."""
    return user_factory.password.generate({"locale": None})


def test_user_create(db_session, company, email, password):
    """Test user creation."""
    user = User(email=email, password=password, company=company)
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email == email
    assert verify(password, user.password)


def test_user_create_without_password(db_session, user_factory, company):
    """Test user creation does not fail without password."""
    user = user_factory.build(password=None, company=company)
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email
    assert user.password is None


def test_user_update_without_password(db_session, user):
    """Test user update removes password."""
    user.password = None
    db_session.add(user)
    db_session.commit()

    assert user.password is None


def test_user_create_with_non_existing_company(db_session, email, password):
    """Test user creation fails with non-existing company."""
    user = User(email=email, password=password, company_id=1)
    db_session.add(user)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()


def test_user_update_with_non_existing_company(db_session, user):
    """Test updating user company to non-existing company."""
    user.company_id = 1
    db_session.add(user)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()


@pytest.mark.usefixtures("db_session")
def test_user_repr(user):
    """Test user model representation."""
    user.__repr__() == f"<User id={user.id} email=nanana@nonono.com>"

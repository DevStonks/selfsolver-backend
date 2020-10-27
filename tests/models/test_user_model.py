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


def test_user_creation(db_session, company, email, password):
    """Test user creation."""
    user = User(email=email, password=password, company=company)
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email == email
    assert verify(password, user.password)


def test_user_creation_without_password(db_session, user_factory, company):
    """Test user creation does not fail without password."""
    user = user_factory.build(password=None, company=company)
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email
    assert user.password is None


def test_user_creation_with_non_existing_company(db_session, email, password):
    """Test user creation fails with non-existing company."""
    user = User(email=email, password=password, company_id=1)
    db_session.add(user)

    with pytest.raises(IntegrityError, match="psycopg2.errors.ForeignKeyViolation"):
        db_session.commit()


@pytest.mark.parametrize("option", ["company", "email"])
def test_user_creation_without_required(db_session, user_factory, option):
    """Test user creation fails without required parameters."""
    user = user_factory.build(**{option: None})
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

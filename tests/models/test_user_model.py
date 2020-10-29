"""Test selfsolver user model."""
import pytest

from selfsolver.models import User
from selfsolver.password import verify


@pytest.fixture()
def user_stub(user_factory):
    """Provide a stub user as a fixture."""
    return user_factory.stub()


def test_user_create(db_session, company, user_stub):
    """Test user creation."""
    user = User(email=user_stub.email, password=user_stub.password, company=company)
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email == user_stub.email
    assert verify(user_stub.password, user.password)


def test_user_create_without_password(db_session, user_factory, company):
    """Test user creation does not fail without password."""
    user = user_factory.build(password=None, company=company)
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email
    assert user.password is None


def test_user_update_password(db_session, user, faker):
    """Test user update changes password."""
    password = faker.password()
    user.password = password
    db_session.add(user)
    db_session.commit()

    assert verify(password, user.password)


def test_user_update_without_password(db_session, user):
    """Test user update removes password."""
    user.password = None
    db_session.add(user)
    db_session.commit()

    assert user.password is None

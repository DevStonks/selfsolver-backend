"""Test selfsolver database models."""
from selfsolver.models import User


def test_user_creation(db_session, user_factory):
    """Test user creation."""
    user = user_factory.build()
    db_session.add(user)
    db_session.flush()

    assert user.id
    assert user.email == user_factory.email
    assert user.password == user_factory.password


def test_user_retrieval(db_session, user, user_factory):
    """Test user retrieval."""
    user = db_session.query(User).first()

    assert user.id
    assert user.email == user_factory.email
    assert user.password == user_factory.password

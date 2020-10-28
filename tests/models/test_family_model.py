"""Test selfsolver family family."""
import pytest

from selfsolver.models import Family


@pytest.fixture()
def family_stub(family_factory):
    """Provide a family stub as a fixture."""
    return family_factory.stub()


def test_family_creation(db_session, brand, family_stub):
    """Test family creation."""
    family = Family(name=family_stub.name, brand=brand)
    db_session.add(family)
    db_session.commit()

    assert family.id
    assert family.name == family_stub.name

"""Test selfsolver brand model."""
import pytest

from selfsolver.models import Brand


@pytest.fixture()
def brand_stub(brand_factory):
    """Provide a brand stub as a fixture."""
    return brand_factory.stub()


def test_brand_creation(db_session, brand_stub):
    """Test brand creation."""
    brand = Brand(name=brand_stub.name)
    db_session.add(brand)
    db_session.commit()

    assert brand.id
    assert brand.name == brand_stub.name

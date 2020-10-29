"""Test selfsolver device model."""
import pytest

from selfsolver.models import Device


@pytest.fixture()
def device_stub(device_factory):
    """Provide a device stub as a fixture."""
    return device_factory.stub()


def test_device_creation(db_session, device_stub, location, family):
    """Test device creation."""
    device = Device(serial=device_stub.serial, family=family, location=location)
    db_session.add(device)
    db_session.commit()

    assert device.id
    assert device.serial == device_stub.serial


def test_device_creation_without_location(db_session, device_stub, family):
    """Test device creation."""
    device = Device(serial=device_stub.serial, family=family)
    db_session.add(device)
    db_session.commit()

    assert device.id
    assert device.serial == device_stub.serial

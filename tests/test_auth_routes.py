"""Test the auth blueprint routes."""
import pytest
from flask import url_for
from flask_jwt_extended.utils import decode_token


@pytest.fixture()
def login_url():
    """Provide login url fixture."""
    return url_for("auth.login")


def test_login_without_data(client, login_url):
    """Ensure a 400 response for no data sent."""
    res = client.post(login_url)
    assert res.status_code == 400


@pytest.mark.usefixtures("db_session")
def test_login_with_missing_data(client, login_url, user_factory):
    """Ensure a 400 response for no data sent."""
    res = client.post(login_url, json={"email": user_factory.email})
    assert res.status_code == 400


@pytest.mark.usefixtures("db_session")
def test_login_with_non_matching_data(client, login_url, user):
    """Ensure a 401 response for wrong credentials."""
    res = client.post(login_url, json={"email": user.email, "password": "swordfish"})
    assert res.status_code == 401


@pytest.mark.usefixtures("db_session")
def test_login_with_matching_data(client, login_url, user, user_factory):
    """Ensure a 200 response with authtoken for right credentials."""
    res = client.post(
        login_url, json={"email": user.email, "password": user_factory.password}
    )
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert "access_token" in res.json

    payload = decode_token(res.json["access_token"])
    assert payload["identity"] == user.id

import pytest

from fastapi.testclient import TestClient

from unittest.mock import patch, MagicMock

from ..test_main import app

client = TestClient(app=app)


@pytest.fixture
def token():
    return {"auth_token": "token"}


@patch('os.getenv', MagicMock(return_value='https://fake.taiga.url'))
@patch("requests.post")
def test_auth(mock_get, token):
    mock_response = MagicMock()
    mock_response.json.return_value = token
    mock_get.return_value = mock_response

    response = client.post(
        "/auth",
        json={"username": "username", "password": "password"}
    )

    assert response.status_code == 200
    auth = response.json()["auth_token"]
    assert auth == "token"


def test_invalid_auth():
    response = client.post(
        "/auth",
        json={"username": "username", "password": "password"}
    )

    assert response.status_code == 401

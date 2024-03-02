import pytest

from fastapi.testclient import TestClient

from unittest.mock import patch, MagicMock

from ..test_main import app

client = TestClient(app=app)

@pytest.fixture
def token():
    return "token"

@patch('os.getenv', MagicMock(return_value='http://fake.taiga.url'))
@patch("requests.post")
def test_auth(mock_get, token):
    mock_response = MagicMock()
    mock_response.json.return_value = token
    mock_get.return_value = mock_response
    
    response = client.post(
        "/auth",
        json={"username": "username", "password": "password"}
    )
    
    assert response.status_code == 401

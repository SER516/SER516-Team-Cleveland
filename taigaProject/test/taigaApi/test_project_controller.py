import pytest

from fastapi.testclient import TestClient

from unittest.mock import patch, MagicMock

from ..test_main import app

client = TestClient(app=app)


@pytest.fixture
def project_request():
    return {
        "projectslug": "project"
    }


@pytest.fixture
def project_info():
    return {
        "id": 550011,
        "name": "project",
        "members": [
            {
                "full_name": "abcd",
                "username": "abcd",
                "id": 1
            },
            {
                "full_name": "pqrs",
                "username": "pqrs",
                "id": 2
            }
        ]
    }


@patch('os.getenv', MagicMock(return_value='https://fake.taiga.url'))
@patch("requests.get")
def test_get_project(mock_get, project_info):
    mock_response = MagicMock()
    mock_response.json.return_value = project_info
    mock_get.return_value = mock_response

    response = client.post(
        "/Project",
        json={"projectslug": "project"},
        headers={"token": "token"}
    )

    assert response.status_code == 200
    project_name = response.json()["name"]
    assert project_name is not None and project_name == "project"

    members = response.json()["members"]
    assert members
    assert len(members) == 2


def test_project_not_found():
    response = client.post(
        "/Project",
        json={"projectslug": "project"},
        headers={"token": "token"}
    )

    assert response.status_code == 404

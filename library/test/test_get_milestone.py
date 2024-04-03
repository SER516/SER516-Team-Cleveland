import pytest
from unittest.mock import MagicMock, patch

from ..milestone.get_milestone import get_milestone


@pytest.fixture
def milestone():
    return {
        "milestoneId": "1"
    }


@patch('os.getenv', MagicMock(return_value='https://fake.taiga.url'))
@patch('requests.get')
def test_get_milestone(mock_get, milestone):
    mock_response = MagicMock()
    mock_response.json.return_value = milestone

    mock_get.return_value = mock_response

    result = get_milestone("id", "auth")

    assert result is not None

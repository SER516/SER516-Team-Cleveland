from unittest.mock import patch
from requests.exceptions import HTTPError

from ..project.getProjectBySlug \
    import get_project_by_slug


@patch('requests.get')
def test_get_project_by_slug_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"name": "Sample Project",
                                       "slug": "sample-project"}

    project_info = get_project_by_slug("sample-project", "fake-token")

    assert project_info is not None
    assert project_info["name"] == "Sample Project"
    assert project_info["slug"] == "sample-project"


@patch('requests.get')
def test_get_project_by_slug_failure(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.side_effect = HTTPError()

    project_info = get_project_by_slug("nonexistent-project", "fake-token")

    assert project_info is None

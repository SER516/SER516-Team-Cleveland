import pytest

from unittest.mock import MagicMock, patch

from ..tasks.get_tasks import (
    get_tasks,
    get_closed_tasks,
    get_tasks_by_story_id,
    get_task_for_member
)


@pytest.fixture
def task():
    return [
        {
            "due_date": None,
            "due_date_reason": "",
            "due_date_status": "not_set",
            "total_comments": 0,
            "tags": [],
            "attachments": [],
            "project": 1521716,
            "project_extra_info": {
                "name": "SER516-Team-Cleveland",
                "slug": "ser516asu-ser516-team-cleveland",
                "logo_small_url": None,
                "id": 1521716
            },
            "status": 7600964,
            "status_extra_info": {
                "name": "In progress",
                "color": "#E47C40",
                "is_closed": False
            },
            "assigned_to": 618022,
            "assigned_to_extra_info": {
                "username": "AdvaitChirmule",
                "full_name_display": "Advait Chirmule",
                "photo": None,
                "big_photo": None,
                "gravatar_id": "5dafd57b749c0d2d00975cce81334152",
                "is_active": True,
                "id": 618022
            },
            "owner": 599211,
            "owner_extra_info": {
                "username": "sverma89",
                "full_name_display": "Shikha Verma",
                "photo": None,
                "big_photo": None,
                "gravatar_id": "d163ef3bd427c2473f561446d8397bca",
                "is_active": True,
                "id": 599211
            },
            "is_watcher": False,
            "total_watchers": 0,
            "is_voter": False,
            "total_voters": 0,
            "id": 5331122,
            "user_story": 5468188,
            "ref": 37,
            "milestone": 376615,
            "milestone_slug": "sprint1-1018",
            "created_at": "2021-01-20T16:03:15.369Z",
            "created_date": "2021-01-20T16:03:15.369Z",
            "modified_date": "2024-02-02T01:22:52.672Z",
            "finished_date": "2024-02-05T00:00:00Z",
            "subject": "FE Login Page",
            "us_order": 1706757804885,
            "taskboard_order": 0,
            "is_iocaine": False,
            "external_reference": None,
            "version": 4,
            "watchers": [],
            "is_blocked": False,
            "blocked_note": "",
            "is_closed": True,
            "username": "hmshahid",
            "full_name": "Hasan Shahid",
            "user_story_extra_info": {
                "id": 5468188,
                "ref": 12,
                "subject": "Select a Taiga project to apply it to",
                "epics": [
                    {
                        "id": 218050,
                        "ref": 3,
                        "subject": "Lead Time",
                        "color": "#D3AC50",
                        "project": {
                            "id": 1521716,
                            "name": "SER516-Team-Cleveland",
                            "slug": "ser516asu-ser516-team-cleveland"
                        }
                    }
                ]
            },
            "values_diff": {
                "status": [
                    "New",
                    "In progress"
                ],
                "taskboard_order": [
                    1610518445123,
                    1
                ]
            }
        }
    ]


@patch('requests.get')
def test_get_tasks(mock_get, task):
    mock_response = MagicMock()
    mock_response.json.return_value = task

    mock_get.return_value = mock_response

    result = get_tasks("sample", "auth")

    assert len(result) == 1


@patch('requests.get')
def test_closed_tasks(mock_get, task):
    mock_response = MagicMock()
    mock_response.json.return_value = task

    mock_get.return_value = mock_response

    result = get_closed_tasks("sample", "auth")

    assert len(result) == 1


@patch('requests.get')
def test_task_by_story_id(mock_get, task):
    mock_response = MagicMock()
    mock_response.json.return_value = task

    mock_get.return_value = mock_response

    result = get_tasks_by_story_id("storyId", "auth")

    assert len(result) == 1


@patch('requests.get')
def test_task_for_member(mock_get, task):
    mock_response = MagicMock()
    mock_response.json.return_value = task

    mock_get.return_value = mock_response

    result = get_task_for_member("sample", "member_id", "auth")

    assert len(result) == 1

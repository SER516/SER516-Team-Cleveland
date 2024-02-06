from unittest.mock import MagicMock, patch

import pytest

from taigaProject.src.taigaApi.task.getTaskHistory import get_task_history


# content of test_sample.py
@pytest.fixture
def tasks():
    return [{
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
    "created_date": "2024-02-01T03: 23: 24.914Z",
    "modified_date": "2024-02-02T01: 22: 52.672Z",
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
    "is_closed": False,
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
    }
}]

@pytest.fixture
def task_details():
    return [
        {'id': '819e8332-c169-11ee-b0eb-e398cbe6c1dc',
                'user': {'pk': 599211, 'username': 'sverma89', 'name': 'Shikha Verma', 'photo': None, 'is_active': True,
                         'gravatar_id': 'd163ef3bd427c2473f561446d8397bca'}, 'created_at': '2024-02-02T01:22:18.544Z',
                'type': 1, 'key': 'tasks.task:5331138',
                'diff': {'status': [7600963, 7600964], 'taskboard_order': [1706758347617, 3]}, 'snapshot': None,
                'values': {'users': {}, 'status': {'7600963': 'New', '7600964': 'In progress'}},
                'values_diff': {'status': ['New', 'In progress'], 'taskboard_order': [1706758347617, 3]}, 'comment': '',
                'comment_html': '', 'delete_comment_date': None, 'delete_comment_user': None, 'edit_comment_date': None,
                'is_hidden': False, 'is_snapshot': False}
    ]

@pytest.fixture
def auth_token():
    return "random_auth"

@patch('os.getenv', MagicMock(return_value='http://fake.taiga.url'))
@patch('requests.get')
def test_get_task_history(mock_get, tasks, auth_token, task_details):
    mock_response = MagicMock()
    mock_response.json.return_value = task_details

    mock_get.return_value = mock_response

    cycle_time, closed_tasks = get_task_history(tasks, auth_token)

    assert cycle_time == 2  # Example cycle time for this test case
    assert closed_tasks == 1  # Both tasks are closed

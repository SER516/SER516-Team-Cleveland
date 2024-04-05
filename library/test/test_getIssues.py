from unittest.mock import MagicMock, patch

import pytest
from datetime import date

from ..issues.get_issues import get_issues


# content of test_sample.py
@pytest.fixture
def issues():
    null = None
    true = True
    false = False
    return [
        {
            "tags": [],
            "due_date": null,
            "due_date_reason": "",
            "due_date_status": "not_set",
            "attachments": [],
            "project": 1521716,
            "project_extra_info": {
                "name": "SER516-Team-Cleveland",
                "slug": "ser516asu-ser516-team-cleveland",
                "logo_small_url": null,
                "id": 1521716
            },
            "status": 10655866,
            "status_extra_info": {
                "name": "Done",
                "color": "#A8E440",
                "is_closed": true
            },
            "assigned_to": 600238,
            "assigned_to_extra_info": {
                "username": "1229969197",
                "full_name_display": "Ashutosh Chaurasia",
                "photo": null,
                "big_photo": null,
                "gravatar_id": "be73b2b6075871e31a7f36d68339bfcf",
                "is_active": true,
                "id": 600238
            },
            "owner": 600238,
            "owner_extra_info": {
                "username": "1229969197",
                "full_name_display": "Ashutosh Chaurasia",
                "photo": null,
                "big_photo": null,
                "gravatar_id": "be73b2b6075871e31a7f36d68339bfcf",
                "is_active": true,
                "id": 600238
            },
            "is_watcher": false,
            "total_watchers": 0,
            "is_voter": false,
            "total_voters": 0,
            "id": 1728129,
            "ref": 101,
            "severity": 7606175,
            "priority": 4568159,
            "type": 4574904,
            "milestone": 376617,
            "created_date": "2024-02-26T02:20:36.552Z",
            "modified_date": "2024-02-27T05:59:37.403Z",
            "finished_date": "2024-02-27T05:59:37.407Z",
            "subject": "Change UI to hide Charts when Dev Focus is selected",
            "external_reference": null,
            "version": 2,
            "watchers": [],
            "is_blocked": false,
            "blocked_note": "",
            "is_closed": true
        },
        {
            "tags": [],
            "due_date": null,
            "due_date_reason": "",
            "due_date_status": "not_set",
            "attachments": [],
            "project": 1521716,
            "project_extra_info": {
                "name": "SER516-Team-Cleveland",
                "slug": "ser516asu-ser516-team-cleveland",
                "logo_small_url": null,
                "id": 1521716
            },
            "status": 10655866,
            "status_extra_info": {
                "name": "Done",
                "color": "#A8E440",
                "is_closed": true
            },
            "assigned_to": 618022,
            "assigned_to_extra_info": {
                "username": "AdvaitChirmule",
                "full_name_display": "Advait Chirmule",
                "photo": null,
                "big_photo": null,
                "gravatar_id": "5dafd57b749c0d2d00975cce81334152",
                "is_active": true,
                "id": 618022
            },
            "owner": 600485,
            "owner_extra_info": {
                "username": "hmshahid",
                "full_name_display": "Hasan Shahid",
                "photo": """https://media-protected.taiga.io/user/0/9/7/d/
                c589eb31c0d982a06f0ae045e9573c5eb95d773578a9d54892705ae83119/
                diamonds.png.80x80_q85_crop.png?token=Zd40Hw%3AB_aAhnvNzZU33
                -XRYfLpclJ321TvHkPAvUiye3oK3qLbS5dL8mWQcG5AZwRLQcuu5
                sGvcYDeBtOGp3vYJ-Zt8w""",
                "big_photo": """https://media-protected.taiga.io/user/
                0/9/7/d/c589eb31c0d982a06f0ae045e9573c5eb95d773578a9d
                54892705ae83119/diamonds.png.300x300_q85_crop.png
                ?token=Zd40Hw%3AyBKLK0_xcz18Es_ZIvRkX0oET8dlgIUQ
                8Wz3w5xVERi9_vvJVCECWxx8SUOBXUCD4bu1_CT-1pJP6Dw7Jkwieg""",
                "gravatar_id": "561c63d156183c4e711f7885c0a4b4e6",
                "is_active": true,
                "id": 600485
            },
            "is_watcher": false,
            "total_watchers": 0,
            "is_voter": false,
            "total_voters": 0,
            "id": 1724585,
            "ref": 72,
            "severity": 7606175,
            "priority": 4568159,
            "type": 4574904,
            "milestone": 376617,
            "created_date": "2024-02-19T22:41:45.415Z",
            "modified_date": "2024-02-23T19:44:39.813Z",
            "finished_date": "2024-02-23T19:44:39.816Z",
            "subject": """Show Task Id and User Story Id on
            hover for Lead Time and Cycle Time""",
            "external_reference": null,
            "version": 5,
            "watchers": [],
            "is_blocked": false,
            "blocked_note": "",
            "is_closed": true
        },
        {
            "tags": [],
            "due_date": null,
            "due_date_reason": "",
            "due_date_status": "not_set",
            "attachments": [],
            "project": 1521716,
            "project_extra_info": {
                "name": "SER516-Team-Cleveland",
                "slug": "ser516asu-ser516-team-cleveland",
                "logo_small_url": null,
                "id": 1521716
            },
            "status": 10655866,
            "status_extra_info": {
                "name": "Done",
                "color": "#A8E440",
                "is_closed": true
            },
            "assigned_to": 618022,
            "assigned_to_extra_info": {
                "username": "AdvaitChirmule",
                "full_name_display": "Advait Chirmule",
                "photo": null,
                "big_photo": null,
                "gravatar_id": "5dafd57b749c0d2d00975cce81334152",
                "is_active": true,
                "id": 618022
            },
            "owner": 600485,
            "owner_extra_info": {
                "username": "hmshahid",
                "full_name_display": "Hasan Shahid",
                "photo": """https://media-protected.taiga.io/user/0/9/7/d/
                c589eb31c0d982a06f0ae045e9573c5eb95d773578a9d54892705ae83119/
                diamonds.png.80x80_q85_crop.png?token=Zd40Hw%3AB_aAhnvNzZU
                33-XRYfLpclJ321TvHkPAvUiye3oK3qLbS5dL8mWQcG5AZwRL
                Qcuu5sGvcYDeBtOGp3vYJ-Zt8w""",
                "big_photo": """https://media-protected.taiga.io/user/
                0/9/7/d/c589eb31c0d982a06f0ae045e9573c5eb95d773578a9d54892
                705ae83119/diamonds.png.300x300_q85_crop.png?token=Zd40Hw
                %3AyBKLK0_xcz18Es_ZIvRkX0oET8dlgIUQ8Wz3w5xVERi9_vvJVC
                ECWxx8SUOBXUCD4bu1_CT-1pJP6Dw7Jkwieg""",
                "gravatar_id": "561c63d156183c4e711f7885c0a4b4e6",
                "is_active": true,
                "id": 600485
            },
            "is_watcher": false,
            "total_watchers": 0,
            "is_voter": false,
            "total_voters": 0,
            "id": 1724584,
            "ref": 71,
            "severity": 7606175,
            "priority": 4568159,
            "type": 4574904,
            "milestone": 376617,
            "created_date": "2024-02-19T22:38:52.911Z",
            "modified_date": "2024-02-25T04:58:49.716Z",
            "finished_date": "2024-02-25T04:58:49.720Z",
            "subject": "Make average visible on Lead and Cycle Time charts",
            "external_reference": null,
            "version": 5,
            "watchers": [],
            "is_blocked": false,
            "blocked_note": "",
            "is_closed": true
        }
    ]


@pytest.fixture
def auth_token():
    return "random_auth"


@patch('os.getenv', MagicMock(return_value='https://fake.taiga.url'))
@patch('requests.get')
def test_get_task_history(mock_get, issues, auth_token):
    mock_response = MagicMock()
    mock_response.json.return_value = issues

    mock_get.return_value = mock_response

    result = get_issues(
        "1521716",
        date.fromisoformat("2024-02-22"),
        date.fromisoformat("2024-02-26"),
        auth_token
    )
    expected_result = {
        'issues': [
            {
                'id': 1724585,
                'created_date': '2024-02-19T22:41:45.415Z',
                'finished_date': '2024-02-23T19:44:39.816Z'
            },
            {
                'id': 1724584,
                'created_date': '2024-02-19T22:38:52.911Z',
                'finished_date': '2024-02-25T04:58:49.720Z'
            }
        ],
        'avg_fix_time': 4.0
    }
    assert result == expected_result

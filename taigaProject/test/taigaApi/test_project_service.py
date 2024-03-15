from taigaProject.src.taigaApi.util.project_service import get_project_members


def test_empty_members_list():
    project_details = {
        "members": []
    }
    members = get_project_members(project_details)

    assert not members


def test_members_list():
    project_details = {
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

    members = get_project_members(project_details)

    assert members
    assert len(members) == 2

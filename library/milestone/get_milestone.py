import requests


def get_milestone(milstone_id, auth_token):
    taiga_url = "https://api.taiga.io/api/v1"

    milestone_api_url = f"{taiga_url}/milestones/{milstone_id}"

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:
        response = requests.get(milestone_api_url, headers=headers)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print("Error fetching Milestone", e)
        return None

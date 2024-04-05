import requests


def get_business_value(user_story_id, attribute_key, auth_token):
    taiga_url = "https://api.taiga.io/api/v1"

    business_value_api_url = (
        f"{taiga_url}/userstories/custom-attributes-values/{user_story_id}"
    )

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(business_value_api_url, headers=headers)

        response.raise_for_status()

        attribute_values = response.json().get('attributes_values', {})
        if attribute_key in attribute_values:
            return attribute_values.get(attribute_key)
        else:
            return 0

    except requests.exceptions.RequestException:
        print("Error fetching Business Value")
        return None

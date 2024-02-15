import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_business_value(user_story_id, attribute_key, auth_token):
    taiga_url = os.getenv('TAIGA_URL')
    
    business_value_api_url = f"{taiga_url}/userstories/custom-attributes-values/{user_story_id}"
    
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(business_value_api_url, headers=headers)

        response.raise_for_status()

        business_value = response.json().get('attributes_values', {})

        return business_value.get(str(attribute_key))
    
    except requests.exceptions.RequestException as e:
        print("Error fetching Business Value")
        return None
    
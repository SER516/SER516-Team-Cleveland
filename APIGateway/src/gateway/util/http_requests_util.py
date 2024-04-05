from http.client import HTTPException

import requests

def post_call(url, token, json_object, api_path):
    header = {"token": token}
    try:
        response = requests.post(f"{url}/{api_path}",
                                 data=json_object.toJSON(), headers=header)
        response.raise_for_status()
        return response.json()

    except (HTTPException, requests.exceptions.RequestException) as e:
        print(f"Authentication failed: {e}")
        raise e
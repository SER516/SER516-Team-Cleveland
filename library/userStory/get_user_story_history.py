import os

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Function to retrieve user stories for a specific project from the Taiga API
def get_user_story(project_id, auth_token):

    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')
    # Construct the URL for the user stories API endpoint
    # for the specified project
    user_story_api_url = f"{taiga_url}/userstories?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:

        # Make a GET request to Taiga API to retrieve user stories
        response = requests.get(user_story_api_url, headers=headers)
        # Raise an exception for HTTP errors (4xx or 5xx)
        response.raise_for_status()

        # Extract and return the user stories information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.RequestException as e:

        # Handle errors during the API request and print an error message
        print(f"Error fetching stories by slug: {e}")
        return None


# Method to return the details for closed user stories
def get_closed_user_stories(project_id, auth_token):

    user_stories = get_user_story(project_id, auth_token)
    if user_stories:

        closed_user_stories = [
            {
                "id": user_story["id"],
                "subject": user_story["subject"],
                "created_date": user_story["created_date"],
                "finished_date": user_story["finish_date"],
                "ref": user_story["ref"],
                "sprintURL": user_story["project_extra_info"]["slug"],
                "story_points": user_story["total_points"]
            }
            for user_story in user_stories if user_story.get("is_closed")
        ]

        return closed_user_stories
    else:
        return []


def get_user_story_details_by_id(
    story,
    headers,
    taiga_url
):
    task_history_url = f"{taiga_url}/history/userstory/{story['id']}"
    return requests.get(task_history_url, headers=headers)

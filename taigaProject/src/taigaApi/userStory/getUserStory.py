import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()


# Function to retrieve user stories for a specific project from the Taiga API
def get_user_story(project_id, auth_token):

    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')
    # Construct the URL for the user stories API endpoint for the specified project
    user_story_api_url = f"{taiga_url}/userstories?project={project_id}"

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:

        # Make a GET request to Taiga API to retrieve user stories
        response = requests.get(user_story_api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Extract and return the user stories information from the response
        project_info = response.json()
        return project_info

    except requests.exceptions.RequestException as e:

        # Handle errors during the API request and print an error message
        print(f"Error fetching stories by slug: {e}")
        return None

#Method to return the details for closed user stories
def get_closed_user_stories(project_id, auth_token):

    user_stories = get_user_story(project_id, auth_token)
    if user_stories:

        closed_user_stories = [
            {
                "id": user_story["id"],
                "subject": user_story["subject"],
                "created_date": user_story["created_date"],
                "finished_date": user_story["finish_date"]
            }
            for user_story in user_stories if user_story.get("is_closed")
        ]

        return closed_user_stories
    else:
        return []


def get_us_lead_time(project_id, auth_token):
    user_stories = get_closed_user_stories(project_id, auth_token)
    lead_time = 0
    closed_user_stories = 0
    lead_times = []
    for user_story in user_stories:
        created_date = datetime.fromisoformat(user_story["created_date"])
        finished_date = datetime.fromisoformat(user_story['finished_date'])
        lead_time += (finished_date - created_date).days
        lead_times.append({
            "taskId": user_story["id"],
            "startTime": user_story["created_date"],
            "endTime": user_story['finished_date'],
            "timeTaken": lead_time
        })
        closed_user_stories += 1
    if closed_user_stories == 0:
        return lead_times, 0
    avg_lead_time = round((lead_time / closed_user_stories), 2)
    return lead_times, avg_lead_time

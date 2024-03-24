import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()


# Function to retrieve issues for a specific project from the Taiga API
def get_closed_issues_by_project(project_id, auth_token):
    # Get Taiga API URL from environment variables
    taiga_url = os.getenv('TAIGA_URL')

    # Construct the URL for the tasks API endpoint for the specified project
    task_api_url = f"""
        {taiga_url}/issues?project={project_id}&status__is_closed=true"""

    # Define headers including the authorization token and content type
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        "x-disable-pagination": "True"
    }

    try:

        # Make a GET request to Taiga API to retrieve tasks
        response = requests.get(task_api_url, headers=headers)
        # Raise an exception for HTTP errors (4xx or 5xx)
        response.raise_for_status()

        # return the issues information from the response
        issues = response.json()
        return issues

    except requests.exceptions.RequestException as e:

        # Handle errors during the API request and print an error message
        print(f"Error fetching tasks: {e}")
        return None


# Function to retrieve closed issues for a specific project
# and date range from the Taiga API
def get_issues(project_id, from_date, to_date, auth_token):

    issues = get_closed_issues_by_project(project_id, auth_token)
    final_issues = []
    total_time = 0
    if issues and len(issues) > 0:
        for issue in issues:
            created_date = datetime.fromisoformat(issue["created_date"])
            finished_date = datetime.fromisoformat(issue['finished_date'])
            if from_date <= finished_date.date() <= to_date:
                print(issue["id"])
                final_issues.append({
                    "id": issue["id"],
                    "created_date": issue["created_date"],
                    "finished_date": issue['finished_date']
                })
                total_time += (finished_date - created_date).days
        if len(final_issues) > 0:
            total_time /= len(final_issues)
    return {
        "issues": final_issues,
        "avg_fix_time": total_time
    }

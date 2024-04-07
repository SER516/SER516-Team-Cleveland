import os
from concurrent.futures import ThreadPoolExecutor

import requests
from dotenv import load_dotenv
from datetime import datetime, date

from userStory.getBusinessValue import get_business_value
from userStory.get_user_story_history import get_user_story


def get_zero_business_value_user_stories(
    project_id,
    start_range,
    end_range,
    attribute_key,
    auth_token
):
    user_stories = get_zero_bv_us(
        project_id,
        start_range,
        end_range,
        auth_token
    )
    zero_bv_user_stories = []
    total_story_points = 0
    zero_bv_story_points = 0
    for user_story in user_stories:
        if user_story["story_points"] is None:
            continue
        total_story_points += int(user_story["story_points"])
        business_value = get_business_value(
            user_story["id"],
            attribute_key,
            auth_token
        )
        if business_value == "0":
            zero_bv_story_points += int(user_story["story_points"])
            zero_bv_user_stories.append(user_story)

    cruft_details = {"zero_bv_user_stories": zero_bv_user_stories,
                     "total_user_stories": len(user_stories),
                     "total_zero_bv_user_stories": len(zero_bv_user_stories),
                     "total_story_points": total_story_points,
                     "total_zero_bv_story_points": zero_bv_story_points}

    return cruft_details


def get_zero_bv_us(
    project_id,
    start_range,
    end_range,
    auth_token
):
    user_stories = get_closed_user_stories(project_id, auth_token)
    user_stories_in_range = []
    start_range_date = datetime.strptime(start_range, '%Y-%m-%d')
    start_range_date = start_range_date.date()
    end_range_date = datetime.strptime(end_range, "%Y-%m-%d")
    end_range_date = end_range_date.date()
    for user_story in user_stories:
        endTime = datetime.fromisoformat(user_story["finished_date"]).date()
        if endTime >= start_range_date and endTime <= end_range_date:
            user_stories_in_range.append(user_story)

    return user_stories_in_range


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

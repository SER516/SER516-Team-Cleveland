from datetime import datetime, timedelta

from ..task.getTaskHistory import get_task_lead_time, get_task_cycle_time
from ..userStory.getUserStory import get_us_lead_time, get_us_cycle_time
from ..milestone.get_milestone import get_milestone
from ..task.getTasks import get_tasks_by_story_id


def get_lead_time_details(project_details, auth_token):
    us_lead_time, avg_us_lt = get_us_lead_time(project_details["id"], auth_token)
    task_lead_time, avg_task_lt = get_task_lead_time(project_details["id"], auth_token)
    
    us_lead_time.sort(key=lambda l: l["endDate"])
    task_lead_time.sort(key=lambda l: l["endDate"])

    #get objects created that store the details for task and user story lead times
    task_lead_time = get_lead_time_object("task", task_lead_time, avg_task_lt)
    us_lead_time = get_lead_time_object("userStory", us_lead_time, avg_us_lt)

    lead_time = {
        "storiesLeadTime": us_lead_time,
        "tasksLeadTime": task_lead_time
    }
    return metric_object("LEAD", "leadTime", lead_time, project_details)

def get_lead_time_object(object_type, task_lead_time, avg_task_lt):
    return {
        object_type: task_lead_time,
        "avgLeadTime": avg_task_lt
    }

def metric_object(metric, time_key, lead_time, project_details):
    return {
        "metric": metric,
        time_key: lead_time,
        "projectInfo": {
            "name": project_details["name"],
            "members": project_details["members"]
        }
    }

def get_cycle_time_details(project_details, auth_token):
    task_cycle_time, avg_task_ct = get_task_cycle_time(project_details["id"], auth_token)
    us_cycle_time, avg_us_ct = get_us_cycle_time(project_details["id"], auth_token)
    
    task_cycle_time.sort(key=lambda l: l["endDate"])
    us_cycle_time.sort(key=lambda l: l["endDate"])
    
    task_cycle_time = get_cycle_time_object("task", task_cycle_time, avg_task_ct)
    us_cycle_time = get_cycle_time_object("story", us_cycle_time, avg_us_ct)
    
    cycle_time = {
        "taskCycleTime": task_cycle_time,
        "storyCycleTime": us_cycle_time
    }
    return metric_object("CYCLE", "cycleTime", cycle_time, project_details)


def get_cycle_time_object(object_type, cycle_time, avg_lt):
    return {
        object_type: cycle_time,
        "avgCycleTime": avg_lt
    }


def get_burndown_chart_metric_detail(milestone_id, auth_token):
    milestone = get_milestone(milestone_id, auth_token)
    
    partial_burndown, expected_partial_burndown = calc_partial_story_points(auth_token, milestone)
    partial_burndown = list(partial_burndown.values())
    partial_burndown.sort(key=lambda l: l["date"])
    
    return {
        "partial_burndown": {
            "partial_burndown_data": partial_burndown,
            "expected_partial_burndown": expected_partial_burndown
        }
    }

def calc_partial_story_points(auth_token, milestone):
    days_data = {}
    milestone_start = datetime.fromisoformat(milestone["estimated_start"]).date()
    milestone_finish = datetime.fromisoformat(milestone["estimated_finish"]).date()
    
    days_data[milestone_start] = append_partial_date_data(milestone_start, 0, milestone["total_points"])
    
    for user_story in milestone["user_stories"]:
        tasks = get_tasks_by_story_id(user_story["id"], auth_token)
        extract_partial_burndown_data(user_story, tasks, days_data)
    
    update_partial_days_data(days_data, milestone_start, milestone_finish)
    
    expected_data = get_expected_data(milestone["total_points"], milestone_start, milestone_finish)

    return days_data, expected_data

def update_partial_days_data(days_data, milestone_start, milestone_finish):
    for dt in daterange(milestone_start + timedelta(1), milestone_finish + timedelta(1)):
        if dt not in days_data:
            days_data[dt] = append_partial_date_data(datetime.fromisoformat(str(dt)).date(), 0, days_data[dt - timedelta(1)]["remaining"])
        else:
            days_data[dt]["remaining"] = round(days_data[dt - timedelta(1)]["remaining"] - days_data[dt]["completed"], 2)

def get_expected_data(total_points, milestone_start, milestone_finish):
    return [
        {
            "date": milestone_start,
            "remaining": total_points
        },
        {
            "date": milestone_finish,
            "remaining": 0
        }
    ]

def extract_partial_burndown_data(user_story, tasks, days_data):
    for task in tasks:
        if task["is_closed"]:
            finished_date = datetime.fromisoformat(task["finished_date"]).date()
            partial_story_points = round(user_story["total_points"]/len(tasks), 2)
            
            if finished_date in days_data:
                days_data[finished_date]["completed"] = days_data[finished_date]["completed"] + partial_story_points
            else:
                days_data[finished_date] = append_partial_date_data(finished_date, partial_story_points, 0)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def append_partial_date_data(date, completed_story_points, remaining_story_points):
    return {
        "date": date,
        "completed": completed_story_points,
        "remaining": remaining_story_points
    }

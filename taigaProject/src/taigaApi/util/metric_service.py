from datetime import datetime, timedelta

from ..task.get_task_history import get_task_lead_time, get_task_cycle_time
from ..userStory.get_user_story_history import get_us_lead_time, get_us_cycle_time
from ..milestone.get_milestone import get_milestone
from ..task.getTasks import get_tasks_by_story_id
from ..userStory.getBusinessValue import get_business_value

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


def get_burndown_chart_metric_detail(milestone_id, attribute_key, auth_token):
    milestone = get_milestone(milestone_id, auth_token)
    
    partial_burndown, bv_burndown, total_burndown = calc_burndown_day_data(auth_token, milestone, attribute_key)
    partial_burndown = list(partial_burndown.values())
    partial_burndown.sort(key=lambda l: l["date"])
    bv_burndown = list(bv_burndown.values())
    bv_burndown.sort(key=lambda l: l["date"])
    total_burndown = list(total_burndown.values())
    total_burndown.sort(key=lambda l: l["date"])
    
    return {
        "partial_burndown": {
            "partial_burndown_data": partial_burndown,
        },
        "bv_burndown": {
            "bv_burndown_data": bv_burndown
        },
        "total_burndown": {
            "total_burndown_data": total_burndown
        }
    }

def calc_burndown_day_data(auth_token, milestone, attribute_key):
    days_data = {}
    days_bv_data = {}
    days_total_data = {}
    start = datetime.fromisoformat(milestone["estimated_start"])
    finish = datetime.fromisoformat(milestone["estimated_finish"])
    milestone_start = start.date()
    milestone_finish = finish.date()
    
    days_data[milestone_start] = append_points_date_data(milestone_start, 0, milestone["total_points"])
    days_data[milestone_start]["expected_remaining"] = milestone["total_points"]
    
    days_total_data[milestone_start] = append_points_date_data(milestone_start, 0, milestone["total_points"])
    days_total_data[milestone_start]["expected_remaining"] = milestone["total_points"]
    
    days_bv_data[milestone_start] = {
        "date": milestone_start,
        "completed": 0
    }
    
    total_business_value = 0
    for user_story in milestone["user_stories"]:
        tasks = get_tasks_by_story_id(user_story["id"], auth_token)
        extract_partial_burndown_data(user_story, tasks, days_data)
        
        business_value = get_business_value(user_story["id"], attribute_key, auth_token)
        total_business_value = total_business_value + int(business_value)
        extract_bv_burndown_data(user_story, int(business_value), days_bv_data)
        
        extract_total_burndown_data(user_story, days_total_data)
    
    expected_decrement = round(milestone["total_points"]/(finish - start).days, 2)
    update_points_days_data(days_data, milestone_start, milestone_finish, expected_decrement)
    update_points_days_data(days_total_data, milestone_start, milestone_finish, expected_decrement)
    
    days_bv_data[milestone_start]["remaining"] = total_business_value
    days_bv_data[milestone_start]["expected_remaining"] = total_business_value
    expected_bv_decrement = round((total_business_value)/(finish - start).days, 2)
    update_bv_days_data(days_bv_data, milestone_start, milestone_finish, expected_bv_decrement)

    return days_data, days_bv_data, days_total_data

def update_points_days_data(days_data, milestone_start, milestone_finish, expected_decrement):
    for dt in daterange(milestone_start + timedelta(1), milestone_finish + timedelta(1)):
        if dt not in days_data:
            days_data[dt] = append_points_date_data(datetime.fromisoformat(str(dt)).date(), 0, days_data[dt - timedelta(1)]["remaining"])
        else:
            days_data[dt]["remaining"] = round(days_data[dt - timedelta(1)]["remaining"] - days_data[dt]["completed"], 2)
        days_data[dt]["expected_remaining"] = round(days_data[dt - timedelta(1)]["expected_remaining"] - expected_decrement, 2)
        
def update_bv_days_data(days_bv_data, milestone_start, milestone_finish, expected_bv_decrement):
    for dt in daterange(milestone_start + timedelta(1), milestone_finish + timedelta(1)):
        if dt not in days_bv_data:
            days_bv_data[dt] = {
                "date": datetime.fromisoformat(str(dt)).date(),
                "completed": 0,
                "remaining": days_bv_data[dt - timedelta(1)]["remaining"]
            }
        else:
            days_bv_data[dt]["remaining"] = round(days_bv_data[dt - timedelta(1)]["remaining"] - days_bv_data[dt]["completed"], 2)
        days_bv_data[dt]["expected_remaining"] = round(days_bv_data[dt - timedelta(1)]["expected_remaining"] - expected_bv_decrement, 2)

def extract_partial_burndown_data(user_story, tasks, days_data):
    for task in tasks:
        if task["is_closed"]:
            finished_date = datetime.fromisoformat(task["finished_date"]).date()
            partial_story_points = round(user_story["total_points"]/len(tasks), 2)
            
            if finished_date in days_data:
                days_data[finished_date]["completed"] = days_data[finished_date]["completed"] + partial_story_points
            else:
                days_data[finished_date] = append_points_date_data(finished_date, partial_story_points, 0)

def extract_bv_burndown_data(user_story, business_value, days_bv_data):
    if user_story["is_closed"]:
        finished_date = datetime.fromisoformat(user_story["finish_date"]).date()
        if finished_date in days_bv_data:
            days_bv_data[finished_date]["completed"] = days_bv_data[finished_date]["completed"] + business_value
        else:
            days_bv_data[finished_date] = {
                "date": finished_date,
                "completed": business_value,
                "remainging": 0
            }

def extract_total_burndown_data(user_story, days_total_data):
    if user_story["is_closed"]:
        finished_date = datetime.fromisoformat(user_story["finish_date"]).date()
        if finished_date in days_total_data:
            days_total_data[finished_date]["completed"] = days_total_data[finished_date]["completed"] + user_story["total_points"]
        else:
            days_total_data[finished_date] = append_points_date_data(finished_date, user_story["total_points"], 0)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def append_points_date_data(date, completed_story_points, remaining_story_points):
    return {
        "date": date,
        "completed": completed_story_points,
        "remaining": remaining_story_points
    }

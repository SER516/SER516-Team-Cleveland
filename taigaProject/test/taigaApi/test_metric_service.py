import pytest

from taigaProject.src.taigaApi.util.metric_service import metric_object, get_lead_time_object, get_cycle_time_object, append_partial_date_data, get_expected_data

def test_metric_object():
    sample_object = metric_object("LEAD", "leadTime", 1, {"name": "project", "members": []})
    
    assert sample_object
    assert sample_object["metric"] and sample_object["metric"] == "LEAD"
    assert "leadTime" in sample_object
    assert sample_object["leadTime"] == 1

def test_lead_time_object():
    lead_time = get_lead_time_object("task", 2, 1.1)
    
    assert lead_time
    assert "task" in lead_time and lead_time["task"] == 2
    assert lead_time["avgLeadTime"] == 1.1
    
def test_cycle_time_object():
    lead_time = get_cycle_time_object("story", 4, 2)
    
    assert lead_time
    assert "story" in lead_time and lead_time["story"] == 4
    assert lead_time["avgCycleTime"] == 2

def test_append_partial_date_data():
    partial_date_data = append_partial_date_data("2024-02-14", 5, 15)
    
    assert "date" in partial_date_data and partial_date_data["date"] == "2024-02-14"
    assert "completed" in partial_date_data and partial_date_data["completed"] == 5
    assert "remaining" in partial_date_data and partial_date_data["remaining"] == 15

def test_expected_data():
    partial_expected_data = get_expected_data(10, "2024-01-29", "2024-02-17")
    
    assert len(partial_expected_data) == 2
    assert "date" in partial_expected_data[0] and partial_expected_data[0]["date"] == "2024-01-29"
    assert "remaining" in partial_expected_data[0] and partial_expected_data[0]["remaining"] == 10
    
    assert "date" in partial_expected_data[1] and partial_expected_data[1]["date"] == "2024-02-17"
    assert "remaining" in partial_expected_data[1] and partial_expected_data[1]["remaining"] == 0

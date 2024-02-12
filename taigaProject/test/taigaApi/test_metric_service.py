import pytest

from taigaProject.src.taigaApi.util.metric_service import metric_object, get_lead_time_object, get_cycle_time_object

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

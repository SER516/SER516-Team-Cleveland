def get_sprints_and_custom_fields_for_project(project_details):
    custom_attributes = []
    if project_details["userstory_custom_attributes"]:
        for custom_attribute in project_details["userstory_custom_attributes"]:
            custom_attributes.append({"id": custom_attribute["id"],
                                      "name": custom_attribute["name"]})
    sprints = []
    for sprint in project_details["milestones"]:
        sprints.append({"id": sprint["id"], "name": sprint["name"],
                        "slug": sprint["slug"]})

    sprint_details = {
        "name": project_details["name"],
        "sprints": sprints,
        "custom_attributes": custom_attributes,
        "id": str(project_details["id"])
    }
    return sprint_details

def get_project_members(project_details):
    members = []
    for member in project_details["members"]:
        members.append({
            "name": member["full_name"],
            "username": member["username"],
            "id": member["id"]
        })

    return members

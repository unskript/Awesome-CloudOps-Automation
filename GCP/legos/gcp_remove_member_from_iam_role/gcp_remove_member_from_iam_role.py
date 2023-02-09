##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import List,Any, Dict
import googleapiclient.discovery


class InputSchema(BaseModel):
    project_id: str = Field(
        title = "Project ID",
        description = "Name of the project e.g unskript-dev"
    )
    role: str = Field(
        title = "Role Name",
        description = "Role name from which member needs to remove e.g iam.serviceAccountUser"
    )
    member_email: str = Field(
        title = "Member Email",
        description = "Member email which has GCP access e.g test@company.com"
    )
    version: int = Field(
        title = "Requested Policy Version",
        description = "Requested Policy Version"
    )

def gcp_remove_member_from_iam_role_printer(output):
    if output is None:
        return
    pprint(output)

def gcp_remove_member_from_iam_role(handle, project_id: str, role: str, member_email:str, version:int = 1) -> Dict:
    """gcp_remove_member_from_iam_role Returns a Dict of new policy details

        :type project_id: string
        :param project_id: Name of the project

        :type role: string
        :param role: Role name from which member needs to remove e.g iam.serviceAccountUser

        :type member_email: string
        :param member_email: Member email which has GCP access e.g test@company.com

        :type version: int
        :param version: Requested Policy Version

        :rtype: Dict of new policy details
    """
    service = googleapiclient.discovery.build(
        "cloudresourcemanager", "v1", credentials=handle)

    result = {}
    try:
        member = "user:" + member_email
        if "gserviceaccount" in member_email:
            member = "serviceAccount:" + member_email
        get_policy = (
            service.projects().getIamPolicy(
                    resource=project_id,
                    body={"options": {"requestedPolicyVersion": version}}).execute())

        get_role = "roles/" + role
        binding = next(b for b in get_policy["bindings"] if b["role"] == get_role)
        if "members" in binding and member in binding["members"]:
            binding["members"].remove(member)

        remove_member = (
            service.projects()
            .setIamPolicy(resource=project_id, body={"policy": get_policy}).execute())
        result = remove_member

    except Exception as error:
        result = {"error": error}

    return result

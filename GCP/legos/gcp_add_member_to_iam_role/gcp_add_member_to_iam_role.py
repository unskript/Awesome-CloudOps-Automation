##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import List,Any, Dict
from googleapiclient import discovery


class InputSchema(BaseModel):
    project_id: str = Field(
        title = "Project ID",
        description = "Name of the project e.g unskript-dev"
    )
    role: str = Field(
        title = "Role Name",
        description = "Permission name assign to member e.g iam.serviceAccountUser"
    )
    member_email: str = Field(
        title = "Member Email",
        description = "Member email which has GCP access e.g test@company.com"
    )
    version: int = Field(
        title = "Requested Policy Version",
        description = "Requested Policy Version"
    )

def gcp_add_member_to_iam_role_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def gcp_add_member_to_iam_role(handle, project_id: str, role: str, member_email:str, version:int = 1) -> Dict:
    """gcp_add_member_to_iam_role Returns a Dict of policy details

        :type project_id: string
        :param project_id: Name of the project

        :type role: string
        :param role: Permission name assign to member e.g iam.serviceAccountUser

        :type member_email: string
        :param member_email: Member email which has GCP access e.g test@company.com

        :type version: int
        :param version: Requested Policy Version

        :rtype: Dict of policy details
    """
    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=handle)

    result = {}
    try:
        get_policy = (
            service.projects().getIamPolicy(
                    resource=project_id,
                    body={"options": {"requestedPolicyVersion": version}}).execute())

        member = "user:" + member_email
        if "gserviceaccount" in member_email:
            member = "serviceAccount:" + member_email

        binding = None
        get_role = "roles/" + role
        for b in get_policy["bindings"]:
            if b["role"] == get_role:
                binding = b
                break
        if binding is not None:
            binding["members"].append(member)
        else:
            binding = {"role": get_role, "members": [member]}
            get_policy["bindings"].append(binding)

        add_member = (
            service.projects()
            .setIamPolicy(resource=project_id, body={"policy": get_policy}).execute())

        result = add_member

    except Exception as error:
        result = {"error": error}

    return result
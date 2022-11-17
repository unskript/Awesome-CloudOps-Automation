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
        description = "Role name from which member needs to remove e.g iam.serviceAccountUser"
    )
    member_email: str = Field(
        title = "Member Email",
        description = "Member email which has GCP access e.g test@company.com"
    )
    sa_id: str = Field(
        title = "Service Account Email",
        description = "Service Account email id e.g test-user@unskript-dev.iam.gserviceaccount.com"
    )

def gcp_add_role_to_service_account_printer(output):
    if output is None:
        return
    pprint(output)

def gcp_add_role_to_service_account(handle, project_id: str, role: str, member_email:str, sa_id:str) -> Dict:
    """gcp_add_role_to_service_account Returns a Dict of new policy details

        :type project_id: string
        :param project_id: Name of the project

        :type role: string
        :param role: Role name from which member needs to remove e.g iam.serviceAccountUser

        :type member_email: string
        :param member_email: Member email which has GCP access e.g test@company.com

        :type sa_id: int
        :param sa_id: Service Account email

        :rtype: Dict of new policy details
    """
    service = discovery.build('iam', 'v1', credentials=handle)
    result = {}
    try:
        resource = 'projects/{}/serviceAccounts/{}'.format(project_id, sa_id)
        request = service.projects().serviceAccounts().getIamPolicy(resource=resource)
        response = request.execute()

        member = "user:" + member_email
        if "gserviceaccount" in member_email:
            member = "serviceAccount:" + member_email
        get_role = "roles/" + role
        if "bindings" not in response:
            add_role = {'version': 1,
                 'bindings': [{'role': get_role,
                 'members': [member]}]}
            response = add_role
        else:
            add_role = {
                  "role": get_role,
                  "members": [member]}
            response["bindings"].append(add_role)
            
        set_policy = service.projects().serviceAccounts().setIamPolicy(resource=resource, body={"policy": response})
        policy_output = set_policy.execute()
        result = policy_output

    except Exception as error:
        result = {"error": error}

    return result
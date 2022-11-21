##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import Dict
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
    sa_id: str = Field(
        title = "Service Account Email",
        description = "Service Account email id e.g test-user@unskript-dev.iam.gserviceaccount.com"
    )

def gcp_remove_role_from_service_account_printer(output):
    if output is None:
        return
    pprint(output)


def gcp_remove_role_from_service_account(handle, project_id: str, role: str, sa_id:str) -> Dict:
    """gcp_remove_role_from_service_account Returns a Dict of new policy details

        :type project_id: string
        :param project_id: Name of the project

        :type role: string
        :param role: Role name from which member needs to remove e.g iam.serviceAccountUser

        :type sa_id: string
        :param sa_id: Service Account email

        :rtype: Dict of new policy details
    """
    service = discovery.build('iam', 'v1', credentials=handle)
    result = {}
    try:
        resource = 'projects/{}/serviceAccounts/{}'.format(project_id, sa_id)
        request = service.projects().serviceAccounts().getIamPolicy(resource=resource)
        get_policy = request.execute()

        get_role = "roles/"+role
        binding = next(b for b in get_policy["bindings"] if b["role"] == get_role)
        get_policy["bindings"].remove(binding)

        set_policy = service.projects().serviceAccounts().setIamPolicy(resource=resource, body={"policy": get_policy})
        policy_output = set_policy.execute()
        result = policy_output
    except Exception as error:
        result = {"error": error}

    return result
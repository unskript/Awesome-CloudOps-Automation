##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List
from google.cloud import compute_v1



from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    project: str = Field(..., description='GCP project ID', title='Project ID')


def gcp_get_unused_backend_services_printer(output):
    if output is None:
        return
    print(output)

def gcp_get_unused_backend_services(handle, project: str) -> List:
    """
    gcp_get_unused_backend_services Returns a list of unused backend services 
    and their target groups which have 0 instances in the given project.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type project: string
    :param project: Google Cloud Platform Project

    :return: Status, List of unused Backend services
    """
    backendClient = compute_v1.BackendServicesClient(credentials=handle)
    instanceClient = compute_v1.InstanceGroupsClient(credentials=handle)

    backend_services = [
        {
            "backend_service_name": page.name, 
            "backend_instance_group_name": page.backends[0].group.split('/')[-1]
        } 
        for page in backendClient.list(project=project)
    ]

    # Create a list for instance groups with instance size = 0
    instance_groups = [
        instance.name for zone, response in instanceClient.aggregated_list(project=project) 
        for instance in response.instance_groups if instance.size == 0
    ]

    # Compare the backend service instance groups to the instance groups that have instance size = 0
    result = [
        {
            "backend_service_name": ser["backend_service_name"], 
            "instance_group_name": ser["backend_instance_group_name"]
        }
        for ser in backend_services if ser["backend_instance_group_name"] in instance_groups
    ]

    return (False, result) if result else (True, None)






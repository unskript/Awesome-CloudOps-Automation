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
    """gcp_get_unused_backend_services Returns a list of unused backend services and their target groups which have 0 instances in the given project.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type project: string
    :param project: Google Cloud Platform Project

    :return: Status, List of unused Backend services
    """
    result = []
    Bclient = compute_v1.BackendServicesClient(credentials=handle)
    backend_services = []
    for page in Bclient.list(project=project):
        service = page.backends[0].group.split('/')[-1]
        backend_services.append({"backend_service_name": page.name, "backend_instance_group_name": service})
    instanceClient = compute_v1.InstanceGroupsClient(credentials=handle)
    agg_list = instanceClient.aggregated_list(project=project)
    for ser in backend_services:
        for zone, response in agg_list:
            if response.instance_groups:
                for instance in response.instance_groups:
                    if instance.size == 0:
                        if ser["backend_instance_group_name"] == instance.name:
                            if instance.name not in result:
                                result.append({"backend_service_name": ser["backend_service_name"], "instance_group_name":instance.name})
    if result:
        return (False, result)
    return(True, None)





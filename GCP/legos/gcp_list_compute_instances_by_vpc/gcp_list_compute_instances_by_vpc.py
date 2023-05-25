##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from google.cloud.compute_v1.services.instances import InstancesClient

class InputSchema(BaseModel):
    project: str = Field(
        title="GCP Project",
        description="GCP Project Name"
    )
    zone: str = Field(
        title="Zone",
        description="GCP Zone where instance list should be gotten from"
    )
    vpc_id: str = Field(
        title="VPC Name",
        description="Name of the VPC."
    )


def gcp_list_compute_instances_by_vpc_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)


def gcp_list_compute_instances_by_vpc(
        handle,
        project: str,
        zone: str,
        vpc_id: str
        ) -> List:
    """gcp_list_instances_by_vpc Returns the List of compute instances
    
        :type project: string
        :param project: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the instance list in the project should be fetched.

        :type vpc_id: string
        :param vpc_id: Name of the VPC.

        :rtype: List of instances
    """
    result = []
    ic = InstancesClient(credentials=handle)
    instances = ic.list(project=project, zone=zone)
    instance_list = []
    for instance in instances:
        instance_list.append(instance.name)

    for instance in instance_list:
        get_data = ic.get(project=project, zone=zone, instance=instance)
        response = get_data.network_interfaces
        for data in response:
            if vpc_id in data.network:
                result.append(instance)

    return result

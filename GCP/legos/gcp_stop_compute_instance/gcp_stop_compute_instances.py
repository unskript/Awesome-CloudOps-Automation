##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint 
from typing import Dict
from pydantic import BaseModel, Field
from google.cloud.compute_v1.services.instances import InstancesClient


class InputSchema(BaseModel):
    project_name: str = Field(
        title = "GCP Project",
        description = "GCP Project Name"
    )
    zone: str = Field(
        title = "Zone",
        description = "GCP Zone where instance list should be gotten from"
    )
    instance_name: str = Field(
        title = "Instance Name",
        description = "Name of the instance."
    )


def gcp_stop_instance_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)


def gcp_stop_instance(handle, project_name: str, zone:str, instance_name: str) -> Dict:
    """gcp_stop_instance Returns the dict of instance data

        :type project: string
        :param project: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the instance list in the project should be fetched.

        :type instance_name: string
        :param instance_name: Name of the instance.

        :rtype: Dict of instances data
    """
    output = {}
    try:
        ic = InstancesClient(credentials=handle)
        result = ic.stop(
            project=project_name, zone=zone, instance=instance_name)
        
        output['id'] = result.id
        output['name'] = result.name
        output['status'] = result.status
    except Exception as error:
        output["error"] = error
        
    return output

from typing import List, Optional
from pydantic import BaseModel, Field
from google.cloud.compute_v1.services.instances import InstancesClient
import re

class InputSchema(BaseModel):
    project: str = Field(
        title = "GCP Project",
        description = "GCP Project Name"
    )
    zone: Optional[str] = Field(
        title = "Zone",
        description = "GCP Zone where instance list should be gotten from"
    )


def gcp_list_compute_instances_printer(output):
    if len(output) == 0:
        return
    for instance in output:
        print(instance)

def gcp_list_compute_instances(handle, project: str, zone:str="") -> List:
    """gcp_list_compute_instances Returns the List of compute instances
    from given project and zone

    :type project: string
    :param project: Google Cloud Platform Project

    :type zone: string
    :param zone: Zone to which the instance list in the project should be fetched.

    :rtype: List of instances
    """
    output = []
    instanceClient = InstancesClient(credentials=handle)
    if zone:
        instances = instanceClient.list(project=project, zone=zone)
        for instance in instances:
            output.append({"instance_name": instance.name,"instance_zone": zone})
    else:
        request = {"project" : project,}
        agg_list = instanceClient.aggregated_list(request=request)
        for instance_zone, response in agg_list:
            if response.instances:
                for instance in response.instances:
                    zone_url = re.compile(r'https:\/\/www\.googleapis\.com\/compute\/v1\/projects\/unskript-dev\/zones\/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)')
                    instance_zone = zone_url.search(instance.zone)
                    output.append({"instance_name": instance.name, "instance_zone": instance_zone.group(1)})
    return output

from typing import List
from pydantic import BaseModel, Field
from google.cloud.compute_v1.services.instances import InstancesClient

class InputSchema(BaseModel):
    project: str = Field(
        title = "GCP Project",
        description = "GCP Project Name"
    )
    zone: str = Field(
        title = "Zone",
        description = "GCP Zone where instance list should be gotten from"
    )


def get_gcp_instance_list_printer(output):
    if len(output) == 0:
        return
    for instance in output:
        print(instance)

def get_gcp_instance_list(handle, project: str, zone:str) -> List:
    """get_gcp_instance_lsit Returns the List of compute instances
    from given project and zone

    :type project: string
    :param project: Google Cloud Platform Project

    :type zone: string
    :param zone: Zone to which the instance list in the project should be fetched.

    :rtype: List of instances
    """
    output = []
    ic = InstancesClient(credentials=handle)
    instances = ic.list(project=project, zone=zone)

    for instance in instances:
        output.append({"Name": instance.name, "MachineType": instance.machine_type})

    return output
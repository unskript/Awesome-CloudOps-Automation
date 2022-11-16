# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ESB.')
    volume_id: str = Field(
        title='Volume id',
        description='The ID of the volume.')


def aws_detach_ebs_to_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_detach_ebs_to_instances(handle, region: str, volume_id: str) -> Dict:
    """aws_detach_ebs_to_instances Detach instances from a particular Elastic Block Store (EBS).

     :type handle: object
     :param handle:Object returned from task.validate(...).
     
     :type volume_id: string
     :param volume_id: The ID of the volume.

     :type region: string
     :param region: AWS Region of the ESB.

     :rtype: dict with registered instance details.
    """

    ec2Client = handle.client('ec2', region_name=region)

    response = ec2Client.detach_volume(VolumeId=volume_id)

    print(response)

    return response

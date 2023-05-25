# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the EBS volume')
    instance_id: str = Field(
        title='Instance Id',
        description='ID of the EC2 instance')
    volume_id: str = Field(
        title='Volume Id',
        description='ID of the EBS volume')
    device_name: str = Field(
        title='Device Name',
        description='The device name')


def aws_attach_ebs_to_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_attach_ebs_to_instances(
    handle: Session,
    region: str,
    instance_id: str,
    volume_id: str,
    device_name: str
    ) -> Dict:   
    """aws_attach_ebs_to_instances Attach instances under a particular Elastic Block Store (EBS).

    :type region: string
    :param region: AWS Region of the EBS volume

    :type instance_id: string
    :param instance_id: ID of the instance

    :type volume_id: string
    :param volume_id: The ID of the volume

    :type device_name: string
    :param device_name: The device name

    :rtype: dict with registered instance details.
    """

    ec2Client = handle.client('ec2', region_name=region)
    response = ec2Client.attach_volume(
        Device=device_name,
        InstanceId=instance_id,
        VolumeId=volume_id
    )

    return response

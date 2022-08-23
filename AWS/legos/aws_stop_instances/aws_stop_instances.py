##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    instance_id: str = Field(
        title='Instance Id',
        description='ID of the instance to be stopped.')
    region: str = Field(
        title='Region',
        description='AWS Region of the instance.')


def aws_stop_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_stop_instances(handle, instance_id: str, region: str) -> Dict:
    """aws_stop_instances Stops instances.

        :type instance_id: string
        :param instance_id: String containing the name of AWS EC2 instance

        :type region: string
        :param region: AWS region for instance

        :rtype: Dict with the stopped instances state info.
    """

    ec2Client = handle.client('ec2', region_name=region)
    output = {}
    res = ec2Client.stop_instances(InstanceIds=[instance_id])
    for instances in res['StoppingInstances']:
        output[instances['InstanceId']] = instances['CurrentState']

    return output

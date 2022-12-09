##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
from unskript.connectors.aws import aws_get_paginator
import pprint

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service.')

def aws_get_all_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_get_all_ec2_instances(handle, region: str) -> List:
    """aws_get_all_ec2_instances Returns an array of instances.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region to filter instances.

        :rtype: Array of instances.
    """
    ec2Client = handle.client('ec2', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
    result = []
    for reservation in res:
        for instance in reservation['Instances']:
            result.append(instance['InstanceId'])
    return result

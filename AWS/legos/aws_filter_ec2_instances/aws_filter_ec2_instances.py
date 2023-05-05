##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from beartype import beartype

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')

@beartype
def aws_filter_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


@beartype
def aws_filter_ec2_instances(handle, region: str) -> List:
    """aws_filter_ec2_by_tags Returns an array of instances.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :rtype: Array of instances.
    """
    # Input param validation.

    ec2Client = handle.client('ec2', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")

    result = []
    for reservation in res:
        for instance in reservation['Instances']:
            result.append(instance['InstanceId'])
    return result

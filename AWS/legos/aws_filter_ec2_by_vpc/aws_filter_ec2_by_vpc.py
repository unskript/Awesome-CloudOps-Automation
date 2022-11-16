##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    vpc_id: str = Field(
        title='VPC Id',
        description='VPC ID of the instances.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_filter_ec2_by_vpc_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})



def aws_filter_ec2_by_vpc(handle, vpc_id: str, region: str) -> List:
    """aws_filter_ec2_by_vpc_id Returns a array of instances matching the vpc id.

        :type handle: object
        :param handle: Object containing global params for the notebook.

        :type vpc_id: string
        :param vpc_id: VPC ID of the instances.

        :type region: string
        :param region: AWS Region.

        :rtype: Array of the instances maching the vpc id.
    """
    # Input param validation.

    ec2Client = handle.client('ec2', region_name=region)

    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations",
                            Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])

    result = []
    for reservation in res:
        for instance in reservation['Instances']:
            result.append(instance['InstanceId'])
    return result

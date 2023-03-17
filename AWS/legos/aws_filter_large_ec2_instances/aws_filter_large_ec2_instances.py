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
    tag_key: str = Field(
        title='Tag Key',
        description='The key for the EC2 instance tag.')
    tag_value: str = Field(
        title='Tag Value',
        description='The value for the EC2 instance tag.')
    

def aws_filter_large_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_filter_large_ec2_instances(handle, tag_key: str, tag_value: str, region: str) -> List:
    """aws_filter_large_ec2_instances Returns an array of instances with large instance type

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type tag_key: string
        :param tag_key: The key for the EC2 instance tag.

        :type tag_value: string
        :param tag_value: The value for the EC2 instance tag.

        :type region: string
        :param region: EC2 instance region.

        :rtype: Array of instances with large instance type.
    """
    result = []
    try:
        ec2Client = handle.client('ec2', region_name=region)
        res = aws_get_paginator(ec2Client, "describe_instances", "Reservations",
                                Filters=[{'Name': 'instance-type', 'Values': ['*large']}])
        for reservation in res:
            for instance in reservation['Instances']:
                if not any(tag['Key'] == tag_key and tag['Value'] == tag_value for tag in instance["Tags"]):
                    result.append(instance['InstanceId'])
    except Exception as e:
        result.append(e)

    return result

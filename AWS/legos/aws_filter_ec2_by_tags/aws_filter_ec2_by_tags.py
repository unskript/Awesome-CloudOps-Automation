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
    tag_key: str = Field(
        title='Tag Key',
        description='The key of the tag.')
    tag_value: str = Field(
        title='Tag Value',
        description='The value of the key.')
    region: str = Field(
        title='Region',
        description='AWS Region.')

@beartype
def aws_filter_ec2_by_tags_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


@beartype
def aws_filter_ec2_by_tags(handle, tag_key: str, tag_value: str, region: str) -> List:
    """aws_filter_ec2_by_tags Returns an array of instances matching tags.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method

        :type tag_key: string
        :param tag_key: AWS Tag Key that was used ex: ServiceName, ClusterName, etc..

        :type tag_value: string
        :param tag_value: The Value for the Above Key, example "vpn-1" so the Lego will search
                          only the required texts in the Lego.
        
        :type region: string
        :param region: The AWS Region, For example `us-west-2`

        :rtype: Array of instances matching tags.
    """
    # Input param validation.

    ec2Client = handle.client('ec2', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations",
                            Filters=[{'Name': 'tag:' + tag_key, 'Values': [tag_value]}])

    result = []
    for reservation in res:
        for instance in reservation['Instances']:
            result.append(instance['InstanceId'])
    return result

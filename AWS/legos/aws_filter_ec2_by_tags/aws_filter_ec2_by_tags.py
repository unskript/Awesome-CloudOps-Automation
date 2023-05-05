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
        :param handle: Object returned by the task.validate(...) method.

        :type tag_key: string
        :param tag_key: Key for the EC2 instance tag.

        :type tag_value: string
        :param tag_value: value for the EC2 instance tag.

        :type region: string
        :param region: EC2 instance region.

        :rtype: Array of instances matching tags.
    """

    ec2Client = handle.client('ec2', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations",
                            Filters=[{'Name': 'tag:' + tag_key, 'Values': [tag_value]}])
    result = []
    for reservation in res:
        for instance in reservation['Instances']:
            result.append(instance['InstanceId'])
    return result

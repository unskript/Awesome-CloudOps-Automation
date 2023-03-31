##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pprint

class InputSchema(BaseModel):
    resource_arn: list = Field(
        title='Resource ARN',
        description='Resource ARNs.')
    tag_key: str = Field(
        title='Tag Key',
        description='Resource Tag Key.')
    tag_value: str = Field(
        title='Tag Value',
        description='Resource Tag Value.')
    region: str = Field(
        title='Region',
        description='AWS Region.')

def aws_attach_tags_to_resources_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_attach_tags_to_resources(handle, resource_arn: list, tag_key: str, tag_value: str, region: str) -> Dict:
    """aws_attach_tags_to_resources Returns an Dict of resource info.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type resource_arn: list
        :param resource_arn: Resource ARNs.

        :type tag_key: str
        :param tag_key: Resource Tag Key.

        :type tag_value: str
        :param tag_value: Resource Tag value.

        :type region: str
        :param region: Region to filter resources.

        :rtype: Dict of resource info.
    """
    ec2Client = handle.client('resourcegroupstaggingapi', region_name=region)
    result = {}
    try:
        response = ec2Client.tag_resources(
            ResourceARNList=resource_arn,
            Tags={tag_key: tag_value}
            )
        result = response

    except Exception as error:
        result["error"] = error

    return result



    
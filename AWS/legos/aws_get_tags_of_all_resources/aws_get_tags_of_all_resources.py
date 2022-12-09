##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pprint

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')

def aws_resources_tags_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_resources_tags(handle, region: str) -> List:
    """aws_resources_tags Returns an List of all Resources Tags.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: Region to filter resources.

        :rtype: List of all Resources Tags.
    """
    ec2Client = handle.client('resourcegroupstaggingapi', region_name=region)
    result = []
    try:
        response = aws_get_paginator(ec2Client, "get_tag_keys", "TagKeys")
        result = response
    except Exception as error:
        result.append({"error":error})

    return result


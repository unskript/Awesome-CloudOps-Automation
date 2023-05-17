##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')

def aws_get_all_untagged_resources_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_all_untagged_resources(handle, region: str) -> List:
    """aws_get_all_untagged_resources Returns an List of Untagged Resources.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: Region to filter resources.

        :rtype: List of untagged resources.
    """

    ec2Client = handle.client('resourcegroupstaggingapi', region_name=region)
    result = []
    try:
        response = aws_get_paginator(ec2Client, "get_resources", "ResourceTagMappingList")
        for resources in response:
            if not resources["Tags"]:
               result.append(resources["ResourceARN"])
    except Exception as error:
        result.append({"error":error})

    return result

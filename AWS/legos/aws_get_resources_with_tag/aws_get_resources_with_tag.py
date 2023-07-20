from __future__ import annotations

##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    tag: str = Field(..., description='The Tag to search for', title='tag')


def aws_get_resources_with_tag_printer(output):
    if output is None:
        return
    pprint.pprint(f"there are {len(output)} resources with the desired tag." )


def aws_get_resources_with_tag(handle, region: str, tag:str) -> List:
    """aws_get_resources_with_tag Returns an List of Untagged Resources.

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
            if  resources["Tags"]:
                #has tags
                #print(tagged_instance)
                #get all the keys for the instance
                for kv in resources['Tags']:
                    key = kv["Key"]
                    if tag == key:
                        temp = {"arn": resources["ResourceARN"], "value":kv["Value"]}
                        result.append(temp)

    except Exception as error:
        result.append({"error":error})

    return result



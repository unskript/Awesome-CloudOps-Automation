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


def aws_get_resources_with_expiration_tag_printer(output):
    if output is None:
        return
    pprint.pprint(f"there are {len(output)} resources with expiration tag." )


def aws_get_resources_with_expiration_tag(handle, region: str, tag:str) -> List:

    ec2Client = handle.client('resourcegroupstaggingapi', region_name=region)
    result = []
    try:
        response = aws_get_paginator(ec2Client, "get_resources", "ResourceTagMappingList")
        for resources in response:
            if resources["Tags"]:
                #has tags
                tags = resources['Tags']
                for kv in resources['Tags']:
                    if kv["Key"] == tag:
                        #we have found an expiration tag
                        temp ={'arn': [resources["ResourceARN"]], 'expires':kv["Value"]}
                        print(temp)
                        result.append(temp)

    except Exception as error:
        result.append({"error":error})

    return result



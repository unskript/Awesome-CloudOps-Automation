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


def aws_get_resources_missing_tag_printer(output):
    if output is None:
        return
    pprint.pprint(f"there are {len(output)} resources missing the tag. We can fix a max of 20." )


def aws_get_resources_missing_tag(handle, region: str, tag:str) -> List:
    """aws_get_resources_missing_tag Returns an List of Untagged Resources.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: Region to filter resources.

        :rtype: List of untagged resources.
    """

    ec2Client = handle.client('resourcegroupstaggingapi', region_name=region)
    result = []

    arnKeywordsToIgnore = ["sqlworkbench",
                           "AutoScalingManagedRule",
                           "sagarProxy",
                           "fsap-0f4d1bbd83f172783",
                           "experiment"]

    try:
        response = aws_get_paginator(ec2Client, "get_resources", "ResourceTagMappingList")
        for resources in response:
            if not resources["Tags"]:
                #no tags at all!!
                arnIgnore = False
                for substring in arnKeywordsToIgnore:
                    if substring in resources["ResourceARN"]:
                        arnIgnore = True
                if not arnIgnore:
                    # instance is missing tag
                    result.append(resources["ResourceARN"])
            else:
                #has tags
                allTags = True
                keyList = []
                tagged_instance = resources['Tags']
                #print(tagged_instance)
                #get all the keys for the instance
                for kv in tagged_instance:
                    key = kv["Key"]
                    keyList.append(key)
                #see if the required tags are represented in the keylist
                #if they are not - the instance is not in compliance
                if tag not in keyList:
                    allTags = False
                if not allTags:
                    arnIgnore = False
                    for substring in arnKeywordsToIgnore:
                        if substring in resources["ResourceARN"]:
                            arnIgnore = True
                    if not arnIgnore:
                        # instance is missing tag
                        result.append(resources["ResourceARN"])

    except Exception as error:
        result.append({"error":error})

    return result



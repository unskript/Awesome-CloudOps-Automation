##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator

class InputSchema(BaseModel):
    tag_key: str = Field(
        title='Tag name',
        description='Name of the tag to filter by.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_filter_target_groups_by_tags_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_filter_target_groups_by_tags(handle, tag_key: str, region: str) -> List:
    """aws_filter_target_groups_by_tags Returns a array of dict with target group and tag value.

        :type handle: object
        :param handle: Object containing global params for the notebook.

        :type vpc_id: string
        :param vpc_id: VPC ID of the instances.

        :type region: string
        :param region: AWS Region.

        :rtype: Returns a array of dict with target group and tag value.
    """
    elbv2Client = handle.client('elbv2', region_name=region)
    tbs = aws_get_paginator(elbv2Client, "describe_target_groups", "TargetGroups")
    tbArnsList = []
    output = []
    count = 0
    tbsLength = len(tbs)
    for index, tb in enumerate(tbs):
        # Need to call describe_tags to get the tags associated with these TGs,
        # however that call can only take 20 TGs.
        tbArnsList.append(tb.get('TargetGroupArn'))
        count = count + 1
        if count == 20 or index == tbsLength - 1:
            tagDescriptions = elbv2Client.describe_tags(ResourceArns=tbArnsList).get('TagDescriptions')
            # Check if the tag name exists in any of the TGs.
            for tagDescription in tagDescriptions:
                for tag in tagDescription.get('Tags'):
                    if tag.get('Key') == tag_key:
                        output.append({
                            "ResourceARN": tagDescription.get('ResourceArn'),
                            "TagValue": tag.get('Value')
                            })
                        break
            count = 0
            tbArnsList = []
    return output

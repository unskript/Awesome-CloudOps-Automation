##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Name of the AWS Region'
    )


def aws_filter_untagged_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def check_untagged_instance(res, r):
    instance_list = []
    for reservation in res:
        for instance in reservation['Instances']:
            instances_dict = {}
            tags = instance.get('Tags', None)
            if tags is None:
                instances_dict['region'] = r
                instances_dict['instanceID'] = instance['InstanceId']
                instance_list.append(instances_dict)
    return instance_list


def aws_filter_untagged_ec2_instances(handle, region: str= None) -> Tuple:
    """aws_filter_untagged_ec2_instances Returns an array of instances which has no tags.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: Region to filter instances.

        :rtype: Tuple of status, and list of untagged EC2 Instances
    """
    if not handle or (region and region not in aws_list_all_regions(handle)):
        raise ValueError("Invalid input parameters provided.")
    result = []
    all_regions = [region]
    if region is None or len(region) == 0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=r)
            res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            untagged_instances = check_untagged_instance(res, r)
            result.extend(untagged_instances)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

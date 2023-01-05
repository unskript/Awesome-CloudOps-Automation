##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


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
    instances_dict = {}
    for reservation in res:
            for instance in reservation['Instances']:
                try:
                    tagged_instance = instance['Tags']
                    if len(tagged_instance) != 0:
                        instance_list.append(instance['InstanceId'])
                except Exception as e:
                    instance_list.append(instance['InstanceId'])
    if len(instance_list)!=0:
        instances_dict['region']= r
        instances_dict['instances']= instance_list
    return instances_dict


def aws_filter_untagged_ec2_instances(handle, region: str) -> Tuple:
    """aws_filter_untagged_ec2_instances Returns an array of instances which has no tags.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: Region to filter instances.

        :rtype: Tupple of the untagged EC2 Instances
    """
    result = []
    all_regions = [region]
    if region is None or len(region)==0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=r)
            res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            untagged_instances = check_untagged_instance(res, r)
            if len(untagged_instances)!=0:
                result.append(untagged_instances)
        except Exception as e:
            pass
    execution_flag = False
    if len(result) > 0:
        execution_flag = True
    output = (execution_flag, result)
    return output

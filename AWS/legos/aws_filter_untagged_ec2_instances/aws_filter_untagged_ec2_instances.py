##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_filter_untagged_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_filter_untagged_ec2_instances(handle, region: str) -> List:
    """aws_filter_untagged_ec2_instances Returns an array of instances which has no tags.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: Region to filter instances.

        :rtype: Result of the API in the List form.
    """

    
    ec2Client = handle.client('ec2', region_name=region)

    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
    
    # get the all untagged ec2 instances.
    result = []
    for reservation in res:
        for instance in reservation['Instances']:
            try:
                tagged_instance = instance['Tags']
                if len(tagged_instance) == 0:
                    result.append(instance['InstanceId'])
                        
            except Exception as e:
                result.append(instance['InstanceId'])

    return result
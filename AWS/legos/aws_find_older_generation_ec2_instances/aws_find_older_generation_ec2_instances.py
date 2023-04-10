##
##  Copyright (c) 2023 unSkript, Inc
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


def aws_find_older_generation_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_find_older_generation_ec2_instances(handle, region: str) -> List:
    """aws_find_older_generation_ec2_instances Returns an array of instances.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region to filter instances.

        :rtype: Array of instances.
    """
    # Define the older generation instance types
    older_instance_types = ['t2', 'm1', 'm2', 'm3', 'm4', 'c1', 'c3']
    try:
        ec2Client = handle.client('ec2', region_name=region)
        res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
        result = []
        for reservation in res:
            for instance in reservation['Instances']:
                # Extract the instance ID, instance type
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                # Check if the instance is of older generation
                if instance_type.split('.')[0].lower() in older_instance_types:
                    result.append(instance_id)
    except Exception as e:
        raise Exception(e)
    return result
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from tabulate import tabulate
from botocore.exceptions import ClientError
import pprint

class InputSchema(BaseModel):
    instance_ids: list = Field(
        title='Instance IDs',
        description='List of instances.')

    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service.')


def aws_get_auto_scaling_instances_printer(output):
    if output is None:
        return
    print(tabulate(output, headers='keys'))


def aws_get_auto_scaling_instances(handle, instance_ids: list, region: str) -> List:
    """aws_get_auto_scaling_instances List of Dict with instanceId and attached groups.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type instance_ids: list
        :param instance_ids: List of instances.

        :type region: string
        :param region: Region to filter instances.

        :rtype: List of Dict with instanceId and attached groups.
    """
    result = []
    ec2Client = handle.client('autoscaling', region_name=region)
    try:
        response = ec2Client.describe_auto_scaling_instances(InstanceIds=instance_ids)
        for group in response["AutoScalingInstances"]:
            group_dict = {}
            group_dict["InstanceId"] = group["InstanceId"]
            group_dict["AutoScalingGroupName"] = group["AutoScalingGroupName"]
            result.append(group_dict)
    except Exception as error:
        err = {"Error":error}
        result.append(err)
    return result
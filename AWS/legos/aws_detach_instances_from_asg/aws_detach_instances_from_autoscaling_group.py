##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    instance_ids: str = Field(
        title='Instance IDs',
        description='List of instances.')
    group_name: str = Field(
        title='Group Name',
        description='Name of AutoScaling Group.')
    region: str = Field(
        title='Region',
        description='AWS Region of autoscaling group.')

def aws_detach_autoscaling_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_detach_autoscaling_instances(
    handle,
    instance_ids: str,
    group_name: str,
    region: str
) -> Dict:
    """aws_detach_autoscaling_instances detach instances from autoscaling group.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type instance_ids: string
        :param instance_ids: Name of instances.

        :type group_name: string
        :param group_name: Name of AutoScaling Group.

        :type region: string
        :param region: AWS Region of autoscaling group.

        :rtype: Dict with the detach instance info.
    """

    ec2Client = handle.client("autoscaling", region_name=region)
    result = {}
    try:
        response = ec2Client.detach_instances(
            InstanceIds=[instance_ids],
            AutoScalingGroupName=group_name,
            ShouldDecrementDesiredCapacity=True
            )
        result = response
    except Exception as error:
        result["error"] = error
        
    return result

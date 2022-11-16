##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint


class InputSchema(BaseModel):
    instance_ids: List[str] = Field(
        title='Instance IDs',
        description='List of instance IDs. For eg. ["i-foo", "i-bar"]')
    region: str = Field(
        title='Region',
        description='AWS Region of the instance.')


def aws_terminate_instance_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_terminate_instance(handle, instance_ids: List, region: str) -> Dict:
    """aws_terminate_instance Returns an Dict of info terminated instance.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type instance_ids: List
        :param instance_ids: Tag to filter Instances.

        :type region: string
        :param region: Used to filter the instance for specific region.

        :rtype: Dict of info terminated instance.
    """
    ec2Client = handle.client('ec2', region_name=region)
    res = ec2Client.terminate_instances(InstanceIds=instance_ids)

    return res
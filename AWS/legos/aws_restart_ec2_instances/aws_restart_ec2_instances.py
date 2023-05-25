##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List, Dict
from pydantic import BaseModel, Field
from beartype import beartype

class InputSchema(BaseModel):
    instance_ids: List[str] = Field(
        title='Instance IDs',
        description='List of instance IDs. For eg. ["i-foo", "i-bar"]')
    region: str = Field(
        title='Region',
        description='AWS Region of the instances.')

@beartype
def aws_restart_ec2_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


@beartype
def aws_restart_ec2_instances(handle, instance_ids: List, region: str) -> Dict:
    """aws_restart_ec2_instances Restarts instances.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type instance_ids: list
        :param instance_ids: List of instance ids.

        :type region: string
        :param region: Region for instance.

        :rtype: Dict with the restarted instances info.
    """

    ec2Client = handle.client('ec2', region_name=region)
    res = ec2Client.reboot_instances(InstanceIds=instance_ids)
    return res

##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List

from unskript.legos.utils import parseARN


class InputSchema(BaseModel):
    arn: str = Field(
        title='Target Group ARN',
        description='ARN of the Target Group.')
    instance_ids: List[str] = Field(
        title='Instance IDs',
        description='List of instance IDs. For eg. ["i-foo", "i-bar"]')
    port: int = Field(
        title='Port',
        description='The port on which the instances are listening.'
    )
    unregister: bool = Field(
        False,
        title='Unregister',
        description='Check this if the instances need to be unregistered. By default, it is false.'
    )


"""
All legos should take inputParamsJson as the input.
They should assume the handle variable is defined already.
"""


def aws_target_group_register_unregister_instances(handle, arn: str, instance_ids: List, port: int,
                                                   unregister: bool = False) -> None:
    """aws_target_group_register_unregister_instances Allows register/unregister instances to a target group.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type arn: string
        :param arn: ARN of the Target Group.

        :type instance_ids: list
        :param instance_ids: List of instance IDs.

        :type port: int
        :param port: The port on which the instances are listening.

        :type unregister: bool
        :param unregister: Check this if the instances need to be unregistered.

        :rtype: None
    """
    # Input param validation.
    # Get the region for the target group.
    parsedArn = parseARN(arn)
    elbv2Client = handle.client('elbv2', region_name=parsedArn['region'])
    # Create the targets
    targets = []
    for i in instance_ids:
        targets.append({
            'Id': i,
            'Port': port,
        })
    try:
        if unregister == True:
            elbv2Client.deregister_targets({
                'TargetGroupArn': arn,
                'Targets': targets
            })
        else:
            elbv2Client.register_targets({
                'TargetGroupArn': arn,
                'Targets': targets
            })
    except Exception as e:
        print(f'Unable to register/unregister: {str(e)}')
        raise e

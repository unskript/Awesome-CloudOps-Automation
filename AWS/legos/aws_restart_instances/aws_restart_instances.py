##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint
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
    """aws_restart_instances Restarts instances.

        :type nbParamsObj: object
        :param nbParamsObj: Object containing global params for the notebook.

        :type credentialsDict: dict
        :param credentialsDict: Dictionary of credentials info.

        :type inputParamsJson: string
        :param inputParamsJson: Json string of the input params.

        :rtype: Dict with the stopped instances state info.
    """

    ec2Client = handle.client('ec2', region_name=region)
    res = ec2Client.reboot_instances(InstanceIds=instance_ids)
    return res
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
import time
from typing import List, Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    instance_ids: List[str] = Field(
        title='Instance IDs',
        description='List of instance IDs. For eg. ["i-foo", "i-bar"]')
    document_name: str = Field(
        'AWS-RunPowerShellScript',
        title='Document Name',
        description='Name of the SSM document to run.')
    parameters: List[str] = Field(
        title='SSM Document Name',
        description='List of commands to execute on instance. For eg. ["ifconfig", "pwd"]')
    region: str = Field(
        title='Region',
        description='AWS Region of the AWS Instance.')


def aws_execute_command_ssm_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def aws_execute_command_ssm(handle, instance_ids: list, parameters: list, region: str,
                            document_name: str = "AWS-RunPowerShellScript") -> Dict:
    """aws_execute_command_via_ssm EC2 Run Command via SSH.
     
     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type instance_ids: list
     :param instance_ids: List of instance IDs. For eg. ["i-foo", "i-bar"]

     :type parameters: list
     :param parameters: List of commands to execute on instance. For eg. ["ifconfig", "pwd"]

     :type document_name: string
     :param document_name: Document Name.

     :type region: string
     :param region: AWS Region of the AWS Instance.

     :rtype: Dict of command output.
    """

    ssm_client = handle.client('ssm', region_name=region)
    response = ssm_client.send_command(
        InstanceIds=instance_ids,
        DocumentName=document_name,
        Parameters={
            'commands': parameters
        })
    command_id = response['Command']['CommandId']
    output = {}
    time.sleep(2)
    for instance_id in instance_ids:
        res = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        output[instance_id] = res
    return output

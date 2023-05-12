##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    group_id: str = Field(
        title='Security Group ID',
        description='AWS Security Group ID. For eg: sg-12345')
    region: str = Field(
        title='Region',
        description='AWS Region'
    )


def aws_get_security_group_details_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_security_group_details(handle, group_id: str, region: str) -> Dict:
    """aws_get_security_group_details returns The decrypted secret value

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type group_id: string
     :param group_id: AWS Security Group ID. For eg: sg-12345

     :type region: string
     :param region: AWS Region.

     :rtype: The decrypted secret value
    """

    ec2Client = handle.client('ec2', region_name=region)

    res = ec2Client.describe_security_groups(GroupIds=[group_id])
    return res

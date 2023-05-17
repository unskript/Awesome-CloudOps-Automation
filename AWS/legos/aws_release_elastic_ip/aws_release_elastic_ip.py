##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    allocation_id: str = Field(
        title='Allocation ID',
        description='Allocation ID of the Elastic IP to release.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_release_elastic_ip_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_release_elastic_ip(handle, region: str, allocation_id: str) -> Dict:
    """aws_release_elastic_ip release elastic ip.
    
        :type allocation_id: string
        :param allocation_id: Allocation ID of the Elastic IP to release.

        :type region: string
        :param region: AWS Region.

        :rtype: Dict with the release elastic ip info.
    """
    try:
        ec2_Client = handle.client('ec2', region_name=region)
        response = ec2_Client.release_address(AllocationId=allocation_id)
        return response
    except Exception as e:
        raise Exception(e) from e

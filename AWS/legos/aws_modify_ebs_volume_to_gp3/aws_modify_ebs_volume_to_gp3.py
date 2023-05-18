##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')
    volume_id: str = Field(
        title='Volume ID',
        description='EBS Volume ID.')


def aws_modify_ebs_volume_to_gp3_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_modify_ebs_volume_to_gp3(handle, region: str, volume_id: str) -> List:
    """aws_modify_ebs_volume_to_gp3 returns an array of modified details for EBS volumes.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :type volume_id: string
        :param volume_id: EBS Volume ID.

        :rtype: List of modified details for EBS volumes
    """
    result = []
    try:
        ec2Client = handle.client('ec2', region_name=region)
        volumes = ec2Client.modify_volume(VolumeId=volume_id, VolumeType='gp3')
        result.append(volumes)
    except Exception as e:
        result.append({"error": e})

    return result

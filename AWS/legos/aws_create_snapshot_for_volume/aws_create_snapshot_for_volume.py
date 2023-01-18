##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint


class InputSchema(BaseModel):
    volume_id: str = Field(
        title='Volume ID',
        description='Volume ID to create snapshot for particular volume e.g. vol-01eb21cfce30a956c')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_create_volumes_snapshot_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_create_volumes_snapshot(handle, volume_id: str, region: str) -> List:
    """aws_create_volumes_snapshot Returns an list containing SnapshotId.

        :type region: string
        :param region: used to filter the volume for a given region.

        :type volume_id: string
        :param volume_id: Volume ID to create snapshot for particular volume.

        :rtype: List containing SnapshotId.
    """
    result = []

    ec2Client = handle.resource('ec2', region_name=region)

    try:
        response = ec2Client.create_snapshot(VolumeId=volume_id)
        result.append(response)
    except Exception as e:
        raise e

    return result

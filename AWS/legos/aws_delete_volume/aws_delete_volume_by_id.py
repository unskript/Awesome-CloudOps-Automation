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
        description='Volume ID is needed to delete a particular volume e.g. vol-01eb21cfce30a956c.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_delete_volumes_printer(output):
    if output is None:
        return
    pprint.pprint({"Output": output})


def aws_delete_volumes(handle, volume_id: str, region: str) -> List:
    """aws_delete_volumes Returns array of delete volume status.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type region: string
        :param region: used to filter the volume for a given region.

        :type volume_id: string
        :param volume_id: Volume ID to delete a given volume.

        :rtype: Array of delete volume status.
    """
    result = []

    ec2Client = handle.client('ec2',region_name=region)

    # Adding logic for deletion criteria
    try:
        response = ec2Client.delete_volume(VolumeId=volume_id,)
        result.append(response)
    except Exception as e:
        result.append(e)

    return result


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
        description='Volume ID.')
    region: str = Field(
        title='Region',
        description='AWS Region.')

def aws_delete_volumes_printer(output):
    if output is None:
        return
    pprint.pprint({"Output": output})

def aws_delete_volumes(handle, volume_id: str, region: str) -> str:
    """aws_filter_ebs_unattached_volumes Returns an array of ebs volumes.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :type volume_id: string
        :param volume_id: Volume ID needed to delete particular volume.

        :rtype: Result of the API in the List form.
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

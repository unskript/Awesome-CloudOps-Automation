##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_get_ebs_volumes_by_type_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_get_ebs_volumes_by_type(handle, region: str) -> Dict:
    """aws_get_ebs_volumes_by_type Returns an dict of ebs volumes with there types.

        :type region: string
        :param region: AWS Region.

        :rtype: Dict of ebs volumes with there types.
    """
    result = {}
    try:
        ec2Client = handle.resource('ec2', region_name=region)
        volumes = ec2Client.volumes.all()
        # collecting the volumes by there types
        for volume in volumes:
            volume_id = volume.id
            volume_type = volume.volume_type
            if volume_type in result:
                result[volume_type].append(volume_id)
            else:
                result[volume_type] = [volume_id]

    except Exception as e:
        raise Exception(e)
    return result
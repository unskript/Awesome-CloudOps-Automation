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


def aws_filter_ebs_unattached_volumes_printer(output):
    if output is None:
        return
    pprint.pprint({"Volume IDs": output})


def aws_filter_ebs_unattached_volumes(handle, region: str) -> List:
    """aws_filter_ebs_unattached_volumes Returns an array of ebs volumes.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.
        
        :type region: string
        :param region: Used to filter the volume for specific region.

        :rtype: Result of the API in the List form.
    """
    # Filtering the volume by region
    ec2Client = handle.resource('ec2',region_name=region)
    volumes = ec2Client.volumes.all()

    # collecting the volumes which has zero attachments
    result=[]
    for volume in volumes:
        if len(volume.attachments) == 0:
            result.append(volume.id)

    return result

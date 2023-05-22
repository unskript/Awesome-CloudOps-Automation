##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')


def aws_get_stopped_instance_volumes_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_stopped_instance_volumes(handle, region: str = "") -> Tuple:
    """aws_get_stopped_instance_volumes Returns an array of volumes.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region to filter instances.

        :rtype: Array of volumes.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=reg)
            res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            for reservation in res:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'stopped':
                        block_device_mappings = instance['BlockDeviceMappings']
                        for mapping in block_device_mappings:
                            if 'Ebs' in mapping:
                                ebs_volume = {}
                                volume_id = mapping['Ebs']['VolumeId']
                                ebs_volume["volume_id"] = volume_id
                                ebs_volume["region"] = reg
                                result.append(ebs_volume)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
    
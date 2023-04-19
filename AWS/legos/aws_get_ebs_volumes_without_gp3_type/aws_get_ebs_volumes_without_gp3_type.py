##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')


def aws_get_ebs_volumes_without_gp3_type_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_get_ebs_volumes_without_gp3_type(handle, region: str = "") -> Tuple:
    """aws_get_ebs_volumes_without_gp3_type Returns an array of ebs volumes.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :rtype: Tuple with status result and list of EBS Volume without GP3 type.
    """
    result=[]
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            # Filtering the volume by region
            ec2Client = handle.resource('ec2', region_name=reg)
            volumes = ec2Client.volumes.all()

            # collecting the volumes which has zero attachments
            for volume in volumes:
                volume_dict = {}
                if volume.volume_type != "gp3":
                    volume_dict["region"] = reg
                    volume_dict["volume_id"] = volume.id
                    volume_dict["volume_type"] = volume.volume_type
                    result.append(volume_dict)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
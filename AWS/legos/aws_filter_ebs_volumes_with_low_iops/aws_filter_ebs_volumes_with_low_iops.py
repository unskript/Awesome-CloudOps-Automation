##
##  Copyright (c) 2023 unSkript, Inc
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
    iops_threshold: Optional[int] = Field(
        default=100,
        title="IOPS's Threshold",
        description="IOPS's Threshold is a metric used to measure the amount of input/output operations that an EBS volume can perform per second.")


def aws_filter_ebs_volumes_with_low_iops_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_filter_ebs_volumes_with_low_iops(handle, region: str = "", iops_threshold: int = 100) -> Tuple:
    """aws_filter_ebs_unattached_volumes Returns an array of ebs volumes.

        :type region: string
        :param region: Used to filter the volume for specific region.

        :type iops_threshold: int
        :param iops_threshold: IOPS's Threshold is a metric used to measure the amount of input/output operations that an EBS volume can perform per second.

        :rtype: Tuple with status result and list of low IOPS EBS Volumes.
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

            # collecting the volumes which has low IOPS's
            for volume in volumes:
                volume_dict = {}
                if volume.iops < iops_threshold:
                    volume_dict["region"] = reg
                    volume_dict["volume_id"] = volume.id
                    volume_dict["volume_iops"] = volume.iops
                    result.append(volume_dict)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, [])
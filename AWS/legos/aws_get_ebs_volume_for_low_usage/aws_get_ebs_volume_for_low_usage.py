##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')
    threshold_days: Optional[int] = Field(
        default=10,
        title='Threshold (In days)',
        description='(in days) The threshold to check the EBS volume usage less than the threshold.')

def aws_get_ebs_volume_for_low_usage_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_get_ebs_volume_for_low_usage(handle, region: str = "", threshold_days: int = 10) -> Tuple:
    """aws_get_ebs_volume_for_low_usage Returns an array of ebs volumes.

        :type region: string
        :param region: AWS Region.

        :type threshold_days: int
        :param threshold_days: (in days) The threshold to check the EBS volume usage
        less than the threshold.

        :rtype: Tuple with status result and list of EBS Volume.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            # Filtering the volume by region
            ec2Client = handle.client('ec2', region_name=reg)
            response = aws_get_paginator(ec2Client, "describe_volumes", "Volumes")
            now = datetime.utcnow()
            days_ago = now - timedelta(days=threshold_days)
            # collecting the volumes which has zero attachments
            for volume in response:
                ebs_volume = {}
                volume_id = volume["VolumeId"]
                cloudwatch = handle.client('cloudwatch', region_name=reg)
                cloudwatch_response = cloudwatch.get_metric_statistics(
                                    Namespace='AWS/EBS',
                                    MetricName='VolumeUsage',
                                    Dimensions=[
                                        {
                                            'Name': 'VolumeId',
                                            'Value': volume_id
                                        }
                                    ],
                                    StartTime=days_ago,
                                    EndTime=now,
                                    Period=3600,
                                    Statistics=['Average']
                                )
                for v in cloudwatch_response['Datapoints']:
                    if v['Average'] < 10:
                        volume_ids = v['Dimensions'][0]['Value']
                        ebs_volume["volume_id"] = volume_ids
                        ebs_volume["region"] = reg
                        result.append(ebs_volume)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

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
        description='(in days) The threshold to check the EBS volume usage within given days.')
    usage_percent: Optional[int] = Field(
        default=10,
        title='Usage Percent (In percent)',
        description='(in days) The threshold to compaire the EBS volume usage less than the threshold.')

def aws_get_ebs_volume_for_low_usage_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_get_ebs_volume_for_low_usage(handle, region: str = "", threshold_days: int = 10, usage_percent: int = 10) -> Tuple:
    """aws_get_ebs_volume_for_low_usage Returns an array of ebs volumes.

        :type region: string
        :param region: AWS Region.

        :type threshold_days: int
        :param threshold_days: (in days) The threshold to check the EBS volume usage within given days.

        :type usage_percent: int
        :param usage_percent: (in percent) The threshold to compaire the EBS volume usage
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
                volume_size = volume['Size']
                cloudwatch = handle.client('cloudwatch', region_name=reg)
                read_metric_data = cloudwatch.get_metric_statistics(
                                    Namespace='AWS/EBS',
                                    MetricName='VolumeReadBytes',
                                    Dimensions=[
                                        {
                                            'Name': 'VolumeId',
                                            'Value': volume_id
                                        }
                                    ],
                                    StartTime=days_ago,
                                    EndTime=now,
                                    Period=86400,
                                    Statistics=['Sum']
                                )
                write_metric_data = cloudwatch.get_metric_statistics(
                                    Namespace='AWS/EBS',
                                    MetricName='VolumeWriteBytes',
                                    Dimensions=[
                                        {'Name': 'VolumeId', 'Value': volume_id},
                                    ],
                                    StartTime=days_ago,
                                    EndTime=now,
                                    Period=86400,
                                    Statistics=['Sum']
                                )
                if not read_metric_data['Datapoints'] and not write_metric_data['Datapoints']:
                    continue
                volume_read_bytes = read_metric_data['Datapoints'][0]['Sum'] if read_metric_data['Datapoints'] else 0
                volume_write_bytes = write_metric_data['Datapoints'][0]['Sum'] if write_metric_data['Datapoints'] else 0
                volume_usage_bytes = volume_read_bytes + volume_write_bytes
                volume_usage_percent = volume_usage_bytes / (volume_size * 1024 * 1024 * 1024) * 100
                if volume_usage_percent < usage_percent:
                    ebs_volume["volume_id"] = volume_id
                    ebs_volume["region"] = reg
                    result.append(ebs_volume)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

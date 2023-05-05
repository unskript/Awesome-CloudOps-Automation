##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pytz


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region.')
    threshold: Optional[int] = Field(
        default=30,
        title="Threshold (in days)",
        description="(in day's) The threshold to check the snapshots older than the threshold.")


def aws_filter_old_ebs_snapshots_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_filter_old_ebs_snapshots(handle, region: str="", threshold: int = 30) -> Tuple:
    """aws_filter_old_ebs_snapshots Returns an array of EBS snapshots details.

        :type region: string
        :param region: AWS Region.
        
        :type threshold: int
        :param threshold: (in days) The threshold to check the snapshots older than the threshold.

        :rtype: List of EBS snapshots details.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            # Filtering the volume by region
            current_time = datetime.now(pytz.UTC)
            ec2Client = handle.resource('ec2', region_name=reg)
            response = ec2Client.snapshots.filter(OwnerIds=['self'])
            for snapshot in response:
                snap_data = {}
                running_time = current_time - snapshot.start_time
                if running_time > timedelta(days=int(threshold)):
                    snap_data["region"] = reg
                    snap_data["snapshot_id"] = snapshot.id
                    result.append(snap_data)
        except Exception:
            pass
    if len(result)!=0:
        return (False, result)
    else:
        return (True, None)

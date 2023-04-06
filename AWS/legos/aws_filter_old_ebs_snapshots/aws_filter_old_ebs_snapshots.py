##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint
from datetime import datetime, timedelta
import pytz


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')
    threshold: int = Field(
        default=30,
        title="Threshold (in day's)",
        description="(in day's) The threshold to check the snapshots older than the threshold.")


def aws_filter_old_ebs_snapshots_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_filter_old_ebs_snapshots(handle, region: str, threshold: int = 30) -> List:
    """aws_filter_old_ebs_snapshots Returns an array of EBS snapshots details.

        :type region: string
        :param region: AWS Region.
        
        :type threshold: int
        :param threshold: (in days) The threshold to check the snapshots older than the threshold.

        :rtype: List of EBS snapshots details.
    """
    result = []
    try:
        # Filtering the volume by region
        current_time = datetime.now(pytz.UTC)
        ec2Client = handle.resource('ec2', region_name=region)
        response = ec2Client.snapshots.filter(OwnerIds=['self'])
        for snapshot in response:
            snap_data = {}
            running_time = current_time - snapshot.start_time
            if running_time > timedelta(days=int(threshold)):
                snap_data["snapshot_id"] = snapshot.id
                snap_data["start_time"] = snapshot.start_time
                snap_data["volume_size"] = snapshot.volume_size
                snap_data["description"] = snapshot.description
                snap_data["volume_id"] = snapshot.volume_id
                snap_data["age"] = running_time
                result.append(snap_data)
            
    except Exception as e:
        raise e

    return  result

##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Dict
import pprint

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')

    snapshot_id: str = Field(
        title='Snapshot ID',
        description='EBS snapshot ID. Eg: "snap-34bt4bfjed9d"')


def aws_delete_ebs_snapshots_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_ebs_snapshots(handle, region: str, snapshot_id: str) -> Dict:
    """aws_delete_ebs_snapshots Returns a dict of deleted snapshot details

        :type region: string
        :param region: AWS Region.

        :type snapshot_id: string
        :param snapshot_id: EBS snapshot ID. Eg: 'snap-34bt4bfjed9d'

        :rtype: Deleted snapshot details
    """
    result = []
    try:
        ec2Client = handle.client('ec2', region_name=region)
        result = ec2Client.delete_snapshot(SnapshotId=snapshot_id)
    except Exception as e:
        raise e
    return  result
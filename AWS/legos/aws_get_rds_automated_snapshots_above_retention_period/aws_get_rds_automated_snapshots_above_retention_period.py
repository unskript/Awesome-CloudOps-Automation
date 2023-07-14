##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import pytz
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', description='AWS Region of database.', title='Region'
    )
    threshold: Optional[int] = Field(
        '',
        description='The threshold number of days check for retention of automated snapshots. Default is 7 days',
        title='Threshold(in days)',
    )



def aws_get_rds_automated_snapshots_above_retention_period_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_rds_automated_snapshots_above_retention_period(handle, region: str="", threshold:int=7) -> Tuple:
    """aws_get_rds_automated_snapshots_above_retention_period List all the manual database snapshots.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region for database.

        :type threshold: int
        :param threshold: The threshold number of days check for retention of automated snapshots. Default is 7 days.

        :rtype: List of manual database snapshots.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    min_creation_time = datetime.now(pytz.UTC) - timedelta(days=threshold)
    for reg in all_regions:
        try:
            rdsClient = handle.client('rds', region_name=reg)
            response = aws_get_paginator(rdsClient, "describe_db_snapshots","DBSnapshots",
                                         SnapshotType='automated')
            for snapshot in response:
                snapshot_time = snapshot['SnapshotCreateTime'].replace(tzinfo=pytz.UTC)
                if snapshot_time < min_creation_time:
                    result.append({"db_identifier": snapshot['DBSnapshotIdentifier'], "region": reg})
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)



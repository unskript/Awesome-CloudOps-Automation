##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of database.')

def aws_filter_all_manual_database_snapshots_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_filter_all_manual_database_snapshots(handle, region: str) -> List:
    """aws_get_manual_snapshots List all the manual database snapshots.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region for database.

        :rtype: List of manual database snapshots.
    """

    ec2Client = handle.client('rds', region_name=region)
    result = []
    try:
        response = aws_get_paginator(ec2Client, "describe_db_snapshots","DBSnapshots",
                                     SnapshotType='manual')
        for snapshot in response:
            result.append(snapshot['DBSnapshotIdentifier'])
    except Exception:
        pass

    return result

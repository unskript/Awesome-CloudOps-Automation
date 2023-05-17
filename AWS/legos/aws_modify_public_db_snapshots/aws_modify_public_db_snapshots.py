##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    db_snapshot_identifier: str = Field(
        title='DB Snapshot Idntifier',
        description='DB Snapshot Idntifier of RDS.'
    )
    region: str = Field(
        title='Region',
        description='Region of the RDS.'
    )

def aws_modify_public_db_snapshots_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_modify_public_db_snapshots(handle, db_snapshot_identifier: str, region: str) -> List:
    """aws_modify_public_db_snapshots lists of publicly accessible DB Snapshot Idntifier Info.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type db_snapshot_identifier: string
        :param db_snapshot_identifier: DB Snapshot Idntifier of RDS.

        :type region: string
        :param region: Region of the RDS.

        :rtype: List with Dict of DB Snapshot Idntifier Info.
    """


    ec2Client = handle.client('rds', region_name=region)
    result = []
    try:
        response = ec2Client.modify_db_snapshot_attribute(
            DBSnapshotIdentifier=db_snapshot_identifier,
            AttributeName='restore', 
            ValuesToRemove=['all'])

        result.append(response)

    except Exception as error:
        result.append(error)

    return result

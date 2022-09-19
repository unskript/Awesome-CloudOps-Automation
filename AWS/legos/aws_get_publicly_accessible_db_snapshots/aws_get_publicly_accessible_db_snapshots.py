##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    db_snapshot_identifier: list = Field(
        title='DB Snapshot Idntifier',
        description='DB Snapshot Idntifier of RDS.'
    )
    region: str = Field(
        title='Region',
        description='Region of the RDS.'
    )


def aws_get_publicly_accessible_db_snapshots_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_publicly_accessible_db_snapshots(handle, db_snapshot_identifier: list, region: str) -> List:
    """aws_get_publicly_accessible_db_snapshots lists of publicly accessible db_snapshot_identifier.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type db_snapshot_identifier: List
        :param db_snapshot_identifier: DB Snapshot Idntifier of RDS.

        :type region: string
        :param region: Region of the RDS.

        :rtype: List with publicly accessible Snapshots Identifier in RDS.
    """

    ec2Client = handle.client('rds', region_name=region)
    result = []
    try:
        for identifier in db_snapshot_identifier:
            response = ec2Client.describe_db_snapshot_attributes(
                DBSnapshotIdentifier=identifier)
            db_attribute = response["DBSnapshotAttributesResult"]
            for value in db_attribute['DBSnapshotAttributes']:
                if "all" in value["AttributeValues"]:
                    result.append(db_attribute['DBSnapshotIdentifier'])

    except Exception as error:
        result.append(error)
        
    return result


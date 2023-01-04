##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_filter_all_manual_database_snapshots.aws_filter_all_manual_database_snapshots import aws_get_manual_database_snapshots
import pprint

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Region of the RDS'
    )


def aws_get_publicly_accessible_db_snapshots_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_publicly_accessible_db_snapshots(handle, region: str=None) -> Tuple:
    """aws_get_publicly_accessible_db_snapshots lists of publicly accessible db_snapshot_identifier.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the RDS.

        :rtype: List with publicly accessible Snapshots Identifier in RDS.
    """
    public_snapshots = []
    manual_snapshots_list=[]
    result=[]
    all_regions = [region]
    if region is None or not region:
        all_regions = aws_list_all_regions(handle=handle)
    try:
        for r in all_regions:
            snapshots_dict = {}
            output = aws_get_manual_database_snapshots(handle=handle, region=r)
            snapshots_dict["region"]=r
            snapshots_dict["snapshot"]=output
            manual_snapshots_list.append(snapshots_dict)
    except Exception as error:
        pass
    for all_snapshots in manual_snapshots_list:
        try:
            ec2Client = handle.client('rds', region_name=all_snapshots['region'])
            for each_snapshot in all_snapshots['snapshot']:
                p_dict={}
                response = ec2Client.describe_db_snapshot_attributes(DBSnapshotIdentifier=each_snapshot)
                db_attribute = response["DBSnapshotAttributesResult"]
                for value in db_attribute['DBSnapshotAttributes']:
                    if "all" in value["AttributeValues"]:
                        public_snapshots.append(db_attribute['DBSnapshotIdentifier'])
                        p_dict["region"] = all_snapshots['region']
                        p_dict["open_snapshot"] = public_snapshots
                        result = [*result, p_dict]
        except Exception as e:
            pass
    execution_flag = False
    if len(result) > 0:
        execution_flag = True
    output = (execution_flag, result)
    return output


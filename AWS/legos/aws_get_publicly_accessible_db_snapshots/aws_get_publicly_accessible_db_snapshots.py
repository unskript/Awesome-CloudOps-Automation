##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.utils import CheckOutput
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_filter_all_manual_database_snapshots.aws_filter_all_manual_database_snapshots import aws_filter_all_manual_database_snapshots


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Region of the RDS'
    )


def aws_get_publicly_accessible_db_snapshots_printer(output):
    if output is None:
        return
    if isinstance(output, CheckOutput):
        print(output.json())
    else:
        pprint.pprint(output)


def aws_get_publicly_accessible_db_snapshots(handle, region: str=None) -> Tuple:
    """aws_get_publicly_accessible_db_snapshots lists of publicly accessible
       db_snapshot_identifier.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the RDS.

        :rtype: Object with status, result having publicly accessible Snapshots 
        Identifier in RDS, error
    """
    manual_snapshots_list=[]
    result=[]
    all_regions = [region]
    if region is None or not region:
        all_regions = aws_list_all_regions(handle=handle)
    try:
        for r in all_regions:
            snapshots_dict = {}
            output = aws_filter_all_manual_database_snapshots(handle=handle, region=r)
            snapshots_dict["region"]=r
            snapshots_dict["snapshot"]=output
            manual_snapshots_list.append(snapshots_dict)
    except Exception as e:
        raise e

    for all_snapshots in manual_snapshots_list:
        try:
            ec2Client = handle.client('rds', region_name=all_snapshots['region'])
            for each_snapshot in all_snapshots['snapshot']:
                response = ec2Client.describe_db_snapshot_attributes(
                    DBSnapshotIdentifier=each_snapshot
                    )
                db_attribute = response["DBSnapshotAttributesResult"]
                for value in db_attribute['DBSnapshotAttributes']:
                    p_dict={}
                    if "all" in value["AttributeValues"]:
                        p_dict["region"] = all_snapshots['region']
                        p_dict["open_snapshot"] = db_attribute['DBSnapshotIdentifier']
                        result.append(p_dict)
        except Exception:
            pass
    if len(result)!=0:
        return (False, result)
    return (True, [])

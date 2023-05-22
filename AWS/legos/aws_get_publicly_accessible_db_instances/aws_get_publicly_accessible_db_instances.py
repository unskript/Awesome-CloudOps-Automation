##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.utils import CheckOutput
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '',
        title='Region for RDS',
        description='Region of the RDS.'
    )


def aws_get_publicly_accessible_db_instances_printer(output):
    if output is None:
        return

    if isinstance(output, CheckOutput):
        print(output.json())
    else:
        pprint.pprint(output)


def aws_get_publicly_accessible_db_instances(handle, region: str = "") -> Tuple:
    """aws_get_publicly_accessible_db_instances Gets all publicly accessible DB instances

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the RDS.

        :rtype: CheckOutput with status result and list of publicly accessible RDS instances.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            ec2Client = handle.client('rds', region_name=reg)
            response = aws_get_paginator(ec2Client, "describe_db_instances", "DBInstances")
            for db in response:
                db_instance_dict = {}
                if db['PubliclyAccessible']:
                    db_instance_dict["region"] = reg
                    db_instance_dict["instance"] = db['DBInstanceIdentifier']
                    result.append(db_instance_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

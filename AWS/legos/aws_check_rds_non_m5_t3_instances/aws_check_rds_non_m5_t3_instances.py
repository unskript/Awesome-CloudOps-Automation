##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '',
        title='AWS Region',
        description='AWS Region.'
    )


def aws_check_rds_non_m5_t3_instances_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_check_rds_non_m5_t3_instances(handle, region: str = "") -> Tuple:
    """aws_check_rds_non_m5_t3_instances Gets all DB instances that are not m5 or t3.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :rtype: A tuple with a status flag and a list of DB instances that are not m5 or t3.
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
                if db['DBInstanceClass'][3:5] not in ['m5', 't3']:
                    db_instance_dict["region"] = reg
                    db_instance_dict["instance"] = db['DBInstanceIdentifier']
                    result.append(db_instance_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
    
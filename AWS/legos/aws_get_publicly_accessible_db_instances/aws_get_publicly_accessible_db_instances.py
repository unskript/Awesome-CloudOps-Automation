##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='Region for RDS',
        description='Region of the RDS.'
    )


def aws_publicly_accessible_db_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_publicly_accessible_db_instances(handle, region: str = "") -> Tuple:
    """aws_list_apllication_loadbalancers lists application loadbalancers ARNs.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the RDS.

        :rtype: List with publicly accessible RDS instances.
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
        except Exception as error:
            pass
    execution_flag = False
    if len(result) > 0:
        execution_flag = True
    output = (execution_flag, result)
    return output
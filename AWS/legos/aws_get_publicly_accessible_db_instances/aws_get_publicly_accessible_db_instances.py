##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region for RDS',
        description='Region of the RDS.'
    )


def aws_publicly_accessible_db_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_publicly_accessible_db_instances(handle, region: str) -> List:
    """aws_list_apllication_loadbalancers lists application loadbalancers ARNs.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the RDS.

        :rtype: List with publicly accessible RDS instances.
    """

    ec2Client = handle.client('rds', region_name=region)
    result = []
    try:
        response = aws_get_paginator(ec2Client, "describe_db_instances", "DBInstances")
        for db in response:
            if db['PubliclyAccessible']:
                result.append(db['DBInstanceIdentifier'])
    except Exception as error:
        result.append(error)
    return result
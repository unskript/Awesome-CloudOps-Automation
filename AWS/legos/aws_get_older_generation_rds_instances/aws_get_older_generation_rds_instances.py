##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field('', description='AWS Region.', title='AWS Region')



def aws_get_older_generation_rds_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def is_previous_gen_instance(instance_type):
    previous_gen_instance_types = ['db.m1', 'db.m2', 'db.t1']
    for prev_gen_type in previous_gen_instance_types:
        if instance_type.startswith(prev_gen_type):
            return True
    return False


def aws_get_older_generation_rds_instances(handle, region: str = "") -> Tuple:
    """aws_get_older_generation_rds_instances Gets all older generation RDS DB instances

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Optional, Region of the RDS.

        :rtype: Status, List of old RDS Instances
    """
    if not handle or (region and region not in aws_list_all_regions(handle)):
        raise ValueError("Invalid input parameters provided.")
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            ec2Client = handle.client('rds', region_name=reg)
            response = aws_get_paginator(ec2Client, "describe_db_instances", "DBInstances")
            for db in response:
                instance_type = ".".join(db['DBInstanceClass'].split(".", 2)[:2])
                response = is_previous_gen_instance(instance_type)
                if response:
                    db_instance_dict = {}
                    db_instance_dict["region"] = reg
                    db_instance_dict["instance"] = db['DBInstanceIdentifier']
                    result.append(db_instance_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
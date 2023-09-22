##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from tabulate import tabulate
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime,timedelta, timezone
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions

class InputSchema(BaseModel):
    region: Optional[str] = Field('', description='AWS Region.', title='AWS Region')
    threshold: Optional[float] = Field(
        10,
        description='Threshold(in days) to find long running RDS instances. Eg: 30, This will find all the instances that have been created a month ago.',
        title='Threshold(in days)',
    )

def aws_get_long_running_rds_instances_without_reserved_instances_printer(output):
    if output is None:
        print("Output is None.")
        return
    status, res = output
    if status:
        print("There are no DB instances that have been running for longer than the specified threshold and do not have corresponding reserved instances.")
    else:
        print("DB instances that have been running for longer than the specified threshold and do not have corresponding reserved instances:")
        table_data = [[item['region'], item['instance_type'], item['instance']] for item in res]
        headers = ['Region', 'Instance Type', 'Instance']
        table = tabulate(table_data, headers=headers, tablefmt='grid')
        print(table)


def aws_get_long_running_rds_instances_without_reserved_instances(handle, region: str = "", threshold: float = 10.0) -> Tuple:
    """aws_get_long_running_rds_instances_without_reserved_instances Gets all DB instances that have been running for longer than the specified threshold and do not have corresponding reserved instances.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type region: string
    :param region: AWS Region.

    :type threshold: int
    :param threshold: Threshold(in days) to find long running RDS instances. Eg: 30, This will find all the instances that have been created a month ago.

    :rtype: A tuple with a Status,and list of DB instances that don't have reserved instances
    """
    result = []
    all_regions = [region]
    reservedInstancesPerRegion = {}
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            rdsClient = handle.client('rds', region_name=reg)
            response = rdsClient.describe_reserved_db_instances()
            reservedInstancesPerType = {}
            if 'ReservedDBInstances' in response:
                for ins in response['ReservedDBInstances']:
                    reservedInstancesPerType[ins['DBInstanceClass']] = True
            reservedInstancesPerRegion[reg] = reservedInstancesPerType
        except Exception:
            pass
    for reg in all_regions:
        try:
            rdsClient = handle.client('rds', region_name=reg)
            response = aws_get_paginator(rdsClient, "describe_db_instances", "DBInstances")
            for instance in response:
                if instance['DBInstanceStatus'] == 'available':
                    # Check for existence of keys before using them
                    if 'InstanceCreateTime' in instance and 'DBInstanceClass' in instance:
                        uptime = datetime.now(timezone.utc) - instance['InstanceCreateTime']
                        if uptime > timedelta(days=threshold):
                            # Check if the DB instance type is present in the reservedInstancesPerRegion map.
                            reservedInstances = reservedInstancesPerRegion.get(reg, {})
                            if not reservedInstances.get(instance['DBInstanceClass']):
                                db_instance_dict = {
                                    "region": reg,
                                    "instance_type": instance['DBInstanceClass'],
                                    "instance": instance['DBInstanceIdentifier']
                                }
                                result.append(db_instance_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
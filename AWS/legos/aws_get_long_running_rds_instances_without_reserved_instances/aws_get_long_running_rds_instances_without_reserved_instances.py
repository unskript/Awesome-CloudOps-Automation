##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
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
        return
    pprint.pprint(output)

def aws_get_long_running_rds_instances_without_reserved_instances(handle, region: str = "", threshold:int=10) -> Tuple:
    """aws_get_long_running_rds_instances_without_reserved_instances Gets all DB instances that are not m5 or t3.

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
            response = rdsClient.describe_reserved_nodes()
            reservedInstancesPerType = {}
            if response['ReservedDBInstances']:
                for ins in response['ReservedDBInstances']:
                    reservedInstancesPerRegion[ins['DBInstanceClass']] = True
            else:
                continue
            reservedInstancesPerRegion[reg] = reservedInstancesPerType
        except Exception:
            pass
    for reg in all_regions:
        try:
            rdsClient = handle.client('rds', region_name=reg)
            response = aws_get_paginator(rdsClient, "describe_db_instances", "DBInstances")
            for instance in response:
                if instance['DBInstanceStatus'] == 'available':
                        uptime = datetime.now(timezone.utc) - instance['InstanceCreateTime']
                        if uptime > timedelta(days=threshold):
                            # Check if the cluster node type is present in the reservedInstancesPerRegion map.
                            reservedInstances = reservedInstancesPerRegion.get(reg)
                            if reservedInstances is not None:
                                if reservedInstances.get(instance['DBInstanceClass']) is True:
                                    continue
                            db_instance_dict = {}
                            db_instance_dict["region"] = reg
                            db_instance_dict["instance_type"] = instance['DBInstanceClass']
                            db_instance_dict["instance"] = instance['DBInstanceIdentifier']
                            result.append(db_instance_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)



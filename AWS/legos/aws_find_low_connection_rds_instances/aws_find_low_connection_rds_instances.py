##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import datetime
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default='',
        title='Region for RDS',
        description='Region of the RDS.'
    )
    min_connections: Optional[int] = Field(
        default=10,
        title='Minimum Number of Connections',
        description='The minimum number of connections for an instance to be considered active.'
    )


def aws_find_low_connection_rds_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_low_connection_rds_instances(handle, min_connections:int = 10, region: str = "") -> Tuple:
    """aws_find_low_connection_rds_instances Gets information about RDS instances.

        :type region: string
        :param region: AWS Region.

        :type min_connections: int
        :param min_connections: The minimum number of connections for an instance to be considered active.

        :rtype: A list containing information about RDS instances.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            rds_Client = handle.client('rds', region_name=reg)
            cloudwatch = handle.client('cloudwatch', region_name=reg)
            response = aws_get_paginator(rds_Client, "describe_db_instances", "DBInstances")
            for db in response:
                db_instance_dict = {}
                db_instance_identifier = db['DBInstanceIdentifier']
                end_time = datetime.datetime.now()
                start_time = end_time - datetime.timedelta(days=1)
                response1 = cloudwatch.get_metric_statistics(
                    Namespace='AWS/RDS',
                    MetricName='DatabaseConnections',
                    Dimensions=[
                        {
                            'Name': 'DBInstanceIdentifier',
                            'Value': db_instance_identifier
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86460,
                    Statistics=['Sum']
                )
                data_points = response1['Datapoints']
                if data_points:
                    connections = data_points[-1]['Sum']
                    if connections < min_connections:
                        db_instance_dict["region"] = reg
                        db_instance_dict["db_instance"] = db_instance_identifier
                        db_instance_dict["connections"] = int(connections)
                        result.append(db_instance_dict)
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
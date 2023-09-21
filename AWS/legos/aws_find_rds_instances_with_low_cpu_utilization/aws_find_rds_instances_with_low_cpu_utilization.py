##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint
from datetime import datetime,timedelta


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', description='AWS Region to get the RDS Instance', title='AWS Region'
    )
    duration_minutes: Optional[int] = Field(
        5,
        description='Value in minutes to get the start time of the metrics for CPU Utilization',
        title='Duration of Start time',
    )
    utilization_threshold: Optional[int] = Field(
        10,
        description='The threshold percentage of CPU utilization for an RDS Instance.',
        title='CPU Utilization Threshold',
    )



def aws_find_rds_instances_with_low_cpu_utilization_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_rds_instances_with_low_cpu_utilization(handle, utilization_threshold:int=10, region: str = "", duration_minutes:int=5) -> Tuple:
    """aws_find_rds_instances_with_low_cpu_utilization finds RDS instances that have a lower cpu utlization than the given threshold

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the RDS.

        :type utilization_threshold: integer
        :param utilization_threshold: The threshold percentage of CPU utilization for an RDS Instance.

        :type duration_minutes: integer
        :param duration_minutes: Value in minutes to get the start time of the metrics for CPU Utilization

        :rtype: status, list of instances and their region.
    """
    if not handle or utilization_threshold < 0 or utilization_threshold > 100 or duration_minutes <= 0:
        raise ValueError("Invalid input parameters provided.")
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            rdsClient = handle.client('rds', region_name=reg)
            cloudwatchClient = handle.client('cloudwatch', region_name=reg)
            all_instances = aws_get_paginator(rdsClient, "describe_db_instances", "DBInstances")
            for db in all_instances:
                response = cloudwatchClient.get_metric_data(
                    MetricDataQueries=[
                        {
                            'Id': 'cpu',
                            'MetricStat': {
                                'Metric': {
                                    'Namespace': 'AWS/RDS',
                                    'MetricName': 'CPUUtilization',
                                    'Dimensions': [
                                        {
                                            'Name': 'DBInstanceIdentifier',
                                            'Value': db['DBInstanceIdentifier']
                                        },
                                    ]
                                },
                                'Period': 60,
                                'Stat': 'Average',
                            },
                            'ReturnData': True,
                        },
                    ],
                    StartTime=(datetime.now() - timedelta(minutes=duration_minutes)).isoformat(),
                    EndTime=datetime.utcnow().isoformat(),
                )
                if 'Values' in response['MetricDataResults'][0]:
                    cpu_utilization = response['MetricDataResults'][0]['Values'][0]
                    if cpu_utilization < utilization_threshold:
                        db_instance_dict = {}
                        db_instance_dict["region"] = reg
                        db_instance_dict["instance"] = db['DBInstanceIdentifier']
                        result.append(db_instance_dict)
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
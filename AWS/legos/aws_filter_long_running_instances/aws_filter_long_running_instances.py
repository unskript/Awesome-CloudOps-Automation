##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pytz


class InputSchema(BaseModel):
    threshold: int = Field(
        default=30,
        title="Threshold (in day's)",
        description="(in day's) The threshold to check the instances older than the threshold.")
    region: str = Field(
        title='Region',
        description='AWS Region')


def aws_filter_long_running_instances_printer(output):
    if output is None:
        return
    pprint.pprint({"Instances": output})


def aws_filter_long_running_instances(handle, region: str, threshold: int = 10) -> List:
    """aws_filter_long_running_instances Returns an array of long running EC2 instances.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type region: string
        :param region: EC2 instance region.

        :type threshold: string
        :param threshold: (in days) The threshold to check the instances older than the threshold.

        :rtype: Array of long running EC2 instances.
    """
    result = []
    current_time = datetime.now(pytz.UTC)
    ec2Client = handle.client('ec2', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
    for reservation in res:
        for instance in reservation['Instances']:
            launch_time = instance["LaunchTime"]
            running_time = current_time - launch_time
            if running_time > timedelta(days=int(threshold)):
                result.append(instance['InstanceId'])
    return result

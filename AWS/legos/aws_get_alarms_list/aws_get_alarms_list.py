##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List
import pprint

from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the cloudwatch.')
    alarm_name: Optional[str] = Field(
        title='Alarm Name',
        description='Name of the particular alarm in the cloudwatch.')


def aws_get_alarms_list_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_alarms_list(handle, region: str, alarm_name: str = None) -> List:
    """aws_get_alarms_list get AWS cloudwatches alarms list.
       for a given instance ID. This routine assume instance_id
       being present in the inputParmsJson.

       :type handle: object
       :param handle: Object returned from task.validate(...).

       :type alarm_name: string
       :param alarm_name: Name of the particular alarm in the cloudwatch.

       :type region: string
       :param region: AWS Region of the cloudwatch.

       :rtype: Returns alarms dict list and next token if pagination requested.
    """
    # Input param validation.
    cloudwatchClient = handle.client('cloudwatch', region_name=region)
    result = []
    # if alarm is specified it's returning only it's details
    if alarm_name is not None:
        res = aws_get_paginator(cloudwatchClient, "describe_alarms", "MetricAlarms", AlarmNames=[alarm_name])
    else:
        res = aws_get_paginator(cloudwatchClient, "describe_alarms", "MetricAlarms")

    for alarm in res:
        alarm_info = {}
        alarm_info['AlarmName'] = alarm['AlarmName']
        alarm_info['AlarmArn'] = alarm['AlarmArn']
        alarm_info['Dimensions'] = alarm['Dimensions']
        if 'AlarmDescription' in alarm:
            alarm_info['AlarmDescription'] = alarm['AlarmDescription']
        else:
            alarm_info['AlarmDescription'] = ""
        result.append(alarm_info)

    return result

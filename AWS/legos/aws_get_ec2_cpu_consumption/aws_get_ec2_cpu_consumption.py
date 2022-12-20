##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
## written by Doug Sillars with the aid of ChatGPT
##read the blog https://unskript.com/will-ai-replace-us-using-chatgpt-to-create-python-actions-for-unskript/
##
from typing import List, Dict
from pydantic import BaseModel, Field
import pprint
from datetime import datetime, timezone, timedelta
from unskript.connectors.aws import aws_get_paginator

from beartype import beartype
@beartype
def aws_get_ec2_CPU_averagev2_printer(output):
    if output is None:
        return
    pprint.pprint(output)

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service')

@beartype
def aws_get_ec2_CPU_averagev2(handle, region: str) -> Dict:


    ec2Client = handle.client('ec2', region_name=region)
    cw= handle.client('cloudwatch', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")

    # Get the current time and the time 24 hours ago
    now = datetime.now()
    yesterday = now - timedelta(hours=24)

    # Set the start and end times for the data to retrieve
    start_time = yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    results={}
    # Iterate through the list of instances
    for reservation in res:
        for instance in reservation['Instances']:
                # Get the instance ID and launch time
                instance_id = instance['InstanceId']
                # Get the average CPU usage for the last 24 hours
                response = cw.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': instance_id
                        },
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,
                    Statistics=['Average']
                )
                
                # Calculate the average CPU usage for the past 24 hours
                #error check for the presence of CPU  usage data
                if len(response['Datapoints'])>0:               
                    cpu_utilization_values = [datapoint['Average'] for datapoint in response['Datapoints']]
                    avg_cpu_utilization = sum(cpu_utilization_values) / len(cpu_utilization_values)
                    results[instance_id] = avg_cpu_utilization
                else:
                    results[instance_id] = "error"
    return(results)

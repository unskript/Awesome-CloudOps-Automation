##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
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
def aws_get_ec2_instance_age_printer(output):
    if output is None:
        return
    pprint.pprint(output)


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service')



@beartype
def aws_get_ec2_instance_age(handle, region: str) -> Dict:


    ec2Client = handle.client('ec2', region_name=region)
    cloudwatch= handle.client('cloudwatch', region_name=region)
    res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")

   # Set the desired time range for the data traffic metrics
    time_range = {
        'StartTime': datetime.utcnow() - timedelta(hours=1),
        'EndTime': datetime.utcnow()
    }
    result={}
        # Iterate through the list of instances
    for reservation in res:
        for instance in reservation['Instances']:
                # Get the instance ID and launch time
                instance_id = instance['InstanceId']
                # Set the desired dimensions for the data traffic metrics
                dimensions = [
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ]

                # Get the data traffic in and out metrics for all EC2 instances
                metrics = cloudwatch.get_metric_data(
                    MetricDataQueries=[
                        {
                            'Id': 'm1',
                            'MetricStat': {
                                'Metric': {
                                    'Namespace': 'AWS/EC2',
                                    'MetricName': 'NetworkIn',
                                    'Dimensions': dimensions
                                },
                                'Period': 3600,
                                'Stat': 'Sum',
                                'Unit': 'Bytes'
                            }
                        },
                        {
                            'Id': 'm2',
                            'MetricStat': {
                                'Metric': {
                                    'Namespace': 'AWS/EC2',
                                    'MetricName': 'NetworkOut',
                                    'Dimensions': dimensions
                                },
                                'Period': 3600,
                                'Stat': 'Sum',
                                'Unit': 'Bytes'
                            }
                        }
                    ],
                    StartTime=time_range['StartTime'],
                    EndTime=time_range['EndTime']
                )
                #bytes dont mean anything.  Lets use MB

                if len(metrics['MetricDataResults'][0]['Values'])>0:
                    NetworkInMB = round(float(metrics['MetricDataResults'][0]['Values'][0])/1024/1024,2)
                else:
                    NetworkInMB = "error"
                if len(metrics['MetricDataResults'][1]['Values'])>0:    
                    NetworkOutMB = round(float(metrics['MetricDataResults'][1]['Values'][0])/1024/1024,2)
                else:
                    NetworkOutMB = "error"
                metricsIwant = {metrics['MetricDataResults'][0]['Label'] : NetworkInMB, metrics['MetricDataResults'][1]['Label'] : NetworkOutMB}
                result[instance_id] = metricsIwant

    return(result)
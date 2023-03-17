##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import pprint

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region.')
    number_of_days: int = Field(
        title="Number of Day's",
        description='Number of days to check the Datapoints.')
    

def aws_filter_unused_nat_gateway_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def is_nat_gateway_used(handle, nat_gateway_id, start_time, end_time):
    datapoints = []
    while start_time < end_time:
        response = handle.get_metric_statistics(
            Namespace='AWS/NATGateway',
            MetricName='BytesOutFromEndpoint',
            Dimensions=[
                {
                    'Name': 'NatGatewayId',
                    'Value': nat_gateway_id
                }
            ],
            StartTime=start_time,
            EndTime=min(start_time + timedelta(days=14), end_time),
            Period=900,
            Statistics=[
                'Sum'
            ]
        )
        datapoints += response['Datapoints']
        start_time += timedelta(days=14)
    if len(datapoints) == 0:
        return False
    sum_bytes_out = sum([dp['Sum'] for dp in datapoints])
    return sum_bytes_out > 0


def aws_filter_unused_nat_gateway(handle, number_of_days: int, region: str) -> List:
    """aws_get_natgateway_by_vpc Returns an array of NAT gateways.

        :type region: string
        :param region: Region to filter NAT Gateways.

        :type number_of_days: int
        :param number_of_days: Number of days to check the Datapoints.

        :rtype: Array of NAT gateways.
    """
    result = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=number_of_days)
    try:
        ec2Client = handle.client('ec2', region_name=region)
        cloudwatch = handle.client('cloudwatch', region_name=region)
        response = ec2Client.describe_nat_gateways()
        for nat_gateway in response['NatGateways']:
            if not is_nat_gateway_used(cloudwatch, nat_gateway['NatGatewayId'], start_time, end_time):
                result.append(nat_gateway['NatGatewayId'])
    except Exception as e:
        pass

    return result
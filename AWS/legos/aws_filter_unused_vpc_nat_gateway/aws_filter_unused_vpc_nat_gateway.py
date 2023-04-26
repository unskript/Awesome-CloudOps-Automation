##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region.')
    number_of_days: Optional[int] = Field(
        default=7,
        title="Number of Days",
        description='Number of days to check the Datapoints.')
    

def aws_filter_unused_vpc_nat_gateway_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def is_nat_gateway_used(handle, nat_gateway, start_time, end_time):
    datapoints = []
    if nat_gateway['State'] != 'deleted':
        # Get the metrics data for the specified NAT Gateway over the last 7 days
        metrics_data = handle.get_metric_statistics(
            Namespace='AWS/NATGateway',
            MetricName='BytesIn',
            Dimensions=[
                {
                    'Name': 'NatGatewayId',
                    'Value': nat_gateway['NatGatewayId']
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Sum']
        )
        datapoints += metrics_data['Datapoints']
    if len(datapoints) == 0 or metrics_data['Datapoints'][0]['Sum']:
        return False
    else:
        return True


def aws_filter_unused_vpc_nat_gateway(handle, number_of_days: int = 7, region: str = "") -> Tuple:
    """aws_filter_unused_vpc_nat_gateway Returns an array of VPC NAT gateways.

        :type region: string
        :param region: Region to filter NAT Gateways.

        :type number_of_days: int
        :param number_of_days: Number of days to check the Datapoints.

        :rtype: Array of VPC NAT gateways.
    """
    result = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=number_of_days)
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=reg)
            cloudwatch = handle.client('cloudwatch', region_name=reg)
            vpc_response = aws_get_paginator(ec2Client, "describe_vpcs", "Vpcs")
            for vpc in vpc_response:
                vpc_id = vpc['VpcId']
                nat_gateways = ec2Client.describe_nat_gateways(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
                for nat_gateway in nat_gateways['NatGateways']:
                    if not is_nat_gateway_used(cloudwatch, nat_gateway, start_time, end_time):
                        result.append({"nat_gateway": nat_gateway['NatGatewayId'], "vpc_id": vpc_id, "region": reg})
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)

##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region.')
    number_of_days: Optional[int] = Field(
        title="Number of Days",
        description='Number of days to check the Datapoints.')


def aws_filter_unused_nat_gateway_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def is_nat_gateway_used(handle, nat_gateway, start_time, end_time,number_of_days):
    datapoints = []
    if nat_gateway['State'] != 'deleted':
        # Get the metrics data for the specified NAT Gateway over the last 7 days
        metrics_data = handle.get_metric_statistics(
            Namespace='AWS/NATGateway',
            MetricName='ActiveConnectionCount',
            Dimensions=[
                {
                    'Name': 'NatGatewayId',
                    'Value': nat_gateway['NatGatewayId']
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400*number_of_days,
            Statistics=['Sum']
        )
        datapoints += metrics_data['Datapoints']
    if len(datapoints) == 0 or metrics_data['Datapoints'][0]['Sum']==0:
        return False
    return True



def aws_filter_unused_nat_gateway(handle, number_of_days: int = 7, region: str = "") -> Tuple:
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
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=reg)
            cloudwatch = handle.client('cloudwatch', region_name=reg)
            response = ec2Client.describe_nat_gateways()
            for nat_gateway in response['NatGateways']:
                nat_gateway_info = {}
                if not is_nat_gateway_used(cloudwatch, nat_gateway, start_time, end_time,number_of_days):
                    nat_gateway_info["nat_gateway_id"] = nat_gateway['NatGatewayId']
                    nat_gateway_info["reg"] = reg
                    result.append(nat_gateway_info)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

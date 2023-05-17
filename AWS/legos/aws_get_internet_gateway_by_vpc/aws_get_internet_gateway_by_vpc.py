##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator

class InputSchema(BaseModel):
    vpc_id: str = Field(
        title='VPC ID',
        description='VPC ID of the Instance.')
    region: str = Field(
        title='Region',
        description='AWS Region.')

def aws_get_internet_gateway_by_vpc_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_get_internet_gateway_by_vpc(handle, vpc_id: str, region: str) -> List:
    """aws_get_internet_gateway_by_vpc Returns an List of internet Gateway.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type vpc_id: str
        :param vpc_id: VPC ID to find Internet Gateway.

        :type region: str
        :param region: Region to filter instance.

        :rtype: List of Internet Gateway.
    """

    ec2Client = handle.client('ec2', region_name=region)
    result = []
    try:
        response = aws_get_paginator(ec2Client, "describe_internet_gateways", "InternetGateways",
                                Filters=[{'Name': 'attachment.vpc-id','Values': [vpc_id]}])
        for nat_info in response:
            if "InternetGatewayId" in nat_info:
                result.append(nat_info["InternetGatewayId"])

    except Exception as error:
        result.append({"error":error})

    return result

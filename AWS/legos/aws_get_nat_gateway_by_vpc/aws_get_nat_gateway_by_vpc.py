##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    vpc_id: str = Field(
        title='VPC ID',
        description='VPC ID of the Instance.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_get_natgateway_by_vpc_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_natgateway_by_vpc(handle, vpc_id: str, region: str) -> Dict:
    """aws_get_natgateway_by_vpc Returns an Dict of NAT Gateway info.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type vpc_id: str
        :param vpc_id: VPC ID to find NAT Gateway.

        :type region: str
        :param region: Region to filter instance.

        :rtype: Dict of NAT Gateway info.
    """

    ec2Client = handle.client('ec2', region_name=region)
    result = {}
    try:
        response = aws_get_paginator(ec2Client, "describe_nat_gateways", "NatGateways",
                                Filters=[{'Name': 'vpc-id','Values': [vpc_id]}])
        for nat_info in response:
            if "NatGatewayId" in nat_info:
                result["NatGatewayId"] = nat_info["NatGatewayId"]
            if "State" in nat_info:
                result["State"] = nat_info["State"]
            if "SubnetId" in nat_info:
                result["SubnetId"] = nat_info["SubnetId"]
    except Exception as error:
        result["error"] = error

    return result

    
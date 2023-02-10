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


def aws_get_nat_gateway_by_vpc_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_nat_gateway_by_vpc(handle, vpc_id: str, region: str) -> List:
    """aws_get_natgateway_by_vpc Returns an array of NAT gateways.

        :type region: string
        :param region: Region to filter instances.

        :type vpc_id: string
        :param vpc_id: ID of the Virtual Private Cloud (VPC)

        :rtype: Array of NAT gateways.
    """
    result = []
    try:
        ec2Client = handle.client('ec2', region_name=region)
        response = ec2Client.describe_nat_gateways(
            Filter=[{'Name': 'vpc-id','Values': [vpc_id]}])
        if response['NatGateways']:
            for i in response['NatGateways']:
                nat_dict = {}
                if "NatGatewayId" in i:
                    nat_dict["nat_id"] = i["NatGatewayId"]
                if "SubnetId" in i:
                    nat_dict["subnet_id"] = i["SubnetId"]
                if "VpcId" in i:
                    nat_dict["vpc_id"] = i["VpcId"]
                for address in i["NatGatewayAddresses"]:
                    if "PrivateIp" in address:
                        nat_dict["private_ip"] = address["PrivateIp"]
                    if "PublicIp" in address:
                        nat_dict["public_ip"] = address["PublicIp"]
                result.append(nat_dict)
    except Exception as e:
        pass
    return result

    

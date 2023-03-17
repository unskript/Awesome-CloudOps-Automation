##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region.')


def aws_get_private_address_from_nat_gateways_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_private_address_from_nat_gateways(handle, region: str = "") -> Tuple:
    """aws_get_private_address_from_nat_gateways Returns an private address of NAT gateways.

        :type region: string
        :param region: Region to filter NAT Gateways.

        :rtype: Tuple with private address of NAT gateways.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=reg)
            response = aws_get_paginator(ec2Client, "describe_nat_gateways", "NatGateways")
            for i in response:
                nat_dict = {}
                nat_dict["nat_id"] = i["NatGatewayId"]
                nat_dict["vpc_id"] = i["VpcId"]
                nat_dict["region"] = reg
                for address in i["NatGatewayAddresses"]:
                    if "PrivateIp" in address:
                        nat_dict["private_ip"] = address["PrivateIp"]
                result.append(nat_dict)
        except Exception as e:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)

    
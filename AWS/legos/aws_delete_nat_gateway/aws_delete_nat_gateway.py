##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Dict
import pprint


class InputSchema(BaseModel):
    nat_gateway_id: str = Field(
        title='NAT Gateway ID',
        description='ID of the NAT Gateway.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_delete_nat_gateway_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_nat_gateway(handle, nat_gateway_id: str, region: str) -> Dict:
    """aws_delete_nat_gateway Returns an dict of NAT gateways information.

        :type region: string
        :param region: AWS Region.

        :type nat_gateway_id: string
        :param nat_gateway_id: ID of the NAT Gateway.

        :rtype: dict of NAT gateways information.
    """
    try:
        ec2Client = handle.client('ec2', region_name=region)
        response = ec2Client.delete_nat_gateway(NatGatewayId=nat_gateway_id)
        return response
    except Exception as e:
        raise Exception(e)

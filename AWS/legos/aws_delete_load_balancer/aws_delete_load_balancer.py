##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint


class InputSchema(BaseModel):
    elb_arn: Optional[str] = Field(
        title='Load Balancer ARN (ALB/NLB type)',
        description='Load Balancer ARN of the ALB/NLB type Load Balancer.'
        )
    region: str = Field(
        title='Region',
        description='AWS Region.'
        )


def aws_delete_load_balancer_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_load_balancer(handle, region: str, elb_arn: str="", elb_name:str="") -> Dict:
    """aws_delete_load_balancer dict of loadbalancers info.

        :type region: string
        :param region: AWS Region.

        :type elb_arn: string
        :param elb_arn: load balancer ARNs.

        :rtype: dict of load balancers info.
    """
    try:
        elbv2Client = handle.client('elbv2', region_name=region)
        response = elbv2Client.delete_load_balancer(LoadBalancerArn=elb_arn)
        return response
    except Exception as e:
        raise Exception(e)
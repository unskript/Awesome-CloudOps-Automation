##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region')
    nlb_arn: str = Field(
        title='Network Loadbalancer ARNs',
        description='Network Load Balancer ARNs.')


def aws_get_nlb_targets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_nlb_targets(handle, region: str, nlb_arn: str) -> List:
    """aws_get_nlb_targets lists Network loadbalancers target details.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :type nlb_arn: string
        :param nlb_arn: Network Load Balancer ARNs.

        :rtype: List Network load balancers target details.
    """
    result = []
    try:
        elb_Client = handle.client('elbv2', region_name=region)
        response = elb_Client.describe_target_health(TargetGroupArn=nlb_arn)
        for target in response['TargetHealthDescriptions']:
            target_dict = {}
            target_dict["target_id"] = target['Target']['Id']
            target_dict["target_port"] = target['Target']['Port']
            target_dict["target_health"] = target['TargetHealth']['State']
            result.append(target_dict)
    except Exception as e:
        raise Exception(e) from e
    return result

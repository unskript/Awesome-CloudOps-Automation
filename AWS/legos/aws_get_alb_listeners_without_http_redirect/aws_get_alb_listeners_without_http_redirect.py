##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import List, Dict
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    loadbalancer_arn: list = Field(
        title='LoadBalancerArn',
        description='List of LoadBalancerArn.')

    region: str = Field(
        title='Region',
        description='AWS Region of the ALB listeners.')


def aws_listeners_without_http_redirect_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_listeners_without_http_redirect(handle, loadbalancer_arn: list, region: str) -> List:
    """aws_get_auto_scaling_instances List of Dict with instanceId and attached groups.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type loadbalancer_arn: list
        :param loadbalancer_arn: List of LoadBalancerArn.

        :type region: string
        :param region: Region to filter ALB listeners.

        :rtype: List of ALB listeners without HTTP redirection.
    """
    ec2Client = handle.client('elbv2', region_name=region)
    result = []
    for alb in loadbalancer_arn:
        try:
            response = aws_get_paginator(ec2Client, "describe_listeners", "Listeners",
                                         LoadBalancerArn=alb)
            for listner in response:
                if 'SslPolicy' not in listner:
                    resp = aws_get_paginator(ec2Client, "describe_rules", "Rules",
                                         ListenerArn=listner['ListenerArn'])
                    for rule in resp:
                        for action in rule['Actions']:
                            if action['Type'] != 'redirect':
                                result.append(listner['ListenerArn'])
        except Exception as error:
            result.append(error)
    return result



    
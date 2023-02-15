##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.legos.aws.aws_list_application_loadbalancers.aws_list_application_loadbalancers import aws_list_application_loadbalancers
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region of the ALB listeners.')


def aws_listeners_without_http_redirect_printer(output):
    if output is None:
        return
        
    pprint.pprint(output)


def aws_listeners_without_http_redirect(handle, region: str = "") -> Tuple:
    """aws_listeners_without_http_redirect List of ALB listeners without HTTP redirection.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region to filter ALB listeners.

        :rtype: Tuple of status result and list of ALB listeners without HTTP redirection.
    """
    result = []
    all_regions = [region]
    alb_list = []
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            alb_dict = {}
            loadbalancer_arn = aws_list_application_loadbalancers(handle, reg)
            alb_dict["region"] = reg
            alb_dict["alb_arn"] = loadbalancer_arn
            alb_list.append(alb_dict)
        except Exception as error:
            pass
        
    for alb in alb_list:
        try:
            ec2Client = handle.client('elbv2', region_name=alb["region"])
            for load in alb["alb_arn"]:
                response = aws_get_paginator(ec2Client, "describe_listeners", "Listeners",
                                             LoadBalancerArn=load)
                for listner in response:
                    if 'SslPolicy' not in listner:
                        resp = aws_get_paginator(ec2Client, "describe_rules", "Rules",
                                             ListenerArn=listner['ListenerArn'])
                        for rule in resp:
                            for action in rule['Actions']:
                                listener_dict = {}
                                if action['Type'] != 'redirect':
                                    listener_dict["region"] = alb["region"]
                                    listener_dict["listener_arn"] = listner['ListenerArn']
                                    result.append(listener_dict)
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, [])
    

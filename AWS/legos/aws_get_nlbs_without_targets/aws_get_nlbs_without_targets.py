##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default='',
        title='AWS Region',
        description='AWS Region')


def aws_get_nlbs_without_targets_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_nlbs_without_targets(handle, region: str = "") -> Tuple:
    """aws_get_nlbs_without_targets lists Network loadbalancers ARNs without targets.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :rtype: lists Network loadbalancers ARNs without targets.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            elbv2_client = handle.client('elbv2', region_name=reg)
            resp = aws_get_paginator(elbv2_client, "describe_load_balancers", "LoadBalancers")
            for elb in resp:
                nlb_dict = {}
                if elb['Type'] == "network":
                    target_groups = elbv2_client.describe_target_groups(
                        LoadBalancerArn=elb['LoadBalancerArn']
                        )
                    if len(target_groups['TargetGroups']) == 0:
                        nlb_dict["loadBalancer_arn"] = elb['LoadBalancerArn']
                        nlb_dict["loadBalancer_name"] = elb["LoadBalancerName"]
                        nlb_dict["region"] = reg
                        result.append(nlb_dict)
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    return (True, None)

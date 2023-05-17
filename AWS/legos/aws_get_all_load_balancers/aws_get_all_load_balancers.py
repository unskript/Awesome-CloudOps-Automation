##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='AWS Region',
        description='AWS Region.'
    )


def aws_get_all_load_balancers_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_all_load_balancers(handle, region: str = "") -> List:
    """aws_get_all_load_balancers Returns an list of load balancer details.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :rtype: List of load balancer details.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            elb_Client = handle.client('elbv2', region_name=reg)
            response = aws_get_paginator(elb_Client, "describe_load_balancers", "LoadBalancers")
            for lb in response:
                elb_dict = {}
                elb_dict["load_balancer_name"] = lb['LoadBalancerName']
                elb_dict["load_balancer_arn"] = lb['LoadBalancerArn']
                elb_dict["load_balancer_type"] = lb['Type']
                elb_dict["load_balancer_dns"] = lb['DNSName']
                elb_dict["region"] = reg
                result.append(elb_dict)
        except Exception:
            pass
    return result

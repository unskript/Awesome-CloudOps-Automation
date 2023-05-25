##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, List
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        title='Region of the Classic Loadbalancer',
        description='Region of the Classic loadbalancer.'
    )


def aws_list_application_loadbalancers_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_application_loadbalancers(handle, region: str) -> List:
    """aws_list_application_loadbalancers lists application loadbalancers ARNs.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the Classic loadbalancer.

        :rtype: List with all the application loadbalancer ARNs
    """
    result = []
    try:
        ec2Client = handle.client('elbv2', region_name=region)
        resp = aws_get_paginator(ec2Client, "describe_load_balancers", "LoadBalancers")
        for elb in resp:
            if elb['Type'] == "application":
                result.append(elb['LoadBalancerArn'])
    except Exception:
        pass
    return result

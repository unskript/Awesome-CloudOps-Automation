##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, List
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        title='Region of the Classic Loadbalancer',
        description='Region of the Classic loadbalancer.'
    )


def aws_list_apllication_loadbalancers_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_list_apllication_loadbalancers(handle, region: str) -> List:
    """aws_list_apllication_loadbalancers lists application loadbalancers ARNs.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the Classic loadbalancer.

        :rtype: List with all the application loadbalancer ARNs
    """

    ec2Client = handle.client('elbv2', region_name=region)
    resp = ec2Client.describe_load_balancers()
    result = []
    for elb in resp['LoadBalancers']:
        if elb['Type'] == "application":
            result.append(elb['LoadBalancerArn'])
    return result
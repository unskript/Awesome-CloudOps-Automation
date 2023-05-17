##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    elb_name: str = Field(..., description='Name of classic ELB', title='Classic Load Balancer Name')



def aws_delete_classic_load_balancer_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_classic_load_balancer(handle, region: str, elb_name: str) -> Dict:
    """aws_delete_classic_load_balancer reponse of deleting a classic load balancer.

        :type region: string
        :param region: AWS Region.

        :type elb_name: string
        :param elb_name: Classic load balancer name.

        :rtype: dict of deleted load balancers reponse.
    """
    try:
        elblient = handle.client('elb', region_name=region)
        response = elblient.delete_load_balancer(LoadBalancerName=elb_name)
        return response
    except Exception as e:
        raise Exception(e)



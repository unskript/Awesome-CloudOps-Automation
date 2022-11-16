# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Dict
import pprint


class InputSchema(BaseModel):
    elb_name: str = Field(
        title='ELB Name',
        description='Name of the Load Balancer.')
    instance_ids: List[str] = Field(
        title='Instance IDs',
        description='List of instance IDs. For eg. ["i-foo", "i-bar"]')
    region: str = Field(
        title='Region',
        description='AWS Region of the ELB.')


def aws_register_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_register_instances(handle, elb_name: str, instance_ids: List, region: str) -> Dict:
    """aws_register_instances returns dict of register info

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type elb_name: string
     :param elb_name: Name of the Load Balancer.

     :type instance_ids: string
     :param instance_ids: List of instance IDs.

     :type region: string
     :param region: AWS Region of the ELB.

     :rtype: Dict of register info
    """
    elbClient = handle.client('elb', region_name=region)

    res = elbClient.register_instances_with_load_balancer(
        LoadBalancerName=elb_name,
        Instances=[{'InstanceId': instance_id} for instance_id in instance_ids]
    )

    return res

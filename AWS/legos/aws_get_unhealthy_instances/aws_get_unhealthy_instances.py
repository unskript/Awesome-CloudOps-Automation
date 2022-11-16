# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint


class InputSchema(BaseModel):
    elb_name: str = Field(
        title='ELB Name',
        description='Name of the ELB. NOTE: It ONLY supports Classic.')
    region: str = Field(
        title='Region',
        description='Name of the AWS Region'
    )


def aws_get_unhealthy_instances_printer(output):
    if output is None:
        return
    if output == []:
        print("All instances are healthy")
    else:
        pprint.pprint(output)


def aws_get_unhealthy_instances(handle, elb_name: str, region: str) -> List:
    """aws_get_unhealthy_instances returns array of unhealthy instances

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type elb_name: string
     :param elb_name: Name of the ELB. Note: It ONLY supports Classic.

     :type region: string
     :param region: Name of the AWS Region.

     :rtype: Returns array of unhealthy instances
    """

    elbClient = handle.client('elb', region_name=region)
    res = elbClient.describe_instance_health(
        LoadBalancerName=elb_name,
    )

    unhealthy_instances = []
    for instance in res['InstanceStates']:
        if instance['State'] == "OutOfService":
            unhealthy_instances.append(instance)

    return unhealthy_instances

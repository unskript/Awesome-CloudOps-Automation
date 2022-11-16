##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##  @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##
from pydantic import BaseModel, Field
import pandas as pd
from typing import List
import pprint


class InputSchema(BaseModel):
    elb_name: str = Field(
        title='Elastic Load Balancer Name',
        description='Name of the Elastic Load Balancer Name')
    region: str = Field(
        title='Region',
        description='AWS Region of the ECS service')


def aws_get_instances_printer(output):
    
    if output is None:
        return
    df = pd.DataFrame(output)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print("\n")
    print(df)


def aws_get_instances(handle, elb_name: str, region: str) -> List:
    """aws_get_all_instances Get a list of all AWS EC2 Instances from given ELB

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type elb_name: string
     :param elb_name: Name of the Elastic Load Balancer Name

     :type region: string
     :param region: AWS Region of the ECS service.

     :rtype: list of dict with all AWS EC2 Instances from given ELB
    """

    elbClient = handle.client('elb', region_name=region)
    res = elbClient.describe_instance_health(
        LoadBalancerName=elb_name,
    )

    instances = []
    for instance in res['InstanceStates']:
        instances.append(instance)
    
    return instances

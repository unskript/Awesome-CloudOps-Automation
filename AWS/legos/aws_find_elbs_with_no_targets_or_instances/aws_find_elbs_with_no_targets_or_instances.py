##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field('', description='AWS Region.', title='region')



def aws_find_elbs_with_no_targets_or_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_find_elbs_with_no_targets_or_instances(handle, region: str = "")->Tuple:
    """aws_find_elbs_with_no_targets_or_instances Returns details of Elb's with no target groups or instances

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: str
        :param region: AWS Region

        :rtype: Tuple of status, and details of ELB's with no targets or instances
    """
    result = []
    all_load_balancers = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            elbv2Client = handle.client('elbv2', region_name=reg)
            elbv2_response = aws_get_paginator(elbv2Client, "describe_load_balancers", "LoadBalancers")
            elbClient = handle.client('elb', region_name=reg)
            elb_response = elbClient.describe_load_balancers()
            for lb in elbv2_response:
                elb_dict = {}
                elb_dict["load_balancer_name"] = lb['LoadBalancerName']
                elb_dict["load_balancer_arn"] = lb['LoadBalancerArn']
                elb_dict["load_balancer_type"] = lb['Type']
                elb_dict["load_balancer_dns"] = lb['DNSName']
                elb_dict["region"] = reg
                all_load_balancers.append(elb_dict)
            for lb in elb_response['LoadBalancerDescriptions']:
                elb_dict = {}
                elb_dict["load_balancer_name"] = lb['LoadBalancerName']
                elb_dict["load_balancer_type"] = 'classic'
                elb_dict["load_balancer_dns"] = lb['DNSName']
                elb_dict["region"] = reg
                all_load_balancers.append(elb_dict)
        except Exception as e:
            pass
    for load_balancer in all_load_balancers:
        if load_balancer['load_balancer_type']=='network' or load_balancer['load_balancer_type']=='application':
            elbv2Client = handle.client('elbv2', region_name=load_balancer['region'])
            target_groups = elbv2Client.describe_target_groups(
                LoadBalancerArn=load_balancer['load_balancer_arn']
            )
            if len(target_groups['TargetGroups']) == 0:
                    elb_dict = {}
                    elb_dict["elb_arn"] = load_balancer['load_balancer_arn']
                    elb_dict["elb_name"] = load_balancer['load_balancer_name']
                    elb_dict["region"] = load_balancer['region']
                    elb_dict["type"] = load_balancer['load_balancer_type']
                    result.append(elb_dict)
        else:
            elbClient = handle.client('elb', region_name=load_balancer['region'])
            res = elbClient.describe_instance_health(
                LoadBalancerName=load_balancer['load_balancer_name'],
            )
            if len(res['InstanceStates'])==0:
                elb_dict = {}
                elb_dict["elb_name"] = load_balancer['load_balancer_name']
                elb_dict["region"] = load_balancer['region']
                elb_dict["type"] = load_balancer['load_balancer_type']
                result.append(elb_dict)
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)



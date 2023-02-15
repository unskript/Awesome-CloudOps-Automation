##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


class InputSchema(BaseModel):
    elb_name: Optional[str] = Field(
        default="",
        title='ELB Name',
        description='Name of the elastic load balancer.')

    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region of the ELB.')


def aws_get_unhealthy_instances_from_elb_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_get_unhealthy_instances_from_elb(handle, elb_name: str = "", region: str = "") -> Tuple:
    """aws_get_unhealthy_instances_from_elb gives unhealthy instances from ELB

        :type elb_name: string
        :param elb_name: Name of the elastic load balancer.

        :type region: string
        :param region: AWS region.

        :rtype: A tuple with execution results and a list of unhealthy instances from ELB
    """
    
    result = []
    all_regions = [region]
    elb_list = []
    if not region:
        all_regions = aws_list_all_regions(handle)

    if not elb_name:
        for reg in all_regions:
            try:
                asg_client = handle.client('elb', region_name=reg)
                response = aws_get_paginator(asg_client, "describe_load_balancers", "LoadBalancerDescriptions")
                for i in response:
                    elb_dict = {}
                    elb_dict["load_balancer_name"] = i["LoadBalancerName"]
                    elb_dict["region"] = reg
                    elb_list.append(elb_dict)
            except Exception as error:
                pass
            
    if elb_name and not region:
        for reg in all_regions:
            try:
                asg_client = handle.client('elb', region_name=reg)
                response = aws_get_paginator(asg_client, "describe_load_balancers", "LoadBalancerDescriptions")
                for i in response:
                    if elb_name in i["LoadBalancerName"]:
                        elb_dict = {}
                        elb_dict["load_balancer_name"] = i["LoadBalancerName"]
                        elb_dict["region"] = reg
                        elb_list.append(elb_dict)
            except Exception as error:
                pass

    if elb_name and region:
        try:
            elbClient = handle.client('elb', region_name=region)
            res = elbClient.describe_instance_health(LoadBalancerName=elb_name)
            for instance in res['InstanceStates']:
                data_dict = {}
                if instance['State'] == "OutOfService":
                    data_dict["instance_id"] = instance["InstanceId"]
                    data_dict["region"] = reg
                    data_dict["load_balancer_name"] = i["LoadBalancerName"]
                    result.append(data_dict)
        except Exception as e:
            pass

    for elb in elb_list:
        try:
            elbClient = handle.client('elb', region_name=elb["region"])
            res = elbClient.describe_instance_health(LoadBalancerName=elb["load_balancer_name"])
            for instance in res['InstanceStates']:
                data_dict = {}
                if instance['State'] == "OutOfService":
                    data_dict["instance_id"] = instance["InstanceId"]
                    data_dict["region"] = reg
                    data_dict["load_balancer_name"] = i["LoadBalancerName"]
                    result.append(data_dict)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, [])




    

##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


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
    all_regions = [region] if region else aws_list_all_regions(handle)
    elb_list = []

    # Handling the logic when elb_name is not provided
    if not elb_name:
        for reg in all_regions:
            print(reg)
            try:
                asg_client = handle.client('elb', region_name=reg)
                response = aws_get_paginator(asg_client, "describe_load_balancers", "LoadBalancerDescriptions")
                for i in response:
                    elb_list.append({"load_balancer_name": i["LoadBalancerName"], "region": reg})
            except Exception:
                pass

    # Handling the logic when only elb_name is provided
    if elb_name and not region:
        for reg in all_regions:
            try:
                asg_client = handle.client('elb', region_name=reg)
                response = aws_get_paginator(asg_client, "describe_load_balancers", "LoadBalancerDescriptions")
                for i in response:
                    if elb_name in i["LoadBalancerName"]:
                        elb_list.append({"load_balancer_name": i["LoadBalancerName"], "region": reg})
            except Exception:
                pass

    # Handling the logic when both elb_name and region are provided
    if elb_name and region:
        try:
            elbClient = handle.client('elb', region_name=region)
            res = elbClient.describe_instance_health(LoadBalancerName=elb_name)
            for instance in res['InstanceStates']:
                if instance['State'] == "OutOfService":
                    result.append({
                        "instance_id": instance["InstanceId"],
                        "region": region,
                        "load_balancer_name": elb_name
                    })
        except Exception as e:
            raise e

    # Handling the logic when elb_list is populated
    for elb in elb_list:
        try:
            elbClient = handle.client('elb', region_name=elb["region"])
            res = elbClient.describe_instance_health(LoadBalancerName=elb["load_balancer_name"])
            for instance in res['InstanceStates']:
                if instance['State'] == "OutOfService":
                    result.append({
                        "instance_id": instance["InstanceId"],
                        "region": elb["region"],
                        "load_balancer_name": elb["load_balancer_name"]
                    })
        except Exception as e:
            raise e

    return (False, result) if result else (True, None)

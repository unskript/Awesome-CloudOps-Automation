##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='AWS Region of the ASG.')


def aws_filter_unhealthy_instances_from_asg_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_filter_unhealthy_instances_from_asg(handle, region: str = "") -> Tuple:
    """aws_filter_unhealthy_instances_from_asg gives unhealthy instances from ASG

        :type region: string
        :param region: AWS region.

        :rtype: CheckOutput with status result and list of unhealthy instances from ASG.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            asg_client = handle.client('autoscaling', region_name=reg)
            response = aws_get_paginator(
                asg_client,
                "describe_auto_scaling_instances",
                "AutoScalingInstances"
                )

            # filter instances to only include those that are in an "unhealthy" state
            for instance in response:
                data_dict = {}
                if instance['HealthStatus'] == 'Unhealthy':
                    data_dict["InstanceId"] = instance["InstanceId"]
                    data_dict["AutoScalingGroupName"] = instance["AutoScalingGroupName"]
                    data_dict["region"] = reg
                    result.append(data_dict)

        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

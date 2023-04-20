##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='AWS Region',
        description='AWS Region.')


def aws_get_ecs_services_without_autoscaling_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_ecs_services_without_autoscaling(handle, region: str = "") -> Tuple:
    """aws_get_ecs_services_without_autoscaling Returns an array of Sevices.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :rtype: Array of Sevices.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            ecs_Client = handle.client('ecs', region_name=reg)
            autoscaling_client = handle.client('application-autoscaling', region_name=reg)
            response = aws_get_paginator(ecs_Client, "list_clusters", "clusterArns")
            cluster_names = [arn.split('/')[-1] for arn in response]
            for cluster in cluster_names:
                response_1 = aws_get_paginator(ecs_Client, "list_services",
                                               "serviceArns", cluster=cluster)
                for service in response_1:
                    cluster_dict = {}
                    response_2 = autoscaling_client.describe_scaling_policies(
                                    ServiceNamespace='ecs', ResourceId=service)
                    scaling_policies = response_2['ScalingPolicies']
                    if not scaling_policies:
                        cluster_dict["service"] = service
                        cluster_dict["cluster"] = cluster
                        cluster_dict["region"] = reg
                        result.append(cluster_dict)
        except Exception as e:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
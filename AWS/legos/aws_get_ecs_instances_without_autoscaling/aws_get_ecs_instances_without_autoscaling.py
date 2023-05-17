##
##  Copyright (c) 2023 unSkript, Inc
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
        title='AWS Region',
        description='AWS Region.')


def aws_get_ecs_instances_without_autoscaling_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_ecs_instances_without_autoscaling(handle, region: str = "") -> Tuple:
    """aws_get_ecs_instances_without_autoscaling Returns an array of instances.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :rtype: Array of instances.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            ecs_Client = handle.client('ecs', region_name=reg)
            autoscaling_client = handle.client('autoscaling', region_name=reg)
            response = aws_get_paginator(ecs_Client, "list_clusters", "clusterArns")
            cluster_names = [arn.split('/')[-1] for arn in response]
            for cluster in cluster_names:
                response_1 = aws_get_paginator(ecs_Client, "list_container_instances",
                                               "containerInstanceArns", cluster=cluster)
                if not response_1:
                    continue
                container_instances_data = ecs_Client.describe_container_instances(
                    cluster=cluster,
                    containerInstances=response_1
                    )
                for ec2_instance in container_instances_data['containerInstances']:
                    cluster_dict = {}
                    response = autoscaling_client.describe_auto_scaling_instances(
                        InstanceIds=[ec2_instance['ec2InstanceId']]
                        )
                    if response['AutoScalingInstances']:
                        asg_name = response['AutoScalingInstances'][0]['AutoScalingGroupName']
                        asg_response = autoscaling_client.describe_auto_scaling_groups(
                            AutoScalingGroupNames=[asg_name]
                            )
                        if not asg_response['AutoScalingGroups']:
                            cluster_dict["instance_id"] = ec2_instance['ec2InstanceId']
                            cluster_dict["cluster"] = cluster
                            cluster_dict["region"] = reg
                            result.append(cluster_dict)
                    else:
                        cluster_dict["instance_id"] = ec2_instance['ec2InstanceId']
                        cluster_dict["cluster"] = cluster
                        cluster_dict["region"] = reg
                        result.append(cluster_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

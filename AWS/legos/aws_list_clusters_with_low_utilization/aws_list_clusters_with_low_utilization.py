##
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
        description='AWS Region.')
    threshold: Optional[int] = Field(
        default=10,
        title='Threshold (In percent)',
        description='Threshold to check for cpu utilization is less than threshold.')


def aws_list_clusters_with_low_utilization_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_list_clusters_with_low_utilization(handle, region: str = "", threshold: int = 10) -> Tuple:
    """aws_list_clusters_with_low_utilization Returns an array of ecs clusters.

        :type region: string
        :param region: AWS Region.

        :type threshold: int
        :param threshold: (In percent) Threshold to check for cpu utilization
        is less than threshold.

        :rtype: List of clusters for low CPU utilization
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            ecs_Client = handle.client('ecs', region_name=reg)
            response = aws_get_paginator(ecs_Client, "list_clusters", "clusterArns")
            for cluster in response:
                cluster_dict = {}
                cluster_name = cluster.split('/')[1]
                stats = ecs_Client.describe_clusters(clusters=[cluster])['clusters'][0]['statistics']
                for stat in stats:
                    if stat['name'] == 'CPUUtilization':
                        cpu_utilization = int(stat['value'])
                        if cpu_utilization < threshold:
                            cluster_dict["cluster_name"] = cluster_name
                            cluster_dict["region"] = reg
                            result.append(cluster_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)

##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
from datetime import datetime, timedelta
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default='',
        title='AWS Region',
        description='AWS Region.'
    )
    max_idle_time: Optional[int] = Field(
        default=30,
        title='Max Idle Time (minutes)',
        description='The maximum idle time in minutes.'
    )


def aws_get_idle_emr_clusters_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_idle_emr_clusters(handle, max_idle_time: int = 30, region: str = "") -> Tuple:
    """aws_get_idle_emr_clusters Gets list of idle EMR clusters.

        :type region: string
        :param region: AWS Region.

        :type max_idle_time: int
        :param max_idle_time: (minutes) The maximum idle time in minutes.

        :rtype: List of idle EMR clusters.
    """
    result = []
    all_regions = [region] if region else aws_list_all_regions(handle)
    min_last_state_change_time = datetime.now() - timedelta(minutes=max_idle_time)
    for reg in all_regions:
        try:
            emr_Client = handle.client('emr', region_name=reg)
            response = aws_get_paginator(emr_Client, "list_clusters", "Clusters")
            for cluster in response:
                if 'Status' in cluster and 'Timeline' in cluster['Status'] and 'ReadyDateTime' in cluster['Status']['Timeline']:
                    last_state_change_time = cluster['Status']['Timeline']['ReadyDateTime']
                    if last_state_change_time < min_last_state_change_time:
                        cluster_dict = {
                            "cluster_id": cluster['Id'],
                            "region": reg
                        }
                        result.append(cluster_dict)
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
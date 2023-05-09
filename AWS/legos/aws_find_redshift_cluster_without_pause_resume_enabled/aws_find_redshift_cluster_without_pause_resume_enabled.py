##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default='',
        title='Region',
        description='AWS Region.')
    

def aws_find_redshift_cluster_without_pause_resume_enabled_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_redshift_cluster_without_pause_resume_enabled(handle, region: str = "") -> Tuple:
    """aws_find_redshift_cluster_without_pause_resume_enabled Gets all redshift cluster which don't have pause and resume not enabled.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: AWS Region.

        :rtype: Tuple with the status result and a list of all redshift clusters that don't have pause and resume enabled.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            redshift_Client = handle.client('redshift', region_name=reg)
            response = aws_get_paginator(redshift_Client, "describe_clusters", "Clusters")
            for cluster in response:
                cluster_dict = {}
                cluster_name = cluster["ClusterIdentifier"]
                schedule_actions = aws_get_paginator(redshift_Client, "describe_scheduled_actions", "ScheduledActions",Filters=[{'Name': 'cluster-identifier', 'Values': [cluster_name]}])

                if schedule_actions:
                    for actions in schedule_actions:
                        if "ResumeCluster" in actions["TargetAction"].keys() or "PauseCluster" in actions["TargetAction"].keys():
                            pass
                        else:
                            cluster_dict["cluster_name"] = cluster_name
                            cluster_dict["region"] = reg
                            result.append(cluster_dict)
                else:
                    cluster_dict["cluster_name"] = cluster_name
                    cluster_dict["region"] = reg
                    result.append(cluster_dict)
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)

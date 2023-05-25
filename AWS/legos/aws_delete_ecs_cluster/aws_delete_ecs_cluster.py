##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    cluster_name: str = Field(
        ...,
        description='ECS Cluster name that needs to be deleted',
        title='ECS Cluster Name',
    )



def aws_delete_ecs_cluster_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_ecs_cluster(handle, region: str, cluster_name: str) -> Dict:
    """aws_delete_ecs_cluster dict of loadbalancers info.

        :type region: string
        :param region: AWS Region.

        :type cluster_name: string
        :param cluster_name: ECS Cluster name

        :rtype: dict of load balancers info.
    """
    try:
        ec2Client = handle.client('ecs', region_name=region)
        response = ec2Client.delete_cluster(cluster=cluster_name)
        return response
    except Exception as e:
        raise Exception(e)



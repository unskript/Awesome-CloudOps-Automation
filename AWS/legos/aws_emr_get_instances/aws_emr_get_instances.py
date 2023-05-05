##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    cluster_id: str = Field(
        title='Cluster Id',
        description='Cluster ID for the EMR cluster. Eg j-abcd')
    instance_group_type: str = Field(
        title='Instance Group Type',
        description='Group type to filter on. Possible values are MASTER|CORE|TASK'
    )
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_emr_get_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)



def aws_emr_get_instances(
        handle,
        cluster_id: str,
        instance_group_type: str,
        region: str) -> List:

    """aws_get_unhealthy_instances returns array of emr instances

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type cluster_id: string
     :param cluster_id: Cluster ID for the EMR cluster.

     :type instance_group_type: string
     :param instance_group_type: Group type to filter on.

     :type region: string
     :param region: AWS Region of the cluster

     :rtype: Returns array of emr instances
    """
    client = handle.client('emr', region_name=region)
    response = client.list_instances(
        ClusterId=cluster_id,
        InstanceGroupTypes=[instance_group_type],
    )
    if response.get('Instances') is None:
        return []
    return([x.get('Ec2InstanceId') for x in response.get('Instances')])

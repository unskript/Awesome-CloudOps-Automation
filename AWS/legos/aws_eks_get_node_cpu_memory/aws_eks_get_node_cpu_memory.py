##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
import pandas as pd
from typing import Optional, List
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException

from unskript.legos.aws.aws_get_handle.aws_get_handle import Session


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster.')
    nodeName: Optional[str] = Field(
        title='Node Name',
        description='Name of node.')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster.')


def aws_eks_get_node_cpu_memory_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(pd.DataFrame(output))


def aws_eks_get_node_cpu_memory(handle: Session, clusterName: str, region: str, nodeName: str = None) -> List:
    """aws_eks_get_node_cpu_memory returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: ECS Cluster name.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :type nodeName: string
        :param nodeName: Name of Node.

        :rtype: List of nodes with cpu and memory details.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.CoreV1Api(api_client=k8shandle)
    try:
        if nodeName:
            resp = coreApiClient.read_node(nodeName)
            data = [{"node_name": resp.metadata.name, "cpu": int(resp.status.capacity.get("cpu").split("Ki")[0]),
                     "memory": f"{round(int(resp.status.capacity.get('memory').split('Ki')[0]) / 1024, 2)} Mi"}]

        else:
            data = []
            resp = coreApiClient.list_node(pretty=True)
            for node in resp.items:
                data.append({"node_name": node.metadata.name,
                             "cpu": node.status.capacity.get("cpu"),
                             "memory": f"{round(int(node.status.capacity.get('memory').split('Ki')[0]) / 1024, 2)} Mi"})

    except ApiException as e:
        pprint.pprint(str(e))
        data = [
            {'error': 'An Exception occured while executing the command' + e.reason}]
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    return data

# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
# @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##

from pydantic import BaseModel, Field
from kubernetes import client
import datetime
from kubernetes.client.rest import ApiException
from typing import List
from unskript.legos.utils import print_output_in_tabular_format


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_get_nodes_printer(output):
    if output is None:
        return
    print("\n")
    print(print_output_in_tabular_format(output))


def aws_eks_get_nodes(handle, clusterName: str, region: str) -> List:
    """aws_eks_get_nodes returns the list of all eks nodes.

        :type handle: object
        :param handle: Object returned from task.validate(...).
        
        :type clusterName: string
        :param clusterName: Name of the cluster.

        :type region: string
        :param region: AWS Region of the cluster.

        :rtype: List with details of nodes.
    """

    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.CoreV1Api(api_client=k8shandle)

    try:
        resp = coreApiClient.list_node(pretty=True)

    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason
        raise e

    output = []
    for node in resp.items:
        labels = ["%s=%s" % (label, value)
                  for label, value in node.metadata.labels.items()]
        nodeStatus = (node.status.conditions)
        type = ""
        for i in nodeStatus:
            type = i.type

        output.append(
            {"name": node.metadata.name, "status": type,
             "age": "%sd" % (datetime.datetime.now() - node.metadata.creation_timestamp.replace(tzinfo=None)).days,
             "version": node.status.node_info.kubelet_version, "labels": ",".join(labels)})
    return output

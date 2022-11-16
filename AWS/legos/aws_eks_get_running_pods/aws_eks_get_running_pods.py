# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
# @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##

import pprint
from pydantic import BaseModel, Field
from kubernetes import client
from typing import List


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    namespace: str = Field(
        title='Cluster Namespace',
        description='Cluster Namespace')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_get_running_pods_printer(output):
    if output is None:
        return
    print("\n") 
    pprint.pprint(output)


def aws_eks_get_running_pods(handle, clusterName: str, namespace: str, region: str) -> List:
    """aws_eks_get_running_pods returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: List of pods with status ip and start time.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.CoreV1Api(api_client=k8shandle)
    ret = coreApiClient.list_namespaced_pod(namespace=namespace)
    all_healthy_pods = []
    for i in ret.items:
        phase = i.status.phase
        if phase in ("Running", "Succeeded"):
            all_healthy_pods.append(i.metadata.name)
    return all_healthy_pods
